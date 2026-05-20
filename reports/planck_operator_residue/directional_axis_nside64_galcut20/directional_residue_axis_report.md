# Planck Operator-Residue Directional Analysis (galcut20 nside64, ell=2)

Status: directional measurement of the operator-residue quadrupole at ell=2. Tests the *axial* feature of the gestural conjecture under a self-similarity reading (physical and epistemic manifolds should share preferred-axis structure). Does not commit the conjecture to Kerr or any specific physical realization.

Input: `data\derived\planck_operator_residue\planck_lowell_alm_fallback_nside64_galcut20.csv`

## Operator quadrupole axes (galactic l, b in degrees)

Each operator's own ell=2 sky pattern. Principal axis = eigenvector of largest |eigenvalue| of the quadrupole tensor Q.

| operator | l (deg) | b (deg) | anisotropy |
| --- | ---: | ---: | ---: |
| `Commander` | 68.0 | 59.5 | 0.323 |
| `NILC` | 69.2 | 57.1 | 0.302 |
| `SEVEM` | 66.9 | 57.8 | 0.316 |
| `SMICA` | 69.7 | 58.1 | 0.315 |

Operator-axis pairwise dispersion (degrees): median = 1.6, mean = 1.7, max = 2.5.

## Pair residual quadrupole axes (galactic l, b in degrees)

Each pair's `Δa_lm = a_lm^i - a_lm^j` ell=2 quadrupole. Principal axis as above.

| pair | l (deg) | b (deg) | anisotropy | residual power |
| --- | ---: | ---: | ---: | ---: |
| `Commander-NILC` | 246.7 | 56.5 | 0.400 | 3.1079e-12 |
| `Commander-SEVEM` | 164.8 | 84.6 | 0.406 | 1.5652e-12 |
| `Commander-SMICA` | 99.2 | 31.2 | 0.445 | 1.0874e-12 |
| `NILC-SEVEM` | 98.4 | 44.4 | 0.390 | 2.9904e-12 |
| `NILC-SMICA` | 232.2 | 54.4 | 0.294 | 8.3419e-13 |
| `SEVEM-SMICA` | 106.6 | 53.9 | 0.371 | 2.1784e-12 |

Pair-residual axis pairwise dispersion (degrees): median = 43.6, mean = 47.1, max = 88.1.

Reference: for axes uniformly distributed on the sphere modulo sign, the expected median pairwise separation is ~57°. Substantially below that suggests clustering; substantially above is unusual.

## Self-similarity check: operator vs residual axes

Angular separation (degrees) between each operator's quadrupole axis (physical: that operator's view of the sky) and each pair's residual axis (epistemic: the direction in which two operators systematically differ).

| operator \ pair | `Commander-NILC` | `Commander-SEVEM` | `Commander-SMICA` | `NILC-SEVEM` | `NILC-SMICA` | `SEVEM-SMICA` |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `Commander` | 64.0 | 31.6 | 35.2 | 23.7 | 65.4 | 21.6 |
| `NILC` | 66.4 | 33.8 | 33.2 | 22.1 | 67.6 | 21.1 |
| `SEVEM` | 65.8 | 33.4 | 34.6 | 23.5 | 67.2 | 22.3 |
| `SMICA` | 65.4 | 32.8 | 33.6 | 22.3 | 66.6 | 20.7 |

Reading: small angles indicate the epistemic preferred axis aligns with the physical preferred axis. Large angles indicate the residual axis points elsewhere than the sky's intrinsic quadrupole axis.

## Alignment with published low-ell anomaly directions

Operator axes:

| operator | axis-of-evil (LM2005) | quad-oct align (S2004) | cold spot | CMB dipole |
| --- | ---: | ---: | ---: | ---: |
| `Commander` | 60.1 | 55.5 | 19.9 | 71.7 |
| `NILC` | 62.6 | 57.9 | 21.0 | 74.2 |
| `SEVEM` | 61.8 | 57.2 | 19.6 | 73.3 |
| `SMICA` | 61.6 | 56.9 | 21.0 | 73.3 |

Pair-residual axes:

| pair | axis-of-evil (LM2005) | quad-oct align (S2004) | cold spot | CMB dipole |
| --- | ---: | ---: | ---: | ---: |
| `Commander-NILC` | 7.8 | 8.7 | 62.7 | 13.5 |
| `Commander-SEVEM` | 30.9 | 25.1 | 37.0 | 43.1 |
| `Commander-SMICA` | 87.4 | 81.1 | 53.2 | 80.4 |
| `NILC-SEVEM` | 74.5 | 68.3 | 43.1 | 86.7 |
| `NILC-SMICA` | 15.9 | 13.8 | 67.2 | 20.7 |
| `SEVEM-SMICA` | 64.1 | 57.8 | 41.2 | 76.3 |

## Interpretation discipline

What this measures: whether the operator-residue quadrupole has a coherent preferred direction across pairs, and whether that direction sits anywhere near published low-ell anomaly directions. Physical-vs-epistemic alignment is a self-similarity check.

What this does *not* measure: cosmological isotropy. With one realization of one sky and 5 modes at ell=2, cosmic variance dominates. A coherent residual axis in this run cannot be hypothesis-tested without simulations of cosmic-variance-bounded null. Alignment with published anomaly directions is a coincidence check, not derivation. The axis-of-evil literature is itself contested.

## Allowed claims

1. The operator-residue at ell=2 has a coherent (or non-coherent) principal axis across the six operator pairs, with median pairwise dispersion of X°.
2. The pair-residual axes [do/do not] cluster within Δθ° of the operators' own quadrupole axes (physical-vs-epistemic alignment readout).
3. The pair-residual axes [do/do not] sit within Δθ° of the published axis-of-evil direction.
4. The pattern is [robust/sensitive] to the galactic-plane mask (compare unmasked vs galcut20 runs).

## Forbidden claims

1. AOC is confirmed by a coherent residual axis.
2. LambdaCDM is refuted by alignment with the axis of evil.
3. Self-similarity between physical and epistemic manifolds is demonstrated by axis alignment in one realization.
4. The result implies rotating-interior cosmology, Kerr-cousin geometry, or any specific bounded-observer realization.

## Phase tag

Near-cousin-phase test of an axial feature of the gestural conjecture. The result is data; interpretation requires sim-level controls and theory-derived predictions of magnitude and direction.
