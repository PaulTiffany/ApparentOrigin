# Directional Axis Galcut Sweep Null

Status: isotropic low-ell threshold-sweep null for the synthetic galactic
cut directional-axis curve.

## Question

Under isotropic ell=2/ell=3 skies, how often does the same synthetic
cut family produce a Q-O cliff at least as large as the Planck
`20 -> 25 deg` threshold feature?

## Setup

- Seeds: 1000
- Cuts: 0.0, 5.0, 10.0, 15.0, 20.0, 25.0, 30.0 deg
- Sky prior: isotropic Gaussian ell=2 and ell=3 only, with
  `C_ell proportional to 1/[ell(ell+1)]`
- Extraction: direct pseudo-alms with mean subtraction on retained sky

## Tail Fractions

| metric | observed | null median | 5-95% null | tail |
| --- | ---: | ---: | ---: | ---: |
| `jump_20_25_deg` | 51.51 | 3.866 | 0-16.62 | 0.002 |
| `max_adjacent_jump_deg` | 51.51 | 8.536 | 3.184-38.55 | 0.017 |

Per-cut Q-O tails:

| cut | observed Q-O | null median | 5-95% null | tail >= observed |
| ---: | ---: | ---: | ---: | ---: |
| 0.0 | 8.582 | 59.04 | 18.88-86.29 | 0.99 |
| 5.0 | 17.25 | 59.26 | 18.62-87 | 0.96 |
| 10.0 | 23.8 | 57.88 | 18.55-87.87 | 0.916 |
| 15.0 | 29.08 | 55.86 | 17.4-87.63 | 0.868 |
| 20.0 | 29.46 | 54.33 | 16.58-86.62 | 0.836 |
| 25.0 | 80.97 | 51.52 | 15.7-86.51 | 0.118 |
| 30.0 | 56.09 | 50.32 | 13.49-85.81 | 0.424 |

## Readout

The specific threshold statistic and the look-elsewhere statistic must
both be read. `jump_20_25_deg` asks whether the observed cliff at the
pre-named threshold is unusual. `max_adjacent_jump_deg` asks whether a
cliff this large anywhere in the seven-cut sweep is unusual.

In this null, the named threshold cliff has tail `0.002`
and the sweep-level look-elsewhere tail is `0.017`.
The high Q-O value at `cut=25` alone is less diagnostic than the
adjacent discontinuity: the statistic is about recomposition across a
changing mask contract, not simply about one large masked-sky angle.

## Allowed Claims

1. This null tests whether the observed galcut-threshold cliff is typical
   under isotropic low-ell skies and the same synthetic mask family.
2. It controls the Opticks-induced hypothesis by converting the visual
   sector transition back into a numeric statistic.
3. It can motivate a high-ell leakage or official-mask sweep if the
   threshold feature remains uncommon.

## Forbidden Claims

1. This proves or refutes AOC.
2. This replaces a full Planck likelihood or official mask analysis.
3. This simulates component-separation pipelines or foregrounds.
4. A rare threshold feature is automatically a cosmological transition.

## Limitations

- No Planck component-separation operators are simulated.
- No beam, detector noise, foregrounds, inpainting, or official Planck mask is simulated.
- Only ell=2 and ell=3 are generated, so leakage from higher multipoles is absent.
- The extraction uses direct pseudo-alms with mean subtraction, matching the fallback extractor convention.
- This is a null for the threshold-sweep shape, not a Planck likelihood.

