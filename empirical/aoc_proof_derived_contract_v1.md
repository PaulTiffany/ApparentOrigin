# AOC Proof-Derived Deformation Empirical Contract v1

Status: pre-registered as of 2026-04-26.

Purpose:

Define the next-generation AOC distance-modulus deformation, derived from
the apparatus-bound `K` program rather than from data exploration, so that
the specification-flexibility caveat in the v0 contract can be tightened.

This contract is committed in writing before any fit, scan, or power-test
result is generated under v1. No knob below may be silently re-chosen after
the run without an explicit amendment dated later than 2026-04-26.

## Shape Derivation

From `docs/apparatus_bound_k_program.md` §5, pipeline reconstruction noise
grows as:

```text
sigma_P(y) = sigma_0 * y^p,      p > 1
```

The relative reconstruction error therefore grows as:

```text
sigma_P(y) / y = sigma_0 * y^{p-1} = eta * (y / K)^{p-1}
```

where `K = (eta / sigma_0)^{1/(p-1)}` is the §3 apparatus-bound floor. The
v1 distance-modulus deformation tracks the same `(1 + z)^{p-1}` shape with a
single dimensional amplitude `lambda_K`:

```text
delta_mu_AOC(z; lambda_K, p) = lambda_K * (1 + z)^{p - 1}
```

A constant magnitude offset is marginalized for every model and cutoff
exactly as in v0. With the offset marginalized, the comparison is between
the deformation `(1 + z)^{p-1}` and its weighted mean across the subset, so
the constant at `z = 0` is absorbed into the calibration nuisance and the
fitted amplitude is invariant under affine recalibration.

The amplitude `lambda_K` is the only fitted parameter. The exponent `p` is a
property of the assumed pipeline noise law and is held fixed.

## Pre-Registered p Values

Primary:

```text
p_primary = 1.8
```

This matches the apparatus-bound K toy
`simulations/apparatus_bound_k/apparatus_k.py` and the two-pipeline run
`simulations/apparatus_bound_k/apparatus_k_two_pipeline.py`. It is not fit
from the Pantheon+ data.

Secondary (shape robustness):

```text
p_robust = 2.0
```

Both `p` values are committed at the time of contract draft. Additional `p`
values must not be silently scanned. If a future contract adds them, that
amendment must explicitly note that the new values were not in v1.

## Pre-Registered Cosmology Baseline

```text
H0 = 70 km/s/Mpc
Omega_m = 0.3
flat LambdaCDM, constant magnitude offset marginalized
```

## Pre-Registered Cutoffs

```text
z_cut_primary   = 1.0
z_cut_secondary = 0.75
```

The primary cutoff is fixed before the run so that the strongest exploratory
v0 region (`z_cut = 0.75 to 1.0`) is not silently re-scanned for the most
favorable v1 cutoff.

## Pre-Registered Inference

Grid:

```text
lambda_K in [-0.30, 0.30] step 0.01
```

Primary statistic:

```text
Delta BIC = (chi2(best lambda_K) - chi2(lambda_K = 0)) + log(n)
```

Interpretation thresholds (matching v0):

```text
Delta BIC < -10:           strong improvement
-10 <= Delta BIC < -2:     weak/moderate improvement
Delta BIC >= -2:           no meaningful support after parameter penalty
```

## Pre-Registered Power Test

Inject a known `lambda_K_inj` into a synthetic distance-modulus vector
constructed from the actual Pantheon+ redshifts and the actual Pantheon+
covariance, then run the v1 fit:

```text
lambda_K_inj in {0.0, -0.025, -0.050, -0.075, -0.100, -0.150, -0.200}
n_seeds = 200
seed_root = 20260426
```

Report, at each `(z_cut, p, lambda_K_inj)` cell:

1. median, p10, p90 of recovered `lambda_K`,
2. median, p10, p90 of `Delta BIC`,
3. fractions `frac(Delta BIC < 0)`, `frac(Delta BIC < -2)`,
   `frac(Delta BIC < -10)`.

## Pre-Registered Comparison to v0

Quote, side by side, the actual-data `Delta BIC` under v1 and v0 at the
primary cutoff, for the primary and secondary `p`. Compare the v1 power
curve to the v0 power curve at matched magnitude scale at `z = 1`.

## Allowed Claims

1. The proof-derived deformation can be evaluated on Pantheon+ data with
   the same machinery as v0.
2. Pre-registered recovery, null distribution, and detection power for the
   proof-derived shape can be computed and reported.
3. The Pantheon+ same-sample `Delta BIC` under v1 can be compared to v0 as
   a measurement of the exploratory result's sensitivity to deformation
   shape inside the apparatus-bound program.

## Forbidden Claims

1. The v1 deformation is the final AOC distance law.
2. v1 outperforming v0 confirms AOC.
3. v1 underperforming v0 refutes AOC.
4. This pre-registered analysis bypasses the SRMF cautionary tale on
   flat-residue data; apparatus-bound `K` still requires two-real-pipeline
   contact for honest external validation.
5. p was tuned to fit the Pantheon+ data. p is committed in advance and
   matches the existing apparatus-bound K toy.

## Discipline Notes

1. The deformation form is now derived rather than fitted-after-data, but
   the value of `p` is still chosen from the toy rather than pinned by
   cosmology. Treating `p` as a fitted parameter would re-open
   look-elsewhere; `p` is therefore committed in advance and held fixed.
2. The Pantheon+ data has been seen multiple times before this contract.
   Pre-registration of the deformation shape and `p` reduces but does not
   eliminate post-hoc effects.
3. As with v0, all results are conditional on the Pantheon+ covariance
   being correct. A covariance-sensitivity sweep is a separate planned
   pass and is not part of this contract.
4. v1 does not deprecate v0. Both contracts coexist; v0 captures the
   phenomenological log-threshold history and v1 captures the proof-derived
   power-law shape.
