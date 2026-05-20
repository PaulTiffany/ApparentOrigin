"""P3 official-mask morphology sweep for Planck directional axes."""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

import numpy as np
from astropy_healpix import HEALPix

from directional_axis_galcut_sweep import (
    DEFAULT_MAP_DIR,
    OPERATORS,
    circular_mean,
    extract_real_coeffs,
    load_low_maps,
    median_pairwise,
    note_for_hue,
)
from directional_axis_null_sim import angle_between, find_axis, precompute_projection
from extract_planck_lowell_fallback_masked import (
    downgrade_mask_conservative,
    read_mask_fits,
)


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_MASK = (
    ROOT
    / "data"
    / "raw"
    / "planck_operator_residue"
    / "masks"
    / "COM_Mask_CMB-common-Mask-Int_2048_R3.00.fits"
)
DEFAULT_OUT = (
    ROOT
    / "reports"
    / "planck_operator_residue"
    / "directional_axis_official_mask_morphology"
)
FAMILY = ("erode2", "erode1", "base", "dilate1", "dilate2")


def neighbour_table(nside: int) -> np.ndarray:
    hp = HEALPix(nside=nside, order="ring", frame="galactic")
    pix = np.arange(12 * nside * nside, dtype=np.int64)
    neighbours = hp.neighbours(pix)
    arr = np.asarray(neighbours, dtype=np.int64)
    if arr.shape[0] == pix.size:
        return arr
    return arr.T


def erode(mask: np.ndarray, neighbours: np.ndarray) -> np.ndarray:
    out = mask.copy()
    for idx in range(mask.size):
        good = neighbours[idx][neighbours[idx] >= 0]
        if mask[idx] <= 0.5 or np.any(mask[good] <= 0.5):
            out[idx] = 0.0
    return out


def dilate(mask: np.ndarray, neighbours: np.ndarray) -> np.ndarray:
    out = mask.copy()
    for idx in range(mask.size):
        good = neighbours[idx][neighbours[idx] >= 0]
        if mask[idx] > 0.5 or np.any(mask[good] > 0.5):
            out[idx] = 1.0
    return out


def build_mask_family(mask_path: Path, nside_out: int, chunk_size: int) -> dict[str, np.ndarray]:
    values, ordering, nside_in = read_mask_fits(mask_path)
    base = downgrade_mask_conservative(values, nside_in, ordering, nside_out, chunk_size)
    neighbours = neighbour_table(nside_out)
    erode1 = erode(base, neighbours)
    erode2 = erode(erode1, neighbours)
    dilate1 = dilate(base, neighbours)
    dilate2 = dilate(dilate1, neighbours)
    return {
        "erode2": erode2,
        "erode1": erode1,
        "base": base,
        "dilate1": dilate1,
        "dilate2": dilate2,
    }


def analyze_mask(
    label: str,
    mask: np.ndarray,
    low_maps: dict[str, np.ndarray],
    nside_out: int,
    projections: dict[int, tuple[np.ndarray, np.ndarray]],
) -> tuple[list[dict], dict]:
    f_sky = float(np.mean(mask > 0.5))
    axis_rows: list[dict] = []
    op_axes: dict[int, dict[str, np.ndarray]] = {2: {}, 3: {}}
    for operator in OPERATORS:
        coeffs = extract_real_coeffs(low_maps[operator], nside_out, mask)
        for ell in (2, 3):
            axis = find_axis(coeffs[ell], *projections[ell])
            op_axes[ell][operator] = axis
            from directional_axis_galcut_sweep import cart_to_lb

            lon, lat = cart_to_lb(axis)
            axis_rows.append(
                {
                    "mask_label": label,
                    "f_sky": f_sky,
                    "operator": operator,
                    "ell": ell,
                    "l_deg": lon,
                    "b_deg": lat,
                    "note": note_for_hue(lon),
                }
            )

    qo_angles = [angle_between(op_axes[2][op], op_axes[3][op]) for op in OPERATORS]
    metric = {
        "mask_label": label,
        "f_sky": f_sky,
        "qo_median_deg": float(np.median(qo_angles)),
        "ell2_operator_dispersion_deg": median_pairwise(op_axes[2]),
        "ell3_operator_dispersion_deg": median_pairwise(op_axes[3]),
        "ell2_notes": "".join(sorted({row["note"] for row in axis_rows if row["ell"] == 2})),
        "ell3_notes": "".join(sorted({row["note"] for row in axis_rows if row["ell"] == 3})),
        "ell2_mean_l_deg": circular_mean([row["l_deg"] for row in axis_rows if row["ell"] == 2]),
        "ell3_mean_l_deg": circular_mean([row["l_deg"] for row in axis_rows if row["ell"] == 3]),
    }
    return axis_rows, metric


def adjacent_jumps(metrics: list[dict]) -> list[dict]:
    rows = []
    for left, right in zip(metrics, metrics[1:]):
        rows.append(
            {
                "step": f"{left['mask_label']}->{right['mask_label']}",
                "left": left["mask_label"],
                "right": right["mask_label"],
                "qo_jump_deg": abs(right["qo_median_deg"] - left["qo_median_deg"]),
            }
        )
    return rows


def write_csv(path: Path, rows: list[dict]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def render_report(summary: dict) -> str:
    lines = [
        "# Directional Axis Official-Mask Morphology",
        "",
        "Status: P3 official Planck common-mask morphology sweep.",
        "",
        "## Setup",
        "",
        f"- Mask: `{summary['mask_path']}`",
        f"- nside_out: {summary['nside_out']}",
        "- Family: erode2, erode1, base, dilate1, dilate2",
        "- Extraction: fallback direct pseudo-alms at ell=2 and ell=3",
        "",
        "## Metrics",
        "",
        "| mask | f_sky | median Q-O | ell=2 dispersion | ell=3 dispersion | ell=2 notes | ell=3 notes |",
        "| --- | ---: | ---: | ---: | ---: | --- | --- |",
    ]
    for row in summary["metrics"]:
        lines.append(
            f"| {row['mask_label']} | {row['f_sky']:.4f} | {row['qo_median_deg']:.1f} | "
            f"{row['ell2_operator_dispersion_deg']:.1f} | {row['ell3_operator_dispersion_deg']:.1f} | "
            f"{row['ell2_notes']} | {row['ell3_notes']} |"
        )
    lines.extend(["", "## Adjacent Jumps", "", "| step | Q-O jump |", "| --- | ---: |"])
    for row in summary["adjacent_jumps"]:
        lines.append(f"| `{row['step']}` | {row['qo_jump_deg']:.1f} |")
    lines.extend(
        [
            "",
            "## P3 Decision",
            "",
            f"Max adjacent jump: `{summary['max_adjacent_jump_deg']:.1f} deg`.",
            f"Decision threshold: `{summary['decision_threshold_deg']:.1f} deg`.",
            f"Result: `{summary['p3_result']}`.",
            "",
            "Allowed claim: this tests whether the synthetic-latitude cliff shape",
            "survives a first official-mask morphology sweep.",
            "",
            "Forbidden claim: this is not AOC evidence and not a Planck likelihood.",
            "",
        ]
    )
    return "\n".join(lines)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--map-dir", type=Path, default=DEFAULT_MAP_DIR)
    parser.add_argument("--mask", type=Path, default=DEFAULT_MASK)
    parser.add_argument("--out-dir", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--nside-out", type=int, default=64)
    parser.add_argument("--column", default="I_STOKES")
    parser.add_argument("--chunk-size", type=int, default=1_000_000)
    parser.add_argument("--projection-nside", type=int, default=64)
    parser.add_argument("--n-lat", type=int, default=37)
    parser.add_argument("--n-lon", type=int, default=72)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    args.out_dir.mkdir(parents=True, exist_ok=True)
    masks = build_mask_family(args.mask, args.nside_out, args.chunk_size)
    projections = {
        ell: precompute_projection(ell, args.projection_nside, args.n_lat, args.n_lon)
        for ell in (2, 3)
    }
    low_maps = load_low_maps(args.map_dir, args.nside_out, args.column, args.chunk_size)
    axis_rows: list[dict] = []
    metrics: list[dict] = []
    for label in FAMILY:
        rows, metric = analyze_mask(label, masks[label], low_maps, args.nside_out, projections)
        axis_rows.extend(rows)
        metrics.append(metric)
    jumps = adjacent_jumps(metrics)
    max_jump = max(row["qo_jump_deg"] for row in jumps)
    threshold = 30.0
    result = "official_morphology_preserves_cliff_like_recomposition" if max_jump >= threshold else "no_comparable_cliff_under_official_morphology"
    summary = {
        "status": "P3 official mask morphology sweep",
        "mask_path": str(args.mask),
        "nside_out": args.nside_out,
        "family": list(FAMILY),
        "metrics": metrics,
        "adjacent_jumps": jumps,
        "max_adjacent_jump_deg": max_jump,
        "decision_threshold_deg": threshold,
        "p3_result": result,
    }
    write_csv(args.out_dir / "directional_axis_official_mask_morphology_axes.csv", axis_rows)
    write_csv(args.out_dir / "directional_axis_official_mask_morphology_metrics.csv", metrics)
    (args.out_dir / "directional_axis_official_mask_morphology_summary.json").write_text(
        json.dumps(summary, indent=2) + "\n", encoding="utf-8"
    )
    (args.out_dir / "directional_axis_official_mask_morphology_report.md").write_text(
        render_report(summary), encoding="utf-8"
    )
    print(json.dumps({"max_jump": max_jump, "result": result, "outdir": str(args.out_dir)}, indent=2))


if __name__ == "__main__":
    main()
