#!/usr/bin/env python3
"""Expose coordinate-like metadata from the pinned MoM-BH*-1 prism product.

Diagnostic only. The goal is to distinguish source coordinates from pointing,
slit, WCS, or other instrumental coordinates before cross-matching archives.
No science arrays are uploaded; only small metadata summaries are retained.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import numpy as np
from astropy.io import fits

INPUT = Path("run/raw/mom_prism.fits")
OUTPUT = Path("run/provenance/mom-prism-coordinate-fields.json")


def jsonable(value: Any) -> Any:
    if isinstance(value, (str, int, bool)) or value is None:
        return value
    if isinstance(value, np.integer):
        return int(value)
    if isinstance(value, np.floating):
        return None if not np.isfinite(value) else float(value)
    if isinstance(value, float):
        return None if not np.isfinite(value) else value
    return str(value)


def interesting_header_key(key: str) -> bool:
    key = key.upper()
    tokens = (
        "RA", "DEC", "POS", "TARG", "SRC", "SOURCE", "SLIT", "MSA",
        "CRVAL", "CRPIX", "CTYPE", "CUNIT", "V2", "V3",
    )
    return any(token in key for token in tokens)


def interesting_column(name: str) -> bool:
    lower = name.lower()
    return any(token in lower for token in ("ra", "dec", "src", "source", "id", "slit", "msa"))


def summarize_array(values: Any) -> dict[str, Any]:
    arr = np.asarray(values)
    flat = arr.ravel()
    result: dict[str, Any] = {
        "dtype": str(arr.dtype),
        "shape": list(arr.shape),
    }
    if flat.size == 0:
        return result

    if np.issubdtype(arr.dtype, np.number):
        numeric = np.asarray(flat, dtype=float)
        finite = numeric[np.isfinite(numeric)]
        result["finite_count"] = int(finite.size)
        if finite.size:
            result.update(
                {
                    "min": float(np.min(finite)),
                    "max": float(np.max(finite)),
                    "median": float(np.median(finite)),
                    "first": [float(x) for x in finite[:8]],
                }
            )
    else:
        sample = []
        for value in flat[:20]:
            text = str(value)
            if text not in sample:
                sample.append(text)
            if len(sample) >= 8:
                break
        result["sample"] = sample
    return result


def main() -> None:
    if not INPUT.exists():
        raise RuntimeError(f"Missing pinned MoM prism product: {INPUT}")
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)

    report: dict[str, Any] = {"input": str(INPUT), "hdus": []}
    with fits.open(INPUT, memmap=False) as hdul:
        for index, hdu in enumerate(hdul):
            header_fields = []
            for key in hdu.header:
                if not key or not interesting_header_key(key):
                    continue
                header_fields.append(
                    {
                        "key": key,
                        "value": jsonable(hdu.header.get(key)),
                        "comment": str(hdu.header.comments[key]),
                    }
                )

            columns = []
            if hdu.data is not None and getattr(hdu.data, "names", None):
                for name in hdu.data.names:
                    if interesting_column(name):
                        try:
                            summary = summarize_array(hdu.data[name])
                        except Exception as exc:
                            summary = {"error": f"{type(exc).__name__}: {exc}"}
                        columns.append({"name": name, **summary})

            report["hdus"].append(
                {
                    "index": index,
                    "name": hdu.name,
                    "header_fields": header_fields,
                    "coordinate_like_columns": columns,
                }
            )

    OUTPUT.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
