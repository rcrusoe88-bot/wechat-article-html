#!/usr/bin/env python3
"""Validate generated WeChat HTML and theme invariants."""

from __future__ import annotations

import argparse
import re
from html.parser import HTMLParser
from pathlib import Path

from convert import LAYOUT_VERSION, THEMES, canonical_theme


VOID_TAGS = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "param", "source", "track", "wbr"}
STYLE_REQUIRED = {
    "a", "blockquote", "code", "div", "figure", "footer", "h1", "h2", "h3",
    "header", "img", "li", "main", "ol", "p", "pre", "section", "span", "table", "td", "th", "ul",
}


class AuditParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.stack: list[str] = []
        self.errors: list[str] = []
        self.attrs_by_tag: list[tuple[str, dict[str, str]]] = []
        self.comments: list[str] = []
        self.style_blocks = 0
        self.script_blocks = 0

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        tag = tag.lower()
        attr_map = {key.lower(): value or "" for key, value in attrs}
        self.attrs_by_tag.append((tag, attr_map))
        if tag == "style":
            self.style_blocks += 1
        if tag == "script":
            self.script_blocks += 1
        for name in attr_map:
            if name.startswith("on"):
                self.errors.append(f"event handler attribute found: {tag}[{name}]")
        if tag in STYLE_REQUIRED and "style" not in attr_map:
            self.errors.append(f"visible element missing inline style: <{tag}>")
        if tag not in VOID_TAGS:
            self.stack.append(tag)

    def handle_startendtag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        self.handle_starttag(tag, attrs)
        if tag.lower() not in VOID_TAGS and self.stack and self.stack[-1] == tag.lower():
            self.stack.pop()

    def handle_endtag(self, tag: str) -> None:
        tag = tag.lower()
        if tag in VOID_TAGS:
            return
        if not self.stack:
            self.errors.append(f"unexpected closing tag: </{tag}>")
            return
        if self.stack[-1] != tag:
            self.errors.append(f"mismatched closing tag: expected </{self.stack[-1]}>, got </{tag}>")
            if tag in self.stack:
                while self.stack and self.stack[-1] != tag:
                    self.stack.pop()
                if self.stack:
                    self.stack.pop()
            return
        self.stack.pop()

    def handle_comment(self, data: str) -> None:
        self.comments.append(data.strip())


def validate_html(
    document: str,
    theme: str | None = None,
) -> list[str]:
    errors: list[str] = []
    parser = AuditParser()
    try:
        parser.feed(document)
        parser.close()
    except Exception as exc:
        return [f"HTML parser error: {exc}"]
    errors.extend(parser.errors)
    if parser.stack:
        errors.append(f"unclosed tags: {', '.join(parser.stack[-5:])}")

    lower = document.lower()
    if parser.script_blocks or "javascript:" in lower:
        errors.append("scripts or javascript URLs are not allowed")
    if parser.style_blocks:
        errors.append("style block found in WeChat output")
    if any(marker in document for marker in ('data-preview-fonts="true"', 'data-embedded-fonts="true"')):
        errors.append("font mode marker found in WeChat output")

    tags = parser.attrs_by_tag
    body_attrs = next((attrs for tag, attrs in tags if tag == "body"), {})
    body_style = body_attrs.get("style", "")
    if "max-width:677px" not in body_style.replace(" ", ""):
        errors.append("body must use max-width: 677px")
    if body_attrs.get("data-layout-version") != LAYOUT_VERSION:
        errors.append(f"body data-layout-version must be {LAYOUT_VERSION}")
    if re.search(r"font-family\s*:", document, re.IGNORECASE):
        errors.append("WeChat output must not declare font-family")
    if "Caveat" in document or "XuanZongTi" in document:
        errors.append("WeChat output must not reference custom fonts")

    for tag, attrs in tags:
        if tag == "img":
            src = attrs.get("src", "")
            if not src.startswith("data:image/"):
                errors.append(f"non-base64 image source found: {src[:80] or '<missing>'}")
        if tag == "link" and attrs.get("rel", "").lower() == "stylesheet":
            errors.append("external stylesheet link found")
        if tag in {"thead", "tbody"}:
            errors.append(f"WeChat-incompatible table tag found: <{tag}>")
        if tag == "tr" and "style" in attrs:
            errors.append("table row styles must be placed on th/td")

    history_items = sum(1 for tag, attrs in tags if tag == "div" and attrs.get("data-history-item"))
    if history_items != 3:
        errors.append(f"expected 3 historical article placeholders, found {history_items}")
    qr_images = [attrs for tag, attrs in tags if tag == "img" and attrs.get("data-qr-code") == "true"]
    if not qr_images:
        errors.append("QR module must contain an image")
    elif not qr_images[0].get("src", "").startswith("data:image/"):
        errors.append("QR module must use a base64 image")
    elif "width:144px" not in qr_images[0].get("style", "").replace(" ", "") or "height:144px" not in qr_images[0].get("style", "").replace(" ", ""):
        errors.append("QR image must preserve its 144px by 144px layout contract")
    if not any(tag == "footer" and attrs.get("data-fixed-footer") == "true" for tag, attrs in tags):
        errors.append("fixed footer module is missing")

    if theme:
        try:
            key = canonical_theme(theme)
        except ValueError as exc:
            errors.append(str(exc))
        else:
            contract = THEMES[key]
            if body_attrs.get("data-theme") != key:
                errors.append(f"body data-theme must be {key}")
            for token, label in (
                (contract.primary, "primary color"),
                (contract.background, "page background"),
                (contract.surface, "surface color"),
            ):
                if token not in document:
                    errors.append(f"theme {key} missing {label} {token}")

    return list(dict.fromkeys(errors))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("html_file", type=Path)
    parser.add_argument("--theme", choices=sorted(THEMES))
    args = parser.parse_args()
    document = args.html_file.read_text(encoding="utf-8")
    errors = validate_html(document, args.theme)
    if errors:
        print("Validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1
    print("Validation passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
