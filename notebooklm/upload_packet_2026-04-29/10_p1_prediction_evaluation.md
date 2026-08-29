# P1 Fine-Cut Prediction Evaluation

Status: post-run audit of `P1` from
`docs/planck_directional_threshold_prediction_contract.md`.

## Frozen Prediction

P1 predicted that a fine synthetic-cut sweep over:

```text
20, 21, 22, 23, 24, 25 deg
```

would show:

1. the largest adjacent Q-O jump inside the `22 -> 25 deg` interval,
2. a transition not evenly distributed across all one-degree steps,
3. at least three of four operators participating in the ell=2 sector
   recomposition across the transition interval.

## Result

| adjacent cut step | Q-O change |
| --- | ---: |
| `20 -> 21` | `3.06 deg` |
| `21 -> 22` | `1.07 deg` |
| `22 -> 23` | `7.40 deg` |
| `23 -> 24` | `38.87 deg` |
| `24 -> 25` | `1.10 deg` |

The largest adjacent jump is `23 -> 24 deg`, inside the predeclared
`22 -> 25 deg` localization interval.

Ell=2 sector recomposition across `23 -> 24 deg`:

| operator | cut 23 ell=2 note | cut 24 ell=2 note | sector changed? |
| --- | --- | --- | --- |
| Commander | G | F | yes |
| NILC | G | F | yes |
| SEVEM | G | G | no |
| SMICA | G | F | yes |

Three of four operators participate in the ell=2 G-to-F recomposition.

## Verdict

P1 is supported under the fallback extractor and synthetic latitude-cut
contract.

This does not prove AOC. It supports the narrower interpretation that the
coarse `20 -> 25 deg` cliff is not merely an artifact of five-degree binning:
the recomposition localizes sharply at `23 -> 24 deg` in the fine sweep and
has coherent multi-operator participation.

## Remaining Risk

1. The extraction is still the fallback direct pseudo-alm pipeline.
2. The mask family is still synthetic latitude cuts, not official Planck mask
   morphology.
3. The axis grid is finite, so exact transition thresholds are quantized by
   the search resolution.
4. High-ell leakage and component-separation physics are not included in this
   P1 check.

