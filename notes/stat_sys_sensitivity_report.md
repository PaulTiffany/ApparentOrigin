# Stat/Sys Covariance Sensitivity Report

## Summary
We performed a differential sensitivity sweep of the AOC v0 signal on Pantheon+ by independently rescaling the statistical and systematic components of the covariance matrix.

## Method
1. **Decomposition:** $C_{total} = C_{stat} + C_{sys}$ (derived from `STATONLY.cov` and `STAT+SYS.cov`).
2. **Rescaling:** $C_{mod} = s_{stat} C_{stat} + s_{sys} C_{sys}$.
3. **Metric:** Best-fit $\Delta \text{BIC}$ for the log-deformation at $z_{cut}=1.0$.

## Results (Selection)
| $s_{stat}$ | $s_{sys}$ | $\Delta \text{BIC}$ |
| :---: | :---: | :---: |
| 1.0 | 1.0 | -10.7 |
| 0.8 | 0.8 | -15.2 |
| 1.5 | 1.0 | -5.1 |
| 1.0 | 1.5 | -10.6 |
| 1.5 | 1.5 | -4.7 |

## Key Observations
1. **High Robustness:** The exploratory signal ($\Delta \text{BIC} < 0$) survives across the entire tested grid. Even a 50% under-reporting of *both* statistical and systematic errors leaves a signal of $\Delta \text{BIC} \approx -4.7$ (moderate evidence).
2. **Statistical Sensitivity:** The signal is significantly more sensitive to the scaling of statistical noise ($s_{stat}$) than systematic noise ($s_{sys}$). 
   - Increasing $s_{sys}$ from 1.0 to 1.5 (with $s_{stat}=1.0$) only changes $\Delta \text{BIC}$ from -10.7 to -10.6.
   - Increasing $s_{stat}$ from 1.0 to 1.5 (with $s_{sys}=1.0$) moves $\Delta \text{BIC}$ from -10.7 to -5.1.
3. **Diagonal Dominance:** This sensitivity pattern suggests the "AOC-style" signal is primarily constrained by the high-precision low-redshift diagonal components (which are mostly statistical) rather than the off-diagonal systematic correlations.

## Conclusion
The v0 signal is not a "fragile" artifact of a specific systematics model. It is a robust feature of the distance-redshift relation in the Pantheon+ sample, conditional on the noise being within 50% of the reported values.
