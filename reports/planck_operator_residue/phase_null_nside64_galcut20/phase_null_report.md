# Planck Operator-Residue Phase Null

Status: coefficient-level control, not a full CMB simulation.

Input:

```text
data\derived\planck_operator_residue\planck_lowell_alm_fallback_nside64_galcut20.csv
```

Band:

```text
2 <= ell <= 30
```

Null:

For each operator and coefficient, preserve `|a_lm|` and randomize phase
independently for `m > 0`; randomly sign-flip `m = 0`.

Headline:

```text
observed stability score = 0.0412436
null median = 1.41421
null q05 = 1.38425
null q95 = 1.44413
fraction null <= observed = 0
n_null = 1000
```

Pair medians:

| pair | observed | null median |
| --- | ---: | ---: |
| `Commander-NILC` | 0.0447651 | 1.41399 |
| `Commander-SEVEM` | 0.046654 | 1.41325 |
| `Commander-SMICA` | 0.0461555 | 1.41605 |
| `NILC-SEVEM` | 0.0360027 | 1.41496 |
| `NILC-SMICA` | 0.0289414 | 1.41296 |
| `SEVEM-SMICA` | 0.0422639 | 1.4135 |

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
