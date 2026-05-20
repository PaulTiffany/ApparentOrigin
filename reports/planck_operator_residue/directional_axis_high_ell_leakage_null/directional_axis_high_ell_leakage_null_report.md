# Directional Axis High-Ell Leakage Null

Status: mask-geometry null with additional Gaussian multipoles above ell=3.

## Question

Does high-ell leakage through the synthetic galactic cut change the
quadrupole-octupole alignment contract relative to the low-ell-only
masked-sky null?

## Setup

- Seeds: 1000
- Mask: |b| > 20 deg (`f_sky=0.6580`)
- Prior: C_ell proportional to 1/[ell(ell+1)] for 2<=ell<=30
- High-ell scale multiplier: 1
- Extraction: direct pseudo-alms at ell=2 and ell=3

## Tail Fractions

| metric | observed threshold | null median | 5-95% null | tail |
| --- | ---: | ---: | ---: | ---: |
| `unmasked_qo_angle_deg` | 11.9 | 59.96 | 17.82-86.76 | 0.02 |
| `masked_qo_angle_deg` | 29.5 | 56.59 | 18.29-86.2 | 0.854 |
| `mask_delta_qo_deg` | 17.6 | -1.891 | -40.23-37.63 | 0.165 |

Axis shifts caused by the mask:

| metric | null median | 5-95% null |
| --- | ---: | ---: |
| `ell2_axis_shift_deg` | 19.57 | 4.811-68.77 |
| `ell3_axis_shift_deg` | 15.04 | 2.472-74.04 |

Joint event:

```text
unmasked Q-O <= 11.9 deg
and mask delta >= 17.6 deg
fraction = 0.012 (12 / 1000)
```

## Contract Reading

The observed mask-state Q-O delta tail is 0.165.
This is a feasibility-contract check: if high-ell leakage makes the
out-of-contract band large, then the next contract must instrument
leakage before interpreting low-ell recomposition.

This also guards the pivot-regime interpretation from becoming numerology.
The low-ell-only masked null produced an ~11% out-of-contract band; after
extending the feasible contract to include high-ell leakage, the band moves to
16.5%. The number is contract-dependent. The invariant claim is not "11%";
it is that out-of-contract residue marks where the observer must recompose
the active contract before interpreting the statistic.

Layer attribution in feasibility-band SRMF: the current residue is primarily
Instrumentation / TTIE, not Operation / TTDC. The operation (`m=ell` axis
maximization) is fixed; the instrumented surface changes when the mask and
leakage model change. A later four-pipeline run would move the question into
Composition / TTCS: whether Commander, NILC, SEVEM, and SMICA compose
coherently after the same mask and leakage controls.

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
