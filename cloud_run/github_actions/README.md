# GitHub Actions Runner: Planck Operator-Prism Contract

Status: repo-native GitHub Actions harness.

Purpose:

Let GitHub provide the Linux machine, `healpy` install, Planck PR3 download,
and contract run. The large FITS files are not committed to Git.

## What It Does

Manual workflow:

```text
.github/workflows/planck_operator_prism.yml
```

Steps:

1. Restore or create a GitHub Actions cache for Planck PR3 inputs.
2. Download the four Planck component-separated maps and official common mask
   from the IRSA Planck mirror.
3. Install `healpy`, `astropy`, and related Python dependencies.
4. Run the official-mask `base` and `dilate1` ell=3 extraction.
5. Evaluate the `C_axis` contract gate.
6. Upload the small reports/JSON files as a workflow artifact.

## Why Not Commit the Data?

GitHub blocks regular Git files over 100 MiB and recommends keeping
repositories small. The local Planck raw folder is about 7.45 GB. The harness
therefore treats Planck FITS as fetched data, not source.

GitHub Actions caches are limited; the Planck cache is deliberately one
repository-level cache key:

```text
planck-pr3-component-maps-common-mask-v1
```

If it gets evicted, the workflow downloads the files again.

## How To Run

1. Push this repo to a private GitHub repository.
2. Open the repository's Actions tab.
3. Select `Planck Operator-Prism Contract`.
4. Click `Run workflow`.
5. Keep defaults unless deliberately changing the contract:

```text
nside_out = 64
lmax = 30
```

6. Download the artifact:

```text
planck-operator-prism-contract
```

## Expected Result

The artifact should contain:

```text
reports/planck_operator_residue/operator_prism_contract/operator_prism_contract_gate_report.md
reports/planck_operator_residue/operator_prism_contract/operator_prism_contract_gate_summary.json
reports/planck_operator_residue/operator_prism_contract/healpy_official_mask/
```

## Allowed Claims

1. This is a reproducible Linux `healpy` run of the predeclared
   official-mask operator-prism contract inputs.
2. The uploaded artifact is small enough to bring back into the working repo.
3. The large FITS inputs remain external scientific data, not Git-tracked
   project source.

## Forbidden Claims

1. The GitHub Actions cache is a publication archive.
2. A successful workflow is an AOC confirmation.
3. A failed contract channel refutes AOC, LambdaCDM, or Kerr physics.
