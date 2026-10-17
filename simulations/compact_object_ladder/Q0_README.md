# Phase Q0: conditional self-gravity / heat-load calculator

Status: **illustrative conditional calculation**, not evidence of any feasible construction, collapse route, replication process, gravitationally bound engineered structure, black hole, or quantum foam. See Issue [#5](https://github.com/PaulTiffany/ApparentOrigin/issues/5).

This extends the **fixed natural-object transfer ladder** without modifying its definitions or reference values. Source: \`compact_object_ladder.py\`; Q0: \`q0_self_gravity.py\`.

## Declared assumptions

For each named case all input fields in \`q0_contract.json\` are in SI units. They are hypothetical premises, not fitted quantities:

- \`initial_mass_kg > 0\`, \`initial_radius_m > 0\`, \`dissipated_power_w >= 0\`.
- \`mass_growth_rate_kg_s >= 0\`, \`duration_s >= 0\`, and \`radius_mass_exponent\` are explicit. The only growth law is **M(t) = M0 + mdot·t; R(t) = R0 (M(t)/M0)^a**. The law is **not** derived from replication, accretion, available material, radiation pressure, confinement, or any supply model.
- \`radiation_emissivity\` in (0,1] assumes effective uniform-area blackbody radiation. Power is treated as **constant waste-heat output**, independently of growth; no energy-supply mechanism is modeled.
- \`max_surface_temperature_k\` may be null. When supplied, a hotter blackbody-equivalent temperature is a conditional thermal failure **for that cap only**, not a universal impossibility.
- \`assumed_entropy_bits\` and \`excitation_energy_above_ground_j\` may be null; null means **not tested**, not zero. For entropy, the Bekenstein comparison is interpreted only in the declared **low-compactness diagnostic** C < 0.1. The 0.1 division is an **illustrative screen**, not a physical theorem threshold.
- Quantum computation bound \`2 E/(π ℏ)\` is interpreted as an upper rate only when an *independently supplied* energy above ground is present. A rest-mass energy is **not** automatically assumed available for computation.

## Reported observables

- Schwarzschild radius and C = 2GM/(Rc²), with a C>=1 diagnostic **not** a proof that a horizon formed (spherical, nonrotating comparison only).
- Mean density, formal Bekenstein bit expression and Bekenstein–Hawking entropy at the **same mass**, both inherited from the ladder. For C near/above unity these formula outputs are algebraic comparisons, **not** an operational matter-entropy bound or an interior-density claim.
- Effective radiative area, flux, blackbody-equivalent temperature and the conditional cap check.
- Optional entropy and computation-rate bounds under the restrictions above.
- Initial and final states under the explicit growth law, plus *formal* C=1 crossing time when that law has a positive finite crossing. **No physical reachability decision** is emitted.

A hypothetical fixed-radius accumulation case is deliberately included to show that C crossing alone **cannot** license a technological scenario; the model supplies no causal mechanism that could maintain the radius or required mass flow.

## Reproduce via GitHub Actions

The \`compact-object-ladder.yml\` workflow continues to verify its original fixed benchmark. The separate \`q0-self-gravity.yml\` workflow tests Q0 and writes \`q0-results.json\` as a small artifact. This is the project's Actions-only science execution pattern. No source telescope data or large physical datasets are needed.

Run contract locally only for software development:

\`\`\`sh
cd simulations/compact_object_ladder
python -m unittest -v test_q0_self_gravity.py
python q0_self_gravity.py --contract q0_contract.json --out q0-results.json
\`\`\`

**Allowed claim:** the exact declared textbook expressions constrain the stipulated inputs and growth laws.

**Forbidden claim:** any physical route from AI, nanotechnology or industrial replication to collapse has survived; a horizon actually forms; black-hole thermodynamics validates such a route; a computation creates spacetime foam.

## Next falsifiable Q0 step (not done here)

Replace the illustrative accumulation law with a **declared substrate, resource supply, transport/confinement and heat-removal feasibility model**. Freeze efficiency and failure criteria before testing. Only then can one attempt a conditional kill/viability result for that *specific* trajectory. Failure to state these premises is \`UNTESTED\`, not a physical null result.
