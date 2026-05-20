# lambda_K Observable-Feasibility First Pass

Status: Episode 4 theory-side first pass.

Phase: near-cousin / feasibility derivation, not observed-number derivation,
not instantiation.

Purpose:

This document takes the first theory-side step after
`docs/lambda_k_kerr_interior_strategy.md`. It uses the Kerr-interior
near-cousin to derive a dimensionless feasibility kernel and a finite-budget
interior floor chart. It does **not** derive an observed `lambda_K` value.

The load-bearing correction is the type distinction:

```text
observable / feasible structure != observed value
```

Do not force `lambda_K` directly into "what did Planck, Pantheon+, or DESI
observe?" before specifying what the near-cousin plus apparatus-bound pipeline
make observable in the first place.

## 1. Type Guard: Observable Versus Observed

Use three levels:

| level | meaning | example |
| --- | --- | --- |
| feasible | allowed by the geometry and observer-access structure | a Kerr spin-horizon kernel exists in the near-cousin |
| observable | survives a specified apparatus/pipeline feasibility band | a Planck operator-residue coordinate is measurable under finite `K_P` |
| observed | estimated in a dataset or measurement record | a pair-count, distance residual, or fitted amplitude |

The corrected chain is:

```text
near-cousin geometry
-> feasible/admissible structure
-> apparatus-bound observable map
-> observed dataset value
```

The forbidden shortcut is:

```text
near-cousin geometry
-> observed value
```

This is the same discipline as the feasibility-band rule:

```text
compose only where the operator remains measurable
```

and the same discipline as the observable-map program:

```text
each observable must earn its own map
```

## 2. Kerr Horizon Kernel

Work in geometrized units `G=c=1`. Let

```tex
\chi := a/M,
\qquad 0 \le \chi \le 1,
```

be the dimensionless Kerr spin. The outer and inner horizon radii are:

```tex
r_\pm = M\left(1 \pm \sqrt{1-\chi^2}\right).
```

Define:

```tex
s(\chi) := \sqrt{1-\chi^2}.
```

The simplest dimensionless two-horizon kernel is the inner-to-outer horizon
ratio:

```tex
h_K(\chi)
:=
\frac{r_-}{r_+}
=
\frac{1-s(\chi)}{1+s(\chi)}.
```

Properties:

```tex
h_K(0)=0,
\qquad
h_K(1)=1,
\qquad
h_K(\chi)\sim \chi^2/4 \quad \text{as } \chi\to 0.
```

Interpretation:

`h_K` measures how strongly the inner horizon participates in the two-horizon
structure. It is zero in the Schwarzschild limit and maximal in the extremal
spin limit.

This is a feasible-structure kernel. It is not an observed amplitude.

The complementary normalized horizon-gap kernel is:

```tex
g_K(\chi)
:=
\frac{r_+-r_-}{r_+}
=
\frac{2s(\chi)}{1+s(\chi)}
=
1-h_K(\chi).
```

`h_K` measures inner-horizon prominence. `g_K` measures normalized gap
thickness between horizons.

## 3. Finite-Budget Interior Floor Chart

The FRW observer-quotient chart uses:

```tex
\Omega_O(t)=a(t)^2,
\qquad
\kappa_O^{access}(t)=\Omega_O(t)^{-1/2}.
```

A direct FRW lift to Kerr is not available from the seed alone. Kerr interior
coordinates are anisotropic, and a Boyer-Lindquist radius is not an FRW scale
factor. Treating Kerr as the territory at this point would violate phase
respect.

What can be done safely is a horizon-normal interior chart.

For `r_- < r < r_+`, define the normalized interior coordinate:

```tex
u
:=
\frac{r-r_-}{r_+-r_-},
\qquad
0<u<1.
```

Candidate access capacity:

```tex
\Omega_K(u):=u^2.
```

Then:

```tex
\kappa_K^{access}(u)
=
\Omega_K(u)^{-1/2}
=
u^{-1}.
```

For finite apparatus-bound budget `K_P`, the deepest reconstructible interior
coordinate satisfies:

```tex
u_K = K_P^{-1}.
```

Thus:

```tex
r_K(P,\chi)
=
r_- + \frac{r_+-r_-}{K_P}.
```

Normalized by the outer horizon:

```tex
\frac{r_K-r_-}{r_+}
=
\frac{g_K(\chi)}{K_P}.
```

Interpretation:

Finite `K_P` prevents the observer pipeline from resolving arbitrarily close
to the inner-horizon boundary in this chart. Increasing `K_P` moves the
reconstruction floor toward `r_-`.

What this establishes:

```text
Kerr near-cousin + finite K_P -> admissible interior reconstruction floor
```

What it does not establish:

```text
Kerr near-cousin + finite K_P -> observed cosmological deformation amplitude
```

## 4. Admissible lambda_K Scale

The first type-safe object is not an observed `lambda_K`. It is an admissible
scale:

```tex
\Lambda_K^{adm}(\chi,K_P)
:=
\frac{h_K(\chi)}{K_P}.
```

Reason:

1. `h_K(\chi)` vanishes when the near-cousin loses axial two-horizon structure
   in the Schwarzschild limit.
2. `K_P^{-1}` vanishes in the infinite-budget observer limit.
3. The product is dimensionless.
4. The product is defined before touching any observed dataset.

This is only the most conservative separable ansatz in the horizon-normal
chart. A more general observable map may use:

```tex
\Lambda_K^{adm}(\chi,K_P;\nu)
=
h_K(\chi)K_P^{-\nu},
\qquad
\nu>0,
```

but `\nu=1` is the first chart choice because the access coordinate above gives
`u_K=K_P^{-1}`.

To become an observable-channel amplitude, a pipeline map must still specify:

```tex
\lambda_{K,\mathcal P}^{obs-allowable}
=
C_{\mathcal P}
\Lambda_K^{adm}(\chi,K_P),
```

where `C_P` is the signed channel-response coefficient for a specified
observable/prism.

`C_P` is not derived here. Without it, there is no observed-amplitude
prediction.

Drift note: `obs-allowable` is an ugly term, but it prevents the observed /
observable type error. Future notation can replace it with `feas` or `adm`
only if the type distinction remains explicit.

## 5. Milestone Readout

### Milestone 1: Does the FRW Chart Lift?

Answer:

```text
Not directly.
```

The FRW chart uses a scale factor. The Kerr-interior near-cousin supplies
horizons and axial structure, but not a native FRW scale factor without an
observer congruence, averaging prescription, or projection rule.

Partial result:

```text
A horizon-normal finite-budget chart exists.
```

### Milestone 2: Is There a Closed-Form Map?

Answer:

```text
There is a closed-form feasibility kernel, not an observed amplitude.
```

The derived kernel is:

```tex
h_K(\chi)=\frac{1-\sqrt{1-\chi^2}}{1+\sqrt{1-\chi^2}}.
```

The first admissible scale is:

```tex
\Lambda_K^{adm}(\chi,K_P)=h_K(\chi)/K_P.
```

### Milestone 3: Does Kerr Predict the ell=3 Parallel-Fifths Finding?

Answer:

```text
No prediction yet.
```

The Kerr near-cousin supplies axial two-horizon structure. It does not yet pick
an `ell=3` operator-residue coordinate, a Planck mask transition, a Galactic
axis direction, or a parallel-fifths detector output.

Allowed statement:

```text
Kerr axiality makes an axial-residue question admissible.
```

Forbidden statement:

```text
Kerr predicts the Episode 3 Planck lockstep.
```

### Milestone 4: How Does Apparatus-Bound K Enter?

Answer:

`K_P` enters before observation, as a feasibility-band cutoff:

```tex
u_K=K_P^{-1}.
```

That is the observable/observed distinction in operational form. `K_P` defines
which part of the near-cousin is reconstructible by the pipeline. It does not
say what value the dataset will estimate.

### Milestone 5: Has the Circle Been Broken?

Answer:

```text
Partly.
```

This document breaks the first circle by deriving an admissible kernel without
fitting it to Pantheon+, DESI, or Planck.

It does not break the full circle because the channel response `C_P` is still
missing. The next theory move is to define one `C_P` for one prism before
looking at the corresponding observed value.

## 6. Next Theory Contract

Pick one observable prism from `docs/prismatic_decomposition_rigor.md`.

For that prism, define:

1. source feasible kernel: `h_K`, `g_K`, or `h_K/K_P`,
2. pipeline feasibility band: `K_P` and atlas-coherence condition,
3. channel response `C_P`,
4. sign convention,
5. predicted survival/collapse/recomposition behavior,
6. disconfirming control.

Only after those are specified may the program ask what was observed.

Recommended first prism:

```text
Planck operator prism
```

Reason:

Episode 3 already has a decomposition grammar and null-calibrated detector
coordinate. A `lambda_K` theory claim should first say whether Kerr-side
axiality predicts survival, collapse, or recomposition in that prism. It
should not start by fitting the Pantheon+ distance amplitude.

## Allowed Claims

1. The Kerr-interior near-cousin supplies a closed-form dimensionless
   spin-horizon feasibility kernel `h_K(chi)`.
2. A finite-budget horizon-normal interior chart gives a reconstruction floor
   `r_K = r_- + (r_+-r_-)/K_P`.
3. The first admissible scale `h_K(chi)/K_P` is observable-feasibility
   structure, not an observed amplitude.
4. A channel-response map is still required before `lambda_K` becomes a
   dataset-facing prediction.

## Forbidden Claims

1. This document derives an observed `lambda_K` number.
2. Kerr-interior cosmology is now the committed AOC territory.
3. Kerr predicts the Episode 3 Planck ell=3 lockstep.
4. Pantheon+, DESI, or Planck have observed `h_K(chi)/K_P`.
5. The channel coefficient `C_P` may be inferred after looking at the target
   dataset and then treated as a prediction.

