$ErrorActionPreference = "Stop"

$MapDir = "data/raw/planck_operator_residue/maps"
New-Item -ItemType Directory -Force -Path $MapDir | Out-Null

$Base = "https://irsa.ipac.caltech.edu/data/Planck/release_3/all-sky-maps/maps/component-maps/cmb"
$Maps = @(
  "COM_CMB_IQU-commander_2048_R3.00_full.fits",
  "COM_CMB_IQU-nilc_2048_R3.00_full.fits",
  "COM_CMB_IQU-sevem_2048_R3.00_full.fits",
  "COM_CMB_IQU-smica_2048_R3.00_full.fits"
)

foreach ($Name in $Maps) {
  $Out = Join-Path $MapDir $Name
  $Url = "$Base/$Name"
  if (Test-Path $Out) {
    $Size = (Get-Item $Out).Length
    if ($Size -gt 100000000) {
      Write-Host "Skipping existing $Name ($Size bytes)"
      continue
    }
  }
  Write-Host "Downloading $Name"
  curl.exe -L --fail --retry 5 --retry-delay 10 -o $Out $Url
}

Get-ChildItem $MapDir | Select-Object Name, Length

