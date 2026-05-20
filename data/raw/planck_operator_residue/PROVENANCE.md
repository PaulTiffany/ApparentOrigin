# Planck Operator-Residue Provenance

Status: source list, no large FITS files downloaded yet.

Primary official source:

```text
Planck Legacy Archive wiki, 2018 CMB maps
https://wiki.cosmos.esa.int/planck-legacy-archive/index.php/CMB_maps
```

The Planck Legacy Archive describes the 2018 CMB maps as produced by four
component-separation methods:

```text
COMMANDER
NILC
SEVEM
SMICA
```

NASA/IPAC IRSA mirror preview pages for PR3 full-mission maps:

```text
https://irsa.ipac.caltech.edu/data/Planck/release_3/all-sky-maps/previews/COM_CMB_IQU-commander_2048_R3.00_full/index.html
https://irsa.ipac.caltech.edu/data/Planck/release_3/all-sky-maps/previews/COM_CMB_IQU-nilc_2048_R3.00_full/index.html
https://irsa.ipac.caltech.edu/data/Planck/release_3/all-sky-maps/previews/COM_CMB_IQU-sevem_2048_R3.00_full/index.html
https://irsa.ipac.caltech.edu/data/Planck/release_3/all-sky-maps/previews/COM_CMB_IQU-smica_2048_R3.00_full/index.html
```

ESA DOI record:

```text
PR3 Legacy CMB Maps
https://doi.org/10.5270/esa-zfx8b4s
```

Local data policy:

The full HEALPix FITS maps are hundreds of MB each and require `healpy` or
equivalent HEALPix tooling. Do not download them into this repo until the
extraction step is ready. The first durable local artifact should be a compact
low-ell coefficient table under:

```text
data/derived/planck_operator_residue/planck_lowell_alm.csv
```

Download helper:

```text
empirical/planck_operator_residue/download_planck_maps.ps1
```

This script targets the four full-mission PR3 component maps listed above.
Expected total size is multiple GB.
