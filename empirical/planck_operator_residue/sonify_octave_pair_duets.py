"""Per-operator octave-pair duet sonification (Sprint C-prime).

Phase tag: sonification / methodology import artifact, not new evidence.

Composition lesson from Episode 2 (sonify_voice_drift.py): the 8-voice
simultaneous voicing made the audible feature *within-chord* ell=2 fusion
under masking (118 cents -> 34 cents), and the *cross-octave per-operator*
Q-O detuning (median 11.9 deg unmasked -> 29.5 deg galcut20) was encoded
faithfully but not the dominant percept. C-prime addresses that with a
different voicing: each operator gets its own 2-voice piece (its ell=2 +
ell=3 axes) so the listener can track *one* pipeline's cross-octave drift
across the mask transition without the other three pipelines masking it.

Conversion contract (preserved verbatim from Episode 2 where possible):

    voice            <- one sine voice per multipole (ell=2, ell=3)
    pitch            <- galactic longitude l_deg in [0, 360) -> exponential
                        sweep over one octave (ell=2 base 220 Hz, ell=3
                        base 440 Hz)
    pan              <- galactic latitude b_deg in [-90, 90] -> equal-power
                        stereo pan in [-1, 1]
    chord time       <- mask state moments: ~6 s unmasked, ~1 s crossfade,
                        ~6 s galcut20, with edge fades. Total ~13 s per
                        operator duet.

Additions (new for C-prime, documented as deltas from Episode 2):

    * 2 voices per piece, not 8.
    * Per-operator durations shortened from ~12+3+12 s to ~6+1+6 s; total
      ~13 s per duet rather than 27 s. Listener focus is the cross-octave
      interval *within one operator*, not chord-fusion across pipelines.
    * Voice amplitude raised from 0.10 to 0.35 (only 2 voices summing
      means clipping headroom is comfortable at this gain).
    * Per-operator WAVs plus an `all_pipelines_sequential.wav` that
      concatenates the four duets with 1 s silent gaps.

Discipline: pure sines, edge fade + linear crossfade only, no reverb or
envelope shaping. Same voicing primitives as Episode 2 (longitude_to_hz,
latitude_to_pan, sine_voice, equal_power_pan, crossfade,
edge_fade_inplace, float_to_pcm16).
"""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
from scipy.io import wavfile


ROOT = Path(__file__).resolve().parents[2]

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

# Conversion-contract constants (preserved verbatim from Episode 2 where
# applicable; durations and VOICE_AMP differ — see additions section in
# the docstring).
SAMPLE_RATE = 44100
BASE_HZ = 220.0  # ell=2 base pitch (A3); ell=3 voices live in 440 Hz octave.
ELL_OCTAVE = {2: 1.0, 3: 2.0}
DUR_UNMASKED = 6.0       # was 12.0 in Episode 2
DUR_TRANSITION = 1.0     # was 3.0 in Episode 2
DUR_GALCUT = 6.0         # was 12.0 in Episode 2
EDGE_FADE = 0.5          # was 1.0 in Episode 2 (proportional to total)
VOICE_AMP = 0.35         # was 0.10 in Episode 2 (only 2 voices now)
GAP_SILENCE = 1.0        # silent gap between operators in concatenated piece


def load_json(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def longitude_to_hz(l_deg: float, ell: int) -> float:
    """Map galactic longitude in [0, 360) to a frequency in [octave_base, 2*octave_base).

    Verbatim from Episode 2: freq_hz = octave_base * 2 ** (l_deg / 360),
    with octave_base = BASE_HZ * ELL_OCTAVE[ell].
    """
    octave_base = BASE_HZ * ELL_OCTAVE[ell]
    frac = (l_deg % 360.0) / 360.0
    return float(octave_base * (2.0 ** frac))


def latitude_to_pan(b_deg: float) -> float:
    """Map galactic latitude in [-90, 90] to stereo pan in [-1, 1]. (Verbatim)."""
    return float(np.clip(b_deg / 90.0, -1.0, 1.0))


def sine_voice(freq_hz: float, n_samples: int, sample_rate: int = SAMPLE_RATE) -> np.ndarray:
    """Single-frequency, zero-phase sine of length n_samples. (Verbatim)."""
    t = np.arange(n_samples, dtype=np.float64) / sample_rate
    return np.sin(2.0 * np.pi * freq_hz * t).astype(np.float32)


def equal_power_pan(mono: np.ndarray, pan: float) -> np.ndarray:
    """Equal-power stereo pan. (Verbatim)."""
    pan = float(np.clip(pan, -1.0, 1.0))
    theta = (pan + 1.0) * 0.25 * np.pi
    left_gain = np.cos(theta)
    right_gain = np.sin(theta)
    return np.stack([mono * left_gain, mono * right_gain], axis=1).astype(np.float32)


def build_chord(
    voices: list[tuple[float, float]],
    duration_s: float,
    sample_rate: int = SAMPLE_RATE,
) -> np.ndarray:
    """Sum (freq, pan) voices into a stereo chord of fixed duration.

    For C-prime each chord has 2 voices (ell=2 + ell=3 of one operator).
    """
    n_samples = int(round(duration_s * sample_rate))
    chord = np.zeros((n_samples, 2), dtype=np.float32)
    for freq_hz, pan in voices:
        mono = VOICE_AMP * sine_voice(freq_hz, n_samples, sample_rate)
        chord += equal_power_pan(mono, pan)
    return chord


def crossfade(chord_a: np.ndarray, chord_b: np.ndarray, duration_s: float,
              sample_rate: int = SAMPLE_RATE) -> np.ndarray:
    """Linear stereo crossfade. (Verbatim)."""
    n = int(round(duration_s * sample_rate))
    if chord_a.shape[0] < n or chord_b.shape[0] < n:
        raise ValueError("crossfade segments shorter than crossfade duration")
    fade_in = np.linspace(0.0, 1.0, n, dtype=np.float32).reshape(-1, 1)
    fade_out = 1.0 - fade_in
    return chord_a[-n:] * fade_out + chord_b[:n] * fade_in


def edge_fade_inplace(buffer: np.ndarray, duration_s: float,
                      sample_rate: int = SAMPLE_RATE) -> None:
    """Linear fade-in at start, fade-out at end. (Verbatim)."""
    n = int(round(duration_s * sample_rate))
    if n <= 0 or buffer.shape[0] < 2 * n:
        return
    fade_in = np.linspace(0.0, 1.0, n, dtype=np.float32).reshape(-1, 1)
    fade_out = np.linspace(1.0, 0.0, n, dtype=np.float32).reshape(-1, 1)
    buffer[:n] *= fade_in
    buffer[-n:] *= fade_out


def float_to_pcm16(stereo_f32: np.ndarray) -> np.ndarray:
    """Clip into [-1, 1] and convert to 16-bit PCM. (Verbatim)."""
    clipped = np.clip(stereo_f32, -1.0, 1.0)
    return (clipped * 32767.0).astype(np.int16)


def write_wav(buffer_f32: np.ndarray, path: Path) -> None:
    """Write stereo float32 buffer as 16-bit PCM WAV. (Verbatim)."""
    pcm = float_to_pcm16(buffer_f32)
    wavfile.write(str(path), SAMPLE_RATE, pcm)


def gather_duet_voices(operator: str, condition: str) -> list[dict]:
    """Two-row table (one row per ell) for the given operator and mask condition.

    Returns list of dicts with keys: ell, l_deg, b_deg, freq_hz, pan.
    """
    if condition not in INPUTS:
        raise ValueError(f"unknown condition {condition!r}; expected unmasked|galcut20")
    if operator not in OPERATORS:
        raise ValueError(f"unknown operator {operator!r}; expected one of {OPERATORS}")

    rows: list[dict] = []
    for ell, path in INPUTS[condition].items():
        payload = load_json(path)
        ax = payload["operator_axes"][operator]
        l_deg = float(ax["l_deg"])
        b_deg = float(ax["b_deg"])
        rows.append({
            "ell": ell,
            "l_deg": l_deg,
            "b_deg": b_deg,
            "freq_hz": longitude_to_hz(l_deg, ell),
            "pan": latitude_to_pan(b_deg),
        })
    rows.sort(key=lambda r: r["ell"])
    return rows


def synthesize_duet(operator: str) -> np.ndarray:
    """Build the unmasked->galcut20 duet for one operator.

    2-voice unmasked chord + 1 s linear crossfade + 2-voice galcut20 chord,
    edge-faded at both ends. Returns stereo float32, ~13 s long.
    """
    unmasked_rows = gather_duet_voices(operator, "unmasked")
    galcut_rows = gather_duet_voices(operator, "galcut20")

    unmasked_voices = [(r["freq_hz"], r["pan"]) for r in unmasked_rows]
    galcut_voices = [(r["freq_hz"], r["pan"]) for r in galcut_rows]

    # Slabs are oversized so crossfade can carve from trailing/leading regions
    # without shortening the sustained periods (same trick as Episode 2).
    slab_unmasked = build_chord(unmasked_voices, DUR_UNMASKED + DUR_TRANSITION)
    slab_galcut = build_chord(galcut_voices, DUR_TRANSITION + DUR_GALCUT)

    sustain_unmasked = slab_unmasked[: int(DUR_UNMASKED * SAMPLE_RATE)]
    transition = crossfade(slab_unmasked, slab_galcut, DUR_TRANSITION)
    sustain_galcut = slab_galcut[int(DUR_TRANSITION * SAMPLE_RATE):]

    full = np.concatenate([sustain_unmasked, transition, sustain_galcut], axis=0)
    edge_fade_inplace(full, EDGE_FADE)
    return full


def cross_octave_alignment_deg(operator: str, condition: str) -> float:
    """Angle between this operator's ell=2 and ell=3 axes, in degrees.

    Reads the cartesian unit vectors stored in the JSONs and takes arccos
    of the dot product. Documented for the pitch-table debug output so
    Q-O detuning is verifiable from the audio.
    """
    payload2 = load_json(INPUTS[condition][2])
    payload3 = load_json(INPUTS[condition][3])
    v2 = np.array(payload2["axes_cartesian"]["operator"][operator])
    v3 = np.array(payload3["axes_cartesian"]["operator"][operator])
    cosang = float(np.dot(v2, v3) / (np.linalg.norm(v2) * np.linalg.norm(v3)))
    cosang = max(-1.0, min(1.0, cosang))
    return float(np.degrees(np.arccos(cosang)))


def print_pitch_table(operator: str) -> dict:
    """Emit the pitch-table debug readout for one operator and return it."""
    rows_un = gather_duet_voices(operator, "unmasked")
    rows_gc = gather_duet_voices(operator, "galcut20")
    qo_un = cross_octave_alignment_deg(operator, "unmasked")
    qo_gc = cross_octave_alignment_deg(operator, "galcut20")

    table = {
        "operator": operator,
        "unmasked": {f"ell={r['ell']}": r for r in rows_un},
        "galcut20": {f"ell={r['ell']}": r for r in rows_gc},
        "cross_octave_alignment_deg": {
            "unmasked": qo_un,
            "galcut20": qo_gc,
            "delta": qo_gc - qo_un,
        },
    }

    print(f"\n--- {operator} duet pitch table ---")
    for cond, rows in (("unmasked", rows_un), ("galcut20", rows_gc)):
        for r in rows:
            print(
                f"  {cond:9s} ell={r['ell']}  l={r['l_deg']:7.2f} deg  "
                f"b={r['b_deg']:6.2f} deg  freq={r['freq_hz']:7.2f} Hz  "
                f"pan={r['pan']:+.2f}"
            )
    print(
        f"  Q-O alignment: unmasked={qo_un:5.2f} deg, "
        f"galcut20={qo_gc:5.2f} deg, delta={qo_gc - qo_un:+5.2f} deg"
    )
    return table


def render_one_operator(operator: str, out_dir: Path) -> dict:
    """Render one operator's duet WAV, return summary dict."""
    waveform = synthesize_duet(operator)
    duration_s = waveform.shape[0] / SAMPLE_RATE
    peak = float(np.max(np.abs(waveform)))

    out_path = out_dir / f"{operator.lower()}_duet.wav"
    write_wav(waveform, out_path)

    return {
        "operator": operator,
        "wav_path": str(out_path),
        "duration_s": duration_s,
        "peak_amplitude": peak,
        "samples": int(waveform.shape[0]),
    }


def main(out_dir: Path | None = None, smoke_only: bool = False) -> None:
    """Render all four operator duets (full mode) or just Commander (smoke).

    Day 1 / smoke-test path: smoke_only=True, render Commander only to a
    smoke directory. Day 2 path: smoke_only=False, render all four operators
    plus the concatenated all-pipelines piece into the full output dir.
    """
    if out_dir is None:
        out_dir = ROOT / "reports" / "planck_operator_residue" / "sonification_octave_pair_duets"
    out_dir.mkdir(parents=True, exist_ok=True)

    operators = [OPERATORS[0]] if smoke_only else OPERATORS

    summaries = []
    for op in operators:
        table = print_pitch_table(op)
        summary = render_one_operator(op, out_dir)
        summary["pitch_table"] = table
        summaries.append(summary)

        print(
            f"  WAV: {summary['wav_path']}  "
            f"({summary['duration_s']:.2f} s, peak={summary['peak_amplitude']:.4f})"
        )

    if not smoke_only:
        # Day 2 concatenated piece: 4 duets glued together with 1 s gaps.
        gap_samples = int(round(GAP_SILENCE * SAMPLE_RATE))
        gap = np.zeros((gap_samples, 2), dtype=np.float32)
        clips = []
        for i, op in enumerate(OPERATORS):
            clips.append(synthesize_duet(op))
            if i < len(OPERATORS) - 1:
                clips.append(gap)
        full = np.concatenate(clips, axis=0)
        full_path = out_dir / "all_pipelines_sequential.wav"
        write_wav(full, full_path)
        print(
            f"  Concatenated piece: {full_path}  "
            f"({full.shape[0] / SAMPLE_RATE:.2f} s, peak={float(np.max(np.abs(full))):.4f})"
        )


def smoke_test() -> None:
    """Render Commander duet only into the smoke directory and verify."""
    smoke_dir = ROOT / "tmp" / "sprint_cprime_smoke"
    smoke_dir.mkdir(parents=True, exist_ok=True)
    main(out_dir=smoke_dir, smoke_only=True)

    wav_path = smoke_dir / "commander_duet.wav"
    sr, data = wavfile.read(str(wav_path))
    duration_s = data.shape[0] / sr
    peak_int = int(np.max(np.abs(data)))
    peak_norm = peak_int / 32767.0
    print("\n--- smoke-test verification ---")
    print(f"  path:           {wav_path}")
    print(f"  sample_rate:    {sr} Hz")
    print(f"  channels:       {data.shape[1] if data.ndim == 2 else 1}")
    print(f"  dtype:          {data.dtype}  (expect int16)")
    print(f"  duration_s:     {duration_s:.4f}")
    print(f"  peak (int16):   {peak_int} / 32767")
    print(f"  peak (norm.):   {peak_norm:.4f}")

    expected_dur = DUR_UNMASKED + DUR_TRANSITION + DUR_GALCUT
    assert abs(duration_s - expected_dur) < 0.01, (
        f"duration {duration_s:.3f} s, expected {expected_dur:.3f} s"
    )
    assert sr == SAMPLE_RATE, f"sample rate {sr}, expected {SAMPLE_RATE}"
    assert data.ndim == 2 and data.shape[1] == 2, "expected stereo"
    assert data.dtype == np.int16, f"expected int16, got {data.dtype}"
    assert peak_norm < 0.95, f"clipping risk: peak {peak_norm:.4f} >= 0.95"

    # Cross-check pitch-table values vs longitude_to_hz directly.
    rows_un = gather_duet_voices("Commander", "unmasked")
    rows_gc = gather_duet_voices("Commander", "galcut20")
    expected_un_2 = longitude_to_hz(rows_un[0]["l_deg"], 2)
    expected_un_3 = longitude_to_hz(rows_un[1]["l_deg"], 3)
    expected_gc_2 = longitude_to_hz(rows_gc[0]["l_deg"], 2)
    expected_gc_3 = longitude_to_hz(rows_gc[1]["l_deg"], 3)
    assert abs(rows_un[0]["freq_hz"] - expected_un_2) < 1e-6
    assert abs(rows_un[1]["freq_hz"] - expected_un_3) < 1e-6
    assert abs(rows_gc[0]["freq_hz"] - expected_gc_2) < 1e-6
    assert abs(rows_gc[1]["freq_hz"] - expected_gc_3) < 1e-6
    print("  pitch-table cross-check: PASS")
    print("  smoke test: PASS")


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "smoke":
        smoke_test()
    else:
        main()
