# Pantheon+ Apparatus-Bound K Report

Status: provisional empirical contract.

## Allowed Claim

AOC's K formalism can be computed on a real supernova distance dataset.

## Forbidden Claim

AOC explains cosmic acceleration.

## Summary

- Rows parsed: `1701`
- Redshift column: `zHD`
- Uncertainty column: `MU_SH0ES_ERR_DIAG`
- Threshold `mu_err_max`: `0.2`
- Rows passing threshold: `643`
- Provisional `K_P = max(1+z)`: `1.78928`
- Redshift at `K_P`: `0.78928`
- Uncertainty at `K_P`: `0.165559`

## Interpretation

K_P is the largest observed 1+z value passing the provisional distance-modulus uncertainty threshold. This is a pipeline dynamic-range estimate, not a cosmological claim.

## Binned Uncertainty

| bin | z range | n | median sigma_mu | p90 sigma_mu |
| --- | --- | ---: | ---: | ---: |
| 0 | 0.00122-0.1896 | 922 | 0.2217 | 0.3726 |
| 1 | 0.1896-0.3779 | 449 | 0.2048 | 0.2859 |
| 2 | 0.3779-0.5663 | 178 | 0.2147 | 0.3317 |
| 3 | 0.5663-0.7546 | 105 | 0.2569 | 0.3708 |
| 4 | 0.7546-0.9429 | 21 | 0.2502 | 0.3117 |
| 5 | 0.9429-1.131 | 7 | 0.3534 | 0.4808 |
| 6 | 1.131-1.32 | 6 | 0.3164 | 0.5278 |
| 7 | 1.32-1.508 | 6 | 0.3124 | 0.5551 |
| 8 | 1.508-1.696 | 3 | 0.333 | 0.3634 |
| 9 | 1.696-1.885 | 2 | 0.3312 | 0.3706 |
| 10 | 1.885-2.073 | 1 | 0.3586 | 0.3586 |
| 11 | 2.073-2.261 | 1 | 0.2813 | 0.2813 |

## Threshold Sensitivity

| mu_err_max | n passing | K_P | z at K_P |
| ---: | ---: | ---: | ---: |
| 0.12 | 3 | 1.37153 | 0.37153 |
| 0.15 | 116 | 1.64962 | 0.64962 |
| 0.18 | 414 | 1.78928 | 0.78928 |
| 0.2 | 643 | 1.78928 | 0.78928 |
| 0.22 | 861 | 1.97423 | 0.97423 |
| 0.25 | 1104 | 2.54901 | 1.54901 |
| 0.3 | 1382 | 3.26137 | 2.26137 |
| 0.35 | 1531 | 3.26137 | 2.26137 |
| 0.4 | 1609 | 3.26137 | 2.26137 |

## Baseline LambdaCDM Residual Check

Baseline used only as a comparison instrument:

```text
flat LambdaCDM, H0 = 70 km/s/Mpc, Omega_m = 0.3
```

This is not a cosmological fit and does not use the covariance matrix.

| bin | z range | n | median residual mag | p10-p90 residual mag | median pull |
| --- | --- | ---: | ---: | ---: | ---: |
| 0 | 0.00122-0.1896 | 922 | -0.09477 | -0.2826 to 0.134 | -0.4176 |
| 1 | 0.1896-0.3779 | 449 | -0.1074 | -0.2653 to 0.07861 | -0.5507 |
| 2 | 0.3779-0.5663 | 178 | -0.1184 | -0.2906 to 0.05569 | -0.5364 |
| 3 | 0.5663-0.7546 | 105 | -0.1477 | -0.3172 to 0.003103 | -0.5975 |
| 4 | 0.7546-0.9429 | 21 | -0.1583 | -0.3931 to -0.02696 | -0.682 |
| 5 | 0.9429-1.131 | 7 | 0.08094 | -0.08345 to 0.2627 | 0.4016 |
| 6 | 1.131-1.32 | 6 | 0.007712 | -0.2168 to 0.2188 | 0.03873 |
| 7 | 1.32-1.508 | 6 | -0.1634 | -0.4686 to -0.04955 | -0.4858 |
| 8 | 1.508-1.696 | 3 | -0.1744 | -0.2168 to -0.02063 | -0.4701 |
| 9 | 1.696-1.885 | 2 | -0.2125 | -0.229 to -0.196 | -0.6466 |
| 10 | 1.885-2.073 | 1 | -0.4137 | -0.4137 to -0.4137 | -1.154 |
| 11 | 2.073-2.261 | 1 | -0.1001 | -0.1001 to -0.1001 | -0.3559 |

## Covariance-Aware Diagnostic

Covariance file loaded successfully.

- Shape: `[1701, 1701]`
- Median covariance diagonal sigma: `0.15556`
- Median table sigma: `0.218994`
- Median diagonal-minus-table sigma: `-0.0609756`
- Max absolute diagonal-minus-table sigma: `1.33821`
- Marginalized constant offset: `-0.105936` mag
- Chi2 after offset: `1764.19`
- DOF after offset: `1700`
- Chi2/DOF after offset: `1.03776`

This is a covariance-aware baseline residual diagnostic, not a fit. The constant offset absorbs calibration/H0-like magnitude shifts.

### Covariance-Diagonal K Sensitivity

This repeats the `K_P` threshold sweep using `sqrt(diag(C))` from the
downloaded covariance matrix rather than `MU_SH0ES_ERR_DIAG` from the
table. Because these differ, both are reported separately.

| sigma threshold | n passing | K_P | z at K_P | sigma at K_P |
| ---: | ---: | ---: | ---: | ---: |
| 0.12 | 299 | 1.76932 | 0.76932 | 0.115234 |
| 0.15 | 783 | 1.97423 | 0.97423 | 0.146607 |
| 0.18 | 1150 | 2.54901 | 1.54901 | 0.167039 |
| 0.2 | 1310 | 2.54901 | 1.54901 | 0.167039 |
| 0.22 | 1430 | 3.26137 | 2.26137 | 0.212109 |
| 0.25 | 1538 | 3.26137 | 2.26137 | 0.212109 |
| 0.3 | 1637 | 3.26137 | 2.26137 | 0.212109 |
| 0.35 | 1676 | 3.26137 | 2.26137 | 0.212109 |
| 0.4 | 1691 | 3.26137 | 2.26137 | 0.212109 |

### Model-Discriminability K

This compares simple alternative distance curves against the fixed
flat-`LambdaCDM` baseline over increasing redshift cutoffs using the
full covariance submatrix. A constant magnitude offset is marginalized
separately for each model and cutoff.

These alternatives are comparison instruments, not AOC models.

| alternative | z cut | K cut | n | delta chi2 | delta chi2 / dof |
| --- | ---: | ---: | ---: | ---: | ---: |
| coasting | 0.05 | 1.05 | 645 | -6.48261 | -0.0100662 |
| linear_low_z | 0.05 | 1.05 | 645 | -14.6493 | -0.0227474 |
| coasting | 0.1 | 1.1 | 741 | -6.80602 | -0.00919733 |
| linear_low_z | 0.1 | 1.1 | 741 | -6.47547 | -0.00875064 |
| coasting | 0.2 | 1.2 | 948 | -10.4636 | -0.0110492 |
| linear_low_z | 0.2 | 1.2 | 948 | 110.644 | 0.116836 |
| coasting | 0.35 | 1.35 | 1328 | 26.8037 | 0.0201987 |
| linear_low_z | 0.35 | 1.35 | 1328 | 629.608 | 0.47446 |
| coasting | 0.5 | 1.5 | 1491 | 47.4353 | 0.0318358 |
| linear_low_z | 0.5 | 1.5 | 1491 | 1027.37 | 0.689508 |
| coasting | 0.75 | 1.75 | 1653 | 44.8961 | 0.0271768 |
| linear_low_z | 0.75 | 1.75 | 1653 | 1354.2 | 0.819731 |
| coasting | 1 | 2 | 1676 | 46.3469 | 0.0276698 |
| linear_low_z | 1 | 2 | 1676 | 1438.97 | 0.859086 |
| coasting | 1.5 | 2.5 | 1694 | 60.8727 | 0.0359555 |
| linear_low_z | 1.5 | 2.5 | 1694 | 1634.97 | 0.965726 |
| coasting | 2.5 | 3.5 | 1701 | 60.844 | 0.0357906 |
| linear_low_z | 2.5 | 3.5 | 1701 | 1686.8 | 0.992236 |

### AOC Threshold-Deformation Probe

Minimal one-parameter deformation:

```text
mu_AOC(z) = mu_LCDM(z) + lambda * log(1 + z / z_star)
z_star = 0.8
```

`lambda = 0` recovers the flat-`LambdaCDM` baseline exactly. This is
a phenomenological threshold probe, not the final AOC distance law.

| z cut | K cut | n | best lambda | best delta chi2 | best delta AIC | best delta BIC |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 0.2 | 1.2 | 948 | -0.3 | -11.7022 | -9.70224 | -4.84788 |
| 0.35 | 1.35 | 1328 | -0.13 | -7.65176 | -5.65176 | -0.460331 |
| 0.5 | 1.5 | 1491 | -0.11 | -9.44726 | -7.44726 | -2.14006 |
| 0.75 | 1.75 | 1653 | -0.13 | -17.5093 | -15.5093 | -10.099 |
| 1 | 2 | 1676 | -0.12 | -18.1096 | -16.1096 | -10.6854 |
| 1.5 | 2.5 | 1694 | -0.09 | -11.6103 | -9.61029 | -4.17544 |
| 2.5 | 3.5 | 1701 | -0.09 | -11.9672 | -9.96716 | -4.52819 |

### AOC Threshold-Deformation Holdout Check

This is a deterministic exploratory train/holdout check. The split is
by `CID` using `sha256(CID)` first-byte parity, so repeated rows for
the same object stay on the same side where the identifier is stable.

For each redshift cutoff, `lambda` is selected on the train side and
then evaluated once on the holdout side. Because the deformation form
was chosen after earlier Pantheon+ exploration, this is still not a
fully blinded confirmation.

| z cut | K cut | n train | n holdout | train lambda | holdout delta chi2 | holdout delta AIC | holdout delta BIC |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 0.2 | 1.2 | 480 | 468 | -0.18 | -8.83551 | -6.83551 | -2.68704 |
| 0.35 | 1.35 | 679 | 649 | -0.12 | -5.73819 | -3.73819 | 0.737246 |
| 0.5 | 1.5 | 746 | 745 | -0.1 | -6.90629 | -4.90629 | -0.292907 |
| 0.75 | 1.75 | 833 | 820 | -0.12 | -12.6036 | -10.6036 | -5.89425 |
| 1 | 2 | 846 | 830 | -0.13 | -12.0416 | -10.0416 | -5.32016 |
| 1.5 | 2.5 | 855 | 839 | -0.11 | -6.25594 | -4.25594 | 0.476274 |
| 2.5 | 3.5 | 858 | 843 | -0.1 | -7.52514 | -5.52514 | -0.788168 |

### AOC Split-Robustness Check

This repeats the train/holdout procedure across 16 salted `CID`
splits and summarizes the holdout distribution. It checks whether
the exploratory pattern depends heavily on the single primary split.

| z cut | K cut | splits | median lambda | median holdout delta chi2 | median holdout delta BIC | frac BIC < 0 | frac BIC < -2 |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 0.2 | 1.2 | 16 | -0.275 | -6.27318 | -0.0983579 | 0.5 | 0.25 |
| 0.35 | 1.35 | 16 | -0.135 | -3.15699 | 3.32969 | 0 | 0 |
| 0.5 | 1.5 | 16 | -0.12 | -3.18263 | 3.452 | 0.25 | 0 |
| 0.75 | 1.75 | 16 | -0.13 | -9.41557 | -2.71394 | 0.688 | 0.5 |
| 1 | 2 | 16 | -0.13 | -10.1995 | -3.46133 | 0.75 | 0.625 |
| 1.5 | 2.5 | 16 | -0.1 | -6.9881 | -0.272861 | 0.625 | 0.188 |
| 2.5 | 3.5 | 16 | -0.095 | -7.35478 | -0.608998 | 0.562 | 0.188 |


## Next Step

Run the predeclared rule on a genuinely separate dataset or a blinded split, then replace the phenomenological threshold deformation with a distance law derived from the AOC proof spine.
