"""CI runner for the Fermi demask-shift SharedShift detector.

The runner is intentionally dependency-light. It can:

1. generate a synthetic smoke-test axis table,
2. download a predeclared axis table from a URL,
3. compute SharedShift metrics for declared mask transitions,
4. write CSV/JSON/Markdown artifacts for GitHub Actions upload.

This is not a Fermi data fetcher yet. A future live Fermi workflow should
replace or precede the axis-table step with a declared Fermi product pipeline.
"""

from __future__ import annotations

import argparse
import csv
import json
import math
import urllib.request
from dataclasses import dataclass
from itertools import combinations
from pathlib import Path
from statistics import median


@dataclass(frozen=True)
class AxisRow:
    voice: str
    mask: str
    band: str
    vector: tuple[float, float, float]
    grade: str


@dataclass(frozen=True)
class Motion:
    voice: str
    delta_deg: float
    axis: tuple[float, float, float] | None
    valid_axis: bool


def dot(a: tuple[float, float, float], b: tuple[float, float, float]) -> float:
    return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]


def cross(
    a: tuple[float, float, float], b: tuple[float, float, float]
) -> tuple[float, float, float]:
    return (
        a[1] * b[2] - a[2] * b[1],
        a[2] * b[0] - a[0] * b[2],
        a[0] * b[1] - a[1] * b[0],
    )


def norm(a: tuple[float, float, float]) -> float:
    return math.sqrt(dot(a, a))


def normalize(a: tuple[float, float, float]) -> tuple[float, float, float]:
    n = norm(a)
    if n == 0:
        raise ValueError("zero-length axis vector")
    return (a[0] / n, a[1] / n, a[2] / n)


def clamp(x: float, lo: float = -1.0, hi: float = 1.0) -> float:
    return max(lo, min(hi, x))


def axial_distance_deg(
    a: tuple[float, float, float], b: tuple[float, float, float]
) -> float:
    return math.degrees(math.acos(clamp(abs(dot(a, b)))))


def signed_partner(
    a: tuple[float, float, float], b: tuple[float, float, float]
) -> tuple[float, float, float]:
    if dot(a, b) >= 0:
        return b
    return (-b[0], -b[1], -b[2])


def mad(values: list[float]) -> float:
    if not values:
        return math.nan
    center = median(values)
    return float(median([abs(v - center) for v in values]))


def median_pairwise_axial_distance(vectors: list[tuple[float, float, float]]) -> float:
    if len(vectors) < 2:
        return math.nan
    distances = [axial_distance_deg(a, b) for a, b in combinations(vectors, 2)]
    return float(median(distances))


def read_axes(path: Path, include_diagnostic: bool) -> list[AxisRow]:
    rows: list[AxisRow] = []
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        required = {"voice", "mask", "band", "x", "y", "z"}
        missing = required - set(reader.fieldnames or [])
        if missing:
            raise ValueError(f"missing required columns: {sorted(missing)}")
        for raw in reader:
            grade = raw.get("grade", "C").strip().upper() or "C"
            if grade == "D" and not include_diagnostic:
                continue
            rows.append(
                AxisRow(
                    voice=raw["voice"].strip(),
                    mask=raw["mask"].strip(),
                    band=raw["band"].strip(),
                    vector=normalize(
                        (float(raw["x"]), float(raw["y"]), float(raw["z"]))
                    ),
                    grade=grade,
                )
            )
    return rows


def build_index(rows: list[AxisRow]) -> dict[tuple[str, str, str], AxisRow]:
    index: dict[tuple[str, str, str], AxisRow] = {}
    for row in rows:
        key = (row.voice, row.mask, row.band)
        if key in index:
            raise ValueError(f"duplicate axis row for {key}")
        index[key] = row
    return index


def compute_motion(
    voice: str,
    a: tuple[float, float, float],
    b: tuple[float, float, float],
    delta_min_deg: float,
    epsilon_deg: float,
) -> Motion:
    b_signed = signed_partner(a, b)
    delta = axial_distance_deg(a, b_signed)
    unstable = delta > 90.0 - epsilon_deg
    if delta < delta_min_deg or unstable:
        return Motion(voice=voice, delta_deg=delta, axis=None, valid_axis=False)
    axis = normalize(cross(a, b_signed))
    return Motion(voice=voice, delta_deg=delta, axis=axis, valid_axis=True)


def compute_results(
    rows: list[AxisRow],
    transitions: list[tuple[str, str]],
    delta_min_deg: float,
    epsilon_deg: float,
    d_iso_deg: float,
) -> list[dict[str, str | int | float]]:
    index = build_index(rows)
    voices = sorted({row.voice for row in rows})
    bands = sorted({row.band for row in rows})
    results: list[dict[str, str | int | float]] = []

    for band in bands:
        for mask_a, mask_b in transitions:
            endpoint_vectors: list[tuple[float, float, float]] = []
            motions: list[Motion] = []
            for voice in voices:
                left = index.get((voice, mask_a, band))
                right = index.get((voice, mask_b, band))
                if left is None or right is None:
                    continue
                endpoint_vectors.append(right.vector)
                motions.append(
                    compute_motion(
                        voice=voice,
                        a=left.vector,
                        b=right.vector,
                        delta_min_deg=delta_min_deg,
                        epsilon_deg=epsilon_deg,
                    )
                )

            valid_axes = [motion.axis for motion in motions if motion.valid_axis]
            valid_axes = [axis for axis in valid_axes if axis is not None]
            d_axis = median_pairwise_axial_distance(valid_axes)
            r_axis = math.nan if math.isnan(d_axis) else 1.0 - d_axis / d_iso_deg
            deltas = [motion.delta_deg for motion in motions]

            results.append(
                {
                    "mask_transition": f"{mask_a}->{mask_b}",
                    "band": band,
                    "n_voices": len(motions),
                    "n_valid_rotation_axes": len(valid_axes),
                    "D_op_deg": median_pairwise_axial_distance(endpoint_vectors),
                    "D_motion_mad_deg": mad(deltas),
                    "R_axis": r_axis,
                    "median_Delta_deg": float(median(deltas)) if deltas else math.nan,
                    "verdict": "numeric_only_no_nulls",
                }
            )
    return results


def parse_transitions(raw: str) -> list[tuple[str, str]]:
    transitions: list[tuple[str, str]] = []
    for item in raw.split(","):
        item = item.strip()
        if not item:
            continue
        if ":" not in item:
            raise ValueError(f"transition must be Ma:Mb, got {item!r}")
        left, right = item.split(":", 1)
        transitions.append((left.strip(), right.strip()))
    if not transitions:
        raise ValueError("at least one transition is required")
    return transitions


def write_csv(path: Path, rows: list[dict[str, str | int | float]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = [
        "mask_transition",
        "band",
        "n_voices",
        "n_valid_rotation_axes",
        "D_op_deg",
        "D_motion_mad_deg",
        "R_axis",
        "median_Delta_deg",
        "verdict",
    ]
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def write_report(path: Path, mode: str, results: list[dict[str, str | int | float]]) -> None:
    lines = [
        "# Fermi Demask-Shift CI Runner Report",
        "",
        f"Mode: `{mode}`.",
        "",
        "Status: CI metric run. Smoke mode is not a Fermi result.",
        "",
        "| transition | band | voices | valid r axes | D_op | D_motion MAD | R_axis | median Delta | verdict |",
        "| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |",
    ]
    for row in results:
        lines.append(
            f"| {row['mask_transition']} | {row['band']} | {row['n_voices']} | "
            f"{row['n_valid_rotation_axes']} | {float(row['D_op_deg']):.3f} | "
            f"{float(row['D_motion_mad_deg']):.3f} | {float(row['R_axis']):.3f} | "
            f"{float(row['median_Delta_deg']):.3f} | {row['verdict']} |"
        )
    lines.extend(
        [
            "",
            "## Allowed Claims",
            "",
            "1. The CI runner executed the SharedShift metric.",
            "2. The artifact is suitable for Desktop GPT inspection.",
            "",
            "## Forbidden Claims",
            "",
            "1. Smoke mode is not a Fermi detection.",
            "2. Numeric-only output is not a calibrated null percentile.",
            "3. Workflow success is not evidence for AOC.",
            "",
        ]
    )
    path.write_text("\n".join(lines), encoding="utf-8")


def write_smoke_axes(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    rows = [
        ("V1", "M0", "low", 1.0, 0.0, 0.0, "B"),
        ("V1", "M1", "low", 0.8660254, 0.5, 0.0, "B"),
        ("V2", "M0", "low", 0.9961947, 0.0871557, 0.0, "B"),
        ("V2", "M1", "low", 0.8191520, 0.5735764, 0.0, "B"),
        ("V3", "M0", "low", 0.9848078, -0.1736482, 0.0, "C"),
        ("V3", "M1", "low", 0.9396926, 0.3420201, 0.0, "C"),
    ]
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(["voice", "mask", "band", "x", "y", "z", "grade"])
        writer.writerows(rows)


def download_axes(url: str, path: Path) -> None:
    if not url:
        raise ValueError("--axes-csv-url is required for mode axes_csv_url")
    path.parent.mkdir(parents=True, exist_ok=True)
    with urllib.request.urlopen(url, timeout=60) as response:
        payload = response.read()
    path.write_bytes(payload)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--mode", choices=["smoke", "axes_csv_url"], default="smoke")
    parser.add_argument("--axes-csv-url", default="")
    parser.add_argument("--transitions", default="M0:M1,M1:M2,M2:M3,M0:M2,M0:M4")
    parser.add_argument("--out-dir", type=Path, required=True)
    parser.add_argument("--delta-min-deg", default=2.0, type=float)
    parser.add_argument("--epsilon-deg", default=2.0, type=float)
    parser.add_argument("--d-iso-deg", default=57.0, type=float)
    parser.add_argument("--include-diagnostic", action="store_true")
    args = parser.parse_args()

    args.out_dir.mkdir(parents=True, exist_ok=True)
    axes_path = args.out_dir / "axes.csv"
    if args.mode == "smoke":
        write_smoke_axes(axes_path)
    else:
        download_axes(args.axes_csv_url, axes_path)

    rows = read_axes(axes_path, include_diagnostic=args.include_diagnostic)
    results = compute_results(
        rows=rows,
        transitions=parse_transitions(args.transitions),
        delta_min_deg=args.delta_min_deg,
        epsilon_deg=args.epsilon_deg,
        d_iso_deg=args.d_iso_deg,
    )
    write_csv(args.out_dir / "shared_shift_metrics.csv", results)
    write_json(
        args.out_dir / "shared_shift_summary.json",
        {
            "mode": args.mode,
            "axes_csv_url": args.axes_csv_url,
            "transitions": args.transitions,
            "delta_min_deg": args.delta_min_deg,
            "epsilon_deg": args.epsilon_deg,
            "d_iso_deg": args.d_iso_deg,
            "results": results,
        },
    )
    write_report(args.out_dir / "shared_shift_report.md", args.mode, results)
    print(f"wrote Fermi demask-shift CI runner artifacts to {args.out_dir}")


if __name__ == "__main__":
    main()

