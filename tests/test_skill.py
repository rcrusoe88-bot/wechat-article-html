from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))


class SkillPackageTests(unittest.TestCase):
    def test_frontmatter_and_required_assets(self) -> None:
        skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        self.assertTrue(skill.startswith("---\n"))
        self.assertIn("name: wechat-article-html", skill)
        self.assertIn("description:", skill)
        self.assertTrue((ROOT / "agents" / "openai.yaml").is_file())
        self.assertTrue((ROOT / "assets" / "fonts" / "Caveat-Bold.ttf").is_file())
        self.assertTrue((ROOT / "assets" / "fonts" / "XuanZongTi.otf").is_file())
        self.assertTrue((ROOT / "assets" / "images" / "qr-placeholder.png").is_file())
        self.assertTrue((ROOT / "assets" / "fonts" / "Caveat-OFL.txt").is_file())
        self.assertTrue((ROOT / "assets" / "fonts" / "XuanZongTi-OFL.txt").is_file())
        self.assertGreater((ROOT / "assets" / "fonts" / "XuanZongTi.otf").stat().st_size, 1_000_000)
        self.assertGreater((ROOT / "assets" / "fonts" / "Caveat-Bold.ttf").stat().st_size, 100_000)

    def test_no_old_font_or_stale_converter_contract(self) -> None:
        files = [
            ROOT / "SKILL.md",
            ROOT / "README.md",
            ROOT / "THIRD_PARTY_NOTICES.md",
            ROOT / "references" / "themes.md",
            ROOT / "references" / "quality.md",
            ROOT / "scripts" / "convert.py",
            ROOT / "scripts" / "validate_html.py",
            ROOT / "scripts" / "build_gallery.py",
            ROOT / "agents" / "openai.yaml",
        ]
        combined = "\n".join(path.read_text(encoding="utf-8") for path in files)
        self.assertNotIn("TiGuFangSong", combined)
        self.assertNotIn("tkFangSong", combined)
        self.assertNotIn("PreTesto", combined)
        self.assertNotIn("cdn.jsdelivr.net", combined)

    def test_only_three_theme_keys_are_documented(self) -> None:
        docs = "\n".join(
            (ROOT / path).read_text(encoding="utf-8")
            for path in ("README.md", "SKILL.md", "references/themes.md")
        )
        for legacy in ("classic", "magazine", "fresh", "vibrant", "swiss", "minimal", "chinese", "narrative", "academic-blue", "cell", "signal", "orange", "nature", "blue", "morandi"):
            self.assertNotIn(f"`{legacy}`", docs, legacy)
        for key in ("kami", "esther", "punk"):
            self.assertIn(f"`{key}`", docs, key)

    def test_example_builders_emit_wechat_only(self) -> None:
        for script in (ROOT / "scripts" / "build_gallery.py", ROOT / "scripts" / "build_showcase.py"):
            content = script.read_text(encoding="utf-8")
            self.assertIn("wechat_mode=True", content, script.name)
            self.assertNotIn("embedded_fonts=True", content, script.name)
            self.assertNotIn("preview_fonts=True", content, script.name)

    def test_skill_contract_is_wechat_only(self) -> None:
        skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        prompt = (ROOT / "agents" / "openai.yaml").read_text(encoding="utf-8")
        self.assertIn("微信公众号", skill)
        self.assertIn("font-family", skill)
        self.assertNotIn("--wechat", skill)
        self.assertIn("微信公众号", prompt)
        self.assertNotIn("不要使用 --wechat", prompt)

    def test_showcase_contains_no_non_wechat_html(self) -> None:
        showcase = ROOT / "examples" / "showcase"
        html_files = sorted(path.name for path in showcase.glob("*.html"))
        self.assertEqual(html_files, ["esther.wechat.html", "kami.wechat.html", "punk.wechat.html"])

    def test_release_packaging_script(self) -> None:
        import tempfile
        from package_release import package_skill
        with tempfile.TemporaryDirectory() as tmpdir:
            zip_path = package_skill("1.0.0", Path(tmpdir))
            self.assertTrue(zip_path.is_file())
            self.assertEqual(zip_path.name, "wechat-article-html-v1.0.0.zip")
            self.assertTrue((Path(tmpdir) / "wechat-article-html-v1.0.0.zip.sha256").is_file())


if __name__ == "__main__":
    unittest.main()
