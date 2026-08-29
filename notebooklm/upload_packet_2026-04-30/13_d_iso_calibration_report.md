# D_iso Calibration

Status: Sprint F1 first-principles calibration of the isotropic axial
dispersion reference used by the lambda_K Planck operator-prism contract.

Phase: methodology / first-principles derivation. Not a measurement on
Planck data.

## Question

The operator-prism contract uses

```text
C_axis = (D_res - D_op) / D_iso
```

with `D_iso = 57 deg` hardcoded in
`empirical/planck_operator_residue/evaluate_operator_prism_contract.py`.
The contract's sign-only prediction is invariant to D_iso, but the
magnitude reading depends on it. This script computes D_iso from first
principles for n=4 axes (Commander, NILC, SEVEM, SMICA).

## Theory

For two uniform unit vectors u, v on S^2, |u . v| is uniform on [0, 1].
The axial angle theta = arccos(|u . v|) has CDF

```tex
P(\theta \le x) = 1 - \cos x, \quad x \in [0, \pi/2].
```

Median: `cos(x) = 1/2`, so `x = pi/3 = 60 deg`.

For n=4 axes the gate uses the median over the 6 pairwise angles per
realization. The median-of-6 distribution is shifted slightly from 60
deg because the six pairwise angles share the underlying four vectors
(non-independence) and the median is order-statistics-asymmetric.

## Result

n=2 (single pair) Monte Carlo (n_realizations=100000, seed=20260432):

- median of pairwise axial angle: **60.062 deg**
- theoretical exact: 60.000 deg
- mean: 57.425 deg, std: 21.522 deg

n=4 (operator-prism setup) Monte Carlo (n_realizations=100000, seed=20260434):

- median of per-realization median pairwise axial angle: **60.029 deg**
- mean: 59.507 deg, std: 11.226 deg
- p05/p25/p75/p95: 39.51 / 52.60 / 67.62 / 76.66 deg

## Audit Versus Hardcoded 57 Degrees

The Sprint F1 calibration places the n=4 isotropic reference at
**60.03 deg** (per-realization spread 1-sigma ~11.23 deg; with 100,000 draws the standard error of the median is ~0.04 deg).

The hardcoded 57 deg in `evaluate_operator_prism_contract.py` is within
the bulk of the per-realization distribution (between the p25 and p75
quantiles, 52.60 and 67.62 deg) but is ~3 deg below the median, well
outside Monte Carlo noise. It is best read as a slightly informal
estimate that landed in the right neighborhood rather than a derivation
of the exact n=4 axial median.

Why the live verdict is unchanged. The C_axis sign is invariant under
any positive choice of D_iso, and the operator-prism contract was
predeclared as a sign-only condition. Under the corrected reference
the live magnitudes become

```text
C_axis(base, D_iso=60)    = (D_res - D_op) / 60
                          = (20.133 - 4.088) / 60
                          = 0.267417
C_axis(dilate1, D_iso=60) = (25.625 - 1.363) / 60
                          = 0.404367
```

vs the as-reported 0.281497 and 0.425643 under D_iso = 57. Both remain
positive; the predeclared sign condition is unchanged.

Discipline note. The hardcoded D_iso = 57 deg is **not** retroactively
modified in the gate code, because the contract was frozen at that
value before the live run. Moving the goalpost after seeing the data
is the failure mode the predeclaration discipline exists to prevent.
Future operator-prism contracts should cite this calibration and use
the empirical n=4 reference (60 deg, or report both).

## Allowed Claims

1. The n=2 axial-angle median matches the exact theoretical value of 60 deg.
2. The n=4 median-of-medians reference is computable from first principles
   and does not depend on any Planck dataset.
3. The hardcoded D_iso = 57 deg sits within the bulk of the n=4 per
   realization distribution but is ~3 deg below the empirical median.
4. The live operator-prism sign verdict is invariant to this correction.
5. The hardcoded value is retained because it was predeclared; future
   contracts should cite this calibration and use 60 deg.

## Forbidden Claims

1. D_iso is a free parameter that may be tuned to flip a verdict.
2. This script measures anything on Planck data.
3. A different D_iso choice would change the operator-prism sign condition.
