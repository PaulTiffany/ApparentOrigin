# Directional Axis Official-Mask Morphology

Status: P3 official Planck common-mask morphology sweep.

## Setup

- Mask: `C:\src\observer_cosmology\data\raw\planck_operator_residue\masks\COM_Mask_CMB-common-Mask-Int_2048_R3.00.fits`
- nside_out: 64
- Family: erode2, erode1, base, dilate1, dilate2
- Extraction: fallback direct pseudo-alms at ell=2 and ell=3

## Metrics

| mask | f_sky | median Q-O | ell=2 dispersion | ell=3 dispersion | ell=2 notes | ell=3 notes |
| --- | ---: | ---: | ---: | ---: | --- | --- |
| erode2 | 0.1144 | 82.8 | 3.6 | 6.0 | G | B |
| erode1 | 0.3358 | 38.1 | 1.2 | 5.6 | G | A |
| base | 0.6670 | 27.7 | 2.5 | 4.5 | G | A |
| dilate1 | 0.8084 | 18.6 | 3.8 | 1.4 | G | AG |
| dilate2 | 0.8386 | 13.3 | 3.7 | 2.6 | G | G |

## Adjacent Jumps

| step | Q-O jump |
| --- | ---: |
| `erode2->erode1` | 44.7 |
| `erode1->base` | 10.4 |
| `base->dilate1` | 9.1 |
| `dilate1->dilate2` | 5.3 |

## P3 Decision

Max adjacent jump: `44.7 deg`.
Decision threshold: `30.0 deg`.
Result: `official_morphology_preserves_cliff_like_recomposition`.

Allowed claim: this tests whether the synthetic-latitude cliff shape
survives a first official-mask morphology sweep.

Forbidden claim: this is not AOC evidence and not a Planck likelihood.
