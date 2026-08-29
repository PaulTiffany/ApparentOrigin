# Planck P3 Official-Mask Specificity Contract

Status: frozen pre-run contract for P3.

Phase: empirical instrumentation control. This is not AOC evidence and not a
Planck likelihood.

## Exact Mask Product

Official mask:

```text
data/raw/planck_operator_residue/masks/COM_Mask_CMB-common-Mask-Int_2048_R3.00.fits
```

Source:

```text
https://irsa.ipac.caltech.edu/data/Planck/release_3/ancillary-data/masks/COM_Mask_CMB-common-Mask-Int_2048_R3.00.fits
```

Product identity: Planck 2018 Component Separation Common mask in Intensity,
field `TMASK`, `NSIDE=2048`, `ORDERING=NESTED`.

## Frozen Morphology Family

The mask is downgraded conservatively to `nside=64`: an output pixel is
retained only if all contributing `nside=2048` pixels are retained.

Run the following morphology family on that downgraded mask:

```text
erode2, erode1, base, dilate1, dilate2
```

where one step means one HEALPix-neighbor ring at `nside=64`.

## Prediction

P3 asks whether the synthetic-latitude cliff was a hand-made-mask artifact.

Prediction:

1. If the cliff is purely a synthetic-latitude artifact, the official-mask
   morphology family should not show a comparably sharp adjacent Q-O jump.
2. If the cliff is instrumentation-bound recomposition, an adjacent cliff may
   reappear under official-mask morphology, but not necessarily at the same
   sky fraction or latitude-equivalent threshold.

Decision read:

```text
max adjacent Q-O jump >= 30 deg  -> official-mask morphology preserves a cliff-like recomposition
max adjacent Q-O jump < 30 deg   -> no comparable cliff under this official-mask morphology
```

The `30 deg` threshold is deliberately weaker than the synthetic `51.51 deg`
cliff because official morphology is not latitude-ordered and the family has
only five points in this first sprint control.

## Allowed Claims

1. This tests whether the threshold-cliff shape survives replacing synthetic
   latitude cuts with official Planck common-mask morphology.
2. The result can prioritize or deprioritize deeper official-mask and
   extractor-robustness work.

## Forbidden Claims

1. This proves or refutes AOC.
2. This is a Planck likelihood.
3. This tests all official mask possibilities.
4. Failure to reproduce a cliff under this five-point family falsifies the
   broader framework.

## Post-Run Audit

Status as of 2026-04-28: P3 first official-mask morphology sweep returned
`official_morphology_preserves_cliff_like_recomposition`.

Artifact:

```text
empirical/planck_operator_residue/directional_axis_official_mask_morphology.py
reports/planck_operator_residue/directional_axis_official_mask_morphology/
```

Result:

| mask | f_sky | median Q-O | ell=2 notes | ell=3 notes |
| --- | ---: | ---: | --- | --- |
| erode2 | 0.1144 | 82.8 | G | B |
| erode1 | 0.3358 | 38.1 | G | A |
| base | 0.6670 | 27.7 | G | A |
| dilate1 | 0.8084 | 18.6 | G | AG |
| dilate2 | 0.8386 | 13.3 | G | G |

Largest adjacent jump: `44.7 deg` at `erode2 -> erode1`, above the frozen
`30 deg` decision threshold.

Interpretation:

The first official-mask morphology control preserves a cliff-like
recomposition shape. This does not prove AOC and does not replace a likelihood
or null over official-mask morphologies. It does say the cliff shape is not
obviously unique to hand-made latitude cuts.

Residual risk:

The largest jump involves a very severe erosion (`f_sky=0.1144`), so the next
official-mask control should test a less extreme morphology grid and an
isotropic null on the same official-mask family.
