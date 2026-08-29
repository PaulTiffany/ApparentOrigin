"""Analyze low-ell operator residue from exported Planck a_lm coefficients.

Input CSV columns:
    operator, ell, m, alm_real, alm_imag

Aliases accepted for coefficient columns:
    real, imag

This script intentionally does not read FITS or HEALPix maps. Map extraction is
a separate operator step that should be performed with healpy/astropy and
recorded in provenance.
"""

from __future__ import annotations

import argparse
import csv
import json
import math
from collections import defaultdict
from itertools import combinations
from pathlib import Path

import numpy as np


def read_alm_csv(path: Path) -> dict[str, dict[int, dict[int, complex]]]:
    by_operator: dict[str, dict[int, dict[int, complex]]] = defaultdict(
        lambda: defaultdict(dict)
    )
    with path.open("r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        required = {"operator", "ell", "m"}
        missing = required - set(reader.fieldnames or [])
        if missing:
            raise ValueError(f"missing columns: {sorted(missing)}")

        real_col = "alm_real" if "alm_real" in reader.fieldnames else "real"
        imag_col = "alm_imag" if "alm_imag" in reader.fieldnames else "imag"
        if real_col not in reader.fieldnames or imag_col not in reader.fieldnames:
            raise ValueError("missing alm_real/alm_imag columns")

        for row in reader:
            op = row["operator"].strip()
            ell = int(row["ell"])
            m = int(row["m"])
            real = float(row[real_col])
            imag = float(row[imag_col])
            if m < 0:
                raise ValueError("expected m >= 0 coefficients for real-map convention")
            by_operator[op][ell][m] = complex(real, imag)

    return {op: dict(ells) for op, ells in by_operator.items()}


def cl_and_entropy(coeffs: dict[int, complex], ell: int) -> tuple[float, float]:
    expected = set(range(ell + 1))
    missing = expected - set(coeffs)
    if missing:
        raise ValueError(f"ell={ell} missing m values: {sorted(missing)}")

    weighted_power = []
    for m in range(ell + 1):
        weight = 1.0 if m == 0 else 2.0
        weighted_power.append(weight * abs(coeffs[m]) ** 2)

    total = float(sum(weighted_power))
    cl = total / float(2 * ell + 1)
    if total <= 0:
        return cl, float("nan")

    p = np.array(weighted_power, dtype=float) / total
    entropy = -float(np.sum(np.where(p > 0, p * np.log(p), 0.0)))
    normalized_entropy = entropy / math.log(2 * ell + 1)
    return cl, normalized_entropy


def summarize_operator(
    op: str, ell_map: dict[int, dict[int, complex]], ell_min: int, ell_max: int
) -> list[dict[str, float | int | str]]:
    rows = []
    for ell in range(ell_min, ell_max + 1):
        if ell not in ell_map:
            continue
        cl, entropy = cl_and_entropy(ell_map[ell], ell)
        rows.append(
            {
                "operator": op,
                "ell": ell,
                "cl": cl,
                "normalized_entropy": entropy,
                "parity": "even" if ell % 2 == 0 else "odd",
            }
        )
    return rows


def coefficient_distance(
    a: dict[int, complex], b: dict[int, complex], ell: int
) -> float:
    shared = sorted(set(a) & set(b))
    if set(shared) != set(range(ell + 1)):
        raise ValueError(f"ell={ell} pair missing shared m coefficients")

    numerator = 0.0
    denominator = 0.0
    for m in shared:
        weight = 1.0 if m == 0 else 2.0
        numerator += weight * abs(a[m] - b[m]) ** 2
        denominator += weight * (abs(a[m]) ** 2 + abs(b[m]) ** 2) / 2.0

    if denominator <= 0:
        return float("nan")
    return math.sqrt(numerator / denominator)


def summarize_pairs(
    data: dict[str, dict[int, dict[int, complex]]], ell_min: int, ell_max: int
) -> list[dict[str, float | int | str]]:
    rows = []
    for op_a, op_b in combinations(sorted(data), 2):
        common_ells = sorted(set(data[op_a]) & set(data[op_b]))
        for ell in common_ells:
            if ell < ell_min or ell > ell_max:
                continue
            rows.append(
                {
                    "operator_a": op_a,
                    "operator_b": op_b,
                    "ell": ell,
                    "coefficient_distance": coefficient_distance(
                        data[op_a][ell], data[op_b][ell], ell
                    ),
                }
            )
    return rows


def parity_ratios(operator_rows: list[dict[str, float | int | str]]) -> dict[str, float]:
    grouped: dict[str, dict[str, float]] = defaultdict(lambda: {"odd": 0.0, "even": 0.0})
    for row in operator_rows:
        grouped[str(row["operator"])][str(row["parity"])] += float(row["cl"])

    out = {}
    for op, sums in grouped.items():
        out[op] = sums["odd"] / sums["even"] if sums["even"] > 0 else float("nan")
    return out


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def make_report(
    path: Path,
    input_path: Path,
    ell_min: int,
    ell_max: int,
    operators: list[str],
    parity: dict[str, float],
    stability_score: float,
    n_pair_rows: int,
) -> None:
    lines = [
        "# Planck Operator-Residue Report",
        "",
        "Status: generated from low-ell coefficient table.",
        "",
        "Input:",
        "",
        f"```text\n{input_path}\n```",
        "",
        "Band:",
        "",
        f"```text\n{ell_min} <= ell <= {ell_max}\n```",
        "",
        "Operators:",
        "",
        *[f"- `{op}`" for op in operators],
        "",
        "Primary stability score:",
        "",
        f"```text\nmedian pairwise coefficient distance = {stability_score:.6g}\n```",
        "",
        "Parity ratios:",
        "",
        "| operator | odd/even low-ell power |",
        "| --- | ---: |",
        *[f"| `{op}` | {parity[op]:.6g} |" for op in sorted(parity)],
        "",
        "Interpretation:",
        "",
        "This report measures whether the same low-ell coefficients remain stable",
        "across reconstruction operators. It does not interpret stability as AOC",
        "evidence without mask, smoothing, simulation, foreground, and statistic",
        "selection controls.",
        "",
        "Pairwise rows:",
        "",
        f"```text\n{n_pair_rows}\n```",
    ]
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def make_example(path: Path, ell_min: int, ell_max: int) -> None:
    rng = np.random.default_rng(20260427)
    operators = ["Commander", "NILC", "SEVEM", "SMICA"]
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f, fieldnames=["operator", "ell", "m", "alm_real", "alm_imag"]
        )
        writer.writeheader()
        base = {}
        for ell in range(ell_min, ell_max + 1):
            for m in range(ell + 1):
                scale = 1.0 / (ell * (ell + 1))
                base[(ell, m)] = complex(
                    rng.normal(0, scale), rng.normal(0, scale if m > 0 else 0.0)
                )
        for op_idx, op in enumerate(operators):
            noise_scale = 0.04 + 0.01 * op_idx
            for ell in range(ell_min, ell_max + 1):
                for m in range(ell + 1):
                    b = base[(ell, m)]
                    perturb = complex(
                        rng.normal(0, noise_scale * abs(b) + 1e-8),
                        rng.normal(0, noise_scale * abs(b) + 1e-8) if m > 0 else 0.0,
                    )
                    z = b + perturb
                    writer.writerow(
                        {
                            "operator": op,
                            "ell": ell,
                            "m": m,
                            "alm_real": z.real,
                            "alm_imag": z.imag,
                        }
                    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path)
    parser.add_argument("--outdir", type=Path, default=Path("reports/planck_operator_residue"))
    parser.add_argument("--ell-min", type=int, default=2)
    parser.add_argument("--ell-max", type=int, default=30)
    parser.add_argument("--make-example", type=Path)
    args = parser.parse_args()

    if args.make_example:
        args.make_example.parent.mkdir(parents=True, exist_ok=True)
        make_example(args.make_example, args.ell_min, args.ell_max)
        print(f"wrote example coefficients: {args.make_example}")
        return

    if args.input is None:
        raise SystemExit("--input is required unless --make-example is used")

    args.outdir.mkdir(parents=True, exist_ok=True)
    data = read_alm_csv(args.input)
    operator_rows: list[dict[str, float | int | str]] = []
    for op in sorted(data):
        operator_rows.extend(summarize_operator(op, data[op], args.ell_min, args.ell_max))

    pair_rows = summarize_pairs(data, args.ell_min, args.ell_max)
    distances = [
        float(row["coefficient_distance"])
        for row in pair_rows
        if not math.isnan(float(row["coefficient_distance"]))
    ]
    stability_score = float(np.median(distances)) if distances else float("nan")
    parity = parity_ratios(operator_rows)

    write_csv(args.outdir / "lowell_operator_summary.csv", operator_rows)
    write_csv(args.outdir / "lowell_pairwise_distances.csv", pair_rows)

    summary = {
        "input": str(args.input),
        "ell_min": args.ell_min,
        "ell_max": args.ell_max,
        "operators": sorted(data),
        "operator_count": len(data),
        "pairwise_row_count": len(pair_rows),
        "stability_score_median_pairwise_distance": stability_score,
        "odd_even_parity_ratio": parity,
    }
    (args.outdir / "planck_operator_residue_summary.json").write_text(
        json.dumps(summary, indent=2) + "\n", encoding="utf-8"
    )
    make_report(
        args.outdir / "planck_operator_residue_report.md",
        args.input,
        args.ell_min,
        args.ell_max,
        sorted(data),
        parity,
        stability_score,
        len(pair_rows),
    )
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()

