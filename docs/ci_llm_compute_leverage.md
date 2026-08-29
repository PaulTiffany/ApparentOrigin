# CI LLM Compute Leverage

Status: Episode 4 methodology note.

Phase: methodology / harness pattern, not new evidence.

Purpose:

Document the operating pattern by which a CI-side LLM agent (in this
case, GPT working through OpenAI Codex) staged the Planck operator-prism
contract on GitHub-hosted Linux compute when the local Windows
environment did not have a working `healpy` install. This note exists
because the pattern is reusable beyond the present run and should be
named explicitly so future agents (and the human-in-the-loop) can
recognize when to invoke it.

The pattern is not "outsource the science to a different LLM." It is
"the local repo is the canonical state; CI compute is fetched data;
and a CI-side agent can be a useful broker between them."

## 1. The Triggering Constraint

Local environment (this repo's machine, 2026-04-30):

```text
Windows 11
Python 3.11 (or whatever venv ships locally)
healpy: not installable / not working
```

The Episode 4 operator-prism contract requires a `healpy.map2alm`
extraction with the official Planck PR3 common mask in the loop, on
2048-nside FITS maps totalling about 7.45 GB. None of that runs locally.

Three failure modes that this pattern avoids:

1. *Quietly defer the contract.* The contract was already predeclared
   (`docs/lambda_k_planck_operator_prism_contract.md`); not running it
   would be a discipline violation.
2. *Move the contract to a coordinate the local machine can compute.*
   That is the post-hoc-tuning failure mode the predeclaration
   discipline exists to prevent.
3. *Stand up a permanent shared infrastructure.* AOC is one researcher
   plus tooling; running a server is overhead that does not amortize.

## 2. The Pattern

```text
local repo (Windows, canonical scientific state)
    |
    | (a) push the predeclared contract + extractor scripts
    v
private GitHub repo  ----- (b) CI-side LLM agent stages workflow ----+
    |                                                                |
    |                                  (c) GitHub Actions runs       |
    |                                      Linux + healpy + FITS     |
    v                                                                v
local repo  <--- (d) artifact pull-back (small reports/ directory) --+
```

Concretely on this run:

1. Local repo had:
   - `docs/lambda_k_planck_operator_prism_contract.md` (frozen 2026-04-29 23:14)
   - `empirical/planck_operator_residue/evaluate_operator_prism_contract.py` (gate code, 2026-04-29 23:28)
   - `empirical/planck_operator_residue/extract_planck_lowell_healpy_morphology.py` (Linux-only extractor)
2. The CI-side agent staged a private GitHub repository hosting the
   workflow plus a small `cloud_run/` packet
   (`cloud_run/planck_operator_prism/`,
   `cloud_run/github_actions/`,
   `.github/workflows/planck_operator_prism.yml`).
3. GitHub Actions on `ubuntu-latest` with Python 3.12 ran:
   - `download_planck_pr3.sh` -- IRSA mirror -> cached FITS files
   - `pip install -r cloud_run/planck_operator_prism/requirements.txt`
   - `extract_planck_lowell_healpy_morphology.py` -- official-mask base + dilate1
   - `directional_residue_axis_octupole.py` -- pair-residue axes at ell=3
   - `evaluate_operator_prism_contract.py` -- contract gate
4. Workflow uploaded only the small report directory
   (`reports/planck_operator_residue/operator_prism_contract/**`) as an
   artifact. The 7.45 GB of FITS stayed on GitHub-managed cache; the
   workflow artifact is kilobytes.
5. The artifact came back into the local repo and the gate report
   plus updated coefficient summaries became part of the canonical
   repo state.

Run record:

```text
https://github.com/PaulTiffany/planck-operator-prism-contract
https://github.com/PaulTiffany/planck-operator-prism-contract/actions/runs/25146431898
```

Result:

```text
C_axis(ell=3, official-mask-base)    = 0.281497
C_axis(ell=3, official-mask-dilate1) = 0.425643
live_verdict = contract_success_if_inputs_were_predeclared
```

## 3. Why This Is Disciplined

Three properties keep this from drifting into "an LLM did the science":

**Predeclaration timestamp order.** The contract document and the gate
script were committed before the workflow that ran them. The gate's
verdict string carries the conditional `if_inputs_were_predeclared`
because the code itself does not know whether predeclaration happened
in the right order; the timestamp record does. The science log entry
records both.

**Data versus source.** The 7.45 GB of Planck FITS files are treated
as fetched data, not Git-tracked source. They live in a GitHub Actions
cache keyed on a public URL; they would be re-downloaded from the IRSA
mirror if the cache were evicted. Treating GitHub as a compute and
cache substrate rather than a scientific archive avoids the failure
mode where infrastructure becomes load-bearing for reproducibility.

**Artifact pull-back.** The CI run produces a small artifact
directory; that artifact is pulled back into the local repo and
becomes part of the canonical state. The live numbers in the science
log are not "what GPT said the gate returned"; they are what the gate
report file in the local repo says, which was uploaded by the
GitHub-hosted runner from the gate script's own output.

## 4. CI LLM Agent Versus Local LLM Agent

Two different LLM agents work the same repo from different ends:

| | Local LLM (Claude here) | CI LLM (GPT via Codex) |
| --- | --- | --- |
| primary tool | Read/Edit/Bash on local repo | git + GitHub Actions on a private fork |
| binds | Windows env constraints; native libraries | Linux runner; whatever pip can install |
| canonical state | the local repo | the local repo (after pull-back) |
| writes | source, docs, packets | workflow YAML, run scripts, fetched-data manifests |
| reads | local files | GitHub repo state + Actions logs |

Either agent can read the other's work via the local repo; neither is
a "judge" of the other. This is why both agents must respect the
phase-tag discipline -- there is no umpire.

The CI-side agent's particular value here was: it knew the
GitHub-Actions YAML dialect, the IRSA Planck mirror layout, and the
caching idioms; it could iterate on the workflow without burning local
cycles; and it produced a self-documenting `cloud_run/` directory that
is part of the local repo now and can be re-run by anyone with a
private fork of the repository.

## 5. When This Pattern Is Worth Invoking

Useful triggers:

1. local environment cannot install a required library
   (`healpy`, GPU-only tools, unsupported OS),
2. the operation needs significantly more compute than the local
   machine has,
3. the operation needs an external fetch that should not be
   hand-managed (large datasets, gated mirrors),
4. the result is a small artifact (reports, coefficients, JSON) that
   pulls back cleanly,
5. the operation is rare enough that maintaining a permanent server
   would not amortize.

Anti-triggers:

1. the operation is a sustained daily workload,
2. the artifact is large and would silently encourage committing the
   data to Git,
3. the operation requires tightly coupled iteration with the local
   agent,
4. the predeclared contract has not been frozen yet (in which case CI
   compute is just a more expensive sandbox).

## 6. What This Note Is Not

It is not a claim about who deserves authorship. The science is the
contract plus the result; the agent identity is a tool choice, like
which IDE.

It is not a permission to skip predeclaration. The discipline runs the
other way: CI compute is *more* expensive and *more* visible than
local cycles, so it should only run frozen contracts.

It is not a permanent infrastructure plan. The GitHub Actions cache
is a Linux-runner amortization, not an archive. If the cache evicts,
the run becomes slow but not unreproducible.

## Allowed Claims

1. Episode 4 used a CI-side LLM agent to broker GitHub-hosted Linux
   compute for a contract that local Windows could not execute.
2. The pattern preserved predeclaration discipline because the contract
   was frozen in the local repo before the workflow ran.
3. Large data inputs are treated as fetched data, not Git-tracked source.
4. The pattern is reusable for future runs that hit the same
   triggering constraint.

## Forbidden Claims

1. The CI LLM agent did the science.
2. GitHub Actions completion is itself evidence for AOC.
3. The pattern replaces predeclaration; CI is just where it ran.
4. This pattern justifies committing large data to the repository.
