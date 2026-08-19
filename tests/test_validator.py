from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from convert import parse_markdown, render_html  # noqa: E402
from validate_html import validate_html  # noqa: E402


class ValidatorTests(unittest.TestCase):
    def setUp(self) -> None:
        self.valid = render_html(parse_markdown("正文", ROOT), "标题", "classic")

    def test_rejects_style_block_in_publish_output(self) -> None:
        errors = validate_html(self.valid.replace("</head>", "<style>p{color:red}</style></head>"), "classic")
        self.assertTrue(any("style block" in error for error in errors), errors)

    def test_rejects_external_image(self) -> None:
        bad = self.valid.replace("</main>", '<img src="https://example.com/a.png" style="width:100%;" /></main>')
        errors = validate_html(bad, "classic")
        self.assertTrue(any("non-base64 image" in error for error in errors), errors)

    def test_rejects_table_section_and_row_styles(self) -> None:
        bad = self.valid.replace("</main>", '<table style="width:100%;"><thead><tr style="color:red"><th style="padding:1px;">A</th></tr></thead></table></main>')
        errors = validate_html(bad, "classic")
        self.assertTrue(any("table tag" in error for error in errors), errors)
        self.assertTrue(any("row styles" in error for error in errors), errors)

    def test_rejects_missing_history_item(self) -> None:
        bad = self.valid.replace('data-history-item="3"', 'data-history-removed="3"')
        errors = validate_html(bad, "classic")
        self.assertTrue(any("expected 3" in error for error in errors), errors)

    def test_wechat_mode_rejects_custom_fonts(self) -> None:
        errors = validate_html(self.valid, "classic", wechat_mode=True)
        self.assertTrue(any("must not declare font-family" in error for error in errors), errors)


if __name__ == "__main__":
    unittest.main()
