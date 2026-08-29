"""Mask-aware fallback extractor for low-ell operator residue.

Extends extract_planck_lowell_fallback with an optional mask. Two sources:

```text
--mask-fits PATH       external HEALPix mask FITS (first column, threshold >0.5)
--galactic-cut DEG     synthetic mask zeroing |b| < DEG in galactic latitude
```

When both are provided, the intersection of unmasked regions is used. Masked
pixels are set to NaN before passing to the existing direct-quadrature alm
solver, which already skips NaN pixels and renormalizes the integration to
the unmasked area.

This is a coefficient-level extraction. It does NOT perform pseudo-Cl mode
decoupling. Both observed and phase-shuffled null operate on the same
masked-pseudo-alms so the operator-residue distance is a self-consistent
control statistic.
"""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

import numpy as np
from astropy.io import fits
from astropy_healpix import HEALPix

from extract_planck_lowell_fallback import (
    MAP_FILENAMES,
    compute_alm_direct,
    downgrade_mean,
    read_map_column,
)


def synthetic_galactic_mask(nside: int, b_cut_deg: float) -> np.ndarray:
    """Binary mask in galactic frame: 1 if |b| > b_cut_deg else 0."""
    hp = HEALPix(nside=nside, order="ring", frame="galactic")
    pix = np.arange(12 * nside * nside, dtype=np.int64)
    _, lat = hp.healpix_to_lonlat(pix)
    return (np.abs(lat.to_value("deg")) > b_cut_deg).astype(np.float64)


def read_mask_fits(path: Path) -> tuple[np.ndarray, str, int]:
    with fits.open(path, memmap=True) as hdul:
        data = hdul[1].data
        header = hdul[1].header
        ordering = str(header.get("ORDERING", "RING")).lower()
        col = data.columns.names[0]
        values = np.asarray(data[col], dtype=np.float64)
        nside = int(header.get("NSIDE", round((values.size / 12) ** 0.5)))
    return values, ordering, nside


def downgrade_mask_conservative(
    values: np.ndarray,
    nside_in: int,
    order_in: str,
    nside_out: int,
    chunk_size: int,
) -> np.ndarray:
    """Downgrade a binary mask conservatively. An output pixel is 1 only if
    every contributing input pixel is 1."""
    hp_in = HEALPix(nside=nside_in, order=order_in, frame=None)
    hp_out = HEALPix(nside=nside_out, order="ring", frame=None)
    npix_in = values.size
    npix_out = 12 * nside_out * nside_out
    out = np.ones(npix_out, dtype=np.float64)
    for start in range(0, npix_in, chunk_size):
        stop = min(start + chunk_size, npix_in)
        pix = np.arange(start, stop, dtype=np.int64)
        lon, lat = hp_in.healpix_to_lonlat(pix)
        out_pix = hp_out.lonlat_to_healpix(lon, lat)
        chunk = (values[start:stop] > 0.5).astype(np.float64)
        np.minimum.at(out, out_pix, chunk)
    return out


def build_mask(args: argparse.Namespace) -> tuple[np.ndarray, list[str]]:
    npix = 12 * args.nside_out * args.nside_out
    mask = np.ones(npix, dtype=np.float64)
    sources: list[str] = []
    if args.mask_fits is not None:
        mvals, mord, mnside = read_mask_fits(args.mask_fits)
        ext_mask = downgrade_mask_conservative(
            mvals, mnside, mord, args.nside_out, args.chunk_size
        )
        mask = mask * ext_mask
        sources.append(f"fits:{args.mask_fits}")
    if args.galactic_cut is not None:
        gal_mask = synthetic_galactic_mask(args.nside_out, args.galactic_cut)
        mask = mask * gal_mask
        sources.append(f"synthetic_galactic_|b|>{args.galactic_cut}deg")
    return mask, sources


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--map-dir", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--manifest", type=Path, default=None)
    parser.add_argument("--lmax", type=int, default=30)
    parser.add_argument("--nside-out", type=int, default=64)
    parser.add_argument("--column", default="I_STOKES")
    parser.add_argument("--chunk-size", type=int, default=1_000_000)
    parser.add_argument(
        "--mask-fits",
        type=Path,
        default=None,
        help="External HEALPix mask FITS (first column, threshold >0.5).",
    )
    parser.add_argument(
        "--galactic-cut",
        type=float,
        default=None,
        help="Synthetic mask: zero |b| < this latitude in degrees (galactic).",
    )
    args = parser.parse_args()

    args.output.parent.mkdir(parents=True, exist_ok=True)

    mask, mask_sources = build_mask(args)
    if not mask_sources:
        raise SystemExit(
            "no mask provided; pass --mask-fits or --galactic-cut, or use "
            "extract_planck_lowell_fallback.py for the unmasked variant."
        )
    f_sky = float(np.mean(mask > 0.5))
    print(f"f_sky = {f_sky:.4f}; mask sources = {mask_sources}")

    with args.output.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f, fieldnames=["operator", "ell", "m", "alm_real", "alm_imag"]
        )
        writer.writeheader()
        for operator, filename in MAP_FILENAMES.items():
            path = args.map_dir / filename
            if not path.exists():
                raise FileNotFoundError(path)
            print(f"reading {operator}: {path}")
            values, ordering, nside_in = read_map_column(path, args.column)
            print(
                f"downgrading {operator}: nside {nside_in} {ordering} "
                f"-> {args.nside_out} ring"
            )
            low = downgrade_mean(
                values,
                nside_in=nside_in,
                order_in=ordering,
                nside_out=args.nside_out,
                chunk_size=args.chunk_size,
            )
            masked_low = np.where(mask > 0.5, low, np.nan)
            print(
                f"computing alm {operator}: lmax={args.lmax} "
                f"f_sky={f_sky:.4f}"
            )
            for ell, m, z in compute_alm_direct(masked_low, args.nside_out, args.lmax):
                writer.writerow(
                    {
                        "operator": operator,
                        "ell": ell,
                        "m": m,
                        "alm_real": z.real,
                        "alm_imag": z.imag,
                    }
                )

    if args.manifest is not None:
        manifest = {
            "output": str(args.output),
            "lmax": args.lmax,
            "nside_out": args.nside_out,
            "column": args.column,
            "mask_sources": mask_sources,
            "f_sky": f_sky,
        }
        args.manifest.parent.mkdir(parents=True, exist_ok=True)
        args.manifest.write_text(
            json.dumps(manifest, indent=2) + "\n", encoding="utf-8"
        )

    print(f"wrote masked low-ell coefficients: {args.output}")


if __name__ == "__main__":
    main()
