# Opticks Axis-Residue Map v2

Status: composition/media instrumentation artifact, not evidence.

This v2 chart extends the v1 two-channel (hue, radius) Opticks-style
encoding by activating a third channel (saturation) over the same
directional operator-axis data. Saturation is a faithful re-encoding
of an already-computed quantity (per-multipole-normalized score
amplitude); it introduces no new statistical handle. Value is held
in reserve at 1.0 by deliberate under-use.

Phase tag: composition/media instrumentation, not evidence. The
geometricity-from-observer-measurement primitive motivates importing
paint-technique discipline (bounded chromatic channels, intentional
channel reservation) as actual chart method, not the other way
around.

## Conversion Contract

| source quantity | conversion | preserved | discarded |
| --- | --- | --- | --- |
| galactic longitude `l_deg` | hue on 0-360 wheel | circular order, clustering, mask-state shift | physical wavelength identity |
| galactic latitude `b_deg` | radius from galactic north pole, `r = R * (1 - abs(b)/90)` | pole/equator ordering | sky-map area, projection fidelity |
| score amplitude (`max_a22^2` for ell=2, `max_a33^2` for ell=3) | saturation, `sat = SAT_FLOOR + (1 - SAT_FLOOR) * score / max_score_per_multipole` (`SAT_FLOOR=0.18`) | relative score amplitude within each multipole | absolute score scale, cross-multipole amplitude comparison |
| (reserved) | value held constant at 1.0 | a deliberate empty channel | nothing yet; reserved for a future earned channel (e.g. uncertainty) |
| hue sector | sevenfold note label `C D E F G A B` | aesthetic/compositional grouping | exact musical pitch or Newtonian historical assignment |
| multipole | marker shape: circle for ell=2, diamond for ell=3 | quadrupole/octupole distinction | statistical significance |

Saturation normalization is per-multipole: the strongest ell=2 mark and
the strongest ell=3 mark each reach `sat = 1.0`. Cross-ell saturation
comparisons are therefore not meaningful and are not licensed by the
chart.

## Score Normalization Constants

| multipole | min(score) | max(score) | sat range observed |
| --- | ---: | ---: | ---: |
| ell=2 | 1.437e-10 | 5.224e-10 | 0.405 -> 1.000 |
| ell=3 | 3.158e-10 | 1.628e-09 | 0.339 -> 1.000 |

## Readout

| condition | median Q-O alignment | saturation/composition read |
| --- | ---: | --- |
| unmasked | 11.9 deg | ell=2 and ell=3 marks cluster in nearby hue/radius cells; saturation makes the relative score-strength ordering across operators visible at a glance |
| galcut20 | 29.5 deg | mask-state shift moves both multipoles around the hue wheel; saturation rebalances when the cut suppresses certain operators' scores more than others |

What v2 makes visible that v1 did not:

1. Operator-by-operator score ordering is inspectable directly from the
   marker rather than only via the underlying JSON. In v1 every Commander
   marker had the same chroma; in v2 the strongest-scoring operator at
   each multipole is most chromatic, the weakest-scoring is desaturated
   toward the saturation floor.
2. Mask-state cross-condition score reweighting is visible: where the
   galcut20 mask suppresses one operator's score relative to another,
   that operator's marker desaturates relative to its peers.
3. The chart's chromatic budget now carries 3 of 4 channels; the empty
   value channel is itself a visible discipline mark, not a defect.

## Confidence on Structural-Similarity Claim

Claim: "saturation as a faithful encoding of score amplitude" — i.e.,
the saturation channel as drawn corresponds monotonically (within each
multipole) to the source `max_a^2` value, with the strongest mark fully
saturated and the weakest at the documented floor.

Confidence: 95%. The mapping is a closed-form per-multipole
normalization with a documented floor; the only soft choices are
(a) the floor value (chosen for legibility, not from theory) and
(b) the per-multipole rather than global normalization (chosen so
ell=2 and ell=3 marks aren't on a shared scale, which would make the
weaker multipole permanently desaturated). Neither soft choice is a
physics claim. The 5% reserve is for the standing risk that a viewer
interprets cross-ell saturation as a comparison the chart does not
license.

## Allowed Claims

1. Saturation faithfully re-encodes the per-multipole-normalized score
   amplitude already in the directional summaries.
2. The v2 chart makes operator-by-operator score ordering and
   mask-state score reweighting inspectable in the same medium that
   already shows hue/radius/note structure.
3. The reserved value channel is a deliberate discipline mark; under-
   using a channel is part of the contract.

## Forbidden Claims

1. Saturation differences are not new evidence; saturation encodes
   existing score amplitudes from the directional-axis summaries.
2. Cross-multipole saturation comparisons (ell=2 vs ell=3) are not
   licensed: each multipole has its own normalization.
3. The chart does not replace statistical nulls, mask-state controls,
   or the Planck likelihood machinery.
4. The Opticks bridge remains a near-cousin/instrumentation layer, not
   an instantiation-grade cosmological claim.
5. The reserved value channel is not evidence of an unmodeled handle;
   it is an admission of an unearned one.

## Outputs

- `opticks_axis_residue_map_v2.svg`
- `opticks_axis_residue_map_v2.csv`
- `opticks_axis_residue_map_v2_summary.json`
