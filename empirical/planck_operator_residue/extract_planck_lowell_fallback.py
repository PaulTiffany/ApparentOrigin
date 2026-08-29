"""Fallback low-ell extractor without healpy.

This script reads Planck HEALPix FITS maps with astropy, downgrades them to a
small HEALPix grid with astropy-healpix, and computes low-ell spherical
harmonic coefficients by direct quadrature.

It is slower and less canonical than healpy.map2alm. Use it for first contact
and operator-residue scouting; use the healpy extractor for final claims.
"""

from __future__ import annotations

import argparse
import csv
from pathlib import Path

import numpy as np
from astropy.io import fits
from astropy_healpix import HEALPix
from scipy.special import sph_harm
from tqdm import tqdm


MAP_FILENAMES = {
    "Commander": "COM_CMB_IQU-commander_2048_R3.00_full.fits",
    "NILC": "COM_CMB_IQU-nilc_2048_R3.00_full.fits",
    "SEVEM": "COM_CMB_IQU-sevem_2048_R3.00_full.fits",
    "SMICA": "COM_CMB_IQU-smica_2048_R3.00_full.fits",
}


def read_map_column(path: Path, column: str) -> tuple[np.ndarray, str, int]:
    with fits.open(path, memmap=True) as hdul:
        data = hdul[1].data
        header = hdul[1].header
        ordering = str(header.get("ORDERING", "RING")).lower()
        nside = int(header.get("NSIDE", round((len(data[column]) / 12) ** 0.5)))
        values = np.asarray(data[column], dtype=np.float64)
    return values, ordering, nside


def downgrade_mean(
    values: np.ndarray,
    nside_in: int,
    order_in: str,
    nside_out: int,
    chunk_size: int,
) -> np.ndarray:
    hp_in = HEALPix(nside=nside_in, order=order_in, frame=None)
    hp_out = HEALPix(nside=nside_out, order="ring", frame=None)
    npix_in = values.size
    npix_out = 12 * nside_out * nside_out
    sums = np.zeros(npix_out, dtype=np.float64)
    counts = np.zeros(npix_out, dtype=np.int64)

    for start in tqdm(range(0, npix_in, chunk_size), desc="downgrade", leave=False):
        stop = min(start + chunk_size, npix_in)
        pix = np.arange(start, stop, dtype=np.int64)
        lon, lat = hp_in.healpix_to_lonlat(pix)
        out_pix = hp_out.lonlat_to_healpix(lon, lat)
        chunk = values[start:stop]
        good = np.isfinite(chunk)
        np.add.at(sums, out_pix[good], chunk[good])
        np.add.at(counts, out_pix[good], 1)

    out = np.full(npix_out, np.nan, dtype=np.float64)
    good_out = counts > 0
    out[good_out] = sums[good_out] / counts[good_out]
    return out


def compute_alm_direct(values: np.ndarray, nside: int, lmax: int) -> list[tuple[int, int, complex]]:
    hp = HEALPix(nside=nside, order="ring", frame=None)
    pix = np.arange(values.size, dtype=np.int64)
    lon, lat = hp.healpix_to_lonlat(pix)
    phi = lon.to_value("rad")
    theta = 0.5 * np.pi - lat.to_value("rad")
    good = np.isfinite(values)
    y = values[good] - np.nanmean(values[good])
    phi = phi[good]
    theta = theta[good]
    pixel_area = 4.0 * np.pi / float(12 * nside * nside)

    rows: list[tuple[int, int, complex]] = []
    for ell in tqdm(range(2, lmax + 1), desc="alm", leave=False):
        for m in range(ell + 1):
            basis = sph_harm(m, ell, phi, theta)
            alm = pixel_area * np.sum(y * np.conjugate(basis))
            rows.append((ell, m, complex(alm)))
    return rows


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--map-dir", type=Path, required=True)
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("data/derived/planck_operator_residue/planck_lowell_alm_fallback.csv"),
    )
    parser.add_argument("--lmax", type=int, default=30)
    parser.add_argument("--nside-out", type=int, default=64)
    parser.add_argument("--column", default="I_STOKES")
    parser.add_argument("--chunk-size", type=int, default=1_000_000)
    args = parser.parse_args()

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
            print(f"reading {operator}: {path}")
            values, ordering, nside_in = read_map_column(path, args.column)
            print(f"downgrading {operator}: nside {nside_in} {ordering} -> {args.nside_out} ring")
            low = downgrade_mean(
                values,
                nside_in=nside_in,
                order_in=ordering,
                nside_out=args.nside_out,
                chunk_size=args.chunk_size,
            )
            print(f"computing alm {operator}: lmax={args.lmax}")
            for ell, m, z in compute_alm_direct(low, args.nside_out, args.lmax):
                writer.writerow(
                    {
                        "operator": operator,
                        "ell": ell,
                        "m": m,
                        "alm_real": z.real,
                        "alm_imag": z.imag,
                    }
                )

    print(f"wrote fallback low-ell coefficients: {args.output}")


if __name__ == "__main__":
    main()

