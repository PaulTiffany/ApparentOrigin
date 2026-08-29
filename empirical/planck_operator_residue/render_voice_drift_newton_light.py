"""Render the Planck voice-drift sonification mapping as Newton light.

This does not interpret sound as evidence. It reads the already-landed
sonification mapping summary, audits the WAV container, and maps the same
voice frequencies into an explicit Newton/Opticks-style visible spectrum.
"""

from __future__ import annotations

import argparse
import array
import csv
import json
import math
import wave
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_SUMMARY = (
    ROOT
    / "reports"
    / "planck_operator_residue"
    / "sonification_voice_drift"
    / "sonification_voice_drift_summary.json"
)
DEFAULT_WAV = (
    ROOT
    / "reports"
    / "planck_operator_residue"
    / "sonification_voice_drift"
    / "sonification_voice_drift.wav"
)
DEFAULT_OUT = (
    ROOT / "reports" / "planck_operator_residue" / "newton_voice_drift_light"
)

NEWTON_BANDS = [
    ("red", 635.0, 700.0),
    ("orange", 590.0, 635.0),
    ("yellow", 560.0, 590.0),
    ("green", 520.0, 560.0),
    ("blue", 490.0, 520.0),
    ("indigo", 450.0, 490.0),
    ("violet", 400.0, 450.0),
]


def load_json(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def clamp(x: float, lo: float = 0.0, hi: float = 1.0) -> float:
    return max(lo, min(hi, x))


def wavelength_to_rgb_hex(wavelength_nm: float) -> str:
    """Approximate visible wavelength to display RGB.

    This is a display encoding, not a physical spectrometer model.
    """
    wl = float(wavelength_nm)
    if 380 <= wl < 440:
        r, g, b = -(wl - 440) / 60, 0.0, 1.0
    elif 440 <= wl < 490:
        r, g, b = 0.0, (wl - 440) / 50, 1.0
    elif 490 <= wl < 510:
        r, g, b = 0.0, 1.0, -(wl - 510) / 20
    elif 510 <= wl < 580:
        r, g, b = (wl - 510) / 70, 1.0, 0.0
    elif 580 <= wl < 645:
        r, g, b = 1.0, -(wl - 645) / 65, 0.0
    elif 645 <= wl <= 780:
        r, g, b = 1.0, 0.0, 0.0
    else:
        r, g, b = 0.0, 0.0, 0.0

    if 380 <= wl < 420:
        factor = 0.3 + 0.7 * (wl - 380) / 40
    elif 420 <= wl < 701:
        factor = 1.0
    elif 701 <= wl <= 780:
        factor = 0.3 + 0.7 * (780 - wl) / 79
    else:
        factor = 0.0

    gamma = 0.8
    red = round(255 * ((clamp(r) * factor) ** gamma))
    green = round(255 * ((clamp(g) * factor) ** gamma))
    blue = round(255 * ((clamp(b) * factor) ** gamma))
    return f"#{red:02x}{green:02x}{blue:02x}"


def newton_band(wavelength_nm: float) -> str:
    for name, lo, hi in NEWTON_BANDS:
        if lo <= wavelength_nm <= hi:
            return name
    return "outside_visible"


def octave_base_for_ell(ell: int) -> float:
    if ell == 2:
        return 220.0
    if ell == 3:
        return 440.0
    raise ValueError(f"unsupported ell: {ell}")


def freq_to_visible_wavelength(freq_hz: float, ell: int) -> tuple[float, float]:
    """Map sonified pitch into one visible-spectrum octave.

    The sonification already used one octave per multipole. This folds each
    voice back into that octave and maps octave phase to 700..400 nm so low
    pitch-class positions are redward and high pitch-class positions are
    violetward.
    """
    base = octave_base_for_ell(ell)
    octave_phase = math.log2(freq_hz / base) % 1.0
    wavelength_nm = 700.0 - 300.0 * octave_phase
    return octave_phase, wavelength_nm


def audit_wav(path: Path) -> dict:
    with wave.open(str(path), "rb") as handle:
        channels = handle.getnchannels()
        sample_width = handle.getsampwidth()
        sample_rate = handle.getframerate()
        frames = handle.getnframes()
        raw = handle.readframes(frames)

    samples = array.array("h")
    samples.frombytes(raw)
    if sample_width != 2:
        peak = None
        rms = None
    else:
        values = [int(v) for v in samples]
        peak = max(abs(v) for v in values) / 32767.0 if values else 0.0
        rms = math.sqrt(sum(v * v for v in values) / len(values)) / 32767.0 if values else 0.0

    return {
        "path": str(path),
        "channels": channels,
        "sample_width_bytes": sample_width,
        "sample_rate_hz": sample_rate,
        "frames": frames,
        "duration_s": frames / sample_rate if sample_rate else 0.0,
        "peak_abs_pcm16": peak,
        "rms_pcm16": rms,
    }


def build_rows(summary: dict) -> list[dict[str, str | int | float]]:
    rows: list[dict[str, str | int | float]] = []
    for mask_state, voices in summary["voices"].items():
        for voice_key, voice in voices.items():
            ell = int(voice["ell"])
            freq_hz = float(voice["freq_hz"])
            octave_phase, wavelength_nm = freq_to_visible_wavelength(freq_hz, ell)
            rows.append(
                {
                    "mask_state": mask_state,
                    "voice_key": voice_key,
                    "operator": voice["operator"],
                    "ell": ell,
                    "l_deg": float(voice["l_deg"]),
                    "b_deg": float(voice["b_deg"]),
                    "freq_hz": freq_hz,
                    "octave_phase": octave_phase,
                    "wavelength_nm": wavelength_nm,
                    "newton_band": newton_band(wavelength_nm),
                    "hex": wavelength_to_rgb_hex(wavelength_nm),
                    "pan": float(voice["pan"]),
                }
            )
    return rows


def summarize(rows: list[dict[str, str | int | float]], wav_audit: dict) -> dict:
    by_state: dict[str, list[dict[str, str | int | float]]] = {}
    for row in rows:
        by_state.setdefault(str(row["mask_state"]), []).append(row)

    state_summary = {}
    for state, state_rows in by_state.items():
        wavelengths = [float(row["wavelength_nm"]) for row in state_rows]
        bands = {}
        for row in state_rows:
            band = str(row["newton_band"])
            bands[band] = bands.get(band, 0) + 1
        state_summary[state] = {
            "mean_wavelength_nm": sum(wavelengths) / len(wavelengths),
            "min_wavelength_nm": min(wavelengths),
            "max_wavelength_nm": max(wavelengths),
            "newton_band_counts": bands,
        }

    if "unmasked" in state_summary and "galcut20" in state_summary:
        shift = (
            state_summary["galcut20"]["mean_wavelength_nm"]
            - state_summary["unmasked"]["mean_wavelength_nm"]
        )
    else:
        shift = None

    return {
        "artifact": "newton_voice_drift_light",
        "phase_tag": "Opticks/light rendering of an existing sonification mapping; not evidence",
        "wav_audit": wav_audit,
        "conversion_contract": {
            "input": "sonification_voice_drift_summary.json plus WAV container audit",
            "audio_frequency": "folded to octave phase within the sonification multipole octave",
            "octave_phase": "mapped linearly to visible wavelength 700..400 nm",
            "newton_band": "red/orange/yellow/green/blue/indigo/violet band label by wavelength",
            "hex": "approximate display RGB from wavelength",
            "preserved": [
                "pitch-class ordering already induced by galactic longitude",
                "mask-state voice drift",
                "operator and multipole labels",
                "latitude as pan metadata",
            ],
            "discarded": [
                "physical equivalence of sound frequency and light frequency",
                "WAV phase interference as evidence",
                "loudness as a scientific amplitude",
            ],
        },
        "state_summary": state_summary,
        "mean_wavelength_shift_galcut20_minus_unmasked_nm": shift,
        "rows": rows,
    }


def svg_text(x: float, y: float, text: str, size: int = 14, anchor: str = "middle") -> str:
    return (
        f'<text x="{x:.2f}" y="{y:.2f}" text-anchor="{anchor}" '
        f'font-family="Inter, Segoe UI, Arial, sans-serif" '
        f'font-size="{size}" fill="#202020">{text}</text>'
    )


def render_svg(rows: list[dict[str, str | int | float]], summary: dict) -> str:
    width, height = 1180, 720
    panels = {"unmasked": 310.0, "galcut20": 870.0}
    y_by_ell = {2: 300.0, 3: 430.0}
    op_offsets = {"Commander": -105.0, "NILC": -35.0, "SEVEM": 35.0, "SMICA": 105.0}
    parts = [
        '<svg xmlns="http://www.w3.org/2000/svg" '
        f'viewBox="0 0 {width} {height}" width="{width}" height="{height}">',
        '<rect width="1180" height="720" fill="#f8f5ed"/>',
        svg_text(590, 48, "Planck Demask-Shift Rendered as Newton Light", size=26),
        svg_text(590, 78, "Same voice-drift mapping as the WAV; light is an inspection instrument, not evidence.", size=13),
    ]

    for state, cx in panels.items():
        parts.append(
            f'<rect x="{cx - 220:.2f}" y="120" width="440" height="430" '
            'rx="6" fill="#fffdf7" stroke="#c8c0ad" stroke-width="1"/>'
        )
        parts.append(svg_text(cx, 154, state, size=20))
        for ell, y in y_by_ell.items():
            parts.append(svg_text(cx - 188, y + 5, f"ell={ell}", size=13, anchor="start"))
            parts.append(
                f'<line x1="{cx - 145:.2f}" y1="{y:.2f}" x2="{cx + 145:.2f}" y2="{y:.2f}" '
                'stroke="#d7ceb9" stroke-width="1"/>'
            )

    for row in rows:
        state = str(row["mask_state"])
        operator = str(row["operator"])
        ell = int(row["ell"])
        cx = panels[state]
        x = cx + op_offsets[operator]
        y = y_by_ell[ell]
        color = str(row["hex"])
        wavelength = float(row["wavelength_nm"])
        band = str(row["newton_band"])
        parts.append(
            f'<line x1="{cx:.2f}" y1="205" x2="{x:.2f}" y2="{y:.2f}" '
            f'stroke="{color}" stroke-width="7" stroke-opacity="0.72"/>'
        )
        parts.append(
            f'<circle cx="{x:.2f}" cy="{y:.2f}" r="16" fill="{color}" '
            'stroke="#242424" stroke-width="1"/>'
        )
        parts.append(svg_text(x, y + 35, operator[:3], size=11))
        parts.append(svg_text(x, y + 51, f"{wavelength:.0f} nm {band}", size=10))

    legend_x = 170
    legend_y = 610
    parts.append(svg_text(590, 590, "Newton-band key: audio octave phase -> visible wavelength", size=15))
    swatch_w = 120
    for idx, (name, lo, hi) in enumerate(NEWTON_BANDS):
        x = legend_x + idx * swatch_w
        mid = (lo + hi) / 2
        color = wavelength_to_rgb_hex(mid)
        parts.append(
            f'<rect x="{x:.2f}" y="{legend_y:.2f}" width="96" height="24" rx="3" '
            f'fill="{color}" stroke="#333" stroke-width="0.7"/>'
        )
        parts.append(svg_text(x + 48, legend_y + 44, name, size=11))

    shift = summary["mean_wavelength_shift_galcut20_minus_unmasked_nm"]
    if shift is not None:
        parts.append(
            svg_text(
                590,
                692,
                f"Mean wavelength shift galcut20 - unmasked: {shift:.1f} nm",
                size=13,
            )
        )
    parts.append("</svg>")
    return "\n".join(parts) + "\n"


def render_report(summary: dict) -> str:
    state = summary["state_summary"]
    shift = summary["mean_wavelength_shift_galcut20_minus_unmasked_nm"]
    lines = [
        "# Newton Voice-Drift Light Rendering",
        "",
        "Status: Opticks/light rendering of an existing sonification mapping; not evidence.",
        "",
        "This artifact reads the Planck voice-drift sonification summary and the",
        "WAV container, then maps the same frequency assignments into a",
        "Newton-style visible spectrum. It does not listen to the note and it",
        "does not treat audio perception as evidence.",
        "",
        "## Conversion Contract",
        "",
        "| source quantity | light mapping | preserved | discarded |",
        "| --- | --- | --- | --- |",
        "| sonified frequency | octave phase within ell-specific octave | pitch-class order induced by longitude | absolute sound frequency |",
        "| octave phase | visible wavelength from 700 nm to 400 nm | circular drift as spectral shift | physical sound-light equivalence |",
        "| wavelength | Newton band and display RGB | inspectable color grouping | spectrometer precision |",
        "| mask state | separate prism panel | before/after comparison | animation and audio phase |",
        "| latitude pan | metadata only | original mapping provenance | claims from stereo perception |",
        "",
        "## WAV Audit",
        "",
        f"- sample rate: `{summary['wav_audit']['sample_rate_hz']}` Hz",
        f"- channels: `{summary['wav_audit']['channels']}`",
        f"- duration: `{summary['wav_audit']['duration_s']:.3f}` s",
        f"- peak abs PCM16: `{summary['wav_audit']['peak_abs_pcm16']:.4f}`",
        f"- RMS PCM16: `{summary['wav_audit']['rms_pcm16']:.4f}`",
        "",
        "## Spectral Readout",
        "",
        "| mask state | mean wavelength | range | Newton-band counts |",
        "| --- | ---: | ---: | --- |",
    ]
    for mask_state, payload in state.items():
        counts = ", ".join(
            f"{name}:{count}" for name, count in sorted(payload["newton_band_counts"].items())
        )
        lines.append(
            f"| {mask_state} | {payload['mean_wavelength_nm']:.1f} nm | "
            f"{payload['min_wavelength_nm']:.1f}-{payload['max_wavelength_nm']:.1f} nm | {counts} |"
        )
    if shift is not None:
        lines.extend(
            [
                "",
                f"Mean spectral shift `galcut20 - unmasked`: `{shift:.1f} nm`.",
                "Negative means the masked state is shifted toward shorter, bluer/violetter wavelengths under this mapping.",
            ]
        )
    lines.extend(
        [
            "",
            "## Allowed Claims",
            "",
            "1. The same operator voice-drift mapping that produced the WAV can be",
            "   rendered as a Newton/Opticks light instrument.",
            "2. The light rendering exposes the before/after mask-state spectral",
            "   shift without relying on listener perception.",
            "3. The artifact is a downstream inspection layer over already-measured",
            "   Planck demask-shift geometry.",
            "",
            "## Forbidden Claims",
            "",
            "1. The light rendering is not new evidence.",
            "2. The mapped wavelengths are not physical gamma-ray wavelengths.",
            "3. The audio frequency to light wavelength map is not a physical",
            "   equivalence; it is an explicit observational instrument.",
            "4. This does not replace nulls, official-mask controls, or Fermi data.",
            "",
            "## Outputs",
            "",
            "- `newton_voice_drift_light.csv`",
            "- `newton_voice_drift_light.svg`",
            "- `newton_voice_drift_light_summary.json`",
            "- `newton_voice_drift_light_report.md`",
            "",
        ]
    )
    return "\n".join(lines)


def write_outputs(summary_path: Path, wav_path: Path, out_dir: Path) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    sonification_summary = load_json(summary_path)
    wav_audit = audit_wav(wav_path)
    rows = build_rows(sonification_summary)
    summary = summarize(rows, wav_audit)

    csv_path = out_dir / "newton_voice_drift_light.csv"
    fieldnames = [
        "mask_state",
        "voice_key",
        "operator",
        "ell",
        "l_deg",
        "b_deg",
        "freq_hz",
        "octave_phase",
        "wavelength_nm",
        "newton_band",
        "hex",
        "pan",
    ]
    with csv_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row[field] for field in fieldnames})

    (out_dir / "newton_voice_drift_light_summary.json").write_text(
        json.dumps(summary, indent=2) + "\n", encoding="utf-8"
    )
    (out_dir / "newton_voice_drift_light.svg").write_text(
        render_svg(rows, summary), encoding="utf-8"
    )
    (out_dir / "newton_voice_drift_light_report.md").write_text(
        render_report(summary), encoding="utf-8"
    )
    print(f"wrote Newton voice-drift light rendering to {out_dir}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--summary-json", type=Path, default=DEFAULT_SUMMARY)
    parser.add_argument("--wav", type=Path, default=DEFAULT_WAV)
    parser.add_argument("--out-dir", type=Path, default=DEFAULT_OUT)
    args = parser.parse_args()
    write_outputs(args.summary_json, args.wav, args.out_dir)


if __name__ == "__main__":
    main()

