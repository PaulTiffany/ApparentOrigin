# Planck Operator-Residue Report

Status: generated from low-ell coefficient table.

Input:

```text
data\derived\planck_operator_residue\planck_lowell_alm_fallback_nside32.csv
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
median pairwise coefficient distance = 0.342372
```

Parity ratios:

| operator | odd/even low-ell power |
| --- | ---: |
| `Commander` | 1.42473 |
| `NILC` | 1.46964 |
| `SEVEM` | 1.406 |
| `SMICA` | 1.45554 |

Interpretation:

This report measures whether the same low-ell coefficients remain stable
across reconstruction operators. It does not interpret stability as AOC
evidence without mask, smoothing, simulation, foreground, and statistic
selection controls.

Pairwise rows:

```text
174
```
