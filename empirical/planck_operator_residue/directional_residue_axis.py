"""Directional analysis of Planck operator-residue at ell=2 (quadrupole).

For each operator and each pair, build the quadrupole tensor Q_ij from
the ell=2 alms and find its principal axis. Compare across operators and
pairs, and against published low-ell anomaly axes.

Phase tag: this is a near-cousin-phase test of the *axial* feature of
the gestural conjecture (reality has the shape of bounded observation,
which under self-similarity should give physical and epistemic manifolds
the same preferred-axis structure at large scales). It does not commit
the conjecture to any specific physical realization.

Allowed claims:
    1. The operator-residue at ell=2 has/lacks a coherent principal axis.
    2. The principal axis (if any) sits at Δθ° from published anomaly
       directions.
    3. The pattern is robust/sensitive to the galactic-plane mask.

Forbidden claims:
    1. AOC is confirmed by a coherent residual axis.
    2. LambdaCDM is refuted by alignment with the axis of evil.
    3. The result demonstrates rotating-interior cosmology.
    4. One realization of one CMB sky is statistical evidence for
       cosmological axiality.
"""

from __future__ import annotations

import argparse
import json
import math
from itertools import combinations
from pathlib import Path

import numpy as np

from analyze_lowell_operator_residue import read_alm_csv


# Spherical-harmonic Cartesian normalizations (Y_2m at ell=2).
# Y_20 = C0 * (3 z^2 - 1) where z is the Cartesian z-component on unit sphere.
# Y_21 = C1 * z * (x + i y) (m=1).
# Y_22 = C2 * (x + i y)^2  (m=2).
C0 = 0.25 * math.sqrt(5.0 / math.pi)
C1 = -0.5 * math.sqrt(15.0 / (2.0 * math.pi))
C2 = 0.25 * math.sqrt(15.0 / (2.0 * math.pi))


# Reference low-ell anomaly directions, galactic (l_deg, b_deg).
# These are *literature reference points*, not commitments. The axis-of-evil
# literature is itself contested.
REFERENCE_AXES = {
    "axis_of_evil_LM2005": (260.0, 60.0),
    "quad_oct_align_S2004": (250.0, 65.0),
    "cmb_cold_spot": (210.0, -57.0),
    "cmb_kinematic_dipole": (264.0, 48.0),
}


def quadrupole_tensor(a20: float, a21: complex, a22: complex) -> np.ndarray:
    """Symmetric traceless 3x3 tensor Q_ij such that
    T_2(n) = Q_ij n^i n^j on the unit sphere.

    Convention: real-valued T(n), m>=0 alms stored, so
        T_2(n) = a_20 Y_20 + 2 Re(a_21 Y_21) + 2 Re(a_22 Y_22).
    """
    Qxx = -a20 * C0 + 2.0 * C2 * a22.real
    Qyy = -a20 * C0 - 2.0 * C2 * a22.real
    Qzz = 2.0 * a20 * C0
    Qxy = -2.0 * C2 * a22.imag
    Qxz = C1 * a21.real
    Qyz = -C1 * a21.imag
    return np.array(
        [
            [Qxx, Qxy, Qxz],
            [Qxy, Qyy, Qyz],
            [Qxz, Qyz, Qzz],
        ]
    )


def principal_axis(Q: np.ndarray) -> tuple[np.ndarray, list[float], float]:
    """Return (axis, eigvals_sorted_by_abs_descending, anisotropy).

    axis: eigenvector with largest |eigenvalue|, sign-fixed to +z hemisphere
    anisotropy: (|lambda_max| - |lambda_min|) / sum(|eigvals|)
    """
    eigvals, eigvecs = np.linalg.eigh(Q)
    idx = np.argsort(-np.abs(eigvals))
    sorted_vals = eigvals[idx]
    axis = eigvecs[:, idx[0]]
    if axis[2] < 0:
        axis = -axis
    s = float(np.sum(np.abs(sorted_vals)))
    aniso = (abs(sorted_vals[0]) - abs(sorted_vals[-1])) / s if s > 0 else 0.0
    return axis, sorted_vals.tolist(), float(aniso)


def cart_to_lb(axis: np.ndarray) -> tuple[float, float]:
    """Cartesian unit vector -> galactic (l_deg in [0,360), b_deg in [0,90])."""
    a = axis if axis[2] >= 0 else -axis
    l = math.degrees(math.atan2(a[1], a[0]))
    if l < 0:
        l += 360.0
    b = math.degrees(math.asin(float(np.clip(a[2], -1.0, 1.0))))
    return l, b


def lb_to_cart(l_deg: float, b_deg: float) -> np.ndarray:
    l = math.radians(l_deg)
    b = math.radians(b_deg)
    return np.array([math.cos(l) * math.cos(b),
                     math.sin(l) * math.cos(b),
                     math.sin(b)])


def angle_between(a: np.ndarray, b: np.ndarray) -> float:
    """Angle in degrees between two directions, treated modulo sign."""
    ua = a / np.linalg.norm(a)
    ub = b / np.linalg.norm(b)
    dot = abs(float(np.dot(ua, ub)))
    return math.degrees(math.acos(min(1.0, max(-1.0, dot))))


def analyze(input_csv: Path) -> dict:
    data = read_alm_csv(input_csv)
    operators = sorted(data)

    op_axes: dict[str, np.ndarray] = {}
    op_axes_lb: dict[str, dict] = {}
    for op in operators:
        e2 = data[op][2]
        a20 = e2[0].real
        a21 = e2[1]
        a22 = e2[2]
        Q = quadrupole_tensor(a20, a21, a22)
        axis, eigvals, aniso = principal_axis(Q)
        op_axes[op] = axis
        l, b = cart_to_lb(axis)
        op_axes_lb[op] = {
            "l_deg": l,
            "b_deg": b,
            "eigvals": eigvals,
            "anisotropy": aniso,
        }

    pair_axes: dict[str, np.ndarray] = {}
    pair_axes_lb: dict[str, dict] = {}
    for op_a, op_b in combinations(operators, 2):
        e2a = data[op_a][2]
        e2b = data[op_b][2]
        a20 = (e2a[0] - e2b[0]).real
        a21 = e2a[1] - e2b[1]
        a22 = e2a[2] - e2b[2]
        Q = quadrupole_tensor(a20, a21, a22)
        axis, eigvals, aniso = principal_axis(Q)
        key = f"{op_a}-{op_b}"
        pair_axes[key] = axis
        residual_power = a20 ** 2 + 2.0 * (abs(a21) ** 2 + abs(a22) ** 2)
        l, b = cart_to_lb(axis)
        pair_axes_lb[key] = {
            "l_deg": l,
            "b_deg": b,
            "eigvals": eigvals,
            "anisotropy": aniso,
            "residual_power": float(residual_power),
        }

    ref_cart = {name: lb_to_cart(*lb) for name, lb in REFERENCE_AXES.items()}

    op_pair_alignments = {
        f"{a}-{b}": angle_between(op_axes[a], op_axes[b])
        for a, b in combinations(operators, 2)
    }

    pair_keys = list(pair_axes)
    pair_pair_alignments = {}
    for i, p1 in enumerate(pair_keys):
        for p2 in pair_keys[i + 1 :]:
            pair_pair_alignments[f"{p1} | {p2}"] = angle_between(
                pair_axes[p1], pair_axes[p2]
            )

    op_vs_ref = {
        op: {ref: angle_between(op_axes[op], ref_cart[ref]) for ref in ref_cart}
        for op in operators
    }
    pair_vs_ref = {
        pair: {
            ref: angle_between(pair_axes[pair], ref_cart[ref]) for ref in ref_cart
        }
        for pair in pair_keys
    }
    op_vs_residue = {
        op: {pair: angle_between(op_axes[op], pair_axes[pair]) for pair in pair_keys}
        for op in operators
    }

    op_dispersion = list(op_pair_alignments.values())
    pair_dispersion = list(pair_pair_alignments.values())

    return {
        "input": str(input_csv),
        "operators": operators,
        "operator_axes": op_axes_lb,
        "pair_residual_axes": pair_axes_lb,
        "operator_pair_alignments_deg": op_pair_alignments,
        "pair_pair_alignments_deg": pair_pair_alignments,
        "operator_vs_reference_deg": op_vs_ref,
        "pair_vs_reference_deg": pair_vs_ref,
        "operator_vs_residue_deg": op_vs_residue,
        "summary": {
            "operator_axis_dispersion_deg": {
                "median": float(np.median(op_dispersion)),
                "mean": float(np.mean(op_dispersion)),
                "max": float(np.max(op_dispersion)),
            },
            "pair_residual_axis_dispersion_deg": {
                "median": float(np.median(pair_dispersion)),
                "mean": float(np.mean(pair_dispersion)),
                "max": float(np.max(pair_dispersion)),
            },
        },
    }


def write_report(path: Path, r: dict, label: str) -> None:
    op_axes = r["operator_axes"]
    pair_axes = r["pair_residual_axes"]
    summary = r["summary"]

    lines = [
        f"# Planck Operator-Residue Directional Analysis ({label})",
        "",
        "Status: directional measurement of the operator-residue quadrupole at ell=2. Tests the *axial* feature of the gestural conjecture under a self-similarity reading (physical and epistemic manifolds should share preferred-axis structure). Does not commit the conjecture to Kerr or any specific physical realization.",
        "",
        f"Input: `{r['input']}`",
        "",
        "## Operator quadrupole axes (galactic l, b in degrees)",
        "",
        "Each operator's own ell=2 sky pattern. Principal axis = eigenvector of largest |eigenvalue| of the quadrupole tensor Q.",
        "",
        "| operator | l (deg) | b (deg) | anisotropy |",
        "| --- | ---: | ---: | ---: |",
    ]
    for op in r["operators"]:
        oa = op_axes[op]
        lines.append(
            f"| `{op}` | {oa['l_deg']:.1f} | {oa['b_deg']:.1f} | {oa['anisotropy']:.3f} |"
        )

    lines += [
        "",
        f"Operator-axis pairwise dispersion (degrees): median = "
        f"{summary['operator_axis_dispersion_deg']['median']:.1f}, "
        f"mean = {summary['operator_axis_dispersion_deg']['mean']:.1f}, "
        f"max = {summary['operator_axis_dispersion_deg']['max']:.1f}.",
        "",
        "## Pair residual quadrupole axes (galactic l, b in degrees)",
        "",
        "Each pair's `Δa_lm = a_lm^i - a_lm^j` ell=2 quadrupole. Principal axis as above.",
        "",
        "| pair | l (deg) | b (deg) | anisotropy | residual power |",
        "| --- | ---: | ---: | ---: | ---: |",
    ]
    for pair, pa in pair_axes.items():
        lines.append(
            f"| `{pair}` | {pa['l_deg']:.1f} | {pa['b_deg']:.1f} | "
            f"{pa['anisotropy']:.3f} | {pa['residual_power']:.4e} |"
        )

    lines += [
        "",
        f"Pair-residual axis pairwise dispersion (degrees): median = "
        f"{summary['pair_residual_axis_dispersion_deg']['median']:.1f}, "
        f"mean = {summary['pair_residual_axis_dispersion_deg']['mean']:.1f}, "
        f"max = {summary['pair_residual_axis_dispersion_deg']['max']:.1f}.",
        "",
        "Reference: for axes uniformly distributed on the sphere modulo sign, the expected median pairwise separation is ~57°. Substantially below that suggests clustering; substantially above is unusual.",
        "",
        "## Self-similarity check: operator vs residual axes",
        "",
        "Angular separation (degrees) between each operator's quadrupole axis (physical: that operator's view of the sky) and each pair's residual axis (epistemic: the direction in which two operators systematically differ).",
        "",
        "| operator \\ pair | "
        + " | ".join(f"`{p}`" for p in pair_axes)
        + " |",
        "| --- |"
        + "".join(" ---: |" for _ in pair_axes),
    ]
    for op in r["operators"]:
        row = [f"`{op}`"]
        for pair in pair_axes:
            row.append(f"{r['operator_vs_residue_deg'][op][pair]:.1f}")
        lines.append("| " + " | ".join(row) + " |")

    lines += [
        "",
        "Reading: small angles indicate the epistemic preferred axis aligns with the physical preferred axis. Large angles indicate the residual axis points elsewhere than the sky's intrinsic quadrupole axis.",
        "",
        "## Alignment with published low-ell anomaly directions",
        "",
        "Operator axes:",
        "",
        "| operator | axis-of-evil (LM2005) | quad-oct align (S2004) | cold spot | CMB dipole |",
        "| --- | ---: | ---: | ---: | ---: |",
    ]
    for op in r["operators"]:
        ovr = r["operator_vs_reference_deg"][op]
        lines.append(
            f"| `{op}` | {ovr['axis_of_evil_LM2005']:.1f} | "
            f"{ovr['quad_oct_align_S2004']:.1f} | "
            f"{ovr['cmb_cold_spot']:.1f} | "
            f"{ovr['cmb_kinematic_dipole']:.1f} |"
        )

    lines += [
        "",
        "Pair-residual axes:",
        "",
        "| pair | axis-of-evil (LM2005) | quad-oct align (S2004) | cold spot | CMB dipole |",
        "| --- | ---: | ---: | ---: | ---: |",
    ]
    for pair in pair_axes:
        pvr = r["pair_vs_reference_deg"][pair]
        lines.append(
            f"| `{pair}` | {pvr['axis_of_evil_LM2005']:.1f} | "
            f"{pvr['quad_oct_align_S2004']:.1f} | "
            f"{pvr['cmb_cold_spot']:.1f} | "
            f"{pvr['cmb_kinematic_dipole']:.1f} |"
        )

    lines += [
        "",
        "## Interpretation discipline",
        "",
        "What this measures: whether the operator-residue quadrupole has a coherent preferred direction across pairs, and whether that direction sits anywhere near published low-ell anomaly directions. Physical-vs-epistemic alignment is a self-similarity check.",
        "",
        "What this does *not* measure: cosmological isotropy. With one realization of one sky and 5 modes at ell=2, cosmic variance dominates. A coherent residual axis in this run cannot be hypothesis-tested without simulations of cosmic-variance-bounded null. Alignment with published anomaly directions is a coincidence check, not derivation. The axis-of-evil literature is itself contested.",
        "",
        "## Allowed claims",
        "",
        "1. The operator-residue at ell=2 has a coherent (or non-coherent) principal axis across the six operator pairs, with median pairwise dispersion of X°.",
        "2. The pair-residual axes [do/do not] cluster within Δθ° of the operators' own quadrupole axes (physical-vs-epistemic alignment readout).",
        "3. The pair-residual axes [do/do not] sit within Δθ° of the published axis-of-evil direction.",
        "4. The pattern is [robust/sensitive] to the galactic-plane mask (compare unmasked vs galcut20 runs).",
        "",
        "## Forbidden claims",
        "",
        "1. AOC is confirmed by a coherent residual axis.",
        "2. LambdaCDM is refuted by alignment with the axis of evil.",
        "3. Self-similarity between physical and epistemic manifolds is demonstrated by axis alignment in one realization.",
        "4. The result implies rotating-interior cosmology, Kerr-cousin geometry, or any specific bounded-observer realization.",
        "",
        "## Phase tag",
        "",
        "Near-cousin-phase test of an axial feature of the gestural conjecture. The result is data; interpretation requires sim-level controls and theory-derived predictions of magnitude and direction.",
    ]

    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--outdir", type=Path, required=True)
    parser.add_argument("--label", type=str, default="ell=2")
    args = parser.parse_args()

    args.outdir.mkdir(parents=True, exist_ok=True)
    r = analyze(args.input)
    (args.outdir / "directional_residue_axis_summary.json").write_text(
        json.dumps(r, indent=2) + "\n", encoding="utf-8"
    )
    write_report(args.outdir / "directional_residue_axis_report.md", r, args.label)
    print(
        json.dumps(
            {
                "input": r["input"],
                "operator_axis_median_dispersion_deg": r["summary"][
                    "operator_axis_dispersion_deg"
                ]["median"],
                "pair_residual_axis_median_dispersion_deg": r["summary"][
                    "pair_residual_axis_dispersion_deg"
                ]["median"],
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
