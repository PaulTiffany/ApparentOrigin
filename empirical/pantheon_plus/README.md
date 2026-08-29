# Pantheon+ Empirical Contract

Status: first real-data branch.

Purpose:

Estimate a provisional apparatus-bound dynamic range `K_P` from public
Pantheon+ supernova distance data.

## Data Source

Repository:

```text
https://github.com/PantheonPlusSH0ES/DataRelease
```

Raw distance file:

```text
https://raw.githubusercontent.com/PantheonPlusSH0ES/DataRelease/main/Pantheon%2B_Data/4_DISTANCES_AND_COVAR/Pantheon%2BSH0ES.dat
```

Local raw path:

```text
data/raw/pantheon_plus/Pantheon+SH0ES.dat
```

## Empirical Contract

Allowed claim:

> This computes a provisional apparatus-bound `K_P` on a real supernova
> distance dataset.

Forbidden claim:

> AOC explains cosmic acceleration.

## Method

Use redshift as:

```tex
y = 1+z.
```

Use distance-modulus uncertainty as the first reliability proxy:

```tex
\operatorname{Rel}(y)=1/\sigma_\mu.
```

For an uncertainty threshold `mu_err_max`, define:

```tex
K_P = \max(1+z_i)
\quad\text{such that}\quad
\sigma_{\mu,i}\le\mu_{\rm err,max}.
```

This is deliberately simple. It is a first empirical interface test, not a
cosmological inference.

## Commands

Download data:

```powershell
python empirical\pantheon_plus\download_pantheon_plus.py
```

Analyze:

```powershell
python empirical\pantheon_plus\analyze_pantheon_k.py
```

Outputs:

```text
data/derived/pantheon_plus/pantheon_k_summary.json
data/derived/pantheon_plus/pantheon_k_bins.csv
data/derived/pantheon_plus/pantheon_k_threshold_sweep.csv
data/derived/pantheon_plus/pantheon_lcdm_residual_bins.csv
reports/pantheon_plus/pantheon_k_report.md
reports/pantheon_plus/pantheon_k_uncertainty.png
reports/pantheon_plus/pantheon_k_threshold_sweep.png
reports/pantheon_plus/pantheon_lcdm_residuals.png
```

## Current Caveat

The baseline `LambdaCDM` residual plot uses fixed `H0=70` and `Omega_m=0.3`.
It is a comparison instrument, not a fit. The next version should use the
Pantheon+ covariance products or published cosmology likelihoods.

## Covariance-Aware Outputs

The downloader also fetches:

```text
data/raw/pantheon_plus/Pantheon+SH0ES_STAT+SYS.cov
```

The analyzer writes:

```text
data/derived/pantheon_plus/pantheon_covariance_summary.json
data/derived/pantheon_plus/pantheon_covariance_diag_k_sweep.csv
data/derived/pantheon_plus/pantheon_model_discriminability.csv
data/derived/pantheon_plus/pantheon_aoc_holdout_validation.csv
data/derived/pantheon_plus/pantheon_aoc_split_robustness.csv
```

The covariance diagnostic marginalizes a constant magnitude offset against a
fixed flat-`LambdaCDM` baseline. This is still not a cosmological fit; it is a
sanity check that the branch can use the full covariance matrix.

## Model-Discriminability Output

The analyzer also compares simple alternative distance operators against the
fixed flat-`LambdaCDM` baseline over increasing redshift cutoffs:

```text
reports/pantheon_plus/pantheon_model_discriminability.png
```

The alternatives are comparison instruments only. This section exists to test a
likelihood-shaped `K`: observer depth as the redshift range over which the data
can discriminate reconstruction operators.

## AOC Threshold-Deformation Probe

The analyzer includes a first AOC-style one-parameter threshold deformation:

```text
mu_AOC(z) = mu_LCDM(z) + lambda * log(1 + z / z_star)
z_star = 0.8
```

Output:

```text
data/derived/pantheon_plus/pantheon_aoc_threshold_deformation.csv
data/derived/pantheon_plus/pantheon_aoc_holdout_validation.csv
data/derived/pantheon_plus/pantheon_aoc_split_robustness.csv
reports/pantheon_plus/pantheon_aoc_threshold_deformation.png
reports/pantheon_plus/pantheon_aoc_holdout_validation.png
reports/pantheon_plus/pantheon_aoc_split_robustness.png
```

This is a phenomenological probe. It is not yet a claimed AOC distance law.

The heldout check selects `lambda` on a deterministic `CID` split and evaluates
the selected value on the other side. This is stronger than same-sample
exploration, but it is still not a blinded confirmation because the deformation
form was introduced after earlier Pantheon+ contact.

The split-robustness check repeats the same procedure across 16 salted `CID`
splits. Its purpose is not to create a stronger claim; it tests whether the
exploratory signal depends heavily on one partition.

The next-pass protocol is recorded in:

```text
empirical/pantheon_plus/PREREG_NEXT.md
```
