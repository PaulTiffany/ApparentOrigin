#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
import shutil
from pathlib import Path
from typing import Any

import numpy as np
import requests
import yaml
from astropy.io import fits


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def download(url: str, path: Path, timeout: int = 120) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with requests.get(url, stream=True, timeout=timeout) as r:
        r.raise_for_status()
        with path.open("wb") as f:
            for chunk in r.iter_content(chunk_size=1024 * 1024):
                if chunk:
                    f.write(chunk)


def read_spec1d(path: Path) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray] | None:
    try:
        with fits.open(path, memmap=False) as hdul:
            hdu = next((h for h in hdul if h.name.upper() == "SPEC1D" and h.data is not None), None)
            if hdu is None or not getattr(hdu.data, "names", None):
                return None
            names = {n.lower(): n for n in hdu.data.names}
            if "wave" not in names or "flux" not in names:
                return None
            wave = np.asarray(hdu.data[names["wave"]], dtype=float)
            flux = np.asarray(hdu.data[names["flux"]], dtype=float)
            err_key = names.get("full_err") or names.get("err")
            err = np.asarray(hdu.data[err_key], dtype=float) if err_key else np.full_like(flux, np.nan)
            valid_key = names.get("valid")
            valid = np.asarray(hdu.data[valid_key], dtype=bool) if valid_key else np.isfinite(wave) & np.isfinite(flux)
            return wave, flux, err, valid
    except Exception:
        return None


def extract_coords(path: Path) -> tuple[float, float] | None:
    header_pairs = [
        ("RA", "DEC"),
        ("RA_TARG", "DEC_TARG"),
        ("TARG_RA", "TARG_DEC"),
        ("SRC_RA", "SRC_DEC"),
        ("SRCRA", "SRCDEC"),
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
                    names = {n.lower(): n for n in hdu.data.names}
                    for ra_key, dec_key in [("ra", "dec"), ("srcra", "srcdec")]:
                        if ra_key in names and dec_key in names:
                            ra = np.asarray(hdu.data[names[ra_key]], dtype=float).ravel()
                            dec = np.asarray(hdu.data[names[dec_key]], dtype=float).ravel()
                            mask = np.isfinite(ra) & np.isfinite(dec)
                            if mask.any():
                                return float(np.nanmedian(ra[mask])), float(np.nanmedian(dec[mask]))
    except Exception:
        return None
    return None


def choose_prism(candidates: list[Path], z: float) -> Path:
    hb_um = 0.4861333 * (1 + z)
    scored: list[tuple[float, Path]] = []
    for path in candidates:
        spec = read_spec1d(path)
        if spec is None:
            continue
        wave, flux, err, valid = spec
        if not (np.nanmin(wave) <= hb_um <= np.nanmax(wave)):
            continue
        local = valid & np.isfinite(flux) & (np.abs(wave - hb_um) < 0.08)
        if local.sum() < 8:
            continue
        sn = np.nanmedian(np.abs(flux[local]) / np.where(np.isfinite(err[local]) & (err[local] > 0), err[local], np.nan))
        if not np.isfinite(sn):
            sn = 0.0
        name_bonus = 5.0 if "prism" in path.name.lower() else 0.0
        scored.append((name_bonus + sn, path))
    if not scored:
        raise RuntimeError("No downloaded Zenodo FITS product contained a usable SPEC1D spectrum covering observed H-beta.")
    scored.sort(key=lambda x: x[0], reverse=True)
    return scored[0][1]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", default="provenance/mom_bh1.yaml")
    parser.add_argument("--out", default="run")
    args = parser.parse_args()

    manifest = yaml.safe_load(Path(args.manifest).read_text())
    out = Path(args.out)
    raw = out / "raw"
    prov = out / "provenance"
    raw.mkdir(parents=True, exist_ok=True)
    prov.mkdir(parents=True, exist_ok=True)

    z = float(manifest["target"]["redshift"])
    zenodo_api = manifest["upstream"]["zenodo_api"]
    max_each = int(manifest["acquisition"]["max_file_mb"]) * 1024 * 1024
    max_total = int(manifest["acquisition"]["max_total_mb"]) * 1024 * 1024

    record = requests.get(zenodo_api, timeout=60)
    record.raise_for_status()
    record_json: dict[str, Any] = record.json()
    (prov / "zenodo-record.json").write_text(json.dumps(record_json, indent=2, sort_keys=True))

    downloaded: list[Path] = []
    receipts: list[dict[str, Any]] = []
    total = 0

    for item in record_json.get("files", []):
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
        download(url, dest)
        total += dest.stat().st_size
        downloaded.append(dest)
        receipts.append(
            {
                "role": "zenodo_prism_candidate",
                "key": key,
                "url": url,
                "bytes": dest.stat().st_size,
                "sha256": sha256(dest),
            }
        )

    if not downloaded:
        raise RuntimeError("Zenodo record returned no FITS products within the configured size caps.")

    prism_source = choose_prism(downloaded, z=z)
    prism_path = raw / "mom_prism.fits"
    shutil.copyfile(prism_source, prism_path)

    coords = extract_coords(prism_source)
    if coords is None:
        raise RuntimeError(f"Could not recover sky coordinates from {prism_source.name}; cannot query DJA.")
    ra, dec = coords

    dja_url = manifest["upstream"]["dja_query"].format(
        ra=f"{ra:.8f}",
        dec=f"{dec:.8f}",
        size=manifest["acquisition"]["dja_radius_arcsec"],
    )
    dja = requests.get(dja_url, timeout=60)
    dja.raise_for_status()
    (prov / "dja-query.csv").write_text(dja.text)

    rows = list(csv.DictReader(io.StringIO(dja.text)))
    program = str(manifest["target"]["excels_program"])
    grating = manifest["target"]["excels_grating"].lower()
    matches = [
        row
        for row in rows
        if program in row.get("file", "")
        and grating in row.get("grating", "").lower()
    ]
    if not matches:
        raise RuntimeError(
            f"DJA returned no {grating} extraction for program {program} near RA={ra}, Dec={dec}. "
            "See run/provenance/dja-query.csv."
        )

    def rank(row: dict[str, str]) -> tuple[int, float]:
        root = row.get("root", "")
        preferred = 1 if root.endswith("-v3") else 0
        try:
            sn = float(row.get("sn50", "nan"))
        except ValueError:
            sn = float("nan")
        return preferred, sn if np.isfinite(sn) else -1.0

    matches.sort(key=rank, reverse=True)
    selected = matches[0]
    dja_file = selected["file"]
    dja_root = selected["root"]
    dja_file_url = manifest["upstream"]["dja_file"].format(root=dja_root, file=dja_file)
    g395m_path = raw / "excels_g395m.fits"
    download(dja_file_url, g395m_path)

    receipts.append(
        {
            "role": "mom_prism_selected",
            "source_file": prism_source.name,
            "local_name": prism_path.name,
            "sha256": sha256(prism_path),
            "ra_deg": ra,
            "dec_deg": dec,
        }
    )
    receipts.append(
        {
            "role": "excels_g395m_selected",
            "url": dja_file_url,
            "root": dja_root,
            "file": dja_file,
            "version": selected.get("version"),
            "z_catalog": selected.get("z"),
            "bytes": g395m_path.stat().st_size,
            "sha256": sha256(g395m_path),
        }
    )

    receipt = {
        "target": manifest["target"],
        "sources": receipts,
        "selection": {
            "prism_candidate": prism_source.name,
            "sky_coordinates_deg": {"ra": ra, "dec": dec},
            "dja_candidates": matches,
            "dja_selected": selected,
        },
    }
    (prov / "acquisition-receipt.json").write_text(json.dumps(receipt, indent=2, sort_keys=True))
    print(json.dumps(receipt["selection"]["dja_selected"], indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
