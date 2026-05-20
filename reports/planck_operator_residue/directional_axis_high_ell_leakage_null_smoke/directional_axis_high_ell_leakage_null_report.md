# Directional Axis High-Ell Leakage Null

Status: mask-geometry null with additional Gaussian multipoles above ell=3.

## Question

Does high-ell leakage through the synthetic galactic cut change the
quadrupole-octupole alignment contract relative to the low-ell-only
masked-sky null?

## Setup

- Seeds: 20
- Mask: |b| > 20 deg (`f_sky=0.6580`)
- Prior: C_ell proportional to 1/[ell(ell+1)] for 2<=ell<=30
- High-ell scale multiplier: 1
- Extraction: direct pseudo-alms at ell=2 and ell=3

## Tail Fractions

| metric | observed threshold | null median | 5-95% null | tail |
| --- | ---: | ---: | ---: | ---: |
| `unmasked_qo_angle_deg` | 11.9 | 63.74 | 23.39-79.91 | 0 |
| `masked_qo_angle_deg` | 29.5 | 51.61 | 20.67-86.32 | 0.85 |
| `mask_delta_qo_deg` | 17.6 | -7.833 | -35.95-29.53 | 0.1 |

Axis shifts caused by the mask:

| metric | null median | 5-95% null |
| --- | ---: | ---: |
| `ell2_axis_shift_deg` | 17.46 | 2.349-73.17 |
| `ell3_axis_shift_deg` | 17.21 | 5.415-68.52 |

Joint event:

```text
unmasked Q-O <= 11.9 deg
and mask delta >= 17.6 deg
fraction = 0 (0 / 20)
```

## Contract Reading

The observed mask-state Q-O delta tail is 0.1.
This is a feasibility-contract check: if high-ell leakage makes the
out-of-contract band large, then the next contract must instrument
leakage before interpreting low-ell recomposition.

## Allowed Claims

1. This null tests whether high-ell leakage through the synthetic mask
   changes the directional-statistic tails.
2. The result is a control on feasibility of the low-ell mask contract.
3. It does not test AOC directly.

## Forbidden Claims

1. This proves or refutes AOC.
2. This refutes LambdaCDM.
3. This replaces official Planck masked-sky likelihood analysis.
4. The simple high-ell power law is a precision CMB simulation.

## Limitations

- No Planck component-separation operators are simulated.
- No beam, detector noise, foregrounds, inpainting, or official Planck mask is simulated.
- High-ell content uses a simple flat-Sachs-Wolfe-like power law, not a precision LambdaCDM Cl.
- The extraction uses direct pseudo-alms with mean subtraction, matching the fallback extractor's convention.

## Next Control

Swap the simple power law for a fiducial LambdaCDM Cl and, if available,
replace the synthetic galactic cut with an official Planck common mask.
