import json
from collections import OrderedDict
from pathlib import Path, PurePosixPath
from typing import Any

import datatree
import netCDF4 as nc
import numpy as np
import xarray
from dask.array import Array
from datatree import DataTree
from xarray.backends.zarr import DIMENSION_KEY

import sentineltoolbox.api as stb
from sentineltoolbox.api import open_datatree
from sentineltoolbox.conversion.utils import generate_datatree_from_legacy_adf
from sentineltoolbox.models.upath import PathFsspec
from sentineltoolbox.writers.zarr import write_zarr

product_description = stb.load_resource_file("metadata/product_description.json")


# flake8: noqa: E501


class NumpyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(
            obj,
            (
                np.integer,
                np.uint8,
                np.uint16,
                np.uint32,
                np.uint64,
                np.int8,
                np.int16,
                np.int32,
                np.int64,
            ),
        ):
            return int(obj)
        elif isinstance(obj, (np.float32, np.float64, np.float_)):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        return json.JSONEncoder.default(self, obj)


class GenericAuxiliaryConverter:
    baseline_collection = 0

    def __init__(
        self,
        input_paths: list[Path | PathFsspec],
        input_files: list | None = None,
    ) -> None:
        if input_files is None:
            input_files = []
        adf_name = [int(ip.name[-8:-5]) for ip in input_paths]
        if adf_name:
            self.baseline_collection = max(adf_name)
        self.coordinates_variables: list = []

        self.attrs = OrderedDict()

        self.name_mapping: dict = {}  # full path -> out var name
        self.path_mapping: dict = {}  # old full path -> new full path

        self.input_paths = input_paths
        self.input_files = input_files

        # TODO: self.metadata_factory = create_mapping_factory(PRODUCT_METADATA_PATH)

    def iter_variables(self, obj):
        for ds in obj.subtree:
            for k, v in ds.variables.items():
                yield ds.path + "/" + k, v

    def iter_groups(self, obj):
        if isinstance(obj, datatree.DataTree):
            yield from obj.subtree
        else:
            yield obj

    def is_custom_variable(self, variable: xarray.Variable, varpath: str):
        """
        Implement this method to define which variable must be managed manually.
        If variable must be managed manually, this method must return True else False.
        By default, always return False
        """
        return False

    def manage_custom_variable(self, out_product, variable: xarray.Variable, varpath: str):
        pass

    def out_varname(self, dt: DataTree[Any], path: str):
        varname = PurePosixPath(path).name
        return self.name_mapping.get(varname, varname.lower())

    def out_varpath(self, dt: DataTree[Any], path: str):
        var_name = self.out_varname(dt, path)
        parts = path.split("/")
        parts[-1] = var_name
        default_path = "/".join(parts).lower()
        variable = dt[path]

        is_coordinate = len(variable.dims) == 1 and variable.path[1:] == variable.dims[0]
        if var_name in self.coordinates_variables or is_coordinate:
            var_path = f"/coordinates{default_path}"
        else:
            var_path = f"/maps{default_path}"

        return self.path_mapping.get(variable.path, var_path)


class AuxiliaryConverterJSON(GenericAuxiliaryConverter):
    def out_varpath(self, dt: DataTree[Any], path: str):
        var_name = self.out_varname(dt, path)
        parts = path.split("/")
        parts[-1] = var_name
        default_path = "/".join(parts).lower()
        variable = dt[path]

        is_coordinate = len(variable.dims) == 1 and path[1:] == variable.dims[0]
        if var_name in self.coordinates_variables or is_coordinate:
            var_path = f"/coordinates{default_path}"
        else:
            var_path = default_path

        return self.path_mapping.get(path, var_path.lower())

    def generate(self):
        json_data = {}
        self.update(json_data, self.input_paths)
        return json_data

    def _dict_tree(self, root: dict, path: str) -> dict:
        dic = root
        for part in path.split("/")[:-1]:
            if not part:
                continue
            if part not in dic:
                dic[part] = {}
            dic = dic[part]
        return dic

    def manage_generic_variable(self, out_product: dict, dt: DataTree[Any], path: str):
        var_name = self.out_varname(dt, path)
        var_path = self.out_varpath(dt, path)
        variable = dt[path]

        if var_name != DIMENSION_KEY and var_name != "coordinates":
            # EXTRACT SCALARS
            if len(variable.dims) == 0:
                # out.attrs[var_name] = {k: v for k, v in variable.attrs.items() if k != "_io_config"}
                dic = out_product
                dtype = variable.data.dtype
                value = variable.data.item()
                dic = self._dict_tree(dic, var_path)
                dic[var_name] = {k: v for k, v in variable.attrs.items() if k != "_io_config"}
                dic[var_name]["value"] = value
                dic[var_name]["type"] = str(dtype)
                io = variable.attrs.get("_io_config", {})
                dic[var_name].update({k: str(v) for k, v in io.items()})
            # COPY VARIABLES
            else:
                group = self._dict_tree(out_product, var_path)
                variable_json = group.setdefault(var_name, {})
                if isinstance(variable.data, Array):
                    lst = variable.data.compute().tolist()
                else:
                    lst = variable.data.tolist()
                variable_json["value"] = lst
                variable_json["type"] = f"array[{variable.data.dtype}]"
                variable_json.update(
                    {k: v for k, v in variable.attrs.items() if k != "_io_config"},
                )
                io = variable.attrs.get("_io_config", {})
                variable_json.update({k: str(v) for k, v in io.items()})
                # out_product.add_variable(out_path, variable)

    def update(self, out_product, input_paths):
        for input_path in input_paths:
            # for nc_file in input_path.glob("*.nc"):
            for nc_file in [i for i in input_path.iterdir() if i.suffix in [".nc", ".nc4"]]:
                if self.input_files and not nc_file.name in self.input_files:
                    continue
                legacy = open_datatree(nc_file)
                for varpath, variable in self.iter_variables(legacy):
                    if self.is_custom_variable(legacy, varpath):
                        self.manage_custom_variable(out_product, legacy, varpath)
                    else:
                        self.manage_generic_variable(out_product, legacy, varpath)
        out_product.update(self.attrs)


def convert_adf_json(adf_type: str, input_path: Path) -> dict[Any, Any]:

    converter = AuxiliaryConverterJSON([input_path])
    data = converter.generate()

    title = product_description.get(adf_type, adf_type)
    attrs = stb.AttributeHandler(data)
    attrs.set_attr("product:type", adf_type)
    attrs.set_attr("title", title)

    """
    output_path = output_path.replace(".zarr", ".json")
    with open(output_path, "w") as json_file:
        json.dump(data, json_file, indent=2, cls=NumpyEncoder)

    return output_path
    """
    return data


def convert_adf_safe(adf_type: str, input_path: PathFsspec) -> DataTree[Any]:
    xdt: DataTree[Any] = datatree.DataTree(name="root")
    if adf_type == "OLLUT":
        for ncgroup in ["bright_reflectance", "sun_glint_risk"]:
            xdt = generate_datatree_from_legacy_adf(
                input_path,
                ncgroup=ncgroup,
                dt=xdt,
            )

    elif adf_type == "OLINS":
        nc_ds = nc.Dataset(input_path / "OL_1_INS_AX.nc")
        ncgroups = nc_ds.groups.keys()
        for ncgroup in ncgroups:
            xdt = generate_datatree_from_legacy_adf(
                input_path,
                ncgroup=ncgroup,
                dt=xdt,
            )
        xdt.attrs.update({attr: nc_ds.getncattr(attr) for attr in nc_ds.ncattrs()})

    elif adf_type == "OLCAL":
        nc_ds = nc.Dataset(input_path / "OL_1_CAL_AX.nc")
        ncgroups = nc_ds.groups.keys()
        for ncgroup in ncgroups:
            xdt = generate_datatree_from_legacy_adf(
                input_path,
                ncgroup=ncgroup,
                dt=xdt,
            )
        xdt.attrs.update({attr: nc_ds.getncattr(attr) for attr in nc_ds.ncattrs()})

    elif adf_type == "OLPRG":
        nc_ds = nc.Dataset(input_path / "OL_1_PRG_AX.nc")
        ncgroups = nc_ds.groups.keys()
        for ncgroup in ncgroups:
            xdt = generate_datatree_from_legacy_adf(
                input_path,
                ncgroup=ncgroup,
                dt=xdt,
            )
        xdt.attrs.update({attr: nc_ds.getncattr(attr) for attr in nc_ds.ncattrs()})

    elif adf_type == "OLPPP":
        xdt = generate_datatree_from_legacy_adf(
            input_path,
            safe_file=["OL_2_PPP_AX.nc"],
            dt=xdt,
        )
        for ncgroup in ["classification_1", "gas_correction", "classification_2"]:
            xdt = generate_datatree_from_legacy_adf(
                input_path,
                ncgroup=ncgroup,
                dt=xdt,
            )

    elif adf_type == "OLACP":

        for ncgroup in [
            "glint_whitecaps",
            "bright_waters_NIR",
            "standard_AC",
            "alternate_AC",
        ]:
            xdt = generate_datatree_from_legacy_adf(
                input_path,
                ncgroup=ncgroup,
                dt=xdt,
            )

    elif adf_type == "OLWVP":
        xdt = generate_datatree_from_legacy_adf(
            input_path,
            group="",
        )

    elif adf_type == "OLOCP":
        xdt = generate_datatree_from_legacy_adf(
            input_path,
            dt=xdt,
        )
        for ncgroup in [
            "rhow_norm_nn",
        ]:
            xdt = generate_datatree_from_legacy_adf(
                input_path,
                ncgroup=ncgroup,
                dt=xdt,
            )

    elif adf_type == "OLVGP":
        xdt = generate_datatree_from_legacy_adf(
            input_path,
            group="",
        )

    elif adf_type == "OLCLP":
        xdt = generate_datatree_from_legacy_adf(
            input_path,
            group="",
        )
    else:
        raise NotImplementedError(f"{input_path.name}: ADF type {adf_type} is not supported")

    title = product_description.get(adf_type, adf_type)
    attrs = stb.AttributeHandler(xdt)
    attrs.set_attr("product:type", adf_type)
    attrs.set_attr("title", title)
    attrs.set_attr("processing:version", input_path.name[-8:-5])
    return xdt


def convert_adf(
    upath_input: PathFsspec,
    semantic_mapping: dict[Any, Any] | None = None,
    **kwargs: Any,
) -> DataTree[Any] | dict[str, Any]:
    if semantic_mapping is None:
        semantic_mapping = {}

    fgen, fgen_data = stb.filename_generator(upath_input.name, semantic_mapping=semantic_mapping)

    if fgen.semantic in CONVERTERS_ADFS_S3_LEGACY:
        data = CONVERTERS_ADFS_S3_LEGACY[fgen.semantic](
            fgen.semantic,
            upath_input,
        )
        return data
    else:
        raise NotImplementedError


def convert_and_merge_adf(adf_type: str, input_paths: list[Path], output_path: str) -> None:
    # TODO: support s3 buckets
    dt = datatree.DataTree(name="root_adf")
    if adf_type == "VSWCD":
        for input_path in input_paths:
            input_name = input_path.name
            group = input_name[9:13].lower()
            dt = generate_datatree_from_legacy_adf(
                input_path,
                coordinates_variable={  # variable : (dimention,coordinate)
                    "cal_uncertainty_uncertainty": (
                        "uncertainty_lut",
                        "cal_uncertainty_radiance",
                    ),
                    "non_linearities": ("lut", "detectors_count"),
                    "coffsets": ("channels", "voffsets"),
                },
                group=group,
                dt=dt,
            )
    else:
        return

    title = product_description.get(adf_type, adf_type)
    attrs = stb.AttributeHandler(dt)
    attrs.set_attr("product:type", adf_type)
    attrs.set_attr("title", title)
    attrs.set_attr("processing:version", input_path.name[-8:-5])
    write_zarr(dt, output_path)


CONVERTERS_ADFS_S3_LEGACY = {
    "OLINS": convert_adf_safe,
    "OLLUT": convert_adf_safe,
    "OLCAL": convert_adf_safe,
    "OLPRG": convert_adf_safe,
    "OLPPP": convert_adf_safe,
    "OLACP": convert_adf_safe,
    "OLWVP": convert_adf_safe,
    "OLOCP": convert_adf_safe,
    "OLVGP": convert_adf_safe,
    "OLCLP": convert_adf_safe,
    "OLEOP": convert_adf_json,
    "OLRAC": convert_adf_json,
    "OLSPC": convert_adf_json,
}
