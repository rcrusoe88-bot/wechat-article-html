#!/usr/bin/env python3
"""Convert Word, Markdown, or text into WeChat-compatible inline HTML."""

from __future__ import annotations

import argparse
import base64
import html
import io
import mimetypes
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable


BODY_FONT = "'Caveat', 'XuanZongTi', '玄宗体', 'FangSong', 'STFangsong', 'SimSun', serif"
LABEL_FONT = "'Caveat', 'Segoe Print', 'Bradley Hand', cursive"
FONT_DIR = Path(__file__).resolve().parents[1] / "assets" / "fonts"
DEFAULT_QR_PATH = Path(__file__).resolve().parents[1] / "assets" / "images" / "qr-placeholder.png"
LAYOUT_VERSION = "1.0"


@dataclass(frozen=True)
class Theme:
    key: str
    name: str
    primary: str
    secondary: str
    background: str
    surface: str
    text: str
    muted: str
    border: str
    variant: str
    description: str


THEMES = {
    "kami": Theme("kami", "Kami 纸感", "#1b365d", "#504e49", "#f5f4ed", "#faf9f5", "#141413", "#6b6a64", "#e8e6dc", "kami", "研究报告、深度长文与知识归档"),
    "esther": Theme("esther", "Esther 组件", "#2b7fd8", "#f4d758", "#fefcf6", "#ffffff", "#1a1a2e", "#4a4a5a", "#e8e2d8", "esther", "设计、产品与轻松解释"),
    "punk": Theme("punk", "Punk 微排", "#1554c0", "#ffd400", "#ffffff", "#eaf2ff", "#171717", "#5f6673", "#dce6f5", "punk", "工具教程、清单与实操步骤"),
}

@dataclass
class Block:
    kind: str
    text: str = ""
    level: int = 0
    items: list[str] = field(default_factory=list)
    rows: list[list[str]] = field(default_factory=list)
    ordered: bool = False
    data_uri: str = ""
    caption: str = ""
    language: str = ""


def canonical_theme(value: str) -> str:
    key = value.lower()
    if key not in THEMES:
        choices = ", ".join(sorted(THEMES))
        raise ValueError(f"unknown theme {value!r}; choose one of: {choices}")
    return key


def _subset_font_data_uri(font_path: Path, text: str) -> str:
    """Return a WOFF2 data URI containing only glyphs used by this article."""
    try:
        from fontTools import subset
        from fontTools.ttLib import TTFont
    except ImportError as exc:
        raise RuntimeError(
            "embedded fonts require fonttools and brotli; run: pip install -r requirements.txt"
        ) from exc
    if not font_path.is_file():
        raise RuntimeError(f"font asset is missing: {font_path}")
    options = subset.Options()
    options.flavor = "woff2"
    options.layout_features = ["*"]
    options.name_IDs = [0, 1, 2, 3, 4, 5, 6]
    options.name_legacy = True
    font = TTFont(font_path, recalcTimestamp=False)
    subsetter = subset.Subsetter(options=options)
    subsetter.populate(text="".join(dict.fromkeys(text)))
    subsetter.subset(font)
    buffer = io.BytesIO()
    font.save(buffer)
    return "data:font/woff2;base64," + base64.b64encode(buffer.getvalue()).decode("ascii")


def _document_text(blocks: list[Block], title: str, subtitle: str, author: str) -> str:
    fixed = "MORE TO READ NOTE CHAPTER 关注公众号 长按识别二维码 阅读更多内容 二维码"
    parts = [title, subtitle, author, fixed]
    for block in blocks:
        parts.extend([block.text, block.caption, *block.items])
        parts.extend(cell for row in block.rows for cell in row)
    return "\n".join(parts)


def _wechat_native_font_html(document: str) -> str:
    """Remove all custom font instructions for the WeChat editor and reader."""
    document = re.sub(
        rf"font:700\s+(\d+px)(?:/([\d.]+))?\s+{re.escape(LABEL_FONT)};",
        lambda match: (
            f"font-size:{match.group(1)};font-weight:700;"
            + (f"line-height:{match.group(2)};" if match.group(2) else "")
        ),
        document,
    )
    return re.sub(r"font-family:[^;]+;", "", document)


def image_to_data_uri(path_value: str, base_dir: Path) -> str:
    value = path_value.strip().strip("<>")
    if value.startswith("data:image/"):
        return value
    if re.match(r"^[a-z][a-z0-9+.-]*://", value, re.IGNORECASE):
        raise ValueError(f"external images are not allowed: {value}")
    image_path = Path(value)
    if not image_path.is_absolute():
        image_path = base_dir / image_path
    image_path = image_path.resolve()
    if not image_path.is_file():
        raise FileNotFoundError(f"image not found: {image_path}")
    mime = mimetypes.guess_type(image_path.name)[0] or "application/octet-stream"
    if not mime.startswith("image/"):
        raise ValueError(f"unsupported image type: {image_path}")
    encoded = base64.b64encode(image_path.read_bytes()).decode("ascii")
    return f"data:{mime};base64,{encoded}"


def default_qr_data_uri() -> str:
    if not DEFAULT_QR_PATH.is_file():
        raise RuntimeError(f"default QR placeholder is missing: {DEFAULT_QR_PATH}")
    return "data:image/png;base64," + base64.b64encode(DEFAULT_QR_PATH.read_bytes()).decode("ascii")


SPECIAL_LINE_RE = re.compile(
    r"^(#{1,3}\s+|>|[-*+]\s+|\d+[.)]\s+|```|~~~|(?:---+|___+|\*\*\*+)$|!\[)"
)


def _table_separator(line: str) -> bool:
    cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
    return bool(cells) and all(re.fullmatch(r":?-{3,}:?", cell) for cell in cells)


def _split_table_row(line: str) -> list[str]:
    return [cell.strip() for cell in line.strip().strip("|").split("|")]


def parse_markdown(content: str, base_dir: Path) -> list[Block]:
    lines = content.replace("\r\n", "\n").replace("\r", "\n").split("\n")
    blocks: list[Block] = []
    index = 0
    while index < len(lines):
        raw = lines[index]
        stripped = raw.strip()
        if not stripped:
            index += 1
            continue

        fence = re.match(r"^(```|~~~)(.*)$", stripped)
        if fence:
            marker = fence.group(1)
            language = fence.group(2).strip()
            code_lines: list[str] = []
            index += 1
            while index < len(lines) and not lines[index].strip().startswith(marker):
                code_lines.append(lines[index])
                index += 1
            if index < len(lines):
                index += 1
            blocks.append(Block("code", text="\n".join(code_lines), language=language))
            continue

        heading = re.match(r"^(#{1,3})\s+(.+)$", stripped)
        if heading:
            blocks.append(Block("heading", text=heading.group(2).strip(), level=len(heading.group(1))))
            index += 1
            continue

        image_match = re.fullmatch(r"!\[([^]]*)\]\(([^)]+)\)", stripped)
        if image_match:
            blocks.append(
                Block(
                    "image",
                    data_uri=image_to_data_uri(image_match.group(2), base_dir),
                    caption=image_match.group(1).strip(),
                )
            )
            index += 1
            continue

        if stripped in {"---", "___", "***"}:
            blocks.append(Block("divider"))
            index += 1
            continue

        if stripped.startswith(">"):
            quote_lines: list[str] = []
            while index < len(lines) and lines[index].strip().startswith(">"):
                quote_lines.append(lines[index].strip()[1:].strip())
                index += 1
            blocks.append(Block("quote", text=" ".join(quote_lines)))
            continue

        list_match = re.match(r"^([-*+]|\d+[.)])\s+(.+)$", stripped)
        if list_match:
            ordered = list_match.group(1)[0].isdigit()
            items: list[str] = []
            while index < len(lines):
                current = re.match(r"^([-*+]|\d+[.)])\s+(.+)$", lines[index].strip())
                if not current or current.group(1)[0].isdigit() != ordered:
                    break
                items.append(current.group(2).strip())
                index += 1
            blocks.append(Block("list", items=items, ordered=ordered))
            continue

        if index + 1 < len(lines) and "|" in stripped and _table_separator(lines[index + 1].strip()):
            rows = [_split_table_row(stripped)]
            index += 2
            while index < len(lines) and "|" in lines[index] and lines[index].strip():
                rows.append(_split_table_row(lines[index]))
                index += 1
            blocks.append(Block("table", rows=rows))
            continue

        paragraph_lines = [stripped]
        index += 1
        while index < len(lines):
            candidate = lines[index].strip()
            if not candidate or SPECIAL_LINE_RE.match(candidate):
                break
            if index + 1 < len(lines) and "|" in candidate and _table_separator(lines[index + 1].strip()):
                break
            paragraph_lines.append(candidate)
            index += 1
        blocks.append(Block("paragraph", text=" ".join(paragraph_lines)))
    return blocks


def _smart_heading(text: str) -> int:
    numbered = r"第[一二三四五六七八九十百0-9]+(?:[章节部篇]|道损耗)"
    editorial = r"(?:数据卡片|换气点|三大工程策略|临床爆发背后|批判性讨论|结语|参考资料)"
    if re.match(rf"^(?:{numbered}|{editorial})(?:[:：]|$)|^§\s*\d+", text) and len(text) <= 90:
        return 2
    return 0


def _normalize_docx_blocks(blocks: list[Block]) -> list[Block]:
    """Promote strong unstyled-document signals without inventing structure."""
    if (
        len(blocks) >= 2
        and blocks[0].kind == "paragraph"
        and blocks[1].kind == "paragraph"
        and blocks[1].text.startswith("副标题：")
        and len(blocks[0].text) <= 100
    ):
        blocks[0] = Block("heading", text=blocks[0].text, level=1)

    normalized: list[Block] = []
    index = 0
    while index < len(blocks):
        block = blocks[index]
        if block.kind == "image":
            caption_parts: list[str] = []
            cursor = index + 1
            if cursor < len(blocks) and blocks[cursor].kind == "paragraph" and re.match(r"^图\s*\d+[:：]", blocks[cursor].text):
                caption_parts.append(blocks[cursor].text)
                cursor += 1
            if cursor < len(blocks) and blocks[cursor].kind == "paragraph" and blocks[cursor].text.startswith("来源："):
                caption_parts.append(blocks[cursor].text)
                cursor += 1
            if caption_parts:
                block.caption = " ".join(caption_parts)
                normalized.append(block)
                index = cursor
                continue
        if block.kind == "paragraph" and block.text.startswith("一句话："):
            normalized.append(Block("quote", text=block.text.removeprefix("一句话：").strip()))
        else:
            normalized.append(block)
        index += 1
    return normalized


def parse_docx(path: Path) -> tuple[list[Block], str]:
    try:
        from docx import Document
        from docx.document import Document as DocumentType
        from docx.oxml.table import CT_Tbl
        from docx.oxml.text.paragraph import CT_P
        from docx.table import Table
        from docx.text.paragraph import Paragraph
    except ImportError as exc:
        raise RuntimeError(".docx input requires python-docx; install requirements.txt") from exc

    document = Document(path)
    blocks: list[Block] = []
    pending_list: list[str] = []
    pending_ordered = False

    def flush_list() -> None:
        nonlocal pending_list
        if pending_list:
            blocks.append(Block("list", items=pending_list, ordered=pending_ordered))
            pending_list = []

    def iter_items(parent: DocumentType) -> Iterable[Paragraph | Table]:
        for child in parent.element.body.iterchildren():
            if isinstance(child, CT_P):
                yield Paragraph(child, parent)
            elif isinstance(child, CT_Tbl):
                yield Table(child, parent)

    for item in iter_items(document):
        if isinstance(item, Table):
            flush_list()
            rows = [[cell.text.strip() for cell in row.cells] for row in item.rows]
            if rows:
                blocks.append(Block("table", rows=rows))
            continue

        paragraph = item
        text_value = paragraph.text.strip()
        image_blocks: list[Block] = []
        for run in paragraph.runs:
            for blip in run._element.xpath(".//a:blip"):
                rel_id = blip.get("{http://schemas.openxmlformats.org/officeDocument/2006/relationships}embed")
                if not rel_id or rel_id not in document.part.rels:
                    continue
                part = document.part.rels[rel_id].target_part
                mime = getattr(part, "content_type", "image/png")
                encoded = base64.b64encode(part.blob).decode("ascii")
                image_blocks.append(Block("image", data_uri=f"data:{mime};base64,{encoded}"))

        style_name = (paragraph.style.name if paragraph.style else "").lower()
        heading_level = 0
        heading_match = re.search(r"heading\s*([1-3])|标题\s*([1-3])", style_name)
        if heading_match:
            heading_level = int(heading_match.group(1) or heading_match.group(2))
        elif text_value:
            heading_level = _smart_heading(text_value)

        num_pr = getattr(getattr(paragraph._p, "pPr", None), "numPr", None)
        is_list = num_pr is not None or "list" in style_name or "列表" in style_name
        if is_list and text_value:
            ordered = bool(
                re.match(r"^\d+[.)、]", text_value)
                or "number" in style_name
                or "编号" in style_name
            )
            cleaned = re.sub(r"^(?:[-*+•]\s*|\d+[.)、]\s*)", "", text_value)
            if pending_list and ordered != pending_ordered:
                flush_list()
            pending_ordered = ordered
            pending_list.append(cleaned)
        else:
            flush_list()
            if text_value:
                if heading_level:
                    blocks.append(Block("heading", text=text_value, level=heading_level))
                else:
                    blocks.append(Block("paragraph", text=text_value))
        if image_blocks:
            flush_list()
            blocks.extend(image_blocks)

    flush_list()
    title = document.core_properties.title.strip() if document.core_properties.title else ""
    return _normalize_docx_blocks(blocks), title


def read_input(path: Path) -> tuple[list[Block], str]:
    suffix = path.suffix.lower()
    if suffix == ".docx":
        return parse_docx(path)
    if suffix not in {".md", ".markdown", ".txt"}:
        raise ValueError(f"unsupported input format: {suffix or '<none>'}")
    content = path.read_text(encoding="utf-8-sig")
    return parse_markdown(content, path.parent), ""


def inline_markup(value: str, theme: Theme) -> str:
    escaped = html.escape(value, quote=True)
    code_tokens: list[str] = []

    def stash_code(match: re.Match[str]) -> str:
        token = f"\x00CODE{len(code_tokens)}\x00"
        code_tokens.append(
            f'<code style="padding:2px 5px;background:{theme.surface};border:1px solid {theme.border};color:{theme.primary};font-size:14px;">{match.group(1)}</code>'
        )
        return token

    escaped = re.sub(r"`([^`]+)`", stash_code, escaped)
    escaped = re.sub(
        r"\[([^]]+)]\((https?://[^)]+)\)",
        lambda m: f'<a href="{html.escape(html.unescape(m.group(2)), quote=True)}" style="color:{theme.primary};text-decoration:underline;text-underline-offset:3px;">{m.group(1)}</a>',
        escaped,
    )
    escaped = re.sub(r"\*\*(.+?)\*\*", rf'<strong style="color:{theme.primary};font-weight:700;">\1</strong>', escaped)
    escaped = re.sub(r"(?<!\*)\*([^*]+)\*(?!\*)", r'<em style="font-style:italic;">\1</em>', escaped)
    for index, code_html in enumerate(code_tokens):
        escaped = escaped.replace(f"\x00CODE{index}\x00", code_html)
    return escaped


def _header(theme: Theme, title: str, subtitle: str, author: str) -> str:
    safe_title = html.escape(title)
    safe_subtitle = html.escape(subtitle)
    safe_author = html.escape(author)
    meta = ""
    if safe_subtitle:
        meta += f'<p style="margin:12px 0 0;font-size:15px;line-height:1.7;color:{theme.muted};">{safe_subtitle}</p>'
    if safe_author:
        meta += f'<p style="margin:14px 0 0;font-size:13px;line-height:1.5;color:{theme.muted};">文 / {safe_author}</p>'

    if theme.variant == "kami":
        return f'<header style="padding:46px 28px 34px;background:{theme.surface};border-top:2px solid {theme.primary};border-bottom:1px solid {theme.border};"><p style="margin:0 0 28px;font:700 12px {LABEL_FONT};color:{theme.primary};">KAMI / NOTE</p><h1 style="margin:0;font-size:30px;line-height:1.42;font-weight:700;color:{theme.text};overflow-wrap:anywhere;">{safe_title}</h1>{meta}<div style="width:58px;height:2px;margin-top:26px;background:{theme.primary};"></div></header>'
    if theme.variant == "esther":
        return f'<header style="padding:38px 24px 34px;background:{theme.surface};border-bottom:1px solid {theme.border};"><div style="display:flex;gap:7px;margin-bottom:24px;"><span style="display:block;width:30px;height:7px;border-radius:999px;background:{theme.primary};"></span><span style="display:block;width:13px;height:7px;border-radius:999px;background:{theme.secondary};"></span><span style="display:block;width:13px;height:7px;border-radius:999px;background:#e84a5f;"></span></div><p style="margin:0 0 12px;font:700 13px {LABEL_FONT};color:{theme.primary};">ESTHER / COMPONENTS</p><h1 style="margin:0;font-size:30px;line-height:1.38;font-weight:800;color:{theme.text};overflow-wrap:anywhere;">{safe_title}</h1>{meta}<div style="display:inline-block;margin-top:26px;padding:8px 12px;border-radius:999px;background:#faf6eb;font:700 12px {LABEL_FONT};color:{theme.primary};">IDEA NOTE / 01</div></header>'
    if theme.variant == "punk":
        return f'<header style="padding:0 22px 30px;background:#ffffff;border-top:9px solid {theme.primary};"><div style="display:flex;align-items:center;gap:9px;padding:22px 0 18px;"><span style="display:inline-block;padding:4px 9px;border-radius:999px;background:{theme.secondary};font:700 12px {LABEL_FONT};color:{theme.primary};">PUNK 微排</span><span style="font:700 11px {LABEL_FONT};color:{theme.muted};">PRACTICAL LAYOUT</span></div><h1 style="margin:0;font-size:29px;line-height:1.42;font-weight:800;color:{theme.primary};overflow-wrap:anywhere;">{safe_title}</h1>{meta}<div style="display:flex;align-items:center;gap:4px;margin-top:26px;"><span style="display:block;width:72px;height:5px;background:{theme.secondary};"></span><span style="display:block;width:14px;height:5px;background:{theme.primary};"></span><span style="display:block;flex:1;height:1px;background:{theme.border};"></span></div></header>'
    raise ValueError(f"unsupported theme variant: {theme.variant}")


def _heading(theme: Theme, text: str, level: int, chapter: int) -> str:
    content = inline_markup(text, theme)
    if level == 3:
        if theme.variant == "kami":
            return f'<h3 style="margin:32px 0 14px;padding-bottom:8px;border-bottom:1px solid {theme.border};font-size:17px;line-height:1.65;font-weight:700;color:{theme.secondary};overflow-wrap:anywhere;">{content}</h3>'
        if theme.variant == "esther":
            return f'<h3 style="margin:30px 0 14px;padding:10px 13px;border-left:4px solid #e84a5f;border-radius:0 9px 9px 0;background:{theme.surface};font-size:17px;line-height:1.65;font-weight:700;color:{theme.text};overflow-wrap:anywhere;">{content}</h3>'
        if theme.variant == "punk":
            return f'<h3 style="margin:30px 0 12px;padding:7px 12px;border-left:7px solid {theme.secondary};background:#f7faff;font-size:18px;line-height:1.6;font-weight:700;color:{theme.primary};overflow-wrap:anywhere;">{content}</h3>'
        raise ValueError(f"unsupported theme variant: {theme.variant}")
    number = f"{chapter:02d}"
    if theme.variant == "kami":
        return f'<section style="margin:48px 0 22px;"><p style="margin:0 0 9px;font:700 13px {LABEL_FONT};color:{theme.primary};">CHAPTER {number}</p><h2 style="margin:0;padding-bottom:14px;border-bottom:1px solid {theme.border};font-size:23px;line-height:1.5;font-weight:700;color:{theme.text};overflow-wrap:anywhere;">{content}</h2></section>'
    if theme.variant == "esther":
        return f'<section style="margin:46px 0 20px;padding:22px 20px;background:{theme.surface};border:1px solid {theme.border};border-radius:14px;"><div style="display:flex;align-items:flex-start;gap:14px;"><span style="display:block;min-width:48px;font:700 30px {LABEL_FONT};line-height:1;color:#dcebfa;">{number}</span><div style="min-width:0;padding-top:1px;"><p style="margin:0 0 5px;font:700 11px {LABEL_FONT};color:#e84a5f;">COMPONENT</p><h2 style="margin:0;font-size:23px;line-height:1.42;font-weight:800;color:{theme.text};overflow-wrap:anywhere;">{content}</h2></div></div><div style="width:64px;height:5px;margin-top:16px;border-radius:999px;background:{theme.secondary};"></div></section>'
    if theme.variant == "punk":
        return f'<section style="margin:46px 0 20px;text-align:center;"><p style="margin:0 0 7px;font:700 12px {LABEL_FONT};color:{theme.primary};">PART {number}</p><h2 style="display:inline-block;margin:0;padding-bottom:8px;border-bottom:5px solid {theme.secondary};font-size:23px;line-height:1.45;font-weight:800;color:{theme.primary};overflow-wrap:anywhere;">{content}</h2><div style="display:flex;justify-content:center;gap:4px;margin-top:12px;"><span style="display:block;width:70px;height:3px;background:{theme.primary};"></span><span style="display:block;width:12px;height:3px;background:{theme.secondary};"></span></div></section>'
    raise ValueError(f"unsupported theme variant: {theme.variant}")


def _paragraph(theme: Theme, text: str) -> str:
    content = inline_markup(text, theme)
    if theme.variant == "kami":
        return f'<p style="margin:0 0 23px;font-size:16px;line-height:2;text-align:justify;color:{theme.text};overflow-wrap:anywhere;">{content}</p>'
    if theme.variant == "esther":
        return f'<p style="margin:0 0 20px;font-size:16px;line-height:1.95;text-align:justify;color:{theme.text};overflow-wrap:anywhere;">{content}</p>'
    if theme.variant == "punk":
        return f'<p style="margin:0 0 18px;font-size:16px;line-height:1.9;text-align:justify;color:#222222;overflow-wrap:anywhere;">{content}</p>'
    raise ValueError(f"unsupported theme variant: {theme.variant}")


def _quote(theme: Theme, text: str) -> str:
    content = inline_markup(text, theme)
    if theme.variant == "kami":
        return f'<blockquote style="margin:32px 0;padding:22px 22px 20px;background:{theme.surface};border-top:2px solid {theme.primary};border-bottom:1px solid {theme.border};"><p style="margin:0 0 9px;font:700 11px {LABEL_FONT};color:{theme.primary};">TAKEAWAY</p><p style="margin:0;font-size:17px;line-height:1.9;color:{theme.text};">{content}</p></blockquote>'
    if theme.variant == "esther":
        return f'<blockquote style="margin:30px 0;padding:28px 24px 24px;background:{theme.surface};border:2px solid {theme.secondary};border-radius:14px;"><p style="margin:0 0 8px;font:700 12px {LABEL_FONT};color:#e84a5f;">PULL QUOTE</p><p style="margin:0;font-size:17px;line-height:1.9;font-weight:700;color:{theme.text};">{content}</p></blockquote>'
    if theme.variant == "punk":
        return f'<blockquote style="margin:28px 0;padding:20px 20px 20px 22px;background:{theme.surface};border-left:7px solid {theme.primary};border-radius:0 9px 9px 0;"><p style="margin:0 0 7px;font:700 11px {LABEL_FONT};color:{theme.primary};">NOTE</p><p style="margin:0;font-size:17px;line-height:1.9;color:{theme.text};">{content}</p></blockquote>'
    raise ValueError(f"unsupported theme variant: {theme.variant}")


def _list(theme: Theme, block: Block) -> str:
    if theme.variant == "kami":
        items = []
        for index, item in enumerate(block.items, 1):
            if block.ordered:
                marker = f'<span style="display:block;min-width:28px;padding-top:2px;font:700 12px {LABEL_FONT};color:{theme.primary};">{index:02d}</span>'
            else:
                marker = f'<span style="display:block;width:7px;height:7px;margin-top:10px;background:{theme.primary};"></span>'
            items.append(f'<li style="display:flex;align-items:flex-start;gap:13px;margin:0;padding:8px 0;font-size:16px;line-height:1.88;color:{theme.text};">{marker}<span style="min-width:0;">{inline_markup(item, theme)}</span></li>')
        tag = "ol" if block.ordered else "ul"
        return f'<{tag} style="margin:24px 0;padding:0;list-style-type:none;">{"".join(items)}</{tag}>'
    if theme.variant == "esther":
        accents = [theme.primary, theme.secondary, "#e84a5f"]
        items = []
        for index, item in enumerate(block.items, 1):
            accent = accents[(index - 1) % len(accents)]
            if block.ordered:
                marker_text = theme.text if accent == theme.secondary else "#ffffff"
                marker = f'<span style="display:block;min-width:28px;height:28px;line-height:28px;border-radius:50%;background:{accent};text-align:center;font:700 13px {LABEL_FONT};color:{marker_text};">{index}</span>'
            else:
                marker = f'<span style="display:block;width:10px;height:10px;margin-top:8px;border-radius:50%;background:{accent};"></span>'
            items.append(f'<li style="display:flex;align-items:flex-start;gap:12px;margin:0 0 11px;padding:15px 16px;background:{theme.surface};border:1px solid {theme.border};border-radius:12px;font-size:16px;line-height:1.82;color:{theme.text};">{marker}<span style="min-width:0;">{inline_markup(item, theme)}</span></li>')
        tag = "ol" if block.ordered else "ul"
        return f'<{tag} style="margin:25px 0;padding:0;list-style-type:none;">{"".join(items)}</{tag}>'
    if theme.variant == "punk":
        items = []
        for index, item in enumerate(block.items, 1):
            if block.ordered:
                marker = f'<span style="display:block;min-width:28px;height:26px;line-height:26px;border-radius:5px;background:{theme.primary};text-align:center;font:700 13px {LABEL_FONT};color:#ffffff;">{index}</span>'
            else:
                marker = f'<span style="display:block;width:9px;height:9px;margin-top:8px;background:{theme.primary};"></span>'
            items.append(f'<li style="display:flex;align-items:flex-start;gap:11px;margin:0;padding:7px 0;font-size:16px;line-height:1.82;color:{theme.text};">{marker}<span style="min-width:0;">{inline_markup(item, theme)}</span></li>')
        tag = "ol" if block.ordered else "ul"
        return f'<{tag} style="margin:22px 0;padding:0;list-style-type:none;">{"".join(items)}</{tag}>'
    raise ValueError(f"unsupported theme variant: {theme.variant}")


def _table(theme: Theme, rows: list[list[str]]) -> str:
    if not rows:
        return ""
    width = max(len(row) for row in rows)
    normalized = [row + [""] * (width - len(row)) for row in rows]
    if theme.variant == "kami":
        header_cells = "".join(f'<th style="padding:12px 11px;border-top:2px solid {theme.primary};border-bottom:1px solid {theme.border};background:{theme.surface};font-size:14px;line-height:1.5;text-align:left;color:{theme.text};vertical-align:bottom;">{inline_markup(cell, theme)}</th>' for cell in normalized[0])
        body_rows = []
        for row in normalized[1:]:
            cells = "".join(f'<td style="padding:12px 11px;border-bottom:1px solid {theme.border};background:{theme.surface};font-size:14px;line-height:1.7;color:{theme.text};vertical-align:top;">{inline_markup(cell, theme)}</td>' for cell in row)
            body_rows.append(f"<tr>{cells}</tr>")
        return f'<div style="margin:30px 0;max-width:100%;overflow-x:auto;"><table style="width:100%;min-width:480px;border-collapse:collapse;table-layout:auto;"><tr>{header_cells}</tr>{"".join(body_rows)}</table></div>'
    if theme.variant == "esther":
        header_cells = "".join(f'<th style="padding:12px 13px;border-right:1px solid #5a9ce4;background:{theme.primary};font-size:14px;line-height:1.5;text-align:left;color:#ffffff;">{inline_markup(cell, theme)}</th>' for cell in normalized[0])
        body_rows = []
        for row in normalized[1:]:
            cells = "".join(f'<td style="padding:12px 13px;border-right:1px solid {theme.border};border-bottom:1px solid {theme.border};background:{theme.surface};font-size:14px;line-height:1.7;color:{theme.text};vertical-align:top;">{inline_markup(cell, theme)}</td>' for cell in row)
            body_rows.append(f"<tr>{cells}</tr>")
        return f'<div style="margin:28px 0;max-width:100%;overflow-x:auto;border:1px solid {theme.border};border-radius:14px;background:{theme.surface};"><table style="width:100%;min-width:480px;border-collapse:collapse;table-layout:auto;"><tr>{header_cells}</tr>{"".join(body_rows)}</table></div>'
    if theme.variant == "punk":
        header_cells = "".join(f'<th style="padding:11px 12px;border-top:3px solid {theme.primary};border-right:1px solid {theme.border};border-bottom:2px solid {theme.secondary};background:#f7faff;font-size:14px;line-height:1.5;text-align:left;color:{theme.primary};">{inline_markup(cell, theme)}</th>' for cell in normalized[0])
        body_rows = []
        for row in normalized[1:]:
            cells = "".join(f'<td style="padding:11px 12px;border-right:1px solid {theme.border};border-bottom:1px solid {theme.border};background:#ffffff;font-size:14px;line-height:1.7;color:{theme.text};vertical-align:top;">{inline_markup(cell, theme)}</td>' for cell in row)
            body_rows.append(f"<tr>{cells}</tr>")
        return f'<div style="margin:28px 0;max-width:100%;overflow-x:auto;border:1px solid {theme.border};"><table style="width:100%;min-width:480px;border-collapse:collapse;table-layout:auto;"><tr>{header_cells}</tr>{"".join(body_rows)}</table></div>'
    raise ValueError(f"unsupported theme variant: {theme.variant}")


def _code(theme: Theme, block: Block) -> str:
    code = html.escape(block.text)
    language = html.escape(block.language or "code")
    if theme.variant == "kami":
        return f'<pre style="margin:30px 0;padding:20px;overflow-x:auto;border-top:1px solid {theme.primary};border-bottom:1px solid {theme.border};background:{theme.surface};font-size:14px;line-height:1.85;color:{theme.text};white-space:pre-wrap;word-break:break-word;"><code style="font-family:Consolas,monospace;">{code}</code></pre>'
    if theme.variant == "esther":
        return f'<section style="margin:30px 0;border:1px solid {theme.border};border-radius:14px;overflow:hidden;background:#1a1a2e;"><div style="padding:10px 14px;background:#2d2d3a;"><span style="display:inline-block;width:10px;height:10px;margin-right:6px;border-radius:50%;background:#ff5f56;"></span><span style="display:inline-block;width:10px;height:10px;margin-right:6px;border-radius:50%;background:#ffbd2e;"></span><span style="display:inline-block;width:10px;height:10px;border-radius:50%;background:#27c93f;"></span><span style="float:right;font:700 11px {LABEL_FONT};color:#d7d7e2;">{language}</span></div><pre style="margin:0;padding:20px;overflow-x:auto;background:#1a1a2e;font-size:14px;line-height:1.85;color:#f4f0ff;white-space:pre-wrap;word-break:break-word;"><code style="font-family:Consolas,monospace;">{code}</code></pre></section>'
    if theme.variant == "punk":
        return f'<section style="margin:30px 0;border:1px solid #0a3b91;border-radius:12px;overflow:hidden;background:#0b3a91;"><div style="padding:10px 14px;background:#082c72;"><span style="display:inline-block;width:10px;height:10px;margin-right:6px;border-radius:50%;background:#ff5f56;"></span><span style="display:inline-block;width:10px;height:10px;margin-right:6px;border-radius:50%;background:#ffbd2e;"></span><span style="display:inline-block;width:10px;height:10px;border-radius:50%;background:#27c93f;"></span><span style="float:right;font:700 11px {LABEL_FONT};color:{theme.secondary};">{language}</span></div><pre style="margin:0;padding:20px;overflow-x:auto;background:{theme.primary};font-size:14px;line-height:1.85;color:#fff3b0;white-space:pre-wrap;word-break:break-word;"><code style="font-family:Consolas,monospace;">{code}</code></pre></section>'
    raise ValueError(f"unsupported theme variant: {theme.variant}")


def _image(theme: Theme, block: Block) -> str:
    caption = ""
    if block.caption:
        caption = f'<p style="margin:9px 0 0;font-size:13px;line-height:1.6;text-align:center;color:{theme.muted};">{html.escape(block.caption)}</p>'
    if theme.variant == "kami":
        return f'<figure style="margin:30px 0;"><img src="{block.data_uri}" alt="{html.escape(block.caption, quote=True)}" style="display:block;width:100%;max-width:100%;height:auto;padding:8px;background:{theme.surface};border-top:1px solid {theme.border};border-bottom:1px solid {theme.border};box-sizing:border-box;" />{caption}</figure>'
    if theme.variant == "esther":
        return f'<figure style="margin:30px 0;"><img src="{block.data_uri}" alt="{html.escape(block.caption, quote=True)}" style="display:block;width:100%;max-width:100%;height:auto;border:1px solid {theme.border};border-radius:14px;" />{caption}</figure>'
    if theme.variant == "punk":
        return f'<figure style="margin:28px 0;"><img src="{block.data_uri}" alt="{html.escape(block.caption, quote=True)}" style="display:block;width:100%;max-width:100%;height:auto;border:2px solid {theme.primary};border-bottom:6px solid {theme.secondary};box-sizing:border-box;" />{caption}</figure>'
    raise ValueError(f"unsupported theme variant: {theme.variant}")


def _footer(theme: Theme, qr_data_uri: str) -> str:
    qr = f'<img data-qr-code="true" src="{qr_data_uri}" alt="公众号二维码" style="display:block;width:144px;height:144px;margin:18px auto 0;object-fit:contain;" />'
    if theme.variant == "kami":
        history = []
        for index in range(1, 4):
            history.append(f'<div data-history-item="{index}" style="margin:0;padding:16px 0;border-top:1px solid {theme.border};"><p style="margin:0 0 5px;font:700 11px {LABEL_FONT};color:{theme.primary};">READ / {index:02d}</p><p style="margin:0;font-size:15px;line-height:1.65;color:{theme.text};"><!-- HISTORY_TITLE_{index} -->往期文章标题 {index}</p><p style="margin:4px 0 0;font-size:12px;line-height:1.5;color:{theme.muted};"><!-- HISTORY_LINK_{index} -->阅读全文</p></div>')
        return f'<footer data-fixed-footer="true" style="padding:40px 28px 44px;background:{theme.surface};border-top:2px solid {theme.primary};"><section style="margin:0 0 30px;"><p style="margin:0 0 8px;font:700 12px {LABEL_FONT};color:{theme.primary};">MORE TO READ</p>{"".join(history)}</section><section style="padding:24px 0 0;text-align:center;border-top:1px solid {theme.border};"><p style="margin:0;font-size:17px;font-weight:700;color:{theme.text};">关注公众号</p><p style="margin:7px 0 0;font-size:13px;line-height:1.6;color:{theme.muted};">长按识别二维码，阅读更多内容</p>{qr}</section></footer>'
    if theme.variant == "esther":
        history = []
        for index in range(1, 4):
            history.append(f'<div data-history-item="{index}" style="margin:0 0 11px;padding:15px 16px;background:{theme.surface};border:1px solid {theme.border};border-radius:12px;"><p style="margin:0;font-size:15px;line-height:1.65;color:{theme.text};"><!-- HISTORY_TITLE_{index} -->往期文章标题 {index}</p><p style="margin:4px 0 0;font-size:12px;line-height:1.5;color:#e84a5f;"><!-- HISTORY_LINK_{index} -->阅读全文</p></div>')
        return f'<footer data-fixed-footer="true" style="padding:38px 24px 42px;background:#faf6eb;border-top:1px solid {theme.border};"><section style="margin:0 0 30px;"><p style="margin:0 0 16px;font:700 13px {LABEL_FONT};color:{theme.primary};">MORE NOTES</p>{"".join(history)}</section><section style="padding:24px 18px;text-align:center;background:{theme.surface};border:2px solid {theme.secondary};border-radius:14px;"><p style="margin:0;font-size:17px;font-weight:700;color:{theme.text};">关注公众号</p><p style="margin:7px 0 0;font-size:13px;line-height:1.6;color:{theme.muted};">长按识别二维码，阅读更多内容</p>{qr}</section></footer>'
    if theme.variant == "punk":
        history = []
        for index in range(1, 4):
            history.append(f'<div data-history-item="{index}" style="margin:0 0 10px;padding:14px 15px;background:#f7faff;border-left:5px solid {theme.primary};"><p style="margin:0 0 5px;font:700 11px {LABEL_FONT};color:{theme.primary};">READ / {index:02d}</p><p style="margin:0;font-size:15px;line-height:1.65;color:{theme.text};"><!-- HISTORY_TITLE_{index} -->往期文章标题 {index}</p><p style="margin:4px 0 0;font-size:12px;line-height:1.5;color:{theme.primary};"><!-- HISTORY_LINK_{index} -->阅读全文</p></div>')
        return f'<footer data-fixed-footer="true" style="padding:36px 22px 42px;background:#ffffff;border-top:9px solid {theme.primary};"><section style="margin:0 0 30px;"><p style="margin:0 0 16px;font:700 13px {LABEL_FONT};color:{theme.primary};">MORE PRACTICE</p>{"".join(history)}</section><section style="padding:24px 18px;text-align:center;background:{theme.surface};border-top:5px solid {theme.secondary};"><p style="margin:0;font-size:17px;font-weight:700;color:{theme.primary};">关注公众号</p><p style="margin:7px 0 0;font-size:13px;line-height:1.6;color:{theme.muted};">长按识别二维码，阅读更多内容</p>{qr}</section></footer>'
    raise ValueError(f"unsupported theme variant: {theme.variant}")


def render_html(
    blocks: list[Block],
    title: str,
    theme_key: str,
    subtitle: str = "",
    author: str = "",
    qr_data_uri: str | None = None,
    preview_fonts: bool = False,
    font_base: str = "assets/fonts",
    embedded_fonts: bool = False,
    wechat_mode: bool = True,
) -> str:
    theme = THEMES[canonical_theme(theme_key)]
    body_blocks = list(blocks)
    if body_blocks and body_blocks[0].kind == "heading" and body_blocks[0].level == 1:
        if not title:
            title = body_blocks[0].text
        body_blocks.pop(0)
    if not title:
        title = "未命名文章"
    if not qr_data_uri:
        qr_data_uri = default_qr_data_uri()

    rendered: list[str] = []
    chapter = 0
    for block in body_blocks:
        if block.kind == "heading":
            level = 2 if block.level == 1 else block.level
            if level == 2:
                chapter += 1
            rendered.append(_heading(theme, block.text, level, max(chapter, 1)))
        elif block.kind == "paragraph":
            rendered.append(_paragraph(theme, block.text))
        elif block.kind == "quote":
            rendered.append(_quote(theme, block.text))
        elif block.kind == "list":
            rendered.append(_list(theme, block))
        elif block.kind == "table":
            rendered.append(_table(theme, block.rows))
        elif block.kind == "image":
            rendered.append(_image(theme, block))
        elif block.kind == "code":
            rendered.append(_code(theme, block))
        elif block.kind == "divider":
            if theme.variant == "kami":
                rendered.append(f'<div style="margin:36px 0;text-align:center;"><span style="display:inline-block;width:34px;height:1px;background:{theme.border};"></span><span style="display:inline-block;width:5px;height:5px;margin:0 9px;border:1px solid {theme.primary};transform:rotate(45deg);"></span><span style="display:inline-block;width:34px;height:1px;background:{theme.border};"></span></div>')
            elif theme.variant == "esther":
                rendered.append(f'<div style="margin:36px 0;text-align:center;"><span style="display:inline-block;width:8px;height:8px;margin:0 4px;border-radius:50%;background:{theme.primary};"></span><span style="display:inline-block;width:8px;height:8px;margin:0 4px;border-radius:50%;background:{theme.secondary};"></span><span style="display:inline-block;width:8px;height:8px;margin:0 4px;border-radius:50%;background:#e84a5f;"></span></div>')
            elif theme.variant == "punk":
                rendered.append(f'<div style="display:flex;align-items:center;gap:5px;margin:34px 0;"><span style="display:block;width:40px;height:5px;background:{theme.secondary};"></span><span style="display:block;flex:1;height:1px;background:{theme.primary};"></span><span style="display:block;width:12px;height:5px;background:{theme.primary};"></span></div>')
            else:
                raise ValueError(f"unsupported theme variant: {theme.variant}")

    font_css = ""
    font_attr = ""
    if embedded_fonts:
        glyph_text = _document_text(body_blocks, title, subtitle, author)
        caveat_uri = _subset_font_data_uri(FONT_DIR / "Caveat-Bold.ttf", glyph_text)
        xuanzong_uri = _subset_font_data_uri(FONT_DIR / "XuanZongTi.otf", glyph_text)
        font_attr = ' data-embedded-fonts="true"'
        font_css = f'''<style>
@font-face{{font-family:"Caveat";src:url("{caveat_uri}") format("woff2");font-style:normal;font-weight:400 700;font-display:swap;}}
@font-face{{font-family:"XuanZongTi";src:url("{xuanzong_uri}") format("woff2");font-style:normal;font-weight:400;font-display:swap;}}
</style>'''
    elif preview_fonts:
        safe_base = font_base.rstrip("/\\").replace("\\", "/")
        font_attr = ' data-preview-fonts="true"'
        font_css = f'''<style>
@font-face{{font-family:"Caveat";src:url("{safe_base}/Caveat-Bold.ttf") format("truetype");font-style:normal;font-weight:400 700;}}
@font-face{{font-family:"XuanZongTi";src:url("{safe_base}/XuanZongTi.otf") format("opentype");font-style:normal;font-weight:400;}}
</style>'''

    document = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<title>{html.escape(title)}</title>
{font_css}
</head>
<body data-theme="{theme.key}" data-layout-version="{LAYOUT_VERSION}"{font_attr} style="max-width:677px;margin:0 auto;padding:0;background:{theme.background};font-family:{BODY_FONT};color:{theme.text};line-height:1.85;">
{_header(theme, title, subtitle, author)}
<main style="padding:10px 26px 34px;">
{''.join(rendered)}
</main>
{_footer(theme, qr_data_uri)}
</body>
</html>
'''
    return _wechat_native_font_html(document) if wechat_mode else document


def convert(
    input_path: Path,
    output_path: Path,
    theme_key: str,
    title: str = "",
    subtitle: str = "",
    author: str = "",
    qr_path: Path | None = None,
    validate: bool = True,
) -> Path:
    blocks, document_title = read_input(input_path)
    blocks = list(blocks)
    subtitle_index = 1 if blocks and blocks[0].kind == "heading" and blocks[0].level == 1 else 0
    if (
        not subtitle
        and subtitle_index < len(blocks)
        and blocks[subtitle_index].kind == "paragraph"
        and blocks[subtitle_index].text.startswith("副标题：")
    ):
        subtitle = blocks[subtitle_index].text.removeprefix("副标题：").strip()
        del blocks[subtitle_index]
    inferred_title = ""
    if blocks and blocks[0].kind == "heading" and blocks[0].level == 1:
        inferred_title = blocks[0].text
    final_title = title or inferred_title or document_title or input_path.stem
    qr_data = image_to_data_uri(str(qr_path), qr_path.parent) if qr_path else default_qr_data_uri()
    canonical = canonical_theme(theme_key)
    output = render_html(
        blocks,
        final_title,
        canonical,
        subtitle,
        author,
        qr_data,
        wechat_mode=True,
    )
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(output, encoding="utf-8")
    if validate:
        from validate_html import validate_html

        errors = validate_html(
            output,
            theme=canonical,
        )
        if errors:
            output_path.unlink(missing_ok=True)
            details = "\n".join(f"- {error}" for error in errors)
            raise RuntimeError(f"generated HTML failed validation:\n{details}")
    return output_path


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", nargs="?", type=Path, help=".docx, .md, .markdown, or .txt input")
    parser.add_argument("--theme", default="kami", help="theme key")
    parser.add_argument("--output", "-o", type=Path, help="output HTML path")
    parser.add_argument("--title", default="", help="override article title")
    parser.add_argument("--subtitle", default="", help="optional subtitle")
    parser.add_argument("--author", default="", help="optional author; never inferred")
    parser.add_argument("--qr", type=Path, help="optional local QR image")
    parser.add_argument("--no-validate", action="store_true", help="skip output validation")
    parser.add_argument("--list-themes", action="store_true", help="list available themes")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if args.list_themes:
        for key, theme in THEMES.items():
            print(f"{key:14} {theme.name} - {theme.description}")
        return 0
    if args.input is None:
        parser.error("input is required unless --list-themes is used")
    input_path = args.input.resolve()
    if not input_path.is_file():
        parser.error(f"input file not found: {input_path}")
    canonical = canonical_theme(args.theme)
    output_path = args.output or input_path.with_name(f"{input_path.stem}_{canonical}.wechat.html")
    output_path = output_path.resolve()
    try:
        result = convert(
            input_path,
            output_path,
            canonical,
            args.title,
            args.subtitle,
            args.author,
            args.qr.resolve() if args.qr else None,
            not args.no_validate,
        )
    except (OSError, RuntimeError, ValueError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    print(f"created: {result}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
