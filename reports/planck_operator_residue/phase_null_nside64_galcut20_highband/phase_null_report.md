# Planck Operator-Residue Phase Null

Status: coefficient-level control, not a full CMB simulation.

Input:

```text
data\derived\planck_operator_residue\planck_lowell_alm_fallback_nside64_galcut20.csv
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
observed stability score = 0.041605
null median = 1.41407
null q05 = 1.38018
null q95 = 1.44518
fraction null <= observed = 0
n_null = 1000
```

Pair medians:

| pair | observed | null median |
| --- | ---: | ---: |
| `Commander-NILC` | 0.0447826 | 1.41542 |
| `Commander-SEVEM` | 0.0464216 | 1.41253 |
| `Commander-SMICA` | 0.0472755 | 1.41505 |
| `NILC-SEVEM` | 0.035704 | 1.41357 |
| `NILC-SMICA` | 0.0294275 | 1.41397 |
| `SEVEM-SMICA` | 0.0421518 | 1.41545 |

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
