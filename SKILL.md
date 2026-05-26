---
name: wechat-article-html
description: >
  将上传的 Word 文档（.docx）转化为微信公众号兼容的全内联式 HTML 文件。提取文档正文结构与内嵌图片，生成自包含的 HTML，可直接在浏览器打开后复制粘贴至公众号编辑器。
  提供四种主题风格：橙皮书（技术白皮书暖色调）、学术深蓝（学术期刊冷色调）、Nature（极简学术风）、Cell（期刊封面风）。
  触发场景：用户上传 .docx 并提到"公众号"、"微信"、"HTML"、"排版"、"橙皮书"、"深蓝"、"nature"、"cell"、"wechat html"时，必须调用本skill。
---

# WeChat Article HTML Skill

将 Word 文档转化为微信公众号兼容 HTML 的端到端工作流。

---

## 微信 HTML 的核心约束

微信公众号编辑器会**完整剥离** `<style>` 标签及 `<head>` 内的所有 CSS。
**只有元素上直接写的 `style=""` 属性才能保留。**

因此生成的 HTML 必须满足：
- ✅ 每个元素的样式都写在 `style=""` 属性里
- ✅ 图片以 `data:image/...;base64,...` 内嵌，不依赖外链
- ❌ 绝不使用 `<style>` 块、CSS class、外部 CSS 文件

---

## 完整工作流

### Step 1：确认输入文件

检查 uploads 目录是否有 `.docx` 文件：
```bash
ls /sessions/*/mnt/uploads/*.docx 2>/dev/null || ls /sessions/*/mnt/uploads/
```

### Step 2：让用户选择主题

向用户展示四个选项，等待选择后再继续：

**主题A：橙皮书 · 技术白皮书风** `--theme orange`
> 底色 `#fffbf0`，橙红强调色 `#e85d04`，衬线感标题，技术深度感强
> 特点：目录、数据统计卡片、渐变分隔线
> 适合：技术解读、研究报告、工艺分析、深度科普

**主题B：学术深蓝 · 期刊风** `--theme blue`
> 底色 `#f8fafd`，深海军蓝 `#1e3a5f`，清朗学术气质
> 特点：目录、数据统计卡片、双色调顶部色带
> 适合：综述类、机制讲解、基础科学、方法论介绍

**主题C：Nature · 极简学术风** `--theme nature`
> 底色 `#fafafa`，黑白灰三色，衬线体主导，极细线条
> 特点：无目录、无数据卡片、大号装饰章节编号（01/02…）、下划线关键词
> 适合：文献深度解读、数据分析报告、严肃长篇综述

**主题D：Cell · 期刊封面风** `--theme cell`
> 底色 `#edf2f7`，深蓝章节头色块，白色正文区域，大胆视觉对比
> 特点：无目录、无数据卡片、深蓝 SECTION NN 色块标题、蓝色圆点 H3、阴影图片
> 适合：临床数据解读（AACR/ESMO）、产品管线分析、行业格局报告

### Step 3：查找用户个人二维码（可选）

检查 workspace 是否存在二维码图片：
```bash
find /sessions/*/mnt/CC_公众号内容创作/ -name "*.jpg" -o -name "*.png" | grep -i "二维码\|qr\|qrcode" 2>/dev/null
```

如有则嵌入，如无则生成对应主题的占位框。

### Step 4：运行转换脚本

```bash
python3 /path/to/skill/scripts/convert.py \
  --input /path/to/uploaded.docx \
  --theme orange  # 或 blue / nature / cell
  --output /sessions/*/mnt/CC_公众号内容创作/[文章标题]_[主题].html \
  --qr /path/to/qr.jpg  # 可选
```

**脚本实际路径**：本 SKILL.md 所在目录的 `scripts/convert.py`

完整示例（含可选元数据）：
```bash
python3 /path/to/skill/scripts/convert.py \
  --input /path/to/article.docx \
  --theme nature \
  --output /path/to/output.html \
  --title "文章标题" \
  --subtitle "导语副标题" \
  --abstract "摘要内容" \
  --keywords "关键词1,关键词2,关键词3" \
  --source "文献来源/署名" \
  --series-tag "系列标签" \
  --year 2026 \
  --vol 01 \
  --qr /path/to/qr.jpg  # 可选
```

### Step 4a：元数据注入说明

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `--title` | 文章标题（不传则从 H1 自动提取） | 文件名 |
| `--subtitle` | 导语/副标题 | 空 |
| `--abstract` | 摘要文字（显示在摘要框） | 空 |
| `--keywords` | 逗号分隔的关键词 | 空 |
| `--source` | 文献来源/署名（显示在标题区） | 空 |
| `--series-tag` | 系列标签（如"博士论文深度解读"） | "深度解读" |
| `--year` / `--vol` | 年份和期号 | 2025 / 01 |

### Step 5：质量检查

```bash
# 检查文件大小（含图应在 200KB-3MB 之间）
ls -lh output.html

# 确认无外部资源引用
grep -c "http[s]://" output.html  # 应为 0

# 确认无 <style> 标签
grep -c "<style" output.html  # 应为 0

# 确认图片已内嵌
grep -c "base64" output.html  # 应 > 0（如原文有图）
```

### Step 6：输出交付

文件保存到用户 workspace 后，提供链接和使用说明：

```
✅ 转换完成！

使用方式：
1. 用浏览器打开生成的 .html 文件
2. 全选（Ctrl+A）→ 复制（Ctrl+C）
3. 在微信公众号"新建图文"正文区粘贴（Ctrl+V）
4. 在编辑器内调整标题、封面图后发布

注意：复制浏览器渲染出的页面内容，而不是 HTML 源码。
```

---

## 文档结构解析规则

### 基础规则（Word 样式匹配）

`convert.py` 识别以下 Word 段落样式：

| Word 样式 | HTML 输出 |
|-----------|-----------|
| Heading 1 | `<h1>` 大标题（文章头部） |
| Heading 2 | `<h2>` 章节标题（各主题渲染方式不同） |
| Heading 3 | `<h3>` 子节标题 |
| Normal（含图） | base64 `<img>` 图片块 |
| Normal（纯文字） | `<p>` 正文段落 |
| List Paragraph / 含 • | `<li>` 列表项 |

### 各主题 H2 渲染差异

| 主题 | H2 渲染方式 |
|------|-------------|
| orange | §N 编号 + 橙色下划线 |
| blue | §N 编号 + 蓝色下划线 |
| nature | 大号装饰编号（01/02…）+ 轻字重标题 |
| cell | 深蓝色块 "SECTION NN" + 白色标题文字 |

### 智能章节嗅探（标题样式补偿）

如果原文没有使用 Word 的 Heading 样式（常见于直接从纯文本粘贴的 docx），`smart_sniff_headings()` 后处理会自动检测以下三种模式，**将普通段落提升为 h2 章节标题**：

| 模式 | 原文示例 | 检测逻辑 | 渲染效果 |
|------|----------|----------|----------|
| A：独立编号 + 标题 | `§01` + `AMBITION...`（两段） | 识别 `§\d+` 独立段落，与下一段合并 | 合并后的标题文字，按主题风格渲染 |
| B：内联节标题 | `§行业惯性批判` | 识别 `§\w` 开头 | 同上 |
| C：中文章节 | `第一章`、`第2节` | 识别 `第X章/节/部/篇` | 同上 |

**提示**：这是对无样式文档的补偿机制。如果希望精确控制标题层级，最好在 Word 中直接应用 Heading 2 样式。

---

## 图片提取方式

所有图片通过文档关系树提取（顺序稳定）：

```python
from docx import Document
import base64

doc = Document(docx_path)
images = []
for rel in doc.part.rels.values():
    if "image" in rel.reltype:
        blob = rel.target_part.blob
        b64 = base64.b64encode(blob).decode()
        ct = rel.target_part.content_type  # e.g. image/jpeg
        ext = ct.split('/')[-1]
        images.append({'b64': b64, 'ext': ext, 'mime': ct})
```

图片按文档 XML 中出现的段落顺序依次插入章节末尾。

---

## 主题参考文件

- `references/theme_orange_book.md` — 橙皮书完整内联样式规范
- `references/theme_academic_blue.md` — 学术深蓝完整内联样式规范
- `references/theme_nature.md` — Nature 极简学术完整内联样式规范
- `references/theme_cell.md` — Cell 期刊封面完整内联样式规范

如需自定义颜色/字号，读取对应参考文件后修改 `convert.py`。
