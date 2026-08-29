# Planck Operator-Residue Report

Status: generated from low-ell coefficient table.

Input:

```text
data\derived\planck_operator_residue\planck_lowell_alm_fallback_nside64.csv
```

Band:

```text
2 <= ell <= 30
```

Operators:

- `Commander`
- `NILC`
- `SEVEM`
- `SMICA`

Primary stability score:

```text
median pairwise coefficient distance = 0.337761
```

Parity ratios:

| operator | odd/even low-ell power |
| --- | ---: |
| `Commander` | 1.42073 |
| `NILC` | 1.46726 |
| `SEVEM` | 1.40346 |
| `SMICA` | 1.45338 |

Interpretation:

This report measures whether the same low-ell coefficients remain stable
across reconstruction operators. It does not interpret stability as AOC
evidence without mask, smoothing, simulation, foreground, and statistic
selection controls.

Pairwise rows:

```text
174
```
