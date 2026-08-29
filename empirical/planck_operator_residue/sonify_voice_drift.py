"""Sonification of Planck operator-residue voice drift across mask states.

Phase tag: sonification / methodology import artifact, not new evidence.

Conversion contract (also documented in the report):

    voice            <- operator (Commander, NILC, SEVEM, SMICA) -> 4 sine voices
    pitch            <- galactic longitude l_deg in [0, 360) -> [base, 2*base) Hz
                        (linear in l_deg over one octave, l=0 -> base, l=360 -> base+octave wrap)
    octave (low/high)<- multipole ell (ell=2 lower, ell=3 upper octave)
    pan              <- galactic latitude b_deg in [-90, 90] -> stereo pan [-1, 1]
                        (b=0 -> center; positive b -> right channel; negative b -> left)
    chord time       <- mask-state moments: ~12 s unmasked, ~3 s transition crossfade,
                        ~12 s galcut20, with ~1 s fades at start/end. Total ~28 s.

Discipline:
    * pure sine waves, no envelopes beyond linear chord-edge fades and a linear
      crossfade between the two mask states.
    * no rhythm, no reverb, no aesthetic shaping.
    * stereo only because we must place latitude somewhere; we picked pan rather
      than amplitude so a listener with one ear blocked still hears every voice.

The artifact reads the four directional-axis JSONs already on disk and emits:

    reports/planck_operator_residue/sonification_voice_drift/
        sonification_voice_drift.wav
        sonification_voice_drift_score.png
        sonification_voice_drift_summary.json
"""

from __future__ import annotations

import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")  # noqa: E402
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
from scipy.io import wavfile  # noqa: E402


ROOT = Path(__file__).resolve().parents[2]
OUT_DIR = ROOT / "reports" / "planck_operator_residue" / "sonification_voice_drift"

INPUTS = {
    "unmasked": {
        2: ROOT / "reports" / "planck_operator_residue" / "directional_axis_nside64"
        / "directional_quadrupole_mlmax_summary.json",
        3: ROOT / "reports" / "planck_operator_residue" / "directional_axis_nside64"
        / "directional_octupole_axis_summary.json",
    },
    "galcut20": {
        2: ROOT / "reports" / "planck_operator_residue" / "directional_axis_nside64_galcut20"
        / "directional_quadrupole_mlmax_summary.json",
        3: ROOT / "reports" / "planck_operator_residue" / "directional_axis_nside64_galcut20"
        / "directional_octupole_axis_summary.json",
    },
}

OPERATORS = ["Commander", "NILC", "SEVEM", "SMICA"]

# Conversion-contract constants.
SAMPLE_RATE = 44100
BASE_HZ = 220.0  # ell=2 base pitch (A3); ell=3 voices live in 440 Hz octave.
ELL_OCTAVE = {2: 1.0, 3: 2.0}  # multiplier on BASE_HZ before longitude mapping.
DUR_UNMASKED = 12.0
DUR_TRANSITION = 3.0
DUR_GALCUT = 12.0
EDGE_FADE = 1.0
VOICE_AMP = 0.10  # 8 voices * 0.10 = 0.80 peak before clipping headroom.


def load_json(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def longitude_to_hz(l_deg: float, ell: int) -> float:
    """Map galactic longitude in [0, 360) to a frequency in [octave_base, 2*octave_base).

    Linear in l_deg. l=0 -> octave_base. l=360 -> 2*octave_base (wraps). The
    auditory axis is therefore the same circular axis as longitude, with a
    pure exponential pitch sweep over one octave.
    """
    octave_base = BASE_HZ * ELL_OCTAVE[ell]
    frac = (l_deg % 360.0) / 360.0
    return float(octave_base * (2.0 ** frac))


def latitude_to_pan(b_deg: float) -> float:
    """Map galactic latitude in [-90, 90] to stereo pan in [-1, 1]."""
    return float(np.clip(b_deg / 90.0, -1.0, 1.0))


def sine_voice(freq_hz: float, n_samples: int, sample_rate: int = SAMPLE_RATE) -> np.ndarray:
    """Single-frequency, zero-phase sine of length n_samples."""
    t = np.arange(n_samples, dtype=np.float64) / sample_rate
    return np.sin(2.0 * np.pi * freq_hz * t).astype(np.float32)


def equal_power_pan(mono: np.ndarray, pan: float) -> np.ndarray:
    """Return (n, 2) stereo array via equal-power pan law (constant intensity)."""
    pan = float(np.clip(pan, -1.0, 1.0))
    # Map pan in [-1, 1] -> theta in [0, pi/2]; left=cos, right=sin.
    theta = (pan + 1.0) * 0.25 * np.pi
    left_gain = np.cos(theta)
    right_gain = np.sin(theta)
    return np.stack([mono * left_gain, mono * right_gain], axis=1).astype(np.float32)


def build_chord(
    voices: list[tuple[float, float]],
    duration_s: float,
    sample_rate: int = SAMPLE_RATE,
) -> np.ndarray:
    """Sum 8 (freq, pan) voices into a stereo chord of fixed duration.

    Returns an (n_samples, 2) float32 array, *unfaded*.
    """
    n_samples = int(round(duration_s * sample_rate))
    chord = np.zeros((n_samples, 2), dtype=np.float32)
    for freq_hz, pan in voices:
        mono = VOICE_AMP * sine_voice(freq_hz, n_samples, sample_rate)
        chord += equal_power_pan(mono, pan)
    return chord


def crossfade(chord_a: np.ndarray, chord_b: np.ndarray, duration_s: float,
              sample_rate: int = SAMPLE_RATE) -> np.ndarray:
    """Linear stereo crossfade. chord_a and chord_b are (n, 2) sustained slabs;
    returns the (m, 2) crossfade segment of length duration_s built from the
    *trailing* duration_s of chord_a and *leading* duration_s of chord_b.

    Both inputs must be at least duration_s long.
    """
    n = int(round(duration_s * sample_rate))
    if chord_a.shape[0] < n or chord_b.shape[0] < n:
        raise ValueError("crossfade segments shorter than crossfade duration")
    fade_in = np.linspace(0.0, 1.0, n, dtype=np.float32).reshape(-1, 1)
    fade_out = 1.0 - fade_in
    return chord_a[-n:] * fade_out + chord_b[:n] * fade_in


def edge_fade_inplace(buffer: np.ndarray, duration_s: float,
                      sample_rate: int = SAMPLE_RATE) -> None:
    """Apply a linear fade-in at the start and fade-out at the end."""
    n = int(round(duration_s * sample_rate))
    if n <= 0 or buffer.shape[0] < 2 * n:
        return
    fade_in = np.linspace(0.0, 1.0, n, dtype=np.float32).reshape(-1, 1)
    fade_out = np.linspace(1.0, 0.0, n, dtype=np.float32).reshape(-1, 1)
    buffer[:n] *= fade_in
    buffer[-n:] *= fade_out


def float_to_pcm16(stereo_f32: np.ndarray) -> np.ndarray:
    """Clip into [-1, 1] and convert to 16-bit PCM."""
    clipped = np.clip(stereo_f32, -1.0, 1.0)
    return (clipped * 32767.0).astype(np.int16)


def gather_voices() -> dict:
    """Pull (operator, ell) -> (l_deg, b_deg, freq_hz, pan) for both mask states."""
    voice_table = {"unmasked": {}, "galcut20": {}}
    for state, ell_paths in INPUTS.items():
        for ell, path in ell_paths.items():
            payload = load_json(path)
            for op in OPERATORS:
                ax = payload["operator_axes"][op]
                l_deg = float(ax["l_deg"])
                b_deg = float(ax["b_deg"])
                freq_hz = longitude_to_hz(l_deg, ell)
                pan = latitude_to_pan(b_deg)
                voice_table[state][(op, ell)] = {
                    "l_deg": l_deg,
                    "b_deg": b_deg,
                    "freq_hz": freq_hz,
                    "pan": pan,
                }
    return voice_table


def synthesize(voice_table: dict) -> np.ndarray:
    """Build the full stereo waveform for the two-moment piece."""
    chord_unmasked_voices = [
        (v["freq_hz"], v["pan"]) for v in voice_table["unmasked"].values()
    ]
    chord_galcut_voices = [
        (v["freq_hz"], v["pan"]) for v in voice_table["galcut20"].values()
    ]

    # Build slabs slightly longer than nominal so crossfade can be carved out
    # of the trailing/leading regions without shortening the sustained period.
    slab_unmasked = build_chord(chord_unmasked_voices, DUR_UNMASKED + DUR_TRANSITION)
    slab_galcut = build_chord(chord_galcut_voices, DUR_TRANSITION + DUR_GALCUT)

    sustain_unmasked = slab_unmasked[
        : int(DUR_UNMASKED * SAMPLE_RATE)
    ]
    transition = crossfade(slab_unmasked, slab_galcut, DUR_TRANSITION)
    sustain_galcut = slab_galcut[
        int(DUR_TRANSITION * SAMPLE_RATE) :
    ]

    full = np.concatenate([sustain_unmasked, transition, sustain_galcut], axis=0)
    edge_fade_inplace(full, EDGE_FADE)
    return full


def write_wav(buffer_f32: np.ndarray, path: Path) -> None:
    pcm = float_to_pcm16(buffer_f32)
    wavfile.write(str(path), SAMPLE_RATE, pcm)


def render_score(voice_table: dict, total_duration_s: float, path: Path) -> None:
    """Piano-roll of 8 voices: x is time, y is pitch (Hz, log scale).

    Two horizontal segments per voice; vertical thin lines mark chord regions.
    """
    fig, ax = plt.subplots(figsize=(11.0, 6.5))

    t0 = 0.0
    t1 = DUR_UNMASKED
    t2 = DUR_UNMASKED + DUR_TRANSITION
    t3 = total_duration_s

    palette = {
        "Commander": "#1f77b4",
        "NILC": "#d62728",
        "SEVEM": "#2ca02c",
        "SMICA": "#9467bd",
    }
    style_for_ell = {2: "solid", 3: "dashed"}

    for op in OPERATORS:
        for ell in (2, 3):
            f_un = voice_table["unmasked"][(op, ell)]["freq_hz"]
            f_gc = voice_table["galcut20"][(op, ell)]["freq_hz"]
            color = palette[op]
            ls = style_for_ell[ell]
            # Unmasked sustained pitch.
            ax.hlines(f_un, t0, t1, colors=color, linestyles=ls, lw=2.0,
                      label=f"{op} ell={ell}")
            # Transition: linear pitch sweep (representational only).
            ax.plot([t1, t2], [f_un, f_gc], color=color, ls=ls, lw=1.0, alpha=0.5)
            # Galcut20 sustained pitch.
            ax.hlines(f_gc, t2, t3, colors=color, linestyles=ls, lw=2.0)

    # Chord region boundaries.
    for tx in (t1, t2):
        ax.axvline(tx, color="grey", lw=0.6, ls=":")
    ax.axvspan(t0, t1, alpha=0.05, color="C0")
    ax.axvspan(t2, t3, alpha=0.05, color="C3")

    ax.set_xlabel("time (seconds)")
    ax.set_ylabel("pitch (Hz, log)")
    ax.set_yscale("log")
    ax.set_title(
        "Operator-Residue Voice Drift\n"
        "ell=2 (solid) and ell=3 (dashed); 4 operators across mask states\n"
        "left chord = unmasked, right chord = galcut20"
    )

    # Octave guides at base pitch and one octave up and down.
    for f_guide, txt in [(BASE_HZ, "ell=2 base (220 Hz)"),
                         (BASE_HZ * 2, "ell=3 base (440 Hz)"),
                         (BASE_HZ * 4, "880 Hz")]:
        ax.axhline(f_guide, color="lightgrey", lw=0.5, ls="--")
        ax.text(t3, f_guide, "  " + txt, va="center", color="grey", fontsize=8)

    # Deduplicate legend entries.
    handles, labels = ax.get_legend_handles_labels()
    seen = set()
    uniq_h, uniq_l = [], []
    for h, l in zip(handles, labels):
        if l not in seen:
            seen.add(l)
            uniq_h.append(h)
            uniq_l.append(l)
    ax.legend(uniq_h, uniq_l, ncol=4, fontsize=8, loc="upper center",
              bbox_to_anchor=(0.5, -0.10))

    ax.set_xlim(t0, t3)
    fig.tight_layout()
    fig.savefig(path, dpi=150, bbox_inches="tight")
    plt.close(fig)


def write_summary_json(voice_table: dict, total_duration_s: float, path: Path) -> None:
    payload = {
        "phase_tag": "sonification / methodology import artifact, not new evidence",
        "sample_rate_hz": SAMPLE_RATE,
        "channels": 2,
        "encoding": "PCM 16-bit signed little-endian",
        "durations_s": {
            "unmasked_chord": DUR_UNMASKED,
            "transition_crossfade": DUR_TRANSITION,
            "galcut20_chord": DUR_GALCUT,
            "edge_fade": EDGE_FADE,
            "total": total_duration_s,
        },
        "conversion_contract": {
            "voice": "one sine voice per operator (Commander, NILC, SEVEM, SMICA)",
            "pitch_from_longitude": (
                "l_deg in [0, 360) -> exponential pitch sweep over one octave; "
                f"ell=2 base = {BASE_HZ:.1f} Hz, ell=3 base = {BASE_HZ * 2:.1f} Hz"
            ),
            "octave_from_multipole": "ell=2 in lower octave, ell=3 in upper octave",
            "pan_from_latitude": "b_deg in [-90, 90] -> equal-power stereo pan in [-1, 1]",
            "chord_time": (
                "two-moment structure: sustained unmasked chord, linear crossfade, "
                "sustained galcut20 chord; edge fades at start and end"
            ),
            "voice_amplitude": VOICE_AMP,
            "discarded": [
                "absolute pitch identity (no anchoring to a musical key)",
                "loudness ratios from |a_lm|^2 (kept all voices at fixed amplitude)",
                "rhythm, envelope shaping, reverb, timbre",
            ],
        },
        "voices": {
            state: {
                f"{op}_ell{ell}": {
                    "operator": op,
                    "ell": ell,
                    "l_deg": v["l_deg"],
                    "b_deg": v["b_deg"],
                    "freq_hz": v["freq_hz"],
                    "pan": v["pan"],
                }
                for (op, ell), v in entries.items()
            }
            for state, entries in voice_table.items()
        },
        "outputs": {
            "wav": "sonification_voice_drift.wav",
            "score_png": "sonification_voice_drift_score.png",
            "report_md": "sonification_voice_drift_report.md",
            "summary_json": "sonification_voice_drift_summary.json",
        },
    }
    with path.open("w", encoding="utf-8") as handle:
        json.dump(payload, handle, indent=2, ensure_ascii=False)


def chord_dispersion(voices: dict, ell: int) -> dict:
    """Return some readout statistics on freq spread per chord, used in the report."""
    freqs = [v["freq_hz"] for (op, e), v in voices.items() if e == ell]
    arr = np.array(freqs)
    return {
        "min_hz": float(arr.min()),
        "max_hz": float(arr.max()),
        "spread_hz": float(arr.max() - arr.min()),
        "spread_cents": float(1200.0 * np.log2(arr.max() / arr.min())),
    }


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    voice_table = gather_voices()
    waveform = synthesize(voice_table)
    total_duration_s = waveform.shape[0] / SAMPLE_RATE

    wav_path = OUT_DIR / "sonification_voice_drift.wav"
    score_path = OUT_DIR / "sonification_voice_drift_score.png"
    summary_path = OUT_DIR / "sonification_voice_drift_summary.json"

    write_wav(waveform, wav_path)
    render_score(voice_table, total_duration_s, score_path)
    write_summary_json(voice_table, total_duration_s, summary_path)

    # Print a small readout for the agent log.
    print(f"WAV  : {wav_path}  ({total_duration_s:.2f} s)")
    print(f"PNG  : {score_path}")
    print(f"JSON : {summary_path}")

    for state in ("unmasked", "galcut20"):
        d2 = chord_dispersion(voice_table[state], 2)
        d3 = chord_dispersion(voice_table[state], 3)
        print(
            f"  {state:9s} ell=2 spread {d2['spread_cents']:6.1f} cents | "
            f"ell=3 spread {d3['spread_cents']:6.1f} cents"
        )


if __name__ == "__main__":
    main()
