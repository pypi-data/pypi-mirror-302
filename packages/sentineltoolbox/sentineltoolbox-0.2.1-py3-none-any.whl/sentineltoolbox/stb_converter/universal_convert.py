import hashlib
import json
import logging
from pathlib import Path, PurePosixPath
from typing import Any, Generator

from datatree import DataTree
from eopf import EOSafeStore, EOZarrStore, OpeningMode

from sentineltoolbox.conversion.convert import product_converter
from sentineltoolbox.conversion.converter_s03_adf_legacy import (
    CONVERTERS_ADFS_S3_LEGACY,
    NumpyEncoder,
    convert_adf,
    convert_and_merge_adf,
)
from sentineltoolbox.exceptions import DataSemanticConversionError
from sentineltoolbox.filesystem_utils import get_universal_path
from sentineltoolbox.models.filename_generator import filename_generator
from sentineltoolbox.models.upath import PathFsspec
from sentineltoolbox.writers.zarr import write_zarr

logger = logging.getLogger("stb_convert_products")
custom_converters = {}
custom_converters.update(CONVERTERS_ADFS_S3_LEGACY)


def convert_product_with_eopf_mapping(input_path: PathFsspec, output_path: str) -> None:
    p = PurePosixPath(output_path)
    zarr_store = EOZarrStore(url=p.parent.as_posix()).open(mode=OpeningMode.CREATE_OVERWRITE)
    store = EOSafeStore(input_path.url, storage_options=input_path.fs.storage_options).open()
    eoproduct = store.load()
    zarr_store[p.name] = eoproduct


def iter_legacy_products(
    inputs: list[str | Path],
    input_dir: PathFsspec | None = None,
    **kwargs: Any,
) -> Generator[PathFsspec, None, None]:
    recursive = kwargs.get("recursive", False)
    if inputs:
        for path in inputs:
            upath = get_universal_path(path, autofix_args=True)
            if upath.exists():
                yield upath
            else:
                logger.critical(f"{upath.url} doesn't exist")
    elif input_dir is not None:
        if recursive:
            for inp in input_dir.rglob("*.SEN3"):
                yield inp
            for inp in input_dir.rglob("*.SAFE"):
                yield inp
        else:
            for inp in input_dir.glob("*.SEN3"):
                yield inp
            for inp in input_dir.glob("*.SAFE"):
                yield inp
    else:
        pass


def _pretty_relpath(upath_input_product: PathFsspec, rel_input_path: str) -> str:
    relpath = rel_input_path + "/" if rel_input_path else ""
    return f"{relpath}{upath_input_product.name}"


def convert_sentinel_products(
    explicit_user_inputs: list[str | Path],
    input_dir: str | None = None,
    output_dir: str | None = None,
    dry_run: bool = False,
    force_hash: int | None = None,
    force_creation_date: str | None = None,
    user_map: dict[str, str] | None = None,
    recursive: bool = False,
    zip: bool = False,
    converter_args: dict[str, Any] | None = None,
    **kwargs: Any,
) -> None:
    if converter_args is None:
        converter_args = {}

    open_datatree_kwargs: dict[Any, Any] = {"autofix_args": True}

    # if user pass explicit inputs (for example xxx1.SEN3 xxx2.SEN3) force input_dir to None
    if explicit_user_inputs:
        input_dir = None

    # if user pass input directory (for example "LEGACY_PRODUCTS/")
    # generate universal path
    if input_dir is not None:
        upath_input_dir = get_universal_path(input_dir, autofix_args=True)
    else:
        upath_input_dir = None

    # if input_dir, iter on it to find all legacy products
    # if explicit inputs, convert it to universal paths
    upath_inputs = iter_legacy_products(explicit_user_inputs, upath_input_dir, recursive=recursive)

    if dry_run:
        logger.info("Conversion PLANNED")

    if user_map is None:
        user_map = {}

    # Check and fix output dir
    if output_dir and output_dir.startswith("s3://"):
        raise NotImplementedError("Cannot convert directly to s3 bucket. Please use local output dir")

    if output_dir is None:
        output_dir_upath = get_universal_path("")
    else:
        output_dir_upath = get_universal_path(output_dir)

    # Generate a dict with all output products that will be generated.
    # key: tuple(output path, relpath).
    #   - output path: the output path (universal path) to generate
    #   - relpath: the path relative to input dir (if --input-dir is used, else "")
    # value: [list of universal_input_path]
    # it is a list because for some ADFS we need to merge multiple ADFS in one
    out_in_dict: dict[tuple[PathFsspec, str], list[PathFsspec]] = {}
    for upath_input_product in upath_inputs:
        input_name = upath_input_product.name
        try:
            logger.debug(f"read {upath_input_product}")
            fgen, fgen_data = filename_generator(input_name, semantic_mapping=user_map)
            if fgen_data["fmt"].startswith("adf"):
                output_name = fgen.to_string(creation_date=force_creation_date)
            elif fgen_data["fmt"].startswith("product"):
                creation_date = fgen_data.get("creation_date", "00010101T000000")
                if force_hash is None:
                    hash = int(hashlib.md5(creation_date.encode("ASCII")).hexdigest()[:3], 16)  # nosec
                else:
                    hash = force_hash
                output_name = fgen.to_string(hash=hash)
            else:
                raise NotImplementedError(f"Product {input_name} of type {fgen_data['fmt']} is not supported")
        except DataSemanticConversionError:
            logger.critical(
                f"Unknown DPR type for {input_name[:15]} Please specify product_type mapping "
                "with -m/--map OLD NEW. For example: -m OL_0_XYZ___ OLCXYZ",
            )
            continue
        except NotImplementedError:
            logger.critical(f"Semantic {input_name!r} is not recognized")
            continue

        # Generate path relative to input dir. Idea is to keep tree inside input_dir and avoid to have all converted
        # product in same directory
        # For example if user pass input_dir == DATA/PRODUCTS and a product DATA/PRODUCTS/OLCI/xxxx.SEN3 is found
        # rel_input_path will be "OLCI/xxxx.SEN3".
        if upath_input_dir is not None:
            rel_input_path = upath_input_product.url.replace(upath_input_dir.url + "/", "")
        else:
            rel_input_path = input_name

        # Keep only path to directory containing legacy product
        # "OLCI/xxxx.SEN3" -> "OLCI"
        # "xxxx.SEN3" -> ""
        rel_input_parent = "/".join(rel_input_path.split("/")[:-1])

        # Generate output path, keeping relative tree
        upath_local_output_dir = output_dir_upath / rel_input_parent
        upath_output = upath_local_output_dir / output_name

        out_in_dict.setdefault((upath_output, rel_input_parent), []).append(upath_input_product)

        del input_name, rel_input_parent, upath_local_output_dir, upath_output

    for outputs, input_paths in out_in_dict.items():
        upath_output, rel_input_path = outputs
        if len(input_paths) == 1:
            upath_input_product = input_paths[0]
            rel_input_parent = "/".join(rel_input_path.split("/")[:-1])
            upath_local_output_dir = output_dir_upath / rel_input_parent

            fgen, fgen_data = filename_generator(upath_input_product.name, semantic_mapping=user_map)

            rel_input_path_str = _pretty_relpath(upath_input_product, rel_input_path)
            if dry_run:

                if fgen.semantic in custom_converters:
                    logger.info("[dry-run] convert (sentineltoolbox/adf)")
                    logger.info(f"[dry-run]   - {rel_input_path_str}")
                    logger.info(f"[dry-run]   ---> {upath_output}")
                else:
                    logger.info("[dry-run] convert (sentineltoolbox or cpm)")
                    logger.info(f"[dry-run]   - {rel_input_path_str}")
                    logger.info(f"[dry-run]   ---> {upath_output}")
            else:
                if not upath_local_output_dir.exists():
                    upath_local_output_dir.mkdir(parents=True, exist_ok=True)

                if fgen.semantic in custom_converters:
                    output_path = upath_output.path
                    try:
                        # TODO: support upath, then remove uncompress=True and cache=True
                        data = convert_adf(
                            upath_input_product,
                            semantic_mapping=user_map,
                            **converter_args.get(fgen.semantic, {}),
                        )
                        if isinstance(data, DataTree):
                            write_zarr(data, upath_output)
                        elif isinstance(data, dict):
                            output_path = output_path.replace(".zarr", ".json")
                            with open(output_path, "w") as json_file:
                                json.dump(data, json_file, indent=2, cls=NumpyEncoder)
                        else:
                            logger.critical(
                                "[sentineltoolbox/adf] ERROR during conversion of "
                                f"{rel_input_path_str!r} to {upath_output}",
                            )
                    except ValueError as err:
                        logger.critical(
                            "[sentineltoolbox/adf] ERROR during conversion of "
                            f"{rel_input_path_str!r} to {upath_output}",
                        )
                        logger.exception(err)
                    else:
                        relpath = Path(output_path).relative_to(output_dir_upath.path)
                        logger.info(f"[sentineltoolbox/adf] convert {rel_input_path_str!r} to {relpath}")
                else:
                    try:
                        logger.info(
                            f"[sentineltoolbox/product] convert {rel_input_path_str!r} to {upath_output} in progress",
                        )
                        _open_datatree_kwargs: dict[str, Any] = {}
                        _open_datatree_kwargs.update(converter_args.get(fgen.semantic, {}))
                        _open_datatree_kwargs.update(open_datatree_kwargs)
                        product_converter(upath_input_product, upath_output.path, zip=zip, **_open_datatree_kwargs)
                    except KeyError:
                        try:
                            convert_product_with_eopf_mapping(upath_input_product, upath_output.path)
                        except:  # noqa: E722
                            logger.critical(f"CANNOT convert {rel_input_path_str!r} to {upath_output}")
                        else:
                            logger.info(f"[eopf] convert {rel_input_path_str!r} to {upath_output}")
                    else:
                        logger.info(f"[sentineltoolbox/product] {upath_output} written!")

        else:
            if dry_run:
                logger.info("[dry-run] convert and merge (sentineltoolbox)")
                for upath_input_product in sorted(input_paths, key=lambda obj: obj.path):
                    rel_input_path_str = _pretty_relpath(upath_input_product, rel_input_path)
                    logger.info(f"[dry-run]  - {rel_input_path_str!r}")
                logger.info(f"[dry-run]   ---> {upath_output}")
            else:
                logger.info("[dry-run] convert and merge (sentineltoolbox)")
                fgen, fgen_data = filename_generator(input_paths[0].name, semantic_mapping=user_map)
                convert_and_merge_adf(
                    fgen.semantic,
                    [Path(input_path.path) for input_path in input_paths],
                    upath_output.path,
                )
