# Planck Operator-Residue Directional Analysis (unmasked nside64, ell=2)

Status: directional measurement of the operator-residue quadrupole at ell=2. Tests the *axial* feature of the gestural conjecture under a self-similarity reading (physical and epistemic manifolds should share preferred-axis structure). Does not commit the conjecture to Kerr or any specific physical realization.

Input: `data\derived\planck_operator_residue\planck_lowell_alm_fallback_nside64.csv`

## Operator quadrupole axes (galactic l, b in degrees)

Each operator's own ell=2 sky pattern. Principal axis = eigenvector of largest |eigenvalue| of the quadrupole tensor Q.

| operator | l (deg) | b (deg) | anisotropy |
| --- | ---: | ---: | ---: |
| `Commander` | 332.3 | 2.7 | 0.432 |
| `NILC` | 334.9 | 2.5 | 0.498 |
| `SEVEM` | 55.0 | 23.7 | 0.411 |
| `SMICA` | 334.0 | 2.8 | 0.457 |

Operator-axis pairwise dispersion (degrees): median = 41.3, mean = 41.4, max = 82.3.

## Pair residual quadrupole axes (galactic l, b in degrees)

Each pair's `Δa_lm = a_lm^i - a_lm^j` ell=2 quadrupole. Principal axis as above.

| pair | l (deg) | b (deg) | anisotropy | residual power |
| --- | ---: | ---: | ---: | ---: |
| `Commander-NILC` | 83.7 | 8.1 | 0.493 | 5.5202e-11 |
| `Commander-SEVEM` | 2.2 | 1.2 | 0.486 | 2.7070e-10 |
| `Commander-SMICA` | 80.2 | 8.3 | 0.381 | 1.9465e-11 |
| `NILC-SEVEM` | 179.9 | 0.4 | 0.312 | 2.1479e-10 |
| `NILC-SMICA` | 221.3 | 78.8 | 0.369 | 1.0913e-11 |
| `SEVEM-SMICA` | 359.1 | 0.9 | 0.363 | 2.4973e-10 |

Pair-residual axis pairwise dispersion (degrees): median = 81.2, mean = 61.7, max = 89.8.

Reference: for axes uniformly distributed on the sphere modulo sign, the expected median pairwise separation is ~57°. Substantially below that suggests clustering; substantially above is unusual.

## Self-similarity check: operator vs residual axes

Angular separation (degrees) between each operator's quadrupole axis (physical: that operator's view of the sky) and each pair's residual axis (epistemic: the direction in which two operators systematically differ).

| operator \ pair | `Commander-NILC` | `Commander-SEVEM` | `Commander-SMICA` | `NILC-SEVEM` | `NILC-SMICA` | `SEVEM-SMICA` |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `Commander` | 69.2 | 29.9 | 72.7 | 27.8 | 88.7 | 26.9 |
| `NILC` | 71.7 | 27.3 | 75.3 | 25.2 | 88.0 | 24.3 |
| `SEVEM` | 31.6 | 55.8 | 28.6 | 58.6 | 77.2 | 58.7 |
| `SMICA` | 70.9 | 28.2 | 74.4 | 26.1 | 88.4 | 25.2 |

Reading: small angles indicate the epistemic preferred axis aligns with the physical preferred axis. Large angles indicate the residual axis points elsewhere than the sky's intrinsic quadrupole axis.

## Alignment with published low-ell anomaly directions

Operator axes:

| operator | axis-of-evil (LM2005) | quad-oct align (S2004) | cold spot | CMB dipole |
| --- | ---: | ---: | ---: | ---: |
| `Commander` | 78.9 | 84.3 | 70.8 | 73.6 |
| `NILC` | 80.4 | 85.6 | 69.7 | 75.5 |
| `SEVEM` | 86.2 | 89.5 | 37.9 | 76.3 |
| `SMICA` | 79.6 | 84.9 | 69.8 | 74.6 |

Pair-residual axes:

| pair | axis-of-evil (LM2005) | quad-oct align (S2004) | cold spot | CMB dipole |
| --- | ---: | ---: | ---: | ---: |
| `Commander-NILC` | 68.2 | 73.8 | 64.1 | 56.1 |
| `Commander-SEVEM` | 85.0 | 81.9 | 60.0 | 85.4 |
| `Commander-SMICA` | 68.3 | 73.7 | 62.2 | 56.4 |
| `NILC-SEVEM` | 84.7 | 81.3 | 62.3 | 85.7 |
| `NILC-SMICA` | 22.3 | 16.1 | 44.0 | 34.5 |
| `SEVEM-SMICA` | 86.2 | 82.8 | 61.3 | 87.2 |

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
