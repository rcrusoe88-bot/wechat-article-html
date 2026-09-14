#!/usr/bin/env python3
"""Build the WeChat-native showcase from one Word/Markdown input."""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter
from pathlib import Path

from convert import THEMES, read_input, render_html
from validate_html import validate_html


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    source = args.input.resolve()
    output = args.output.resolve()
    blocks, document_title = read_input(source)
    title = next((block.text for block in blocks if block.kind == "heading" and block.level == 1), None) or document_title or source.stem
    subtitle = ""
    remaining = list(blocks)
    if remaining and remaining[0].kind == "heading" and remaining[0].level == 1:
        remaining.pop(0)
    if remaining and remaining[0].kind == "paragraph" and remaining[0].text.startswith("副标题："):
        subtitle = remaining.pop(0).text.removeprefix("副标题：").strip()

    output.mkdir(parents=True, exist_ok=True)
    manifest = {
        "source": str(source),
        "title": title,
        "subtitle": subtitle,
        "blocks": dict(Counter(block.kind for block in remaining)),
        "themes": [],
    }
    for key, theme in THEMES.items():
        # Keep committed examples aligned with the only public CLI output.
        wechat = render_html(remaining, title, key, subtitle=subtitle, wechat_mode=True)
        wechat_errors = validate_html(wechat, key)
        if wechat_errors:
            raise RuntimeError(f"{key}: wechat={wechat_errors}")
        wechat_bytes = wechat.encode("utf-8")
        wechat_path = output / f"{key}.wechat.html"
        for stale_name in (f"{key}.html", f"{key}.preview.html"):
            (output / stale_name).unlink(missing_ok=True)
        wechat_path.write_bytes(wechat_bytes)
        manifest["themes"].append(
            {
                "key": key,
                "name": theme.name,
                "wechat": wechat_path.name,
                "bytes": len(wechat_bytes),
                "sha256": hashlib.sha256(wechat_bytes).hexdigest(),
            }
        )
    (output / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    readme_lines = [
        "# anything-to-html 主题展示",
        "",
        f"源文档：`{source.name}`。只生成微信公众号版，不声明 `font-family`，粘贴后跟随微信读者端原生字体。共生成 {len(THEMES)} 个主题，不含外链图片或脚本。",
        "",
        "| 主题 | 微信公众号版 |",
        "|---|---|",
    ]
    for key, theme in THEMES.items():
        readme_lines.append(
            f"| {theme.name} (`{key}`) | [{key}.wechat.html]({key}.wechat.html) |"
        )
    (output / "README.md").write_text("\n".join(readme_lines) + "\n", encoding="utf-8")
    print(f"built {len(THEMES)} themes in {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
