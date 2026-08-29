# Science Log

## 2026-04-26: First Real-Data Empirical Contract

Branch:

```text
empirical/pantheon_plus
```

Data:

```text
Pantheon+SH0ES distance table
https://github.com/PantheonPlusSH0ES/DataRelease
```

Local provenance:

```text
data/raw/pantheon_plus/PROVENANCE.md
```

Result:

```text
n_rows = 1701
threshold mu_err_max = 0.20
n_passing = 643
K_P = 1.78928
z_at_K_P = 0.78928
mu_err_at_K_P = 0.165559
```

Interpretation:

This is the first successful computation of a provisional apparatus-bound
`K_P` on a real public cosmology dataset.

Allowed claim:

> AOC's `K` formalism can be computed on a real supernova distance dataset.

Forbidden claim:

> AOC explains cosmic acceleration.

Report:

```text
reports/pantheon_plus/pantheon_k_report.md
```

Figure:

```text
reports/pantheon_plus/pantheon_k_uncertainty.png
```

Next technical improvement:

Replace threshold-only `K_P` with a likelihood-aware or covariance-aware
pipeline estimate, then compare against a baseline `LambdaCDM` distance
relation.

## 2026-04-26: Pantheon+ Threshold Sensitivity and Baseline Residuals

Branch:

```text
empirical/pantheon_plus
```

Added:

1. threshold sweep for `mu_err_max`,
2. simple flat-`LambdaCDM` residual instrument,
3. binned residual table,
4. threshold-sensitivity figure,
5. residual figure.

Threshold sensitivity:

| `mu_err_max` | rows passing | `K_P` | `z_at_K_P` |
| ---: | ---: | ---: | ---: |
| 0.12 | 3 | 1.37153 | 0.37153 |
| 0.15 | 116 | 1.64962 | 0.64962 |
| 0.18 | 414 | 1.78928 | 0.78928 |
| 0.20 | 643 | 1.78928 | 0.78928 |
| 0.22 | 861 | 1.97423 | 0.97423 |
| 0.25 | 1104 | 2.54901 | 1.54901 |
| 0.30 | 1382 | 3.26137 | 2.26137 |

Interpretation:

`K_P` is threshold-sensitive, as expected. This is good: it confirms that `K`
is a pipeline/contract quantity, not a hidden universal constant in this
apparatus-bound framing.

Baseline residual caveat:

The flat-`LambdaCDM` residual plot uses fixed `H0=70` and `Omega_m=0.3` only as
a comparison instrument. It is not a fit and does not use the covariance matrix.

Next technical improvement:

Implement a covariance-aware distance likelihood or use published Pantheon+
cosmology products before making any claim about model comparison.

## 2026-04-26: Pantheon+ Covariance-Aware Diagnostic

Downloaded:

```text
data/raw/pantheon_plus/Pantheon+SH0ES_STAT+SYS.cov
```

Provenance:

```text
data/raw/pantheon_plus/PROVENANCE.md
```

Covariance diagnostic:

```text
shape = 1701 x 1701
median sqrt(diag(C)) = 0.155560
median MU_SH0ES_ERR_DIAG = 0.218994
median difference = -0.060976
max absolute difference = 1.33821
```

Baseline residual diagnostic:

```text
model = flat LambdaCDM, H0=70, Omega_m=0.3
constant offset marginalized = -0.105936 mag
chi2 after offset = 1764.19
dof = 1700
chi2/dof = 1.03776
```

Interpretation:

The covariance file makes the branch materially stronger: we can now compute
covariance-aware residual diagnostics. It also shows that table-diagonal and
covariance-diagonal uncertainty definitions are not interchangeable, so both
must be reported separately.

Covariance-diagonal `K_P` sweep:

| sigma threshold | rows passing | `K_P` | `z_at_K_P` |
| ---: | ---: | ---: | ---: |
| 0.12 | 299 | 1.76932 | 0.76932 |
| 0.15 | 783 | 1.97423 | 0.97423 |
| 0.18 | 1150 | 2.54901 | 1.54901 |
| 0.20 | 1310 | 2.54901 | 1.54901 |
| 0.22 | 1430 | 3.26137 | 2.26137 |

Allowed claim:

> AOC's empirical contract can distinguish different reconstruction operators
> or uncertainty definitions on the same public dataset.

Forbidden claim:

> The covariance diagnostic validates AOC over LambdaCDM.

Next technical improvement:

Use the covariance matrix to define `K_P` through a degradation of
model-discriminability or likelihood curvature, not only through diagonal
thresholds.

## 2026-04-26: Pantheon+ Model-Discriminability K

Added:

```text
data/derived/pantheon_plus/pantheon_model_discriminability.csv
reports/pantheon_plus/pantheon_model_discriminability.png
```

Method:

Compare simple alternative distance operators against the fixed flat
`LambdaCDM` baseline over increasing redshift cutoffs. For each cutoff and
model, use the full covariance submatrix and marginalize a constant magnitude
offset. Report:

```text
Delta chi2 = chi2(alternative) - chi2(flat LambdaCDM)
```

The alternatives are comparison instruments, not AOC models:

1. coasting distance law,
2. low-z linear Hubble law extended beyond its valid regime.

Observed pattern:

1. At very low redshift, crude alternatives remain weakly distinguishable after
   offset marginalization.
2. The low-z linear law breaks strongly by approximately `z_cut=0.2`.
3. The coasting law separates more weakly, becoming positive around
   `z_cut=0.35`.

Representative values:

| alternative | `z_cut` | `K_cut` | `Delta chi2` |
| --- | ---: | ---: | ---: |
| linear_low_z | 0.20 | 1.20 | 110.64 |
| linear_low_z | 0.35 | 1.35 | 629.61 |
| coasting | 0.35 | 1.35 | 26.80 |
| coasting | 2.50 | 3.50 | 60.84 |

Interpretation:

This is the first likelihood-shaped `K` instrument in the repo. Instead of
asking only "how far does the diagonal uncertainty remain below a threshold?",
it asks "how deep in redshift does the dataset discriminate one reconstruction
operator from another?"

Allowed claim:

> AOC's empirical contract can define observer depth through
> model-discriminability using a real covariance matrix.

Forbidden claim:

> These comparison alternatives establish or refute AOC.

Next technical improvement:

Replace the placeholder alternatives with an AOC-motivated distance operator
or a one-parameter threshold deformation, then predeclare the comparison rule.

## 2026-04-26: First AOC-Style Threshold Deformation

Added:

```text
data/derived/pantheon_plus/pantheon_aoc_threshold_deformation.csv
reports/pantheon_plus/pantheon_aoc_threshold_deformation.png
```

Probe:

```text
mu_AOC(z) = mu_LCDM(z) + lambda * log(1 + z / z_star)
z_star = 0.8
```

Properties:

1. `lambda = 0` recovers the fixed flat-`LambdaCDM` baseline exactly.
2. Positive `lambda` makes high-redshift distances dimmer.
3. Negative `lambda` makes high-redshift distances brighter.
4. The form is phenomenological and threshold-shaped; it is not claimed as the
   final AOC distance law.

Best grid values:

| `z_cut` | `K_cut` | best `lambda` | best `Delta chi2` |
| ---: | ---: | ---: | ---: |
| 0.20 | 1.20 | -0.20 | -10.26 |
| 0.35 | 1.35 | -0.15 | -7.39 |
| 0.50 | 1.50 | -0.10 | -9.37 |
| 0.75 | 1.75 | -0.15 | -16.87 |
| 1.00 | 2.00 | -0.10 | -17.47 |
| 1.50 | 2.50 | -0.10 | -11.58 |
| 2.50 | 3.50 | -0.10 | -11.91 |

Interpretation:

The coarse grid prefers a small negative threshold deformation across most
redshift cutoffs. This is interesting but not yet a model-comparison result:
the run does not fit `H0`/`Omega_m`, does not penalize the extra parameter, and
does not pre-register this deformation.

Allowed claim:

> A one-parameter AOC-style threshold deformation can be evaluated against real
> Pantheon+ data with the full covariance matrix.

Forbidden claim:

> Pantheon+ currently supports AOC over `LambdaCDM`.

Next technical improvement:

Add a parameter penalty / information criterion and a finer optimizer for
`lambda`, or predeclare a physically motivated deformation from the AOC proof
spine before further data contact.

## 2026-04-26: Penalized AOC Threshold-Deformation Pass

Updated:

```text
empirical/pantheon_plus/analyze_pantheon_k.py
```

Change:

1. refined `lambda` grid to `[-0.30, 0.30]` in steps of `0.01`,
2. added `Delta AIC`,
3. added `Delta BIC`,
4. updated threshold-deformation figure to show BIC penalty.

Best penalized values:

| `z_cut` | `K_cut` | best `lambda` | `Delta chi2` | `Delta AIC` | `Delta BIC` |
| ---: | ---: | ---: | ---: | ---: | ---: |
| 0.20 | 1.20 | -0.30 | -11.70 | -9.70 | -4.85 |
| 0.35 | 1.35 | -0.13 | -7.65 | -5.65 | -0.46 |
| 0.50 | 1.50 | -0.11 | -9.45 | -7.45 | -2.14 |
| 0.75 | 1.75 | -0.13 | -17.51 | -15.51 | -10.10 |
| 1.00 | 2.00 | -0.12 | -18.11 | -16.11 | -10.69 |
| 1.50 | 2.50 | -0.09 | -11.61 | -9.61 | -4.18 |
| 2.50 | 3.50 | -0.09 | -11.97 | -9.97 | -4.53 |

Interpretation:

After a one-parameter BIC penalty, the threshold deformation remains strongest
around `z_cut=0.75` to `1.00`. This is hypothesis-forming only: the deformation
was introduced after seeing the Pantheon+ branch, so it must not be sold as a
confirmed prediction.

Added preregistration stub:

```text
empirical/pantheon_plus/PREREG_NEXT.md
```

Allowed claim:

> The AOC-style threshold-deformation probe remains evaluable under AIC/BIC
> penalties and shows its strongest exploratory signal near `z_cut=0.75-1.00`.

Forbidden claim:

> This is confirmed evidence for AOC.

Next technical improvement:

Run the predeclared rule on a genuinely separate dataset, a held-out split, or
DESI BAO products.

## 2026-04-26: Exploratory Pantheon+ Heldout Check

Added:

```text
data/derived/pantheon_plus/pantheon_aoc_holdout_validation.csv
reports/pantheon_plus/pantheon_aoc_holdout_validation.png
```

Method:

Use a deterministic object-level split:

```text
split = sha256(CID) first-byte parity
```

For each redshift cutoff, select `lambda` for the AOC-style threshold
deformation on the train side, then evaluate that selected value once on the
holdout side. Repeated rows for the same `CID` stay on the same side.

Holdout result:

| `z_cut` | `K_cut` | train `lambda` | holdout `Delta chi2` | holdout `Delta BIC` |
| ---: | ---: | ---: | ---: | ---: |
| 0.20 | 1.20 | -0.18 | -8.84 | -2.69 |
| 0.35 | 1.35 | -0.12 | -5.74 | 0.74 |
| 0.50 | 1.50 | -0.10 | -6.91 | -0.29 |
| 0.75 | 1.75 | -0.12 | -12.60 | -5.89 |
| 1.00 | 2.00 | -0.13 | -12.04 | -5.32 |
| 1.50 | 2.50 | -0.11 | -6.26 | 0.48 |
| 2.50 | 3.50 | -0.10 | -7.53 | -0.79 |

Interpretation:

The heldout pass is materially better discipline than same-sample reporting:
the same qualitative region remains strongest, around `z_cut=0.75` to `1.00`,
but the BIC improvement is weaker. This is still exploratory because the
deformation form was selected after prior Pantheon+ contact.

Implementation note:

The analyzer now reuses the covariance solve across the whole `lambda` grid for
each subset. This preserves the same statistic while reducing the full
Pantheon+ analysis runtime from roughly `344s` to roughly `14s` on this
machine.

Allowed claim:

> The first AOC-style threshold deformation survives a deterministic Pantheon+
> holdout check as a weak exploratory pattern, with its strongest heldout signal
> near `z_cut=0.75-1.00`.

Forbidden claim:

> The heldout check confirms AOC or explains cosmic acceleration.

Next technical improvement:

Commit a new deformation rule before data contact, then evaluate it on a
separate public dataset or a truly blinded split.

## 2026-04-26: Pantheon+ Split-Robustness Check

Added:

```text
data/derived/pantheon_plus/pantheon_aoc_split_robustness.csv
reports/pantheon_plus/pantheon_aoc_split_robustness.png
```

Method:

Repeat the AOC threshold-deformation train/holdout procedure across 16 salted
`CID` splits. For each split and cutoff, select `lambda` on train and evaluate
on holdout. Summarize the holdout distribution.

Robustness summary:

| `z_cut` | median train `lambda` | median holdout `Delta chi2` | median holdout `Delta BIC` | frac `Delta BIC < 0` | frac `Delta BIC < -2` |
| ---: | ---: | ---: | ---: | ---: | ---: |
| 0.20 | -0.275 | -6.27 | -0.10 | 0.50 | 0.25 |
| 0.35 | -0.135 | -3.16 | 3.33 | 0.00 | 0.00 |
| 0.50 | -0.120 | -3.18 | 3.45 | 0.25 | 0.00 |
| 0.75 | -0.130 | -9.42 | -2.71 | 0.69 | 0.50 |
| 1.00 | -0.130 | -10.20 | -3.46 | 0.75 | 0.63 |
| 1.50 | -0.100 | -6.99 | -0.27 | 0.63 | 0.19 |
| 2.50 | -0.095 | -7.35 | -0.61 | 0.56 | 0.19 |

Interpretation:

The split-robustness check preserves the same broad intermediate-redshift
pattern, with the strongest median heldout BIC behavior at `z_cut=1.00`.
However, the split distribution is broad: some salted splits do not support the
deformation after BIC penalty. The result is therefore a useful empirical handle,
not evidence strong enough to claim support for AOC.

Allowed claim:

> The exploratory AOC-style threshold deformation is not solely an artifact of
> one object-level split; its strongest split-robust behavior remains near
> `z_cut=0.75-1.00`.

Forbidden claim:

> Split robustness confirms the deformation or validates AOC.

Next technical improvement:

Derive a deformation from the AOC proof spine or freeze the phenomenological
form before testing a separate public dataset.
