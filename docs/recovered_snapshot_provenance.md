# Recovered Pre-Git Snapshot Provenance

Status: provenance record for the April-May 2026 working tree.

## What This Commit Establishes

This repository snapshot was recovered from the local working directory
`C:\src\observer_cosmology`. The directory was not a Git working tree when it
was recovered. Its files nevertheless preserve a substantial pre-JWST phase of
the Apparent-Origin Cosmology research program.

The import commit is therefore a **recovered snapshot**, not a reconstruction
of a Git history that did not survive. Its author date is set to the latest
modification time among the retained research files so that the independent
history has an approximate temporal position. The commit date records when the
snapshot was actually placed under version control.

File modification times are filesystem metadata. They are useful provenance
evidence, but they are not claimed as cryptographically authenticated creation
dates. Git blob and tree identifiers establish the exact imported content from
the time of recovery onward.

## Observed Date Range

The retained local materials have visible modification dates spanning April
20-May 20, 2026. The public `PaulTiffany/ApparentOrigin` Git history began on
August 28, 2026. The two histories were developed independently and are joined
with a two-parent merge rather than by rebasing or rewriting either line.

## Deliberate Exclusions

The snapshot does not include:

- local Python virtual environments;
- downloaded Planck and other reproducible upstream datasets;
- scratch and compiler-generated files;
- generated report arrays and figures already excluded by the working tree;
- NotebookLM audio, video, PDF, archive, and table exports.

Acquisition notes, source manifests, instructions, prompts, scripts, research
documents, and NotebookLM preparation materials are retained. Exclusion of a
binary export is not a claim that it lacks research value; it preserves a clean
rights and publication boundary until that artifact is reviewed separately.

## Claim Boundary

This record supports the claim that the retained files existed in this local
form, with the recorded filesystem metadata, when the snapshot was recovered.
It does not establish a complete edit history, prove sole authorship of every
sentence, or retroactively turn filesystem timestamps into contemporaneous Git
commits.
