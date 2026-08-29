# Directional Axis Masked-Sky Null

Status: first mask-geometry simulation for the corrected ell=2/ell=3
m=ell-maximizing directional statistic.

## Question

Under isotropic low-ell skies, can the synthetic galactic cut alone
commonly weaken quadrupole-octupole alignment by the observed amount?

## Setup

- Seeds: 20
- Mask: |b| > 20 deg (`f_sky=0.6580`)
- Low-ell prior: C_ell proportional to 1/[ell(ell+1)] for ell=2,3
- Extraction: direct pseudo-alms with mean subtraction on the retained sky

## Tail Fractions

| metric | observed threshold | null median | 5-95% null | tail |
| --- | ---: | ---: | ---: | ---: |
| `unmasked_qo_angle_deg` | 11.9 | 65.76 | 26.43-83.91 | 0 |
| `masked_qo_angle_deg` | 29.5 | 62.85 | 23.46-81.55 | 0.85 |
| `mask_delta_qo_deg` | 17.6 | -6.749 | -23.73-26.86 | 0.1 |

Axis shifts caused by the mask:

| metric | null median | 5-95% null |
| --- | ---: | ---: |
| `ell2_axis_shift_deg` | 16.3 | 0-55.35 |
| `ell3_axis_shift_deg` | 11.64 | 4.345-58.51 |

Joint event:

```text
unmasked Q-O <= 11.9 deg
and mask delta >= 17.6 deg
fraction = 0 (0 / 20)
```

## Readout

The observed mask-state Q-O delta is compared against direct masked-sky draws; tail = 0.1.
This says how often mask geometry alone produces at least the observed
weakening under this restricted low-ell null.

## Allowed Claims

1. This null tests mask geometry directly for ell=2 and ell=3.
2. The result says whether the synthetic galactic cut commonly produces
   the observed Q-O weakening in isotropic low-ell skies.
3. The result is a control on the directional statistic, not an AOC test.

## Forbidden Claims

1. This proves or refutes AOC.
2. This refutes LambdaCDM.
3. This replaces official Planck masked-sky likelihood analysis.
4. This includes real component separation or foreground physics.

## Limitations

- No Planck component-separation operators are simulated.
- No beam, noise, high-ell leakage, inpainting, or official Planck mask is simulated.
- Only ell=2 and ell=3 are generated, so leakage from higher multipoles is absent.
- The extraction uses direct pseudo-alms with mean subtraction, matching the fallback extractor's convention.

## Next Control

Add high-ell Gaussian sky content and an official Planck common mask,
then rerun the same pseudo-alm extraction to test leakage and mask
specificity.
