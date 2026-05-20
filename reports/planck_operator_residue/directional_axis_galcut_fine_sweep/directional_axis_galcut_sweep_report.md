# Directional Axis Galcut Sweep

Status: synthetic-mask threshold sweep for the corrected ell=2/ell=3
m=ell-maximizing directional statistic.

## Question

Does the Opticks-observed sector transition behave like a smooth mask
deformation or like a sharper recomposition as the feasible sky contract
changes?

## Setup

- Cuts: 20.0, 21.0, 22.0, 23.0, 24.0, 25.0 deg
- nside_out: 64
- axis grid: 37 x 72
- Mask: synthetic galactic cut, retaining `|b| > cut`
- Extraction: fallback direct pseudo-alms at ell=2 and ell=3

## Sweep Metrics

| cut | f_sky | median Q-O | ell=2 dispersion | ell=3 dispersion | ell=2 notes | ell=3 notes | mean ell=2 l | mean ell=3 l |
| ---: | ---: | ---: | ---: | ---: | --- | --- | ---: | ---: |
| 20.0 | 0.6615 | 29.5 | 4.6 | 5.1 | AG | A | 257.9 | 284.4 |
| 21.0 | 0.6406 | 32.5 | 2.5 | 6.9 | AG | A | 254.1 | 286.9 |
| 22.0 | 0.6302 | 33.6 | 4.4 | 5.7 | AG | A | 252.8 | 288.2 |
| 23.0 | 0.6094 | 41.0 | 4.4 | 8.1 | G | A | 241.4 | 293.2 |
| 24.0 | 0.5885 | 79.9 | 12.9 | 10.2 | FG | AB | 198.5 | 305.9 |
| 25.0 | 0.5781 | 81.0 | 8.2 | 11.5 | F | AB | 188.4 | 316.1 |

## Readout

The sector transition is not just decorative. From `cut=0` through
`cut=20`, the mean longitudes drift in a controlled way from the G
sector toward A while operator dispersion stays comparatively small.
The largest adjacent Q-O jump occurs between `23.0` and
`24.0` deg, with a change of `38.9` deg. At
`cut=25`, ell=2 has recomposed into the F sector and ell=3 has moved
toward A/B, with median Q-O alignment weakening to about `81 deg`.

`cut=0` is a near-full-sky synthetic-mask case (`f_sky < 1`), not a
replacement for the separately reported unmasked coefficient table.
The result is therefore a threshold-sweep readout of this extractor
and mask family, not a new absolute all-sky axis estimate.


## Allowed Claims

1. This sweep maps how the fallback directional statistic responds to
   synthetic galactic-plane removal.
2. Note-sector changes are useful as a compact compositional readout of
   longitude movement under the explicit Opticks conversion contract.
3. A sharp change in this sweep can motivate a richer mask/instrumentation
   control.

## Forbidden Claims

1. This sweep is not evidence for AOC.
2. Synthetic galactic cuts are not official Planck masks.
3. The note sectors are not physical pitch measurements.
4. A threshold feature in the fallback extractor is not automatically a
   cosmological phase transition.

## Outputs

- `directional_axis_galcut_sweep_metrics.csv`
- `directional_axis_galcut_sweep_axes.csv`
- `directional_axis_galcut_sweep_summary.json`
