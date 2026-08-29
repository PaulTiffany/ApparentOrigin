# Pantheon+ Next-Step Preregistration Stub

Status: draft protocol. The deterministic Pantheon+ heldout pass below has now
been run and should be treated as exploratory, not blinded.

## Goal

Test whether an AOC-motivated threshold deformation remains useful when the
comparison rule is fixed before the run.

## Fixed Baseline

Flat `LambdaCDM` with:

```text
H0 = 70 km/s/Mpc
Omega_m = 0.3
```

Constant magnitude offset is marginalized for every model and cutoff.

## Candidate Deformation

Current phenomenological probe:

```text
mu_AOC(z) = mu_LCDM(z) + lambda * log(1 + z / z_star)
z_star = 0.8
```

This is not yet claimed as the final AOC distance law.

## Primary Comparison

Use the full Pantheon+ covariance submatrix at each redshift cutoff.

Cutoffs:

```text
z_cut = 0.20, 0.35, 0.50, 0.75, 1.00, 1.50, 2.50
```

Fit only:

```text
lambda
```

Grid:

```text
lambda in [-0.30, 0.30] by 0.01
```

Primary statistic:

```text
Delta BIC = BIC_AOC - BIC_LCDM
```

Interpretation:

1. `Delta BIC < -10`: strong improvement for the deformation at that cutoff.
2. `-10 <= Delta BIC < -2`: weak/moderate improvement.
3. `Delta BIC >= -2`: no meaningful support after parameter penalty.

## Current Observed Result

The current exploratory run already looked at this data, so the next pass is
not blinded. The current result should therefore be treated as hypothesis
formation, not confirmation.

Current strongest BIC improvements occur near:

```text
z_cut = 0.75 to 1.00
```

## Next Clean Test

Use one of:

1. a predeclared alternate public supernova compilation,
2. DESI BAO expansion products,
3. a held-out Pantheon+ split defined before analysis.

## Exploratory Heldout Pass Already Run

A deterministic Pantheon+ split was added after the same-sample deformation
probe:

```text
split = sha256(CID) first-byte parity
```

For each cutoff, `lambda` was selected on the train side and evaluated on the
holdout side. This reduces same-sample overfitting pressure, but it is still not
a clean confirmation because the deformation form had already been chosen after
Pantheon+ exploration.

Holdout summary:

| `z_cut` | train `lambda` | holdout `Delta chi2` | holdout `Delta BIC` |
| ---: | ---: | ---: | ---: |
| 0.20 | -0.18 | -8.84 | -2.69 |
| 0.35 | -0.12 | -5.74 | 0.74 |
| 0.50 | -0.10 | -6.91 | -0.29 |
| 0.75 | -0.12 | -12.60 | -5.89 |
| 1.00 | -0.13 | -12.04 | -5.32 |
| 1.50 | -0.11 | -6.26 | 0.48 |
| 2.50 | -0.10 | -7.53 | -0.79 |

Interpretation:

The heldout pass preserves the same qualitative location of the strongest
exploratory signal, near `z_cut = 0.75` to `1.00`, but the BIC improvement is
weaker than the same-sample result. The correct next clean test remains a
separate dataset or a split committed before any new deformation choice.

## Split-Robustness Pass Already Run

The train/holdout procedure was repeated across 16 salted `CID` splits. This is
still exploratory, but it checks whether the qualitative result depends on one
partition.

Summary:

| `z_cut` | median train `lambda` | median holdout `Delta BIC` | fraction `Delta BIC < 0` | fraction `Delta BIC < -2` |
| ---: | ---: | ---: | ---: | ---: |
| 0.20 | -0.275 | -0.10 | 0.50 | 0.25 |
| 0.35 | -0.135 | 3.33 | 0.00 | 0.00 |
| 0.50 | -0.120 | 3.45 | 0.25 | 0.00 |
| 0.75 | -0.130 | -2.71 | 0.69 | 0.50 |
| 1.00 | -0.130 | -3.46 | 0.75 | 0.63 |
| 1.50 | -0.100 | -0.27 | 0.63 | 0.19 |
| 2.50 | -0.095 | -0.61 | 0.56 | 0.19 |

Interpretation:

The intermediate cutoff band remains the most stable exploratory region,
especially `z_cut = 1.00`. The broad p10-p90 range means this remains a weak
pattern, not a confirmed effect.
