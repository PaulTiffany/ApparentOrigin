# Data Directory

This directory separates raw external data from derived analysis products.

## Policy

Raw third-party data should not be treated as authored repo content. Keep raw
data under `data/raw/` and record provenance in the relevant empirical branch.

Generated tables and figures should go under `data/derived/` and `reports/`.

The `.gitignore` excludes raw downloads and generated CSV/JSON/PNG outputs by
default.

## Current Branches

1. `pantheon_plus`
   - First empirical contract for apparatus-bound `K` using public Pantheon+
     supernova distance data.
2. `desi_dr2_bao`
   - First external BAO gate using compact DESI DR2 Gaussian BAO likelihood
     inputs linked by the official DESI DR2 cosmology products page.
3. `planck_operator_residue`
   - Source/provenance notes for Planck component-separated CMB maps and
     derived low-ell coefficient tables. Full FITS maps should not be
     downloaded until the HEALPix extraction step is ready.
