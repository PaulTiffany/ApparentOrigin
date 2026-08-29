"""High-ell leakage null for masked low-ell directional statistics.

The previous masked-sky null generated only ell=2 and ell=3. This script asks
whether higher multipoles leaking through the galactic cut change the
quadrupole-octupole alignment contract.

It draws isotropic Gaussian skies for 2 <= ell <= lmax, synthesizes maps on an
approximately equal-area sphere grid, extracts unmasked and masked pseudo-alms
only at ell=2 and ell=3, and evaluates the same m=ell-maximizing axis statistic.

This is still not a Planck likelihood or component-separation simulation. It is
the next feasible control on the operator/instrument/compose chain: mask
geometry plus high-ell leakage, without foregrounds or real Planck masks.
"""

from __future__ import annotations

import argparse
import csv
import json
import math
from pathlib import Path

import numpy as np
from scipy.special import sph_harm_y

from directional_axis_masked_sky_null import (
    extract_pseudo_coeffs,
    q_o_angle,
    axis_shift,
)
from directional_axis_null_sim import (
    OBSERVED,
    fibonacci_positions,
    percentile_geq,
    percentile_leq,
    precompute_projection,
    random_real_alm_coeffs,
)


def flat_sachs_wolfe_scale(ell: int) -> float:
    return math.sqrt(1.0 / float(ell * (ell + 1)))


def real_basis_for_ell(ell: int, positions: np.ndarray) -> np.ndarray:
    """Real-map basis columns: a_l0, Re/Im a_lm for m>0."""
    x, y, z = positions
    phi = np.arctan2(y, x)
    theta = np.arccos(np.clip(z, -1.0, 1.0))
    cols = [sph_harm_y(ell, 0, theta, phi).real]
    for m in range(1, ell + 1):
        ylm = sph_harm_y(ell, m, theta, phi)
        cols.append(2.0 * ylm.real)
        cols.append(-2.0 * ylm.imag)
    return np.column_stack(cols)


def build_synthesis_basis(
    positions: np.ndarray, ell_min: int, ell_max: int
) -> tuple[np.ndarray, list[tuple[int, int]]]:
    blocks = []
    slices: list[tuple[int, int]] = []
    start = 0
    for ell in range(ell_min, ell_max + 1):
        block = real_basis_for_ell(ell, positions)
        stop = start + block.shape[1]
        blocks.append(block)
        slices.append((start, stop))
        start = stop
    return np.column_stack(blocks), slices


def draw_coeff_vector(
    rng: np.random.Generator,
    ell_min: int,
    ell_max: int,
    high_ell_scale: float,
) -> np.ndarray:
    parts = []
    for ell in range(ell_min, ell_max + 1):
        scale = flat_sachs_wolfe_scale(ell)
        if ell > 3:
            scale *= high_ell_scale
        parts.append(random_real_alm_coeffs(rng, ell, scale=scale))
    return np.concatenate(parts)


def summarize(rows: list[dict[str, float | int]], f_sky: float, ell_max: int, high_ell_scale: float) -> dict:
    obs_unmasked = OBSERVED["unmasked"]["qo_median_deg"]
    obs_masked = OBSERVED["galcut20"]["qo_median_deg"]
    obs_delta = obs_masked - obs_unmasked

    def vals(key: str) -> list[float]:
        return [float(row[key]) for row in rows]

    def stat_block(key: str, observed: float, tail: str) -> dict:
        samples = vals(key)
        return {
            "observed": observed,
            "null_mean": float(np.mean(samples)),
            "null_median": float(np.median(samples)),
            "null_q05": float(np.quantile(samples, 0.05)),
            "null_q95": float(np.quantile(samples, 0.95)),
            "tail_definition": tail,
            "tail_fraction": percentile_leq(samples, observed)
            if tail == "<= observed"
            else percentile_geq(samples, observed),
        }

    joint = [
        row
        for row in rows
        if float(row["unmasked_qo_angle_deg"]) <= obs_unmasked
        and float(row["mask_delta_qo_deg"]) >= obs_delta
    ]

    return {
        "status": "high-ell leakage masked-sky null",
        "n_seeds": len(rows),
        "mask": {
            "type": "synthetic galactic cut",
            "condition": "|b| > 20 deg",
            "f_sky": f_sky,
        },
        "cl_prior": f"C_ell proportional to 1/[ell(ell+1)] for 2<=ell<={ell_max}",
        "high_ell_scale": high_ell_scale,
        "statistics": {
            "unmasked_qo_angle_deg": stat_block(
                "unmasked_qo_angle_deg", obs_unmasked, "<= observed"
            ),
            "masked_qo_angle_deg": stat_block(
                "masked_qo_angle_deg", obs_masked, ">= observed"
            ),
            "mask_delta_qo_deg": stat_block(
                "mask_delta_qo_deg", obs_delta, ">= observed"
            ),
            "ell2_axis_shift_deg": {
                "null_mean": float(np.mean(vals("ell2_axis_shift_deg"))),
                "null_median": float(np.median(vals("ell2_axis_shift_deg"))),
                "null_q05": float(np.quantile(vals("ell2_axis_shift_deg"), 0.05)),
                "null_q95": float(np.quantile(vals("ell2_axis_shift_deg"), 0.95)),
            },
            "ell3_axis_shift_deg": {
                "null_mean": float(np.mean(vals("ell3_axis_shift_deg"))),
                "null_median": float(np.median(vals("ell3_axis_shift_deg"))),
                "null_q05": float(np.quantile(vals("ell3_axis_shift_deg"), 0.05)),
                "null_q95": float(np.quantile(vals("ell3_axis_shift_deg"), 0.95)),
            },
            "joint_unmasked_tight_and_delta_large": {
                "observed_unmasked_qo_max_deg": obs_unmasked,
                "observed_delta_min_deg": obs_delta,
                "fraction": float(len(joint) / len(rows)),
                "count": len(joint),
            },
        },
        "limitations": [
            "No Planck component-separation operators are simulated.",
            "No beam, detector noise, foregrounds, inpainting, or official Planck mask is simulated.",
            "High-ell content uses a simple flat-Sachs-Wolfe-like power law, not a precision LambdaCDM Cl.",
            "The extraction uses direct pseudo-alms with mean subtraction, matching the fallback extractor's convention.",
        ],
    }


def write_csv(path: Path, rows: list[dict[str, float | int]]) -> None:
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def make_report(path: Path, summary: dict) -> None:
    stats = summary["statistics"]
    delta = stats["mask_delta_qo_deg"]
    joint = stats["joint_unmasked_tight_and_delta_large"]
    lines = [
        "# Directional Axis High-Ell Leakage Null",
        "",
        "Status: mask-geometry null with additional Gaussian multipoles above ell=3.",
        "",
        "## Question",
        "",
        "Does high-ell leakage through the synthetic galactic cut change the",
        "quadrupole-octupole alignment contract relative to the low-ell-only",
        "masked-sky null?",
        "",
        "## Setup",
        "",
        f"- Seeds: {summary['n_seeds']}",
        f"- Mask: {summary['mask']['condition']} (`f_sky={summary['mask']['f_sky']:.4f}`)",
        f"- Prior: {summary['cl_prior']}",
        f"- High-ell scale multiplier: {summary['high_ell_scale']:.4g}",
        "- Extraction: direct pseudo-alms at ell=2 and ell=3",
        "",
        "## Tail Fractions",
        "",
        "| metric | observed threshold | null median | 5-95% null | tail |",
        "| --- | ---: | ---: | ---: | ---: |",
    ]
    for key in ("unmasked_qo_angle_deg", "masked_qo_angle_deg", "mask_delta_qo_deg"):
        block = stats[key]
        lines.append(
            f"| `{key}` | {block['observed']:.4g} | {block['null_median']:.4g} | "
            f"{block['null_q05']:.4g}-{block['null_q95']:.4g} | "
            f"{block['tail_fraction']:.4g} |"
        )

    lines.extend(
        [
            "",
            "Axis shifts caused by the mask:",
            "",
            "| metric | null median | 5-95% null |",
            "| --- | ---: | ---: |",
        ]
    )
    for key in ("ell2_axis_shift_deg", "ell3_axis_shift_deg"):
        block = stats[key]
        lines.append(
            f"| `{key}` | {block['null_median']:.4g} | "
            f"{block['null_q05']:.4g}-{block['null_q95']:.4g} |"
        )

    lines.extend(
        [
            "",
            "Joint event:",
            "",
            "```text",
            f"unmasked Q-O <= {joint['observed_unmasked_qo_max_deg']:.4g} deg",
            f"and mask delta >= {joint['observed_delta_min_deg']:.4g} deg",
            f"fraction = {joint['fraction']:.6g} ({joint['count']} / {summary['n_seeds']})",
            "```",
            "",
            "## Contract Reading",
            "",
            f"The observed mask-state Q-O delta tail is {delta['tail_fraction']:.4g}.",
            "This is a feasibility-contract check: if high-ell leakage makes the",
            "out-of-contract band large, then the next contract must instrument",
            "leakage before interpreting low-ell recomposition.",
            "",
            "## Allowed Claims",
            "",
            "1. This null tests whether high-ell leakage through the synthetic mask",
            "   changes the directional-statistic tails.",
            "2. The result is a control on feasibility of the low-ell mask contract.",
            "3. It does not test AOC directly.",
            "",
            "## Forbidden Claims",
            "",
            "1. This proves or refutes AOC.",
            "2. This refutes LambdaCDM.",
            "3. This replaces official Planck masked-sky likelihood analysis.",
            "4. The simple high-ell power law is a precision CMB simulation.",
            "",
            "## Limitations",
            "",
            *[f"- {item}" for item in summary["limitations"]],
            "",
            "## Next Control",
            "",
            "Swap the simple power law for a fiducial LambdaCDM Cl and, if available,",
            "replace the synthetic galactic cut with an official Planck common mask.",
        ]
    )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--outdir",
        type=Path,
        default=Path("reports/planck_operator_residue/directional_axis_high_ell_leakage_null"),
    )
    parser.add_argument("--seeds", type=int, default=1000)
    parser.add_argument("--seed", type=int, default=20260429)
    parser.add_argument("--map-nside", type=int, default=32)
    parser.add_argument("--projection-nside", type=int, default=16)
    parser.add_argument("--ell-max", type=int, default=30)
    parser.add_argument("--high-ell-scale", type=float, default=1.0)
    parser.add_argument("--galactic-cut", type=float, default=20.0)
    parser.add_argument("--n-lat", type=int, default=37)
    parser.add_argument("--n-lon", type=int, default=72)
    args = parser.parse_args()

    positions = fibonacci_positions(12 * args.map_nside * args.map_nside)
    synthesis_basis, _ = build_synthesis_basis(positions, 2, args.ell_max)
    z = positions[2]
    mask = (
        np.abs(np.degrees(np.arcsin(np.clip(z, -1.0, 1.0)))) > args.galactic_cut
    ).astype(float)
    full_mask = np.ones_like(mask)
    f_sky = float(np.mean(mask > 0.5))
    projections = {
        ell: precompute_projection(ell, args.projection_nside, args.n_lat, args.n_lon)
        for ell in (2, 3)
    }

    rng = np.random.default_rng(args.seed)
    rows: list[dict[str, float | int]] = []
    for idx in range(args.seeds):
        coeff_vector = draw_coeff_vector(rng, 2, args.ell_max, args.high_ell_scale)
        sky_map = synthesis_basis @ coeff_vector
        unmasked_coeffs = extract_pseudo_coeffs(sky_map, positions, full_mask)
        masked_coeffs = extract_pseudo_coeffs(sky_map, positions, mask)
        unmasked_qo = q_o_angle(unmasked_coeffs, projections)
        masked_qo = q_o_angle(masked_coeffs, projections)
        rows.append(
            {
                "seed": idx,
                "unmasked_qo_angle_deg": unmasked_qo,
                "masked_qo_angle_deg": masked_qo,
                "mask_delta_qo_deg": masked_qo - unmasked_qo,
                "ell2_axis_shift_deg": axis_shift(
                    unmasked_coeffs, masked_coeffs, 2, projections
                ),
                "ell3_axis_shift_deg": axis_shift(
                    unmasked_coeffs, masked_coeffs, 3, projections
                ),
            }
        )

    summary = summarize(rows, f_sky, args.ell_max, args.high_ell_scale)
    summary["simulation_parameters"] = {
        "seed": args.seed,
        "map_nside": args.map_nside,
        "projection_nside": args.projection_nside,
        "ell_max": args.ell_max,
        "high_ell_scale": args.high_ell_scale,
        "galactic_cut_deg": args.galactic_cut,
        "n_lat": args.n_lat,
        "n_lon": args.n_lon,
        "axis_grid_size": args.n_lat * args.n_lon,
    }

    args.outdir.mkdir(parents=True, exist_ok=True)
    write_csv(args.outdir / "directional_axis_high_ell_leakage_null_samples.csv", rows)
    (args.outdir / "directional_axis_high_ell_leakage_null_summary.json").write_text(
        json.dumps(summary, indent=2) + "\n", encoding="utf-8"
    )
    make_report(args.outdir / "directional_axis_high_ell_leakage_null_report.md", summary)

    print(
        json.dumps(
            {
                "n_seeds": summary["n_seeds"],
                "f_sky": summary["mask"]["f_sky"],
                "mask_delta_tail": summary["statistics"]["mask_delta_qo_deg"][
                    "tail_fraction"
                ],
                "joint_tail": summary["statistics"][
                    "joint_unmasked_tight_and_delta_large"
                ]["fraction"],
                "outdir": str(args.outdir),
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
