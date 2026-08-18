#!/usr/bin/env python3
"""Build publish and local-font preview samples for every theme."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from convert import THEMES, parse_markdown, render_html
from validate_html import validate_html


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "examples" / "sample.md"
OUTPUT = ROOT / "examples" / "generated"


def main() -> int:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    blocks = parse_markdown(SOURCE.read_text(encoding="utf-8"), SOURCE.parent)
    title = blocks[0].text
    manifest = []
    for key, theme in THEMES.items():
        publish = render_html(blocks, title, key, subtitle=theme.description)
        preview = render_html(
            blocks,
            title,
            key,
            subtitle=theme.description,
            preview_fonts=True,
            font_base="../../assets/fonts",
        )
        publish_errors = validate_html(publish, key)
        preview_errors = validate_html(preview, key, allow_preview=True)
        if publish_errors or preview_errors:
            raise RuntimeError(f"{key}: publish={publish_errors}; preview={preview_errors}")
        publish_path = OUTPUT / f"{key}.html"
        preview_path = OUTPUT / f"{key}.preview.html"
        publish_bytes = publish.encode("utf-8")
        preview_bytes = preview.encode("utf-8")
        publish_path.write_bytes(publish_bytes)
        preview_path.write_bytes(preview_bytes)
        manifest.append(
            {
                "theme": key,
                "name": theme.name,
                "publish": publish_path.name,
                "preview": preview_path.name,
                "sha256": hashlib.sha256(publish_bytes).hexdigest(),
                "bytes": len(publish_bytes),
            }
        )
    (OUTPUT / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"built {len(manifest)} themes in {OUTPUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
