"""Octupole (ell=3) directional analysis of Planck operator-residue.

For each operator and each pair, find the axis n that maximizes
|a'_3,3(n)|^2 — the m=±3 component of the ell=3 alms in a frame with
z'-axis along n. This is the standard "preferred axis" methodology
used in the axis-of-evil / quadrupole-octupole-alignment literature.

Implementation: brute-force grid search on the northern hemisphere
(axes are sign-invariant so the southern hemisphere is redundant).
T_3 is reconstructed at each HEALPix pixel from the ell=3 alms;
|a'_3,3(n)|^2 is computed per axis by integrating T_3 against the
m=3 spherical harmonic in a frame with z'=n.

Phase tag: near-cousin-phase test of the axial feature of the
gestural conjecture. Companion to the ell=2 directional analysis;
the published quadrupole-octupole alignment lives in joint ell=2-3
structure.

Allowed claims:
    1. The operator-residue ell=3 axes do/do not have coherent
       preferred directions across pairs.
    2. The ell=2 and ell=3 axes do/do not align with each other
       (quadrupole-octupole alignment readout).
    3. The ell=3 pattern is robust/sensitive to the galactic mask.

Forbidden claims:
    1. AOC is confirmed by quadrupole-octupole alignment.
    2. LambdaCDM is refuted by axis alignment.
    3. The result demonstrates rotating-interior cosmology.
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


# Cartesian Y_lm coefficients for ell=3 on the unit sphere with x^2+y^2+z^2=1.
# Y_30 = C30 * z * (5 z^2 - 3)
# Y_31 = C31 * (5 z^2 - 1) * (x + i y)
# Y_32 = C32 * z * (x + i y)^2
# Y_33 = C33 * (x + i y)^3
C30 = 0.25 * math.sqrt(7.0 / math.pi)
C31 = -0.125 * math.sqrt(21.0 / math.pi)
C32 = 0.25 * math.sqrt(105.0 / (2.0 * math.pi))
C33 = -0.125 * math.sqrt(35.0 / math.pi)


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


def build_t3_pixels(
    a30: float, a31: complex, a32: complex, a33: complex, nside: int
) -> tuple[np.ndarray, np.ndarray]:
    """Reconstruct T_3 (the ell=3 component of the temperature) at every
    HEALPix pixel; return (T_pixels, positions[3, N])."""
    hp = HEALPix(nside=nside, order="ring", frame="galactic")
    pix = np.arange(12 * nside * nside, dtype=np.int64)
    lon, lat = hp.healpix_to_lonlat(pix)
    phi = lon.to_value("rad")
    theta_pol = np.pi / 2.0 - lat.to_value("rad")

    x = np.sin(theta_pol) * np.cos(phi)
    y = np.sin(theta_pol) * np.sin(phi)
    z = np.cos(theta_pol)

    # T_3 = a_30 Y_30 + 2 Re(a_31 Y_31) + 2 Re(a_32 Y_32) + 2 Re(a_33 Y_33)
    T = a30 * C30 * z * (5.0 * z**2 - 3.0)
    T += 2.0 * C31 * (5.0 * z**2 - 1.0) * (a31.real * x - a31.imag * y)
    T += 2.0 * C32 * z * (a32.real * (x**2 - y**2) - 2.0 * a32.imag * x * y)
    T += 2.0 * C33 * (
        a33.real * (x**3 - 3.0 * x * y**2)
        - a33.imag * (3.0 * x**2 * y - y**3)
    )
    return T, np.array([x, y, z])


def find_octupole_axis(
    T: np.ndarray, positions: np.ndarray, n_lat: int = 37, n_lon: int = 72
) -> tuple[np.ndarray, float, tuple[float, float]]:
    """Grid-search for n maximizing |a'_3,3|^2 = |int T_3(x) Y*_3,3(x; n) dOmega|^2."""
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

            # build orthonormal e_x, e_y in plane perpendicular to n_ax
            ref = np.array([1.0, 0.0, 0.0]) if abs(n_ax[2]) > 0.99 else np.array(
                [0.0, 0.0, 1.0]
            )
            e_x = ref - n_ax * np.dot(n_ax, ref)
            e_x /= np.linalg.norm(e_x)
            e_y = np.cross(n_ax, e_x)

            proj_x = np.einsum("i,ij->j", e_x, positions)
            proj_y = np.einsum("i,ij->j", e_y, positions)
            phi_n = np.arctan2(proj_y, proj_x)

            # Y_3,3(theta_n, phi_n) = C33 * sin^3(theta_n) * exp(3 i phi_n)
            Y33 = C33 * sin_t**3 * np.exp(3j * phi_n)
            a33 = pixel_area * np.sum(T * np.conj(Y33))
            score = float(abs(a33) ** 2)
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
        e3 = data[op][3]
        T, positions = build_t3_pixels(
            e3[0].real, e3[1], e3[2], e3[3], nside
        )
        axis, score, (lon_deg, lat_deg) = find_octupole_axis(
            T, positions, n_lat=n_lat, n_lon=n_lon
        )
        op_axes[op] = axis
        op_results[op] = {
            "l_deg": lon_deg,
            "b_deg": lat_deg,
            "max_a33_squared": score,
        }

    pair_axes: dict[str, np.ndarray] = {}
    pair_results: dict[str, dict] = {}
    for op_a, op_b in combinations(operators, 2):
        e3a = data[op_a][3]
        e3b = data[op_b][3]
        d_a30 = (e3a[0] - e3b[0]).real
        d_a31 = e3a[1] - e3b[1]
        d_a32 = e3a[2] - e3b[2]
        d_a33 = e3a[3] - e3b[3]
        T, positions = build_t3_pixels(d_a30, d_a31, d_a32, d_a33, nside)
        axis, score, (lon_deg, lat_deg) = find_octupole_axis(
            T, positions, n_lat=n_lat, n_lon=n_lon
        )
        key = f"{op_a}-{op_b}"
        pair_axes[key] = axis
        residual_power = (
            d_a30**2
            + 2.0 * (abs(d_a31) ** 2 + abs(d_a32) ** 2 + abs(d_a33) ** 2)
        )
        pair_results[key] = {
            "l_deg": lon_deg,
            "b_deg": lat_deg,
            "max_a33_squared": score,
            "residual_power": float(residual_power),
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
            pair_pair_align[f"{p1} | {p2}"] = angle_between(
                pair_axes[p1], pair_axes[p2]
            )

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
        "ell": 3,
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
    parser.add_argument("--n-lat", type=int, default=37)
    parser.add_argument("--n-lon", type=int, default=72)
    args = parser.parse_args()

    args.outdir.mkdir(parents=True, exist_ok=True)
    r = analyze(args.input, nside=args.nside, n_lat=args.n_lat, n_lon=args.n_lon)
    (args.outdir / "directional_octupole_axis_summary.json").write_text(
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
