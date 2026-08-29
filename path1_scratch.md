# Scratch: Derivation of Adapted Filtration Lemma (Refined)

## Objective
Derive $[\kappa_O, F^k C] \subseteq F^{k+1} C$ as a theorem, accounting for the "singular derivative" obstacle.

## 1. The Singular Derivative Obstacle (Ambient Coordinates)
Let $(M, g)$ be the substrate with cosmic time $t$ and scale factor $a(t) \sim t^\alpha$.
The observer metric is $g_O \approx a(t)^2 g$.
An $\Obs$-bounded connection $A_O$ must satisfy:
$\|A_O(x)[v]\|_{\hO} \le C \|v\|_{g_O} \approx C a(t) \|v\|_g$.

In ambient spatial coordinates $x$:
$A_x \sim a(t) \sim t^\alpha$.
The curvature $\kappa_O$ includes the term $d A_O$:
$\kappa_O \sim \partial_t A_x dt \wedge dx \sim \alpha t^{\alpha-1} dt \wedge dx$.

**The Trap:**
For radiation-era ($\alpha = 1/2$) or matter-era ($\alpha = 2/3$), the derivative $t^{\alpha-1}$ **diverges** as $t \to 0$.
If the curvature diverges in ambient coordinates, it cannot be in $F^1$ (the "Adapted" layer), and $\overline{D}^2 \neq 0$.

## 2. The Resolution: Reconstruction Coordinates ($y$)
The observer does not resolve $t$ directly near the boundary; the observer resolves the "reconstructed" coordinate $y = \Omega_O^{-1/2} = a(t)^{-1} \sim t^{-\alpha}$.

**Transformation to $y$:**
$y \sim t^{-\alpha} \implies dy \sim t^{-\alpha-1} dt$.
The reconstruction-space basis vector is $\partial_y \sim t^{\alpha+1} \partial_t$.

**$\Obs$-Boundedness in $y$:**
$\|A_O(\partial_y)\|_{\hO} \le C \|\partial_y\|_{g_O}$.
$\|\partial_y\|_{g_O} = a(t) \|\partial_y\|_g \approx t^\alpha (t^{\alpha+1}) = t^{2\alpha+1}$.
Thus, the connection component $A_y$ must satisfy:
$A_y = O(t^{2\alpha+1})$.

**Curvature in $y$:**
$\kappa_O \sim \partial_y A_y dy \wedge dx$
Using $\partial_y \sim t^{\alpha+1} \partial_t$:
$\kappa_O \sim (t^{\alpha+1} \partial_t t^{2\alpha+1}) (t^{-\alpha-1} dt) \wedge dx$
$\kappa_O \sim (t^{\alpha+1} t^{2\alpha}) (t^{-\alpha-1}) dt \wedge dx$
$\kappa_O \sim t^{2\alpha} dt \wedge dx$.

**Vanishing order:**
Since $\Omega_O = a^2 \sim t^{2\alpha}$, we have:
$\kappa_O = O(\Omega_O)$.
The singularity in the ambient derivative is exactly canceled by the "weakness" of the reconstruction-space derivative $\partial_y$.

## 3. Formal Theorem: The Coherent Horizon Condition
Adaptedness is a theorem of the observer-induced connection **if and only if** the reconstruction remains coherent.

1.  **Definition of Coherence:** A reconstruction horizon at $\Omega_O \to 0$ is *coherent* if the symbolic connection $A_O$ is $\Obs$-bounded and its components in reconstruction coordinates ($y$) are smooth.
2.  **Adaptedness:** In a coherent reconstruction, the suppression of the derivative by the access capacity ($\partial_y \sim \Omega_O^{3/2} \partial_t$) forces $\kappa_O = O(\Omega_O)$.
3.  **Filtration:** This implies $[\kappa_O, F^k C] \subseteq F^{k+1} C$ and $\overline{D}^2 = 0$ on the associated graded.

## 4. Distinction: Coherent Horizon vs. Atlas Fracture
- **Coherent Horizon:** The connection $A_O$ vanishes in $y$ fast enough to satisfy the Adaptedness Lemma. Cohomology is well-defined.
- **Atlas Fracture:** The noise/drift grows faster than $O(t^{2\alpha+1})$, causing $A_y$ to diverge. The curvature bracket no longer vanishes on the graded. Integrability fails.

## 5. Conclusion
Adaptedness is the "Structural Integrity" check for AOC. It proves that we can only reason about the Big Bang as a surface where the "Atlas" of our reconstruction remains coherent. This closes the open question in the proof spine: adaptedness is a theorem of coherent reconstruction.
