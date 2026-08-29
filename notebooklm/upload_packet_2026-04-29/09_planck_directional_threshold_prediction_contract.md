# Planck Directional Threshold Prediction Contract

Status: pre-run prediction contract for the next Planck directional threshold
controls.

Phase: near-cousin / empirical-control bridge. This is not yet an
instantiation-grade AOC prediction, because the proof spine has not derived a
specific axis direction or apparatus-bound `K` magnitude. It is a frozen
forecast from the feasibility-band reading of the already-landed threshold
sweep.

## Source Pattern

Observed artifacts:

```text
reports/planck_operator_residue/directional_axis_galcut_sweep/
reports/planck_operator_residue/directional_axis_galcut_sweep_null/
```

The Planck fallback sweep over synthetic cuts
`0, 5, 10, 15, 20, 25, 30 deg` shows:

1. controlled G-to-A drift through `20 deg`,
2. a `20 -> 25 deg` Q-O cliff of `51.51 deg`,
3. ell=2 sector recomposition into F at `25 deg`,
4. ell=3 movement toward A/B at `25 deg`,
5. low-ell isotropic null tails:
   `jump_20_25_deg = 0.002`,
   `max_adjacent_jump_deg = 0.017`.

Interpretation before prediction: the signal is not "large Q-O at cut=25" by
itself. The signal is the adjacent recomposition under a changing mask
contract.

## Feasibility-Band Reading

The relevant SRMF chain is:

```text
TTDC / Operation        -> m=ell axis statistic
TTIE / Instrumentation  -> synthetic mask and pseudo-alm extraction
TTCS / Composition      -> four Planck component operators move coherently
TTPR / Analysis         -> null tails and allowed/forbidden claims
```

The theory-shaped claim is not that a universal threshold lives at `25 deg`.
The claim is:

> When an observer/extractor crosses a feasibility boundary, continuation
> should fail locally as an adjacent recomposition cliff rather than as a
> uniformly smooth drift.

That forecast is about the *shape* of the next control, not about proving AOC.

## Frozen Next Predictions

These predictions must be judged against future runs, not rewritten after the
fact.

### P1. Fine-Cut Localization

Run the same Planck fallback extraction with a finer synthetic cut grid over:

```text
20, 21, 22, 23, 24, 25 deg
```

Prediction:

1. The largest adjacent Q-O jump in the fine grid will occur within the
   `22 -> 25 deg` interval.
2. The transition will not distribute evenly across all five one-degree
   steps.
3. At least three of four operators will participate in the ell=2 sector
   recomposition across the transition interval.

Failure mode:

The Q-O angle changes approximately smoothly across `20..25 deg`, or the
observed `20 -> 25 deg` cliff decomposes into unrelated one-operator flips
without coherent operator participation.

### P2. High-Ell Leakage Null

Run the threshold-sweep null with Gaussian content through at least `ell=30`,
using the same synthetic cut grid.

Prediction:

1. High-ell leakage will broaden the null distribution of
   `max_adjacent_jump_deg` relative to the low-ell-only null.
2. If leakage fully explains the Planck cliff, the look-elsewhere tail for a
   `51.51 deg` jump should rise above `0.05`.
3. If the cliff is not explained by simple leakage, the look-elsewhere tail
   should remain below `0.05`.

This is a forked prediction: it does not prejudge the outcome. It names the
decision boundary before running the control.

### P3. Official-Mask Specificity

If an official Planck/common mask is available, run the same sweep logic with
the official mask family or with monotone erosions/dilations of that mask.

Prediction:

1. A purely synthetic-latitude artifact will not reproduce a comparably sharp
   adjacent cliff under official-mask morphology.
2. A genuine instrumentation-bound recomposition should reappear as a cliff in
   the official-mask family, though not necessarily at the same sky fraction or
   latitude-equivalent threshold.

Failure mode:

The cliff appears only for the hand-made latitude cuts and disappears under
official-mask morphology.

## Allowed Claims

1. This document freezes next-run predictions before the controls are run.
2. The predictions are about feasibility-boundary shape: drift versus adjacent
   recomposition cliff.
3. The high-ell leakage run has a predeclared decision boundary.

## Forbidden Claims

1. This contract proves AOC.
2. A rare threshold cliff is automatically a cosmological phase transition.
3. The `25 deg` threshold is universal.
4. A shape prediction substitutes for a theory-derived axis direction or
   apparatus-bound `K` magnitude.
5. The framework may count both outcomes of P2 as confirmation. P2 is a forked
   control: leakage-explained and leakage-resistant outcomes mean different
   things.

## Next Action

Run P1 first. It is the cheapest and tests whether the observed coarse-grid
cliff is a real localized transition or an artifact of using five-degree
steps.

## Post-Run Audit: P1

Status as of 2026-04-28: P1 supported under the fallback extractor and
synthetic latitude-cut contract.

Artifact:

```text
reports/planck_operator_residue/directional_axis_galcut_fine_sweep/
reports/planck_operator_residue/directional_axis_galcut_fine_sweep/p1_prediction_evaluation.md
```

Result:

1. Largest adjacent Q-O jump localized at `23 -> 24 deg`, inside the
   predeclared `22 -> 25 deg` interval.
2. The transition did not distribute evenly across the one-degree steps:
   `23 -> 24 deg` produced a `38.87 deg` jump.
3. Three of four operators participated in the ell=2 G-to-F sector
   recomposition across `23 -> 24 deg`.

Interpretation:

P1 supports the narrower feasibility-boundary reading of the coarse
`20 -> 25 deg` cliff. It does not promote the result to AOC evidence and does
not remove the need for high-ell leakage, official-mask, and extractor
robustness controls.

## Post-Run Audit: P2

Status as of 2026-04-28: P2 returned
`leakage_does_not_explain_under_control`.

Artifact:

```text
empirical/planck_operator_residue/directional_axis_galcut_sweep_high_ell_null.py
reports/planck_operator_residue/directional_axis_galcut_sweep_high_ell_null/
```

Result over 1000 isotropic skies with Gaussian content through `ell=30`:

| metric | observed | null median | 5-95% null | tail |
| --- | ---: | ---: | ---: | ---: |
| `jump_20_25_deg` | 51.51 | 5.02 | 0.29-22.40 | 0.004 |
| `max_adjacent_jump_deg` | 51.51 | 13.21 | 4.71-43.22 | 0.021 |

The frozen P2 decision boundary was the look-elsewhere
`max_adjacent_jump_deg` tail:

```text
tail > 0.05   -> leakage plausibly explains the cliff under this control
tail <= 0.05  -> leakage does not explain the cliff under this control
```

The observed tail is `0.021`, so simple high-ell leakage under this synthetic
mask family does not make the Planck cliff ordinary. Leakage does broaden the
null relative to the low-ell-only sweep (`0.017 -> 0.021` look-elsewhere tail),
but not enough to cross the predeclared boundary.

Interpretation:

P2 supports prioritizing P3 official-mask specificity. It does not prove AOC
and does not eliminate foregrounds, component separation, official mask
morphology, or extractor artifacts.
