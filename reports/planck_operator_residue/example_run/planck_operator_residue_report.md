# Planck Operator-Residue Report

Status: generated from low-ell coefficient table.

Input:

```text
data\derived\planck_operator_residue\example_lowell_alm.csv
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
median pairwise coefficient distance = 0.106512
```

Parity ratios:

| operator | odd/even low-ell power |
| --- | ---: |
| `Commander` | 1.21524 |
| `NILC` | 1.31438 |
| `SEVEM` | 1.54556 |
| `SMICA` | 1.1245 |

Interpretation:

This report measures whether the same low-ell coefficients remain stable
across reconstruction operators. It does not interpret stability as AOC
evidence without mask, smoothing, simulation, foreground, and statistic
selection controls.

Pairwise rows:

```text
174
```
