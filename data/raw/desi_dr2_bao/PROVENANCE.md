# DESI DR2 BAO Data Provenance

Branch: `empirical/desi_dr2_bao`

Purpose:

Use the compact official DESI DR2 BAO likelihood inputs before touching the
large Zenodo archive or cosmology chains.

Official DESI DR2 publication index:

```text
https://data.desi.lbl.gov/doc/papers/dr2/
```

Official DESI DR2 BAO cosmology products page:

```text
https://data.desi.lbl.gov/public/papers/y3/bao-cosmo-params/README.html
```

The DESI products page states that the DESI DR2 BAO likelihoods used for the
cosmology results are public here:

```text
https://github.com/CobayaSampler/bao_data/tree/master/desi_bao_dr2
```

## Local Files

Mean vector source URL:

```text
https://raw.githubusercontent.com/CobayaSampler/bao_data/master/desi_bao_dr2/desi_gaussian_bao_ALL_GCcomb_mean.txt
```

Mean vector local file:

```text
data/raw/desi_dr2_bao/desi_gaussian_bao_ALL_GCcomb_mean.txt
```

Mean vector SHA256:

```text
9ac154ab583ce759c0f7eef3c978c7c70a6ead2d18774caceadf1a350a640585
```

Covariance source URL:

```text
https://raw.githubusercontent.com/CobayaSampler/bao_data/master/desi_bao_dr2/desi_gaussian_bao_ALL_GCcomb_cov.txt
```

Covariance local file:

```text
data/raw/desi_dr2_bao/desi_gaussian_bao_ALL_GCcomb_cov.txt
```

Covariance SHA256:

```text
252a143274c8a07c78694c119617d36594f6d7965d00319ca611c6ffb886e509
```

## Notes

The selected mean vector has 13 BAO measurements:

```text
DV_over_rs at z=0.295
DM_over_rs and DH_over_rs at z=0.510, 0.706, 0.934, 1.321, 1.484, 2.330
```

The covariance file has 169 entries, interpreted as a 13 by 13 covariance
matrix in the same row order as the mean vector.

