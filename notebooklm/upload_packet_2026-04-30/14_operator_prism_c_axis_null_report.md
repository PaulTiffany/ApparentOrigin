# C_axis Null Baseline (Sprint F2)

Status: Sprint F2 simulation-level null baseline for the operator-prism
C_axis coordinate.

Phase: instantiation-class baseline. Not the official-mask null. The
proper test of the live values requires another GitHub Actions `healpy`
run with the official Planck common mask in the loop -- see Section 7.

## Coordinate

```text
C_axis = ( D_res - D_op ) / D_iso
D_iso  = 57 deg (matches operator_prism gate; see d_iso_calibration_report.md)
```

D_op is the median pairwise axial angle among the four operator axes
(n=4 -> 6 pairs). D_res is the median pairwise axial angle among the
six pair-residue axes (n=6 -> 15 pairs).

## Live Observed (GitHub Actions, 2026-04-30)

- C_axis(ell=3, official-mask-base)    = 0.281497
- C_axis(ell=3, official-mask-dilate1) = 0.425643

## Null Conditions

Each condition draws an isotropic LambdaCDM low-ell sky, synthesizes
to a map, optionally masks with synthetic galcut20, extracts pseudo-alm
coefficients as the shared base, then four surrogate operators receive
independent operator noise (noise_scale = 1.0 -> sigma = 0.5 * RMS).
Operator axes and pair-residue axes are computed by the same
m=ell-maximizing extractor used in the gate.

## Results

| condition | n_valid | mean C_axis | median C_axis | std | p05 | p95 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `ell3_unmasked` | 500 | +0.4739 | +0.5323 | 0.3313 | -0.1317 | +0.9312 |
| `ell3_galcut20` | 500 | +0.5010 | +0.5497 | 0.3298 | -0.1685 | +0.9464 |

## Percentile Of Live Observed Values

Suggestive only -- the null does not use the official Planck mask.

| condition | live label | live C_axis | percentile in null |
| --- | --- | ---: | ---: |
| `ell3_unmasked` | `official-mask-base` | +0.2815 | 26.40 |
| `ell3_unmasked` | `official-mask-dilate1` | +0.4256 | 39.40 |
| `ell3_galcut20` | `official-mask-base` | +0.2815 | 22.20 |
| `ell3_galcut20` | `official-mask-dilate1` | +0.4256 | 34.80 |

Reading: a percentile near 100 means the live observed value is
atypical for the null condition above; a percentile near 50 means
it sits in the bulk of the null distribution.

## What This Null Reveals About The Contract

The methodologically substantive finding from this run is that **the
contract's sign condition `C_axis > 0` is trivially satisfied under
the surrogate cartoon**. Under both null conditions about 90% of
realizations produce `C_axis > 0`, with median around 0.5.

Why. In a shared-sky-plus-small-noise model, pair-residues reduce to
`alms_i - alms_j = noise_i - noise_j`, which is pure noise. Their
m=ell-maximizing axes are nearly uniform on `S^2`, giving `D_res`
near 60 deg (the n>=2 isotropic axial median). Operator axes track
the shared sky with small dispersion, giving `D_op` small. So
`D_res - D_op` is broadly positive by construction, not by Kerr-side
prediction.

Reading the live values against this. The live observed values
(0.281 base, 0.426 dilate1) sit at the 22 to 39th percentile of the
surrogate null distribution -- *below* the surrogate bulk. That is
informative in the opposite direction: the real Planck pair-residues
are *more aligned* than the surrogate cartoon predicts. The four real
Planck pipelines' pair-residues do not look like uniform-random axes;
they have shared structure that the cartoon omits.

What follows. The contract's sign-only verdict reads
`contract_success_if_inputs_were_predeclared` correctly, but a
sign-only condition under a shared-sky null does not discriminate
Kerr-side axial feasibility from any other "operators agree more than
their pair-residues do" prior. The contract was deliberately weak;
this null clarifies just how weak.

## Section 7 -- Frozen Open Question (Episode 4)

The proper null for the live operator-prism contract requires an
isotropic LambdaCDM low-ell sky pushed through the **official Planck
common mask** with the same `healpy.map2alm` extractor used in the
live run, and with a noise model calibrated to the actual
component-separation residual covariances rather than the
shared-sky-plus-iid-noise cartoon used here. That requires another
GitHub Actions run, since the local Windows environment does not have
`healpy` available. This is the frozen open question that closes the
Episode 4 packet.

What this script does establish:

1. The contract's sign condition is trivially satisfied (90% of
   realizations) under the surrogate Pipeline-Independence-Postulate
   cartoon. The live PASS is therefore a weak ordinal claim, not a
   Kerr-specific empirical anchor.
2. The live values sit *below* the surrogate null bulk. The real
   Planck pair-residues are more aligned than uniform-random would
   predict.
3. The synthetic galcut20 condition is similar to unmasked under this
   surrogate (median C_axis 0.55 vs 0.53). Mask geometry alone in
   this cartoon does not flip the picture; whether the official mask
   would flip it is the frozen open question.

## Allowed Claims

1. This script computes a local-machine surrogate C_axis null without
   official-mask geometry.
2. The percentiles reported are suggestive, not the proper test of the
   live operator-prism result.
3. The proper null is the next required artifact (GitHub Actions run).

## Forbidden Claims

1. This null confirms or refutes the operator-prism contract.
2. The synthetic galcut20 reproduces official Planck mask geometry.
3. A high percentile here is evidence for AOC.
