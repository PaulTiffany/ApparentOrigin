# GitHub Actions Runner: Fermi Demask-Shift Recurrence

Status: CI runner scaffold for the predeclared Fermi demask-shift recurrence
contract.

Purpose:

Let GitHub provide a Linux runner for the Fermi demask-shift SharedShift
detector. The runner is intentionally split into two stages:

```text
stage 1: smoke test with synthetic axis rows
stage 2: live run from a supplied axes CSV URL or future Fermi fetcher
```

This packet does not claim a Fermi result. It gives Desktop GPT and future
GitHub-side agents an executable harness to extend.

## Workflow

```text
.github/workflows/fermi_demask_shift.yml
```

Manual inputs:

```text
mode = smoke | axes_csv_url
axes_csv_url = optional URL to a CSV with columns voice,mask,band,x,y,z,grade
transitions = default M0:M1,M1:M2,M2:M3,M0:M2,M0:M4
```

The output artifact is:

```text
fermi-demask-shift-run
```

and contains:

```text
reports/fermi_demask_shift_recurrence/ci_runner/
```

## CSV Contract

The detector expects:

```text
voice,mask,band,x,y,z,grade
```

where `(x,y,z)` is a unit or nonzero Cartesian axis vector. Axes are treated
axially:

```text
u == -u
```

Grade `D` rows are excluded from the primary metric unless the script is run
with `--include-diagnostic`.

## Allowed Claims

1. This runner executes the Fermi SharedShift metric scaffold in GitHub
   Actions.
2. The smoke mode verifies the CI harness and artifact upload path.
3. The `axes_csv_url` mode allows a frozen Fermi axis table to be evaluated
   without committing large sky maps.

## Forbidden Claims

1. Smoke mode is not a Fermi experiment.
2. A workflow success is not AOC evidence.
3. A supplied axes CSV is not trusted unless its provenance and voice
   independence ledger are also supplied.

