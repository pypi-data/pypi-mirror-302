from pathlib import Path

from sentineltoolbox.conversion.converter_s03_adf_legacy import convert_adf_safe
from sentineltoolbox.conversion.utils import extract_legacy, gen_static_adf_name

in_path = Path(
    "/mount/internal/work-st/projects/cs-412/2078-dpr/Samples/Auxiliary/SAFE/S3",
)
out_path = Path(
    "/mount/internal/work-st/projects/cs-412/2078-dpr/Samples/Auxiliary/Zarr_new/OL2",
)
tmp_path = Path("/tmp")
_LOG_GENERATING_ADF = "*** Generating ADF "


def generate(adf_type: str) -> None:

    if adf_type == "OLPPP":
        for legacy_adf in ["S3A_OL_2_PPP_AX", "S3B_OL_2_PPP_AX"]:
            safe = extract_legacy(in_path, legacy_adf, tmp_path)
            out_file = gen_static_adf_name(legacy_adf[0:3], adf_type, format="zarr")
            print(_LOG_GENERATING_ADF + out_file)
            out_file = out_path / out_file
            convert_adf_safe(adf_type, safe, out_file)

    if adf_type == "OLACP":
        for legacy_adf in ["S3A_OL_2_ACP_AX", "S3B_OL_2_ACP_AX"]:
            safe = extract_legacy(in_path, legacy_adf, tmp_path)
            out_file = gen_static_adf_name(legacy_adf[0:3], adf_type, format="zarr")
            print(_LOG_GENERATING_ADF + out_file)
            out_file = out_path / out_file
            convert_adf_safe(adf_type, safe, out_file)

    if adf_type == "OLWVP":
        for legacy_adf in ["S3A_OL_2_WVP_AX", "S3B_OL_2_WVP_AX"]:
            safe = extract_legacy(in_path, legacy_adf, tmp_path)
            out_file = gen_static_adf_name(legacy_adf[0:3], adf_type, format="zarr")
            print(_LOG_GENERATING_ADF + out_file)
            out_file = out_path / out_file
            convert_adf_safe(adf_type, safe, out_file)

    if adf_type == "OLOCP":
        for legacy_adf in [
            "S3A_OL_2_OCP_AX",
            "S3B_OL_2_OCP_AX",
        ]:
            safe = extract_legacy(in_path, legacy_adf, tmp_path)
            out_file = gen_static_adf_name(legacy_adf[0:3], adf_type, format="zarr")
            print(_LOG_GENERATING_ADF + out_file)
            out_file = out_path / out_file
            convert_adf_safe(adf_type, safe, out_file)

    if adf_type == "OLVGP":
        for legacy_adf in [
            "S3A_OL_2_VGP_AX",
            "S3B_OL_2_VGP_AX",
        ]:
            safe = extract_legacy(in_path, legacy_adf, tmp_path)
            out_file = gen_static_adf_name(legacy_adf[0:3], adf_type, format="zarr")
            print(_LOG_GENERATING_ADF + out_file)
            out_file = out_path / out_file
            convert_adf_safe(adf_type, safe, out_file)
    if adf_type == "OLCLP":
        for legacy_adf in [
            "S3A_OL_2_CLP_AX",
            "S3B_OL_2_CLP_AX",
        ]:
            safe = extract_legacy(in_path, legacy_adf, tmp_path)
            out_file = gen_static_adf_name(legacy_adf[0:3], adf_type, format="zarr")
            print(_LOG_GENERATING_ADF + out_file)
            out_file = out_path / out_file
            convert_adf_safe(adf_type, safe, out_file)


if __name__ == "__main__":
    generate("OLPPP")
    generate("OLACP")
    generate("OLWVP")
    generate("OLOCP")
    generate("OLVGP")
    generate("OLCLP")
