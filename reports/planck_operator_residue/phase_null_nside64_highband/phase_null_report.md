# Planck Operator-Residue Phase Null

Status: coefficient-level control, not a full CMB simulation.

Input:

```text
data\derived\planck_operator_residue\planck_lowell_alm_fallback_nside64.csv
```

Band:

```text
11 <= ell <= 30
```

Null:

For each operator and coefficient, preserve `|a_lm|` and randomize phase
independently for `m > 0`; randomly sign-flip `m = 0`.

Headline:

```text
observed stability score = 0.377989
null median = 1.41489
null q05 = 1.38498
null q95 = 1.44088
fraction null <= observed = 0
n_null = 1000
```

Pair medians:

| pair | observed | null median |
| --- | ---: | ---: |
| `Commander-NILC` | 0.323794 | 1.41362 |
| `Commander-SEVEM` | 0.47402 | 1.41491 |
| `Commander-SMICA` | 0.29971 | 1.41513 |
| `NILC-SEVEM` | 0.520379 | 1.41223 |
| `NILC-SMICA` | 0.101391 | 1.41408 |
| `SEVEM-SMICA` | 0.505091 | 1.4138 |

Interpretation:

This null asks whether cross-operator closeness depends on phase alignment
rather than only on each operator's low-ell power. If the observed score
is far below the randomized null, the operators share more aligned
low-ell structure than expected from their per-coefficient amplitudes
alone.

Allowed claim:

> The observed operator-residue score is compared against a phase-randomized
> coefficient-level null.

Forbidden claim:

> This null alone proves AOC, a false bottom, cosmic torque, or a physical
> origin-boundary effect.
