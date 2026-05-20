"""High-ell leakage threshold-sweep null for the galcut directional curve.

This is P2 from docs/planck_directional_threshold_prediction_contract.md. It
extends the low-ell galcut sweep null by drawing isotropic Gaussian skies
through ell=30 before applying the same synthetic cut family and extracting
pseudo ell=2/3 coefficients.

Frozen decision boundary:
    If the look-elsewhere tail for the observed 51.51 deg adjacent jump rises
    above 0.05, simple high-ell leakage plausibly explains the Planck cliff
    under this control. If it remains below 0.05, simple leakage alone does
    not explain the cliff under this control.
"""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

import numpy as np
from scipy.special import sph_harm

from directional_axis_galcut_sweep_null import (
    DEFAULT_OBSERVED,
    cut_label,
    jump_stats,
    load_observed,
    observed_stats,
    parse_cuts,
    synthetic_mask_from_positions,
)
from directional_axis_masked_sky_null import extract_pseudo_coeffs, q_o_angle
from directional_axis_null_sim import (
    fibonacci_positions,
    percentile_geq,
    precompute_projection,
    random_real_alm_coeffs,
)


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_OUT = (
    ROOT
    / "reports"
    / "planck_operator_residue"
    / "directional_axis_galcut_sweep_high_ell_null"
)


def flat_sachs_wolfe_scale(ell: int) -> float:
    return float(np.sqrt(1.0 / float(ell * (ell + 1))))


def real_basis_for_ell(ell: int, positions: np.ndarray) -> np.ndarray:
    """Real-map basis columns: a_l0, Re/Im a_lm for m>0."""
    x, y, z = positions
    phi = np.arctan2(y, x)
    theta = np.arccos(np.clip(z, -1.0, 1.0))
    cols = [sph_harm(0, ell, phi, theta).real]
    for m in range(1, ell + 1):
        ylm = sph_harm(m, ell, phi, theta)
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


def summarize(
    rows: list[dict[str, float | int]],
    observed: dict,
    cuts: list[float],
    f_sky_by_cut: dict[float, float],
    ell_max: int,
    high_ell_scale: float,
) -> dict:
    obs = observed_stats(observed, cuts)

    def vals(key: str) -> list[float]:
        return [float(row[key]) for row in rows]

    def stat_block(key: str, observed_value: float) -> dict:
        samples = vals(key)
        return {
            "observed": observed_value,
            "null_mean": float(np.mean(samples)),
            "null_median": float(np.median(samples)),
            "null_q05": float(np.quantile(samples, 0.05)),
            "null_q95": float(np.quantile(samples, 0.95)),
            "tail_definition": ">= observed",
            "tail_fraction": percentile_geq(samples, observed_value),
        }

    per_cut = {}
    for cut in cuts:
        key = f"qo_cut_{cut_label(cut)}_deg"
        observed_value = obs["qo_by_cut"][cut]
        samples = vals(key)
        per_cut[str(cut)] = {
            "observed": observed_value,
            "null_median": float(np.median(samples)),
            "null_q05": float(np.quantile(samples, 0.05)),
            "null_q95": float(np.quantile(samples, 0.95)),
            "tail_ge_observed": percentile_geq(samples, observed_value),
        }

    max_jump = stat_block("max_adjacent_jump_deg", obs["max_adjacent_jump_deg"])
    decision = (
        "leakage_explains_under_control"
        if max_jump["tail_fraction"] > 0.05
        else "leakage_does_not_explain_under_control"
    )

    return {
        "status": "high-ell leakage galcut threshold-sweep null",
        "n_seeds": len(rows),
        "cuts_deg": cuts,
        "ell_max": ell_max,
        "high_ell_scale": high_ell_scale,
        "cl_prior": f"C_ell proportional to 1/[ell(ell+1)] for 2<=ell<={ell_max}",
        "f_sky_by_cut": {str(key): value for key, value in f_sky_by_cut.items()},
        "observed": obs,
        "statistics": {
            "per_cut_qo_angle_deg": per_cut,
            "jump_20_25_deg": stat_block("jump_20_25_deg", obs["jump_20_25_deg"]),
            "max_adjacent_jump_deg": max_jump,
        },
        "p2_decision_boundary": {
            "tail_metric": "max_adjacent_jump_deg",
            "threshold": 0.05,
            "rule": "tail > 0.05 means simple leakage plausibly explains the cliff under this control; tail <= 0.05 means it does not",
            "result": decision,
        },
        "limitations": [
            "No Planck component-separation operators are simulated.",
            "No beam, detector noise, foregrounds, inpainting, or official Planck mask is simulated.",
            "High-ell content uses a simple flat-Sachs-Wolfe-like power law, not a precision LambdaCDM Cl.",
            "The extraction uses direct pseudo-alms with mean subtraction, matching the fallback extractor convention.",
            "This is a high-ell leakage control for the threshold-sweep shape, not a Planck likelihood.",
        ],
    }


def write_csv(path: Path, rows: list[dict[str, float | int]]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def make_report(path: Path, summary: dict) -> None:
    stats = summary["statistics"]
    jump = stats["jump_20_25_deg"]
    max_jump = stats["max_adjacent_jump_deg"]
    decision = summary["p2_decision_boundary"]
    lines = [
        "# Directional Axis Galcut Sweep High-Ell Leakage Null",
        "",
        "Status: P2 high-ell leakage threshold-sweep null.",
        "",
        "## Question",
        "",
        "Does simple isotropic high-ell leakage through the synthetic galactic",
        "cut family make the observed Planck adjacent Q-O cliff ordinary?",
        "",
        "## Setup",
        "",
        f"- Seeds: {summary['n_seeds']}",
        f"- Cuts: {', '.join(str(cut) for cut in summary['cuts_deg'])} deg",
        f"- Multipoles: `2 <= ell <= {summary['ell_max']}`",
        f"- High-ell scale: `{summary['high_ell_scale']}`",
        f"- Prior: {summary['cl_prior']}",
        "- Extraction: direct pseudo-alms at ell=2 and ell=3 after masking",
        "",
        "## Frozen P2 Decision Boundary",
        "",
        f"- Metric: `{decision['tail_metric']}`",
        f"- Boundary: `{decision['threshold']}`",
        f"- Rule: {decision['rule']}",
        f"- Result: `{decision['result']}`",
        "",
        "## Tail Fractions",
        "",
        "| metric | observed | null median | 5-95% null | tail |",
        "| --- | ---: | ---: | ---: | ---: |",
        (
            f"| `jump_20_25_deg` | {jump['observed']:.4g} | "
            f"{jump['null_median']:.4g} | {jump['null_q05']:.4g}-{jump['null_q95']:.4g} | "
            f"{jump['tail_fraction']:.4g} |"
        ),
        (
            f"| `max_adjacent_jump_deg` | {max_jump['observed']:.4g} | "
            f"{max_jump['null_median']:.4g} | {max_jump['null_q05']:.4g}-{max_jump['null_q95']:.4g} | "
            f"{max_jump['tail_fraction']:.4g} |"
        ),
        "",
        "Per-cut Q-O tails:",
        "",
        "| cut | observed Q-O | null median | 5-95% null | tail >= observed |",
        "| ---: | ---: | ---: | ---: | ---: |",
    ]
    for cut in summary["cuts_deg"]:
        block = stats["per_cut_qo_angle_deg"][str(cut)]
        lines.append(
            f"| {cut:.1f} | {block['observed']:.4g} | {block['null_median']:.4g} | "
            f"{block['null_q05']:.4g}-{block['null_q95']:.4g} | "
            f"{block['tail_ge_observed']:.4g} |"
        )

    lines.extend(
        [
            "",
            "## Readout",
            "",
            "This is the predeclared P2 fork. If the look-elsewhere tail rises above",
            "`0.05`, simple high-ell leakage is enough to make the observed adjacent",
            "cliff ordinary under this control. If it remains below `0.05`, simple",
            "leakage does not explain the cliff here, and the official-mask",
            "specificity control becomes the next meaningful test.",
            "",
            "## Allowed Claims",
            "",
            "1. This tests whether simple high-ell leakage explains the galcut",
            "   threshold cliff under the stated synthetic-mask null.",
            "2. The P2 decision boundary was frozen before this run.",
            "3. The result can decide whether P3 official-mask specificity is worth",
            "   prioritizing.",
            "",
            "## Forbidden Claims",
            "",
            "1. This proves or refutes AOC.",
            "2. This replaces a full Planck likelihood or official mask analysis.",
            "3. This simulates component separation, beam, detector noise, or",
            "   foreground physics.",
            "4. Either P2 fork counts as confirmation of the framework.",
            "",
            "## Limitations",
            "",
            *[f"- {item}" for item in summary["limitations"]],
            "",
        ]
    )
    path.write_text("\n".join(lines), encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--outdir", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--observed-summary", type=Path, default=DEFAULT_OBSERVED)
    parser.add_argument("--cuts", default="0,5,10,15,20,25,30")
    parser.add_argument("--seeds", type=int, default=1000)
    parser.add_argument("--seed", type=int, default=20260429)
    parser.add_argument("--map-nside", type=int, default=32)
    parser.add_argument("--projection-nside", type=int, default=16)
    parser.add_argument("--ell-max", type=int, default=30)
    parser.add_argument("--high-ell-scale", type=float, default=1.0)
    parser.add_argument("--n-lat", type=int, default=37)
    parser.add_argument("--n-lon", type=int, default=72)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    cuts = parse_cuts(args.cuts)
    observed = load_observed(args.observed_summary)
    positions = fibonacci_positions(12 * args.map_nside * args.map_nside)
    synthesis_basis, _ = build_synthesis_basis(positions, 2, args.ell_max)
    masks = {cut: synthetic_mask_from_positions(positions, cut) for cut in cuts}
    f_sky_by_cut = {cut: float(np.mean(mask > 0.5)) for cut, mask in masks.items()}
    projections = {
        ell: precompute_projection(ell, args.projection_nside, args.n_lat, args.n_lon)
        for ell in (2, 3)
    }

    rng = np.random.default_rng(args.seed)
    rows: list[dict[str, float | int]] = []
    for idx in range(args.seeds):
        coeff_vector = draw_coeff_vector(rng, 2, args.ell_max, args.high_ell_scale)
        sky_map = synthesis_basis @ coeff_vector
        qo_by_cut: dict[float, float] = {}
        for cut in cuts:
            coeffs = extract_pseudo_coeffs(sky_map, positions, masks[cut])
            qo_by_cut[cut] = q_o_angle(coeffs, projections)
        jumps = jump_stats(qo_by_cut, cuts)
        row: dict[str, float | int] = {"seed": idx}
        for cut in cuts:
            row[f"qo_cut_{cut_label(cut)}_deg"] = qo_by_cut[cut]
        row["jump_20_25_deg"] = jumps["jump_20_25_deg"]
        row["max_adjacent_jump_deg"] = jumps["max_adjacent_jump_deg"]
        row["max_adjacent_jump_from_deg"] = jumps["max_adjacent_jump_from_deg"]
        row["max_adjacent_jump_to_deg"] = jumps["max_adjacent_jump_to_deg"]
        rows.append(row)

    summary = summarize(
        rows,
        observed,
        cuts,
        f_sky_by_cut,
        ell_max=args.ell_max,
        high_ell_scale=args.high_ell_scale,
    )
    summary["simulation_parameters"] = {
        "seed": args.seed,
        "map_nside": args.map_nside,
        "projection_nside": args.projection_nside,
        "ell_max": args.ell_max,
        "high_ell_scale": args.high_ell_scale,
        "n_lat": args.n_lat,
        "n_lon": args.n_lon,
        "axis_grid_size": args.n_lat * args.n_lon,
        "observed_summary": str(args.observed_summary),
    }

    args.outdir.mkdir(parents=True, exist_ok=True)
    write_csv(args.outdir / "directional_axis_galcut_sweep_high_ell_null_samples.csv", rows)
    (args.outdir / "directional_axis_galcut_sweep_high_ell_null_summary.json").write_text(
        json.dumps(summary, indent=2) + "\n", encoding="utf-8"
    )
    make_report(
        args.outdir / "directional_axis_galcut_sweep_high_ell_null_report.md",
        summary,
    )
    print(
        json.dumps(
            {
                "n_seeds": summary["n_seeds"],
                "jump_20_25_tail": summary["statistics"]["jump_20_25_deg"][
                    "tail_fraction"
                ],
                "max_adjacent_jump_tail": summary["statistics"]["max_adjacent_jump_deg"][
                    "tail_fraction"
                ],
                "p2_result": summary["p2_decision_boundary"]["result"],
                "outdir": str(args.outdir),
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
