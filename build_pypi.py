#!/usr/bin/env python3
"""Download wheels and build a local PyPI index for piplite.

Creates a pypi/ directory with wheel files and an all.json index that
piplite uses to resolve packages locally, eliminating 404 warnings when
the JupyterLite kernel starts on the live site.

Usage:
    python build_pypi.py [output_dir]

    output_dir defaults to lectures/_build/html/pypi
"""

import datetime
import hashlib
import json
import re
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path

# Packages required by active lectures (see lectures/myst.yml TOC)
# long_run_growth.md:      openpyxl
# inflation_history.md:    xlrd, openpyxl
# french_rev.md:           openpyxl, requests
# markov_chains_I.md:      quantecon_wasm
# markov_chains_II.md:     quantecon_wasm
# eigen_II.md:             quantecon_wasm
# networks.md:             quantecon_wasm, quantecon-book-networks, pandas-datareader
PACKAGES = [
    "openpyxl",
    "requests",
    "xlrd",
    "quantecon_wasm",
    "quantecon-book-networks",
    "pandas-datareader",
]


def download_wheels(packages, dest_dir):
    """Download pure-Python wheels for the given packages (no deps)."""
    subprocess.check_call([
        sys.executable, "-m", "pip", "download",
        "--no-deps",
        "--only-binary=:all:",
        "--dest", str(dest_dir),
        *packages,
    ])


def get_wheel_metadata(whl_path):
    """Extract name, version, and requires_python from a wheel's METADATA."""
    with zipfile.ZipFile(whl_path) as zf:
        for entry in zf.namelist():
            if entry.endswith("/METADATA"):
                text = zf.read(entry).decode("utf-8")
                info = {"requires_python": None}
                for line in text.splitlines():
                    if line.startswith("Name: "):
                        info["name"] = line[6:].strip()
                    elif line.startswith("Version: "):
                        info["version"] = line[9:].strip()
                    elif line.startswith("Requires-Python: "):
                        info["requires_python"] = line[17:].strip()
                    elif line == "":
                        break  # end of headers
                return info
    raise ValueError(f"No METADATA found in {whl_path}")


def build_index(wheel_dir):
    """Build a piplite-compatible all.json index from wheels in a directory."""
    all_json = {}
    now = (
        datetime.datetime.now(tz=datetime.timezone.utc)
        .isoformat()
        .split("+")[0] + "Z"
    )

    for whl_path in sorted(Path(wheel_dir).glob("*.whl")):
        meta = get_wheel_metadata(whl_path)
        whl_bytes = whl_path.read_bytes()
        whl_sha256 = hashlib.sha256(whl_bytes).hexdigest()
        whl_md5 = hashlib.md5(whl_bytes).hexdigest()

        # PEP 503 normalized name
        normalized = re.sub(r"[-_.]+", "-", meta["name"]).lower()

        release = {
            "comment_text": "",
            "digests": {"sha256": whl_sha256, "md5": whl_md5},
            "downloads": -1,
            "filename": whl_path.name,
            "has_sig": False,
            "md5_digest": whl_md5,
            "packagetype": "bdist_wheel",
            "python_version": "py3",
            "requires_python": meta["requires_python"],
            "size": whl_path.stat().st_size,
            "upload_time": now,
            "upload_time_iso_8601": now,
            "url": f"./{whl_path.name}",
            "yanked": False,
            "yanked_reason": None,
        }

        if normalized not in all_json:
            all_json[normalized] = {"releases": {}}
        all_json[normalized]["releases"][meta["version"]] = [release]

    return all_json


def main():
    output_dir = (
        Path(sys.argv[1]) if len(sys.argv) > 1
        else Path("lectures/_build/html/pypi")
    )
    output_dir.mkdir(parents=True, exist_ok=True)

    with tempfile.TemporaryDirectory() as tmpdir:
        print(f"Downloading wheels: {', '.join(PACKAGES)}")
        download_wheels(PACKAGES, tmpdir)

        for whl in sorted(Path(tmpdir).glob("*.whl")):
            dest = output_dir / whl.name
            dest.write_bytes(whl.read_bytes())
            print(f"  {whl.name} ({whl.stat().st_size:,} bytes)")

    index = build_index(output_dir)
    index_path = output_dir / "all.json"
    index_path.write_text(json.dumps(index, indent=2, sort_keys=True))

    total = sum(f.stat().st_size for f in output_dir.glob("*.whl"))
    count = sum(len(v["releases"]) for v in index.values())
    print(f"\nBuilt {index_path} with {count} packages ({total:,} bytes)")


if __name__ == "__main__":
    main()
