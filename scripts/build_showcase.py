#!/usr/bin/env python3
"""Build a 10-theme showcase from one Word/Markdown input."""

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
        publish = render_html(remaining, title, key, subtitle=subtitle)
        preview = render_html(
            remaining,
            title,
            key,
            subtitle=subtitle,
            preview_fonts=True,
            font_base="../../assets/fonts",
        )
        publish_errors = validate_html(publish, key)
        preview_errors = validate_html(preview, key, allow_preview=True)
        if publish_errors or preview_errors:
            raise RuntimeError(f"{key}: publish={publish_errors}; preview={preview_errors}")
        publish_bytes = publish.encode("utf-8")
        preview_bytes = preview.encode("utf-8")
        publish_path = output / f"{key}.html"
        preview_path = output / f"{key}.preview.html"
        publish_path.write_bytes(publish_bytes)
        preview_path.write_bytes(preview_bytes)
        manifest["themes"].append(
            {
                "key": key,
                "name": theme.name,
                "publish": publish_path.name,
                "preview": preview_path.name,
                "bytes": len(publish_bytes),
                "sha256": hashlib.sha256(publish_bytes).hexdigest(),
            }
        )
    (output / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    readme_lines = [
        "# mRNA 体内细胞治疗主题展示",
        "",
        f"源文档：`{source.name}`。共生成 {len(THEMES)} 个主题；发布版 HTML 不含 `<style>`、外链图片或脚本。",
        "",
        "| 主题 | 发布版 | 本地字体预览 | README 面板 |",
        "|---|---|---|---|",
    ]
    for key, theme in THEMES.items():
        readme_lines.append(f"| {theme.name} (`{key}`) | [{key}.html]({key}.html) | [{key}.preview.html]({key}.preview.html) | `panels/{key}.png` |")
    (output / "README.md").write_text("\n".join(readme_lines) + "\n", encoding="utf-8")
    print(f"built {len(THEMES)} themes in {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
