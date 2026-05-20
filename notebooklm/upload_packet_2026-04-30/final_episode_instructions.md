# Final-Episode NotebookLM Instructions (Episode 4)

Paste this block before requesting any podcast, tutorial, or video script
from the 2026-04-30 packet.

This is the final episode for now. The reports themselves carry their
own Allowed/Forbidden claim sections — trust those. The block below is
context, not a leash.

## Instruction block

```text
You are working from a source packet for Apparent-Origin Cosmology
(AOC), a bounded-observer research program. This is Episode 4, the
final episode for now.

The arc this packet covers: a frozen empirical contract was written
in advance (`11_lambda_k_planck_operator_prism_contract.md`,
committed 2026-04-29 23:14), its evaluation gate was committed at
23:28, and a GitHub Actions Linux run on 2026-04-30 produced the
result reported in `12_operator_prism_contract_gate_report.md`. The
sign condition was satisfied. The verdict string keeps the literal
clause "if_inputs_were_predeclared" because the auditor checks
timestamps, not the code. Sprint F1 then audited the gate's
hardcoded normalization and Sprint F2 ran a local-machine null that
clarifies what the sign-only PASS does and does not show. Sprint F3
documents how a CI-side LLM agent staged the live run on Linux
compute the local Windows machine could not run.

Type discipline runs through the λ_K theory stack: feasible (allowed
by near-cousin Kerr-interior geometry), observable (survives an
apparatus / pipeline feasibility band), observed (estimated in a
dataset). The Episode 4 derivation lands a closed-form Kerr horizon
kernel at the feasible / observable level. No number for λ_K is
narrated.

Slogan to preserve verbatim: "Boundary of reconstruction, not
beginning of being."

Each report carries its own Allowed and Forbidden Claims sections —
defer to those rather than to a separate guardrail list. Read the
packet, find what's interesting, and use your own judgment about
what to foreground. Where the source has tension or unresolved
questions, name them; you don't need permission to be precise.
```

## Prompts

These are starting points, not scripts. Reorder, recombine, or skip
sections if your reading of the packet suggests a different shape.

### Internal Episode 4 podcast (~25 min, two hosts)

```text
Brief a collaborator who heard the Episode 3 podcast on what's
happened since. The packet has the full arc; you decide the
sequencing. Touchstones if useful: predeclaration timestamp order
(contract, gate code, live run), the operator-prism PASS with its
conditional verdict string, what the surrogate null in Sprint F2
actually reveals about the sign condition, and the frozen open
question that closes the episode.

End with the slogan.
```

### Public explainer (~6 min)

```text
Scientifically literate but non-specialist audience. The story to
tell is how predeclaration was actually enforced this time and what
that PASS does and does not mean. The Sprint F2 null is part of the
story, not a footnote — it sharpens the reading rather than
weakening it.

End with the slogan.
```

### Technical episode on the λ_K horizon kernel (~10 min)

```text
For working CMB analysts and mathematical physicists. The Kerr horizon
kernel h_K(chi) = (1 - sqrt(1 - chi^2)) / (1 + sqrt(1 - chi^2)), the
horizon-normal interior chart, and the admissible scale
Lambda_K^adm = h_K(chi) / K_P are in the source. Why these are
observable-feasibility structure rather than observed amplitude is
the load-bearing point. State raw angles alongside normalized scores.

End with the slogan.
```

### Sprint E listening guide (~5 min)

```text
Methodology-focused. The three prisms (multipole, mask / sky-partition,
operator) and the feature-state vocabulary are routing labels for
carrying low-ell residue features forward. Apply the grammar to the
Episode 3 features the way the source does, or differently if you see
a cleaner path.

End with the slogan.
```

### CI LLM compute leverage (~4 min)

```text
The pattern: when the local environment cannot run a required library,
a CI-side LLM agent can stage GitHub-hosted Linux compute for a frozen
contract, with the local repo remaining canonical and the artifact
pulling back. Why this is a tool choice, not a delegation of
authorship, is the interesting part.

End with the slogan.
```

## Optional uploads

The packet is Markdown-only. If linking back to Episode 3 audio is
useful, the Episode 3 packet's `all_pipelines_sequential.wav`
(per-operator octave-pair duets) is the closest auditory companion.
Treat any WAV as a measurement readout, not new evidence.
