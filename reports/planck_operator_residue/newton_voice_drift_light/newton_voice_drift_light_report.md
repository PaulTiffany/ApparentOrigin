# Newton Voice-Drift Light Rendering

Status: Opticks/light rendering of an existing sonification mapping; not evidence.

This artifact reads the Planck voice-drift sonification summary and the
WAV container, then maps the same frequency assignments into a
Newton-style visible spectrum. It does not listen to the note and it
does not treat audio perception as evidence.

## Conversion Contract

| source quantity | light mapping | preserved | discarded |
| --- | --- | --- | --- |
| sonified frequency | octave phase within ell-specific octave | pitch-class order induced by longitude | absolute sound frequency |
| octave phase | visible wavelength from 700 nm to 400 nm | circular drift as spectral shift | physical sound-light equivalence |
| wavelength | Newton band and display RGB | inspectable color grouping | spectrometer precision |
| mask state | separate prism panel | before/after comparison | animation and audio phase |
| latitude pan | metadata only | original mapping provenance | claims from stereo perception |

## WAV Audit

- sample rate: `44100` Hz
- channels: `2`
- duration: `27.000` s
- peak abs PCM16: `0.7087`
- RMS PCM16: `0.1655`

## Spectral Readout

| mask state | mean wavelength | range | Newton-band counts |
| --- | ---: | ---: | --- |
| unmasked | 503.0 nm | 493.5-527.2 nm | blue:7, green:1 |
| galcut20 | 474.0 nm | 455.6-489.3 nm | indigo:8 |

Mean spectral shift `galcut20 - unmasked`: `-29.0 nm`.
Negative means the masked state is shifted toward shorter, bluer/violetter wavelengths under this mapping.

## Allowed Claims

1. The same operator voice-drift mapping that produced the WAV can be
   rendered as a Newton/Opticks light instrument.
2. The light rendering exposes the before/after mask-state spectral
   shift without relying on listener perception.
3. The artifact is a downstream inspection layer over already-measured
   Planck demask-shift geometry.

## Forbidden Claims

1. The light rendering is not new evidence.
2. The mapped wavelengths are not physical gamma-ray wavelengths.
3. The audio frequency to light wavelength map is not a physical
   equivalence; it is an explicit observational instrument.
4. This does not replace nulls, official-mask controls, or Fermi data.

## Outputs

- `newton_voice_drift_light.csv`
- `newton_voice_drift_light.svg`
- `newton_voice_drift_light_summary.json`
- `newton_voice_drift_light_report.md`
