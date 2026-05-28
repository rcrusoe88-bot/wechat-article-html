#!/usr/bin/env python3
"""
WeChat Article HTML Converter
将 Word(.docx) 转化为微信公众号兼容全内联式 HTML

用法:
  python3 convert.py --input article.docx --theme orange --output out.html
  python3 convert.py --input article.docx --theme blue --output out.html --qr qr.jpg
"""

import argparse
import base64
import os
import re
import sys
from pathlib import Path

try:
    from docx import Document
    from docx.oxml.ns import qn
except ImportError:
    print("请安装 python-docx: pip install python-docx --break-system-packages")
    sys.exit(1)


# ─────────────────────────────────────────────
# 主题定义
# ─────────────────────────────────────────────

THEMES = {
    "orange": {
        "name": "橙皮书",
        "label": "技术白皮书",
        "body": "margin:0;padding:0;background:#f5f0e8;font-family:-apple-system,'PingFang SC','Helvetica Neue',Arial,sans-serif;color:#1a0800;line-height:1.8;",
        "container": "max-width:680px;margin:0 auto;background:#fffbf0;",
        "top_band": "background:#e85d04;height:8px;",
        "bottom_band1": "background:#e85d04;height:8px;margin-top:8px;",
        "bottom_band2": None,
        "header_wrap": "padding:16px 28px 14px;display:flex;justify-content:space-between;align-items:center;border-bottom:1px solid #f0e8d8;",
        "header_label": "font-size:11px;font-weight:700;color:#e85d04;letter-spacing:0.1em;",
        "header_vol": "font-size:11px;color:#999;",
        "series_badge": "display:inline-block;background:#e85d04;color:#fff;font-size:11px;font-weight:700;letter-spacing:0.08em;padding:4px 12px;border-radius:2px;margin-bottom:16px;",
        "h1": "font-size:22px;font-weight:800;color:#1a0800;line-height:1.35;margin:0 0 12px;padding-bottom:16px;border-bottom:3px solid #e85d04;",
        "subtitle": "font-size:14px;color:#7a4020;line-height:1.6;margin:0 0 14px;font-style:italic;",
        "source_box": "font-size:11px;color:#999;background:#f5ece0;border-left:3px solid #f97316;padding:8px 12px;border-radius:0 4px 4px 0;margin-bottom:24px;",
        "stat_row": "display:flex;gap:12px;margin:0 28px 24px;",
        "stat_card": "flex:1;background:#fff8f0;border:1px solid #fcd9b6;border-radius:6px;padding:14px 10px;text-align:center;",
        "stat_num": "font-size:26px;font-weight:800;color:#e85d04;line-height:1;margin-bottom:4px;",
        "stat_label": "font-size:10px;color:#a05030;line-height:1.4;",
        "abstract_box": "margin:0 28px 20px;background:#fff8f0;border:1px solid #fcd9b6;border-radius:6px;padding:16px 20px;",
        "abstract_label": "font-size:10px;font-weight:700;color:#e85d04;letter-spacing:0.1em;text-transform:uppercase;margin-bottom:8px;",
        "abstract_label_text": "摘要 Abstract",
        "abstract_text": "font-size:13px;color:#4a2010;line-height:1.75;margin:0;",
        "keyword_wrap": "padding:0 28px 20px;display:flex;flex-wrap:wrap;gap:6px;",
        "keyword": "font-size:11px;padding:3px 10px;background:#fff3e0;border:1px solid #f97316;color:#c2410c;border-radius:3px;",
        "toc_wrap": "margin:0 28px 28px;border:1px solid #e8d0b0;border-radius:6px;overflow:hidden;",
        "toc_header": "background:#e85d04;color:#fff;font-size:11px;font-weight:700;letter-spacing:0.08em;padding:8px 16px;text-transform:uppercase;",
        "toc_header_text": "目录 Contents",
        "toc_row": "display:flex;justify-content:space-between;align-items:center;padding:9px 16px;border-bottom:1px solid #f0e4d0;font-size:13px;color:#3a1a08;",
        "toc_row_alt": "display:flex;justify-content:space-between;align-items:center;padding:9px 16px;border-bottom:1px solid #f0e4d0;font-size:13px;color:#3a1a08;background:#fffaf4;",
        "toc_num": "font-size:11px;font-weight:700;color:#e85d04;",
        "divider": "height:2px;background:linear-gradient(to right,#e85d04 30%,#fcd9b6 100%);margin:0 28px 28px;border-radius:1px;",
        "section_pad": "padding:0 28px 32px;",
        "h2": "font-size:18px;font-weight:800;color:#1a0800;line-height:1.4;margin:0 0 16px;padding-bottom:10px;border-bottom:2px solid #e85d04;",
        "h2_num": "color:#e85d04;font-size:14px;font-weight:700;display:block;margin-bottom:4px;",
        "h3": "font-size:15px;font-weight:700;color:#e85d04;margin:0 0 12px;padding-left:10px;border-left:3px solid #e85d04;",
        "p": "font-size:15px;color:#2a1000;line-height:1.9;margin:0 0 16px;text-align:justify;",
        "callout_wrap": "background:#fff3e0;border:1px solid #fcd9b6;border-left:4px solid #e85d04;border-radius:0 6px 6px 0;padding:14px 18px;margin:18px 0;",
        "callout_label": "font-size:11px;font-weight:700;color:#e85d04;text-transform:uppercase;letter-spacing:0.08em;margin-bottom:6px;",
        "callout_text": "font-size:14px;color:#7a3010;line-height:1.7;",
        "figure_wrap": "background:#f5ece0;border-radius:6px;padding:12px;margin:20px 0;",
        "figure_caption": "font-size:11px;color:#a05030;text-align:center;margin:8px 0 0;line-height:1.4;",
        "li": "font-size:14px;color:#2a1000;line-height:1.8;margin-bottom:6px;",
        "qr_wrap": "padding:24px 28px;text-align:center;background:#fff8f0;border-top:1px solid #fcd9b6;",
        "qr_caption": "font-size:13px;color:#7a4020;margin:0 0 12px;",
        "qr_img": "width:160px;height:160px;border:3px solid #f97316;border-radius:8px;display:block;margin:0 auto 12px;",
        "qr_placeholder": "width:160px;height:160px;border:3px solid #f97316;border-radius:8px;display:flex;align-items:center;justify-content:center;margin:0 auto 12px;background:#fff3e0;",
        "qr_placeholder_text": "font-size:11px;color:#e85d04;text-align:center;padding:8px;",
        "qr_footnote": "font-size:11px;color:#999;margin:0;",
        "series_label": "RNAscript · 技术白皮书",
        "vol_text": "Vol.{vol} · {year}",
    },
    "blue": {
        "name": "学术深蓝",
        "label": "学术综述",
        "body": "margin:0;padding:0;background:#eef2f7;font-family:-apple-system,'PingFang SC','Helvetica Neue',Arial,sans-serif;color:#0f172a;line-height:1.85;",
        "container": "max-width:680px;margin:0 auto;background:#f8fafd;",
        "top_band": "background:#1e3a5f;height:6px;",
        "top_band2": "background:#2563eb;height:2px;",
        "bottom_band1": "background:#2563eb;height:2px;margin-top:8px;",
        "bottom_band2": "background:#1e3a5f;height:6px;",
        "header_wrap": "padding:14px 28px 12px;display:flex;justify-content:space-between;align-items:center;border-bottom:1px solid #bfdbfe;",
        "header_label": "font-size:11px;font-weight:700;color:#1e3a5f;letter-spacing:0.12em;font-family:-apple-system,sans-serif;",
        "header_vol": "font-size:11px;color:#94a3b8;font-family:-apple-system,sans-serif;",
        "series_badge": "display:inline-block;background:#1e3a5f;color:#fff;font-size:10px;font-weight:700;letter-spacing:0.1em;padding:4px 12px;border-radius:2px;margin-bottom:16px;font-family:-apple-system,sans-serif;",
        "h1": "font-size:22px;font-weight:700;color:#0f172a;line-height:1.4;margin:0 0 14px;padding-bottom:16px;border-bottom:3px solid #1e3a5f;font-family:Georgia,'Songti SC',serif;",
        "subtitle": "font-size:14px;color:#334e7a;line-height:1.65;margin:0 0 14px;font-style:italic;font-family:Georgia,'Songti SC',serif;",
        "source_box": "font-size:11px;color:#94a3b8;background:#e8f0fb;border-left:3px solid #2563eb;padding:8px 12px;border-radius:0 4px 4px 0;margin-bottom:24px;font-family:-apple-system,sans-serif;",
        "stat_row": "display:flex;gap:12px;margin:0 28px 24px;",
        "stat_card": "flex:1;background:#f0f7ff;border:1px solid #bfdbfe;border-radius:6px;padding:14px 10px;text-align:center;",
        "stat_num": "font-size:24px;font-weight:700;color:#1e3a5f;line-height:1;margin-bottom:4px;font-family:Georgia,serif;",
        "stat_label": "font-size:10px;color:#4a6fa5;line-height:1.4;font-family:-apple-system,sans-serif;",
        "abstract_box": "margin:0 28px 20px;background:#f0f7ff;border:1px solid #bfdbfe;border-radius:6px;padding:16px 20px;",
        "abstract_label": "font-size:10px;font-weight:700;color:#1e3a5f;letter-spacing:0.12em;text-transform:uppercase;margin-bottom:8px;font-family:-apple-system,sans-serif;",
        "abstract_label_text": "ABSTRACT · 摘要",
        "abstract_text": "font-size:13px;color:#1e293b;line-height:1.8;margin:0;",
        "keyword_wrap": "padding:0 28px 20px;display:flex;flex-wrap:wrap;gap:6px;",
        "keyword": "font-size:11px;padding:3px 10px;background:#dbeafe;border:1px solid #93c5fd;color:#1e40af;border-radius:3px;font-family:-apple-system,sans-serif;",
        "toc_wrap": "margin:0 28px 28px;border:1px solid #bfdbfe;border-radius:6px;overflow:hidden;",
        "toc_header": "background:#1e3a5f;color:#fff;font-size:11px;font-weight:700;letter-spacing:0.1em;padding:8px 16px;text-transform:uppercase;font-family:-apple-system,sans-serif;",
        "toc_header_text": "CONTENTS · 目录",
        "toc_row": "display:flex;justify-content:space-between;align-items:center;padding:9px 16px;border-bottom:1px solid #e0eaff;font-size:13px;color:#1e3a5f;",
        "toc_row_alt": "display:flex;justify-content:space-between;align-items:center;padding:9px 16px;border-bottom:1px solid #e0eaff;font-size:13px;color:#1e3a5f;background:#f4f8ff;",
        "toc_num": "font-size:11px;font-weight:700;color:#2563eb;",
        "divider": "height:2px;background:linear-gradient(to right,#1e3a5f 30%,#dbeafe 100%);margin:0 28px 28px;border-radius:1px;",
        "section_pad": "padding:0 28px 32px;",
        "h2": "font-size:18px;font-weight:700;color:#0f172a;line-height:1.4;margin:0 0 16px;padding-bottom:10px;border-bottom:2px solid #1e3a5f;font-family:Georgia,'Songti SC',serif;",
        "h2_num": "color:#2563eb;font-size:13px;font-weight:700;display:block;margin-bottom:4px;font-family:-apple-system,sans-serif;letter-spacing:0.05em;",
        "h3": "font-size:15px;font-weight:700;color:#1e3a5f;margin:0 0 12px;padding-left:10px;border-left:3px solid #2563eb;font-family:Georgia,'Songti SC',serif;",
        "p": "font-size:15px;color:#1e293b;line-height:1.9;margin:0 0 16px;text-align:justify;",
        "callout_wrap": "background:#eff6ff;border:1px solid #bfdbfe;border-left:4px solid #2563eb;border-radius:0 6px 6px 0;padding:14px 18px;margin:18px 0;",
        "callout_label": "font-size:10px;font-weight:700;color:#1e3a5f;text-transform:uppercase;letter-spacing:0.1em;margin-bottom:6px;font-family:-apple-system,sans-serif;",
        "callout_text": "font-size:14px;color:#334e7a;line-height:1.75;",
        "figure_wrap": "background:#e8f0fb;border-radius:6px;padding:12px;margin:20px 0;",
        "figure_caption": "font-size:11px;color:#4a6fa5;text-align:center;margin:8px 0 0;line-height:1.4;font-family:-apple-system,sans-serif;",
        "li": "font-size:14px;color:#1e293b;line-height:1.85;margin-bottom:6px;",
        "qr_wrap": "padding:24px 28px;text-align:center;background:#f0f7ff;border-top:1px solid #bfdbfe;",
        "qr_caption": "font-size:13px;color:#334e7a;margin:0 0 12px;font-family:-apple-system,sans-serif;",
        "qr_img": "width:160px;height:160px;border:3px solid #2563eb;border-radius:8px;display:block;margin:0 auto 12px;",
        "qr_placeholder": "width:160px;height:160px;border:3px solid #2563eb;border-radius:8px;display:flex;align-items:center;justify-content:center;margin:0 auto 12px;background:#dbeafe;",
        "qr_placeholder_text": "font-size:11px;color:#1e3a5f;text-align:center;padding:8px;font-family:-apple-system,sans-serif;",
        "qr_footnote": "font-size:11px;color:#94a3b8;margin:0;font-family:-apple-system,sans-serif;",
        "series_label": "RNAscript · 学术综述",
        "vol_text": "Vol.{vol} · {year}",
    },
    "nature": {
        "name": "Nature · 极简学术",
        "label": "极简学术",
    },
    "cell": {
        "name": "Cell · 期刊封面",
        "label": "期刊封面",
    },
}


# ─────────────────────────────────────────────
# 智能章节嗅探
# ─────────────────────────────────────────────

# 识别 "§01" "§12" 等独立节标志段落
SECTION_MARKER_RE = re.compile(r'^§(\d+)$')
# 识别 "§行业惯性批判" "§结语" "§参考资料" 等内联节标题
SECTION_HEADING_RE = re.compile(r'^§\w')
# 识别 "第X章" "第X节" "第X部分" 等中文节标志
CHAPTER_MARKER_RE = re.compile(r'^第[一二三四五六七八九十百千\d]+[章节部篇]')
# 识别 "一、" "二、" "十二、" 等中文数字编号标题 → H2
CN_NUM_HEADING_RE = re.compile(r'^[一二三四五六七八九十]+、')
# 识别 "2.1" "3.2" "10.1" 等数字子标题 → H3
SUB_HEADING_RE = re.compile(r'^\d+\.\d+\s')
# 识别 "Figure X |" 格式的图注 → figure caption
FIGURE_CAPTION_RE = re.compile(r'^Figure\s+\d+\s*[|｜]')
# 特殊标题词（导语、结语等）→ H2
SPECIAL_HEADINGS = {'导语', '结语', '引言', '前言', '背景', '总结', '参考文献', '参考资料', 'References',
                     '封面提示词', '封面图提示词', '下一篇', '下一篇选题延伸建议',
                     '致谢', '附录', '补充材料', '技术上游方向', 'CMC/监管视角方向', '产业化落地方向'}


def smart_sniff_headings(items):
    """
    后处理：将普通段落中符合章节模式的条目提升为 h2 或 h3。
    处理模式：
      模式A：连续两个段落 ["§01", "AMBITION..."] → 合并为一个 h2 "AMBITION..."
      模式B：单个段落 "§结语" → 直接提升为 h2
      模式C：中文编号 "一、xxx" → h2
      模式D：数字子标题 "2.1 xxx" → h3
      模式E：特殊标题词（导语、结语等）→ h2
      模式F：Figure X | ... → figure
      模式G：中文章节 "第一章" → h2
    自动编号由 build_html 的 section_nums 系统处理，不在标题文本中重复。
    """
    sniffed = []
    pending_marker = None  # 存储待合并的独立节标志（如 "§01"）

    for it in items:
        if it["type"] != "p":
            # 非纯文本段落，先刷出待合并标志
            if pending_marker:
                sniffed.append({"type": "h2", "text": pending_marker})
                pending_marker = None
            sniffed.append(it)
            continue

        text = it["text"]

        # 模式A：独立节标志 "§01", "§02"
        m = SECTION_MARKER_RE.match(text)
        if m:
            if pending_marker:
                sniffed.append({"type": "h2", "text": pending_marker})
            pending_marker = f"§{m.group(1)}"
            continue

        # 模式B：内联节标题 "§行业惯性批判"
        if SECTION_HEADING_RE.match(text):
            if pending_marker:
                sniffed.append({"type": "h2", "text": pending_marker})
                pending_marker = None
            sniffed.append({"type": "h2", "text": text})
            continue

        # 模式G：中文章节 "第一章"
        if CHAPTER_MARKER_RE.match(text):
            if pending_marker:
                sniffed.append({"type": "h2", "text": pending_marker})
                pending_marker = None
            sniffed.append({"type": "h2", "text": text})
            continue

        # 模式C：中文数字编号 "一、xxx" → H2
        if CN_NUM_HEADING_RE.match(text):
            if pending_marker:
                sniffed.append({"type": "h2", "text": pending_marker})
                pending_marker = None
            sniffed.append({"type": "h2", "text": text})
            continue

        # 模式D：数字子标题 "2.1 xxx" → H3
        if SUB_HEADING_RE.match(text):
            if pending_marker:
                sniffed.append({"type": "h2", "text": pending_marker})
                pending_marker = None
            sniffed.append({"type": "h3", "text": text})
            continue

        # 模式E：特殊标题词 → H2
        if text.strip() in SPECIAL_HEADINGS:
            if pending_marker:
                sniffed.append({"type": "h2", "text": pending_marker})
                pending_marker = None
            sniffed.append({"type": "h2", "text": text})
            continue

        # 模式F：Figure caption → 保持为 p，但标记为 figure
        if FIGURE_CAPTION_RE.match(text):
            if pending_marker:
                sniffed.append({"type": "h2", "text": pending_marker})
                pending_marker = None
            sniffed.append({"type": "figure", "text": text})
            continue

        # 普通段落：如有待合并标志，合并为 h2
        if pending_marker:
            sniffed.append({"type": "h2", "text": text})
            pending_marker = None
        else:
            sniffed.append(it)

    # 末尾遗留的待合并标志
    if pending_marker:
        sniffed.append({"type": "h2", "text": pending_marker})

    return sniffed


# ─────────────────────────────────────────────
# 文档解析
# ─────────────────────────────────────────────

def extract_images(docx_path):
    """提取文档中所有图片，返回 [{b64, ext, mime}] 列表（按关系顺序）"""
    doc = Document(docx_path)
    images = []
    seen = set()
    for rel in doc.part.rels.values():
        if "image" in rel.reltype and rel.target_ref not in seen:
            seen.add(rel.target_ref)
            blob = rel.target_part.blob
            b64 = base64.b64encode(blob).decode()
            ct = rel.target_part.content_type  # e.g. "image/jpeg"
            ext = ct.split("/")[-1].replace("png", "png").replace("jpeg", "jpeg")
            images.append({"b64": b64, "ext": ext, "mime": ct})
    return images


def parse_paragraphs(docx_path):
    """
    解析文档段落，返回结构化列表：
    每项为 dict，type 为 h1/h2/h3/p/li/img
    """
    doc = Document(docx_path)
    items = []

    # 提取图片（顺序）
    images = extract_images(docx_path)
    img_idx = [0]  # 使用列表以支持嵌套修改

    # 检测段落是否包含图片（用元素查找，避免误判 xmlns 声明）
    def para_has_image(para):
        return (
            len(para._element.findall('.//' + qn('w:drawing'))) > 0 or
            len(para._element.findall('.//' + qn('w:pict'))) > 0
        )

    for para in doc.paragraphs:
        text = para.text.strip()
        style = para.style.name if para.style else "Normal"

        # 图片段落
        if para_has_image(para):
            if img_idx[0] < len(images):
                items.append({"type": "img", "data": images[img_idx[0]]})
                img_idx[0] += 1
            continue

        # 跳过空段落
        if not text:
            continue

        # 标题
        if style == "Heading 1" or style.startswith("标题 1"):
            items.append({"type": "h1", "text": text})
        elif style == "Heading 2" or style.startswith("标题 2"):
            items.append({"type": "h2", "text": text})
        elif style == "Heading 3" or style.startswith("标题 3"):
            items.append({"type": "h3", "text": text})
        # 列表
        elif style == "List Paragraph" or text.startswith(("•", "·", "-", "●", "◆", "*")):
            clean = text.lstrip("•·-●◆* \t")
            items.append({"type": "li", "text": clean})
        # 正文
        else:
            items.append({"type": "p", "text": text})

    # 未插入的图片追加到末尾
    while img_idx[0] < len(images):
        items.append({"type": "img", "data": images[img_idx[0]]})
        img_idx[0] += 1

    return items


# ─────────────────────────────────────────────
# HTML 生成
# ─────────────────────────────────────────────

def esc(s):
    """HTML 转义"""
    return (s.replace("&", "&amp;")
             .replace("<", "&lt;")
             .replace(">", "&gt;")
             .replace('"', "&quot;"))


def build_html(items, theme_name="orange", title="文章标题", subtitle="",
               keywords=None, abstract="", source="", series_tag="深度解读",
               qr_path=None, vol="01", year="2025"):
    """
    将解析后的段落列表生成完整 HTML 字符串
    """
    t = THEMES.get(theme_name, THEMES["orange"])
    kws = keywords or []

    # 读取 QR 码
    qr_b64 = None
    qr_mime = "image/jpeg"
    if qr_path and os.path.exists(qr_path):
        with open(qr_path, "rb") as f:
            qr_b64 = base64.b64encode(f.read()).decode()
        ext = Path(qr_path).suffix.lower()
        qr_mime = "image/png" if ext == ".png" else "image/jpeg"

    # ── 收集标题用于 TOC ──
    # 不参与编号的特殊标题集合
    NO_NUM_HEADINGS = {"导语", "引言", "前言", "结语", "总结", "参考文献", "参考资料", "References",
                       "封面提示词", "封面图提示词", "下一篇", "下一篇选题延伸建议",
                       "致谢", "附录", "补充材料", "技术上游方向", "CMC/监管视角方向", "产业化落地方向"}
    headings = [(it["type"], it["text"]) for it in items if it["type"] in ("h1", "h2", "h3")]
    section_nums = {}
    h2_count = 0
    h3_count = {}
    for htype, htxt in headings:
        if htype == "h2":
            if htxt.strip() not in NO_NUM_HEADINGS:
                h2_count += 1
                section_nums[htxt] = f"§{h2_count}"
                h3_count[h2_count] = 0
            # 特殊标题不编号
        elif htype == "h3":
            h3_count[h2_count] = h3_count.get(h2_count, 0) + 1
            section_nums[htxt] = f"§{h2_count}.{h3_count[h2_count]}"

    # ── 数据卡片（从段落提取数字）──
    stat_candidates = []
    for it in items:
        if it["type"] == "p":
            nums = re.findall(r"(\d+(?:\.\d+)?%|\d+(?:\.\d+)?[kKmMnNntT]+)", it["text"])
            for n in nums[:3]:
                if n not in [s[0] for s in stat_candidates]:
                    stat_candidates.append((n, it["text"][:30] + "…"))
            if len(stat_candidates) >= 3:
                break

    # ── 开始拼 HTML ──
    lines = []
    a = lines.append  # 简写

    a('<!DOCTYPE html>')
    a('<html lang="zh-CN">')
    a('<head>')
    a('<meta charset="UTF-8">')
    a('<meta name="viewport" content="width=device-width, initial-scale=1.0">')
    a(f'<title>{esc(title)}</title>')
    a('</head>')
    a(f'<body style="{t["body"]}">')
    a('')
    a(f'<div style="{t["container"]}">')
    a('')
    a(f'<!-- 顶部色带 -->')
    a(f'<div style="{t["top_band"]}"></div>')
    if theme_name == "blue" and "top_band2" in t:
        a(f'<div style="{t["top_band2"]}"></div>')
    a('')

    # 页眉
    vol_text = t["vol_text"].format(vol=vol, year=year)
    a(f'<!-- 页眉 -->')
    a(f'<div style="{t["header_wrap"]}">')
    a(f'  <span style="{t["header_label"]}">{esc(t["series_label"])}</span>')
    a(f'  <span style="{t["header_vol"]}">{esc(vol_text)}</span>')
    a(f'</div>')
    a('')

    # 封面
    a(f'<!-- 封面 -->')
    a(f'<div style="padding:28px 28px 0;">')
    a(f'  <span style="{t["series_badge"]}">{esc(series_tag)}</span>')
    a(f'  <h1 style="{t["h1"]}">{esc(title)}</h1>')
    if subtitle:
        a(f'  <p style="{t["subtitle"]}">{esc(subtitle)}</p>')
    if source:
        a(f'  <div style="{t["source_box"]}">文献来源：{esc(source)}</div>')
    a(f'</div>')
    a('')

    # 数据卡（若有足够的数字）
    if len(stat_candidates) >= 2:
        a(f'<!-- 数据卡片 -->')
        a(f'<div style="{t["stat_row"]}">')
        for num, label in stat_candidates[:2]:
            a(f'  <div style="{t["stat_card"]}">')
            a(f'    <div style="{t["stat_num"]}">{esc(num)}</div>')
            a(f'    <div style="{t["stat_label"]}">{esc(label)}</div>')
            a(f'  </div>')
        a(f'</div>')
        a('')

    # 摘要
    if abstract:
        a(f'<!-- 摘要 -->')
        a(f'<div style="{t["abstract_box"]}">')
        a(f'  <div style="{t["abstract_label"]}">{t["abstract_label_text"]}</div>')
        a(f'  <p style="{t["abstract_text"]}">{esc(abstract)}</p>')
        a(f'</div>')
        a('')

    # 关键词
    if kws:
        a(f'<!-- 关键词 -->')
        a(f'<div style="{t["keyword_wrap"]}">')
        for kw in kws:
            a(f'  <span style="{t["keyword"]}">{esc(kw)}</span>')
        a(f'</div>')
        a('')

    # 目录
    if headings:
        a(f'<!-- 目录 -->')
        a(f'<div style="{t["toc_wrap"]}">')
        a(f'  <div style="{t["toc_header"]}">{t["toc_header_text"]}</div>')
        alt = False
        for htype, htxt in headings:
            if htxt.strip() in NO_NUM_HEADINGS:
                continue  # TOC 中不显示特殊标题
            row_style = t["toc_row_alt"] if alt else t["toc_row"]
            num = section_nums.get(htxt, "")
            if htype == "h2":
                a(f'  <div style="{row_style}">')
                a(f'    <span>{esc(htxt)}</span>')
                a(f'    <span style="{t["toc_num"]}">{num}</span>')
                a(f'  </div>')
                alt = not alt
            # h3 不显示在目录中（保持简洁）
        a(f'</div>')
        a('')

    # 主分隔线
    a(f'<div style="{t["divider"]}"></div>')
    a('')

    # ── 正文内容 ──
    in_list = False
    img_counter = [0]
    h2_sect = [0]

    def close_list():
        nonlocal in_list
        if in_list:
            a('</ul>')
            in_list = False

    a(f'<!-- 正文 -->')
    a(f'<div style="{t["section_pad"]}">')

    for it in items:
        itype = it["type"]

        if itype == "h1":
            close_list()
            # H1 已在封面区域，跳过
            continue

        elif itype == "h2":
            close_list()
            # 关闭上一节
            a('</div>')
            text = it["text"]
            is_special = any(text.strip().startswith(k) for k in NO_NUM_HEADINGS)

            if not is_special:
                h2_sect[0] += 1

            num = section_nums.get(text, "")
            # 特殊标题（导语、结语等）用不同渲染
            if text.strip() in ("导语", "引言", "前言"):
                a('')
                a(f'<div style="padding:0 28px 8px;">')
                a(f'  <div style="display:inline-block;background:#1e3a5f;color:#fff;font-size:12px;font-weight:700;letter-spacing:0.08em;padding:4px 14px;border-radius:3px;font-family:-apple-system,sans-serif;">{esc(text)}</div>')
                a(f'</div>')
            elif text.strip().startswith(("参考文献", "参考资料", "References")):
                a('')
                a(f'<div style="{t["section_pad"]}">')
                a(f'  <div style="display:flex;align-items:center;gap:8px;margin-bottom:16px;">')
                a(f'    <div style="width:40px;height:2px;background:#2563eb;border-radius:1px;"></div>')
                a(f'    <span style="font-size:15px;font-weight:700;color:#0f172a;letter-spacing:0.02em;">{esc(text)}</span>')
                a(f'  </div>')
            elif text.strip().startswith(("封面提示词", "封面图提示词")):
                a('')
                a(f'<div style="{t["section_pad"]}">')
                a(f'  <div style="display:flex;align-items:center;gap:8px;margin-bottom:16px;">')
                a(f'    <div style="width:40px;height:2px;background:#93c5fd;border-radius:1px;"></div>')
                a(f'    <span style="font-size:14px;font-weight:600;color:#475569;">{esc(text)}</span>')
                a(f'  </div>')
            elif text.strip().startswith(("下一篇", "技术上游", "CMC", "产业化")):
                # 末尾补充信息，淡化处理
                a('')
                a(f'<div style="{t["section_pad"]}">')
                a(f'  <div style="display:flex;align-items:center;gap:8px;margin-bottom:16px;">')
                a(f'    <div style="width:40px;height:2px;background:#cbd5e1;border-radius:1px;"></div>')
                a(f'    <span style="font-size:14px;font-weight:600;color:#64748b;">{esc(text)}</span>')
                a(f'  </div>')
            elif text.strip().startswith("结语"):
                a('')
                a(f'<div style="{t["section_pad"]}">')
                a(f'  <h2 style="font-size:18px;font-weight:700;color:#0f172a;line-height:1.4;margin:0 0 16px;padding-bottom:10px;border-bottom:2px solid #2563eb;font-family:Georgia,\'Songti SC\',serif;">{esc(text)}</h2>')
            else:
                a('')
                a(f'<div style="{t["section_pad"]}">')
                a(f'  <h2 style="{t["h2"]}">')
                a(f'    <span style="{t["h2_num"]}">{num}</span>')
                a(f'    {esc(text)}')
                a(f'  </h2>')

        elif itype == "h3":
            close_list()
            a(f'  <h3 style="{t["h3"]}">{esc(it["text"])}</h3>')

        elif itype == "figure":
            close_list()
            a(f'  <div style="background:#f0f4fa;border-radius:6px;padding:10px 14px;margin:16px 0;border-left:3px solid #93c5fd;">')
            a(f'    <p style="font-size:12px;color:#475569;line-height:1.65;margin:0;font-family:-apple-system,sans-serif;">{esc(it["text"])}</p>')
            a(f'  </div>')

        elif itype == "p":
            close_list()
            a(f'  <p style="{t["p"]}">{esc(it["text"])}</p>')

        elif itype == "li":
            if not in_list:
                a(f'  <ul style="margin:0 0 16px;padding-left:20px;">')
                in_list = True
            a(f'    <li style="{t["li"]}">{esc(it["text"])}</li>')

        elif itype == "img":
            close_list()
            img_counter[0] += 1
            d = it["data"]
            img_src = f'data:{d["mime"]};base64,{d["b64"]}'
            a(f'  <div style="{t["figure_wrap"]}">')
            a(f'    <img src="{img_src}" style="width:100%;display:block;border-radius:4px;" alt="图{img_counter[0]}">')
            a(f'    <p style="{t["figure_caption"]}">图{img_counter[0]}</p>')
            a(f'  </div>')

    close_list()
    a('</div>')  # 关闭最后一个 section_pad
    a('')

    # 底部色带
    a(f'<!-- 底部色带 -->')
    a(f'<div style="{t["bottom_band1"]}"></div>')
    if t.get("bottom_band2"):
        a(f'<div style="{t["bottom_band2"]}"></div>')
    a('')

    # 二维码区域
    a(f'<!-- 关注区 -->')
    a(f'<div style="{t["qr_wrap"]}">')
    a(f'  <p style="{t["qr_caption"]}">扫码关注 · 获取最新内容</p>')
    if qr_b64:
        a(f'  <img src="data:{qr_mime};base64,{qr_b64}" style="{t["qr_img"]}" alt="公众号二维码">')
    else:
        a(f'  <div style="{t["qr_placeholder"]}">')
        a(f'    <span style="{t["qr_placeholder_text"]}">扫码关注<br>公众号</span>')
        a(f'  </div>')
    a(f'  <p style="{t["qr_footnote"]}">{esc(t["series_label"])}</p>')
    a(f'</div>')
    a('')

    a('</div>')  # 关闭主容器
    a('</body>')
    a('</html>')

    return "\n".join(lines)


# ─────────────────────────────────────────────
# Nature 极简学术风 构建器
# 克制、留白、衬线体、极细线条撑起层次
# ─────────────────────────────────────────────

def build_nature_html(items, title="文章标题", subtitle="",
                      keywords=None, abstract="", source="",
                      series_tag="深度解读", qr_path=None,
                      vol="01", year="2025"):
    """
    Nature 极简学术编辑风。
    结构特征：无目录、无数据卡片、大号装饰章节编号、极简 H3 左竖线。
    """
    kws = keywords or []
    serif = "'Georgia','Palatino','Songti SC','SimSun',serif"
    sans = "-apple-system,'Helvetica Neue','PingFang SC',sans-serif"

    # QR 码
    qr_b64 = None
    qr_mime = "image/jpeg"
    if qr_path and os.path.exists(qr_path):
        with open(qr_path, "rb") as f:
            qr_b64 = base64.b64encode(f.read()).decode()
        ext = Path(qr_path).suffix.lower()
        qr_mime = "image/png" if ext == ".png" else "image/jpeg"

    lines = []
    a = lines.append

    a('<!DOCTYPE html><html lang="zh-CN"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0">')
    a(f'<title>{esc(title)}</title></head>')
    a(f'<body style="margin:0;padding:0;background:#fafafa;font-family:{serif};color:#1a1a1a;line-height:1;">')
    a(f'<div style="max-width:640px;margin:0 auto;background:#fff;">')

    # 顶线 — 极细黑线
    a('<div style="height:3px;background:#1a1a1a;"></div>')

    # 页眉
    a(f'<div style="padding:20px 32px 16px;border-bottom:1px solid #e5e5e5;">')
    a(f'  <div style="display:flex;justify-content:space-between;align-items:baseline;">')
    a(f'    <span style="font-size:10px;font-weight:700;color:#1a1a1a;letter-spacing:0.18em;text-transform:uppercase;font-family:{sans};">RNAscript</span>')
    a(f'    <span style="font-size:10px;color:#999;font-family:{sans};letter-spacing:0.05em;">Vol.{vol} · {year}</span>')
    a(f'  </div>')
    a('</div>')

    # 标题区 — 大量留白
    a(f'<div style="padding:36px 32px 0;">')
    a(f'  <span style="display:inline-block;font-size:10px;font-weight:600;color:#666;letter-spacing:0.1em;text-transform:uppercase;margin-bottom:20px;font-family:{sans};">{esc(series_tag)}</span>')
    a(f'  <h1 style="font-size:26px;font-weight:400;color:#1a1a1a;line-height:1.35;margin:0 0 20px;letter-spacing:-0.01em;font-family:{serif};">{esc(title)}</h1>')
    if subtitle:
        a(f'  <p style="font-size:15px;color:#666;line-height:1.6;margin:0 0 24px;font-style:italic;font-family:{serif};">{esc(subtitle)}</p>')
    if source:
        a(f'  <div style="font-size:11px;color:#999;border-left:2px solid #ccc;padding:6px 12px;margin-bottom:28px;font-family:{sans};">{esc(source)}</div>')
    a('</div>')

    # 摘要 — 极简灰底
    if abstract:
        a(f'<div style="margin:0 32px 24px;padding:16px 20px;background:#f7f7f7;border-radius:4px;">')
        a(f'  <div style="font-size:9px;font-weight:700;color:#999;letter-spacing:0.15em;text-transform:uppercase;margin-bottom:8px;font-family:{sans};">ABSTRACT</div>')
        a(f'  <p style="font-size:13px;color:#333;line-height:1.8;margin:0;font-family:{serif};">{esc(abstract)}</p>')
        a('</div>')

    # 关键词 — 下划线文字风格
    if kws:
        a(f'<div style="padding:0 32px 24px;display:flex;flex-wrap:wrap;gap:8px;">')
        for kw in kws:
            a(f'  <span style="font-size:11px;color:#666;padding:3px 0;border-bottom:1px solid #ccc;font-family:{sans};">{esc(kw)}</span>')
        a('</div>')

    # 分隔线
    a('<div style="margin:0 32px 28px;height:1px;background:#e5e5e5;"></div>')

    # 正文
    sec_cnt = [0]
    in_list = False

    for it in items:
        t = it["type"]

        if t == "h1":
            continue  # 已在封面区渲染

        elif t == "h2":
            if in_list:
                a('</ul>')
                in_list = False

            text = it["text"]
            if text.startswith("§"):
                text = text[1:]

            if text in ("参考资料", "参考文献", "References"):
                a(f'<div style="margin:0 32px;">')
                a(f'  <h2 style="font-size:16px;font-weight:400;color:#1a1a1a;margin:0 0 16px;padding-bottom:8px;border-bottom:1px solid #e5e5e5;letter-spacing:0.02em;">{esc(text)}</h2>')
                a('</div>')
            else:
                sec_cnt[0] += 1
                n = sec_cnt[0]
                a(f'<div style="margin:0 32px;margin-top:36px;">')
                a(f'  <div style="display:flex;align-items:baseline;gap:12px;margin-bottom:20px;">')
                a(f'    <span style="font-size:32px;font-weight:300;color:#e0e0e0;line-height:1;font-family:{serif};">{n:02d}</span>')
                a(f'    <h2 style="font-size:19px;font-weight:400;color:#1a1a1a;margin:0;line-height:1.3;letter-spacing:-0.005em;">{esc(text)}</h2>')
                a(f'  </div>')
                a('</div>')

        elif t == "h3":
            if in_list:
                a('</ul>')
                in_list = False
            a(f'<div style="margin:0 32px;margin-top:20px;">')
            a(f'  <h3 style="font-size:14px;font-weight:600;color:#1a1a1a;margin:0 0 12px;padding-left:14px;border-left:2px solid #1a1a1a;font-family:{sans};letter-spacing:0.01em;">{esc(it["text"])}</h3>')
            a('</div>')

        elif t == "figure":
            if in_list:
                a('</ul>')
                in_list = False
            a(f'<div style="margin:0 32px;margin-bottom:14px;">')
            a(f'  <p style="font-size:12px;color:#666;line-height:1.65;margin:0;font-family:{sans};font-style:italic;">{esc(it["text"])}</p>')
            a('</div>')

        elif t == "p":
            if in_list:
                a('</ul>')
                in_list = False
            a(f'<div style="margin:0 32px;">')
            a(f'  <p style="font-size:15px;color:#2a2a2a;line-height:1.9;margin:0 0 14px;text-align:justify;font-family:{serif};">{esc(it["text"])}</p>')
            a('</div>')

        elif t == "li":
            if not in_list:
                a(f'<ul style="margin:0 32px 14px;padding-left:20px;">')
                in_list = True
            a(f'    <li style="font-size:14px;color:#2a2a2a;line-height:1.8;margin-bottom:6px;font-family:{serif};">{esc(it["text"])}</li>')

        elif t == "img":
            if in_list:
                a('</ul>')
                in_list = False
            d = it["data"]
            src = f'data:{d["mime"]};base64,{d["b64"]}'
            a(f'<div style="margin:20px 32px;">')
            a(f'  <img src="{src}" style="width:100%;display:block;border-radius:2px;" alt="">')
            a('</div>')

    if in_list:
        a('</ul>')

    # 底部
    a('<div style="margin:0 32px 20px;height:1px;background:#e5e5e5;"></div>')
    a(f'<div style="padding:28px 32px;text-align:center;">')
    a(f'  <p style="font-size:12px;color:#999;margin:0 0 16px;font-family:{sans};letter-spacing:0.05em;">FOLLOW US</p>')
    if qr_b64:
        a(f'  <img src="data:{qr_mime};base64,{qr_b64}" style="width:140px;height:140px;display:block;margin:0 auto 12px;border-radius:2px;" alt="">')
    else:
        a(f'  <div style="width:140px;height:140px;border:2px solid #e0e0e0;border-radius:2px;display:flex;align-items:center;justify-content:center;margin:0 auto 12px;">')
        a(f'    <span style="font-size:11px;color:#999;text-align:center;font-family:{sans};">扫码关注<br>公众号</span>')
        a(f'  </div>')
    a(f'  <p style="font-size:10px;color:#bbb;margin:0;font-family:{sans};letter-spacing:0.08em;">RNAscript · 信使引擎</p>')
    a('</div>')
    a('<div style="height:3px;background:#1a1a1a;"></div>')
    a('</div></body></html>')

    return "\n".join(lines)


# ─────────────────────────────────────────────
# Cell 期刊封面风 构建器
# 色块分区、层次丰富、大胆视觉对比
# ─────────────────────────────────────────────

def build_cell_html(items, title="文章标题", subtitle="",
                    keywords=None, abstract="", source="",
                    series_tag="深度解读", qr_path=None,
                    vol="01", year="2025"):
    """
    Cell 期刊封面风。
    结构特征：无目录、无数据卡片、深蓝章节头色块（SECTION NN）、蓝色圆点 H3。
    """
    kws = keywords or []
    sans = "-apple-system,'Helvetica Neue','PingFang SC',sans-serif"
    serif = "Georgia,'Songti SC',serif"

    # QR 码
    qr_b64 = None
    qr_mime = "image/jpeg"
    if qr_path and os.path.exists(qr_path):
        with open(qr_path, "rb") as f:
            qr_b64 = base64.b64encode(f.read()).decode()
        ext = Path(qr_path).suffix.lower()
        qr_mime = "image/png" if ext == ".png" else "image/jpeg"

    lines = []
    a = lines.append

    a('<!DOCTYPE html><html lang="zh-CN"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0">')
    a(f'<title>{esc(title)}</title></head>')
    a(f'<body style="margin:0;padding:0;background:#edf2f7;font-family:{sans};color:#0f172a;line-height:1;">')
    a(f'<div style="max-width:640px;margin:0 auto;background:#fff;box-shadow:0 0 40px rgba(0,0,0,0.06);">')

    # 顶部装饰条
    a('<div style="height:6px;background:#1e3a5f;"></div>')

    # Header bar
    a(f'<div style="padding:16px 32px;display:flex;justify-content:space-between;align-items:center;border-bottom:2px solid #e2e8f0;">')
    a(f'  <span style="font-size:11px;font-weight:800;color:#1e3a5f;letter-spacing:0.15em;">RNAscript</span>')
    a(f'  <span style="font-size:11px;color:#94a3b8;">Vol.{vol} · {year}</span>')
    a('</div>')

    # 标题区
    a(f'<div style="padding:32px 32px 0;">')
    a(f'  <div style="display:flex;align-items:center;gap:8px;margin-bottom:16px;">')
    a(f'    <div style="width:4px;height:20px;background:#2563eb;border-radius:2px;"></div>')
    a(f'    <span style="font-size:10px;font-weight:700;color:#2563eb;letter-spacing:0.12em;text-transform:uppercase;">{esc(series_tag)}</span>')
    a(f'  </div>')
    a(f'  <h1 style="font-size:23px;font-weight:800;color:#0f172a;line-height:1.35;margin:0 0 14px;letter-spacing:-0.01em;">{esc(title)}</h1>')
    if subtitle:
        a(f'  <p style="font-size:14px;color:#64748b;line-height:1.6;margin:0 0 20px;">{esc(subtitle)}</p>')
    if source:
        a(f'  <div style="display:inline-block;font-size:11px;color:#64748b;background:#f1f5f9;padding:6px 12px;border-radius:4px;margin-bottom:24px;">{esc(source)}</div>')
    a('</div>')

    # 摘要
    if abstract:
        a(f'<div style="margin:20px 32px;padding:18px 20px;background:#f8fafc;border:1px solid #e2e8f0;border-radius:8px;">')
        a(f'  <div style="font-size:9px;font-weight:800;color:#2563eb;letter-spacing:0.15em;text-transform:uppercase;margin-bottom:8px;">ABSTRACT</div>')
        a(f'  <p style="font-size:13px;color:#334155;line-height:1.8;margin:0;font-family:{serif};">{esc(abstract)}</p>')
        a('</div>')

    # 关键词
    if kws:
        a(f'<div style="padding:0 32px 20px;display:flex;flex-wrap:wrap;gap:6px;">')
        for kw in kws:
            a(f'  <span style="font-size:10px;padding:4px 10px;background:#eff6ff;color:#1e40af;border-radius:20px;font-weight:600;border:1px solid #bfdbfe;">{esc(kw)}</span>')
        a('</div>')

    # 正文
    sec_cnt = [0]
    in_list = False

    for it in items:
        t = it["type"]

        if t == "h1":
            continue

        elif t == "h2":
            if in_list:
                a('</ul>')
                in_list = False

            text = it["text"]
            if text.startswith("§"):
                text = text[1:]

            if text in ("参考资料", "参考文献", "References"):
                a(f'<div style="padding:8px 32px;">')
                a(f'  <div style="width:40px;height:2px;background:#2563eb;border-radius:1px;margin-bottom:12px;"></div>')
                a(f'  <h2 style="font-size:15px;font-weight:800;color:#0f172a;margin:0 0 12px;">{esc(text)}</h2>')
                a('</div>')
            else:
                sec_cnt[0] += 1
                n = sec_cnt[0]
                a(f'<div style="margin-top:36px;padding:0 32px;">')
                a(f'  <div style="background:#1e3a5f;margin:0 -32px;padding:16px 32px;margin-bottom:20px;border-radius:0 12px 0 0;">')
                a(f'    <div style="display:flex;align-items:center;gap:14px;">')
                a(f'      <div style="font-size:13px;font-weight:800;color:#93c5fd;letter-spacing:0.05em;">SECTION {n:02d}</div>')
                a(f'      <div style="flex:1;height:1px;background:rgba(255,255,255,0.15);"></div>')
                a(f'    </div>')
                a(f'    <h2 style="font-size:18px;font-weight:700;color:#fff;margin:8px 0 0;line-height:1.3;">{esc(text)}</h2>')
                a(f'  </div>')
                a('</div>')

        elif t == "h3":
            if in_list:
                a('</ul>')
                in_list = False
            a(f'<div style="padding:0 32px;margin-top:20px;">')
            a(f'  <div style="display:flex;align-items:center;gap:8px;">')
            a(f'    <div style="width:8px;height:8px;background:#2563eb;border-radius:50%;flex-shrink:0;"></div>')
            a(f'    <h3 style="font-size:14px;font-weight:700;color:#1e3a5f;margin:0;">{esc(it["text"])}</h3>')
            a(f'  </div>')
            a('</div>')

        elif t == "figure":
            if in_list:
                a('</ul>')
                in_list = False
            a(f'<div style="padding:0 32px;margin-bottom:14px;">')
            a(f'  <div style="background:#f1f5f9;border-left:3px solid #93c5fd;padding:10px 14px;border-radius:0 4px 4px 0;">')
            a(f'    <p style="font-size:12px;color:#64748b;line-height:1.65;margin:0;">{esc(it["text"])}</p>')
            a(f'  </div>')
            a('</div>')

        elif t == "p":
            if in_list:
                a('</ul>')
                in_list = False
            a(f'<div style="padding:0 32px;">')
            a(f'  <p style="font-size:14.5px;color:#334155;line-height:1.85;margin:0 0 13px;text-align:justify;font-family:{serif};">{esc(it["text"])}</p>')
            a('</div>')

        elif t == "li":
            if not in_list:
                a(f'<ul style="margin:0 32px 13px;padding-left:20px;">')
                in_list = True
            a(f'    <li style="font-size:14px;color:#334155;line-height:1.85;margin-bottom:6px;font-family:{serif};">{esc(it["text"])}</li>')

        elif t == "img":
            if in_list:
                a('</ul>')
                in_list = False
            d = it["data"]
            src = f'data:{d["mime"]};base64,{d["b64"]}'
            a(f'<div style="padding:0 32px;margin:16px 0;">')
            a(f'  <div style="border-radius:8px;overflow:hidden;box-shadow:0 2px 8px rgba(30,58,95,0.08);">')
            a(f'    <img src="{src}" style="width:100%;display:block;" alt="">')
            a(f'  </div>')
            a('</div>')

    if in_list:
        a('</ul>')

    # 底部 — 深蓝 Footer
    a('<div style="margin-top:32px;background:#1e3a5f;padding:28px 32px;text-align:center;border-radius:12px 12px 0 0;">')
    a(f'  <p style="font-size:12px;color:#93c5fd;margin:0 0 16px;font-weight:600;letter-spacing:0.08em;">FOLLOW US</p>')
    if qr_b64:
        a(f'  <img src="data:{qr_mime};base64,{qr_b64}" style="width:140px;height:140px;display:block;margin:0 auto 12px;border-radius:8px;border:2px solid rgba(255,255,255,0.15);" alt="">')
    else:
        a(f'  <div style="width:140px;height:140px;border:2px solid rgba(255,255,255,0.2);border-radius:8px;display:flex;align-items:center;justify-content:center;margin:0 auto 12px;">')
        a(f'    <span style="font-size:11px;color:#93c5fd;text-align:center;">扫码关注<br>公众号</span>')
        a(f'  </div>')
    a(f'  <p style="font-size:10px;color:#64748b;margin:0;letter-spacing:0.06em;">RNAscript · 信使引擎</p>')
    a('</div>')

    a('</div></body></html>')

    return "\n".join(lines)


# ─────────────────────────────────────────────
# 命令行入口
# ─────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="将 .docx 转化为微信公众号兼容全内联 HTML"
    )
    parser.add_argument("--input", "-i", required=True, help=".docx 文件路径")
    parser.add_argument("--theme", "-t", choices=["orange", "blue", "nature", "cell"], default="orange",
                        help="主题：orange（橙皮书）、blue（学术深蓝）、nature（极简学术）、cell（期刊封面）")
    parser.add_argument("--output", "-o", required=True, help="输出 HTML 路径")
    parser.add_argument("--qr", help="个人二维码图片路径（可选）")
    parser.add_argument("--title", help="文章标题（默认从 H1 提取）")
    parser.add_argument("--subtitle", default="", help="导语副标题")
    parser.add_argument("--abstract", default="", help="摘要文字")
    parser.add_argument("--keywords", default="", help="关键词，逗号分隔")
    parser.add_argument("--source", default="", help="文献来源")
    parser.add_argument("--series-tag", default="深度解读", help="系列标签（如：博士论文深度解读）")
    parser.add_argument("--vol", default="01", help="期号")
    parser.add_argument("--year", default="2025", help="年份")

    args = parser.parse_args()

    if not os.path.exists(args.input):
        print(f"错误：找不到文件 {args.input}")
        sys.exit(1)

    print(f"📄 读取文档：{args.input}")
    items = parse_paragraphs(args.input)

    # 后处理：智能章节嗅探（无 Word 标题样式的 § 段落 → h2）
    items = smart_sniff_headings(items)

    # 从 H1 提取标题
    title = args.title
    if not title:
        for it in items:
            if it["type"] == "h1":
                title = it["text"]
                break
    if not title:
        title = Path(args.input).stem

    kws = [k.strip() for k in args.keywords.split(",") if k.strip()] if args.keywords else []

    print(f"🎨 使用主题：{THEMES[args.theme]['name']}")
    print(f"📊 解析段落：{len(items)} 个（含图片：{sum(1 for i in items if i['type']=='img')} 张）")

    # 根据 theme 选择构建器
    if args.theme in ("orange", "blue"):
        html = build_html(
            items,
            theme_name=args.theme,
            title=title,
            subtitle=args.subtitle,
            keywords=kws,
            abstract=args.abstract,
            source=args.source,
            series_tag=args.series_tag,
            qr_path=args.qr,
            vol=args.vol,
            year=args.year,
        )
    else:
        # nature / cell 使用独立构建器
        builder = {"nature": build_nature_html, "cell": build_cell_html}[args.theme]
        html = builder(
            items,
            title=title,
            subtitle=args.subtitle,
            keywords=kws,
            abstract=args.abstract,
            source=args.source,
            series_tag=args.series_tag,
            qr_path=args.qr,
            vol=args.vol,
            year=args.year,
        )

    # 写入文件
    out_path = Path(args.output)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(html, encoding="utf-8")

    size_kb = out_path.stat().st_size / 1024
    print(f"✅ 生成完成：{out_path}（{size_kb:.0f} KB）")
    print(f"")
    print(f"使用方式：")
    print(f"  1. 用浏览器打开 {out_path.name}")
    print(f"  2. 全选（Ctrl+A）→ 复制（Ctrl+C）")
    print("  3. 粘贴到微信公众号【新建图文】正文区")


if __name__ == "__main__":
    main()
