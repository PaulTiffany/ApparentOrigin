# Apparatus-Bound K Toy Model

Status: runnable toy model.

Purpose:

This script implements the first apparatus-bound `K` calculation from
`docs/apparatus_bound_k_program.md`.

It does not use real cosmological data. It tests the mechanism:

> If reconstruction uncertainty grows with inverse scale factor, a finite
> pipeline has a calculable deepest reliable inverse scale factor `K_P`, and
> therefore a calculable apparent-origin time `t_K(P)`.

## Model

Let:

```tex
y(t)=1/a(t)=A^{-1}t^{-\alpha}.
```

Let pipeline uncertainty grow as:

```tex
\sigma_P(y)=\sigma_0 y^p,
\qquad p>1.
```

For allowed relative error `eta`:

```tex
K_{P,\eta}
=
\left(\frac{\eta}{\sigma_0}\right)^{1/(p-1)}.
```

Then:

```tex
t_K(P)=(A K_P)^{-1/\alpha}.
```

## Command

```powershell
python simulations\apparatus_bound_k\apparatus_k.py
```

Outputs:

1. `apparatus_k_results.csv`
2. `apparatus_k_sweep.csv`

If matplotlib is installed:

```powershell
python simulations\apparatus_bound_k\plot_apparatus_k.py
```

also writes:

1. `apparatus_k_sweep.png`

## Interpretation

Lower `sigma_0` means better reconstruction. Better reconstruction increases
`K_P` and pushes `t_K` earlier.

That is the core apparatus-bound prediction shape.

## Two-Pipeline Extension

The closed-form toy above implements §3 of `docs/apparatus_bound_k_program.md`
only. The §5--§7 program (forward-model noise instantiation, two-pipeline
ratio, atlas-coherence cutoff) is implemented as a separate script:

```text
simulations/apparatus_bound_k/apparatus_k_two_pipeline.py
```

This script samples observations from each pipeline under
`sigma_P(y) = sigma_0 * y^p`, reconstructs `sigma_hat(y)` from binned residuals,
finds `K_emp` by log-log interpolation, runs two independent reconstruction
charts (Gaussian kernel and binned median in `log t`) to compute the §7 atlas
coherence `Gamma(y)`, and aggregates over Monte Carlo seeds.

Why a separate script: the closed-form toy is meant to stay minimal because it
documents the §3 mechanism. The two-pipeline extension is where the §6 ratio
prediction `K_2 / K_1 = (sigma_{0,1} / sigma_{0,2})^{1/(p-1)}` becomes a real
internal check rather than a tautology against the closed form.

Allowed claim from this run:

> The §6 two-pipeline ratio prediction is reproduced under explicit
> forward-model noise. The §7 atlas-coherence cutoff distinguishes a
> reliability floor from chart fracture.

Forbidden claim:

> This simulation validates AOC against any real cosmological dataset.

Outputs:

```text
simulations/apparatus_bound_k/apparatus_k_two_pipeline_seeds.csv
simulations/apparatus_bound_k/apparatus_k_two_pipeline_ratio.csv
simulations/apparatus_bound_k/apparatus_k_two_pipeline_atlas.csv
simulations/apparatus_bound_k/apparatus_k_two_pipeline_summary.json
simulations/apparatus_bound_k/apparatus_k_two_pipeline.png
```

Run:

```powershell
python simulations\apparatus_bound_k\apparatus_k_two_pipeline.py
```

