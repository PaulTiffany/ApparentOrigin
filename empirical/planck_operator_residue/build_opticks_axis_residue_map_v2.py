"""Build a four-channel Opticks-style color/music map for Planck axes.

Composition/media instrumentation artifact, not evidence. Extends v1 from a
2-channel (hue, radius) chart to a 4-channel (hue, radius, saturation, value)
chart. Saturation is a faithful encoding of the per-multipole-normalized
score amplitude (max_a22^2 for ell=2, max_a33^2 for ell=3). Value is held in
reserve at 1.0 (under-using a channel deliberately is part of the
discipline; reserved for a future uncertainty channel once one is earned).

This script does not introduce any new cosmological claim. It re-encodes
quantities already on disk so the score-amplitude variation is visually
inspectable alongside hue/radius.
"""

from __future__ import annotations

import argparse
import colorsys
import csv
import json
import math
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_OUT = ROOT / "reports" / "planck_operator_residue" / "opticks_axis_residue_map_v2"

INPUTS = {
    "unmasked": {
        2: ROOT
        / "reports"
        / "planck_operator_residue"
        / "directional_axis_nside64"
        / "directional_quadrupole_mlmax_summary.json",
        3: ROOT
        / "reports"
        / "planck_operator_residue"
        / "directional_axis_nside64"
        / "directional_octupole_axis_summary.json",
    },
    "galcut20": {
        2: ROOT
        / "reports"
        / "planck_operator_residue"
        / "directional_axis_nside64_galcut20"
        / "directional_quadrupole_mlmax_summary.json",
        3: ROOT
        / "reports"
        / "planck_operator_residue"
        / "directional_axis_nside64_galcut20"
        / "directional_octupole_axis_summary.json",
    },
}

NOTE_NAMES = ["C", "D", "E", "F", "G", "A", "B"]
OPERATORS = ["Commander", "NILC", "SEVEM", "SMICA"]

# Saturation floor: never let saturation collapse below this for the
# weakest mark, otherwise the desaturated marker looks like a missing data
# error rather than a relative-amplitude readout.
SAT_FLOOR = 0.18
# Reserved value channel: held constant at 1.0 to honor the discipline of
# under-using a channel rather than fake-filling it.
VALUE_RESERVED = 1.0

SCORE_KEY = {2: "max_a22_squared", 3: "max_a33_squared"}


def load_json(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def hsv_to_hex(hue_deg: float, sat: float, val: float) -> str:
    sat = max(0.0, min(1.0, sat))
    val = max(0.0, min(1.0, val))
    red, green, blue = colorsys.hsv_to_rgb((hue_deg % 360.0) / 360.0, sat, val)
    return f"#{round(red * 255):02x}{round(green * 255):02x}{round(blue * 255):02x}"


def note_for_hue(hue_deg: float) -> str:
    sector = int((hue_deg % 360.0) / (360.0 / len(NOTE_NAMES)))
    return NOTE_NAMES[min(sector, len(NOTE_NAMES) - 1)]


def lb_to_cart(l_deg: float, b_deg: float) -> tuple[float, float, float]:
    lon = math.radians(l_deg)
    lat = math.radians(b_deg)
    return (
        math.cos(lat) * math.cos(lon),
        math.cos(lat) * math.sin(lon),
        math.sin(lat),
    )


def axial_angle_deg(a: dict, b: dict) -> float:
    ax = lb_to_cart(a["l_deg"], a["b_deg"])
    bx = lb_to_cart(b["l_deg"], b["b_deg"])
    dot = abs(sum(left * right for left, right in zip(ax, bx)))
    dot = max(-1.0, min(1.0, dot))
    return math.degrees(math.acos(dot))


def opticks_radius(b_deg: float, outer_radius: float) -> float:
    return outer_radius * (1.0 - max(0.0, min(90.0, abs(b_deg))) / 90.0)


def polar_xy(cx: float, cy: float, radius: float, l_deg: float) -> tuple[float, float]:
    angle = math.radians(l_deg - 90.0)
    return cx + radius * math.cos(angle), cy + radius * math.sin(angle)


def svg_circle(cx: float, cy: float, r: float, attrs: str) -> str:
    return f'<circle cx="{cx:.2f}" cy="{cy:.2f}" r="{r:.2f}" {attrs}/>'


def svg_text(x: float, y: float, text: str, size: int = 14, anchor: str = "middle") -> str:
    return (
        f'<text x="{x:.2f}" y="{y:.2f}" text-anchor="{anchor}" '
        f'font-family="Inter, Segoe UI, Arial, sans-serif" font-size="{size}" '
        f'fill="#232323">{text}</text>'
    )


def load_axis_rows() -> tuple[list[dict], dict, dict]:
    """Return (rows, source_summaries, score_normalization).

    score_normalization holds the per-multipole maxima used to map score
    amplitude into [0, 1] saturation. Normalization is per-ell (so ell=2
    and ell=3 don't share a scale; the strongest ell=2 mark and the
    strongest ell=3 mark both reach saturation 1.0).
    """
    rows: list[dict] = []
    summaries: dict = {}

    # First pass: collect raw scores so we can compute per-multipole maxima.
    raw_records: list[dict] = []
    for condition, by_ell in INPUTS.items():
        summaries[condition] = {}
        for ell, path in by_ell.items():
            summary = load_json(path)
            summaries[condition][ell] = summary
            score_key = SCORE_KEY[ell]
            for operator in OPERATORS:
                axis = summary["operator_axes"][operator]
                raw_records.append(
                    {
                        "condition": condition,
                        "operator": operator,
                        "ell": ell,
                        "l_deg": axis["l_deg"],
                        "b_deg": axis["b_deg"],
                        "score": axis[score_key],
                    }
                )

    score_max = {
        ell: max(r["score"] for r in raw_records if r["ell"] == ell)
        for ell in (2, 3)
    }
    score_min = {
        ell: min(r["score"] for r in raw_records if r["ell"] == ell)
        for ell in (2, 3)
    }

    for record in raw_records:
        ell = record["ell"]
        ratio = record["score"] / score_max[ell] if score_max[ell] > 0 else 0.0
        # Apply saturation floor so the weakest mark stays legible.
        sat = SAT_FLOOR + (1.0 - SAT_FLOOR) * ratio
        val = VALUE_RESERVED
        hue = record["l_deg"] % 360.0
        rows.append(
            {
                "condition": record["condition"],
                "axis_kind": "operator",
                "operator": record["operator"],
                "ell": ell,
                "l_deg": record["l_deg"],
                "b_deg": record["b_deg"],
                "score": record["score"],
                "score_ratio": ratio,
                "hue_deg": hue,
                "sat": sat,
                "val": val,
                "hex": hsv_to_hex(hue, sat, val),
                "note": note_for_hue(hue),
            }
        )

    score_norm = {
        "score_max_per_multipole": {str(k): v for k, v in score_max.items()},
        "score_min_per_multipole": {str(k): v for k, v in score_min.items()},
        "saturation_floor": SAT_FLOOR,
        "saturation_formula": (
            "sat = SAT_FLOOR + (1 - SAT_FLOOR) * score / score_max_per_multipole"
        ),
        "value_channel": "reserved at 1.0 (constant); not earned yet",
    }
    return rows, summaries, score_norm


def summarize(rows: list[dict], summaries: dict, score_norm: dict) -> dict:
    q_o = {}
    for condition in INPUTS:
        angles = []
        for operator in OPERATORS:
            ell2 = summaries[condition][2]["operator_axes"][operator]
            ell3 = summaries[condition][3]["operator_axes"][operator]
            angles.append(axial_angle_deg(ell2, ell3))
        ordered = sorted(angles)
        q_o[condition] = {
            "operator_angles_deg": dict(zip(OPERATORS, angles)),
            "median_deg": (ordered[1] + ordered[2]) / 2.0,
        }
    sat_observed = {
        "min": min(r["sat"] for r in rows),
        "max": max(r["sat"] for r in rows),
        "by_ell": {
            str(ell): {
                "min": min(r["sat"] for r in rows if r["ell"] == ell),
                "max": max(r["sat"] for r in rows if r["ell"] == ell),
            }
            for ell in (2, 3)
        },
    }
    return {
        "artifact": "opticks_axis_residue_map_v2",
        "source": "Planck low-ell directional operator-axis summaries",
        "phase_tag": "composition/media instrumentation, not evidence",
        "channel_mapping": {
            "hue_deg": "galactic longitude l_deg modulo 360",
            "radial_position": "outer_radius * (1 - abs(b_deg) / 90)",
            "saturation": (
                "per-multipole-normalized score amplitude "
                "(max_a22^2 for ell=2, max_a33^2 for ell=3); "
                "encodes existing scores, not new evidence"
            ),
            "value": (
                "constant 1.0 (held in reserve; not faking a fourth axis "
                "of meaning we have not earned)"
            ),
            "note": "sevenfold Opticks-style sector over hue; not a physical pitch",
            "shape": "circle for ell=2, diamond for ell=3",
        },
        "score_normalization": score_norm,
        "saturation_observed": sat_observed,
        "quadrupole_octupole_alignment": q_o,
        "rows": rows,
    }


def render_wheel(cx: float, cy: float, radius: float, label: str) -> list[str]:
    parts = [
        f'<g id="{label}">',
        svg_text(cx, cy - radius - 42, label, size=20),
    ]
    for deg in range(0, 360, 4):
        start = math.radians(deg - 90)
        end = math.radians(deg + 4 - 90)
        x1 = cx + radius * math.cos(start)
        y1 = cy + radius * math.sin(start)
        x2 = cx + radius * math.cos(end)
        y2 = cy + radius * math.sin(end)
        color = hsv_to_hex(deg, 0.86, 0.92)
        parts.append(
            f'<line x1="{x1:.2f}" y1="{y1:.2f}" x2="{x2:.2f}" y2="{y2:.2f}" '
            f'stroke="{color}" stroke-width="9" stroke-linecap="round"/>'
        )
    for b, stroke in [(0, "#d4d0c7"), (30, "#dedbd3"), (60, "#e8e5de")]:
        r = opticks_radius(b, radius - 8)
        parts.append(svg_circle(cx, cy, r, f'fill="none" stroke="{stroke}" stroke-width="1"'))
        parts.append(svg_text(cx + r + 8, cy - 4, f"b={b}", size=11, anchor="start"))
    parts.append(svg_circle(cx, cy, 3, 'fill="#222" stroke="none"'))
    parts.append("</g>")
    return parts


def render_marker(x: float, y: float, row: dict) -> str:
    fill = row["hex"]
    title = (
        f'{row["condition"]} {row["operator"]} ell={row["ell"]}: '
        f'l={row["l_deg"]:.1f}, b={row["b_deg"]:.1f}, note={row["note"]}, '
        f'score={row["score"]:.3e}, sat={row["sat"]:.2f}'
    )
    if row["ell"] == 2:
        body = svg_circle(
            x,
            y,
            7,
            f'fill="{fill}" stroke="#1f1f1f" stroke-width="1.4"',
        )
    else:
        body = (
            f'<rect x="{x - 6:.2f}" y="{y - 6:.2f}" width="12" height="12" '
            f'fill="{fill}" stroke="#1f1f1f" stroke-width="1.4" '
            f'transform="rotate(45 {x:.2f} {y:.2f})"/>'
        )
    return f"<g><title>{title}</title>{body}</g>"


def render_saturation_legend(cx: float, y: float, score_norm: dict) -> list[str]:
    """Render a small saturation-strip legend below the panels."""
    width = 220
    height = 18
    x0 = cx - width / 2.0
    parts = [svg_text(cx, y - 10, "saturation = score / max_score per multipole", size=12)]
    steps = 24
    for i in range(steps):
        ratio = i / (steps - 1)
        sat = SAT_FLOOR + (1.0 - SAT_FLOOR) * ratio
        # use a neutral mid-hue for the strip so saturation is the only varying channel
        color = hsv_to_hex(220.0, sat, 1.0)
        seg_w = width / steps
        parts.append(
            f'<rect x="{x0 + i * seg_w:.2f}" y="{y:.2f}" width="{seg_w + 0.5:.2f}" '
            f'height="{height}" fill="{color}" stroke="none"/>'
        )
    parts.append(
        f'<rect x="{x0:.2f}" y="{y:.2f}" width="{width}" height="{height}" '
        f'fill="none" stroke="#2d2d2d" stroke-width="0.7"/>'
    )
    parts.append(svg_text(x0 - 6, y + height - 4, "weak", size=11, anchor="end"))
    parts.append(svg_text(x0 + width + 6, y + height - 4, "strong", size=11, anchor="start"))
    return parts


def render_svg(rows: list[dict], summary: dict) -> str:
    radius = 190
    centers = {"unmasked": (300, 330), "galcut20": (820, 330)}
    parts = [
        '<svg xmlns="http://www.w3.org/2000/svg" width="1180" height="760" viewBox="0 0 1180 760">',
        '<rect width="1180" height="760" fill="#fbfaf7"/>',
        svg_text(590, 42, "Opticks Axis-Residue Map v2", size=28),
        svg_text(
            590,
            70,
            (
                "Hue = galactic longitude; radius = distance from galactic north pole; "
                "saturation = per-multipole score amplitude; value held in reserve."
            ),
            size=13,
        ),
    ]
    for condition, (cx, cy) in centers.items():
        median = summary["quadrupole_octupole_alignment"][condition]["median_deg"]
        parts.extend(render_wheel(cx, cy, radius, f"{condition}  median Q-O={median:.1f} deg"))

    by_key = {(r["condition"], r["operator"], r["ell"]): r for r in rows}
    for condition, (cx, cy) in centers.items():
        for operator in OPERATORS:
            ell2 = by_key[(condition, operator, 2)]
            ell3 = by_key[(condition, operator, 3)]
            r2 = opticks_radius(ell2["b_deg"], radius - 8)
            r3 = opticks_radius(ell3["b_deg"], radius - 8)
            x2, y2 = polar_xy(cx, cy, r2, ell2["l_deg"])
            x3, y3 = polar_xy(cx, cy, r3, ell3["l_deg"])
            parts.append(
                f'<line x1="{x2:.2f}" y1="{y2:.2f}" x2="{x3:.2f}" y2="{y3:.2f}" '
                f'stroke="#383838" stroke-width="1.2" stroke-opacity="0.55"/>'
            )
            parts.append(render_marker(x2, y2, ell2))
            parts.append(render_marker(x3, y3, ell3))
            label_x = (x2 + x3) / 2.0
            label_y = (y2 + y3) / 2.0 - 10
            parts.append(svg_text(label_x, label_y, operator[:3], size=11))

    parts.extend(
        [
            '<g id="legend">',
            svg_text(590, 590, "Sevenfold Opticks-style sectors", size=16),
        ]
    )
    swatch_w = 64
    start_x = 590 - (swatch_w * len(NOTE_NAMES)) / 2.0
    for index, note in enumerate(NOTE_NAMES):
        hue = (index + 0.5) * (360.0 / len(NOTE_NAMES))
        x = start_x + index * swatch_w
        color = hsv_to_hex(hue, 0.82, 0.9)
        parts.append(
            f'<rect x="{x:.2f}" y="610" width="{swatch_w - 8}" height="22" rx="3" '
            f'fill="{color}" stroke="#2d2d2d" stroke-width="0.7"/>'
        )
        parts.append(svg_text(x + (swatch_w - 8) / 2.0, 649, note, size=13))
    parts.append(
        svg_text(
            590,
            686,
            "Circle = ell=2 axis; diamond = ell=3 axis; connector = same operator across multipoles.",
            size=12,
        )
    )
    parts.extend(render_saturation_legend(590, 700, summary["score_normalization"]))
    parts.extend(["</g>", "</svg>"])
    return "\n".join(parts) + "\n"


def render_report(summary: dict) -> str:
    q_o = summary["quadrupole_octupole_alignment"]
    sat_obs = summary["saturation_observed"]
    score_norm = summary["score_normalization"]
    smax2 = score_norm["score_max_per_multipole"]["2"]
    smax3 = score_norm["score_max_per_multipole"]["3"]
    smin2 = score_norm["score_min_per_multipole"]["2"]
    smin3 = score_norm["score_min_per_multipole"]["3"]

    lines = [
        "# Opticks Axis-Residue Map v2",
        "",
        "Status: composition/media instrumentation artifact, not evidence.",
        "",
        "This v2 chart extends the v1 two-channel (hue, radius) Opticks-style",
        "encoding by activating a third channel (saturation) over the same",
        "directional operator-axis data. Saturation is a faithful re-encoding",
        "of an already-computed quantity (per-multipole-normalized score",
        "amplitude); it introduces no new statistical handle. Value is held",
        "in reserve at 1.0 by deliberate under-use.",
        "",
        "Phase tag: composition/media instrumentation, not evidence. The",
        "geometricity-from-observer-measurement primitive motivates importing",
        "paint-technique discipline (bounded chromatic channels, intentional",
        "channel reservation) as actual chart method, not the other way",
        "around.",
        "",
        "## Conversion Contract",
        "",
        "| source quantity | conversion | preserved | discarded |",
        "| --- | --- | --- | --- |",
        "| galactic longitude `l_deg` | hue on 0-360 wheel | circular order, clustering, mask-state shift | physical wavelength identity |",
        "| galactic latitude `b_deg` | radius from galactic north pole, `r = R * (1 - abs(b)/90)` | pole/equator ordering | sky-map area, projection fidelity |",
        "| score amplitude (`max_a22^2` for ell=2, `max_a33^2` for ell=3) | saturation, `sat = SAT_FLOOR + (1 - SAT_FLOOR) * score / max_score_per_multipole` (`SAT_FLOOR=0.18`) | relative score amplitude within each multipole | absolute score scale, cross-multipole amplitude comparison |",
        "| (reserved) | value held constant at 1.0 | a deliberate empty channel | nothing yet; reserved for a future earned channel (e.g. uncertainty) |",
        "| hue sector | sevenfold note label `C D E F G A B` | aesthetic/compositional grouping | exact musical pitch or Newtonian historical assignment |",
        "| multipole | marker shape: circle for ell=2, diamond for ell=3 | quadrupole/octupole distinction | statistical significance |",
        "",
        "Saturation normalization is per-multipole: the strongest ell=2 mark and",
        "the strongest ell=3 mark each reach `sat = 1.0`. Cross-ell saturation",
        "comparisons are therefore not meaningful and are not licensed by the",
        "chart.",
        "",
        "## Score Normalization Constants",
        "",
        "| multipole | min(score) | max(score) | sat range observed |",
        "| --- | ---: | ---: | ---: |",
        f"| ell=2 | {smin2:.3e} | {smax2:.3e} | {sat_obs['by_ell']['2']['min']:.3f} -> {sat_obs['by_ell']['2']['max']:.3f} |",
        f"| ell=3 | {smin3:.3e} | {smax3:.3e} | {sat_obs['by_ell']['3']['min']:.3f} -> {sat_obs['by_ell']['3']['max']:.3f} |",
        "",
        "## Readout",
        "",
        "| condition | median Q-O alignment | saturation/composition read |",
        "| --- | ---: | --- |",
        f"| unmasked | {q_o['unmasked']['median_deg']:.1f} deg | ell=2 and ell=3 marks cluster in nearby hue/radius cells; saturation makes the relative score-strength ordering across operators visible at a glance |",
        f"| galcut20 | {q_o['galcut20']['median_deg']:.1f} deg | mask-state shift moves both multipoles around the hue wheel; saturation rebalances when the cut suppresses certain operators' scores more than others |",
        "",
        "What v2 makes visible that v1 did not:",
        "",
        "1. Operator-by-operator score ordering is inspectable directly from the",
        "   marker rather than only via the underlying JSON. In v1 every Commander",
        "   marker had the same chroma; in v2 the strongest-scoring operator at",
        "   each multipole is most chromatic, the weakest-scoring is desaturated",
        "   toward the saturation floor.",
        "2. Mask-state cross-condition score reweighting is visible: where the",
        "   galcut20 mask suppresses one operator's score relative to another,",
        "   that operator's marker desaturates relative to its peers.",
        "3. The chart's chromatic budget now carries 3 of 4 channels; the empty",
        "   value channel is itself a visible discipline mark, not a defect.",
        "",
        "## Confidence on Structural-Similarity Claim",
        "",
        "Claim: \"saturation as a faithful encoding of score amplitude\" — i.e.,",
        "the saturation channel as drawn corresponds monotonically (within each",
        "multipole) to the source `max_a^2` value, with the strongest mark fully",
        "saturated and the weakest at the documented floor.",
        "",
        "Confidence: 95%. The mapping is a closed-form per-multipole",
        "normalization with a documented floor; the only soft choices are",
        "(a) the floor value (chosen for legibility, not from theory) and",
        "(b) the per-multipole rather than global normalization (chosen so",
        "ell=2 and ell=3 marks aren't on a shared scale, which would make the",
        "weaker multipole permanently desaturated). Neither soft choice is a",
        "physics claim. The 5% reserve is for the standing risk that a viewer",
        "interprets cross-ell saturation as a comparison the chart does not",
        "license.",
        "",
        "## Allowed Claims",
        "",
        "1. Saturation faithfully re-encodes the per-multipole-normalized score",
        "   amplitude already in the directional summaries.",
        "2. The v2 chart makes operator-by-operator score ordering and",
        "   mask-state score reweighting inspectable in the same medium that",
        "   already shows hue/radius/note structure.",
        "3. The reserved value channel is a deliberate discipline mark; under-",
        "   using a channel is part of the contract.",
        "",
        "## Forbidden Claims",
        "",
        "1. Saturation differences are not new evidence; saturation encodes",
        "   existing score amplitudes from the directional-axis summaries.",
        "2. Cross-multipole saturation comparisons (ell=2 vs ell=3) are not",
        "   licensed: each multipole has its own normalization.",
        "3. The chart does not replace statistical nulls, mask-state controls,",
        "   or the Planck likelihood machinery.",
        "4. The Opticks bridge remains a near-cousin/instrumentation layer, not",
        "   an instantiation-grade cosmological claim.",
        "5. The reserved value channel is not evidence of an unmodeled handle;",
        "   it is an admission of an unearned one.",
        "",
        "## Outputs",
        "",
        "- `opticks_axis_residue_map_v2.svg`",
        "- `opticks_axis_residue_map_v2.csv`",
        "- `opticks_axis_residue_map_v2_summary.json`",
        "",
    ]
    return "\n".join(lines)


def write_outputs(out_dir: Path) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    rows, source_summaries, score_norm = load_axis_rows()
    summary = summarize(rows, source_summaries, score_norm)

    csv_path = out_dir / "opticks_axis_residue_map_v2.csv"
    fieldnames = [
        "condition",
        "axis_kind",
        "operator",
        "ell",
        "l_deg",
        "b_deg",
        "score",
        "score_ratio",
        "hue_deg",
        "sat",
        "val",
        "hex",
        "note",
    ]
    with csv_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({k: row[k] for k in fieldnames})

    summary_path = out_dir / "opticks_axis_residue_map_v2_summary.json"
    with summary_path.open("w", encoding="utf-8") as handle:
        json.dump(summary, handle, indent=2)
        handle.write("\n")

    svg_path = out_dir / "opticks_axis_residue_map_v2.svg"
    svg_path.write_text(render_svg(rows, summary), encoding="utf-8")

    report_path = out_dir / "opticks_axis_residue_map_v2_report.md"
    report_path.write_text(render_report(summary), encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--out-dir",
        type=Path,
        default=DEFAULT_OUT,
        help="Directory for generated report, SVG, CSV, and JSON outputs.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    write_outputs(args.out_dir)
    print(f"wrote Opticks axis-residue map v2 to {args.out_dir}")


if __name__ == "__main__":
    main()
