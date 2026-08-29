"""Build an Opticks-style color/music map for Planck directional axes.

This is a composition/instrumentation artifact, not an evidential statistic.
It converts already-computed galactic axes into a visible sevenfold
color/note chart so mask-state shifts and operator clustering can be inspected
without adding new cosmological claims.
"""

from __future__ import annotations

import argparse
import colorsys
import csv
import json
import math
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_OUT = ROOT / "reports" / "planck_operator_residue" / "opticks_axis_residue_map"

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


def load_json(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def hue_to_hex(hue_deg: float, sat: float = 0.76, val: float = 0.9) -> str:
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
    # North-polar axes sit near the center; equatorial axes sit near the rim.
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


def load_axis_rows() -> tuple[list[dict], dict]:
    rows: list[dict] = []
    summaries: dict = {}
    for condition, by_ell in INPUTS.items():
        summaries[condition] = {}
        for ell, path in by_ell.items():
            summary = load_json(path)
            summaries[condition][ell] = summary
            for operator in OPERATORS:
                axis = summary["operator_axes"][operator]
                hue = axis["l_deg"] % 360.0
                rows.append(
                    {
                        "condition": condition,
                        "axis_kind": "operator",
                        "operator": operator,
                        "ell": ell,
                        "l_deg": axis["l_deg"],
                        "b_deg": axis["b_deg"],
                        "hue_deg": hue,
                        "hex": hue_to_hex(hue),
                        "note": note_for_hue(hue),
                    }
                )
    return rows, summaries


def summarize(rows: list[dict], summaries: dict) -> dict:
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
    return {
        "artifact": "opticks_axis_residue_map",
        "source": "Planck low-ell directional operator-axis summaries",
        "conversion_contract": {
            "hue_deg": "galactic longitude l_deg modulo 360",
            "note": "sevenfold Opticks-style sector over hue; not a physical pitch",
            "radial_position": "outer_radius * (1 - abs(b_deg) / 90)",
            "shape": "circle for ell=2, diamond for ell=3",
            "preserves": [
                "axis circular order",
                "operator clustering",
                "quadrupole-octupole separation",
                "mask-state directional shift",
            ],
            "discards": [
                "physical wavelength identity",
                "exact musical pitch",
                "statistical evidential force",
            ],
        },
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
        color = hue_to_hex(deg, sat=0.86, val=0.92)
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
        f'l={row["l_deg"]:.1f}, b={row["b_deg"]:.1f}, note={row["note"]}'
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


def render_svg(rows: list[dict], summary: dict) -> str:
    width = 1180
    height = 720
    radius = 190
    centers = {"unmasked": (300, 330), "galcut20": (820, 330)}
    parts = [
        '<svg xmlns="http://www.w3.org/2000/svg" width="1180" height="720" viewBox="0 0 1180 720">',
        '<rect width="1180" height="720" fill="#fbfaf7"/>',
        svg_text(590, 42, "Opticks Axis-Residue Map", size=28),
        svg_text(
            590,
            70,
            "Hue = galactic longitude; radial distance = distance from galactic north pole; sevenfold notes are composition labels.",
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
        color = hue_to_hex(hue, sat=0.82, val=0.9)
        parts.append(
            f'<rect x="{x:.2f}" y="610" width="{swatch_w - 8}" height="22" rx="3" '
            f'fill="{color}" stroke="#2d2d2d" stroke-width="0.7"/>'
        )
        parts.append(svg_text(x + (swatch_w - 8) / 2.0, 649, note, size=13))
    parts.extend(
        [
            svg_text(590, 686, "Circle = ell=2 axis; diamond = ell=3 axis; connector = same operator across multipoles.", size=12),
            "</g>",
            "</svg>",
        ]
    )
    return "\n".join(parts) + "\n"


def write_outputs(out_dir: Path) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    rows, source_summaries = load_axis_rows()
    summary = summarize(rows, source_summaries)

    csv_path = out_dir / "opticks_axis_residue_map.csv"
    with csv_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    summary_path = out_dir / "opticks_axis_residue_map_summary.json"
    with summary_path.open("w", encoding="utf-8") as handle:
        json.dump(summary, handle, indent=2)
        handle.write("\n")

    svg_path = out_dir / "opticks_axis_residue_map.svg"
    svg_path.write_text(render_svg(rows, summary), encoding="utf-8")

    report_path = out_dir / "opticks_axis_residue_map_report.md"
    report_path.write_text(render_report(summary), encoding="utf-8")


def render_report(summary: dict) -> str:
    q_o = summary["quadrupole_octupole_alignment"]
    lines = [
        "# Opticks Axis-Residue Map",
        "",
        "Status: composition/media instrumentation artifact, not evidence.",
        "",
        "This artifact converts the already-computed Planck low-ell directional",
        "operator axes into an Opticks-style color and sevenfold-note chart. The",
        "goal is to make the mask-state recomposition visually inspectable while",
        "keeping the empirical contract fixed.",
        "",
        "## Conversion Contract",
        "",
        "| source quantity | conversion | preserved | discarded |",
        "| --- | --- | --- | --- |",
        "| galactic longitude `l_deg` | hue on a 0-360 color wheel | circular order, clustering, mask-state shift | physical wavelength identity |",
        "| galactic latitude `b_deg` | radial distance from galactic north pole, `r = R * (1 - abs(b)/90)` | pole/equator ordering | sky-map area and projection fidelity |",
        "| hue sector | sevenfold note label `C D E F G A B` | aesthetic/compositional grouping | exact musical pitch or Newtonian historical assignment |",
        "| multipole | marker shape: circle for ell=2, diamond for ell=3 | quadrupole/octupole distinction | statistical significance |",
        "",
        "## Readout",
        "",
        "| condition | median Q-O alignment | visual/compositional read |",
        "| --- | ---: | --- |",
        f"| unmasked | {q_o['unmasked']['median_deg']:.1f} deg | ell=2 and ell=3 operator markers occupy a nearby hue/radius neighborhood |",
        f"| galcut20 | {q_o['galcut20']['median_deg']:.1f} deg | both multipoles shift, with weaker Q-O proximity than the unmasked extraction |",
        "",
        "The visual artifact recovers the same qualitative fact as the directional",
        "reports: the unmasked operator axes compose tightly enough to show the",
        "published quadrupole-octupole alignment, while the synthetic galactic cut",
        "moves the feasible chart and weakens that alignment.",
        "",
        "## Allowed Claims",
        "",
        "1. The conversion is a disciplined media/composition layer over existing",
        "   directional-axis products.",
        "2. Hue and note labels can make operator clustering and mask-state shifts",
        "   easier to inspect.",
        "3. The artifact is useful for communication, aesthetic operations, and",
        "   cross-modal composition when its conversion contract is explicit.",
        "",
        "## Forbidden Claims",
        "",
        "1. The colors or notes are not new evidence for AOC.",
        "2. The sevenfold sectors are not a physical pitch measurement.",
        "3. The artifact does not replace the statistical nulls, mask controls, or",
        "   Planck likelihood machinery.",
        "4. The Opticks bridge is a near-cousin/instrumentation layer, not an",
        "   instantiation-grade cosmological claim.",
        "",
        "## Outputs",
        "",
        "- `opticks_axis_residue_map.svg`",
        "- `opticks_axis_residue_map.csv`",
        "- `opticks_axis_residue_map_summary.json`",
        "",
    ]
    return "\n".join(lines)


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
    print(f"wrote Opticks axis-residue map to {args.out_dir}")


if __name__ == "__main__":
    main()
