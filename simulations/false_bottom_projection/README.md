# False-Bottom Projection Toy Model

Status: runnable toy model.

Purpose:

This simulation demonstrates the mechanism behind the Observer-Quotient /
Apparent-Origin Lemma. It is not a cosmology simulation. It shows how finite
observer access can collapse unresolved depth into an apparent floor.

## Model

Underlying coordinate:

```tex
u \in \mathbb R.
```

Observer floor:

```tex
\epsilon > 0.
```

Smooth quotient:

```tex
q_{\epsilon,\delta}(u)
=
\epsilon
+
\delta \log\left(1+\exp\left(\frac{u-\epsilon}{\delta}\right)\right),
\qquad \delta>0.
```

For `u << epsilon`, the map returns approximately `epsilon`. For
`u >> epsilon`, the map returns approximately `u`. Thus sub-threshold depth is
compressed into a floor while above-threshold structure is preserved.

## Files

1. `false_bottom.py`
   - Pure-Python model and CSV generation.
2. `plot_false_bottom.py`
   - Optional matplotlib plotter. If matplotlib is unavailable, the CSV output
     from `false_bottom.py` is still useful.

## Commands

Generate sample data:

```powershell
python simulations\false_bottom_projection\false_bottom.py
```

Generate a plot:

```powershell
python simulations\false_bottom_projection\plot_false_bottom.py
```

## Interpretation

This toy model makes only one point:

> Apparent floors can arise from bounded reconstruction maps.

It does not establish that the Big Bang boundary is such a floor. That stronger
claim requires the FRW chart, a theory of `K`, empirical controls, and
observational comparison.

