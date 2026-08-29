# Theorem: Adaptedness of Observer-Induced Bundles

Status: formal proof supporting the AOC Proof Spine.

## Objective
To prove that the observer-induced curved bicomplex $(C^{\bullet\bullet}, D)$ is adapted to the $\Omega_O$-filtration, ensuring that observer-bounded cohomology is well-defined.

## Theorem
Let $(\EE, h_O, \nabla_O)$ be an observer-induced symbolic bundle with kernel scale $s_O$. Let $\Omega_O(\lambda)$ be the access capacity. If the connection $A_O$ is $\Obs$-bounded, then:
\[
[\kappa_O, F^k C^{\bullet\bullet}] \subseteq F^{k+1} C^{\bullet\bullet}.
\]

## Proof

### 1. Metric Degeneracy and Access Capacity
By Definition 2 of the Figure 3 companion, $\Omega_O(\lambda)$ is the minimum Rayleigh quotient of the capacity form $B_\lambda$ restricted to the observer-accessible subspace $W$. This implies that there exists a direction $e_1 \in W$ (the Rayleigh direction) such that the observer-induced metric $g_O$ satisfies:
\[
g_O(e_1, e_1) = \Omega_O(\lambda).
\]
For any other direction $v \in W$ with ambient norm $\|v\|_g = 1$, we have $g_O(v, v) \ge \Omega_O(\lambda)$.

### 2. Scaling of the Connection $A_O$
The connection $A_O$ is required to be $\Obs$-bounded (Definition 1, Figure 2), meaning:
\[
\|A_O(x)[v]\|_{h_O} \le \|A_O\|_\infty \|v\|_{g_O}
\]
for all tangent vectors $v$. Applying this to the Rayleigh direction $e_1$:
\[
\|A_O(e_1)\|_{h_O} \le \|A_O\|_\infty \sqrt{g_O(e_1, e_1)} = \|A_O\|_\infty \sqrt{\Omega_O(\lambda)}.
\]
Thus, the components of $A_O$ in the directions of least access scale as $O(\Omega_O^{1/2})$.

### 3. Scaling of the Curvature $\kappa_O$
The curvature 2-form is given by $\kappa_O = d A_O + A_O \wedge A_O$. We analyze the scaling of its norm as $\Omega_O \to 0$.

**The Quadratic Term:**
The term $A_O \wedge A_O$ evaluated on a pair of vectors $(v, w)$ involves the composition of endomorphisms $A_O(v)$ and $A_O(w)$. Using the bound from Step 2:
\[
\|(A_O \wedge A_O)(e_1, v)\|_{h_O} \le 2 \|A_O(e_1)\| \|A_O(v)\| \le 2 \|A_O\|_\infty^2 \sqrt{\Omega_O} \sqrt{g_O(v, v)} = O(\Omega_O^{1/2}).
\]
In a fully access-limited regime (such as the early FRW spatial slices where all directions scale with $a^2 = \Omega_O$), the term scales as $O(\Omega_O)$.

**The Differential Term:**
To analyze $d A_O$, we transform to the "access-divergent" coordinate $y = \Omega_O^{-1/2}$, which corresponds to the reconstruction space $R_O$. In this coordinate, the basis vector is $\partial_y$. The metric norm is:
\[
\|\partial_y\|_{g_O} \sim \Omega_O^{3/2}.
\]
The $\Obs$-bounded condition $\|A_O(\partial_y)\| \le C \|\partial_y\|_{g_O}$ forces the connection component $A_y$ to satisfy $\|A_y\| = O(\Omega_O^{3/2})$. The exterior derivative $d A_O$ in this coordinate frame involves $\partial_y A_y$, which scales as $O(\Omega_O^2)$.

### 4. Filtration Order of the Curvature Action
Combining the terms, the endomorphism-valued curvature satisfies:
\[
\|\kappa_O\|_{h_O} = O(\Omega_O^k) \quad \text{with } k \ge 1.
\]
By the definition of the $\Omega_O$-filtration (Definition 4, Figure 3), this means $\kappa_O \in F^1 C^{0,2}$.
The action of curvature on a cochain $\omega \in F^k C^{p,q}$ is given by the bracket $[\kappa_O, \omega]$. The filtration order of the result is:
\[
\text{ord}([\kappa_O, \omega]) \ge \text{ord}(\kappa_O) + \text{ord}(\omega) = 1 + k.
\]
Therefore, $[\kappa_O, F^k C] \subseteq F^{k+1} C$.

### 5. Conclusion
Since the curvature action raises the filtration order, the total differential $D$ satisfies:
\[
D^2 = [\kappa_O, \cdot] \equiv 0 \pmod{F^{k+1}}
\]
when acting on $F^k$. This ensures that the induced differential $\overline{D}$ on the associated graded $\mathrm{gr}^k C = F^k C / F^{k+1} C$ satisfies $\overline{D}^2 = 0$.

**The observer-induced curved bicomplex is adapted to the $\Omega_O$-filtration.**
