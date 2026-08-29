"""Quadrupole (ell=2) m=l-maximizing axis search — methodology consistent
with the octupole (ell=3) script.

This is a methodology fix for the original ell=2 directional analysis,
which used the tensor-largest-|eigenvalue| eigenvector. That convention
can flip the axis by 90° depending on which eigenvalue dominates in
magnitude (positive or negative). The m=l-maximizing methodology used
for ell=3 (and standard in the axis-of-evil / QO-alignment literature)
picks the eigenvector of the *smallest* |eigenvalue| of the quadrupole
tensor, equivalently the axis maximizing |a'_2,2|^2.

This script reuses the same Y_l,m Cartesian forms and grid-search
machinery as directional_residue_axis_octupole.py, just at l=2.

Phase tag: methodology correction. The original tensor-eigenvector
report stays in place; this produces a parallel m=l-max report so
the ell=2 / ell=3 comparison is apples-to-apples.
"""

from __future__ import annotations

import argparse
import json
import math
from itertools import combinations
from pathlib import Path

import numpy as np
from astropy_healpix import HEALPix

from analyze_lowell_operator_residue import read_alm_csv


# Cartesian Y_2,m on the unit sphere x^2+y^2+z^2=1.
# Y_20 = C20 * (3 z^2 - 1)
# Y_21 = C21 * z * (x + i y)
# Y_22 = C22 * (x + i y)^2
C20 = 0.25 * math.sqrt(5.0 / math.pi)
C21 = -0.5 * math.sqrt(15.0 / (2.0 * math.pi))
C22 = 0.25 * math.sqrt(15.0 / (2.0 * math.pi))

REFERENCE_AXES_DEG = {
    "axis_of_evil_LM2005": (260.0, 60.0),
    "quad_oct_align_S2004": (250.0, 65.0),
    "cmb_cold_spot": (210.0, -57.0),
    "cmb_kinematic_dipole": (264.0, 48.0),
}


def lb_to_cart(l_deg: float, b_deg: float) -> np.ndarray:
    l = math.radians(l_deg)
    b = math.radians(b_deg)
    return np.array(
        [math.cos(l) * math.cos(b), math.sin(l) * math.cos(b), math.sin(b)]
    )


def cart_to_lb(axis: np.ndarray) -> tuple[float, float]:
    a = axis if axis[2] >= 0 else -axis
    l = math.degrees(math.atan2(a[1], a[0]))
    if l < 0:
        l += 360.0
    b = math.degrees(math.asin(float(np.clip(a[2], -1.0, 1.0))))
    return l, b


def angle_between(a: np.ndarray, b: np.ndarray) -> float:
    ua = a / np.linalg.norm(a)
    ub = b / np.linalg.norm(b)
    dot = abs(float(np.dot(ua, ub)))
    return math.degrees(math.acos(min(1.0, max(-1.0, dot))))


def build_t2_pixels(
    a20: float, a21: complex, a22: complex, nside: int
) -> tuple[np.ndarray, np.ndarray]:
    hp = HEALPix(nside=nside, order="ring", frame="galactic")
    pix = np.arange(12 * nside * nside, dtype=np.int64)
    lon, lat = hp.healpix_to_lonlat(pix)
    phi = lon.to_value("rad")
    theta_pol = np.pi / 2.0 - lat.to_value("rad")
    x = np.sin(theta_pol) * np.cos(phi)
    y = np.sin(theta_pol) * np.sin(phi)
    z = np.cos(theta_pol)

    T = a20 * C20 * (3.0 * z**2 - 1.0)
    T += 2.0 * C21 * z * (a21.real * x - a21.imag * y)
    T += 2.0 * C22 * (a22.real * (x**2 - y**2) - 2.0 * a22.imag * x * y)
    return T, np.array([x, y, z])


def find_quadrupole_max_axis(
    T: np.ndarray, positions: np.ndarray, n_lat: int = 37, n_lon: int = 72
) -> tuple[np.ndarray, float, tuple[float, float]]:
    pixel_area = 4.0 * math.pi / float(T.size)
    lats = np.linspace(0.5, 89.5, n_lat)
    lons = np.linspace(0.0, 359.0, n_lon)
    best_score = -1.0
    best_axis = np.array([0.0, 0.0, 1.0])
    best_lb = (0.0, 90.0)

    for lat_deg in lats:
        for lon_deg in lons:
            n_ax = lb_to_cart(lon_deg, lat_deg)
            cos_t = np.dot(n_ax, positions)
            cos_t = np.clip(cos_t, -1.0, 1.0)
            sin_t = np.sqrt(np.maximum(0.0, 1.0 - cos_t**2))
            ref = np.array([1.0, 0.0, 0.0]) if abs(n_ax[2]) > 0.99 else np.array(
                [0.0, 0.0, 1.0]
            )
            e_x = ref - n_ax * np.dot(n_ax, ref)
            e_x /= np.linalg.norm(e_x)
            e_y = np.cross(n_ax, e_x)
            proj_x = np.einsum("i,ij->j", e_x, positions)
            proj_y = np.einsum("i,ij->j", e_y, positions)
            phi_n = np.arctan2(proj_y, proj_x)
            Y22 = C22 * sin_t**2 * np.exp(2j * phi_n)
            a22 = pixel_area * np.sum(T * np.conj(Y22))
            score = float(abs(a22) ** 2)
            if score > best_score:
                best_score = score
                best_axis = n_ax
                best_lb = (lon_deg, lat_deg)
    return best_axis, best_score, best_lb


def analyze(input_csv: Path, nside: int = 64, n_lat: int = 37, n_lon: int = 72) -> dict:
    data = read_alm_csv(input_csv)
    operators = sorted(data)

    op_axes: dict[str, np.ndarray] = {}
    op_results: dict[str, dict] = {}
    for op in operators:
        e2 = data[op][2]
        T, positions = build_t2_pixels(e2[0].real, e2[1], e2[2], nside)
        axis, score, (lon_deg, lat_deg) = find_quadrupole_max_axis(
            T, positions, n_lat=n_lat, n_lon=n_lon
        )
        op_axes[op] = axis
        op_results[op] = {
            "l_deg": lon_deg,
            "b_deg": lat_deg,
            "max_a22_squared": score,
        }

    pair_axes: dict[str, np.ndarray] = {}
    pair_results: dict[str, dict] = {}
    for op_a, op_b in combinations(operators, 2):
        e2a = data[op_a][2]
        e2b = data[op_b][2]
        d_a20 = (e2a[0] - e2b[0]).real
        d_a21 = e2a[1] - e2b[1]
        d_a22 = e2a[2] - e2b[2]
        T, positions = build_t2_pixels(d_a20, d_a21, d_a22, nside)
        axis, score, (lon_deg, lat_deg) = find_quadrupole_max_axis(
            T, positions, n_lat=n_lat, n_lon=n_lon
        )
        key = f"{op_a}-{op_b}"
        pair_axes[key] = axis
        pair_results[key] = {
            "l_deg": lon_deg,
            "b_deg": lat_deg,
            "max_a22_squared": score,
        }

    ref_cart = {name: lb_to_cart(*lb) for name, lb in REFERENCE_AXES_DEG.items()}
    op_pair_align = {
        f"{a}-{b}": angle_between(op_axes[a], op_axes[b])
        for a, b in combinations(operators, 2)
    }
    pair_keys = list(pair_axes)
    pair_pair_align = {}
    for i, p1 in enumerate(pair_keys):
        for p2 in pair_keys[i + 1 :]:
            pair_pair_align[f"{p1} | {p2}"] = angle_between(pair_axes[p1], pair_axes[p2])
    op_vs_ref = {
        op: {ref: angle_between(op_axes[op], ref_cart[ref]) for ref in ref_cart}
        for op in operators
    }
    pair_vs_ref = {
        pair: {ref: angle_between(pair_axes[pair], ref_cart[ref]) for ref in ref_cart}
        for pair in pair_keys
    }

    op_disp = list(op_pair_align.values())
    pair_disp = list(pair_pair_align.values())

    return {
        "input": str(input_csv),
        "ell": 2,
        "methodology": "m=l-maximizing (consistent with ell=3 directional)",
        "operators": operators,
        "operator_axes": op_results,
        "pair_residual_axes": pair_results,
        "operator_pair_alignments_deg": op_pair_align,
        "pair_pair_alignments_deg": pair_pair_align,
        "operator_vs_reference_deg": op_vs_ref,
        "pair_vs_reference_deg": pair_vs_ref,
        "summary": {
            "operator_axis_dispersion_deg": {
                "median": float(np.median(op_disp)),
                "mean": float(np.mean(op_disp)),
                "max": float(np.max(op_disp)),
            },
            "pair_residual_axis_dispersion_deg": {
                "median": float(np.median(pair_disp)),
                "mean": float(np.mean(pair_disp)),
                "max": float(np.max(pair_disp)),
            },
        },
        "axes_cartesian": {
            "operator": {op: op_axes[op].tolist() for op in operators},
            "pair": {p: pair_axes[p].tolist() for p in pair_keys},
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--outdir", type=Path, required=True)
    parser.add_argument("--nside", type=int, default=64)
    args = parser.parse_args()
    args.outdir.mkdir(parents=True, exist_ok=True)
    r = analyze(args.input, nside=args.nside)
    (args.outdir / "directional_quadrupole_mlmax_summary.json").write_text(
        json.dumps(r, indent=2) + "\n", encoding="utf-8"
    )
    print(
        json.dumps(
            {
                "input": r["input"],
                "operator_axis_median_dispersion_deg": r["summary"][
                    "operator_axis_dispersion_deg"
                ]["median"],
                "pair_residual_axis_median_dispersion_deg": r["summary"][
                    "pair_residual_axis_dispersion_deg"
                ]["median"],
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
