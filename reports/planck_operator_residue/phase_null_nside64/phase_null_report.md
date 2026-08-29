# Planck Operator-Residue Phase Null

Status: coefficient-level control, not a full CMB simulation.

Input:

```text
data\derived\planck_operator_residue\planck_lowell_alm_fallback_nside64.csv
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
observed stability score = 0.337761
null median = 1.41407
null q05 = 1.38699
null q95 = 1.44149
fraction null <= observed = 0
n_null = 1000
```

Pair medians:

| pair | observed | null median |
| --- | ---: | ---: |
| `Commander-NILC` | 0.273684 | 1.41249 |
| `Commander-SEVEM` | 0.460631 | 1.41335 |
| `Commander-SMICA` | 0.251256 | 1.41535 |
| `NILC-SEVEM` | 0.498159 | 1.41434 |
| `NILC-SMICA` | 0.0920114 | 1.4129 |
| `SEVEM-SMICA` | 0.48244 | 1.41265 |

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
