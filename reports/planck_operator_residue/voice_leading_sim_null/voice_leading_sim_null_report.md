# Voice-Leading Sim-Null (Sprint D)

Status: instantiation-class null calibration. The detector contract is
frozen from Episode 2; this is a computational measurement, not an AOC
prediction.

This report calibrates the Episode 2 voice-leading finding — all 6/6
voice pairs of the four Planck PR3 component-separation algorithms
(Commander, NILC, SEVEM, SMICA) triggered the parallel-fifths
forbidden-motion analog at ell=3 under the synthetic galcut20 mask
transition — by asking how often that block-motion pattern arises in
ΛCDM low-ell realizations under matched detector parameters.

Phase tag: instantiation-class for the null computation; the surrogate
operator-noise model is a methodological choice documented and swept,
not a physics claim. Detector parameters (parallel-fifths Δ-match 5°,
rotation-axis-align 15°, min motion 3°; hidden-unison arrival 5°,
starting gap 15°) are imported verbatim from
`empirical/planck_operator_residue/counterpoint_voice_leading.py`.

## Conversion Contract

| source quantity | sim-null operationalization | preserved | discarded |
| --- | --- | --- | --- |
| Planck PR3 component-separation algorithm (Commander, NILC, SEVEM, SMICA) | one of four "surrogate pipelines"; independent Gaussian noise draw added to the same underlying ΛCDM low-ell sky | identity-as-distinguishable-voice | actual algorithmic structure (parametric pixel modeling, ILC, template-fitting), foreground residuals |
| underlying CMB sky | isotropic ΛCDM low-ell realization via flat-Sachs-Wolfe scaling at ell∈{2,3} | cosmic-variance-level Gaussian fluctuations at the relevant multipoles | beam, detector noise, foregrounds, high-ell leakage, time-evolution |
| mask transition | piece-time: unmasked pseudo-alms → galcut20 pseudo-alms (or two independent noise re-draws on same sky for the no-mask baseline) | per-pipeline axis motion under the geometric transformation | f_sky-dependent power redistribution beyond pseudo-alm extraction |
| Episode 2 forbidden-motion detector | imported verbatim from `counterpoint_voice_leading.py`; constants frozen | parallel-fifths/voice-crossing/hidden-unison rule structure | calibration of the rule cutoffs against any field-standard p-value |

## Methodology

For each of 1000 realizations:

1. Draw a ΛCDM low-ell sky `alms` via `draw_lowell_sky` (flat
   Sachs-Wolfe scaling).
2. Synthesize a HEALPix nside=64 map.
3. **Apply mask if requested**: for `mask=galcut20`, set pixels with
   `|b| < 20°` to NaN before pseudo-alm extraction. For `mask=none`,
   no mask; the "transition" is two independent noise re-draws on the
   same underlying sky (noise-only baseline).
4. Extract pseudo-alms at the requested ell.
5. **Build four surrogate pipelines**: add four independent Gaussian
   operator-noise draws to the same underlying-sky pseudo-alms.
   Calibration: `noise_sigma_per_alm = noise_scale * 0.5 *
   RMS(unmasked alms at ell)`. The `noise_scale` is swept at 0.5, 1.0,
   2.0 to characterize sensitivity.
6. For each surrogate pipeline, find the m=l-maximizing axis at the
   requested ell.
7. Compute voice-leading distances and rotation axes for the
   transition.
8. Run `detect_parallel_fifths`, `detect_voice_crossing`,
   `detect_hidden_unison` on the axes dict.
9. Record per-realization: pair-count for each rule, per-pipeline Δ,
   median rotation-axis dispersion across the four surrogates.

The Episode 2 observed Planck values (input to the percentile
readout): **6/6 voice pairs trigger parallel-fifths at ell=3 under
galcut20**, with median rotation-axis dispersion ~12° across the four
pipelines and median voice-leading Δ ≈ 22.5° at ell=3.

## Main Results — noise_scale = 1.0 (1000 realizations each)

| condition | P(0 pairs) | P(1) | P(2) | P(3) | P(4) | P(5) | P(6) | P(≥6) | obs Planck | percentile | median Δ | median rot-axis disp |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| galcut20, ell=3 | 71.3% | 24.2% | 2.8% | 1.4% | 0.3% | 0.0% | 0.0% | **0.0%** | 6 | **100.0** | 15.9° | 42.8° |
| none, ell=3 | 75.7% | 22.3% | 1.6% | 0.4% | 0.0% | 0.0% | 0.0% | 0.0% | 6 | 100.0 | 21.9° | 38.3° |
| galcut20, ell=2 | 70.6% | 23.8% | 4.0% | 1.2% | 0.4% | 0.0% | 0.0% | 0.0% | 2 | (bulk) | 18.7° | 37.8° |
| none, ell=2 | 80.0% | 18.6% | 1.2% | 0.1% | 0.1% | 0.0% | 0.0% | 0.0% | 2 | (bulk) | 23.4° | 41.6° |

The Episode 2 observed value of **6/6 pairs at ell=3 under galcut20**
does not occur in 1000 ΛCDM realizations under either mask condition
at the default noise scale. The observed value sits at the 100th
percentile of the null distribution; raw rate < 0.1%.

The Episode 2 ell=2 value (2/6 pairs) sits in the bulk of the
distribution (P(2)=4.0% under galcut20, cumulative P(≤2)=98.4%) — the
ell=2 finding is not anomalous against this null. This matches the
parent counterpoint report's read that ell=2 is "partly independent"
with SEVEM as outlier, and that the headline anomaly is specifically
at ell=3.

## Sensitivity Sweep — ell=3 across noise scales (1000 realizations each)

The default surrogate noise calibration (1.0x) produces median
rotation-axis dispersion of 42.8° (galcut20) and 38.3° (no-mask), much
higher than the Episode 2 observed Planck value of ~12°. A smaller
noise scale brings the surrogate dispersion closer to the observed
range. The 0.5x noise scale produces dispersion of 24.1° (galcut20),
still larger than 12° but within a factor of 2.

| condition | noise | P(≥6 pairs) | observed percentile | median Δ | median rot-axis disp |
| --- | ---: | ---: | ---: | ---: | ---: |
| galcut20 | 0.5x | **1.4%** | 98.6 | 14.2° | 24.1° |
| galcut20 | 1.0x | 0.0% | 100.0 | 15.9° | 42.8° |
| galcut20 | 2.0x | 0.0% | 100.0 | 15.9° | 55.2° |
| none | 0.5x | 0.2% | 99.8 | 9.7° | 37.2° |
| none | 1.0x | 0.0% | 100.0 | 21.9° | 38.3° |
| none | 2.0x | 0.0% | 100.0 | 42.9° | 48.4° |

Two readings emerge from the sweep:

1. **The headline survives across noise scales tested.** The Episode
   2 observed 6/6-pair pattern at ell=3 under galcut20 sits at the
   98.6th percentile or higher across all three noise scales.
2. **The mask contributes meaningfully to lockstep motion.** At every
   noise scale, the galcut20 condition produces more ≥6-pair events
   than the no-mask baseline. At noise=0.5x the ratio is 7×
   (1.4% vs 0.2%); at noise=1.0x and 2.0x the no-mask rate is at the
   detector floor and no comparison is possible. The mask geometry
   alone, in this surrogate model, does push the four pipelines toward
   correlated axis motion — but not all the way to the observed
   lockstep.

## Histogram

`voice_leading_sim_null_histogram_ell3.png` shows pair-count
distributions for ell=3 main runs (top row) and the noise sweep at
ell=3 (bottom row). The observed Planck value (6) is marked as a red
dashed vertical line; in every panel it sits beyond the rightmost
non-empty bin of the null distribution, with the partial exception of
the noise=0.5x galcut20 panel where 1.4% of realizations reach the 6
bin.

## Allowed Claims

1. Under ΛCDM low-ell cosmic variance with the documented surrogate
   operator-noise model, the all-six-pair parallel-fifths configuration
   at ell=3 under galcut20 occurs in 0.0% (noise=1.0x and 2.0x) to 1.4%
   (noise=0.5x) of 1000 realizations. The Episode 2 observed Planck
   result sits at the 98.6-100.0 percentile of this null distribution
   depending on noise calibration.
2. The mask geometry alone (galcut20 applied to the same underlying
   sky) produces more frequent ≥6-pair events than the noise-only
   baseline at every noise scale tested, by approximately a factor of
   7 at noise=0.5x. Mask contribution to surrogate lockstep is real
   but, in this model, insufficient to reproduce the observed pattern.
3. The Episode 2 ell=2 observed value (2/6 pairs) is not anomalous
   against this null and lies in the bulk of the distribution
   (cumulative P(≤2) ≈ 98%).
4. Detector parameters and surrogate-pipeline construction match the
   Episode 2 analysis on the operator-axis side (m=l-maximizing axis,
   same forbidden-motion thresholds), making the null and the
   observation directly comparable in the parallel-fifths-pair-count
   coordinate.

## Forbidden Claims

1. The null does not refute the Pipeline Independence Postulate. This
   tests *surrogate* pipelines built from independent Gaussian noise
   draws on a shared underlying sky, not the four real Planck PR3
   component-separation algorithms.
2. ΛCDM is not ruled out. The null calibrates a specific lockstep
   configuration of a specific detector under a specific surrogate
   noise model; it does not bind ΛCDM.
3. AOC is not confirmed. This is null calibration, not an
   AOC-positive prediction. The Episode 4 work that would land an
   AOC-positive prediction is the Kerr-interior `λ_K` derivation; see
   `docs/lambda_k_kerr_interior_strategy.md`.
4. The 100.0 percentile readout at noise=1.0x is not a literal
   probability; with 1000 realizations the upper bound on the rate is
   ~0.001 (3/n if zero events were observed), i.e. the lower bound on
   the percentile is ~99.7. State raw rate alongside percentile to
   avoid implying a sub-permille certainty.
5. The detector thresholds are not p-values. They are first-pass
   forbidden-motion rule cutoffs adapted from classical counterpoint;
   their probability under the null is what *this report measures*.

## Limitations

1. **Surrogate pipelines are independent Gaussian noise draws on a
   shared underlying sky; not real Planck component-separation
   operators.** The four actual algorithms differ in foreground
   handling and beam treatment; their joint behavior under masking
   could plausibly produce more lockstep motion than this null
   captures (which would weaken the anomaly) or less (which would
   strengthen it).
2. **Low-ell-only sky**: ell ∈ {2, 3} only. No high-ell leakage, no
   foregrounds, no beam, no detector noise. The P2 high-ell-leakage
   null in `reports/planck_operator_residue/directional_axis_galcut_sweep_high_ell_null/`
   already showed leakage broadens the null modestly but does not
   close the gap; this report inherits that finding's scope.
3. **Synthetic galactic cut |b|>20°**, not the official Planck common
   mask. The P3 official-mask morphology sweep
   (`reports/planck_operator_residue/directional_axis_official_mask_morphology/`)
   showed the cliff shape preserves under the morphology family; this
   sim-null does not re-test that.
4. **Detector thresholds are uncalibrated rule cutoffs imported from
   Episode 2**; they are not p-values. The probability the observed
   configuration lies in the deep tail under the null is what this
   measures.
5. **The "observed pair count" for the percentile readout is the
   Episode 2 same-realization measurement on real Planck data**; this
   null does not invert that to a Planck-likelihood claim.

## Outputs

- `voice_leading_sim_null_report.md` (this document)
- `voice_leading_sim_null_histogram_ell3.png` (4-panel histogram)
- Main runs (noise_scale=1.0):
  - `main/galcut20_ell3/voice_leading_sim_null_summary.json` and `_samples.csv`
  - `main/none_ell3/...`
  - `main/galcut20_ell2/...`
  - `main/none_ell2/...`
- Sensitivity sweep (ell=3):
  - `sensitivity/galcut20_ell3_n0p5/...`
  - `sensitivity/galcut20_ell3_n2p0/...`
  - `sensitivity/none_ell3_n0p5/...`
  - `sensitivity/none_ell3_n2p0/...`

Provenance:

```text
empirical/planck_operator_residue/voice_leading_sim_null.py
empirical/planck_operator_residue/plot_sim_null_histograms.py
```
