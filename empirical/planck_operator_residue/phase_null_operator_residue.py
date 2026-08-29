"""Phase-randomized null control for Planck low-ell operator residue.

The null preserves each operator's coefficient magnitudes by (ell, m) and
destroys cross-operator phase alignment for m > 0. The m = 0 coefficients are
randomly sign-flipped. This is a coefficient-level control, not a full CMB
simulation or mask/noise likelihood.
"""

from __future__ import annotations

import argparse
import csv
import json
import math
from pathlib import Path

import numpy as np

from analyze_lowell_operator_residue import coefficient_distance, read_alm_csv


def stability_score(data: dict[str, dict[int, dict[int, complex]]], ell_min: int, ell_max: int) -> float:
    distances: list[float] = []
    operators = sorted(data)
    for i, op_a in enumerate(operators):
        for op_b in operators[i + 1 :]:
            common_ells = sorted(set(data[op_a]) & set(data[op_b]))
            for ell in common_ells:
                if ell_min <= ell <= ell_max:
                    d = coefficient_distance(data[op_a][ell], data[op_b][ell], ell)
                    if not math.isnan(d):
                        distances.append(d)
    return float(np.median(distances))


def pair_scores(data: dict[str, dict[int, dict[int, complex]]], ell_min: int, ell_max: int) -> dict[str, float]:
    out = {}
    operators = sorted(data)
    for i, op_a in enumerate(operators):
        for op_b in operators[i + 1 :]:
            distances: list[float] = []
            for ell in sorted(set(data[op_a]) & set(data[op_b])):
                if ell_min <= ell <= ell_max:
                    d = coefficient_distance(data[op_a][ell], data[op_b][ell], ell)
                    if not math.isnan(d):
                        distances.append(d)
            out[f"{op_a}-{op_b}"] = float(np.median(distances))
    return out


def phase_randomized(
    data: dict[str, dict[int, dict[int, complex]]], rng: np.random.Generator
) -> dict[str, dict[int, dict[int, complex]]]:
    randomized: dict[str, dict[int, dict[int, complex]]] = {}
    for op, ell_map in data.items():
        randomized[op] = {}
        for ell, coeffs in ell_map.items():
            randomized[op][ell] = {}
            for m, z in coeffs.items():
                amp = abs(z)
                if m == 0:
                    randomized[op][ell][m] = amp * (1.0 if rng.random() < 0.5 else -1.0)
                else:
                    phi = rng.uniform(0.0, 2.0 * math.pi)
                    randomized[op][ell][m] = amp * complex(math.cos(phi), math.sin(phi))
    return randomized


def write_rows(path: Path, rows: list[dict[str, object]]) -> None:
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def percentile_rank_less_equal(samples: np.ndarray, observed: float) -> float:
    return float(np.mean(samples <= observed))


def make_report(
    path: Path,
    input_path: Path,
    ell_min: int,
    ell_max: int,
    observed: float,
    samples: np.ndarray,
    seed_count: int,
    pair_observed: dict[str, float],
    pair_null_median: dict[str, float],
) -> None:
    q05, q50, q95 = np.quantile(samples, [0.05, 0.5, 0.95])
    p_low = percentile_rank_less_equal(samples, observed)
    lines = [
        "# Planck Operator-Residue Phase Null",
        "",
        "Status: coefficient-level control, not a full CMB simulation.",
        "",
        "Input:",
        "",
        f"```text\n{input_path}\n```",
        "",
        "Band:",
        "",
        f"```text\n{ell_min} <= ell <= {ell_max}\n```",
        "",
        "Null:",
        "",
        "For each operator and coefficient, preserve `|a_lm|` and randomize phase",
        "independently for `m > 0`; randomly sign-flip `m = 0`.",
        "",
        "Headline:",
        "",
        f"```text\nobserved stability score = {observed:.6g}\n"
        f"null median = {q50:.6g}\n"
        f"null q05 = {q05:.6g}\n"
        f"null q95 = {q95:.6g}\n"
        f"fraction null <= observed = {p_low:.6g}\n"
        f"n_null = {seed_count}\n```",
        "",
        "Pair medians:",
        "",
        "| pair | observed | null median |",
        "| --- | ---: | ---: |",
        *[
            f"| `{pair}` | {pair_observed[pair]:.6g} | {pair_null_median[pair]:.6g} |"
            for pair in sorted(pair_observed)
        ],
        "",
        "Interpretation:",
        "",
        "This null asks whether cross-operator closeness depends on phase alignment",
        "rather than only on each operator's low-ell power. If the observed score",
        "is far below the randomized null, the operators share more aligned",
        "low-ell structure than expected from their per-coefficient amplitudes",
        "alone.",
        "",
        "Allowed claim:",
        "",
        "> The observed operator-residue score is compared against a phase-randomized",
        "> coefficient-level null.",
        "",
        "Forbidden claim:",
        "",
        "> This null alone proves AOC, a false bottom, cosmic torque, or a physical",
        "> origin-boundary effect.",
    ]
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument(
        "--outdir",
        type=Path,
        default=Path("reports/planck_operator_residue/phase_null"),
    )
    parser.add_argument("--ell-min", type=int, default=2)
    parser.add_argument("--ell-max", type=int, default=30)
    parser.add_argument("--seeds", type=int, default=1000)
    parser.add_argument("--seed", type=int, default=20260428)
    args = parser.parse_args()

    args.outdir.mkdir(parents=True, exist_ok=True)
    data = read_alm_csv(args.input)
    observed = stability_score(data, args.ell_min, args.ell_max)
    observed_pairs = pair_scores(data, args.ell_min, args.ell_max)

    rng = np.random.default_rng(args.seed)
    rows: list[dict[str, object]] = []
    pair_samples: dict[str, list[float]] = {pair: [] for pair in observed_pairs}
    for idx in range(args.seeds):
        randomized = phase_randomized(data, rng)
        score = stability_score(randomized, args.ell_min, args.ell_max)
        rows.append({"seed_index": idx, "stability_score": score})
        for pair, value in pair_scores(randomized, args.ell_min, args.ell_max).items():
            pair_samples[pair].append(value)

    samples = np.array([float(row["stability_score"]) for row in rows])
    pair_null_median = {pair: float(np.median(values)) for pair, values in pair_samples.items()}

    write_rows(args.outdir / "phase_null_scores.csv", rows)
    pair_rows = [
        {
            "pair": pair,
            "observed": observed_pairs[pair],
            "null_median": pair_null_median[pair],
            "null_q05": float(np.quantile(pair_samples[pair], 0.05)),
            "null_q95": float(np.quantile(pair_samples[pair], 0.95)),
        }
        for pair in sorted(observed_pairs)
    ]
    write_rows(args.outdir / "phase_null_pair_scores.csv", pair_rows)

    summary = {
        "input": str(args.input),
        "ell_min": args.ell_min,
        "ell_max": args.ell_max,
        "seed": args.seed,
        "seed_count": args.seeds,
        "observed_stability_score": observed,
        "null_mean": float(np.mean(samples)),
        "null_median": float(np.median(samples)),
        "null_q05": float(np.quantile(samples, 0.05)),
        "null_q95": float(np.quantile(samples, 0.95)),
        "fraction_null_less_equal_observed": percentile_rank_less_equal(samples, observed),
        "observed_pair_scores": observed_pairs,
        "null_pair_median": pair_null_median,
    }
    (args.outdir / "phase_null_summary.json").write_text(
        json.dumps(summary, indent=2) + "\n", encoding="utf-8"
    )
    make_report(
        args.outdir / "phase_null_report.md",
        args.input,
        args.ell_min,
        args.ell_max,
        observed,
        samples,
        args.seeds,
        observed_pairs,
        pair_null_median,
    )
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()

