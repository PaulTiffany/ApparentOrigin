"""Masked-sky null for the corrected ell=2/ell=3 directional statistic.

This is the next control after directional_axis_null_sim.py. It removes the
mock four-operator layer and directly tests mask geometry:

    Draw an isotropic low-ell sky, synthesize a map, extract unmasked and
    |b|>20 deg pseudo-alms with the same mean-subtracted direct-quadrature
    convention as the fallback Planck extractor, then run the same
    m=ell-maximizing axis statistic.

This is not a full Planck simulation. It does not include beam, noise,
component separation, high-ell leakage, or an official Planck mask. It asks
whether the synthetic galactic cut alone can commonly produce the observed
weakening of quadrupole-octupole alignment.
"""

from __future__ import annotations

import argparse
import csv
import json
import math
from pathlib import Path

import numpy as np

from directional_axis_null_sim import (
    C20,
    C21,
    C22,
    C30,
    C31,
    C32,
    C33,
    OBSERVED,
    angle_between,
    find_axis,
    fibonacci_positions,
    percentile_geq,
    percentile_leq,
    precompute_projection,
    random_real_alm_coeffs,
    real_coeff_basis,
)


def complex_ylm(ell: int, m: int, positions: np.ndarray) -> np.ndarray:
    x, y, z = positions
    xy = x + 1j * y
    if ell == 2 and m == 0:
        return C20 * (3.0 * z**2 - 1.0)
    if ell == 2 and m == 1:
        return C21 * z * xy
    if ell == 2 and m == 2:
        return C22 * xy**2
    if ell == 3 and m == 0:
        return C30 * z * (5.0 * z**2 - 3.0)
    if ell == 3 and m == 1:
        return C31 * (5.0 * z**2 - 1.0) * xy
    if ell == 3 and m == 2:
        return C32 * z * xy**2
    if ell == 3 and m == 3:
        return C33 * xy**3
    raise ValueError(f"unsupported ell,m = {ell},{m}")


def synthesize_map(
    coeffs: dict[int, np.ndarray], basis: dict[int, np.ndarray]
) -> np.ndarray:
    values = np.zeros(basis[2].shape[0], dtype=float)
    for ell in (2, 3):
        values += basis[ell] @ coeffs[ell]
    return values


def extract_pseudo_coeffs(
    values: np.ndarray,
    positions: np.ndarray,
    mask: np.ndarray,
) -> dict[int, np.ndarray]:
    good = mask > 0.5
    centered = values[good] - float(np.mean(values[good]))
    pos_good = positions[:, good]
    pixel_area = 4.0 * math.pi / float(values.size)
    out: dict[int, np.ndarray] = {}

    for ell in (2, 3):
        pieces: list[float] = []
        for m in range(ell + 1):
            ylm = complex_ylm(ell, m, pos_good)
            alm = pixel_area * np.sum(centered * np.conj(ylm))
            if m == 0:
                pieces.append(float(alm.real))
            else:
                pieces.append(float(alm.real))
                pieces.append(float(alm.imag))
        out[ell] = np.array(pieces, dtype=float)
    return out


def flat_sachs_wolfe_scale(ell: int) -> float:
    """Use C_ell proportional to 1/[ell(ell+1)] for a simple low-ell prior."""
    return math.sqrt(1.0 / float(ell * (ell + 1)))


def draw_lowell_sky(rng: np.random.Generator) -> dict[int, np.ndarray]:
    return {
        2: random_real_alm_coeffs(rng, 2, scale=flat_sachs_wolfe_scale(2)),
        3: random_real_alm_coeffs(rng, 3, scale=flat_sachs_wolfe_scale(3)),
    }


def q_o_angle(
    coeffs: dict[int, np.ndarray],
    projections: dict[int, tuple[np.ndarray, np.ndarray]],
) -> float:
    axis_2 = find_axis(coeffs[2], *projections[2])
    axis_3 = find_axis(coeffs[3], *projections[3])
    return angle_between(axis_2, axis_3)


def axis_shift(
    a: dict[int, np.ndarray],
    b: dict[int, np.ndarray],
    ell: int,
    projections: dict[int, tuple[np.ndarray, np.ndarray]],
) -> float:
    return angle_between(
        find_axis(a[ell], *projections[ell]),
        find_axis(b[ell], *projections[ell]),
    )


def summarize(rows: list[dict[str, float | int]], f_sky: float) -> dict:
    obs_unmasked = OBSERVED["unmasked"]["qo_median_deg"]
    obs_masked = OBSERVED["galcut20"]["qo_median_deg"]
    obs_delta = obs_masked - obs_unmasked

    def vals(key: str) -> list[float]:
        return [float(row[key]) for row in rows]

    def stat_block(key: str, observed: float, tail: str) -> dict:
        samples = vals(key)
        return {
            "observed": observed,
            "null_mean": float(np.mean(samples)),
            "null_median": float(np.median(samples)),
            "null_q05": float(np.quantile(samples, 0.05)),
            "null_q95": float(np.quantile(samples, 0.95)),
            "tail_definition": tail,
            "tail_fraction": percentile_leq(samples, observed)
            if tail == "<= observed"
            else percentile_geq(samples, observed),
        }

    joint = [
        row
        for row in rows
        if float(row["unmasked_qo_angle_deg"]) <= obs_unmasked
        and float(row["mask_delta_qo_deg"]) >= obs_delta
    ]

    return {
        "status": "masked-sky isotropic low-ell null",
        "n_seeds": len(rows),
        "mask": {
            "type": "synthetic galactic cut",
            "condition": "|b| > 20 deg",
            "f_sky": f_sky,
        },
        "cl_prior": "C_ell proportional to 1/[ell(ell+1)] for ell=2,3",
        "statistics": {
            "unmasked_qo_angle_deg": stat_block(
                "unmasked_qo_angle_deg", obs_unmasked, "<= observed"
            ),
            "masked_qo_angle_deg": stat_block(
                "masked_qo_angle_deg", obs_masked, ">= observed"
            ),
            "mask_delta_qo_deg": stat_block(
                "mask_delta_qo_deg", obs_delta, ">= observed"
            ),
            "ell2_axis_shift_deg": {
                "null_mean": float(np.mean(vals("ell2_axis_shift_deg"))),
                "null_median": float(np.median(vals("ell2_axis_shift_deg"))),
                "null_q05": float(np.quantile(vals("ell2_axis_shift_deg"), 0.05)),
                "null_q95": float(np.quantile(vals("ell2_axis_shift_deg"), 0.95)),
            },
            "ell3_axis_shift_deg": {
                "null_mean": float(np.mean(vals("ell3_axis_shift_deg"))),
                "null_median": float(np.median(vals("ell3_axis_shift_deg"))),
                "null_q05": float(np.quantile(vals("ell3_axis_shift_deg"), 0.05)),
                "null_q95": float(np.quantile(vals("ell3_axis_shift_deg"), 0.95)),
            },
            "joint_unmasked_tight_and_delta_large": {
                "observed_unmasked_qo_max_deg": obs_unmasked,
                "observed_delta_min_deg": obs_delta,
                "fraction": float(len(joint) / len(rows)),
                "count": len(joint),
            },
        },
        "limitations": [
            "No Planck component-separation operators are simulated.",
            "No beam, noise, high-ell leakage, inpainting, or official Planck mask is simulated.",
            "Only ell=2 and ell=3 are generated, so leakage from higher multipoles is absent.",
            "The extraction uses direct pseudo-alms with mean subtraction, matching the fallback extractor's convention.",
        ],
    }


def write_csv(path: Path, rows: list[dict[str, float | int]]) -> None:
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def make_report(path: Path, summary: dict) -> None:
    stats = summary["statistics"]
    delta = stats["mask_delta_qo_deg"]
    joint = stats["joint_unmasked_tight_and_delta_large"]
    lines = [
        "# Directional Axis Masked-Sky Null",
        "",
        "Status: first mask-geometry simulation for the corrected ell=2/ell=3",
        "m=ell-maximizing directional statistic.",
        "",
        "## Question",
        "",
        "Under isotropic low-ell skies, can the synthetic galactic cut alone",
        "commonly weaken quadrupole-octupole alignment by the observed amount?",
        "",
        "## Setup",
        "",
        f"- Seeds: {summary['n_seeds']}",
        f"- Mask: {summary['mask']['condition']} (`f_sky={summary['mask']['f_sky']:.4f}`)",
        f"- Low-ell prior: {summary['cl_prior']}",
        "- Extraction: direct pseudo-alms with mean subtraction on the retained sky",
        "",
        "## Tail Fractions",
        "",
        "| metric | observed threshold | null median | 5-95% null | tail |",
        "| --- | ---: | ---: | ---: | ---: |",
    ]
    for key in ("unmasked_qo_angle_deg", "masked_qo_angle_deg", "mask_delta_qo_deg"):
        block = stats[key]
        lines.append(
            f"| `{key}` | {block['observed']:.4g} | {block['null_median']:.4g} | "
            f"{block['null_q05']:.4g}-{block['null_q95']:.4g} | "
            f"{block['tail_fraction']:.4g} |"
        )

    lines.extend(
        [
            "",
            "Axis shifts caused by the mask:",
            "",
            "| metric | null median | 5-95% null |",
            "| --- | ---: | ---: |",
        ]
    )
    for key in ("ell2_axis_shift_deg", "ell3_axis_shift_deg"):
        block = stats[key]
        lines.append(
            f"| `{key}` | {block['null_median']:.4g} | "
            f"{block['null_q05']:.4g}-{block['null_q95']:.4g} |"
        )

    lines.extend(
        [
            "",
            "Joint event:",
            "",
            "```text",
            f"unmasked Q-O <= {joint['observed_unmasked_qo_max_deg']:.4g} deg",
            f"and mask delta >= {joint['observed_delta_min_deg']:.4g} deg",
            f"fraction = {joint['fraction']:.6g} ({joint['count']} / {summary['n_seeds']})",
            "```",
            "",
            "## Readout",
            "",
            f"The observed mask-state Q-O delta is compared against direct masked-sky draws; tail = {delta['tail_fraction']:.4g}.",
            "This says how often mask geometry alone produces at least the observed",
            "weakening under this restricted low-ell null.",
            "",
            "## Allowed Claims",
            "",
            "1. This null tests mask geometry directly for ell=2 and ell=3.",
            "2. The result says whether the synthetic galactic cut commonly produces",
            "   the observed Q-O weakening in isotropic low-ell skies.",
            "3. The result is a control on the directional statistic, not an AOC test.",
            "",
            "## Forbidden Claims",
            "",
            "1. This proves or refutes AOC.",
            "2. This refutes LambdaCDM.",
            "3. This replaces official Planck masked-sky likelihood analysis.",
            "4. This includes real component separation or foreground physics.",
            "",
            "## Limitations",
            "",
            *[f"- {item}" for item in summary["limitations"]],
            "",
            "## Next Control",
            "",
            "Add high-ell Gaussian sky content and an official Planck common mask,",
            "then rerun the same pseudo-alm extraction to test leakage and mask",
            "specificity.",
        ]
    )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--outdir",
        type=Path,
        default=Path("reports/planck_operator_residue/directional_axis_masked_sky_null"),
    )
    parser.add_argument("--seeds", type=int, default=1000)
    parser.add_argument("--seed", type=int, default=20260429)
    parser.add_argument("--projection-nside", type=int, default=16)
    parser.add_argument("--map-nside", type=int, default=64)
    parser.add_argument("--galactic-cut", type=float, default=20.0)
    parser.add_argument("--n-lat", type=int, default=37)
    parser.add_argument("--n-lon", type=int, default=72)
    args = parser.parse_args()

    projections = {
        ell: precompute_projection(ell, args.projection_nside, args.n_lat, args.n_lon)
        for ell in (2, 3)
    }
    basis = {ell: real_coeff_basis(ell, args.map_nside)[0] for ell in (2, 3)}
    positions = fibonacci_positions(12 * args.map_nside * args.map_nside)
    z = positions[2]
    mask = (np.abs(np.degrees(np.arcsin(np.clip(z, -1.0, 1.0)))) > args.galactic_cut).astype(float)
    f_sky = float(np.mean(mask > 0.5))
    full_mask = np.ones_like(mask)

    rng = np.random.default_rng(args.seed)
    rows: list[dict[str, float | int]] = []
    for idx in range(args.seeds):
        sky_coeffs = draw_lowell_sky(rng)
        sky_map = synthesize_map(sky_coeffs, basis)
        unmasked_coeffs = extract_pseudo_coeffs(sky_map, positions, full_mask)
        masked_coeffs = extract_pseudo_coeffs(sky_map, positions, mask)

        unmasked_qo = q_o_angle(unmasked_coeffs, projections)
        masked_qo = q_o_angle(masked_coeffs, projections)
        rows.append(
            {
                "seed": idx,
                "unmasked_qo_angle_deg": unmasked_qo,
                "masked_qo_angle_deg": masked_qo,
                "mask_delta_qo_deg": masked_qo - unmasked_qo,
                "ell2_axis_shift_deg": axis_shift(
                    unmasked_coeffs, masked_coeffs, 2, projections
                ),
                "ell3_axis_shift_deg": axis_shift(
                    unmasked_coeffs, masked_coeffs, 3, projections
                ),
            }
        )

    summary = summarize(rows, f_sky)
    summary["simulation_parameters"] = {
        "seed": args.seed,
        "projection_nside": args.projection_nside,
        "map_nside": args.map_nside,
        "galactic_cut_deg": args.galactic_cut,
        "n_lat": args.n_lat,
        "n_lon": args.n_lon,
        "axis_grid_size": args.n_lat * args.n_lon,
    }

    args.outdir.mkdir(parents=True, exist_ok=True)
    write_csv(args.outdir / "directional_axis_masked_sky_null_samples.csv", rows)
    (args.outdir / "directional_axis_masked_sky_null_summary.json").write_text(
        json.dumps(summary, indent=2) + "\n", encoding="utf-8"
    )
    make_report(args.outdir / "directional_axis_masked_sky_null_report.md", summary)

    print(
        json.dumps(
            {
                "n_seeds": summary["n_seeds"],
                "f_sky": summary["mask"]["f_sky"],
                "unmasked_qo_tail": summary["statistics"]["unmasked_qo_angle_deg"][
                    "tail_fraction"
                ],
                "masked_qo_tail": summary["statistics"]["masked_qo_angle_deg"][
                    "tail_fraction"
                ],
                "mask_delta_tail": summary["statistics"]["mask_delta_qo_deg"][
                    "tail_fraction"
                ],
                "joint_tail": summary["statistics"][
                    "joint_unmasked_tight_and_delta_large"
                ]["fraction"],
                "outdir": str(args.outdir),
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
