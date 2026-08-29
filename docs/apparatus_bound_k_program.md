# Apparatus-Bound K Program

Status: next technical program for AOC.

Purpose:

Turn `K` from a free finite reconstruction budget into a pipeline-estimated
quantity.

## 1. Starting Point

The first FRW observer-quotient chart uses:

```tex
\Omega_O(t)=a(t)^2,
\qquad
\kappa_O^{access}(t)=\Omega_O(t)^{-1/2}=1/a(t).
```

Let:

```tex
y(t):=1/a(t).
```

For standard redshift notation:

```tex
y=1+z.
```

The chart currently defines a finite observer by:

```tex
y(t) \le K.
```

The missing work is to define `K` from an actual reconstruction pipeline.

## 2. Pipeline Definition

Let:

```tex
\mathcal P=(\mathcal I,\mathcal M,\mathcal R,\mathcal C)
```

where:

1. `I` is the instrument stack,
2. `M` is the model family,
3. `R` is the reduction/inference procedure,
4. `C` is calibration, priors, and controls.

The pipeline estimates:

```tex
\widehat y_{\mathcal P}
```

with uncertainty:

```tex
\sigma_{\mathcal P}(y).
```

## 3. First Definition of Apparatus-Bound K

For a required relative accuracy `eta`, define:

```tex
K_{\mathcal P,\eta}
:=
\sup
\left\{
y :
\frac{\sigma_{\mathcal P}(y)}{y}\le \eta
\right\}.
```

Equivalently, for a reliability threshold `tau`:

```tex
K_{\mathcal P,\tau}
:=
\sup
\left\{
y :
\frac{y}{\sigma_{\mathcal P}(y)}\ge \tau
\right\}.
```

Interpretation:

> `K` is the deepest inverse-scale-factor value the pipeline can reconstruct
> with accepted reliability.

This is not yet a claim about physical ontology. It is a claim about pipeline
dynamic range.

## 4. Mapping K to an Apparent-Origin Surface

For:

```tex
a(t)=A t^\alpha,
```

we have:

```tex
y(t)=A^{-1}t^{-\alpha}.
```

The pipeline-specific reconstruction floor satisfies:

```tex
y(t_K)=K_{\mathcal P}.
```

Therefore:

```tex
t_K(\mathcal P)
=
(A K_{\mathcal P})^{-1/\alpha}.
```

For a perfect fluid with:

```tex
\alpha=\frac{2}{3(1+w)},
```

this is:

```tex
t_K(\mathcal P)
=
(A K_{\mathcal P})^{-3(1+w)/2}.
```

## 5. Minimal Toy Pipeline

The first toy pipeline should not use real cosmological data. It should test the
formal mechanism.

Let uncertainty grow with inverse scale factor:

```tex
\sigma_{\mathcal P}(y)
=
\sigma_0 y^p,
\qquad
p>1.
```

Then relative error is:

```tex
\frac{\sigma_{\mathcal P}(y)}{y}
=
\sigma_0 y^{p-1}.
```

The threshold condition:

```tex
\sigma_0 y^{p-1}\le \eta
```

gives:

```tex
K_{\mathcal P,\eta}
=
\left(\frac{\eta}{\sigma_0}\right)^{1/(p-1)}.
```

Then:

```tex
t_K(\mathcal P)
=
A^{-1/\alpha}
\left(\frac{\eta}{\sigma_0}\right)^{-1/(\alpha(p-1))}.
```

This toy model gives a concrete first demonstration:

> improving instrument noise `sigma_0` lowers the apparent-origin time `t_K`.

## 6. Comparing Two Pipelines

Let two pipelines have:

```tex
\sigma_{\mathcal P_1}(y)=\sigma_{0,1}y^p,
\qquad
\sigma_{\mathcal P_2}(y)=\sigma_{0,2}y^p.
```

Then:

```tex
\frac{K_{\mathcal P_2}}{K_{\mathcal P_1}}
=
\left(\frac{\sigma_{0,1}}{\sigma_{0,2}}\right)^{1/(p-1)}.
```

and:

```tex
\frac{t_K(\mathcal P_2)}{t_K(\mathcal P_1)}
=
\left(
\frac{K_{\mathcal P_2}}{K_{\mathcal P_1}}
\right)^{-1/\alpha}.
```

If `sigma_{0,2}<sigma_{0,1}`, then:

```tex
K_{\mathcal P_2}>K_{\mathcal P_1},
\qquad
t_K(\mathcal P_2)<t_K(\mathcal P_1).
```

Better reconstruction capacity pushes the apparent-origin surface deeper.

## 7. Atlas-Coherence Control

Reliability alone is not enough. A pipeline can be precise and wrong if its
charts do not compose.

Let multiple reconstruction charts estimate `y`:

```tex
\widehat y_1,\ldots,\widehat y_m.
```

Define:

```tex
\Gamma_{\mathcal P}(y)
:=
\max_{i,j}
\frac{
\left|T_{ij}\widehat y_i-\widehat y_j\right|
}{
\sqrt{\sigma_i(y)^2+\sigma_j(y)^2}
}.
```

Require:

```tex
\Gamma_{\mathcal P}(y)\le \gamma.
```

Then the stronger apparatus-bound definition is:

```tex
K_{\mathcal P,\eta,\gamma}
:=
\sup
\left\{
y :
\frac{\sigma_{\mathcal P}(y)}{y}\le\eta
\ \text{and}\
\Gamma_{\mathcal P}(y)\le\gamma
\right\}.
```

This distinguishes a coherent reconstruction horizon from atlas fracture.

## 8. Cacophony Discipline

The Cacophony transfer is methodological:

1. Define the oracle/interface.
2. Calibrate the budget.
3. Treat surrogates as screening statistics.
4. Route rather than always stage.
5. Measure failure modes.

For AOC:

1. `K` should be calibrated from pipeline reliability.
2. pipeline-risk features should trigger controls, not verdicts.
3. extra modeling should not be treated as free capacity.
4. smooth extrapolation should not be confused with reliable reconstruction.

## 9. First Implementation Task

Build a toy script with parameters:

```tex
A,\alpha,\sigma_0,p,\eta,\gamma.
```

It should compute:

1. `K_P`,
2. `t_K(P)`,
3. the effect of lowering `sigma_0`,
4. a two-pipeline comparison,
5. an optional atlas-fracture cutoff.

This will not be evidence for AOC. It will be the first executable
apparatus-bound `K` calculation.

