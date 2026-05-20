"""Compute the demask-shift SharedShift metrics from declared axis rows.

Input CSV columns:

    voice,mask,band,x,y,z,grade

`grade` is optional. Rows with grade D are reported only if
`--include-diagnostic` is set; by default they do not enter the primary metric.
"""

from __future__ import annotations

import argparse
import csv
import math
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
    m = median(values)
    return float(median([abs(v - m) for v in values]))


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


def build_index(
    rows: list[AxisRow],
) -> dict[tuple[str, str, str], AxisRow]:
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


def write_results(path: Path, results: list[dict[str, str | int | float]]) -> None:
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
        writer.writerows(results)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--axes-csv", required=True, type=Path)
    parser.add_argument("--out-csv", required=True, type=Path)
    parser.add_argument(
        "--transitions",
        default="M0:M1,M1:M2,M2:M3,M0:M2,M0:M4",
        help="comma-separated Ma:Mb transitions",
    )
    parser.add_argument("--delta-min-deg", default=2.0, type=float)
    parser.add_argument("--epsilon-deg", default=2.0, type=float)
    parser.add_argument("--d-iso-deg", default=57.0, type=float)
    parser.add_argument(
        "--include-diagnostic",
        action="store_true",
        help="include grade-D diagnostic voices in the metric",
    )
    args = parser.parse_args()

    rows = read_axes(args.axes_csv, include_diagnostic=args.include_diagnostic)
    results = compute_results(
        rows=rows,
        transitions=parse_transitions(args.transitions),
        delta_min_deg=args.delta_min_deg,
        epsilon_deg=args.epsilon_deg,
        d_iso_deg=args.d_iso_deg,
    )
    write_results(args.out_csv, results)


if __name__ == "__main__":
    main()

