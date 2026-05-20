"""Coefficient-space null for Planck low-ell directional statistics.

This is the first simulation-level control for the corrected ell=2/ell=3
directional analysis. It generates an isotropic common low-ell sky, gives four
mock reconstruction operators independent coefficient noise, then reruns the
same m=ell-maximizing axis statistic used in the Planck readout.

This is not a full Planck component-separation simulation and does not model
mask-induced mode coupling. It asks a narrower question:

    Under an isotropic common sky plus operator noise calibrated from the
    observed coefficient distances, how often do the observed directional
    statistics occur?

Phase tag: empirical control, not evidence for AOC.
"""

from __future__ import annotations

import argparse
import csv
import json
import math
from itertools import combinations
from pathlib import Path

import numpy as np

from analyze_lowell_operator_residue import coefficient_distance, read_alm_csv


OPERATORS = ("Commander", "NILC", "SEVEM", "SMICA")

C20 = 0.25 * math.sqrt(5.0 / math.pi)
C21 = -0.5 * math.sqrt(15.0 / (2.0 * math.pi))
C22 = 0.25 * math.sqrt(15.0 / (2.0 * math.pi))

C30 = 0.25 * math.sqrt(7.0 / math.pi)
C31 = -0.125 * math.sqrt(21.0 / math.pi)
C32 = 0.25 * math.sqrt(105.0 / (2.0 * math.pi))
C33 = -0.125 * math.sqrt(35.0 / math.pi)


OBSERVED = {
    "unmasked": {
        "qo_median_deg": 11.9,
        "ell2_operator_dispersion_deg": 14.127136172131596,
        "ell3_operator_dispersion_deg": 3.3427816071657364,
        "ell2_pair_residue_dispersion_deg": 80.89510737409172,
        "ell3_pair_residue_dispersion_deg": 33.168223264892,
    },
    "galcut20": {
        "qo_median_deg": 29.5,
        "ell2_operator_dispersion_deg": 4.615091828878166,
        "ell3_operator_dispersion_deg": 5.111582223038215,
        "ell2_pair_residue_dispersion_deg": 58.43819284622772,
        "ell3_pair_residue_dispersion_deg": 55.61741685772555,
    },
}


def lb_to_cart(l_deg: float, b_deg: float) -> np.ndarray:
    l_rad = math.radians(l_deg)
    b_rad = math.radians(b_deg)
    return np.array(
        [
            math.cos(l_rad) * math.cos(b_rad),
            math.sin(l_rad) * math.cos(b_rad),
            math.sin(b_rad),
        ]
    )


def angle_between(a: np.ndarray, b: np.ndarray) -> float:
    ua = a / np.linalg.norm(a)
    ub = b / np.linalg.norm(b)
    dot = abs(float(np.dot(ua, ub)))
    return math.degrees(math.acos(min(1.0, max(-1.0, dot))))


def median_pairwise_angle(axes: dict[str, np.ndarray]) -> float:
    return float(
        np.median(
            [
                angle_between(axes[a], axes[b])
                for a, b in combinations(sorted(axes), 2)
            ]
        )
    )


def coefficient_distance_to_noise_ratio(distance: float) -> float:
    """Convert pairwise coefficient distance to C_noise / C_sky.

    For x_i = s + n_i, x_j = s + n_j with independent operator noise,
    E[d_ij^2] = 2 r / (1 + r), where r = C_noise / C_sky.
    """
    d2 = distance * distance
    if d2 >= 2.0:
        return float("inf")
    return d2 / (2.0 - d2)


def calibrated_noise_ratios(input_csv: Path) -> dict[int, float]:
    data = read_alm_csv(input_csv)
    ratios: dict[int, float] = {}
    for ell in (2, 3):
        distances = []
        for op_a, op_b in combinations(sorted(data), 2):
            distances.append(coefficient_distance(data[op_a][ell], data[op_b][ell], ell))
        ratios[ell] = coefficient_distance_to_noise_ratio(float(np.median(distances)))
    return ratios


def fibonacci_positions(n_points: int) -> np.ndarray:
    """Approximately equal-area sphere points, returned as shape (3, N)."""
    idx = np.arange(n_points, dtype=float) + 0.5
    z = 1.0 - 2.0 * idx / float(n_points)
    radius = np.sqrt(np.maximum(0.0, 1.0 - z**2))
    phi = math.pi * (3.0 - math.sqrt(5.0)) * idx
    x = radius * np.cos(phi)
    y = radius * np.sin(phi)
    return np.array([x, y, z])


def real_coeff_basis(ell: int, projection_nside: int) -> tuple[np.ndarray, np.ndarray]:
    """Return basis matrix B and positions for real-map alm coordinates.

    Coefficient order:
      ell=2: a20, Re a21, Im a21, Re a22, Im a22
      ell=3: a30, Re a31, Im a31, Re a32, Im a32, Re a33, Im a33
    """
    n_points = 12 * projection_nside * projection_nside
    positions = fibonacci_positions(n_points)
    x, y, z = positions

    if ell == 2:
        basis = np.column_stack(
            [
                C20 * (3.0 * z**2 - 1.0),
                2.0 * C21 * z * x,
                -2.0 * C21 * z * y,
                2.0 * C22 * (x**2 - y**2),
                -4.0 * C22 * x * y,
            ]
        )
    elif ell == 3:
        basis = np.column_stack(
            [
                C30 * z * (5.0 * z**2 - 3.0),
                2.0 * C31 * (5.0 * z**2 - 1.0) * x,
                -2.0 * C31 * (5.0 * z**2 - 1.0) * y,
                2.0 * C32 * z * (x**2 - y**2),
                -4.0 * C32 * z * x * y,
                2.0 * C33 * (x**3 - 3.0 * x * y**2),
                -2.0 * C33 * (3.0 * x**2 * y - y**3),
            ]
        )
    else:
        raise ValueError(f"unsupported ell={ell}")

    return basis, positions


def axis_grid(n_lat: int, n_lon: int) -> np.ndarray:
    lats = np.linspace(0.5, 89.5, n_lat)
    lons = np.linspace(0.0, 359.0, n_lon)
    return np.array([lb_to_cart(lon, lat) for lat in lats for lon in lons])


def precompute_projection(
    ell: int, nside: int, n_lat: int, n_lon: int
) -> tuple[np.ndarray, np.ndarray]:
    basis, positions = real_coeff_basis(ell, nside)
    axes = axis_grid(n_lat, n_lon)
    pixel_area = 4.0 * math.pi / float(positions.shape[1])
    weights = np.empty((len(axes), basis.shape[1]), dtype=np.complex128)

    for idx, n_ax in enumerate(axes):
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

        if ell == 2:
            y_ll = C22 * sin_t**2 * np.exp(2j * phi_n)
        elif ell == 3:
            y_ll = C33 * sin_t**3 * np.exp(3j * phi_n)
        else:
            raise ValueError(f"unsupported ell={ell}")

        weights[idx] = pixel_area * np.conj(y_ll) @ basis

    return axes, weights


def random_real_alm_coeffs(rng: np.random.Generator, ell: int, scale: float = 1.0) -> np.ndarray:
    values = [rng.normal(0.0, scale)]
    for _m in range(1, ell + 1):
        sigma = scale / math.sqrt(2.0)
        values.append(rng.normal(0.0, sigma))
        values.append(rng.normal(0.0, sigma))
    return np.array(values, dtype=float)


def find_axis(coeffs: np.ndarray, axes: np.ndarray, weights: np.ndarray) -> np.ndarray:
    scores = np.abs(weights @ coeffs) ** 2
    return axes[int(np.argmax(scores))]


def condition_metrics(
    rng: np.random.Generator,
    common: dict[int, np.ndarray],
    noise_ratios: dict[int, float],
    projections: dict[int, tuple[np.ndarray, np.ndarray]],
) -> dict[str, float]:
    op_axes: dict[int, dict[str, np.ndarray]] = {2: {}, 3: {}}
    pair_axes: dict[int, dict[str, np.ndarray]] = {2: {}, 3: {}}
    op_coeffs: dict[int, dict[str, np.ndarray]] = {2: {}, 3: {}}

    for ell in (2, 3):
        axes, weights = projections[ell]
        noise_scale = math.sqrt(noise_ratios[ell])
        for op in OPERATORS:
            coeffs = common[ell] + noise_scale * random_real_alm_coeffs(rng, ell)
            op_coeffs[ell][op] = coeffs
            op_axes[ell][op] = find_axis(coeffs, axes, weights)

        for op_a, op_b in combinations(OPERATORS, 2):
            key = f"{op_a}-{op_b}"
            residual = op_coeffs[ell][op_a] - op_coeffs[ell][op_b]
            pair_axes[ell][key] = find_axis(residual, axes, weights)

    qo_angles = [
        angle_between(op_axes[2][op], op_axes[3][op])
        for op in OPERATORS
    ]

    return {
        "qo_median_deg": float(np.median(qo_angles)),
        "ell2_operator_dispersion_deg": median_pairwise_angle(op_axes[2]),
        "ell3_operator_dispersion_deg": median_pairwise_angle(op_axes[3]),
        "ell2_pair_residue_dispersion_deg": median_pairwise_angle(pair_axes[2]),
        "ell3_pair_residue_dispersion_deg": median_pairwise_angle(pair_axes[3]),
    }


def percentile_leq(samples: list[float], observed: float) -> float:
    arr = np.array(samples, dtype=float)
    return float(np.mean(arr <= observed))


def percentile_geq(samples: list[float], observed: float) -> float:
    arr = np.array(samples, dtype=float)
    return float(np.mean(arr >= observed))


def summarize(samples: list[dict[str, object]], noise_ratios: dict[str, dict[int, float]]) -> dict:
    by_condition: dict[str, list[dict[str, object]]] = {"unmasked": [], "galcut20": []}
    for row in samples:
        by_condition[str(row["condition"])].append(row)

    metric_keys = list(OBSERVED["unmasked"])
    conditions = {}
    for condition, rows in by_condition.items():
        conditions[condition] = {}
        for key in metric_keys:
            vals = [float(row[key]) for row in rows]
            obs = OBSERVED[condition][key]
            tail = percentile_leq(vals, obs)
            if "pair_residue_dispersion" in key:
                # The observed pair-residue null is a lack of clustering, so the
                # relevant tail is high dispersion, not unusually small dispersion.
                tail = percentile_geq(vals, obs)
            conditions[condition][key] = {
                "observed": obs,
                "null_mean": float(np.mean(vals)),
                "null_median": float(np.median(vals)),
                "null_q05": float(np.quantile(vals, 0.05)),
                "null_q95": float(np.quantile(vals, 0.95)),
                "tail_fraction": tail,
                "tail_definition": "<= observed"
                if "pair_residue_dispersion" not in key
                else ">= observed",
            }

    delta_obs = OBSERVED["galcut20"]["qo_median_deg"] - OBSERVED["unmasked"]["qo_median_deg"]
    by_seed: dict[int, dict[str, dict[str, object]]] = {}
    for row in samples:
        by_seed.setdefault(int(row["seed"]), {})[str(row["condition"])] = row
    deltas = [
        float(rows["galcut20"]["qo_median_deg"]) - float(rows["unmasked"]["qo_median_deg"])
        for rows in by_seed.values()
        if "unmasked" in rows and "galcut20" in rows
    ]

    return {
        "status": "coefficient-space isotropic common-sky null",
        "n_seeds": len(by_seed),
        "observed_thresholds": OBSERVED,
        "noise_ratios_c_noise_over_c_sky": noise_ratios,
        "conditions": conditions,
        "mask_delta_qo_median_deg": {
            "observed": delta_obs,
            "null_mean": float(np.mean(deltas)),
            "null_median": float(np.median(deltas)),
            "null_q05": float(np.quantile(deltas, 0.05)),
            "null_q95": float(np.quantile(deltas, 0.95)),
            "fraction_null_greater_equal_observed": percentile_geq(deltas, delta_obs),
        },
        "limitations": [
            "No Planck component-separation machinery is simulated.",
            "No mask-induced mode coupling is simulated.",
            "The galcut20 condition shares the same synthetic sky and differs only by calibrated operator-noise level.",
            "The statistic is evaluated on a finite axis grid using a Fibonacci projection quadrature, matching the published pipeline approximately.",
        ],
    }


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def make_report(path: Path, summary: dict) -> None:
    cond = summary["conditions"]
    delta = summary["mask_delta_qo_median_deg"]
    lines = [
        "# Directional Axis Coefficient-Space Null",
        "",
        "Status: first simulation-level control for the corrected ell=2/ell=3",
        "m=ell-maximizing directional statistic.",
        "",
        "## Question",
        "",
        "Under an isotropic common low-ell sky plus independent operator noise",
        "calibrated from the observed coefficient distances, how often do the",
        "observed Q-O alignment, operator-axis clustering, and mask-state shift",
        "occur?",
        "",
        "## Calibration",
        "",
        "| condition | ell=2 C_noise/C_sky | ell=3 C_noise/C_sky |",
        "| --- | ---: | ---: |",
        *[
            f"| {name} | {ratios[2]:.6g} | {ratios[3]:.6g} |"
            for name, ratios in summary["noise_ratios_c_noise_over_c_sky"].items()
        ],
        "",
        "## Tail Fractions",
        "",
        "| condition | metric | observed | null median | 5-95% null | tail |",
        "| --- | --- | ---: | ---: | ---: | ---: |",
    ]
    for condition in ("unmasked", "galcut20"):
        for key, stats in cond[condition].items():
            lines.append(
                "| "
                f"{condition} | `{key}` | {stats['observed']:.4g} | "
                f"{stats['null_median']:.4g} | "
                f"{stats['null_q05']:.4g}-{stats['null_q95']:.4g} | "
                f"{stats['tail_fraction']:.4g} |"
            )

    lines.extend(
        [
            "",
            "Mask-state Q-O delta:",
            "",
            "```text",
            f"observed galcut20 - unmasked = {delta['observed']:.4g} deg",
            f"null median = {delta['null_median']:.4g} deg",
            f"null 5-95% = {delta['null_q05']:.4g} to {delta['null_q95']:.4g} deg",
            f"fraction null >= observed = {delta['fraction_null_greater_equal_observed']:.4g}",
            "```",
            "",
            "## Allowed Claims",
            "",
            "1. This null quantifies how expensive the observed directional",
            "   statistics are under an isotropic common-sky, calibrated-noise",
            "   coefficient model.",
            "2. A low tail fraction means the measured statistic is atypical under",
            "   this specific null, not under every standard cosmology control.",
            "3. The mask-state delta is tested only against a no-mode-coupling",
            "   coefficient model; it is not a replacement for a real masked-sky",
            "   CMB simulation.",
            "",
            "## Forbidden Claims",
            "",
            "1. This simulation proves AOC, a false bottom, cosmic torque, or",
            "   apparatus-bound K.",
            "2. This simulation refutes LambdaCDM.",
            "3. This simulation fully explains the Planck low-ell anomaly literature.",
            "4. The galcut20 result is a complete mask likelihood analysis.",
            "",
            "## Limitations",
            "",
            *[f"- {item}" for item in summary["limitations"]],
            "",
            "## Next Control",
            "",
            "Replace this coefficient-space null with a masked-sky CMB null: draw",
            "Gaussian skies from a fiducial low-ell Cl, apply the same galactic mask",
            "or official Planck common mask, extract pseudo-alms, and rerun this",
            "directional statistic.",
        ]
    )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--unmasked-input",
        type=Path,
        default=Path("data/derived/planck_operator_residue/planck_lowell_alm_fallback_nside64.csv"),
    )
    parser.add_argument(
        "--galcut20-input",
        type=Path,
        default=Path("data/derived/planck_operator_residue/planck_lowell_alm_fallback_nside64_galcut20.csv"),
    )
    parser.add_argument(
        "--outdir",
        type=Path,
        default=Path("reports/planck_operator_residue/directional_axis_null_coeffspace"),
    )
    parser.add_argument("--seeds", type=int, default=1000)
    parser.add_argument("--seed", type=int, default=20260429)
    parser.add_argument("--projection-nside", type=int, default=16)
    parser.add_argument("--n-lat", type=int, default=37)
    parser.add_argument("--n-lon", type=int, default=72)
    args = parser.parse_args()

    noise_ratios = {
        "unmasked": calibrated_noise_ratios(args.unmasked_input),
        "galcut20": calibrated_noise_ratios(args.galcut20_input),
    }
    projections = {
        ell: precompute_projection(ell, args.projection_nside, args.n_lat, args.n_lon)
        for ell in (2, 3)
    }

    rng = np.random.default_rng(args.seed)
    rows: list[dict[str, object]] = []
    for idx in range(args.seeds):
        common = {
            2: random_real_alm_coeffs(rng, 2),
            3: random_real_alm_coeffs(rng, 3),
        }
        for condition in ("unmasked", "galcut20"):
            metrics = condition_metrics(rng, common, noise_ratios[condition], projections)
            rows.append({"seed": idx, "condition": condition, **metrics})

    summary = summarize(rows, noise_ratios)
    summary["simulation_parameters"] = {
        "seed": args.seed,
        "projection_nside": args.projection_nside,
        "n_lat": args.n_lat,
        "n_lon": args.n_lon,
        "axis_grid_size": args.n_lat * args.n_lon,
        "unmasked_input": str(args.unmasked_input),
        "galcut20_input": str(args.galcut20_input),
    }

    args.outdir.mkdir(parents=True, exist_ok=True)
    write_csv(args.outdir / "directional_axis_null_samples.csv", rows)
    (args.outdir / "directional_axis_null_summary.json").write_text(
        json.dumps(summary, indent=2) + "\n", encoding="utf-8"
    )
    make_report(args.outdir / "directional_axis_null_report.md", summary)

    print(
        json.dumps(
            {
                "n_seeds": summary["n_seeds"],
                "unmasked_qo_tail": summary["conditions"]["unmasked"][
                    "qo_median_deg"
                ]["tail_fraction"],
                "galcut20_qo_tail": summary["conditions"]["galcut20"][
                    "qo_median_deg"
                ]["tail_fraction"],
                "mask_delta_tail": summary["mask_delta_qo_median_deg"][
                    "fraction_null_greater_equal_observed"
                ],
                "outdir": str(args.outdir),
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
