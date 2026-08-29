# lambda_K Planck Operator-Prism Contract

Status: Episode 4 TTCS candidate map.

Phase: near-cousin / candidate theory contract, not instantiation, not an
observed-value claim.

Purpose:

This document turns the `lambda_K` invariant card into one concrete candidate
map for the Planck operator prism. It does not reinterpret Episode 3 as an AOC
prediction. It freezes a coordinate and a survival/collapse rule for the next
Planck-side theory contact.

Core rule:

```text
Kerr-side axial feasibility may only enter Planck through a predeclared
operator-prism coordinate, not through narrative resemblance to an anomaly.
```

## 1. Source Objects

From `docs/lambda_k_observable_feasibility_first_pass.md`:

```tex
h_K(\chi)
=
\frac{1-\sqrt{1-\chi^2}}{1+\sqrt{1-\chi^2}},
\qquad
\Lambda_K^{adm}(\chi,K_P)=h_K(\chi)/K_P.
```

Type:

```text
observable-feasibility scale
```

Not type:

```text
observed CMB amplitude
```

From `docs/prismatic_decomposition_rigor.md`, selected prism:

```text
operator prism
```

Operators:

```text
Commander, NILC, SEVEM, SMICA
```

## 2. Coordinate

For each operator `o`, multipole `ell`, and mask state `m`, let:

```tex
A_{o,\ell,m}
```

be the axial direction returned by the fixed directional-axis extractor. For
the next run this extractor must be stated in advance, including whether it is:

1. fallback direct quadrature,
2. canonical `healpy.map2alm`,
3. masked pseudo-alm,
4. official-mask morphology extraction.

Define the operator-axis dispersion:

```tex
D_{op}(\ell,m)
:=
\operatorname{median}_{o_i<o_j}
d_{axial}(A_{o_i,\ell,m},A_{o_j,\ell,m}).
```

Define pair-residue axes:

```tex
R_{o_i o_j,\ell,m}
```

from pairwise operator differences, and their dispersion:

```tex
D_{res}(\ell,m)
:=
\operatorname{median}_{(i,j)<(k,l)}
d_{axial}(R_{o_i o_j,\ell,m},R_{o_k o_l,\ell,m}).
```

Use the isotropic axial median reference:

```tex
D_{iso}=57^\circ
```

as a fixed normalization. Then:

```tex
S_{op}(\ell,m)
:=
1-\frac{D_{op}(\ell,m)}{D_{iso}},
```

and:

```tex
S_{res}(\ell,m)
:=
1-\frac{D_{res}(\ell,m)}{D_{iso}}.
```

The channel coordinate is:

```tex
C_{axis}(\ell,m)
:=
S_{op}(\ell,m)-S_{res}(\ell,m)
=
\frac{D_{res}(\ell,m)-D_{op}(\ell,m)}{D_{iso}}.
```

Interpretation:

`C_axis > 0` means the shared operator axis survives the operator prism more
strongly than the pair-residue axes. `C_axis <= 0` means the supposed shared
axis does not survive the operator prism better than the epistemic residual
structure.

This is a judge-free scalar coordinate.

## 3. Candidate Channel Map

The minimal Planck operator-prism channel map is sign/ordering only:

```tex
\operatorname{sign}(C_{axis})
=
\operatorname{sign}(C_P \Lambda_K^{adm}).
```

For this first contract, do not estimate `C_P` as an amplitude. Fix only the
channel orientation:

```tex
C_P > 0.
```

Theory reading:

If Kerr-side axial feasibility has a Planck operator-prism channel, it should
first show up as shared axial survival across reconstruction operators, not as
pair-residue domination.

Plain form:

```text
operator-axis survival should exceed pair-residue-axis survival.
```

This is deliberately weaker than predicting a direction, magnitude, or observed
Planck anomaly.

## 4. Next-Run Prediction

For the next canonical Planck directional rerun, predeclare:

```text
C_axis(ell=3, official-mask-base) > 0
```

and:

```text
C_axis(ell=3, official-mask-base)
remains > 0 under at least one adjacent official-mask morphology step.
```

Recommended morphology pair:

```text
base -> dilate1
```

because extreme erosions can become sky-fraction dominated and should not be
the first theory-channel test.

Success:

```text
operator-axis survival exceeds pair-residue survival at ell=3 under the
predeclared official-mask base condition and at least one adjacent morphology
step.
```

Failure:

```text
C_axis <= 0 at ell=3 under official-mask base, or C_axis becomes positive only
after changing the extraction, mask family, or normalization after seeing the
result.
```

Inconclusive:

```text
extraction fails quality controls, official-mask sky fraction becomes too
small for stable low-ell axis estimation, or the four operators cannot be
compared under the same map/mask contract.
```

## 5. Why This Is the Right First Candidate

This contract respects the current theory discipline:

1. It uses `h_K/K_P` only as a feasibility source.
2. It selects one Sprint E prism.
3. It defines a judge-free scalar.
4. It predicts survival versus collapse, not a fitted amplitude.
5. It does not reuse Pantheon+ `lambda_K`.
6. It does not claim the existing Episode 3 result was predicted.

It also respects zero-order science:

1. CMB acoustic physics is untouched.
2. CMB blackbody and standard cosmological parameters are untouched.
3. The test is about reconstruction-operator behavior at low ell.
4. A failed result kills this channel map without killing the standard CMB
   account.

## 6. Relation to Episode 3

Episode 3 already measured related coordinates using fallback extraction and
synthetic masks. Those measurements motivate this contract, but they do not
count as its confirmation.

This contract becomes live only for a future run whose extraction, mask family,
and quality controls are specified before evaluation.

Allowed retrospective statement:

```text
Episode 3 exposed the coordinate family that makes this theory contract
possible.
```

Forbidden retrospective statement:

```text
Episode 3 confirmed the lambda_K Planck operator-prism channel.
```

## 7. Required Report Shape

The future report must include:

1. extractor definition,
2. mask family and sky fractions,
3. `D_op`, `D_res`, `S_op`, `S_res`, and `C_axis`,
4. quality-control failures,
5. success/failure/inconclusive verdict,
6. allowed claims,
7. forbidden claims,
8. provenance paths.

It must also state raw angles. Do not report only normalized scores.

## Allowed Claims

1. This document defines a Planck operator-prism candidate map for the
   `lambda_K` lane.
2. The map predicts an ordinal survival relation:
   `C_axis(ell=3, official-mask-base) > 0` for a future canonical run.
3. The coordinate is judge-free and does not require fitting a Planck amplitude.
4. Failure of this contract would count against this Planck channel map, not
   against all AOC or all Kerr near-cousin work.

## Forbidden Claims

1. This document predicts the sky direction of the Planck low-ell axis.
2. This document predicts the Episode 3 results after the fact.
3. This document derives an observed `lambda_K` amplitude.
4. `C_axis > 0` confirms AOC.
5. Failure of this channel map refutes AOC, LambdaCDM, or Kerr physics.

