#!/usr/bin/env python3
"""Build the WeChat-native sample for every theme."""

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
        # Generated examples must match the only public CLI output.
        wechat = render_html(blocks, title, key, subtitle=theme.description, wechat_mode=True)
        wechat_errors = validate_html(wechat, key)
        if wechat_errors:
            raise RuntimeError(f"{key}: wechat={wechat_errors}")
        wechat_path = OUTPUT / f"{key}.wechat.html"
        wechat_bytes = wechat.encode("utf-8")
        for stale_name in (f"{key}.html", f"{key}.preview.html"):
            (OUTPUT / stale_name).unlink(missing_ok=True)
        wechat_path.write_bytes(wechat_bytes)
        manifest.append(
            {
                "theme": key,
                "name": theme.name,
                "wechat": wechat_path.name,
                "sha256": hashlib.sha256(wechat_bytes).hexdigest(),
                "bytes": len(wechat_bytes),
            }
        )
    (OUTPUT / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"built {len(manifest)} themes in {OUTPUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
