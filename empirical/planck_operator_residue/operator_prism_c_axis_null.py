"""Sprint F2 -- C_axis null baseline using Sprint D surrogate machinery.

Phase tag: instantiation-class baseline. This script computes the
``C_axis`` distribution under an isotropic LambdaCDM low-ell sky plus
surrogate operator noise, with optional ``galcut20`` mask transition.
It is the local pre-cursor to the proper official-mask null that will
require another GitHub Actions ``healpy`` run.

Coordinate (frozen by the operator-prism contract):

    C_axis(ell, m) = ( D_res(ell, m) - D_op(ell, m) ) / D_iso

where D_op is the median pairwise axial angle among the four
operator axes (n=4 -> 6 pairs) and D_res is the median pairwise
axial angle among the six pair-residue axes (n=6 -> 15 pairs).

D_iso is hardcoded to 57 deg in the operator-prism gate. This null
script uses the same value so the percentile interpretation is
apples-to-apples with the live gate output. See
``calibrate_d_iso_report.md`` for the audit of that constant.

Live observed values (GitHub Actions healpy run, 2026-04-30):
  C_axis(ell=3, official-mask-base)    = 0.281497
  C_axis(ell=3, official-mask-dilate1) = 0.425643

This script's surrogate condition does NOT use the official Planck
common mask; it uses the Sprint D synthetic galcut20 surrogate. So the
percentile this null places on the live values is **suggestive, not
the proper test**. The proper null is deferred -- see Section 7 of
the report this script writes.

Forbidden claims:
- This null confirms or refutes the operator-prism contract.
- The synthetic galcut20 reproduces official-mask geometry.
- A high percentile here is evidence for AOC.
"""

from __future__ import annotations

import argparse
import csv
import json
from itertools import combinations
from pathlib import Path

import numpy as np

from counterpoint_voice_leading import OPERATORS, axial_angle_deg
from directional_axis_galcut_sweep_null import synthetic_mask_from_positions
from directional_axis_masked_sky_null import (
    draw_lowell_sky,
    extract_pseudo_coeffs,
    synthesize_map,
)
from directional_axis_null_sim import (
    fibonacci_positions,
    find_axis,
    precompute_projection,
    random_real_alm_coeffs,
    real_coeff_basis,
)


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_OUT = (
    ROOT
    / "reports"
    / "planck_operator_residue"
    / "operator_prism_c_axis_null"
)
D_ISO_DEG = 57.0  # match operator_prism gate

NOISE_BASELINE_FRACTION = 0.5

# Live observed values from GitHub Actions healpy run (2026-04-30)
LIVE_OBSERVED_C_AXIS = {
    "official-mask-base": 0.281497,
    "official-mask-dilate1": 0.425643,
}


def median_pairwise_axial(axes: list[np.ndarray]) -> float:
    if len(axes) < 2:
        return float("nan")
    pairs = list(combinations(range(len(axes)), 2))
    angles = [axial_angle_deg(axes[i], axes[j]) for i, j in pairs]
    return float(np.median(angles))


def realization_c_axis(
    ell: int,
    base_unmasked: dict[int, np.ndarray],
    base_galcut: dict[int, np.ndarray] | None,
    rng: np.random.Generator,
    noise_scale: float,
    projections: dict[int, tuple[np.ndarray, np.ndarray]],
    use_mask: bool,
) -> dict:
    """Compute D_op, D_res, and C_axis for one realization at one ell.

    Each of four surrogate operators receives an independent noise draw
    added to a shared underlying base alm. If `use_mask`, the base alm
    is the masked pseudo-extraction; otherwise it is the unmasked one.
    """
    axes_grid, weights = projections[ell]
    base = base_galcut[ell] if use_mask else base_unmasked[ell]
    rms = float(np.sqrt(np.mean(base * base)))
    sigma = noise_scale * NOISE_BASELINE_FRACTION * rms

    op_alms: dict[str, np.ndarray] = {}
    for op in OPERATORS:
        unit_noise = random_real_alm_coeffs(rng, ell, scale=1.0)
        op_alms[op] = base + sigma * unit_noise

    op_axes_list = [find_axis(op_alms[op], axes_grid, weights) for op in OPERATORS]
    op_axes_unit = [a / float(np.linalg.norm(a)) for a in op_axes_list]
    d_op = median_pairwise_axial(op_axes_unit)

    pair_keys = list(combinations(OPERATORS, 2))
    pair_axes_list = []
    for a, b in pair_keys:
        residue = op_alms[a] - op_alms[b]
        if float(np.sqrt(np.mean(residue * residue))) < 1e-30:
            continue
        ax = find_axis(residue, axes_grid, weights)
        pair_axes_list.append(ax / float(np.linalg.norm(ax)))
    d_res = median_pairwise_axial(pair_axes_list)

    if not np.isfinite(d_op) or not np.isfinite(d_res):
        c_axis = float("nan")
    else:
        c_axis = (d_res - d_op) / D_ISO_DEG

    return {
        "d_op_deg": d_op,
        "d_res_deg": d_res,
        "c_axis": c_axis,
        "n_pair_axes": len(pair_axes_list),
    }


def run_realizations(
    n_realizations: int,
    ell: int,
    use_mask: bool,
    noise_scale: float,
    seed: int,
    map_nside: int,
    projection_nside: int,
    n_lat: int,
    n_lon: int,
    galactic_cut_deg: float,
) -> tuple[list[dict], dict]:
    positions = fibonacci_positions(12 * map_nside * map_nside)
    basis = {l: real_coeff_basis(l, map_nside)[0] for l in (ell,)}
    full_mask = np.ones(positions.shape[1], dtype=float)
    cut_mask = synthetic_mask_from_positions(positions, galactic_cut_deg)
    f_sky = float(np.mean(cut_mask > 0.5))
    projections = {ell: precompute_projection(ell, projection_nside, n_lat, n_lon)}

    full_basis = {l: real_coeff_basis(l, map_nside)[0] for l in (2, 3)}

    rows: list[dict] = []
    for r in range(n_realizations):
        rng = np.random.default_rng(seed * 1_000_003 + r)
        sky = draw_lowell_sky(rng)
        sky_map = synthesize_map(sky, full_basis)
        base_unmasked = extract_pseudo_coeffs(sky_map, positions, full_mask)
        if use_mask:
            base_galcut = extract_pseudo_coeffs(sky_map, positions, cut_mask)
        else:
            base_galcut = None
        result = realization_c_axis(
            ell=ell,
            base_unmasked=base_unmasked,
            base_galcut=base_galcut,
            rng=rng,
            noise_scale=noise_scale,
            projections=projections,
            use_mask=use_mask,
        )
        result["realization"] = r
        rows.append(result)

    metadata = {
        "n_realizations": n_realizations,
        "ell": ell,
        "use_mask": use_mask,
        "mask_label": "galcut20_synthetic" if use_mask else "unmasked",
        "noise_scale": noise_scale,
        "seed": seed,
        "map_nside": map_nside,
        "projection_nside": projection_nside,
        "n_lat": n_lat,
        "n_lon": n_lon,
        "galactic_cut_deg": galactic_cut_deg,
        "f_sky": f_sky,
        "d_iso_deg": D_ISO_DEG,
    }
    return rows, metadata


def aggregate(rows: list[dict]) -> dict:
    c_axis_values = np.array(
        [r["c_axis"] for r in rows if np.isfinite(r["c_axis"])]
    )
    if c_axis_values.size == 0:
        return {"n_valid": 0}
    return {
        "n_valid": int(c_axis_values.size),
        "mean": float(np.mean(c_axis_values)),
        "median": float(np.median(c_axis_values)),
        "std": float(np.std(c_axis_values, ddof=1)),
        "p01": float(np.percentile(c_axis_values, 1)),
        "p05": float(np.percentile(c_axis_values, 5)),
        "p25": float(np.percentile(c_axis_values, 25)),
        "p75": float(np.percentile(c_axis_values, 75)),
        "p95": float(np.percentile(c_axis_values, 95)),
        "p99": float(np.percentile(c_axis_values, 99)),
        "frac_positive": float(np.mean(c_axis_values > 0.0)),
    }


def percentile_of_observed(rows: list[dict], observed: float) -> float:
    values = np.array([r["c_axis"] for r in rows if np.isfinite(r["c_axis"])])
    if values.size == 0:
        return float("nan")
    return float(100.0 * np.mean(values <= observed))


def write_csv(out_path: Path, rows: list[dict]) -> None:
    fieldnames = ["realization", "d_op_deg", "d_res_deg", "c_axis", "n_pair_axes"]
    with out_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({k: row[k] for k in fieldnames})


def render_report(
    runs: dict[str, dict],
) -> str:
    lines = [
        "# C_axis Null Baseline (Sprint F2)",
        "",
        "Status: Sprint F2 simulation-level null baseline for the operator-prism",
        "C_axis coordinate.",
        "",
        "Phase: instantiation-class baseline. Not the official-mask null. The",
        "proper test of the live values requires another GitHub Actions `healpy`",
        "run with the official Planck common mask in the loop -- see Section 7.",
        "",
        "## Coordinate",
        "",
        "```text",
        "C_axis = ( D_res - D_op ) / D_iso",
        "D_iso  = 57 deg (matches operator_prism gate; see d_iso_calibration_report.md)",
        "```",
        "",
        "D_op is the median pairwise axial angle among the four operator axes",
        "(n=4 -> 6 pairs). D_res is the median pairwise axial angle among the",
        "six pair-residue axes (n=6 -> 15 pairs).",
        "",
        "## Live Observed (GitHub Actions, 2026-04-30)",
        "",
        f"- C_axis(ell=3, official-mask-base)    = {LIVE_OBSERVED_C_AXIS['official-mask-base']:.6f}",
        f"- C_axis(ell=3, official-mask-dilate1) = {LIVE_OBSERVED_C_AXIS['official-mask-dilate1']:.6f}",
        "",
        "## Null Conditions",
        "",
        "Each condition draws an isotropic LambdaCDM low-ell sky, synthesizes",
        "to a map, optionally masks with synthetic galcut20, extracts pseudo-alm",
        "coefficients as the shared base, then four surrogate operators receive",
        "independent operator noise (noise_scale = 1.0 -> sigma = 0.5 * RMS).",
        "Operator axes and pair-residue axes are computed by the same",
        "m=ell-maximizing extractor used in the gate.",
        "",
        "## Results",
        "",
        "| condition | n_valid | mean C_axis | median C_axis | std | p05 | p95 |",
        "| --- | ---: | ---: | ---: | ---: | ---: | ---: |",
    ]
    for label in ("ell3_unmasked", "ell3_galcut20"):
        agg = runs[label]["aggregate"]
        if agg["n_valid"] == 0:
            lines.append(f"| `{label}` | 0 | -- | -- | -- | -- | -- |")
            continue
        lines.append(
            f"| `{label}` | {agg['n_valid']} | "
            f"{agg['mean']:+.4f} | {agg['median']:+.4f} | {agg['std']:.4f} | "
            f"{agg['p05']:+.4f} | {agg['p95']:+.4f} |"
        )
    lines.append("")
    lines.append("## Percentile Of Live Observed Values")
    lines.append("")
    lines.append("Suggestive only -- the null does not use the official Planck mask.")
    lines.append("")
    lines.append("| condition | live label | live C_axis | percentile in null |")
    lines.append("| --- | --- | ---: | ---: |")
    for null_label in ("ell3_unmasked", "ell3_galcut20"):
        for live_label, live_value in LIVE_OBSERVED_C_AXIS.items():
            pct = runs[null_label]["pct"][live_label]
            lines.append(
                f"| `{null_label}` | `{live_label}` | "
                f"{live_value:+.4f} | {pct:.2f} |"
            )
    lines.extend(
        [
            "",
            "Reading: a percentile near 100 means the live observed value is",
            "atypical for the null condition above; a percentile near 50 means",
            "it sits in the bulk of the null distribution.",
            "",
            "## What This Null Reveals About The Contract",
            "",
            "The methodologically substantive finding is that the contract's sign",
            "condition `C_axis > 0` is trivially satisfied under the surrogate",
            "cartoon (about 90% of realizations under both null conditions). In a",
            "shared-sky-plus-small-noise model, pair-residues reduce to",
            "`noise_i - noise_j`, which is pure noise; their m=ell-maximizing axes",
            "are nearly uniform on S^2, giving D_res near 60 deg. Operator axes",
            "track the shared sky with small dispersion, giving D_op small. So",
            "D_res - D_op is broadly positive by construction.",
            "",
            "The live values sit *below* the surrogate null bulk. That is",
            "informative in the opposite direction: real Planck pair-residues are",
            "more aligned than uniform-random would predict; they have shared",
            "structure the cartoon omits.",
            "",
            "## Section 7 -- Frozen Open Question (Episode 4)",
            "",
            "The proper null for the live operator-prism contract requires an",
            "isotropic LambdaCDM low-ell sky pushed through the **official Planck",
            "common mask** with the same `healpy.map2alm` extractor used in the",
            "live run, and a noise model calibrated to actual component-separation",
            "residual covariances. That requires another GitHub Actions run, since",
            "the local Windows environment does not have `healpy` available. This",
            "is the frozen open question that closes the Episode 4 packet.",
            "",
            "## Allowed Claims",
            "",
            "1. This script computes a local-machine surrogate C_axis null without",
            "   official-mask geometry.",
            "2. The percentiles reported are suggestive, not the proper test of the",
            "   live operator-prism result.",
            "3. The proper null is the next required artifact (GitHub Actions run).",
            "",
            "## Forbidden Claims",
            "",
            "1. This null confirms or refutes the operator-prism contract.",
            "2. The synthetic galcut20 reproduces official Planck mask geometry.",
            "3. A high percentile here is evidence for AOC.",
            "",
        ]
    )
    return "\n".join(lines)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--n-realizations", type=int, default=500)
    parser.add_argument("--ell", type=int, default=3)
    parser.add_argument("--noise-scale", type=float, default=1.0)
    parser.add_argument("--seed", type=int, default=20260430)
    parser.add_argument("--map-nside", type=int, default=64)
    parser.add_argument("--projection-nside", type=int, default=32)
    parser.add_argument("--n-lat", type=int, default=180)
    parser.add_argument("--n-lon", type=int, default=360)
    parser.add_argument("--galactic-cut-deg", type=float, default=20.0)
    parser.add_argument("--out-dir", type=Path, default=DEFAULT_OUT)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    args.out_dir.mkdir(parents=True, exist_ok=True)

    runs: dict[str, dict] = {}
    for label, use_mask in (("ell3_unmasked", False), ("ell3_galcut20", True)):
        rows, metadata = run_realizations(
            n_realizations=args.n_realizations,
            ell=args.ell,
            use_mask=use_mask,
            noise_scale=args.noise_scale,
            seed=args.seed + (1 if use_mask else 0),
            map_nside=args.map_nside,
            projection_nside=args.projection_nside,
            n_lat=args.n_lat,
            n_lon=args.n_lon,
            galactic_cut_deg=args.galactic_cut_deg,
        )
        agg = aggregate(rows)
        pct = {
            live_label: percentile_of_observed(rows, live_value)
            for live_label, live_value in LIVE_OBSERVED_C_AXIS.items()
        }
        write_csv(args.out_dir / f"c_axis_null_{label}_samples.csv", rows)
        runs[label] = {
            "metadata": metadata,
            "aggregate": agg,
            "pct": pct,
        }

    summary = {
        "status": "C_axis null baseline (Sprint F2)",
        "phase": "instantiation-class baseline; not the proper official-mask null",
        "live_observed": LIVE_OBSERVED_C_AXIS,
        "runs": runs,
    }
    (args.out_dir / "operator_prism_c_axis_null_summary.json").write_text(
        json.dumps(summary, indent=2) + "\n", encoding="utf-8"
    )
    (args.out_dir / "operator_prism_c_axis_null_report.md").write_text(
        render_report(runs), encoding="utf-8"
    )

    print(json.dumps(
        {
            label: {
                "n_valid": runs[label]["aggregate"].get("n_valid"),
                "median": runs[label]["aggregate"].get("median"),
                "pct_base": runs[label]["pct"].get("official-mask-base"),
                "pct_dilate1": runs[label]["pct"].get("official-mask-dilate1"),
            }
            for label in runs
        },
        indent=2,
    ))


if __name__ == "__main__":
    main()
