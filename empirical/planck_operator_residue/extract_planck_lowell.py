"""Extract low-ell a_lm coefficients from Planck component-separated maps.

This is the FITS/HEALPix extraction layer for the Planck operator-residue
contract. It requires healpy and actual Planck FITS maps. The metric analyzer
does not require healpy once this CSV has been exported.
"""

from __future__ import annotations

import argparse
import csv
from pathlib import Path

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
            "healpy is required for FITS/HEALPix extraction. Install healpy in "
            "the analysis environment, or export a low-ell coefficient CSV by "
            "another HEALPix-capable tool."
        ) from exc
    return hp


def extract_one(hp, path: Path, lmax: int, field: int, mask: np.ndarray | None):
    sky = hp.read_map(path, field=field, dtype=np.float64, verbose=False)
    sky = hp.remove_dipole(sky, fitval=False, verbose=False)
    if mask is not None:
        if mask.shape != sky.shape:
            raise ValueError(f"mask shape {mask.shape} does not match map {sky.shape}")
        sky = sky * mask
    return hp.map2alm(sky, lmax=lmax, iter=3)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--map-dir", type=Path, required=True)
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("data/derived/planck_operator_residue/planck_lowell_alm.csv"),
    )
    parser.add_argument("--lmax", type=int, default=30)
    parser.add_argument(
        "--field",
        type=int,
        default=0,
        help="FITS field index; 0 is I_STOKES for the Planck PR3 IQU maps.",
    )
    parser.add_argument(
        "--mask",
        type=Path,
        help="Optional HEALPix mask FITS file. Field 0 is thresholded at >0.5.",
    )
    args = parser.parse_args()

    hp = require_healpy()
    mask = None
    if args.mask:
        mask = hp.read_map(args.mask, field=0, dtype=np.float64, verbose=False)
        mask = (mask > 0.5).astype(np.float64)

    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f, fieldnames=["operator", "ell", "m", "alm_real", "alm_imag"]
        )
        writer.writeheader()
        for operator, filename in MAP_FILENAMES.items():
            path = args.map_dir / filename
            if not path.exists():
                raise FileNotFoundError(path)
            alm = extract_one(hp, path, args.lmax, args.field, mask)
            for ell in range(2, args.lmax + 1):
                for m in range(ell + 1):
                    idx = hp.Alm.getidx(args.lmax, ell, m)
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

    print(f"wrote low-ell coefficients: {args.output}")


if __name__ == "__main__":
    main()

