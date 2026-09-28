#!/usr/bin/env python3
"""Package the wechat-article-html skill into a release zip archive."""

from __future__ import annotations

import argparse
import hashlib
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# Top-level items to include in the release archive
INCLUDED_PATTERNS = [
    "SKILL.md",
    "README.md",
    "LICENSE",
    "CONTRIBUTING.md",
    "SECURITY.md",
    "THIRD_PARTY_NOTICES.md",
    "requirements.txt",
    "agents/**/*",
    "assets/**/*",
    "references/**/*",
    "scripts/**/*",
    "examples/**/*",
]

EXCLUDED_PATTERNS = {
    "__pycache__",
    ".pytest_cache",
    ".coverage",
    ".DS_Store",
}


def compute_sha256(filepath: Path) -> str:
    hasher = hashlib.sha256()
    with filepath.open("rb") as f:
        while chunk := f.read(65536):
            hasher.update(chunk)
    return hasher.hexdigest()


def package_skill(version: str, output_dir: Path) -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)
    clean_version = version.lstrip("v")
    zip_name = f"wechat-article-html-v{clean_version}.zip"
    zip_path = output_dir / zip_name

    print(f"Creating release package: {zip_path}")
    count = 0

    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for pattern in INCLUDED_PATTERNS:
            for path in ROOT.glob(pattern):
                if not path.is_file():
                    continue
                if any(part in EXCLUDED_PATTERNS for part in path.parts):
                    continue
                if path.suffix in {".pyc", ".pyo"}:
                    continue
                
                # Archive with folder prefix for convenient extraction
                rel_path = path.relative_to(ROOT)
                arcname = f"wechat-article-html/{rel_path.as_posix()}"
                zf.write(path, arcname)
                count += 1

    sha256 = compute_sha256(zip_path)
    sha_path = output_dir / f"{zip_name}.sha256"
    sha_path.write_text(f"{sha256}  {zip_name}\n", encoding="utf-8")

    size_mb = zip_path.stat().st_size / (1024 * 1024)
    print(f"Packaged {count} files ({size_mb:.2f} MB)")
    print(f"SHA-256: {sha256}")
    print(f"Checksum file: {sha_path}")
    return zip_path


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--version", "-v", default="1.0.0", help="Release version (default: 1.0.0)")
    parser.add_argument("--output-dir", "-o", type=Path, default=ROOT / "dist", help="Output directory")
    args = parser.parse_args()

    package_skill(args.version, args.output_dir)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
