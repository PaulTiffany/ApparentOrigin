# Sonification of Operator-Residue Voice Drift

Status: sonification / methodology import artifact, not new evidence.

This report documents an audio rendering of the four Planck PR3
component-separation operators (Commander, NILC, SEVEM, SMICA) at ell=2
and ell=3 across two mask states (unmasked vs `|b|>20°` galcut20). It
is the auditory-channel companion to the visual Opticks axis-residue
map. The conversion contract is fully stated; the WAV is a measurement
readout, not a composition.

Cross-modal precedent: `reports/planck_operator_residue/opticks_axis_residue_map/opticks_axis_residue_map_report.md`.
Data sources:

- `reports/planck_operator_residue/directional_axis_nside64/directional_quadrupole_mlmax_summary.json`
- `reports/planck_operator_residue/directional_axis_nside64/directional_octupole_axis_summary.json`
- `reports/planck_operator_residue/directional_axis_nside64_galcut20/directional_quadrupole_mlmax_summary.json`
- `reports/planck_operator_residue/directional_axis_nside64_galcut20/directional_octupole_axis_summary.json`

## Conversion contract

| source quantity | audio feature | preserved | discarded |
| --- | --- | --- | --- |
| operator (Commander/NILC/SEVEM/SMICA) | one sine voice each | identity, simultaneity | timbre, pipeline-specific noise floor |
| galactic longitude `l_deg` in [0, 360) | exponential pitch sweep over one octave (220 Hz base for ell=2, 440 Hz base for ell=3); `l=0` -> base, `l=360` wraps to `2*base` | circular order; longitude differences become audible musical intervals | absolute pitch identity (no key anchor) |
| multipole ell | octave assignment: ell=2 in lower octave (220-440 Hz), ell=3 in upper octave (440-880 Hz) | quadrupole vs octupole separation | scalar-vs-rank-3 tensor structure |
| galactic latitude `b_deg` in [-90, 90] | equal-power stereo pan in [-1, 1] | pole/equator placement | sky-map projection geometry |
| mask state | piece-time: `~12 s unmasked` -> `3 s linear crossfade` -> `~12 s galcut20`; `1 s` linear edge-fade in/out | temporal succession; before/after audibility | causal interpretation of the transition |
| `|a_lm|^2` magnitude | (NOT MAPPED) all voices held at fixed amplitude (0.10 / voice) | -- | absolute power, signal-to-noise ratio |

No reverb, no envelope shaping beyond chord-edge fades and the inter-
chord crossfade, no rhythm. Pure sine voices.

Sample rate: 44100 Hz, stereo, 16-bit PCM. Total duration: 27.00 s.

## Pitch tables (l_deg -> Hz)

The mapping is `freq_hz = octave_base * 2^(l_deg / 360)` with
`octave_base = 220 Hz` for ell=2 and `octave_base = 440 Hz` for ell=3.

### Unmasked

| operator | ell | l_deg | b_deg | freq (Hz) | pan |
| --- | ---: | ---: | ---: | ---: | ---: |
| Commander | 2 | 237.65 | 47.47 | 347.65 | +0.53 |
| NILC      | 2 | 242.70 | 57.36 | 351.05 | +0.64 |
| SEVEM     | 2 | 207.31 | 64.78 | 327.92 | +0.72 |
| SMICA     | 2 | 237.65 | 54.89 | 347.65 | +0.61 |
| Commander | 3 | 242.70 | 64.78 | 702.10 | +0.72 |
| NILC      | 3 | 237.65 | 62.31 | 695.30 | +0.69 |
| SEVEM     | 3 | 247.76 | 67.25 | 708.97 | +0.75 |
| SMICA     | 3 | 237.65 | 62.31 | 695.30 | +0.69 |

### Galcut20

| operator | ell | l_deg | b_deg | freq (Hz) | pan |
| --- | ---: | ---: | ---: | ---: | ---: |
| Commander | 2 | 257.87 | 30.17 | 361.46 | +0.34 |
| NILC      | 2 | 262.93 | 32.64 | 364.99 | +0.36 |
| SEVEM     | 2 | 252.82 | 32.64 | 357.95 | +0.36 |
| SMICA     | 2 | 257.87 | 32.64 | 361.46 | +0.36 |
| Commander | 3 | 283.15 | 54.89 | 758.97 | +0.61 |
| NILC      | 3 | 283.15 | 57.36 | 758.97 | +0.64 |
| SEVEM     | 3 | 293.27 | 52.42 | 773.89 | +0.58 |
| SMICA     | 3 | 278.10 | 54.89 | 751.62 | +0.61 |

### Within-chord pitch dispersion

| condition | ell | min (Hz) | max (Hz) | spread (cents) |
| --- | ---: | ---: | ---: | ---: |
| unmasked | 2 | 327.92 | 351.05 | **118.0** |
| unmasked | 3 | 695.30 | 708.97 | 33.7 |
| galcut20 | 2 | 357.95 | 364.99 | **33.7** |
| galcut20 | 3 | 751.62 | 773.89 | 50.6 |

A 118-cent spread is just over a tempered semitone (100 cents);
33-50-cent spreads are within a quarter-tone. The reference threshold
for *audible roughness* between two simultaneous pure tones is ~30-40
cents at this fundamental range (the critical-band beating regime).

## Readout: what the listener should hear

This rendering is honest about what it does and does not show.

**Lower octave (ell=2, around 330-365 Hz).** The unmasked chord has a
~118-cent internal spread, dominated by SEVEM at 327.92 Hz vs the other
three near 347-351 Hz. The listener should hear the lower octave of
chord A as an audibly *rough* cluster — beating, semitonal width.
Under masking the lower-octave voices collapse to ~34 cents of spread:
the four ell=2 voices fuse into a tight cluster that is just barely
distinguishable from a unison, with mild beating but no semitone
roughness. **At ell=2, masking moves the chord toward fusion, not away
from it.** This matches the directional-axis report: operator-axis
dispersion at ell=2 falls from 14.1° unmasked to 4.6° under galcut20.

**Upper octave (ell=3, around 695-775 Hz).** The unmasked chord is
already tight at 33.7 cents. Under masking it widens slightly to 50.6
cents, mostly because SEVEM walks ~10° in longitude. The shift is
audible but small.

**Cross-octave Q-O alignment.** What the original brief framed as the
"dissonance shift" lives between the lower and upper octaves of the
*same operator*: the angle between each operator's ell=2 and ell=3 axes
goes from median 11.9° (unmasked) to 29.5° (galcut20). In pitch terms,
that means each operator's lower voice and upper voice come from
similar longitudes unmasked (consonant pairing across the octave) and
from drifted longitudes galcut20 (each operator's octave pairing is
itself off-tune). This is *not* something a naive ear easily picks out
in a 4-voice + 4-voice stereo blend: the listener has to track a single
operator's two voices through the chord. It is the audible signature
the brief was reaching for, but it is harder to hear than the
within-chord cluster width at ell=2.

**Honest summary.** The most audible feature is the *opposite* of what
the brief's headline suggested: the lower-octave chord goes from rough
(unmasked) to fused (galcut20). The cross-octave per-operator detuning
is in the data and is encoded faithfully, but it is not the dominant
auditory percept in this voicing. The "cacophony shift" framing fits
the visual Q-O alignment angle better than it fits the auditory
chord-fusion percept of this particular sonification.

## Visual-vs-auditory channel claim

The framework gesture is that the auditory system has sharper temporal
and dissonance discrimination than the visual system, and that
sonification therefore makes some operator-residue features easier to
inspect than the visual chart does. Confidence-quantified:

| claim | confidence |
| --- | ---: |
| longitude is on a topological circle and pitch-class is on a topological circle, so longitude -> pitch is an isomorphism of S^1 -> S^1 (the conversion is well-formed) | ~95% |
| the auditory system resolves frequency ratios at smaller fractional thresholds than the visual system resolves color ratios in the analogous sense | ~70% |
| in *this specific* sonification, an attentive listener picks out the within-chord ell=2 dispersion shift more easily than an attentive viewer picks it out from the Opticks chart | ~55% |
| sonification reveals patterns that visual inspection of the same data does not | ~30% — not demonstrated by this artifact; the dominant audible feature is the ell=2 chord-fusion direction, which the directional-axis tables already make obvious |
| the "auditory channel as a real method" claim, in the strong sense of finding new structure, deserves the methodology-import phase tag and not an evidential phase tag | ~95% |

The honest reading is that this sonification is *useful* (the within-
chord narrowing under masking is audibly striking) but it does not
out-perform the existing directional tables on this dataset. It earns
its place as an instrumentation/methodology import; the case for
auditory channel surfacing genuinely new structure has to be made on a
different dataset (e.g. larger ensembles, time-evolving alm, or
realization sweeps where the eye loses the structure first).

## Allowed claims

1. The conversion contract longitude->pitch is a well-formed S^1->S^1
   isomorphism over one octave.
2. The four ell=2 voices audibly tighten from a ~118-cent rough cluster
   to a ~34-cent near-unison cluster between unmasked and galcut20
   chords. This matches the operator-axis dispersion dropping from
   14.1° to 4.6° in the directional-axis report.
3. The four ell=3 voices remain tight in both chords (33-51 cents).
4. The piece-time succession (chord A -> crossfade -> chord B) gives
   the listener an A/B comparison without rhythm or composition.
5. Sonification is a legitimate cross-modal methodology import for
   directional-axis residue data, on the same epistemic footing as the
   Opticks visual chart.

## Forbidden claims

1. The WAV is not new evidence; pitch differences encode existing
   longitude differences; auditory dissonance perception is sharper
   than visual but the underlying data is unchanged.
2. The audible chord-narrowing under masking is not a discovery; it is
   a re-presentation of the published 14.1° -> 4.6° operator-axis
   dispersion drop with a different sensory channel.
3. The ell=2 -> ell=3 cross-octave detuning per operator (the Q-O
   alignment angle) is *encoded* in the rendering, but the WAV is not a
   statistical demonstration of that angle's mask-state shift.
4. This sonification does not refute or confirm any AOC claim, the
   axis-of-evil literature, or the bounded-observer conjecture.
5. Auditory perception sharpness over visual perception sharpness is a
   framework-level proposition that this single artifact does not
   establish; the case for auditory-channel-as-real-method has to be
   made on a dataset where the visual channel demonstrably loses
   structure first.

## Phase tag

Sonification / methodology import artifact, not evidence. Cross-modal
companion to the Opticks visual chart. Disciplined to a measurement
readout; explicitly not a composition.

## Outputs

- `sonification_voice_drift.wav` — 27.00 s, 44100 Hz, stereo, 16-bit PCM
- `sonification_voice_drift_score.png` — piano-roll of 8 voices across 2 chords
- `sonification_voice_drift_summary.json` — pitch table, durations, conversion contract
- `sonification_voice_drift_report.md` — this document

Provenance:

```text
empirical/planck_operator_residue/sonify_voice_drift.py
```
