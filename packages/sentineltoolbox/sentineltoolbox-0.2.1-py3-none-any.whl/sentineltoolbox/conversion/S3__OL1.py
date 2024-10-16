from pathlib import Path

from sentineltoolbox.conversion.converter_s03_adf_legacy import convert_adf_safe
from sentineltoolbox.conversion.utils import extract_legacy, gen_static_adf_name

in_path = Path(
    "/mount/internal/work-st/projects/cs-412/2078-dpr/Samples/Auxiliary/SAFE/S3",
)
out_path = Path(
    "/mount/internal/work-st/projects/cs-412/2078-dpr/Samples/Auxiliary/Zarr_new/OL1",
)
tmp_path = Path("/tmp")
_LOG_GENERATING_ADF = "*** Generating ADF "


def generate(adf_type: str) -> None:

    if adf_type == "OLLUT":
        for legacy_adf in ["S3A_OL_1_CLUTAX", "S3B_OL_1_CLUTAX"]:
            safe = extract_legacy(in_path, legacy_adf, tmp_path)
            out_file = gen_static_adf_name(legacy_adf[0:3], adf_type, format="zarr")
            print(_LOG_GENERATING_ADF + out_file)
            out_file = out_path / out_file
            convert_adf_safe(adf_type, safe, out_file)

    if adf_type == "OLINS":
        for legacy_adf in ["S3A_OL_1_INS_AX", "S3B_OL_1_INS_AX"]:
            safe = extract_legacy(in_path, legacy_adf, tmp_path)
            out_file = gen_static_adf_name(legacy_adf[0:3], adf_type, format="zarr")
            print(_LOG_GENERATING_ADF + out_file)
            out_file = out_path / out_file
            convert_adf_safe(adf_type, safe, out_file)

    if adf_type == "OLCAL":
        for legacy_adf in ["S3A_OL_1_CAL_AX", "S3B_OL_1_CAL_AX"]:
            safe = extract_legacy(in_path, legacy_adf, tmp_path)
            out_file = gen_static_adf_name(legacy_adf[0:3], adf_type, format="zarr")
            print(_LOG_GENERATING_ADF + out_file)
            out_file = out_path / out_file
            convert_adf_safe(adf_type, safe, out_file)

    if adf_type == "OLPRG":
        for legacy_adf in [
            "S3A_OL_1_PRG_AX",
            "S3B_OL_1_PRG_AX",
        ]:
            safe = extract_legacy(in_path, legacy_adf, tmp_path)
            out_file = gen_static_adf_name(legacy_adf[0:3], adf_type, format="zarr")
            print(_LOG_GENERATING_ADF + out_file)
            out_file = out_path / out_file
            convert_adf_safe(adf_type, safe, out_file)


if __name__ == "__main__":
    generate("OLLUT")
    generate("OLINS")
    generate("OLCAL")
    generate("OLPRG")
