#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
import math
import re
import shutil
from html.parser import HTMLParser
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


def probe_download(url: str, path: Path, max_bytes: int, timeout: int = 60) -> dict[str, Any]:
    receipt: dict[str, Any] = {"url": url, "status": None, "downloaded": False}
    try:
        with requests.get(url, stream=True, timeout=timeout) as r:
            receipt["status"] = r.status_code
            receipt["content_type"] = r.headers.get("content-type")
            receipt["content_length"] = r.headers.get("content-length")
            if r.status_code != 200:
                return receipt
            declared = int(r.headers.get("content-length") or 0)
            if declared and declared > max_bytes:
                receipt["reason"] = f"declared size {declared} exceeds cap {max_bytes}"
                return receipt
            path.parent.mkdir(parents=True, exist_ok=True)
            written = 0
            with path.open("wb") as f:
                for chunk in r.iter_content(chunk_size=1024 * 1024):
                    if not chunk:
                        continue
                    written += len(chunk)
                    if written > max_bytes:
                        f.close()
                        path.unlink(missing_ok=True)
                        receipt["reason"] = f"stream exceeded cap {max_bytes}"
                        return receipt
                    f.write(chunk)
            receipt["bytes"] = written
            receipt["downloaded"] = True
            receipt["sha256"] = sha256(path)
            return receipt
    except requests.RequestException as exc:
        receipt["error"] = f"{type(exc).__name__}: {exc}"
        return receipt


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
            valid = (
                np.asarray(hdu.data[valid_key], dtype=bool)
                if valid_key
                else np.isfinite(wave) & np.isfinite(flux)
            )
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


def choose_prism(candidates: list[Path], z: float, source_id: str) -> Path:
    hb_um = 0.4861333 * (1 + z)
    scored: list[tuple[float, Path]] = []
    exact_token = f"_{source_id}.spec.fits"
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
        denom = np.where(np.isfinite(err[local]) & (err[local] > 0), err[local], np.nan)
        sn = np.nanmedian(np.abs(flux[local]) / denom)
        if not np.isfinite(sn):
            sn = 0.0
        identity_bonus = 1000.0 if exact_token in path.name else 0.0
        prism_bonus = 5.0 if "prism" in path.name.lower() else 0.0
        scored.append((identity_bonus + prism_bonus + sn, path))
    if not scored:
        raise RuntimeError("No downloaded Zenodo FITS product contained a usable SPEC1D spectrum covering observed H-beta.")
    scored.sort(key=lambda x: x[0], reverse=True)
    chosen = scored[0][1]
    if exact_token not in chosen.name:
        raise RuntimeError(
            f"Zenodo products were readable, but none matched pinned source_id={source_id}; "
            f"best candidate was {chosen.name}."
        )
    return chosen


def parse_dja_rows(text: str) -> list[dict[str, str]]:
    if not text.strip() or text.lstrip().lower().startswith("nothing found"):
        return []
    return list(csv.DictReader(io.StringIO(text)))


class SimpleTableParser(HTMLParser):
    """Extract table cell text and hrefs without third-party HTML dependencies."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.rows: list[list[dict[str, Any]]] = []
        self._row: list[dict[str, Any]] | None = None
        self._parts: list[str] | None = None
        self._hrefs: list[str] | None = None

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        tag = tag.lower()
        if tag == "tr":
            self._row = []
        elif tag in {"td", "th"} and self._row is not None:
            self._parts = []
            self._hrefs = []
        elif tag == "a" and self._parts is not None and self._hrefs is not None:
            href = dict(attrs).get("href")
            if href:
                self._hrefs.append(href)

    def handle_data(self, data: str) -> None:
        if self._parts is not None:
            self._parts.append(data)

    def handle_endtag(self, tag: str) -> None:
        tag = tag.lower()
        if tag in {"td", "th"} and self._row is not None and self._parts is not None:
            text = re.sub(r"\s+", " ", " ".join(self._parts)).strip()
            self._row.append({"text": text, "hrefs": list(self._hrefs or [])})
            self._parts = None
            self._hrefs = None
        elif tag == "tr" and self._row is not None:
            if self._row:
                self.rows.append(self._row)
            self._row = None


def angular_sep_arcsec(ra1: float, dec1: float, ra2: float, dec2: float) -> float:
    dra = (ra1 - ra2) * math.cos(math.radians((dec1 + dec2) / 2.0))
    ddec = dec1 - dec2
    return math.hypot(dra, ddec) * 3600.0


def discover_from_v3_catalog(
    url: str,
    ra: float,
    dec: float,
    radius_arcsec: float,
    program: str,
    grating: str,
    source_id: str,
    prov: Path,
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    response = requests.get(url, timeout=120)
    response.raise_for_status()
    text = response.text

    parser = SimpleTableParser()
    parser.feed(text)

    header_index: int | None = None
    headers: list[str] = []
    for i, row in enumerate(parser.rows):
        values = [cell["text"].strip().lower() for cell in row]
        if {"ra", "dec", "file", "root"}.issubset(set(values)):
            header_index = i
            headers = values
            break

    if header_index is None:
        diag = {
            "url": url,
            "status": response.status_code,
            "bytes": len(response.content),
            "rows_parsed": len(parser.rows),
            "error": "Could not identify ra/dec/file/root header row.",
        }
        (prov / "dja-v3-discovery.json").write_text(json.dumps(diag, indent=2, sort_keys=True))
        return [], diag

    candidates: list[dict[str, Any]] = []
    nearest: list[dict[str, Any]] = []
    for row in parser.rows[header_index + 1 :]:
        if len(row) < len(headers):
            continue
        record = {headers[j]: row[j] for j in range(len(headers))}
        try:
            row_ra = float(record["ra"]["text"])
            row_dec = float(record["dec"]["text"])
        except (KeyError, TypeError, ValueError):
            continue

        root = record.get("root", {}).get("text", "")
        file_name = record.get("file", {}).get("text", "")
        grating_text = record.get("grating", {}).get("text", "")
        srcid = record.get("srcid", {}).get("text", "")
        sep = angular_sep_arcsec(ra, dec, row_ra, row_dec)

        if "excels" not in root.lower():
            continue

        item = {
            "root": root,
            "file": file_name,
            "ra": row_ra,
            "dec": row_dec,
            "sep_arcsec": sep,
            "srcid": srcid,
            "grating_text": grating_text,
            "file_hrefs": record.get("file", {}).get("hrefs", []),
            "fits_hrefs": record.get("fits", {}).get("hrefs", []),
            "source_id_matches_mom": srcid == source_id,
        }
        nearest.append(item)

        file_ok = grating in file_name.lower()
        grating_ok = grating in grating_text.lower()
        program_ok = program in file_name or program in " ".join(item["fits_hrefs"])
        if sep <= radius_arcsec and (file_ok or grating_ok) and program_ok:
            candidates.append(item)

    nearest.sort(key=lambda x: x["sep_arcsec"])
    candidates.sort(key=lambda x: x["sep_arcsec"])
    diag = {
        "url": url,
        "status": response.status_code,
        "bytes": len(response.content),
        "rows_parsed": len(parser.rows),
        "header": headers,
        "target": {"ra": ra, "dec": dec, "radius_arcsec": radius_arcsec},
        "candidates": candidates,
        "nearest_excels_rows": nearest[:10],
    }
    (prov / "dja-v3-discovery.json").write_text(json.dumps(diag, indent=2, sort_keys=True))
    return candidates, diag


def resolve_candidate_url(candidate: dict[str, Any], fallback_template: str) -> tuple[str, str]:
    for href in candidate.get("fits_hrefs", []) + candidate.get("file_hrefs", []):
        if ".spec.fits" in href:
            if href.startswith("http://") or href.startswith("https://"):
                return href, "catalog_href"
            if href.startswith("/"):
                return "https://s3.amazonaws.com" + href, "catalog_href_relative"
    return (
        fallback_template.format(root=candidate["root"], file=candidate["file"]),
        "catalog_root_file",
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", default="provenance/mom_bh1.yaml")
    parser.add_argument("--out", default="run")
    args = parser.parse_args()

    manifest = yaml.safe_load(Path(args.manifest).read_text())
    target = manifest["target"]
    out = Path(args.out)
    raw = out / "raw"
    prov = out / "provenance"
    raw.mkdir(parents=True, exist_ok=True)
    prov.mkdir(parents=True, exist_ok=True)

    z = float(target["redshift"])
    source_id = str(target["source_id"])
    program = str(target["excels_program"])
    grating = str(target["excels_grating"]).lower()
    zenodo_api = manifest["upstream"]["zenodo_api"]
    max_each = int(manifest["acquisition"]["max_file_mb"]) * 1024 * 1024
    max_total = int(manifest["acquisition"]["max_total_mb"]) * 1024 * 1024
    radius = float(manifest["acquisition"]["dja_radius_arcsec"])

    # 1) Resolve the authors' Zenodo record and keep its full metadata as a receipt.
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

    # 2) Select the pinned MoM source, not merely the highest-S/N spectrum.
    prism_source = choose_prism(downloaded, z=z, source_id=source_id)
    prism_path = raw / "mom_prism.fits"
    shutil.copyfile(prism_source, prism_path)

    coords = extract_coords(prism_source)
    if coords is None:
        raise RuntimeError(f"Could not recover sky coordinates from {prism_source.name}.")
    ra, dec = coords

    receipts.append(
        {
            "role": "mom_prism_selected",
            "source_id": source_id,
            "source_file": prism_source.name,
            "local_name": prism_path.name,
            "sha256": sha256(prism_path),
            "ra_deg": ra,
            "dec_deg": dec,
        }
    )

    # 3) Retain DJA's rolling coordinate query as a contemporary archive witness.
    dja_url = manifest["upstream"]["dja_query"].format(
        ra=f"{ra:.8f}",
        dec=f"{dec:.8f}",
        size=radius,
    )
    dja = requests.get(dja_url, timeout=60)
    dja.raise_for_status()
    (prov / "dja-query.csv").write_text(dja.text)
    rows = parse_dja_rows(dja.text)
    rolling_matches = [
        row
        for row in rows
        if program in row.get("file", "")
        and grating in row.get("grating", "").lower()
    ]

    # 4) Discover the historical v3 EXCELS row from the v3 release table by sky
    # position. The EXCELS MSA source id need not equal the MoM source id.
    v3_candidates, _ = discover_from_v3_catalog(
        url=manifest["upstream"]["dja_v3_catalog"],
        ra=ra,
        dec=dec,
        radius_arcsec=max(radius, 1.0),
        program=program,
        grating=grating,
        source_id=source_id,
        prov=prov,
    )

    selected: dict[str, Any] | None = None
    g395m_path = raw / "excels_g395m.fits"
    probe_receipts: list[dict[str, Any]] = []

    for candidate in v3_candidates:
        url, route = resolve_candidate_url(candidate, manifest["upstream"]["dja_file"])
        probe = probe_download(url, g395m_path, max_bytes=max_each)
        probe.update(
            {
                "route": route,
                "root": candidate["root"],
                "file": candidate["file"],
                "sep_arcsec": candidate["sep_arcsec"],
                "srcid": candidate["srcid"],
            }
        )
        probe_receipts.append(probe)
        if probe.get("downloaded"):
            selected = dict(candidate)
            selected["url"] = url
            selected["version"] = "v3"
            selected["selection_note"] = (
                "Selected from DJA nirspec_graded_v3 by sky-position match to the pinned MoM spectrum."
            )
            break

    # 5) If the v3 summary table does not expose a usable link, leave a bounded
    # root-probe matrix as a diagnostic fallback. This is never accepted as
    # identity evidence by itself.
    if selected is None:
        for root in target["excels_roots"]:
            filename = f"{root}_{grating}-f290lp_{program}_{source_id}.spec.fits"
            url = manifest["upstream"]["dja_file"].format(root=root, file=filename)
            probe = probe_download(url, g395m_path, max_bytes=max_each)
            probe.update({"route": "fallback_root_probe", "root": root, "file": filename})
            probe_receipts.append(probe)
            if probe.get("downloaded"):
                selected = {
                    "root": root,
                    "file": filename,
                    "grating": grating,
                    "program": program,
                    "srcid": source_id,
                    "version": root.rsplit("-", 1)[-1],
                    "url": url,
                    "selection_note": (
                        "Fallback root probe; verify against dja-v3-discovery.json before scientific use."
                    ),
                }
                break

    (prov / "dja-probes.json").write_text(json.dumps(probe_receipts, indent=2, sort_keys=True))

    if selected is None or not g395m_path.exists():
        raise RuntimeError(
            f"Could not resolve EXCELS {grating} spectrum near MoM source_id={source_id}. "
            "See dja-v3-discovery.json, dja-query.csv, and dja-probes.json."
        )

    # Reject a syntactically downloadable file that is not actually a spectrum.
    if read_spec1d(g395m_path) is None:
        raise RuntimeError(
            f"Resolved EXCELS file {selected.get('file')} downloaded but is not a readable SPEC1D FITS product."
        )

    receipts.append(
        {
            "role": "excels_g395m_selected",
            "mom_source_id": source_id,
            "excels_srcid": selected.get("srcid"),
            "url": selected["url"],
            "root": selected.get("root"),
            "file": selected.get("file"),
            "version": selected.get("version"),
            "sep_arcsec": selected.get("sep_arcsec"),
            "bytes": g395m_path.stat().st_size,
            "sha256": sha256(g395m_path),
        }
    )

    receipt = {
        "target": target,
        "sources": receipts,
        "selection": {
            "mom_source_id": source_id,
            "prism_candidate": prism_source.name,
            "sky_coordinates_deg": {"ra": ra, "dec": dec},
            "rolling_dja_candidates": rolling_matches,
            "dja_selected": selected,
        },
    }
    (prov / "acquisition-receipt.json").write_text(json.dumps(receipt, indent=2, sort_keys=True))
    print(json.dumps(receipt["selection"]["dja_selected"], indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
