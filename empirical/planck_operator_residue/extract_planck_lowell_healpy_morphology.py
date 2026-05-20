"""Cloud/Linux healpy extraction for official-mask morphology states.

This script is meant for the Episode 4 operator-prism contract gate. It reads
the Planck component-separated FITS maps, downgrades them to the declared
low-ell analysis resolution, applies the official common-mask base/dilate1
states at that same resolution, and writes coefficient CSVs suitable for the
existing directional-axis analyzers.

It intentionally does not evaluate the theory contract. It only creates the
missing observed coefficient tables.
"""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Any

import numpy as np


MAP_FILENAMES = {
    "Commander": "COM_CMB_IQU-commander_2048_R3.00_full.fits",
    "NILC": "COM_CMB_IQU-nilc_2048_R3.00_full.fits",
    "SEVEM": "COM_CMB_IQU-sevem_2048_R3.00_full.fits",
    "SMICA": "COM_CMB_IQU-smica_2048_R3.00_full.fits",
}


def require_healpy():
    try:
        import healpy as hp  # type: ignore
    except ImportError as exc:
        raise SystemExit(
            "healpy is required. Run this in Linux/macOS, Colab, Codespaces, "
            "or WSL with `python -m pip install -r cloud_run/planck_operator_prism/requirements.txt`."
        ) from exc
    return hp


def read_map_low(hp: Any, path: Path, field: int, nside_out: int) -> np.ndarray:
    sky = hp.read_map(path, field=field, dtype=np.float64, verbose=False)
    sky = hp.remove_dipole(sky, fitval=False, verbose=False)
    nside_in = hp.get_nside(sky)
    if nside_in != nside_out:
        sky = hp.ud_grade(sky, nside_out=nside_out, order_in="RING", order_out="RING")
    return np.asarray(sky, dtype=np.float64)


def conservative_downgrade_mask(hp: Any, mask: np.ndarray, nside_out: int) -> np.ndarray:
    nside_in = hp.get_nside(mask)
    binary = (mask > 0.5).astype(np.float64)
    if nside_in == nside_out:
        return binary
    degraded = hp.ud_grade(
        binary, nside_out=nside_out, order_in="RING", order_out="RING"
    )
    return (degraded >= 1.0).astype(np.float64)


def dilate_one(hp: Any, mask: np.ndarray) -> np.ndarray:
    nside = hp.get_nside(mask)
    pix = np.arange(mask.size, dtype=np.int64)
    neighbours = hp.get_all_neighbours(nside, pix)
    out = mask.copy()
    for row in neighbours:
        valid = row >= 0
        out[pix[valid]] = np.maximum(out[pix[valid]], mask[row[valid]])
    return (out > 0.5).astype(np.float64)


def write_alm_csv(
    hp: Any,
    output: Path,
    low_maps: dict[str, np.ndarray],
    mask: np.ndarray,
    lmax: int,
) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle, fieldnames=["operator", "ell", "m", "alm_real", "alm_imag"]
        )
        writer.writeheader()
        for operator, sky in low_maps.items():
            masked = sky * mask
            alm = hp.map2alm(masked, lmax=lmax, iter=3)
            for ell in range(2, lmax + 1):
                for m in range(ell + 1):
                    idx = hp.Alm.getidx(lmax, ell, m)
                    z = alm[idx]
                    writer.writerow(
                        {
                            "operator": operator,
                            "ell": ell,
                            "m": m,
                            "alm_real": float(np.real(z)),
                            "alm_imag": float(np.imag(z)),
                        }
                    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--map-dir", type=Path, required=True)
    parser.add_argument("--mask", type=Path, required=True)
    parser.add_argument("--out-dir", type=Path, required=True)
    parser.add_argument("--nside-out", type=int, default=64)
    parser.add_argument("--lmax", type=int, default=30)
    parser.add_argument("--field", type=int, default=0)
    parser.add_argument(
        "--mask-label",
        action="append",
        choices=["base", "dilate1"],
        default=None,
        help="Mask label to emit. Defaults to base and dilate1.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    hp = require_healpy()
    labels = args.mask_label or ["base", "dilate1"]
    args.out_dir.mkdir(parents=True, exist_ok=True)

    raw_mask = hp.read_map(args.mask, field=0, dtype=np.float64, verbose=False)
    base_mask = conservative_downgrade_mask(hp, raw_mask, args.nside_out)
    masks = {"base": base_mask}
    if "dilate1" in labels:
        masks["dilate1"] = dilate_one(hp, base_mask)

    low_maps = {}
    for operator, filename in MAP_FILENAMES.items():
        path = args.map_dir / filename
        if not path.exists():
            raise FileNotFoundError(path)
        low_maps[operator] = read_map_low(hp, path, args.field, args.nside_out)

    manifest = {
        "status": "healpy official-mask morphology low-ell extraction",
        "map_dir": str(args.map_dir),
        "mask": str(args.mask),
        "nside_out": args.nside_out,
        "lmax": args.lmax,
        "field": args.field,
        "mask_labels": labels,
        "outputs": {},
    }

    for label in labels:
        output = args.out_dir / f"planck_lowell_healpy_official_mask_{label}.csv"
        write_alm_csv(hp, output, low_maps, masks[label], args.lmax)
        manifest["outputs"][label] = {
            "coefficient_csv": str(output),
            "f_sky": float(np.mean(masks[label] > 0.5)),
        }

    manifest_path = args.out_dir / "planck_lowell_healpy_official_mask_manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"manifest": str(manifest_path), "outputs": manifest["outputs"]}, indent=2))


if __name__ == "__main__":
    main()
