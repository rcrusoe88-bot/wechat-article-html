# wechat-article-html

将 Word 文档（`.docx`）转化为微信公众号兼容的**全内联式 HTML**，可直接在浏览器打开后复制粘贴至公众号编辑器。

---

## 功能特点

- **全内联样式**：每个元素的样式都写在 `style=""` 属性里，不依赖 `<style>` 块或外部 CSS，完全符合微信编辑器的渲染规则
- **图片自包含**：所有图片以 `data:image/...;base64` 内嵌，无需外链
- **4 款主题**：覆盖技术报告、学术综述、期刊解读等常见场景
- **智能标题嗅探**：自动识别无 Heading 样式的 docx，补偿章节层级

---

## 主题一览

| 主题 | 风格 | 适合场景 |
|------|------|----------|
| `--theme orange` | 橙皮书·技术白皮书 | 技术解读、研究报告、工艺分析 |
| `--theme blue` | 学术深蓝·期刊风 | 综述、机制讲解、方法论 |
| `--theme nature` | Nature·极简学术 | 文献深度解读、严肃长篇综述 |
| `--theme cell` | Cell·期刊封面风 | 临床数据解读、产品管线分析 |

---

## 快速开始

### 依赖

```bash
pip install python-docx
```

### 基本用法

```bash
python scripts/convert.py \
  --input article.docx \
  --theme orange \
  --output output.html
```

### 完整参数

```bash
python scripts/convert.py \
  --input article.docx \
  --theme nature \
  --output output.html \
  --title "文章标题" \
  --subtitle "导语副标题" \
  --abstract "摘要内容" \
  --keywords "关键词1,关键词2,关键词3" \
  --source "文献来源/署名" \
  --series-tag "系列标签" \
  --year 2026 \
  --vol 01 \
  --qr qrcode.jpg
```

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `--input` | 输入的 .docx 文件路径 | 必填 |
| `--theme` | 主题：`orange` / `blue` / `nature` / `cell` | `orange` |
| `--output` | 输出的 .html 文件路径 | 必填 |
| `--title` | 文章标题（不传则从 H1 自动提取） | 文件名 |
| `--subtitle` | 导语/副标题 | 空 |
| `--abstract` | 摘要文字 | 空 |
| `--keywords` | 逗号分隔的关键词 | 空 |
| `--source` | 文献来源/署名 | 空 |
| `--series-tag` | 系列标签 | "深度解读" |
| `--year` / `--vol` | 年份和期号 | 2025 / 01 |
| `--qr` | 二维码图片路径（可选） | 空 |

---

## 使用方式

1. 运行脚本，生成 `.html` 文件
2. 用浏览器打开生成的文件
3. 全选（`Ctrl+A`）→ 复制（`Ctrl+C`）
4. 在微信公众号「新建图文」正文区粘贴（`Ctrl+V`）
5. 在编辑器内调整标题、封面图后发布

> 注意：复制浏览器**渲染出的页面内容**，而不是 HTML 源码。

---

## Word 文档规范

脚本识别以下 Word 段落样式：

| Word 样式 | 输出 |
|-----------|------|
| Heading 1 | 文章大标题 |
| Heading 2 | 章节标题 |
| Heading 3 | 子节标题 |
| Normal（含图） | base64 图片块 |
| Normal（纯文字） | 正文段落 |
| List Paragraph / 含 • | 列表项 |

如原文未使用 Word Heading 样式，脚本会自动识别 `§01`、`第一章` 等格式并提升为章节标题。

---

## 文件结构

```
wechat-article-html/
├── scripts/
│   └── convert.py          # 主转换脚本
├── references/
│   ├── theme_orange_book.md
│   ├── theme_academic_blue.md
│   ├── theme_nature.md
│   └── theme_cell.md
├── SKILL.md                # Claude Code skill 配置
└── README.md
```

---

## License

MIT
