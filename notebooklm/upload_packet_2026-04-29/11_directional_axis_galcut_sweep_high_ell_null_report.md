# Directional Axis Galcut Sweep High-Ell Leakage Null

Status: P2 high-ell leakage threshold-sweep null.

## Question

Does simple isotropic high-ell leakage through the synthetic galactic
cut family make the observed Planck adjacent Q-O cliff ordinary?

## Setup

- Seeds: 1000
- Cuts: 0.0, 5.0, 10.0, 15.0, 20.0, 25.0, 30.0 deg
- Multipoles: `2 <= ell <= 30`
- High-ell scale: `1.0`
- Prior: C_ell proportional to 1/[ell(ell+1)] for 2<=ell<=30
- Extraction: direct pseudo-alms at ell=2 and ell=3 after masking

## Frozen P2 Decision Boundary

- Metric: `max_adjacent_jump_deg`
- Boundary: `0.05`
- Rule: tail > 0.05 means simple leakage plausibly explains the cliff under this control; tail <= 0.05 means it does not
- Result: `leakage_does_not_explain_under_control`

## Tail Fractions

| metric | observed | null median | 5-95% null | tail |
| --- | ---: | ---: | ---: | ---: |
| `jump_20_25_deg` | 51.51 | 5.018 | 0.287-22.4 | 0.004 |
| `max_adjacent_jump_deg` | 51.51 | 13.21 | 4.708-43.22 | 0.021 |

Per-cut Q-O tails:

| cut | observed Q-O | null median | 5-95% null | tail >= observed |
| ---: | ---: | ---: | ---: | ---: |
| 0.0 | 8.582 | 59.96 | 17.82-86.76 | 0.992 |
| 5.0 | 17.25 | 60.14 | 18.65-87.27 | 0.957 |
| 10.0 | 23.8 | 59.45 | 18.52-87.31 | 0.921 |
| 15.0 | 29.08 | 57.64 | 19.86-86.57 | 0.869 |
| 20.0 | 29.46 | 56.59 | 18.29-86.2 | 0.854 |
| 25.0 | 80.97 | 56.14 | 15.58-85.85 | 0.129 |
| 30.0 | 56.09 | 53.9 | 13.87-86.13 | 0.472 |

## Readout

This is the predeclared P2 fork. If the look-elsewhere tail rises above
`0.05`, simple high-ell leakage is enough to make the observed adjacent
cliff ordinary under this control. If it remains below `0.05`, simple
leakage does not explain the cliff here, and the official-mask
specificity control becomes the next meaningful test.

## Allowed Claims

1. This tests whether simple high-ell leakage explains the galcut
   threshold cliff under the stated synthetic-mask null.
2. The P2 decision boundary was frozen before this run.
3. The result can decide whether P3 official-mask specificity is worth
   prioritizing.

## Forbidden Claims

1. This proves or refutes AOC.
2. This replaces a full Planck likelihood or official mask analysis.
3. This simulates component separation, beam, detector noise, or
   foreground physics.
4. Either P2 fork counts as confirmation of the framework.

## Limitations

- No Planck component-separation operators are simulated.
- No beam, detector noise, foregrounds, inpainting, or official Planck mask is simulated.
- High-ell content uses a simple flat-Sachs-Wolfe-like power law, not a precision LambdaCDM Cl.
- The extraction uses direct pseudo-alms with mean subtraction, matching the fallback extractor convention.
- This is a high-ell leakage control for the threshold-sweep shape, not a Planck likelihood.
