# Planck Operator-Residue Phase Null

Status: coefficient-level control, not a full CMB simulation.

Input:

```text
data\derived\planck_operator_residue\planck_lowell_alm_fallback_nside64.csv
```

Band:

```text
2 <= ell <= 10
```

Null:

For each operator and coefficient, preserve `|a_lm|` and randomize phase
independently for `m > 0`; randomly sign-flip `m = 0`.

Headline:

```text
observed stability score = 0.246507
null median = 1.41623
null q05 = 1.33193
null q95 = 1.49252
fraction null <= observed = 0
n_null = 1000
```

Pair medians:

| pair | observed | null median |
| --- | ---: | ---: |
| `Commander-NILC` | 0.209266 | 1.41481 |
| `Commander-SEVEM` | 0.340659 | 1.4131 |
| `Commander-SMICA` | 0.143128 | 1.42062 |
| `NILC-SEVEM` | 0.347643 | 1.41962 |
| `NILC-SMICA` | 0.0639116 | 1.41124 |
| `SEVEM-SMICA` | 0.356939 | 1.40789 |

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
