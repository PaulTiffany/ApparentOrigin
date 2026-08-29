# Planck Operator-Residue First Contact

Status: real Planck data, fallback extractor, first-contact result only.

Date: 2026-04-28.

## Input

Downloaded four Planck PR3 full-mission component-separated CMB maps from the
IRSA Planck release mirror:

```text
COM_CMB_IQU-commander_2048_R3.00_full.fits
COM_CMB_IQU-nilc_2048_R3.00_full.fits
COM_CMB_IQU-sevem_2048_R3.00_full.fits
COM_CMB_IQU-smica_2048_R3.00_full.fits
```

Local directory:

```text
data/raw/planck_operator_residue/maps/
```

Sizes:

| map | bytes |
| --- | ---: |
| Commander | 1,610,660,160 |
| NILC | 1,610,660,160 |
| SEVEM | 2,013,278,400 |
| SMICA | 2,013,312,960 |

## Method

`healpy` could not be installed cleanly on the local Windows Python stack, so
this first contact used:

```text
empirical/planck_operator_residue/extract_planck_lowell_fallback.py
```

The fallback extractor:

1. reads each FITS map with `astropy`,
2. downgrades `I_STOKES` from `nside=2048` to a small HEALPix grid using
   `astropy-healpix`,
3. computes `2 <= ell <= 30` coefficients by direct quadrature,
4. exports:

```text
operator,ell,m,alm_real,alm_imag
```

Two first-contact resolutions were run:

```text
nside_out = 32
nside_out = 64
```

The predeclared analyzer was then run:

```text
empirical/planck_operator_residue/analyze_lowell_operator_residue.py
```

## Headline Results

| run | median pairwise coefficient distance | Commander parity | NILC parity | SEVEM parity | SMICA parity |
| --- | ---: | ---: | ---: | ---: | ---: |
| fallback nside32 | 0.342372 | 1.424730 | 1.469643 | 1.406000 | 1.455541 |
| fallback nside64 | 0.337761 | 1.420728 | 1.467259 | 1.403465 | 1.453378 |

The nside32 and nside64 runs agree closely. That is a useful sanity check for
the fallback extractor.

## Pairwise Operator Distances

For the `nside64` run:

| pair | median | mean | min | max |
| --- | ---: | ---: | ---: | ---: |
| Commander-NILC | 0.273684 | 0.274773 | 0.058750 | 0.403586 |
| Commander-SEVEM | 0.460631 | 0.435448 | 0.248629 | 0.586833 |
| Commander-SMICA | 0.251256 | 0.242084 | 0.063026 | 0.382052 |
| NILC-SEVEM | 0.498159 | 0.472316 | 0.277638 | 0.636481 |
| NILC-SMICA | 0.092011 | 0.087035 | 0.016541 | 0.130642 |
| SEVEM-SMICA | 0.482440 | 0.467335 | 0.286257 | 0.613046 |

The strongest first-contact pattern is that NILC and SMICA are very close to
each other under this metric, while SEVEM is farther from the other operators.
That is an operator-residue result, not an AOC result.

## Multipole Stability

Lowest median operator distances:

| ell | median pairwise distance |
| ---: | ---: |
| 3 | 0.155827 |
| 5 | 0.189490 |
| 4 | 0.219584 |
| 7 | 0.227503 |
| 11 | 0.248560 |

Highest median operator distances:

| ell | median pairwise distance |
| ---: | ---: |
| 25 | 0.431287 |
| 23 | 0.442251 |
| 22 | 0.458790 |
| 27 | 0.471967 |
| 21 | 0.486774 |

The lowest few multipoles are more operator-stable than much of the upper part
of the `ell <= 30` band under this metric.

## Interpretation

Plain English:

> The largest-scale Planck coefficients are not random-looking across
> reconstruction operators. The low multipoles show meaningful cross-operator
> stability, especially for NILC and SMICA. SEVEM differs more strongly.

AOC-safe interpretation:

> This is exactly the kind of object AOC should study: same sky, multiple
> reconstruction operators, measurable residue. It is a first operator-residue
> contact, not evidence for a false bottom.

Standard-cosmology interpretation:

> These differences and similarities may reflect known component-separation
> behavior, masks, foreground residuals, smoothing, inpainting, or ordinary
> low-ell cosmic variance. No physical interpretation is licensed yet.

## Phase-Randomized Null Control

Added first control:

```text
empirical/planck_operator_residue/phase_null_operator_residue.py
reports/planck_operator_residue/phase_null_nside64/
```

Null definition:

> Preserve each operator's `|a_lm|` amplitudes and independently randomize
> phases for `m > 0`; randomly sign-flip `m = 0`.

This destroys cross-operator phase alignment while preserving each operator's
low-ell coefficient amplitudes.

Headline:

| metric | value |
| --- | ---: |
| observed median pairwise distance | 0.337761 |
| null median | 1.414070 |
| null q05 | 1.386992 |
| null q95 | 1.441485 |
| fraction null <= observed | 0 / 1000 |

Pair medians:

| pair | observed | null median |
| --- | ---: | ---: |
| Commander-NILC | 0.273684 | 1.412485 |
| Commander-SEVEM | 0.460631 | 1.413349 |
| Commander-SMICA | 0.251256 | 1.415351 |
| NILC-SEVEM | 0.498159 | 1.414337 |
| NILC-SMICA | 0.092011 | 1.412899 |
| SEVEM-SMICA | 0.482440 | 1.412648 |

Interpretation:

The observed cross-operator closeness is not explained by each operator's
low-ell power spectrum alone. The component maps share aligned low-ell
structure that is destroyed by phase randomization.

This is expected at some level because the operators are reconstructing the
same sky. The result becomes scientifically useful only after comparing the
size and localization of the residue against masks, simulations, and known
Planck low-ell analyses.

## Allowed Claim

> The repo now has real Planck component-separated maps downloaded locally and a
> first operator-residue measurement showing stable low-ell behavior across
> reconstruction operators under a fallback low-resolution extractor.

## Forbidden Claims

Do not claim:

1. Planck supports AOC.
2. The CMB proves a false bottom.
3. The low-ell pattern proves torque, white-hole leakage, or horizon geometry.
4. `LambdaCDM` is refuted.
5. The fallback extractor is equivalent to final `healpy` harmonic analysis.

## Mask-Aware Phase Null Control (2026-04-28)

Added a second null control that re-runs the phase-randomized null on
masked-pseudo-alms extracted with a synthetic galactic-plane cut at
`|b| > 20°` (`f_sky = 0.6615`).

```text
empirical/planck_operator_residue/extract_planck_lowell_fallback_masked.py
data/derived/planck_operator_residue/planck_lowell_alm_fallback_nside64_galcut20.csv
reports/planck_operator_residue/phase_null_nside64_galcut20/
```

Headline:

| metric | unmasked | galcut20 |
| --- | ---: | ---: |
| observed median pairwise distance | 0.337761 | 0.041244 |
| null median | 1.414070 | 1.414207 |
| null q05 | 1.386992 | 1.384254 |
| null q95 | 1.441485 | 1.444125 |
| fraction null <= observed | 0 / 1000 | 0 / 1000 |

Pairwise pattern: in the unmasked variant every pair *involving SEVEM* sits
at 0.46-0.50; once the galactic plane is cut, all six pairs collapse into
the same ~0.03-0.05 band. The unmasked SEVEM-vs-others gap is dominated by
galactic-plane disagreement.

Interpretation:

> The observed cross-operator alignment is *not* a galactic-plane artifact.
> Cutting the plane sharpens the alignment by an order of magnitude while
> the phase-randomized null distribution stays at ~1.414. The four operators
> agree on the cosmic sky and disagree on the foreground residue.

This is consistent with the AOC operator-residue framing but does not prove
it. The clean-sky alignment is also exactly what one would expect from four
pipelines reconstructing the same underlying CMB realization: a coefficient-
level phase null cannot separate "shared cosmic sky" from "operator-bound
apparatus signal". That separation requires a simulation-level null where
we control the input sky.

Full comparison:
`reports/planck_operator_residue/phase_null_nside64_galcut20/mask_aware_comparison.md`.

## Next Controls

1. Re-run with the official Planck PR3 common-Int confidence mask
   (`COM_Mask_CMB-common-Mask-Int_2048_R3.00.fits`, ESA PLA route confirmed
   reachable; the synthetic galcut20 mask is a proxy only).
2. Simulation-level null. Generate CMB-only realizations from a fiducial
   `LambdaCDM` `Cl`, propagate through pipeline-equivalent reconstruction
   operators, and ask whether the observed clean-sky operator-residue
   distance is small relative to the realization-to-realization spread of
   that distance under known cosmic input.
3. Cross-band split (`2 <= ell <= 10` and `11 <= ell <= 30`) to localize the
   alignment.
4. Add a published low-ell comparison if available.
5. Re-run with canonical `healpy.map2alm` in a Linux/conda environment.
