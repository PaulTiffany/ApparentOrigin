# Empirical Contract: Accessible Data

Status: working map of public data that can support first AOC tests.

Purpose:

Define what "empirical contract" means in this repo:

> use real public data, declare the pipeline, declare the reconstruction budget,
> state the allowed claim, and state what would count against the claim.

This is not a claim that AOC is already validated.

## Data Branches

| Branch | Public data | AOC use | First safe test |
| --- | --- | --- | --- |
| Supernova distance | Pantheon+ / Pantheon+SH0ES | Luminosity-distance relation and pipeline-bound uncertainty | Fit a toy `K_P` from redshift/distance-modulus uncertainty growth |
| BAO / expansion history | DESI DR2 BAO measurements, chains, and supplementary products | Cross-probe expansion-history gate after Pantheon+ | Test whether the frozen Pantheon+ deformation direction is compatible with BAO observables |
| CMB maps / acoustic structure | Planck Legacy Archive 2018 CMB maps and likelihood products | Acoustic-peak / reconstruction-horizon burden | Use published peak positions and component-separation products as operator/pipeline examples |
| Gamma-ray sky | Fermi LAT/GBM public data and catalogs | Instrument-bound high-energy observation pipeline | Treat source catalogs or GRB products as a clean apparatus-bound `K` example, not as origin cosmology yet |

## 1. Pantheon+ / Supernovae

Access:

1. Pantheon+SH0ES GitHub organization:
   `https://github.com/PantheonPlusSH0ES`
2. DataRelease repository:
   `https://github.com/PantheonPlusSH0ES/DataRelease`
3. Distance file:
   `Pantheon+_Data/4_DISTANCES_AND_COVAR/Pantheon+SH0ES.dat`

Why it is useful:

Supernovae are the cleanest first comparison because AOC already needs a
luminosity-distance sandbox. Pantheon+ gives redshifts, distance moduli, and
covariance products.

First safe AOC contract:

> Given a published supernova pipeline, estimate how relative distance
> uncertainty grows with redshift and translate that into an apparatus-bound
> dynamic range `K_P`.

Allowed claim:

> This tests whether the apparatus-bound `K` formalism can be computed on a
> real distance dataset.

Forbidden claim:

> AOC explains supernova acceleration.

## 2. DESI DR2 / BAO

Access:

1. DESI DR2 publication index:
   `https://data.desi.lbl.gov/doc/papers/dr2/`
2. DESI DR2 cosmology chains and data products announcement:
   `https://www.desi.lbl.gov/2025/10/06/desi-dr2-cosmology-chains-and-data-products-released/`
3. DESI DR2 Results II supplementary data:
   `https://zenodo.org/records/16644577`

Why it is useful:

DESI DR2 BAO is the clean next external gate after Pantheon+. Supernovae alone
cannot distinguish real expansion-history structure from calibration,
`M_B`/`H0`, or dark-energy mimicry. BAO provides a different ruler and reports
distance information through observables such as:

```text
D_M(z) / r_d
D_H(z) / r_d
D_V(z) / r_d
```

First safe AOC contract:

> Carry the frozen Pantheon+ v0/v1 deformation families into DESI DR2 BAO and
> test whether the DESI-preferred deformation direction is compatible,
> rejected, or inconclusive.

Allowed claim:

> DESI DR2 BAO is the correct next external expansion-history gate after
> Pantheon+.

Forbidden claim:

> AOC explains evolving dark energy or the Hubble tension.

## 3. Planck / CMB

Access:

1. Planck Legacy Archive CMB maps:
   `https://wiki.cosmos.esa.int/planck-legacy-archive/index.php/CMB_maps`
2. Planck 2018 cosmological parameter paper and products.

Why it is useful:

Planck provides multiple CMB component-separation products: Commander, NILC,
SEVEM, and SMICA. These are already different reconstruction pipelines applied
to the same sky.

First safe AOC contract:

> Treat the Planck component-separation products as operator/pipeline variants
> and examine which features remain stable across them.

Allowed claim:

> CMB component-separation is a concrete example of observer-bound
> reconstruction with explicit operators and masks.

Forbidden claim:

> The CMB is just a projection artifact.

## 4. Fermi / Gamma-Ray Data

Access:

1. Fermi Science Support Center data products:
   `https://fermi.gsfc.nasa.gov/ssc/data/`
2. LAT data access:
   `https://fermi.gsfc.nasa.gov/ssc/data/access/lat/`
3. NASA Open Data Portal LAT FTP and LAT data server entries.
4. Fermi LAT 14-Year Point Source Catalog, 4FGL-DR4.

Why it is useful:

Fermi is instrument-forward. It has public event/catalog products, caveats,
known exposure issues, source catalogs, energy bands, and transient products.
That makes it a good place to practice apparatus-bound `K`.

First safe AOC contract:

> Use a Fermi catalog or GRB product to define an instrument pipeline with
> energy range, source-detection threshold, uncertainty, and catalog caveats.
> Compute a toy reconstruction budget from published uncertainties or catalog
> thresholds.

Allowed claim:

> Fermi is a good apparatus-bound case study.

Forbidden claim:

> Fermi data currently supports Apparent-Origin Cosmology.

## Recommended First Real-Data Task

Start with Pantheon+ distances, not Fermi.

Reason:

1. direct contact with `D_L(z)`,
2. small enough files,
3. easy CSV-like parsing,
4. directly tied to the existing `K` toy model,
5. easier to explain as a first empirical contract.

Task:

1. Download or vendor the Pantheon+ distance file.
2. Parse redshift and distance-modulus uncertainty.
3. Define a provisional reliability score.
4. Estimate where relative uncertainty crosses a threshold.
5. Report that as a toy `K_P`, with caveats.

## Second Real-Data Task

Use Planck component-separation products conceptually before downloading maps.

Reason:

The maps are large, but the operator/pipeline structure is already documented.
For a first AOC note, it is enough to compare the reconstruction operators:
Commander, NILC, SEVEM, and SMICA.

## Third Real-Data Task

Use Fermi only after deciding the observable:

1. point-source catalog completeness,
2. GRB timing/energy products,
3. diffuse gamma-ray background,
4. source light curves,
5. EBL attenuation studies.

Without choosing one, "Fermi" is too broad.
