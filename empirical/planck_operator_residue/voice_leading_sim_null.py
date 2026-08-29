"""Sprint D simulation-level null for the parallel-fifths block-motion finding.

Phase tag: instantiation-class (computational measurement under frozen
detector contract). This script calibrates the Episode 2 voice-leading
result -- all 6/6 voice pairs of the four Planck PR3 component-separation
algorithms triggered the parallel-fifths analog at ell=3 under the
galcut20 mask transition -- by asking how often that block-motion
pattern arises by chance under an isotropic LambdaCDM-like low-ell sky
plus surrogate operator noise.

Detector parameters frozen from Episode 2 analysis. THRESHOLDS,
OPERATORS, and the three forbidden-motion detectors are imported from
`counterpoint_voice_leading.py` -- they are not redeclared here.

Forbidden claims for any document derived from this script:
- "Pipeline Independence Postulate has been refuted" -- we test
  surrogates, not real pipelines.
- "LambdaCDM is ruled out" -- this is a null calibration, not a
  cosmology test.
- "This is evidence for AOC" -- this measures the parallel-fifths
  rule's behaviour under the null only.

Per-mask logic:
- mask=galcut20: draw an underlying sky, synthesize a map, extract
  unmasked and galcut20 pseudo-alms. The four surrogate pipelines are
  four independent operator-noise draws added to the underlying-sky
  alms (one shared draw per pipeline applied to both mask states). The
  voice-leading transition is unmasked->galcut20 per pipeline. Tests:
  does mask geometry plus noise commonly produce the all-six-pairs
  parallel-fifths pattern observed at ell=3?
- mask=none: there is no mask transition. The transition is two
  independent noise re-draws on the same underlying sky (no mask in
  either state). This is the noise-only baseline: how often does pure
  operator noise produce a parallel-fifths trigger?
"""

from __future__ import annotations

import argparse
import csv
import json
from itertools import combinations
from pathlib import Path

import numpy as np

# Detector parameters and forbidden-motion detectors are FROZEN -- imported
# from Episode 2 module verbatim. Do not redeclare.
from counterpoint_voice_leading import (
    OPERATORS,
    THRESHOLDS,
    axial_angle_deg,
    detect_hidden_unison,
    detect_parallel_fifths,
    detect_voice_crossing,
    rotation_axis,
)
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


# Surrogate operator-noise calibration.
#
# The Episode 2 measurement reports per-voice motion Δ ~22-26° at ell=3
# under unmasked->galcut20 (median 22.5°), and operator-axis dispersions
# at galcut20 of ~5° (ell=3) from the parent directional analysis.
#
# We tie noise to the realization's signal RMS so the calibration is
# scale-stable across realizations:
#     noise_sigma_per_alm(ell) = noise_scale * 0.5 * RMS(unmasked alms at ell)
# Confidence ~50% this value produces motion magnitudes in a comparable
# range to the Episode 2 measurement; the script defaults to 1.0x and
# the orchestrator can sweep 0.5x and 2x later for sensitivity. The
# 0.5 factor below is the heuristic baseline; noise_scale = 1.0 means
# "default calibration."
NOISE_BASELINE_FRACTION = 0.5


def build_axes_dict(
    base_unmasked: dict[int, np.ndarray],
    base_galcut: dict[int, np.ndarray] | None,
    ell: int,
    rng: np.random.Generator,
    noise_scale: float,
    projections: dict[int, tuple[np.ndarray, np.ndarray]],
    no_mask_transition: bool,
) -> dict:
    """Build axes[condition][ell][operator] -> unit vector matching the schema
    expected by detect_parallel_fifths / detect_voice_crossing /
    detect_hidden_unison.

    For each operator, we draw one independent noise vector at the requested
    ell. If `no_mask_transition`, the "unmasked" and "galcut20" labels share
    the same base coeffs but get *two independent* noise draws -- this is
    the noise-only baseline.

    Otherwise both labels share the same operator-noise draw, but the
    underlying-sky base coeffs differ between mask states (this isolates the
    mask-induced motion plus pipeline-correlated noise).
    """
    axes_grid, weights = projections[ell]

    rms_unmasked = float(np.sqrt(np.mean(base_unmasked[ell] ** 2)))
    sigma_per_alm = noise_scale * NOISE_BASELINE_FRACTION * rms_unmasked

    axes_out = {"unmasked": {ell: {}}, "galcut20": {ell: {}}}
    for op in OPERATORS:
        # One independent noise draw per surrogate pipeline.
        unit_noise = random_real_alm_coeffs(rng, ell, scale=1.0)
        noise_vec = sigma_per_alm * unit_noise

        if no_mask_transition:
            # Two independent noise re-draws on the same underlying sky.
            unit_noise_2 = random_real_alm_coeffs(rng, ell, scale=1.0)
            noise_vec_2 = sigma_per_alm * unit_noise_2
            coeffs_unmasked = base_unmasked[ell] + noise_vec
            coeffs_galcut = base_unmasked[ell] + noise_vec_2
        else:
            coeffs_unmasked = base_unmasked[ell] + noise_vec
            coeffs_galcut = base_galcut[ell] + noise_vec

        axis_u = find_axis(coeffs_unmasked, axes_grid, weights)
        axis_g = find_axis(coeffs_galcut, axes_grid, weights)
        # Normalize (find_axis returns a grid point; ensure unit vector).
        axes_out["unmasked"][ell][op] = axis_u / float(np.linalg.norm(axis_u))
        axes_out["galcut20"][ell][op] = axis_g / float(np.linalg.norm(axis_g))
    return axes_out


def per_voice_motion(axes: dict, ell: int) -> tuple[dict, dict]:
    """Return (delta[ell][op] -> deg, rotations[ell][op] -> {axis,motion_deg})."""
    delta = {ell: {}}
    rotations = {ell: {}}
    for op in OPERATORS:
        u = axes["unmasked"][ell][op]
        v = axes["galcut20"][ell][op]
        delta[ell][op] = axial_angle_deg(u, v)
        rax, mag = rotation_axis(u, v)
        rotations[ell][op] = {"axis": rax, "motion_deg": mag}
    return delta, rotations


def realization_metrics(
    axes: dict, delta: dict, rotations: dict, ell: int
) -> dict:
    """Run the three frozen detectors and aggregate per-realization metrics."""
    pf = detect_parallel_fifths(delta, rotations, ell)
    vc = detect_voice_crossing(axes, ell)
    hu = detect_hidden_unison(axes, ell)

    voice_deltas = [delta[ell][op] for op in OPERATORS]
    rax_vectors = [
        rotations[ell][op]["axis"]
        for op in OPERATORS
        if float(np.linalg.norm(rotations[ell][op]["axis"])) > 0.0
    ]
    if len(rax_vectors) >= 2:
        rax_pairwise = [
            axial_angle_deg(rax_vectors[i], rax_vectors[j])
            for i, j in combinations(range(len(rax_vectors)), 2)
        ]
        rax_disp = float(np.median(rax_pairwise))
    else:
        rax_disp = float("nan")

    return {
        "n_pf_pairs": len(pf),
        "n_vc": len(vc),
        "n_hu": len(hu),
        "mean_delta_deg": float(np.mean(voice_deltas)),
        "median_delta_deg": float(np.median(voice_deltas)),
        "max_delta_deg": float(np.max(voice_deltas)),
        "mean_rot_axis_disp_deg": rax_disp,
        "pf_pair_keys": ",".join(
            f"{f['voice_a']}-{f['voice_b']}" for f in pf
        ),
    }


def run_realizations(
    n_realizations: int,
    ell: int,
    mask: str,
    noise_scale: float,
    seed: int,
    map_nside: int,
    projection_nside: int,
    n_lat: int,
    n_lon: int,
    galactic_cut_deg: float,
) -> tuple[list[dict], dict]:
    """Run the realization loop. Returns (rows, run_metadata)."""
    positions = fibonacci_positions(12 * map_nside * map_nside)
    basis = {l: real_coeff_basis(l, map_nside)[0] for l in (2, 3)}
    full_mask = np.ones(positions.shape[1], dtype=float)
    cut_mask = synthetic_mask_from_positions(positions, galactic_cut_deg)
    f_sky = float(np.mean(cut_mask > 0.5))
    projections = {
        l: precompute_projection(l, projection_nside, n_lat, n_lon)
        for l in (2, 3)
    }

    rows: list[dict] = []
    for r in range(n_realizations):
        rng = np.random.default_rng(seed * 1_000_000 + r)
        sky_coeffs = draw_lowell_sky(rng)
        sky_map = synthesize_map(sky_coeffs, basis)
        base_unmasked = extract_pseudo_coeffs(sky_map, positions, full_mask)
        if mask == "galcut20":
            base_galcut = extract_pseudo_coeffs(sky_map, positions, cut_mask)
            no_mask_transition = False
        elif mask == "none":
            base_galcut = None
            no_mask_transition = True
        else:
            raise ValueError(f"unsupported mask={mask}")

        axes = build_axes_dict(
            base_unmasked,
            base_galcut,
            ell,
            rng,
            noise_scale,
            projections,
            no_mask_transition,
        )
        delta, rotations = per_voice_motion(axes, ell)
        metrics = realization_metrics(axes, delta, rotations, ell)
        rows.append({"realization": r, **metrics})

    metadata = {
        "f_sky_galcut20": f_sky,
        "map_nside": map_nside,
        "projection_nside": projection_nside,
        "n_lat": n_lat,
        "n_lon": n_lon,
        "galactic_cut_deg": galactic_cut_deg,
        "noise_baseline_fraction": NOISE_BASELINE_FRACTION,
        "noise_calibration": (
            "noise_sigma_per_alm = noise_scale * "
            f"{NOISE_BASELINE_FRACTION} * RMS(unmasked alms at ell); "
            "ties noise to per-realization signal RMS"
        ),
    }
    return rows, metadata


def summarize(
    rows: list[dict],
    ell: int,
    mask: str,
    n_realizations: int,
    noise_scale: float,
    seed: int,
    metadata: dict,
) -> dict:
    pf_counts = [int(row["n_pf_pairs"]) for row in rows]
    vc_counts = [int(row["n_vc"]) for row in rows]
    hu_counts = [int(row["n_hu"]) for row in rows]
    deltas = [float(row["mean_delta_deg"]) for row in rows]
    rax_disps = [
        float(row["mean_rot_axis_disp_deg"])
        for row in rows
        if not np.isnan(row["mean_rot_axis_disp_deg"])
    ]

    pf_distribution = {}
    for k in range(7):
        pf_distribution[str(k)] = float(np.mean(np.asarray(pf_counts) == k))

    pf_at_least_6_rate = float(np.mean(np.asarray(pf_counts) >= 6))
    # observed Planck pair count at ell=3 under galcut20 was 6/6 from Episode 2.
    observed_pair_count = 6
    pf_arr = np.asarray(pf_counts)
    pct_observed = float(np.mean(pf_arr <= observed_pair_count) * 100.0)

    median_disp = (
        float(np.median(rax_disps)) if rax_disps else float("nan")
    )

    return {
        "ell": ell,
        "mask": mask,
        "n_realizations": n_realizations,
        "noise_scale": noise_scale,
        "seed": seed,
        "detector_parameters_provenance": (
            "imported from counterpoint_voice_leading.py"
        ),
        "thresholds": THRESHOLDS,
        "operators_surrogated": list(OPERATORS),
        "phase_tag": (
            "instantiation-class null calibration; surrogate pipelines, not real Planck pipelines"
        ),
        "parallel_fifths_pair_counts_distribution": pf_distribution,
        "parallel_fifths_at_least_6_pairs_rate": pf_at_least_6_rate,
        "parallel_fifths_at_least_6_pairs_percentile_observed": pct_observed,
        "observed_planck_pair_count": observed_pair_count,
        "voice_crossing_count_distribution_summary": {
            "mean": float(np.mean(vc_counts)),
            "median": float(np.median(vc_counts)),
            "max": float(np.max(vc_counts)),
        },
        "hidden_unison_count_distribution_summary": {
            "mean": float(np.mean(hu_counts)),
            "median": float(np.median(hu_counts)),
            "max": float(np.max(hu_counts)),
        },
        "median_voice_leading_distance_deg": float(np.median(deltas)),
        "mean_voice_leading_distance_deg": float(np.mean(deltas)),
        "median_rotation_axis_dispersion_deg": median_disp,
        "simulation_metadata": metadata,
        "limitations": [
            "Surrogate pipelines are independent Gaussian noise draws on a shared underlying sky; not real Planck component-separation operators.",
            "Low-ell-only sky (ell in {2,3}); no high-ell leakage, no foregrounds, no beam, no detector noise.",
            "Synthetic galactic cut |b|>20 deg; not the official Planck common mask.",
            "Detector thresholds are uncalibrated rule cutoffs imported from Episode 2; they are not p-values.",
            "The 'observed pair count' for the percentile readout is the Episode 2 same-realization measurement; this null does not invert that to a Planck-likelihood claim.",
        ],
    }


def write_outputs(
    out_dir: Path, rows: list[dict], summary: dict
) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    summary_path = out_dir / "voice_leading_sim_null_summary.json"
    with summary_path.open("w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2, default=lambda o: o.tolist() if hasattr(o, "tolist") else str(o))
        f.write("\n")
    csv_path = out_dir / "voice_leading_sim_null_samples.csv"
    fieldnames = [
        "realization",
        "n_pf_pairs",
        "n_vc",
        "n_hu",
        "mean_delta_deg",
        "median_delta_deg",
        "max_delta_deg",
        "mean_rot_axis_disp_deg",
        "pf_pair_keys",
    ]
    with csv_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({k: row.get(k, "") for k in fieldnames})


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--n-realizations", type=int, default=1000)
    parser.add_argument(
        "--ell",
        choices=("2", "3"),
        default="3",
        help="Multipole to evaluate (one per invocation).",
    )
    parser.add_argument(
        "--mask",
        choices=("none", "galcut20"),
        default="galcut20",
        help="Mask condition for the transition (one per invocation).",
    )
    parser.add_argument("--noise-scale", type=float, default=1.0)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument(
        "--out-dir",
        type=Path,
        default=ROOT / "reports" / "planck_operator_residue" / "voice_leading_sim_null",
    )
    parser.add_argument("--map-nside", type=int, default=64)
    parser.add_argument("--projection-nside", type=int, default=16)
    parser.add_argument("--n-lat", type=int, default=37)
    parser.add_argument("--n-lon", type=int, default=72)
    parser.add_argument("--galactic-cut-deg", type=float, default=20.0)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    ell = int(args.ell)
    rows, metadata = run_realizations(
        n_realizations=args.n_realizations,
        ell=ell,
        mask=args.mask,
        noise_scale=args.noise_scale,
        seed=args.seed,
        map_nside=args.map_nside,
        projection_nside=args.projection_nside,
        n_lat=args.n_lat,
        n_lon=args.n_lon,
        galactic_cut_deg=args.galactic_cut_deg,
    )
    summary = summarize(
        rows,
        ell=ell,
        mask=args.mask,
        n_realizations=args.n_realizations,
        noise_scale=args.noise_scale,
        seed=args.seed,
        metadata=metadata,
    )
    write_outputs(args.out_dir, rows, summary)
    print(
        json.dumps(
            {
                "ell": ell,
                "mask": args.mask,
                "n_realizations": args.n_realizations,
                "pf_distribution": summary["parallel_fifths_pair_counts_distribution"],
                "pf_at_least_6_rate": summary["parallel_fifths_at_least_6_pairs_rate"],
                "median_voice_leading_distance_deg": summary["median_voice_leading_distance_deg"],
                "median_rotation_axis_dispersion_deg": summary["median_rotation_axis_dispersion_deg"],
                "out_dir": str(args.out_dir),
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
