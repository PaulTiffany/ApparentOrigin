"""Download the public Pantheon+SH0ES distance table."""

from __future__ import annotations

import hashlib
import urllib.request
from pathlib import Path


DATA_URL = (
    "https://raw.githubusercontent.com/PantheonPlusSH0ES/DataRelease/main/"
    "Pantheon%2B_Data/4_DISTANCES_AND_COVAR/Pantheon%2BSH0ES.dat"
)
COV_URLS = [
    (
        "https://raw.githubusercontent.com/PantheonPlusSH0ES/DataRelease/main/"
        "Pantheon%2B_Data/4_DISTANCES_AND_COVAR/Pantheon%2BSH0ES_STAT%2BSYS.cov"
    ),
    (
        "https://raw.githubusercontent.com/PantheonPlusSH0ES/DataRelease/main/"
        "Pantheon%2B_Data/4_DISTANCES_AND_COVAR/Pantheon%2BSH0ES_STATONLY.cov"
    ),
]

ROOT = Path(__file__).resolve().parents[2]
RAW_DIR = ROOT / "data" / "raw" / "pantheon_plus"
RAW_PATH = RAW_DIR / "Pantheon+SH0ES.dat"
COV_PATH = RAW_DIR / "Pantheon+SH0ES_STAT+SYS.cov"
COV_STAT_PATH = RAW_DIR / "Pantheon+SH0ES_STATONLY.cov"
PROVENANCE_PATH = RAW_DIR / "PROVENANCE.md"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> None:
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    print(f"Downloading {DATA_URL}...")
    urllib.request.urlretrieve(DATA_URL, RAW_PATH)
    data_digest = sha256(RAW_PATH)

    provenance_lines = [
        "# Pantheon+ Data Provenance",
        "",
        f"Distance source URL: {DATA_URL}",
        f"Distance local file: `{RAW_PATH.relative_to(ROOT)}`",
        f"Distance SHA256: `{data_digest}`",
        "",
    ]

    for url in COV_URLS:
        filename = url.split("/")[-1].replace("%2B", "+")
        target = RAW_DIR / filename
        print(f"Downloading {url}...")
        try:
            urllib.request.urlretrieve(url, target)
            digest = sha256(target)
            provenance_lines.extend(
                [
                    f"Covariance source URL: {url}",
                    f"Covariance local file: `{target.relative_to(ROOT)}`",
                    f"Covariance SHA256: `{digest}`",
                    "",
                ]
            )
            print(f"Wrote {target}")
        except Exception as e:
            print(f"Failed to download {url}: {e}")
            continue

    provenance_lines.extend(
        [
            "Repository: https://github.com/PantheonPlusSH0ES/DataRelease",
            "",
        ]
    )
    PROVENANCE_PATH.write_text(
        "\n".join(provenance_lines),
        encoding="utf-8",
    )
    print(f"Wrote {RAW_PATH}")
    print(f"Wrote {PROVENANCE_PATH}")
    print(f"Distance SHA256 {data_digest}")


if __name__ == "__main__":
    main()
