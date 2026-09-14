from __future__ import annotations

import base64
import re
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
sys.path.insert(0, str(SCRIPTS))

from convert import (  # noqa: E402
    Block,
    DEFAULT_QR_PATH,
    LABEL_FONT,
    LAYOUT_VERSION,
    THEMES,
    canonical_theme,
    parse_docx,
    parse_markdown,
    render_html,
    _normalize_docx_blocks,
    _smart_heading,
)
from validate_html import validate_html  # noqa: E402


SAMPLE_MD = """# 基准文章标题

这是第一段正文，用于确认中文字体、行高与段落节奏。原始标签 <img src="https://example.com/a.png"> 必须被转义。

## 第一部分

> 设计不是装饰，而是信息优先级的可见表达。

- 结构应当清晰
- 数据应当可核查
- 图片应当自包含

## 第二部分

| 指标 | 结果 | 说明 |
|---|---|---|
| 完整率 | 100% | 主题均通过验证 |
| 外链图片 | 0 | 发布版全部内嵌 |

### 实现细节

正文包含 **重点信息**、*术语* 和 `inline code`。

```python
print("quality")
```
"""


class ConverterTests(unittest.TestCase):
    def test_theme_set_is_exactly_three(self) -> None:
        self.assertEqual(set(THEMES), {"kami", "esther", "punk"})
        for legacy in (
            "classic",
            "magazine",
            "fresh",
            "vibrant",
            "swiss",
            "minimal",
            "chinese",
            "narrative",
            "academic-blue",
            "cell",
            "signal",
            "orange",
            "nature",
            "blue",
            "morandi",
        ):
            with self.assertRaises(ValueError):
                canonical_theme(legacy)

    def test_kami_theme_uses_paper_and_chapter_components(self) -> None:
        blocks = parse_markdown(SAMPLE_MD, ROOT)
        document = render_html(blocks, "基准文章标题", "kami", wechat_mode=True)
        self.assertEqual(validate_html(document, "kami"), [])
        self.assertIn("KAMI / NOTE", document)
        self.assertIn("CHAPTER", document)
        self.assertIn("TAKEAWAY", document)
        self.assertNotIn("font-family", document)

    def test_esther_theme_uses_component_card_components(self) -> None:
        blocks = parse_markdown(SAMPLE_MD, ROOT)
        document = render_html(blocks, "基准文章标题", "esther", wechat_mode=True)
        self.assertEqual(validate_html(document, "esther"), [])
        self.assertIn("ESTHER / COMPONENTS", document)
        self.assertIn("COMPONENT", document)
        self.assertIn("PULL QUOTE", document)
        self.assertNotIn("font-family", document)

    def test_punk_theme_uses_practical_layout_components(self) -> None:
        blocks = parse_markdown(SAMPLE_MD, ROOT)
        document = render_html(blocks, "基准文章标题", "punk", wechat_mode=True)
        self.assertEqual(validate_html(document, "punk"), [])
        self.assertIn("PUNK 微排", document)
        self.assertIn("PART", document)
        self.assertIn("PRACTICE", document)
        self.assertNotIn("font-family", document)

    def test_all_themes_render_and_validate(self) -> None:
        blocks = parse_markdown(SAMPLE_MD, ROOT)
        outputs = []
        for key in THEMES:
            document = render_html(blocks, "基准文章标题", key, wechat_mode=True)
            self.assertEqual(validate_html(document, key), [], key)
            self.assertEqual(document.count("基准文章标题"), 2)  # title element and <title>
            self.assertIn("&lt;img src=&quot;https://example.com/a.png&quot;&gt;", document)
            self.assertNotIn("font-family", document)
            outputs.append(document)
        self.assertEqual(len(set(outputs)), len(THEMES))

    def test_rendering_is_byte_stable(self) -> None:
        blocks = parse_markdown(SAMPLE_MD, ROOT)
        for key in THEMES:
            first = render_html(blocks, "基准文章标题", key, wechat_mode=True)
            second = render_html(blocks, "基准文章标题", key, wechat_mode=True)
            self.assertEqual(first.encode("utf-8"), second.encode("utf-8"), key)

    def test_layout_contract_is_versioned_and_exact(self) -> None:
        document = render_html(parse_markdown("正文", ROOT), "标题", "kami", wechat_mode=True)
        body = re.search(r"<body\b[^>]*>", document)
        self.assertIsNotNone(body)
        body_tag = body.group(0)
        self.assertIn(f'data-layout-version="{LAYOUT_VERSION}"', body_tag)
        self.assertIn("max-width:677px", body_tag)
        self.assertIn("width:144px;height:144px", document)
        self.assertIn('data-fixed-footer="true"', document)
        self.assertIn('data-qr-code="true"', document)
        self.assertIn(DEFAULT_QR_PATH.name, str(DEFAULT_QR_PATH))

    def test_long_text_and_unbroken_strings_wrap_anywhere(self) -> None:
        long_title = "超长标题" * 40
        long_word = "A" * 240
        document = render_html(parse_markdown(long_word, ROOT), long_title, "punk", wechat_mode=True)
        self.assertIn("overflow-wrap:anywhere", document)
        self.assertGreaterEqual(document.count("overflow-wrap:anywhere"), 2)

    def test_wide_tables_use_scrollable_wrapper(self) -> None:
        table = "\n".join(
            [
                "| A | B | C | D | E | F |",
                "|---|---|---|---|---|---|",
                "| 1 | 2 | 3 | 4 | 5 | 6 |",
            ]
        )
        for key in THEMES:
            document = render_html(parse_markdown(table, ROOT), "表格", key, wechat_mode=True)
            wrapper_start = document.rfind("<div", 0, document.find("<table"))
            wrapper = document[wrapper_start : document.find("<table")]
            self.assertIn("overflow-x:auto", wrapper, key)
            self.assertIn("max-width:100%", wrapper, key)

    def test_all_themes_use_an_actual_qr_image(self) -> None:
        blocks = parse_markdown("正文", ROOT)
        for key in THEMES:
            document = render_html(blocks, "标题", key, wechat_mode=True)
            self.assertIn('data-qr-code="true"', document)
            self.assertIn("data:image/png;base64,", document)
            self.assertNotIn("data-qr-placeholder", document)
            self.assertNotIn("QR_CODE_IMAGE_BASE64_PLACEHOLDER", document)

    def test_list_and_quote_close_before_following_blocks(self) -> None:
        blocks = parse_markdown("- item\n## heading\n> quote\nafter", ROOT)
        self.assertEqual([block.kind for block in blocks], ["list", "heading", "quote", "paragraph"])
        document = render_html(blocks, "T", "kami", wechat_mode=True)
        self.assertNotIn("<ul", document[document.find("<h2"):])
        self.assertEqual(validate_html(document, "kami"), [])

    def test_external_markdown_image_is_rejected(self) -> None:
        with self.assertRaises(ValueError):
            parse_markdown("![bad](https://example.com/a.png)", ROOT)

    def test_unstyled_docx_editorial_structure_is_promoted(self) -> None:
        self.assertEqual(_smart_heading("第一道损耗：血清中的屏障"), 2)
        self.assertEqual(_smart_heading("三大工程策略：全链路耦合"), 2)
        blocks = _normalize_docx_blocks(
            [
                Block("paragraph", text="文章标题"),
                Block("paragraph", text="副标题：补充说明"),
                Block("quote", text="正文"),
                Block("image", data_uri="data:image/png;base64,AA=="),
                Block("paragraph", text="图 1：示意图"),
                Block("paragraph", text="来源：公开资料"),
                Block("paragraph", text="一句话：关键判断"),
            ]
        )
        self.assertEqual((blocks[0].kind, blocks[0].level), ("heading", 1))
        image = next(block for block in blocks if block.kind == "image")
        self.assertIn("来源：公开资料", image.caption)
        self.assertEqual(blocks[-1].kind, "quote")

    def test_wechat_output_is_default_and_removes_all_custom_font_declarations(self) -> None:
        blocks = parse_markdown("English 123 中文", ROOT)
        document = render_html(blocks, "标题", "kami")
        self.assertNotIn("font-family", document)
        self.assertNotIn("Caveat", document)
        self.assertNotIn("XuanZongTi", document)
        self.assertNotIn(LABEL_FONT, document)
        self.assertEqual(validate_html(document, "kami"), [])

    def test_docx_parses_heading_table_and_image(self) -> None:
        try:
            from docx import Document
        except ImportError:
            self.skipTest("python-docx is not installed")
        tiny_png = base64.b64decode(
            "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNk+A8AAQUBAScY42YAAAAASUVORK5CYII="
        )
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            image = root / "tiny.png"
            image.write_bytes(tiny_png)
            source = root / "sample.docx"
            doc = Document()
            doc.add_heading("Word 标题", level=1)
            doc.add_paragraph("正文段落")
            doc.add_picture(str(image))
            table = doc.add_table(rows=2, cols=2)
            table.cell(0, 0).text = "指标"
            table.cell(0, 1).text = "结果"
            table.cell(1, 0).text = "图片"
            table.cell(1, 1).text = "已提取"
            doc.save(source)
            blocks, _ = parse_docx(source)
        kinds = [block.kind for block in blocks]
        self.assertIn("heading", kinds)
        self.assertIn("image", kinds)
        self.assertIn("table", kinds)
        image_block = next(block for block in blocks if block.kind == "image")
        self.assertTrue(image_block.data_uri.startswith("data:image/"))


if __name__ == "__main__":
    unittest.main()
