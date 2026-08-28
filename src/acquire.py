#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
import math
import shutil
from pathlib import Path
from typing import Any

import numpy as np
import requests
import yaml
from astropy.io import fits
from astropy.table import Table


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def download_limited(url: str, path: Path, max_bytes: int, timeout: int = 120) -> dict[str, Any]:
    """Download one public upstream object with a hard size cap and receipt."""
    receipt: dict[str, Any] = {"url": url, "status": None, "downloaded": False}
    path.parent.mkdir(parents=True, exist_ok=True)
    try:
        with requests.get(url, stream=True, timeout=timeout) as response:
            receipt["status"] = response.status_code
            receipt["content_type"] = response.headers.get("content-type")
            receipt["content_length"] = response.headers.get("content-length")
            response.raise_for_status()
            declared = int(response.headers.get("content-length") or 0)
            if declared and declared > max_bytes:
                raise RuntimeError(f"Upstream object declares {declared} bytes, above cap {max_bytes}: {url}")

            written = 0
            with path.open("wb") as f:
                for chunk in response.iter_content(chunk_size=1024 * 1024):
                    if not chunk:
                        continue
                    written += len(chunk)
                    if written > max_bytes:
                        f.close()
                        path.unlink(missing_ok=True)
                        raise RuntimeError(f"Upstream object exceeded cap {max_bytes} while streaming: {url}")
                    f.write(chunk)

        receipt.update(
            {
                "downloaded": True,
                "bytes": path.stat().st_size,
                "sha256": sha256(path),
            }
        )
        return receipt
    except Exception as exc:
        path.unlink(missing_ok=True)
        receipt["error"] = f"{type(exc).__name__}: {exc}"
        return receipt


def spec1d_hdu(path: Path):
    hdul = fits.open(path, memmap=False)
    hdu = next((h for h in hdul if h.name.upper() == "SPEC1D" and h.data is not None), None)
    if hdu is None or not getattr(hdu.data, "names", None):
        hdul.close()
        raise RuntimeError(f"{path} has no readable SPEC1D binary table")
    return hdul, hdu


def read_spec1d(path: Path) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    hdul, hdu = spec1d_hdu(path)
    try:
        names = {name.lower(): name for name in hdu.data.names}
        if "wave" not in names or "flux" not in names:
            raise RuntimeError(f"{path} SPEC1D is missing wave/flux columns")
        wave = np.asarray(hdu.data[names["wave"]], dtype=float)
        flux = np.asarray(hdu.data[names["flux"]], dtype=float)
        err_key = names.get("full_err") or names.get("err")
        err = np.asarray(hdu.data[err_key], dtype=float) if err_key else np.full_like(flux, np.nan)
        valid_key = names.get("valid")
        valid = (
            np.asarray(hdu.data[valid_key], dtype=bool)
            if valid_key
            else np.isfinite(wave) & np.isfinite(flux)
        )
        return wave, flux, err, valid
    finally:
        hdul.close()


def extract_coords(path: Path) -> tuple[float, float] | None:
    header_pairs = [
        ("SRCRA", "SRCDEC"),
        ("SRC_RA", "SRC_DEC"),
        ("RA_TARG", "DEC_TARG"),
        ("TARG_RA", "TARG_DEC"),
        ("RA", "DEC"),
    ]
    try:
        with fits.open(path, memmap=False) as hdul:
            for hdu in hdul:
                for ra_key, dec_key in header_pairs:
                    if ra_key in hdu.header and dec_key in hdu.header:
                        ra = float(hdu.header[ra_key])
                        dec = float(hdu.header[dec_key])
                        if np.isfinite(ra) and np.isfinite(dec):
                            return ra, dec
                if hdu.data is not None and getattr(hdu.data, "names", None):
                    names = {name.lower(): name for name in hdu.data.names}
                    for ra_key, dec_key in [("srcra", "srcdec"), ("ra", "dec")]:
                        if ra_key in names and dec_key in names:
                            ra = np.asarray(hdu.data[names[ra_key]], dtype=float).ravel()
                            dec = np.asarray(hdu.data[names[dec_key]], dtype=float).ravel()
                            mask = np.isfinite(ra) & np.isfinite(dec)
                            if mask.any():
                                return float(np.nanmedian(ra[mask])), float(np.nanmedian(dec[mask]))
    except Exception:
        return None
    return None


def choose_prism(candidates: list[Path], z: float, source_id: str) -> Path:
    """Select the pinned MoM source, never merely a convenient spectrum."""
    observed_hbeta = 0.4861333 * (1 + z)
    exact_token = f"_{source_id}.spec.fits"
    matches: list[Path] = []
    for path in candidates:
        if exact_token not in path.name:
            continue
        try:
            wave, flux, _, valid = read_spec1d(path)
        except Exception:
            continue
        local = valid & np.isfinite(flux) & (np.abs(wave - observed_hbeta) < 0.08)
        if local.sum() >= 8:
            matches.append(path)
    if len(matches) != 1:
        raise RuntimeError(
            f"Expected exactly one usable Zenodo spectrum for pinned source_id={source_id}; "
            f"found {[p.name for p in matches]}"
        )
    return matches[0]


def angular_sep_arcsec(ra1: float, dec1: float, ra2: float, dec2: float) -> float:
    dra = (ra1 - ra2) * math.cos(math.radians((dec1 + dec2) / 2.0))
    ddec = dec1 - dec2
    return math.hypot(dra, ddec) * 3600.0


def scalar(row: Any, columns: dict[str, str], key: str, default: Any = None) -> Any:
    actual = columns.get(key.lower())
    if actual is None:
        return default
    value = row[actual]
    if np.ma.is_masked(value):
        return default
    if isinstance(value, np.generic):
        return value.item()
    return value


def discover_excels_v3(
    catalog_path: Path,
    ra: float,
    dec: float,
    radius_arcsec: float,
    program: str,
    grating: str,
) -> tuple[dict[str, Any], list[dict[str, Any]], dict[str, Any]]:
    """Resolve the exact historical EXCELS spectrum from DJA's frozen v3 ECSV."""
    table = Table.read(catalog_path, format="ascii.ecsv")
    columns = {name.lower(): name for name in table.colnames}
    required = {"ra", "dec", "root", "file", "grating"}
    missing = sorted(required - set(columns))
    if missing:
        raise RuntimeError(f"DJA v3 ECSV missing required columns: {missing}; has {table.colnames}")

    near_excels: list[dict[str, Any]] = []
    candidates: list[dict[str, Any]] = []
    for row in table:
        root = str(scalar(row, columns, "root", ""))
        if "excels" not in root.lower():
            continue
        try:
            row_ra = float(scalar(row, columns, "ra"))
            row_dec = float(scalar(row, columns, "dec"))
        except (TypeError, ValueError):
            continue
        sep = angular_sep_arcsec(ra, dec, row_ra, row_dec)
        if sep > 5.0:
            continue

        file_name = str(scalar(row, columns, "file", ""))
        grating_value = str(scalar(row, columns, "grating", ""))
        item = {
            "root": root,
            "file": file_name,
            "ra": row_ra,
            "dec": row_dec,
            "sep_arcsec": sep,
            "srcid": str(scalar(row, columns, "srcid", "")),
            "grating": grating_value,
            "filter": str(scalar(row, columns, "filter", "")),
            "grade": scalar(row, columns, "grade"),
            "z": scalar(row, columns, "z"),
        }
        near_excels.append(item)

        if sep <= radius_arcsec and grating.lower() in grating_value.lower() and program in file_name:
            candidates.append(item)

    near_excels.sort(key=lambda item: item["sep_arcsec"])
    candidates.sort(
        key=lambda item: (
            item["sep_arcsec"],
            -float(item["grade"]) if item.get("grade") not in (None, "") else 0.0,
        )
    )
    if not candidates:
        raise RuntimeError(
            f"DJA v3 ECSV contains no EXCELS {grating} program-{program} row within "
            f"{radius_arcsec:.2f} arcsec of RA={ra:.8f}, Dec={dec:.8f}. "
            f"Nearest EXCELS rows: {near_excels[:5]}"
        )

    selected = candidates[0]
    diagnostic = {
        "catalog_rows": len(table),
        "catalog_columns": table.colnames,
        "target": {"ra": ra, "dec": dec, "radius_arcsec": radius_arcsec},
        "candidate_count": len(candidates),
        "candidates": candidates,
        "nearest_excels_rows": near_excels[:10],
        "selected": selected,
    }
    return selected, candidates, diagnostic


def parse_current_dja(text: str) -> list[dict[str, str]]:
    if not text.strip() or text.lstrip().lower().startswith("nothing found"):
        return []
    return list(csv.DictReader(io.StringIO(text)))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", default="provenance/mom_bh1.yaml")
    parser.add_argument("--out", default="run")
    args = parser.parse_args()

    manifest = yaml.safe_load(Path(args.manifest).read_text())
    target = manifest["target"]
    upstream = manifest["upstream"]
    acquisition = manifest["acquisition"]

    out = Path(args.out)
    raw = out / "raw"
    provenance = out / "provenance"
    raw.mkdir(parents=True, exist_ok=True)
    provenance.mkdir(parents=True, exist_ok=True)

    z = float(target["redshift"])
    source_id = str(target["source_id"])
    program = str(target["excels_program"])
    grating = str(target["excels_grating"]).lower()
    max_each = int(acquisition["max_file_mb"]) * 1024 * 1024
    max_total = int(acquisition["max_total_mb"]) * 1024 * 1024
    radius = max(float(acquisition["dja_radius_arcsec"]), 1.0)

    receipts: list[dict[str, Any]] = []

    # Authors' public MoM release. Keep the record metadata, not the science blobs.
    record_response = requests.get(upstream["zenodo_api"], timeout=60)
    record_response.raise_for_status()
    record = record_response.json()
    (provenance / "zenodo-record.json").write_text(json.dumps(record, indent=2, sort_keys=True))

    zenodo_candidates: list[Path] = []
    total = 0
    for item in record.get("files", []):
        key = str(item.get("key", ""))
        size = int(item.get("size") or 0)
        if not key.lower().endswith((".fits", ".fits.gz")):
            continue
        if size > max_each or total + size > max_total:
            continue
        url = item.get("links", {}).get("content") or item.get("links", {}).get("self")
        if not url:
            continue
        dest = raw / "zenodo" / Path(key).name
        receipt = download_limited(url, dest, max_each)
        receipt.update({"role": "zenodo_prism_candidate", "key": key})
        receipts.append(receipt)
        if receipt.get("downloaded"):
            total += dest.stat().st_size
            zenodo_candidates.append(dest)

    prism_source = choose_prism(zenodo_candidates, z=z, source_id=source_id)
    prism_path = raw / "mom_prism.fits"
    shutil.copyfile(prism_source, prism_path)
    coords = extract_coords(prism_source)
    if coords is None:
        raise RuntimeError(f"Could not recover coordinates from pinned MoM spectrum {prism_source.name}")
    ra, dec = coords
    receipts.append(
        {
            "role": "mom_prism_selected",
            "source_id": source_id,
            "source_file": prism_source.name,
            "sha256": sha256(prism_path),
            "bytes": prism_path.stat().st_size,
            "ra_deg": ra,
            "dec_deg": dec,
        }
    )

    # Contemporary DJA coordinate query is an independent witness only. The
    # endpoint currently tracks the rolling release, while the paper used v3.
    current_url = upstream["dja_query"].format(ra=f"{ra:.8f}", dec=f"{dec:.8f}", size=radius)
    current = requests.get(current_url, timeout=60)
    current.raise_for_status()
    (provenance / "dja-current-query.csv").write_text(current.text)
    current_rows = parse_current_dja(current.text)

    # Frozen v3 machine-readable catalog used to identify the historical EXCELS
    # extraction by sky position. Do not assume MoM and EXCELS share source IDs.
    catalog_path = raw / "nirspec_graded_v3.ecsv"
    catalog_receipt = download_limited(upstream["dja_v3_catalog_ecsv"], catalog_path, max_total)
    catalog_receipt["role"] = "dja_v3_catalog"
    receipts.append(catalog_receipt)
    if not catalog_receipt.get("downloaded"):
        (provenance / "acquisition-partial.json").write_text(json.dumps({"sources": receipts}, indent=2, sort_keys=True))
        raise RuntimeError(
            "Could not retrieve DJA frozen v3 ECSV catalog. "
            f"Receipt: {catalog_receipt}"
        )

    selected, candidates, diagnostic = discover_excels_v3(
        catalog_path=catalog_path,
        ra=ra,
        dec=dec,
        radius_arcsec=radius,
        program=program,
        grating=grating,
    )
    diagnostic["catalog"] = {
        "url": upstream["dja_v3_catalog_ecsv"],
        "sha256": catalog_receipt.get("sha256"),
        "bytes": catalog_receipt.get("bytes"),
    }
    (provenance / "dja-v3-selection.json").write_text(json.dumps(diagnostic, indent=2, sort_keys=True, default=str))

    g395m_url = upstream["dja_file"].format(root=selected["root"], file=selected["file"])
    g395m_path = raw / "excels_g395m.fits"
    g395m_receipt = download_limited(g395m_url, g395m_path, max_each)
    g395m_receipt.update(
        {
            "role": "excels_g395m_selected",
            "root": selected["root"],
            "file": selected["file"],
            "excels_srcid": selected.get("srcid"),
            "sep_arcsec": selected["sep_arcsec"],
        }
    )
    receipts.append(g395m_receipt)
    if not g395m_receipt.get("downloaded"):
        (provenance / "acquisition-partial.json").write_text(json.dumps({"sources": receipts}, indent=2, sort_keys=True, default=str))
        raise RuntimeError(f"DJA catalog resolved an exact EXCELS row, but its FITS download failed: {g395m_receipt}")

    # Validate that archive identity and bytes agree on basic scientific content.
    wave, _, _, _ = read_spec1d(g395m_path)
    observed_hbeta = 0.4861333 * (1 + z)
    if not (np.nanmin(wave) <= observed_hbeta <= np.nanmax(wave)):
        raise RuntimeError(
            f"Resolved EXCELS spectrum does not cover observed H-beta at {observed_hbeta:.4f} um: "
            f"range={np.nanmin(wave):.4f}-{np.nanmax(wave):.4f} um"
        )

    receipt = {
        "target": target,
        "sources": receipts,
        "selection": {
            "mom_source_id": source_id,
            "sky_coordinates_deg": {"ra": ra, "dec": dec},
            "current_dja_rows": len(current_rows),
            "v3_candidate_count": len(candidates),
            "excels_selected": selected,
        },
    }
    (provenance / "acquisition-receipt.json").write_text(json.dumps(receipt, indent=2, sort_keys=True, default=str))
    print(json.dumps(receipt["selection"]["excels_selected"], indent=2, sort_keys=True, default=str))


if __name__ == "__main__":
    main()
