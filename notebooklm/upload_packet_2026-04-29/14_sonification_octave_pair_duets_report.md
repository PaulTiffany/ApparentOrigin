# Octave-Pair Duet Sonification (Sprint C-prime)

Status: sonification / methodology import artifact, not new evidence —
duet companion to Sprint D sim-null.

## Brief

Sprint C-prime is a re-voicing of the Episode 2 operator-residue
sonification. Episode 2 played all eight voices simultaneously
(Commander/NILC/SEVEM/SMICA × ell=2/ell=3) and returned an honest null
on the strong "auditory channel reveals what visual cannot" claim: the
dominant percept was the within-chord ell=2 dispersion shift under
masking (118 cents -> 34 cents), which the visual directional-axis
table already makes obvious. The cross-octave per-operator Q-O detuning
(median 11.9° unmasked -> 29.5° galcut20) was encoded faithfully but
buried under chord fusion. C-prime addresses that limitation by
splitting the eight voices into four 2-voice duets — one per operator —
so the listener can attend to *one* pipeline's cross-octave drift at a
time. It is a methodology import re-render, not new evidence; Sprint D
remains the empirical-class test for cross-pipeline structure.

Cross-modal precedent: `reports/planck_operator_residue/sonification_voice_drift/sonification_voice_drift_report.md`.

Data sources:

- `reports/planck_operator_residue/directional_axis_nside64/directional_quadrupole_mlmax_summary.json`
- `reports/planck_operator_residue/directional_axis_nside64/directional_octupole_axis_summary.json`
- `reports/planck_operator_residue/directional_axis_nside64_galcut20/directional_quadrupole_mlmax_summary.json`
- `reports/planck_operator_residue/directional_axis_nside64_galcut20/directional_octupole_axis_summary.json`

## Conversion contract

| source quantity | audio feature | preserved | discarded |
| --- | --- | --- | --- |
| operator (Commander/NILC/SEVEM/SMICA) | one separate 2-voice piece per operator | per-pipeline isolation; cross-octave detuning within one operator | simultaneity across operators (deliberately removed) |
| galactic longitude `l_deg` in [0, 360) | exponential pitch sweep over one octave (220 Hz base for ell=2, 440 Hz base for ell=3); `freq_hz = octave_base * 2^(l_deg / 360)` | circular order; longitude differences become audible musical intervals | absolute pitch identity (no key anchor) |
| multipole ell | octave assignment: ell=2 in lower octave (220-440 Hz), ell=3 in upper octave (440-880 Hz) | quadrupole vs octupole separation | scalar-vs-rank-3 tensor structure |
| galactic latitude `b_deg` in [-90, 90] | equal-power stereo pan in [-1, 1] | pole/equator placement | sky-map projection geometry |
| mask state | piece-time: `~6 s unmasked` -> `1 s linear crossfade` -> `~6 s galcut20`; `0.5 s` linear edge-fade in/out | temporal succession; before/after audibility within one operator | causal interpretation of the transition |
| `\|a_lm\|^2` magnitude | (NOT MAPPED) all voices held at fixed amplitude (0.35 / voice) | -- | absolute power, signal-to-noise ratio |

Additions vs. Episode 2 (documented as deltas, not as a new contract):

- Voices per piece: **2** instead of 8.
- Per-operator durations: **6+1+6 s** (total ~13 s) instead of 12+3+12 s.
- Voice amplitude: **0.35** instead of 0.10 (only two voices summing,
  comfortable headroom; observed peak across the four duets is
  0.64-0.68, ~30% headroom against 0.95 clipping threshold).
- Output set: four per-operator WAVs plus
  `all_pipelines_sequential.wav` (concatenated playthrough, 1 s silent
  gaps between operators, total 55 s).

No reverb, no envelope shaping beyond chord-edge fades and the
inter-chord crossfade, no rhythm. Pure sine voices.

Sample rate: 44100 Hz, stereo, 16-bit PCM. Per-operator duration:
13.00 s. Concatenated piece: 55.00 s.

## Per-operator pitch tables (l_deg -> Hz)

The mapping is `freq_hz = octave_base * 2^(l_deg / 360)` with
`octave_base = 220 Hz` for ell=2 and `octave_base = 440 Hz` for ell=3.

### Commander

| ell | condition | l_deg | b_deg | freq (Hz) | pan |
| ---: | --- | ---: | ---: | ---: | ---: |
| 2 | unmasked | 237.65 | 47.47 | 347.65 | +0.53 |
| 3 | unmasked | 242.70 | 64.78 | 702.10 | +0.72 |
| 2 | galcut20 | 257.87 | 30.17 | 361.46 | +0.34 |
| 3 | galcut20 | 283.15 | 54.89 | 758.97 | +0.61 |

### NILC

| ell | condition | l_deg | b_deg | freq (Hz) | pan |
| ---: | --- | ---: | ---: | ---: | ---: |
| 2 | unmasked | 242.70 | 57.36 | 351.05 | +0.64 |
| 3 | unmasked | 237.65 | 62.31 | 695.30 | +0.69 |
| 2 | galcut20 | 262.93 | 32.64 | 364.99 | +0.36 |
| 3 | galcut20 | 283.15 | 57.36 | 758.97 | +0.64 |

### SEVEM

| ell | condition | l_deg | b_deg | freq (Hz) | pan |
| ---: | --- | ---: | ---: | ---: | ---: |
| 2 | unmasked | 207.31 | 64.78 | 327.92 | +0.72 |
| 3 | unmasked | 247.76 | 67.25 | 708.97 | +0.75 |
| 2 | galcut20 | 252.82 | 32.64 | 357.95 | +0.36 |
| 3 | galcut20 | 293.27 | 52.42 | 773.89 | +0.58 |

### SMICA

| ell | condition | l_deg | b_deg | freq (Hz) | pan |
| ---: | --- | ---: | ---: | ---: | ---: |
| 2 | unmasked | 237.65 | 54.89 | 347.65 | +0.61 |
| 3 | unmasked | 237.65 | 62.31 | 695.30 | +0.69 |
| 2 | galcut20 | 257.87 | 32.64 | 361.46 | +0.36 |
| 3 | galcut20 | 278.10 | 54.89 | 751.62 | +0.61 |

## Per-operator Q-O detuning angles

Angle between each operator's ell=2 and ell=3 cartesian axis vectors
(read directly from `axes_cartesian.operator` in the source JSONs).

| operator | unmasked | galcut20 | delta |
| --- | ---: | ---: | ---: |
| Commander | 17.52° | 30.60° | +13.08° |
| NILC      |  5.56° | 28.32° | +22.76° |
| SEVEM     | 16.33° | 35.09° | +18.76° |
| SMICA     |  7.42° | 26.40° | +18.99° |

All four operators move in the same direction (cross-octave alignment
*loosens* under masking), consistent with the Episode 2 median shift
(11.9° -> 29.5°). NILC starts the most consonant (5.56°, a quarter-tone-
class interval at the conversion ratio) and walks the largest delta;
SEVEM ends the most detuned (35.09°). Commander has the smallest delta
(+13.08°). The galcut20 column is tighter than the unmasked column
(range 26.4-35.1° vs 5.6-17.5°) — under masking the four pipelines
converge toward a similar amount of cross-octave detuning.

## Listener guide

Each duet is a single piece in two phases. In phase A (0-6 s, light
blue background on the score) the listener hears the operator's ell=2
and ell=3 axes as a two-note interval whose width encodes the
unmasked Q-O alignment. The 1 s crossfade (6-7 s, tan background)
moves both voices to their galcut20 longitudes; in phase B (7-13 s)
the listener hears the same two-note interval at its galcut20 width.

What to track within each duet: whether the lower voice (ell=2) and
the upper voice (ell=3) come from similar longitudes (consonant
octave-pair, small Q-O angle) or from drifted longitudes (detuned
octave-pair, large Q-O angle). The structural pattern is that all four
operators move from "more consonant" toward "more detuned" across the
mask transition, but the magnitudes differ:

- **NILC** is the most striking by relative change: phase A is nearly
  a clean octave (5.56° = both axes at the same longitude within ~5°),
  phase B is unambiguously detuned (28.32°). The audible "before
  closer-to-octave, after off" reading is cleanest here.
- **SEVEM** is the most striking by absolute end-state: phase B
  detuning (35.09°) is the largest of the four. Its phase-A ell=2
  longitude (207.31°) is also the lone outlier across the four
  pipelines, audible as the lowest ell=2 starting frequency
  (327.92 Hz).
- **Commander** moves least (+13.08° delta). The audible difference
  between phase A and phase B is real but the smallest of the four.
- **SMICA** behaves like a less-extreme NILC: small unmasked
  alignment (7.42°), moderate end-state (26.40°).

The `all_pipelines_sequential.wav` plays the four duets in order
Commander -> NILC -> SEVEM -> SMICA with 1 s silences between them.
This is a sequential A/B/C/D readout, not a chord — it lets the
listener carry one operator's cross-octave reference into the next
without 8-voice fusion masking the per-pipeline structure.

Honest framing: this voicing isolates the per-pipeline cross-octave
structure that Episode 2's 8-voice voicing buried under chord fusion.
It is still a rendering, not new evidence. The Q-O detuning numbers
in the table above are read directly from the directional-axis JSONs;
the audio is a re-presentation, not a measurement.

## Confidence on the listener-guide claim

Claim: "duet voicing makes per-pipeline Q-O detuning more inspectable
than the 8-voice voicing of Episode 2."

Confidence: **80%**. The structural argument is sound: removing six of
the eight simultaneous voices removes the chord-fusion percept that
Episode 2's report explicitly named as the dominant audible feature,
which mechanically makes the remaining two voices' relative interval
the foreground. The Q-O alignment angles span 5.6°-17.5° unmasked and
26.4°-35.1° galcut20 — these correspond to interval-width changes that
a listener attending to *one* operator's two voices should pick up
more easily than the same two voices embedded in an eight-voice chord.

The 20% reserve covers the soft side: on a casual listen the
audio is not dramatically different from Episode 2 — they share the
same primitives (sine voices, longitude->pitch mapping, equal-power
pan, edge fades, crossfade), and the per-operator pitch differences
are still small in absolute terms (the largest within-duet phase-A
interval, NILC, is 695.30 Hz vs 351.05 Hz, almost exactly a clean
octave; the audible "detuning" is on top of an octave that the ear
heavily fuses). The improvement is real but modest, and the
empirical-class question of cross-pipeline structure belongs to
Sprint D, not to this rendering.

## Allowed claims

1. The conversion contract longitude->pitch is a well-formed S^1->S^1
   isomorphism over one octave (preserved verbatim from Episode 2).
2. Each per-operator duet faithfully encodes that operator's ell=2 and
   ell=3 longitudes (and latitudes via stereo pan) at the unmasked and
   galcut20 mask states. The Q-O alignment angles in the table above
   are computed directly from the source axis JSONs, not from the
   audio.
3. All four operators show monotonic loosening of cross-octave
   alignment under galcut20 masking (Commander +13.08°, NILC +22.76°,
   SEVEM +18.76°, SMICA +18.99°), consistent with the Episode 2
   directional-axis median shift (11.9° -> 29.5°).
4. The 2-voice duet voicing isolates per-pipeline cross-octave
   structure that the 8-voice voicing in Episode 2 audibly buried
   under chord fusion. This is a re-voicing improvement at the
   composition layer, not a new statistical handle.
5. Sonification remains a legitimate cross-modal methodology import
   for directional-axis residue data, on the same epistemic footing
   as the Opticks visual chart.

## Forbidden claims

1. The WAV is not new evidence; pitch differences encode existing
   longitude differences from the directional-axis summaries
   (preserved from Episode 2).
2. Per-operator audible Q-O detuning is not statistical evidence of
   pipeline interdependence — Sprint D is the empirical-class test
   that addresses cross-pipeline structure under sim-null calibration.
3. The duet voicing does not establish auditory-channel sharpness over
   visual-channel sharpness. Episode 2 returned an honest null on that
   strong claim; C-prime is a different voicing addressing a different
   feature, not a counter-claim.
4. This sonification does not refute or confirm any AOC claim, the
   axis-of-evil literature, or the bounded-observer conjecture.
5. SEVEM's outlier behavior (largest absolute galcut20 detuning, lone
   ell=2 unmasked longitude at 207.31°) and NILC's outlier behavior
   (largest mask-state delta) are not new findings; the underlying
   axis values are unchanged from the directional-axis report and the
   Episode 2 sonification.

## Phase tag

Sonification / methodology import artifact, not evidence. Composition
companion to Sprint D's sim-null calibration. Disciplined to a
measurement readout; explicitly not a composition.

## Outputs

- `commander_duet.wav` — 13.00 s, 44100 Hz, stereo, 16-bit PCM, peak 0.6677
- `nilc_duet.wav` — 13.00 s, 44100 Hz, stereo, 16-bit PCM, peak 0.6757
- `sevem_duet.wav` — 13.00 s, 44100 Hz, stereo, 16-bit PCM, peak 0.6847
- `smica_duet.wav` — 13.00 s, 44100 Hz, stereo, 16-bit PCM, peak 0.6407
- `all_pipelines_sequential.wav` — 55.00 s, 44100 Hz, stereo, 16-bit PCM, peak 0.6847
- `sonification_octave_pair_duets_score.png` — piano-roll listening guide, 4 stacked panels (one per operator), ell=2 + ell=3 voice trajectories across the unmasked -> galcut20 transition
- `sonification_octave_pair_duets_summary.json` — per-operator pitch tables, Q-O detuning angles, conversion-contract decisions
- `sonification_octave_pair_duets_report.md` — this document

Provenance:

```text
empirical/planck_operator_residue/sonify_octave_pair_duets.py
```
