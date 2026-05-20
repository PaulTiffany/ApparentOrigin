# Cacophony-to-K Bridge

Status: working transfer note.

Purpose:

Use the Cacophony rebuttal machinery to strengthen Apparent-Origin Cosmology's
`K` theory without pretending that LLM constraint satisfaction and cosmological
reconstruction are the same domain.

## Source Context

This note draws on rebuttal-prep templates in:

```text
C:\src\ICML_2026_Template\rebuttal\templates
```

Highest-signal templates:

1. `zero_order_framing.md`
2. `routing_not_staging.md`
3. `staging_regression.md`
4. `hard_negatives.md`
5. `novelty.md`
6. `constrained_decoding.md`

## Core Transfer

Cacophony's mature move is not "the math is new." Its mature move is:

> Classical geometry becomes empirically useful only after an operational
> interface is defined, calibrated, and tested.

For Cacophony, that interface is the generative oracle:

```text
bounded displacement per query, calibrated query cost, online violation
detection, zero-query feasibility surrogate, and routing policy.
```

For AOC, the analogous interface must be a reconstruction oracle:

```text
finite instrument access, finite inference budget, distinguishability
threshold, atlas-coherence check, and pipeline-dependent reconstruction floor.
```

The transfer is methodological, not literal.

## Translation Table

| Cacophony term | AOC/K-theory analogue | Transfer status |
| --- | --- | --- |
| Generative oracle | Reconstruction oracle | Direct methodological analogue |
| Query cost | Observation/inference cost | Direct methodological analogue |
| Displacement budget `L` | Reconstruction budget `K` or dynamic range | Analogue only; not same variable |
| `rho_hat` feasibility surrogate | Pre-fit pipeline-risk surrogate | Future target |
| Feasibility cliff | Reconstruction floor / apparent-origin surface | Analogue only |
| Routing | Pipeline/strategy selection | Direct methodological analogue |
| Staging | Additional observations, priors, calibration, tools, model passes | Direct analogue with different costs |
| Hard negatives | False alarms in pipeline-risk estimates | Direct analogue |
| Constrained decoding | Syntactic/model-form enforcement | Analogue: priors and parameterization do not remove geometric/information cost |
| Regret vs oracle | Performance vs best pipeline selected after the fact | Future target |

## What Does Not Transfer

Do not transfer these as claims:

1. Cacophony's calibrated `L` value.
2. Cacophony's `rho_hat` values or thresholds.
3. LLM pass rates.
4. The exact three-regime `rho` cutoffs.
5. Any claim that cosmological data must exhibit the same cliff shape.

What transfers is the discipline:

1. define the oracle,
2. define cost,
3. define distinguishability,
4. calibrate the interface,
5. test controls,
6. route rather than always stage,
7. treat surrogates as screening statistics, not verdicts.

## AOC Reconstruction Oracle

Define a reconstruction pipeline:

```tex
\mathcal P = (\mathcal I, \mathcal M, \mathcal R, \mathcal C),
```

where:

```tex
\mathcal I \quad \text{instrument stack}
\mathcal M \quad \text{model class}
\mathcal R \quad \text{reduction/inference procedure}
\mathcal C \quad \text{calibration, priors, and controls}.
```

The pipeline acts as a reconstruction oracle:

```tex
\mathcal O_{\mathcal P}: \text{data stream} \to \widehat{y},
```

where the first FRW chart uses:

```tex
y(t) := \frac{1}{a(t)} = 1+z.
```

The apparatus-bound `K` is then the largest reliably reconstructible value of
`y` under the pipeline:

```tex
K_{\mathcal P,\tau}
:=
\sup
\left\{
y :
\operatorname{Rel}_{\mathcal P}(y) \ge \tau
\ \text{and}\
\operatorname{Atlas}_{\mathcal P}(y) \le \gamma
\right\}.
```

Here:

1. `Rel_P(y)` is a reliability or distinguishability score.
2. `tau` is the required reliability threshold.
3. `Atlas_P(y)` measures chart-transition failure, model degeneracy, or
   incoherent reconstruction.
4. `gamma` is the maximum tolerated atlas-fracture score.

This makes `K` a property of a concrete pipeline, not a free metaphysical knob.

## Distinguishability Definitions

There are several viable definitions of `Rel_P(y)`. The safest first options
are:

### Relative-Error Reliability

If the pipeline estimates `y` with uncertainty `sigma_P(y)`, define:

```tex
\operatorname{Rel}_{\mathcal P}(y)
:=
\frac{y}{\sigma_{\mathcal P}(y)}.
```

Then:

```tex
K_{\mathcal P,\tau}
=
\sup \{ y : y/\sigma_{\mathcal P}(y) \ge \tau \}.
```

Equivalently, for an allowed relative error `eta`:

```tex
K_{\mathcal P,\eta}
=
\sup \{ y : \sigma_{\mathcal P}(y)/y \le \eta \}.
```

### Fisher-Information Reliability

If the pipeline has Fisher information `I_P(y)` for `y`, then a local
distinguishability condition can be:

```tex
\sqrt{I_{\mathcal P}(y)} \, \Delta y \ge \tau.
```

This yields:

```tex
K_{\mathcal P,\tau,\Delta y}
=
\sup \{ y : \sqrt{I_{\mathcal P}(y)} \Delta y \ge \tau \}.
```

### Atlas-Coherence Reliability

If multiple charts or probes estimate the same boundary quantity, require
transition coherence:

```tex
\operatorname{Atlas}_{\mathcal P}(y)
:=
\max_{i,j}
d\!\left(
T_{ij}\widehat y_i,
\widehat y_j
\right).
```

Then include:

```tex
\operatorname{Atlas}_{\mathcal P}(y) \le \gamma.
```

This prevents mistaking failed chart composition for a legitimate
reconstruction horizon.

## First AOC K Claim Worth Testing

In the first FRW chart:

```tex
\kappa_O^{access}(t)=1/a(t)=y(t).
```

If:

```tex
K_{\mathcal P,\tau}
=
\sup \{ y : \operatorname{Rel}_{\mathcal P}(y)\ge \tau \},
```

then the apparent-origin surface is:

```tex
t_{K(\mathcal P)}
=
a^{-1}\!\left(K_{\mathcal P,\tau}^{-1}\right).
```

For:

```tex
a(t)=A t^\alpha,
```

this becomes:

```tex
t_{K(\mathcal P)}
=
(A K_{\mathcal P,\tau})^{-1/\alpha}.
```

This is the cleanest native apparatus-bound statement so far:

> The apparent-origin surface is the time at which a concrete reconstruction
> pipeline runs out of reliable dynamic range on inverse scale factor.

## Routing, Not Always-Staging

Cacophony's staging result transfers directly as a warning:

> More staging is not automatically better. The value is knowing when to stage.

For AOC:

1. low-risk regimes should use the simplest reconstruction pipeline,
2. moderate-risk regimes should add calibration, probes, priors, or cross-checks,
3. high-risk regimes should reject, defer, or mark the boundary as unresolved.

This prevents "throw more instruments/models at it" from becoming an
uncontrolled version of always-staging.

## Screening Statistics, Not Verdicts

Cacophony's `rho_hat` is a screening statistic, not a conflict verdict. The AOC
analogue should follow the same rule.

Candidate AOC screening features:

1. relative uncertainty growth,
2. foreground/model degeneracy,
3. cross-pipeline disagreement,
4. prior sensitivity,
5. chart-transition residual,
6. extrapolation distance beyond calibration data,
7. information saturation or entropy bound proximity.

These should trigger controls, not conclusions.

False positives are acceptable if they cause extra checks. False negatives are
dangerous if they let a fractured atlas masquerade as a horizon.

## Constrained-Decoding Analogue

Cacophony's constrained-decoding lesson:

> Syntactic restriction can enforce form but cannot remove geometric conflict.

AOC analogue:

> Model priors, parameterizations, or coordinate choices can enforce smooth
> forms, but they do not by themselves remove information limits,
> distinguishability limits, or atlas-fracture risk.

This matters for `K`: a pipeline may produce a clean extrapolated `a(t)` curve
past the data-supported region. That smoothness is not evidence that `K` has
increased unless reliability and atlas-coherence conditions also improve.

## Immediate Work Program

1. Choose a simple observable proxy for `y=1/a=1+z`.
2. Define `sigma_P(y)` for a toy or real pipeline.
3. Choose reliability threshold `tau` or relative-error threshold `eta`.
4. Compute `K_P`.
5. Map `K_P` to `t_K`.
6. Compare two pipelines and show whether `t_K` differs.
7. Add an atlas-coherence control.
8. Only then discuss empirical cosmology.

## Canonical Guardrail

The bridge from Cacophony to AOC is:

> operationalize the bound through a calibrated observer interface.

It is not:

> LLM constraint cliffs prove the Big Bang is an observer artifact.

