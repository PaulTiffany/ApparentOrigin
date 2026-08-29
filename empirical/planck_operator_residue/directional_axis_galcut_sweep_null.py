"""Isotropic threshold-sweep null for the galcut directional-axis curve.

This controls the mask-threshold feature found in
directional_axis_galcut_sweep.py. It draws isotropic ell=2 and ell=3 skies,
applies the same family of synthetic galactic cuts, extracts pseudo-alms, and
measures whether the observed 20->25 deg Q-O cliff is typical.

Phase tag: empirical control. This is not an official Planck mask likelihood
and does not simulate component separation, beam, detector noise, foregrounds,
or high-ell leakage.
"""

from __future__ import annotations

import argparse
import csv
import json
import math
from pathlib import Path

import numpy as np

from directional_axis_masked_sky_null import (
    draw_lowell_sky,
    extract_pseudo_coeffs,
    q_o_angle,
    synthesize_map,
)
from directional_axis_null_sim import (
    fibonacci_positions,
    percentile_geq,
    precompute_projection,
    real_coeff_basis,
)


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_OBSERVED = (
    ROOT
    / "reports"
    / "planck_operator_residue"
    / "directional_axis_galcut_sweep"
    / "directional_axis_galcut_sweep_summary.json"
)
DEFAULT_OUT = (
    ROOT
    / "reports"
    / "planck_operator_residue"
    / "directional_axis_galcut_sweep_null"
)


def parse_cuts(value: str) -> list[float]:
    return [float(part.strip()) for part in value.split(",") if part.strip()]


def cut_label(cut: float) -> str:
    if float(cut).is_integer():
        return str(int(cut))
    return str(cut).replace(".", "p")


def load_observed(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def metric_by_cut(summary: dict) -> dict[float, dict]:
    return {float(row["cut_deg"]): row for row in summary["metrics"]}


def synthetic_mask_from_positions(positions: np.ndarray, cut: float) -> np.ndarray:
    z = positions[2]
    lat = np.degrees(np.arcsin(np.clip(z, -1.0, 1.0)))
    return (np.abs(lat) > cut).astype(float)


def jump_stats(qo_by_cut: dict[float, float], cuts: list[float]) -> dict[str, float]:
    jumps: dict[str, float] = {}
    max_jump = -1.0
    max_from = cuts[0]
    max_to = cuts[1]
    for left, right in zip(cuts, cuts[1:]):
        jump = abs(qo_by_cut[right] - qo_by_cut[left])
        key = f"jump_{cut_label(left)}_{cut_label(right)}_deg"
        jumps[key] = jump
        if jump > max_jump:
            max_jump = jump
            max_from = left
            max_to = right
    jumps["max_adjacent_jump_deg"] = max_jump
    jumps["max_adjacent_jump_from_deg"] = max_from
    jumps["max_adjacent_jump_to_deg"] = max_to
    return jumps


def observed_stats(observed: dict, cuts: list[float]) -> dict:
    by_cut = metric_by_cut(observed)
    qo = {cut: float(by_cut[cut]["qo_median_deg"]) for cut in cuts}
    jumps = jump_stats(qo, cuts)
    return {
        "qo_by_cut": qo,
        "jumps": jumps,
        "jump_20_25_deg": jumps["jump_20_25_deg"],
        "max_adjacent_jump_deg": jumps["max_adjacent_jump_deg"],
    }


def summarize(
    rows: list[dict[str, float | int]],
    observed: dict,
    cuts: list[float],
    f_sky_by_cut: dict[float, float],
) -> dict:
    obs = observed_stats(observed, cuts)

    def vals(key: str) -> list[float]:
        return [float(row[key]) for row in rows]

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

    return {
        "status": "isotropic low-ell galcut threshold-sweep null",
        "n_seeds": len(rows),
        "cuts_deg": cuts,
        "f_sky_by_cut": {str(key): value for key, value in f_sky_by_cut.items()},
        "observed": obs,
        "statistics": {
            "per_cut_qo_angle_deg": per_cut,
            "jump_20_25_deg": stat_block("jump_20_25_deg", obs["jump_20_25_deg"]),
            "max_adjacent_jump_deg": stat_block(
                "max_adjacent_jump_deg", obs["max_adjacent_jump_deg"]
            ),
        },
        "limitations": [
            "No Planck component-separation operators are simulated.",
            "No beam, detector noise, foregrounds, inpainting, or official Planck mask is simulated.",
            "Only ell=2 and ell=3 are generated, so leakage from higher multipoles is absent.",
            "The extraction uses direct pseudo-alms with mean subtraction, matching the fallback extractor convention.",
            "This is a null for the threshold-sweep shape, not a Planck likelihood.",
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
    lines = [
        "# Directional Axis Galcut Sweep Null",
        "",
        "Status: isotropic low-ell threshold-sweep null for the synthetic galactic",
        "cut directional-axis curve.",
        "",
        "## Question",
        "",
        "Under isotropic ell=2/ell=3 skies, how often does the same synthetic",
        "cut family produce a Q-O cliff at least as large as the Planck",
        "`20 -> 25 deg` threshold feature?",
        "",
        "## Setup",
        "",
        f"- Seeds: {summary['n_seeds']}",
        f"- Cuts: {', '.join(str(cut) for cut in summary['cuts_deg'])} deg",
        "- Sky prior: isotropic Gaussian ell=2 and ell=3 only, with",
        "  `C_ell proportional to 1/[ell(ell+1)]`",
        "- Extraction: direct pseudo-alms with mean subtraction on retained sky",
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
            "The specific threshold statistic and the look-elsewhere statistic must",
            "both be read. `jump_20_25_deg` asks whether the observed cliff at the",
            "pre-named threshold is unusual. `max_adjacent_jump_deg` asks whether a",
            "cliff this large anywhere in the seven-cut sweep is unusual.",
            "",
            f"In this null, the named threshold cliff has tail `{jump['tail_fraction']:.4g}`",
            f"and the sweep-level look-elsewhere tail is `{max_jump['tail_fraction']:.4g}`.",
            "The high Q-O value at `cut=25` alone is less diagnostic than the",
            "adjacent discontinuity: the statistic is about recomposition across a",
            "changing mask contract, not simply about one large masked-sky angle.",
            "",
            "## Allowed Claims",
            "",
            "1. This null tests whether the observed galcut-threshold cliff is typical",
            "   under isotropic low-ell skies and the same synthetic mask family.",
            "2. It controls the Opticks-induced hypothesis by converting the visual",
            "   sector transition back into a numeric statistic.",
            "3. It can motivate a high-ell leakage or official-mask sweep if the",
            "   threshold feature remains uncommon.",
            "",
            "## Forbidden Claims",
            "",
            "1. This proves or refutes AOC.",
            "2. This replaces a full Planck likelihood or official mask analysis.",
            "3. This simulates component-separation pipelines or foregrounds.",
            "4. A rare threshold feature is automatically a cosmological transition.",
            "",
            "## Limitations",
            "",
            *[f"- {item}" for item in summary["limitations"]],
            "",
        ]
    )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--outdir", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--observed-summary", type=Path, default=DEFAULT_OBSERVED)
    parser.add_argument("--cuts", default="0,5,10,15,20,25,30")
    parser.add_argument("--seeds", type=int, default=1000)
    parser.add_argument("--seed", type=int, default=20260429)
    parser.add_argument("--map-nside", type=int, default=64)
    parser.add_argument("--projection-nside", type=int, default=16)
    parser.add_argument("--n-lat", type=int, default=37)
    parser.add_argument("--n-lon", type=int, default=72)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    cuts = parse_cuts(args.cuts)
    observed = load_observed(args.observed_summary)
    positions = fibonacci_positions(12 * args.map_nside * args.map_nside)
    masks = {cut: synthetic_mask_from_positions(positions, cut) for cut in cuts}
    f_sky_by_cut = {cut: float(np.mean(mask > 0.5)) for cut, mask in masks.items()}
    basis = {ell: real_coeff_basis(ell, args.map_nside)[0] for ell in (2, 3)}
    projections = {
        ell: precompute_projection(ell, args.projection_nside, args.n_lat, args.n_lon)
        for ell in (2, 3)
    }

    rng = np.random.default_rng(args.seed)
    rows: list[dict[str, float | int]] = []
    for idx in range(args.seeds):
        sky_coeffs = draw_lowell_sky(rng)
        sky_map = synthesize_map(sky_coeffs, basis)
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

    summary = summarize(rows, observed, cuts, f_sky_by_cut)
    summary["simulation_parameters"] = {
        "seed": args.seed,
        "map_nside": args.map_nside,
        "projection_nside": args.projection_nside,
        "n_lat": args.n_lat,
        "n_lon": args.n_lon,
        "axis_grid_size": args.n_lat * args.n_lon,
        "observed_summary": str(args.observed_summary),
    }

    args.outdir.mkdir(parents=True, exist_ok=True)
    write_csv(args.outdir / "directional_axis_galcut_sweep_null_samples.csv", rows)
    (args.outdir / "directional_axis_galcut_sweep_null_summary.json").write_text(
        json.dumps(summary, indent=2) + "\n", encoding="utf-8"
    )
    make_report(args.outdir / "directional_axis_galcut_sweep_null_report.md", summary)
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
                "outdir": str(args.outdir),
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
