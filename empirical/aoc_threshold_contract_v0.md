# AOC Threshold-Deformation Empirical Contract v0

Status: frozen exploratory contract as of 2026-04-26.

Purpose:

Define the current AOC-style threshold-deformation probe in a way that can be
handed to source-grounded tools or reused on a separate dataset without
quietly changing the rule.

## Scope

This contract covers the first phenomenological AOC threshold-deformation
probe applied to supernova distance-modulus data.

It does not define the final AOC distance law.

## Baseline

Use fixed flat `LambdaCDM`:

```text
H0 = 70 km/s/Mpc
Omega_m = 0.3
```

For every model and redshift cutoff, marginalize a constant magnitude offset.
This offset absorbs calibration or `H0`-like shifts and prevents the comparison
from depending on an arbitrary vertical normalization.

## Candidate Deformation

Use:

```text
mu_AOC(z) = mu_LCDM(z) + lambda * log(1 + z / z_star)
z_star = 0.8
```

Grid:

```text
lambda in [-0.30, 0.30] by 0.01
```

Interpretation:

1. `lambda = 0` recovers the baseline exactly.
2. Positive `lambda` makes high-redshift distances dimmer.
3. Negative `lambda` makes high-redshift distances brighter.
4. The form is threshold-shaped and phenomenological.

## Cutoffs

Use:

```text
z_cut = 0.20, 0.35, 0.50, 0.75, 1.00, 1.50, 2.50
```

Report:

```text
K_cut = 1 + z_cut
```

## Primary Statistic

Use the covariance submatrix for each redshift cutoff.

For same-sample exploratory scans, report:

```text
Delta chi2 = chi2_AOC - chi2_LCDM
Delta AIC = AIC_AOC - AIC_LCDM
Delta BIC = BIC_AOC - BIC_LCDM
```

Because the AOC probe has one extra parameter:

```text
Delta AIC = Delta chi2 + 2
Delta BIC = Delta chi2 + log(n)
```

Primary interpretation should use `Delta BIC`.

## Holdout Procedure

Use object-level splits when object identifiers are available.

Primary Pantheon+ split:

```text
split = sha256(CID) first-byte parity
```

For each cutoff:

1. select `lambda` on the train side,
2. evaluate that selected `lambda` once on holdout,
3. report holdout `Delta chi2`, `Delta AIC`, and `Delta BIC`.

Robustness check:

Repeat the train/holdout procedure across salted `CID` splits and summarize
the distribution of holdout `Delta BIC`.

## Current Pantheon+ Exploratory Result

Same-sample strongest region:

```text
z_cut = 0.75 to 1.00
K_cut = 1.75 to 2.00
```

Primary heldout result:

| `z_cut` | train `lambda` | holdout `Delta chi2` | holdout `Delta BIC` |
| ---: | ---: | ---: | ---: |
| 0.75 | -0.12 | -12.60 | -5.89 |
| 1.00 | -0.13 | -12.04 | -5.32 |

Split-robustness result:

| `z_cut` | median train `lambda` | median holdout `Delta BIC` | fraction `Delta BIC < -2` |
| ---: | ---: | ---: | ---: |
| 0.75 | -0.13 | -2.71 | 0.50 |
| 1.00 | -0.13 | -3.46 | 0.63 |

## Allowed Claims

The current allowed claims are:

1. AOC's `K` formalism can be computed on real supernova distance data.
2. A covariance-aware empirical contract can evaluate AOC-style threshold
   operators.
3. The first phenomenological threshold deformation has its strongest
   exploratory behavior around `z_cut = 0.75` to `1.00`.
4. The pattern is not solely an artifact of one deterministic object-level
   split.

## Forbidden Claims

Do not claim:

1. Pantheon+ confirms AOC.
2. AOC explains cosmic acceleration.
3. AOC explains the Hubble tension.
4. The Big Bang is false.
5. `LambdaCDM` has been refuted.
6. The current deformation is the final AOC distance law.
7. The heldout or split-robustness checks are blinded confirmation.

## Current Interpretation

The result is a live empirical handle, not evidence strong enough to establish
the theory. The next clean step is to test a frozen deformation rule on a
separate public dataset or derive a replacement deformation from the AOC proof
spine before further data contact.

