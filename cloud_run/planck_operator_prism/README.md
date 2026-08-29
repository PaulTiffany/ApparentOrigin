# Cloud Run Packet: Planck Operator-Prism Contract

Status: Linux/cloud execution packet for the Episode 4 `lambda_K`
operator-prism contract.

Purpose:

Run the missing official-mask `base` and `dilate1` ell=3 pair-residue
extraction in a Linux environment with `healpy`, without changing the local
Windows machine.

This packet does not make a new theory claim. It only produces the missing
observed coefficient and directional-summary inputs needed by:

```text
reports/planck_operator_residue/operator_prism_contract/operator_prism_contract_gate_report.md
```

## Required Inputs

The cloud runtime needs these five Planck PR3 FITS files:

```text
COM_CMB_IQU-commander_2048_R3.00_full.fits
COM_CMB_IQU-nilc_2048_R3.00_full.fits
COM_CMB_IQU-sevem_2048_R3.00_full.fits
COM_CMB_IQU-smica_2048_R3.00_full.fits
COM_Mask_CMB-common-Mask-Int_2048_R3.00.fits
```

The local raw Planck folder is about 7.45 GB, so do not put it in a public
Git repository. Use private cloud storage, a private Codespace volume, or a
mounted Drive folder.

## Colab Shape

1. Upload or mount the Planck FITS files.
2. Clone or upload this repo.
3. Run:

```bash
export MAP_DIR="/content/drive/MyDrive/planck_operator_residue/maps"
export MASK_PATH="/content/drive/MyDrive/planck_operator_residue/masks/COM_Mask_CMB-common-Mask-Int_2048_R3.00.fits"
bash cloud_run/planck_operator_prism/run_operator_prism_contract.sh
```

## Codespaces Shape

1. Open the repo in a private Codespace.
2. Copy the Planck FITS files into a non-committed data directory.
3. Run:

```bash
export MAP_DIR="$PWD/data/raw/planck_operator_residue/maps"
export MASK_PATH="$PWD/data/raw/planck_operator_residue/masks/COM_Mask_CMB-common-Mask-Int_2048_R3.00.fits"
bash cloud_run/planck_operator_prism/run_operator_prism_contract.sh
```

## Outputs

The runner writes:

```text
reports/planck_operator_residue/operator_prism_contract/healpy_official_mask/
```

and refreshes:

```text
reports/planck_operator_residue/operator_prism_contract/operator_prism_contract_gate_summary.json
reports/planck_operator_residue/operator_prism_contract/operator_prism_contract_gate_report.md
```

## Allowed Claims

1. The cloud packet runs the predeclared `healpy.map2alm` official-mask
   `base -> dilate1` contract inputs.
2. A completed run supplies the missing `D_res` values needed to evaluate
   `C_axis`.
3. The result is a contract evaluation for this Planck operator-prism channel,
   not confirmation or refutation of AOC.

## Forbidden Claims

1. Installing `healpy` or moving to cloud changes the theory status.
2. A positive `C_axis` confirms `lambda_K` or AOC.
3. A failed channel refutes AOC, LambdaCDM, or Kerr physics.
4. Retrospective fallback runs may be substituted for this cloud run.
