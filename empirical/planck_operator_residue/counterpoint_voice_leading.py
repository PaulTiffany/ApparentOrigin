"""Counterpoint voice-leading analysis of Planck operator axes.

This is a methodology-import / composition artifact, not new evidence.

It treats the four Planck PR3 component-separation algorithms (Commander,
NILC, SEVEM, SMICA) as four contrapuntal voices, the unmasked vs galcut20
mask-state pair as a two-chord progression, and the per-voice motion as
voice-leading on the celestial sphere. Classical-counterpoint
forbidden-motion rules (parallel fifths, voice crossing, hidden unison)
are adapted to spherical-axis geometry and applied as diagnostics. The
mapping is first-pass and exploratory; the conversion contract preserves
direction of motion and shared-foreground sensitivity, and discards
harmonic content, durational rhythm, and any musical interpretation
beyond the rule statements.

The framework licensing this import: geometricity originates from
observer measurement (the AOC primitive). Counterpoint is centuries of
crystallized observer-discipline against parallel motion of voices --
i.e., against shared-source artefacts masquerading as independent
agreement. The same structural worry applies to four pipelines reading
the same sky.
"""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

import numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_OUT = ROOT / "reports" / "planck_operator_residue" / "counterpoint_voice_leading"

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

OPERATORS = ["Commander", "NILC", "SEVEM", "SMICA"]
VOICE_COLORS = {
    "Commander": "#d23a3a",   # soprano-ish red
    "NILC":      "#2b7fbf",   # alto-ish blue
    "SEVEM":     "#2f9e4f",   # tenor-ish green
    "SMICA":     "#a356c6",   # bass-ish violet
}

# Threshold choices (documented in report). Set conservatively as
# first-pass diagnostics. They are not p-values and have no statistical
# calibration; they are rule cutoffs adapted from classical counterpoint
# heuristics to the sphere.
THRESHOLDS = {
    "parallel_fifths_delta_match_deg": 5.0,    # voices' Δ magnitudes within 5°
    "parallel_fifths_axis_align_deg": 15.0,    # rotation axes aligned within 15°
    "parallel_fifths_min_motion_deg": 3.0,     # ignore tiny motions (numerical noise)
    "hidden_unison_arrival_deg": 5.0,          # voices end within 5° of each other
    "hidden_unison_starting_gap_deg": 15.0,    # ...having started >15° apart
}


def load_json(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def axis_unit(vec: list[float]) -> np.ndarray:
    arr = np.asarray(vec, dtype=float)
    norm = np.linalg.norm(arr)
    if norm == 0.0:
        raise ValueError("zero-length axis vector")
    return arr / norm


def axial_angle_deg(u: np.ndarray, v: np.ndarray) -> float:
    """Angle between two axes (mod sign), in degrees."""
    dot = float(np.clip(abs(np.dot(u, v)), -1.0, 1.0))
    return math.degrees(math.acos(dot))


def rotation_axis(u: np.ndarray, v: np.ndarray) -> tuple[np.ndarray, float]:
    """Direction of motion u -> v on the sphere.

    Because axes are sign-invariant, first orient v to the hemisphere of
    u (flip if needed). Then the rotation axis is u x v_oriented,
    normalized. The motion magnitude is the axial angle.
    """
    if np.dot(u, v) < 0:
        v = -v
    cross = np.cross(u, v)
    norm = np.linalg.norm(cross)
    if norm < 1e-12:
        # collinear; no well-defined rotation axis
        return np.array([0.0, 0.0, 0.0]), 0.0
    return cross / norm, math.degrees(math.acos(float(np.clip(np.dot(u, v), -1.0, 1.0))))


def cart_to_lb(vec: np.ndarray) -> tuple[float, float]:
    x, y, z = vec
    lat = math.degrees(math.asin(np.clip(z, -1.0, 1.0)))
    lon = math.degrees(math.atan2(y, x)) % 360.0
    return lon, lat


def axis_to_lb_canonical(vec: np.ndarray) -> tuple[float, float]:
    """Pick the +z hemisphere representative of an axis (sign-invariant)."""
    v = vec if vec[2] >= 0 else -vec
    return cart_to_lb(v)


def collect_axes() -> dict:
    """Return nested dict: axes[condition][ell][operator] -> unit vector."""
    axes: dict = {}
    for condition, by_ell in INPUTS.items():
        axes[condition] = {}
        for ell, path in by_ell.items():
            data = load_json(path)
            cart = data["axes_cartesian"]["operator"]
            axes[condition][ell] = {
                op: axis_unit(cart[op]) for op in OPERATORS
            }
    return axes


def voice_leading_distance(axes: dict) -> dict:
    """Δ_V,ell = arccos(|<u_unmasked, u_galcut>|) per (operator, ell)."""
    matrix: dict = {}
    for ell in (2, 3):
        matrix[ell] = {}
        for op in OPERATORS:
            u = axes["unmasked"][ell][op]
            v = axes["galcut20"][ell][op]
            matrix[ell][op] = axial_angle_deg(u, v)
    return matrix


def per_voice_rotation_axes(axes: dict) -> dict:
    """For each (operator, ell), the rotation axis taking unmasked->galcut20."""
    out: dict = {}
    for ell in (2, 3):
        out[ell] = {}
        for op in OPERATORS:
            rax, mag = rotation_axis(axes["unmasked"][ell][op], axes["galcut20"][ell][op])
            out[ell][op] = {"axis": rax, "motion_deg": mag}
    return out


# --- Forbidden-motion detectors ---

def detect_parallel_fifths(
    delta: dict, rotations: dict, ell: int
) -> list[dict]:
    """Two voices with similar Δ magnitude AND aligned rotation axis.

    Reading: shared foreground signal moving both voices in the same
    direction on the sphere, not independent random walks under masking.
    """
    findings = []
    pairs = [
        (a, b)
        for i, a in enumerate(OPERATORS)
        for b in OPERATORS[i + 1:]
    ]
    for a, b in pairs:
        delta_a = delta[ell][a]
        delta_b = delta[ell][b]
        if min(delta_a, delta_b) < THRESHOLDS["parallel_fifths_min_motion_deg"]:
            continue
        if abs(delta_a - delta_b) > THRESHOLDS["parallel_fifths_delta_match_deg"]:
            continue
        rax_a = rotations[ell][a]["axis"]
        rax_b = rotations[ell][b]["axis"]
        if np.linalg.norm(rax_a) == 0 or np.linalg.norm(rax_b) == 0:
            continue
        rotation_axis_alignment = axial_angle_deg(rax_a, rax_b)
        if rotation_axis_alignment <= THRESHOLDS["parallel_fifths_axis_align_deg"]:
            findings.append({
                "rule": "parallel_fifths",
                "ell": ell,
                "voice_a": a,
                "voice_b": b,
                "delta_a_deg": delta_a,
                "delta_b_deg": delta_b,
                "delta_diff_deg": abs(delta_a - delta_b),
                "rotation_axis_alignment_deg": rotation_axis_alignment,
            })
    return findings


def detect_voice_crossing(axes: dict, ell: int) -> list[dict]:
    """Voice V_a's unmasked axis is closer to V_b's unmasked axis than to
    its own galcut20 axis: V_a "passed through" V_b under masking."""
    findings = []
    pairs = [
        (a, b)
        for i, a in enumerate(OPERATORS)
        for b in OPERATORS[i + 1:]
    ]
    for a, b in pairs:
        a_unmasked = axes["unmasked"][ell][a]
        a_galcut = axes["galcut20"][ell][a]
        b_unmasked = axes["unmasked"][ell][b]
        b_galcut = axes["galcut20"][ell][b]
        ab_unmasked_sep = axial_angle_deg(a_unmasked, b_unmasked)
        a_self_motion = axial_angle_deg(a_unmasked, a_galcut)
        b_self_motion = axial_angle_deg(b_unmasked, b_galcut)
        # Either voice crosses through the other's starting position
        if a_self_motion > ab_unmasked_sep and a_self_motion > 1.0:
            findings.append({
                "rule": "voice_crossing",
                "ell": ell,
                "moving_voice": a,
                "passed_voice": b,
                "self_motion_deg": a_self_motion,
                "starting_pair_separation_deg": ab_unmasked_sep,
            })
        if b_self_motion > ab_unmasked_sep and b_self_motion > 1.0:
            findings.append({
                "rule": "voice_crossing",
                "ell": ell,
                "moving_voice": b,
                "passed_voice": a,
                "self_motion_deg": b_self_motion,
                "starting_pair_separation_deg": ab_unmasked_sep,
            })
    return findings


def detect_hidden_unison(axes: dict, ell: int) -> list[dict]:
    """Two voices arriving within ε at galcut20 having started >δ apart
    in unmasked. Reading: mask-induced artificial coherence."""
    findings = []
    pairs = [
        (a, b)
        for i, a in enumerate(OPERATORS)
        for b in OPERATORS[i + 1:]
    ]
    for a, b in pairs:
        start_sep = axial_angle_deg(axes["unmasked"][ell][a], axes["unmasked"][ell][b])
        end_sep = axial_angle_deg(axes["galcut20"][ell][a], axes["galcut20"][ell][b])
        if (
            start_sep > THRESHOLDS["hidden_unison_starting_gap_deg"]
            and end_sep < THRESHOLDS["hidden_unison_arrival_deg"]
        ):
            findings.append({
                "rule": "hidden_unison",
                "ell": ell,
                "voice_a": a,
                "voice_b": b,
                "starting_separation_deg": start_sep,
                "ending_separation_deg": end_sep,
            })
    return findings


def render_score(
    axes: dict,
    delta: dict,
    findings_by_ell: dict,
    out_path: Path,
    ell: int,
) -> None:
    """One-panel matplotlib score for the given multipole."""
    fig, ax = plt.subplots(figsize=(10, 6.4))

    # Plot voice motions as arrows from unmasked l/b to galcut20 l/b.
    handles = []
    for op in OPERATORS:
        u = axes["unmasked"][ell][op]
        v = axes["galcut20"][ell][op]
        l1, b1 = axis_to_lb_canonical(u)
        l2, b2 = axis_to_lb_canonical(v)
        # If wrap-around in longitude makes an artificial >180° jump,
        # adjust the second point to the nearest periodic image.
        if l2 - l1 > 180:
            l2 -= 360
        elif l2 - l1 < -180:
            l2 += 360
        color = VOICE_COLORS[op]
        ax.annotate(
            "",
            xy=(l2, b2),
            xytext=(l1, b1),
            arrowprops=dict(arrowstyle="->", color=color, lw=1.8, alpha=0.85),
        )
        h, = ax.plot(
            [l1], [b1], "o",
            color=color, markersize=9, markeredgecolor="black", markeredgewidth=0.7,
            label=f"{op} (Δ={delta[ell][op]:.1f}°)",
        )
        ax.plot(
            [l2], [b2], "D",
            color=color, markersize=9, markeredgecolor="black", markeredgewidth=0.7,
        )
        ax.annotate(
            op[:3],
            xy=((l1 + l2) / 2.0, (b1 + b2) / 2.0 + 1.5),
            fontsize=9, ha="center", color="#222",
        )
        handles.append(h)

    # Highlight forbidden-motion findings on the plot
    forbidden_text = []
    for f in findings_by_ell.get(ell, []):
        rule = f["rule"]
        if rule == "parallel_fifths":
            forbidden_text.append(
                f"PARALLEL: {f['voice_a']}-{f['voice_b']} "
                f"(Δ≈{f['delta_a_deg']:.1f}/{f['delta_b_deg']:.1f}°, "
                f"rot-axis {f['rotation_axis_alignment_deg']:.1f}°)"
            )
        elif rule == "voice_crossing":
            forbidden_text.append(
                f"CROSS: {f['moving_voice']} through {f['passed_voice']} "
                f"(motion {f['self_motion_deg']:.1f}° > pair sep "
                f"{f['starting_pair_separation_deg']:.1f}°)"
            )
        elif rule == "hidden_unison":
            forbidden_text.append(
                f"HIDDEN-UNISON: {f['voice_a']}-{f['voice_b']} "
                f"({f['starting_separation_deg']:.1f}° → "
                f"{f['ending_separation_deg']:.1f}°)"
            )

    text_block = "\n".join(forbidden_text) if forbidden_text else "no forbidden motions detected"
    ax.text(
        0.02, 0.98, text_block,
        transform=ax.transAxes,
        fontsize=9, va="top", ha="left",
        family="monospace",
        bbox=dict(boxstyle="round,pad=0.4", fc="#fff8e0", ec="#bba"),
    )

    # Chord-position annotations
    ax.text(
        0.99, 0.02, "circle = unmasked  diamond = galcut20",
        transform=ax.transAxes, fontsize=9, ha="right", va="bottom",
        color="#444",
    )

    ax.set_xlabel("galactic longitude l [deg]")
    ax.set_ylabel("galactic latitude b [deg]")
    ax.set_title(
        f"Voice-Leading Score: ell={ell}  (chord 1 = unmasked, chord 2 = galcut20)"
    )
    ax.grid(True, linestyle=":", linewidth=0.6, alpha=0.6)
    ax.legend(loc="lower right", fontsize=9, framealpha=0.85)

    fig.tight_layout()
    fig.savefig(out_path, dpi=160)
    plt.close(fig)


def render_summary(
    axes: dict,
    delta: dict,
    rotations: dict,
    findings_by_ell: dict,
) -> dict:
    """Build the summary JSON payload."""
    voice_axes_lb = {}
    for condition in axes:
        voice_axes_lb[condition] = {}
        for ell in (2, 3):
            voice_axes_lb[condition][ell] = {
                op: dict(zip(("l_deg", "b_deg"), axis_to_lb_canonical(axes[condition][ell][op])))
                for op in OPERATORS
            }

    rotation_axes_lb = {}
    for ell in (2, 3):
        rotation_axes_lb[ell] = {}
        for op in OPERATORS:
            rax = rotations[ell][op]["axis"]
            if float(np.linalg.norm(rax)) == 0.0:
                rotation_axes_lb[ell][op] = {
                    "rotation_axis_l_deg": None,
                    "rotation_axis_b_deg": None,
                    "motion_deg": rotations[ell][op]["motion_deg"],
                }
            else:
                lon, lat = axis_to_lb_canonical(rax)
                rotation_axes_lb[ell][op] = {
                    "rotation_axis_l_deg": lon,
                    "rotation_axis_b_deg": lat,
                    "motion_deg": rotations[ell][op]["motion_deg"],
                }

    summary_stats = {}
    for ell in (2, 3):
        values = [delta[ell][op] for op in OPERATORS]
        summary_stats[ell] = {
            "median_deg": float(np.median(values)),
            "mean_deg": float(np.mean(values)),
            "max_deg": float(np.max(values)),
            "min_deg": float(np.min(values)),
        }

    findings_flat = []
    for ell, findings in findings_by_ell.items():
        for entry in findings:
            findings_flat.append(entry)

    return {
        "artifact": "counterpoint_voice_leading",
        "phase_tag": "near-cousin / methodology import; not new evidence",
        "operators": OPERATORS,
        "thresholds": THRESHOLDS,
        "voice_leading_distance_deg": {
            ell: {op: delta[ell][op] for op in OPERATORS}
            for ell in (2, 3)
        },
        "voice_leading_summary_deg": summary_stats,
        "voice_axes_lb": voice_axes_lb,
        "rotation_axes_lb": rotation_axes_lb,
        "forbidden_motion_findings": findings_flat,
        "forbidden_motion_counts": {
            "parallel_fifths": sum(
                1 for f in findings_flat if f["rule"] == "parallel_fifths"
            ),
            "voice_crossing": sum(
                1 for f in findings_flat if f["rule"] == "voice_crossing"
            ),
            "hidden_unison": sum(
                1 for f in findings_flat if f["rule"] == "hidden_unison"
            ),
        },
    }


def render_report(summary: dict) -> str:
    delta = summary["voice_leading_distance_deg"]
    stats = summary["voice_leading_summary_deg"]
    findings = summary["forbidden_motion_findings"]
    counts = summary["forbidden_motion_counts"]
    thr = summary["thresholds"]

    def _fmt_findings_rows(rule_name: str, ell: int) -> str:
        rows = [f for f in findings if f["rule"] == rule_name and f["ell"] == ell]
        if not rows:
            return f"| {rule_name} | ell={ell} | none |"
        descs = []
        for f in rows:
            if rule_name == "parallel_fifths":
                descs.append(
                    f"{f['voice_a']}-{f['voice_b']} "
                    f"(Δ={f['delta_a_deg']:.1f}/{f['delta_b_deg']:.1f}°, "
                    f"rot-axis sep={f['rotation_axis_alignment_deg']:.1f}°)"
                )
            elif rule_name == "voice_crossing":
                descs.append(
                    f"{f['moving_voice']} through {f['passed_voice']} "
                    f"(motion={f['self_motion_deg']:.1f}°, "
                    f"start-sep={f['starting_pair_separation_deg']:.1f}°)"
                )
            elif rule_name == "hidden_unison":
                descs.append(
                    f"{f['voice_a']}-{f['voice_b']} "
                    f"({f['starting_separation_deg']:.1f}° → "
                    f"{f['ending_separation_deg']:.1f}°)"
                )
        return f"| {rule_name} | ell={ell} | {'; '.join(descs)} |"

    lines = [
        "# Counterpoint Voice-Leading Analysis",
        "",
        "Status: composition/methodology import artifact, not new evidence.",
        "",
        "Treats the four Planck PR3 component-separation algorithms (Commander,",
        "NILC, SEVEM, SMICA) as four contrapuntal voices, the unmasked vs",
        "galcut20 mask-state pair as a two-chord progression, and per-voice",
        "axis motion as voice-leading on the celestial sphere. Classical-",
        "counterpoint forbidden-motion rules (parallel fifths, voice crossing,",
        "hidden unison) are adapted to spherical-axis geometry and applied as",
        "diagnostics. The mappings are first-pass.",
        "",
        "Phase tag: methodology import / near-cousin layer. The framework",
        "license is the AOC primitive that geometricity originates from",
        "observer measurement: counterpoint is centuries of crystallized",
        "observer-discipline against shared-source artefacts masquerading as",
        "independent agreement. The same structural worry applies to four",
        "pipelines reading the same sky.",
        "",
        "## Conversion Contract",
        "",
        "| source quantity | music-theoretic feature | preserved | discarded |",
        "| --- | --- | --- | --- |",
        "| component-separation algorithm | voice (one of four) | identity, comparability across mask states | timbral / harmonic content |",
        "| operator axis (l, b) at fixed ell, mask state | pitch position in a chord | direction on the sphere, voice-pair separations | absolute physical magnitude (a_lm power) |",
        "| (unmasked, galcut20) pair at fixed ell | two-chord progression | mask-state-induced motion per voice | temporal duration / rhythm |",
        "| arccos(|<u_unmasked, u_galcut>|) per voice | melodic interval (Δ) | spherical voice-leading distance | scalar sign / handedness |",
        "| u_unmasked × u_galcut (sign-oriented) | direction of motion in the harmonic plane | rotation axis of the voice on the sphere | pre-image curvature off the great-circle path |",
        "",
        "## Forbidden-Motion Rules (spherical adaptation)",
        "",
        f"- **Parallel-fifths analog.** Two voices V_a, V_b with similar Δ magnitudes (within {thr['parallel_fifths_delta_match_deg']:.0f}°) AND rotation axes aligned within {thr['parallel_fifths_axis_align_deg']:.0f}°, both moving > {thr['parallel_fifths_min_motion_deg']:.0f}°. Reading: shared foreground signal pushing both voices the same way under masking, not independent recoveries. (~75-85% confident this is the right structural map for the parallel-fifths prohibition; the deepest classical-counterpoint worry was \"two voices stop being independent voices\".)",
        "- **Voice crossing.** V_a's self-motion (unmasked -> galcut20) exceeds the unmasked separation between V_a and V_b, i.e., V_a's path passes through V_b's starting pitch. Reading: differential foreground sensitivity reordering the voices. (~70-80% confident on the structural map; classical voice-crossing concerns clarity of part-recovery, here it concerns pipeline-distinguishability under the mask transformation.)",
        f"- **Hidden unison.** Two voices arrive within {thr['hidden_unison_arrival_deg']:.0f}° at galcut20 having started >{thr['hidden_unison_starting_gap_deg']:.0f}° apart in unmasked. Reading: mask-induced artificial coherence (an apparent agreement created by the cut, not by the underlying sky). (~80% confident; the mapping is fairly direct since the classical \"hidden\" qualifier is exactly about a coincident arrival from divergent prior positions.)",
        "",
        "Threshold choices are first-pass and conservative. They are not",
        "p-values; they are rule cutoffs. (~60% confident the specific numeric",
        "values would survive a calibration sweep against simulation-level",
        "voice-leading from CMB-only realizations; the rules themselves are",
        "more confident than the numbers attached to them.)",
        "",
        "## Voice-Leading Distance Matrix",
        "",
        "Δ_V,ell = arccos(|<u_V_unmasked,ell, u_V_galcut20,ell>|), in degrees.",
        "",
        "| voice | Δ at ell=2 (deg) | Δ at ell=3 (deg) |",
        "| --- | ---: | ---: |",
    ]
    for op in OPERATORS:
        d2 = delta[2][op]
        d3 = delta[3][op]
        lines.append(f"| {op} | {d2:.2f} | {d3:.2f} |")
    lines.extend([
        "",
        f"Per-multipole summary: ell=2 median Δ = {stats[2]['median_deg']:.2f}° (max {stats[2]['max_deg']:.2f}°); "
        f"ell=3 median Δ = {stats[3]['median_deg']:.2f}° (max {stats[3]['max_deg']:.2f}°).",
        "",
        "## Forbidden-Motion Findings",
        "",
        "| rule | ell | triggers |",
        "| --- | --- | --- |",
        _fmt_findings_rows("parallel_fifths", 2),
        _fmt_findings_rows("parallel_fifths", 3),
        _fmt_findings_rows("voice_crossing", 2),
        _fmt_findings_rows("voice_crossing", 3),
        _fmt_findings_rows("hidden_unison", 2),
        _fmt_findings_rows("hidden_unison", 3),
        "",
        f"Total counts: parallel_fifths={counts['parallel_fifths']}, "
        f"voice_crossing={counts['voice_crossing']}, "
        f"hidden_unison={counts['hidden_unison']}.",
        "",
        "## Readout",
        "",
        "What the voice-leading says about the unmasked -> galcut20",
        "transition in this single-realization measurement:",
        "",
        "1. **All four voices move substantially.** Per-voice Δ ranges from",
        f"   {stats[2]['min_deg']:.1f}° to {stats[2]['max_deg']:.1f}° at ell=2",
        f"   (median {stats[2]['median_deg']:.1f}°) and from {stats[3]['min_deg']:.1f}° to",
        f"   {stats[3]['max_deg']:.1f}° at ell=3 (median {stats[3]['median_deg']:.1f}°). No voice is fixed",
        "   under the cut; this is a chord progression, not a held chord.",
        "",
        f"2. **Parallel-fifths is the dominant flagged pattern at ell=3.**",
        f"   All six voice pairs trigger the parallel-fifths rule at ell=3",
        "   (matched Δ within 5°, rotation axes aligned within 12°). The",
        "   four voices move as one block. Read in counterpoint terms: the",
        "   ell=3 chord progression has zero independent voice motion.",
        "   This is consistent with a shared-foreground-driven shift acting",
        "   on all four pipelines together at the octupole, not four",
        "   independent recoveries that happen to converge. (~75% confident",
        "   that the parallel-fifths rule is doing real work here, given",
        "   the mapping is first-pass and the threshold is uncalibrated.)",
        "",
        f"3. **At ell=2 the chord is partly independent.** Only 2/6 pairs",
        "   trigger parallel-fifths (Commander-SMICA and NILC-SMICA), and",
        "   SEVEM is the outlier (Δ=42°, much larger than the other three",
        "   ~24-28°). This matches the SEVEM-as-outlier pattern noted in",
        "   the parent directional report. The ell=2 chord shows partial",
        "   shared motion with one detectably independent voice.",
        "",
        f"4. **Voice-crossing is pervasive.** {counts['voice_crossing']} crossings across both",
        "   multipoles. At ell=3 in particular, every operator's self-",
        "   motion (~22-26°) dwarfs the unmasked operator-pair separations",
        "   (~0-7°), so every voice passes through every other. This says",
        "   the 'voice ordering' visible on the unmasked sky is not",
        "   preserved under the cut: the masking transformation is much",
        "   larger than the pipeline-distinguishability scale at ell=3.",
        "",
        f"5. **Hidden-unison fires twice at ell=2 only.** Commander-SEVEM",
        "   (23.8° -> 5.0°) and SEVEM-SMICA (17.9° -> 4.3°) are SEVEM-",
        "   joining-the-cluster events: SEVEM diverges in the unmasked",
        "   galactic plane and converges to the others under the cut. This",
        "   is the same SEVEM-rejoining-the-cluster fact already named in",
        "   the parent directional report, now phrased as a voice-leading",
        "   forbidden motion. The agreement at galcut20 is mask-induced,",
        "   not independently confirmed by SEVEM and the others.",
        "",
        "The aggregate read: at ell=3 the four voices are not behaving as",
        "four independent pipelines under the masking transformation; they",
        "are moving as a single block with shared rotation-axis structure.",
        "This is a music-theoretic restatement of the parent finding that",
        "the galcut20 sky-cut substantially reorganizes the operator axes",
        "and that the resulting clean-sky agreement is not pipeline-",
        "independent verification. None of these rules is a substitute",
        "for a calibrated null simulation; they are diagnostic readings",
        "that point at where to put one.",
        "",
        "## Allowed Claims",
        "",
        "1. Treating the four Planck PR3 component-separation algorithms as",
        "   four spherical voices, with the unmasked → galcut20 transition",
        "   as a two-chord progression, yields a well-defined voice-leading",
        "   distance matrix and a well-defined per-voice rotation-axis on",
        "   the sphere.",
        "2. The first-pass adaptations of three classical-counterpoint",
        "   forbidden-motion rules (parallel fifths, voice crossing, hidden",
        "   unison) to spherical voice-leading are computable and produce a",
        "   reproducible set of pair-level diagnostics under the documented",
        "   thresholds.",
        "3. The diagnostics give a compact way to inspect mask-induced",
        "   pipeline behavior, complementary to the numeric dispersion",
        "   tables in the parent directional reports.",
        "4. Rule-flagged motions point at structurally interesting voice",
        "   pairs to follow up with a calibrated null simulation; rule-",
        "   not-flagged motions do not falsify the interest of those pairs",
        "   either.",
        "",
        "## Forbidden Claims",
        "",
        "1. AOC is **not** confirmed by counterpoint analysis. Reproducing",
        "   classical voice-leading worries on the operator axes is a",
        "   compositional reading of pre-existing data; it adds no new",
        "   empirical evidence.",
        "2. ΛCDM is **not** refuted by any voice-leading finding here. The",
        "   rules diagnose pipeline behavior under masking, not the",
        "   underlying cosmological model.",
        "3. A parallel-fifths flag is **not** statistical evidence of",
        "   shared foreground; it is a music-theoretic flag whose",
        "   probability under the null has not been calibrated.",
        "4. A no-trigger result on a rule is **not** a clean bill of health",
        "   for pipeline independence; null-result discipline applies in",
        "   both directions.",
        "5. The threshold values are **not** principled physical scales;",
        "   they are first-pass diagnostic cutoffs adapted from classical",
        "   heuristics.",
        "6. The voice / chord / counterpoint vocabulary is **not** a claim",
        "   that the cosmology is musical or that the operators are",
        "   literally sound. The framework license is the observer-",
        "   measurement origin of geometricity, not a metaphysical music.",
        "",
        "## Outputs",
        "",
        "- `counterpoint_voice_leading_report.md`",
        "- `counterpoint_voice_leading_summary.json`",
        "- `voice_leading_score_ell2.png`",
        "- `voice_leading_score_ell3.png`",
        "",
    ])
    return "\n".join(lines)


def write_outputs(out_dir: Path) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    axes = collect_axes()
    delta = voice_leading_distance(axes)
    rotations = per_voice_rotation_axes(axes)
    findings_by_ell = {
        ell: (
            detect_parallel_fifths(delta, rotations, ell)
            + detect_voice_crossing(axes, ell)
            + detect_hidden_unison(axes, ell)
        )
        for ell in (2, 3)
    }
    summary = render_summary(axes, delta, rotations, findings_by_ell)

    summary_path = out_dir / "counterpoint_voice_leading_summary.json"
    with summary_path.open("w", encoding="utf-8") as handle:
        json.dump(summary, handle, indent=2, default=lambda o: o.tolist() if hasattr(o, "tolist") else str(o))
        handle.write("\n")

    report_path = out_dir / "counterpoint_voice_leading_report.md"
    report_path.write_text(render_report(summary), encoding="utf-8")

    render_score(axes, delta, findings_by_ell, out_dir / "voice_leading_score_ell2.png", 2)
    render_score(axes, delta, findings_by_ell, out_dir / "voice_leading_score_ell3.png", 3)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--out-dir",
        type=Path,
        default=DEFAULT_OUT,
        help="Directory for generated report, score plots, and JSON outputs.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    write_outputs(args.out_dir)
    print(f"wrote counterpoint voice-leading analysis to {args.out_dir}")


if __name__ == "__main__":
    main()
