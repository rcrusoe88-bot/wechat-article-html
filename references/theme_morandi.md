# 莫兰迪淡雅主题 · 完整内联样式规范

## 设计系统

| 变量 | 值 | 用途 |
|------|----|------|
| `bg_page` | `#ede8e1` | 页面外背景 |
| `bg_card` | `#faf7f4` | 主容器底色 |
| `accent` | `#c9847a` | 主强调色（莫兰迪玫瑰，标题线、徽标、编号） |
| `accent2` | `#7a9e8e` | 辅强调色（矿绿，H3 标题、左边线） |
| `accent_light` | `#e8d4cf` | 浅调边框色 |
| `bg_callout` | `#faf0ee` | 标注框底色 |
| `bg_stat` | `#f5f0ec` | 数据卡底色 |
| `bg_figure` | `#f0ebe6` | 图片块底色 |
| `text_main` | `#3d2c2c` | 正文主色 |
| `text_body` | `#4a3a38` | 正文段落色 |
| `text_meta` | `#9a7a78` | 导语/副标题色 |
| `text_muted` | `#b0998f` | 次要说明文字 |
| `text_gray` | `#b0998f` | 期号/次要信息 |
| `text_toc` | `#3d2c2c` | 目录条目色 |
| `text_keyword` | `#c9847a` | 关键词标签文字 |

---

## 页面外壳

```html
<!-- 页面 body -->
<body style="margin:0;padding:0;background:#ede8e1;font-family:-apple-system,'PingFang SC','Helvetica Neue',Arial,sans-serif;color:#3d2c2c;line-height:1.85;">

<!-- 主容器 -->
<div style="max-width:680px;margin:0 auto;background:#faf7f4;">

<!-- 顶部色带（双层：玫瑰 + 矿绿） -->
<div style="background:#c9847a;height:5px;"></div>
<div style="background:#b3cfc5;height:3px;"></div>
```

---

## 页眉

```html
<div style="padding:14px 28px 12px;display:flex;justify-content:space-between;align-items:center;border-bottom:1px solid #e8ddd8;">
  <span style="font-size:11px;font-weight:700;color:#c9847a;letter-spacing:0.12em;">RNAscript · 前沿解读</span>
  <span style="font-size:11px;color:#b0998f;">Vol.XX · 202X</span>
</div>
```

---

## 封面区域

```html
<div style="padding:28px 28px 0;">
  <!-- 系列标签（胶囊圆角） -->
  <span style="display:inline-block;background:#c9847a;color:#fff;font-size:11px;font-weight:700;letter-spacing:0.08em;padding:4px 14px;border-radius:20px;margin-bottom:16px;">深度解读</span>

  <!-- H1 大标题 -->
  <h1 style="font-size:22px;font-weight:800;color:#3d2c2c;line-height:1.4;margin:0 0 14px;padding-bottom:16px;border-bottom:3px solid #c9847a;">
    [文章主标题]
  </h1>

  <!-- 导语副标题 -->
  <p style="font-size:14px;color:#9a7a78;line-height:1.65;margin:0 0 14px;font-style:italic;">
    [导语说明文字]
  </p>

  <!-- 文献来源 -->
  <div style="font-size:11px;color:#b0998f;background:#f2ece7;border-left:3px solid #c9847a;padding:8px 12px;border-radius:0 6px 6px 0;margin-bottom:24px;">
    文献来源：[引用信息]
  </div>
</div>
```

---

## 数据统计卡片行

```html
<div style="display:flex;gap:12px;margin:0 28px 24px;">
  <div style="flex:1;background:#f5f0ec;border:1px solid #ddd0c8;border-radius:12px;padding:14px 10px;text-align:center;">
    <div style="font-size:24px;font-weight:800;color:#c9847a;line-height:1;margin-bottom:4px;">42%</div>
    <div style="font-size:10px;color:#9a7a78;line-height:1.4;">指标说明<br>第二行</div>
  </div>
  <!-- 重复 2-3 个 -->
</div>
```

---

## 摘要框

```html
<div style="margin:0 28px 20px;background:#f5f0ec;border:1px solid #ddd0c8;border-radius:12px;padding:16px 20px;">
  <div style="font-size:10px;font-weight:700;color:#c9847a;letter-spacing:0.1em;text-transform:uppercase;margin-bottom:8px;">摘要 Abstract</div>
  <p style="font-size:13px;color:#4a3a38;line-height:1.8;margin:0;">[摘要内容]</p>
</div>
```

---

## 关键词标签（胶囊圆角）

```html
<div style="padding:0 28px 20px;display:flex;flex-wrap:wrap;gap:6px;">
  <span style="font-size:11px;padding:4px 12px;background:#faf0ee;border:1px solid #c9847a;color:#c9847a;border-radius:20px;">关键词</span>
</div>
```

---

## 目录

```html
<div style="margin:0 28px 28px;border:1px solid #ddd0c8;border-radius:12px;overflow:hidden;">
  <!-- 目录头 -->
  <div style="background:#c9847a;color:#fff;font-size:11px;font-weight:700;letter-spacing:0.08em;padding:10px 18px;">目录 Contents</div>

  <!-- 主章节条目 -->
  <div style="display:flex;justify-content:space-between;align-items:center;padding:9px 18px;border-bottom:1px solid #ece4e0;font-size:13px;color:#3d2c2c;">
    <span>一、章节名称</span>
    <span style="font-size:11px;font-weight:700;color:#c9847a;">§1</span>
  </div>

  <!-- 偶数行交替底色 -->
  <div style="display:flex;justify-content:space-between;align-items:center;padding:9px 18px;border-bottom:1px solid #ece4e0;font-size:13px;color:#3d2c2c;background:#fdf8f6;">
    <span>二、章节名称</span>
    <span style="font-size:11px;font-weight:700;color:#c9847a;">§2</span>
  </div>
</div>
```

---

## 章节分隔线

```html
<div style="height:2px;background:linear-gradient(to right,#c9847a 30%,#e8d4cf 100%);margin:0 28px 28px;border-radius:1px;"></div>
```

---

## H2 章节标题

```html
<h2 style="font-size:18px;font-weight:800;color:#3d2c2c;line-height:1.4;margin:0 0 16px;padding-bottom:10px;border-bottom:2px solid #c9847a;">
  <span style="color:#c9847a;font-size:13px;font-weight:700;display:block;margin-bottom:4px;letter-spacing:0.05em;">§ N 节号</span>
  章节正文标题
</h2>
```

---

## H3 子节标题

> 使用矿绿色（`#7a9e8e`）区分层级，与 H2 玫瑰色形成莫兰迪色彩对比。

```html
<h3 style="font-size:15px;font-weight:700;color:#7a9e8e;margin:0 0 12px;padding-left:12px;border-left:3px solid #7a9e8e;">
  子节标题
</h3>
```

---

## 正文段落

```html
<p style="font-size:15px;color:#4a3a38;line-height:1.95;margin:0 0 16px;text-align:justify;">
  段落内容
</p>
```

---

## 标注/引用框（Callout）

```html
<div style="background:#faf0ee;border:1px solid #ddd0c8;border-left:4px solid #c9847a;border-radius:0 12px 12px 0;padding:14px 18px;margin:18px 0;">
  <div style="font-size:11px;font-weight:700;color:#c9847a;text-transform:uppercase;letter-spacing:0.08em;margin-bottom:6px;">编者按</div>
  <div style="font-size:14px;color:#6a4a48;line-height:1.75;">[标注内容，可含 <strong style="color:#c9847a;font-weight:800;">加粗强调</strong>]</div>
</div>
```

---

## 图片块

```html
<div style="background:#f0ebe6;border-radius:12px;padding:12px;margin:20px 0;">
  <img src="data:image/jpeg;base64,[BASE64]" style="width:100%;display:block;border-radius:8px;" alt="图N">
  <p style="font-size:11px;color:#9a7a78;text-align:center;margin:8px 0 0;line-height:1.4;">图N · [图注文字]</p>
</div>
```

---

## 列表

```html
<ul style="margin:0 0 16px;padding-left:20px;">
  <li style="font-size:14px;color:#4a3a38;line-height:1.88;margin-bottom:6px;">列表项内容</li>
</ul>
```

---

## 底部色带

```html
<!-- 底部色带（双层，与顶部对称） -->
<div style="background:#b3cfc5;height:3px;margin-top:8px;"></div>
<div style="background:#c9847a;height:5px;"></div>
```

---

## 二维码 / 关注区

```html
<div style="padding:24px 28px;text-align:center;background:#f5f0ec;border-top:1px solid #ddd0c8;">
  <p style="font-size:13px;color:#9a7a78;margin:0 0 12px;">扫码关注 · 获取最新内容</p>
  <img src="data:image/jpeg;base64,[QR_BASE64]"
       style="width:160px;height:160px;border:3px solid #c9847a;border-radius:12px;display:block;margin:0 auto 12px;"
       alt="公众号二维码">
  <p style="font-size:11px;color:#b0998f;margin:0;">RNAscript · 前沿解读</p>
</div>
```

若无二维码图片，使用占位框：
```html
<div style="width:160px;height:160px;border:3px dashed #c9847a;border-radius:12px;display:flex;align-items:center;justify-content:center;margin:0 auto 12px;background:#faf0ee;">
  <span style="font-size:11px;color:#c9847a;text-align:center;padding:8px;">扫码关注<br>公众号</span>
</div>
```

---

## THEME 字典（Python，可直接复制进 convert.py 的 THEMES）

```python
"morandi": {
    "name": "莫兰迪淡雅",
    "label": "前沿解读",
    "body": "margin:0;padding:0;background:#ede8e1;font-family:-apple-system,'PingFang SC','Helvetica Neue',Arial,sans-serif;color:#3d2c2c;line-height:1.85;",
    "container": "max-width:680px;margin:0 auto;background:#faf7f4;",
    "top_band": "background:#c9847a;height:5px;",
    "top_band2": "background:#b3cfc5;height:3px;",
    "bottom_band1": "background:#b3cfc5;height:3px;margin-top:8px;",
    "bottom_band2": "background:#c9847a;height:5px;",
    "header_wrap": "padding:14px 28px 12px;display:flex;justify-content:space-between;align-items:center;border-bottom:1px solid #e8ddd8;",
    "header_label": "font-size:11px;font-weight:700;color:#c9847a;letter-spacing:0.12em;",
    "header_vol": "font-size:11px;color:#b0998f;",
    "series_badge": "display:inline-block;background:#c9847a;color:#fff;font-size:11px;font-weight:700;letter-spacing:0.08em;padding:4px 14px;border-radius:20px;margin-bottom:16px;",
    "h1": "font-size:22px;font-weight:800;color:#3d2c2c;line-height:1.4;margin:0 0 14px;padding-bottom:16px;border-bottom:3px solid #c9847a;",
    "subtitle": "font-size:14px;color:#9a7a78;line-height:1.65;margin:0 0 14px;font-style:italic;",
    "source_box": "font-size:11px;color:#b0998f;background:#f2ece7;border-left:3px solid #c9847a;padding:8px 12px;border-radius:0 6px 6px 0;margin-bottom:24px;",
    "stat_row": "display:flex;gap:12px;margin:0 28px 24px;",
    "stat_card": "flex:1;background:#f5f0ec;border:1px solid #ddd0c8;border-radius:12px;padding:14px 10px;text-align:center;",
    "stat_num": "font-size:24px;font-weight:800;color:#c9847a;line-height:1;margin-bottom:4px;",
    "stat_label": "font-size:10px;color:#9a7a78;line-height:1.4;",
    "abstract_box": "margin:0 28px 20px;background:#f5f0ec;border:1px solid #ddd0c8;border-radius:12px;padding:16px 20px;",
    "abstract_label": "font-size:10px;font-weight:700;color:#c9847a;letter-spacing:0.1em;text-transform:uppercase;margin-bottom:8px;",
    "abstract_label_text": "摘要 Abstract",
    "abstract_text": "font-size:13px;color:#4a3a38;line-height:1.8;margin:0;",
    "keyword_wrap": "padding:0 28px 20px;display:flex;flex-wrap:wrap;gap:6px;",
    "keyword": "font-size:11px;padding:4px 12px;background:#faf0ee;border:1px solid #c9847a;color:#c9847a;border-radius:20px;",
    "toc_wrap": "margin:0 28px 28px;border:1px solid #ddd0c8;border-radius:12px;overflow:hidden;",
    "toc_header": "background:#c9847a;color:#fff;font-size:11px;font-weight:700;letter-spacing:0.08em;padding:10px 18px;",
    "toc_header_text": "目录 Contents",
    "toc_row": "display:flex;justify-content:space-between;align-items:center;padding:9px 18px;border-bottom:1px solid #ece4e0;font-size:13px;color:#3d2c2c;",
    "toc_row_alt": "display:flex;justify-content:space-between;align-items:center;padding:9px 18px;border-bottom:1px solid #ece4e0;font-size:13px;color:#3d2c2c;background:#fdf8f6;",
    "toc_num": "font-size:11px;font-weight:700;color:#c9847a;",
    "divider": "height:2px;background:linear-gradient(to right,#c9847a 30%,#e8d4cf 100%);margin:0 28px 28px;border-radius:1px;",
    "section_pad": "padding:0 28px 32px;",
    "h2": "font-size:18px;font-weight:800;color:#3d2c2c;line-height:1.4;margin:0 0 16px;padding-bottom:10px;border-bottom:2px solid #c9847a;",
    "h2_num": "color:#c9847a;font-size:13px;font-weight:700;display:block;margin-bottom:4px;letter-spacing:0.05em;",
    "h3": "font-size:15px;font-weight:700;color:#7a9e8e;margin:0 0 12px;padding-left:12px;border-left:3px solid #7a9e8e;",
    "p": "font-size:15px;color:#4a3a38;line-height:1.95;margin:0 0 16px;text-align:justify;",
    "callout_wrap": "background:#faf0ee;border:1px solid #ddd0c8;border-left:4px solid #c9847a;border-radius:0 12px 12px 0;padding:14px 18px;margin:18px 0;",
    "callout_label": "font-size:11px;font-weight:700;color:#c9847a;text-transform:uppercase;letter-spacing:0.08em;margin-bottom:6px;",
    "callout_text": "font-size:14px;color:#6a4a48;line-height:1.75;",
    "figure_wrap": "background:#f0ebe6;border-radius:12px;padding:12px;margin:20px 0;",
    "figure_caption": "font-size:11px;color:#9a7a78;text-align:center;margin:8px 0 0;line-height:1.4;",
    "li": "font-size:14px;color:#4a3a38;line-height:1.88;margin-bottom:6px;",
    "qr_wrap": "padding:24px 28px;text-align:center;background:#f5f0ec;border-top:1px solid #ddd0c8;",
    "qr_caption": "font-size:13px;color:#9a7a78;margin:0 0 12px;",
    "qr_img": "width:160px;height:160px;border:3px solid #c9847a;border-radius:12px;display:block;margin:0 auto 12px;",
    "qr_placeholder": "width:160px;height:160px;border:3px dashed #c9847a;border-radius:12px;display:flex;align-items:center;justify-content:center;margin:0 auto 12px;background:#faf0ee;",
    "qr_placeholder_text": "font-size:11px;color:#c9847a;text-align:center;padding:8px;",
    "qr_footnote": "font-size:11px;color:#b0998f;margin:0;",
    "series_label": "RNAscript · 前沿解读",
    "vol_text": "Vol.{vol} · {year}",
},
```

---

## 与其他主题的差异对比

| 设计维度 | 橙皮书 | 学术深蓝 | **莫兰迪淡雅** |
|----------|--------|----------|----------------|
| 主色调 | 橙红 `#e85d04` | 海军蓝 `#1e3a5f` | **玫瑰 `#c9847a`** |
| 辅色 | 橙黄 `#f97316` | 亮蓝 `#2563eb` | **矿绿 `#7a9e8e`** |
| 背景 | 暖米白 `#fffbf0` | 冷蓝白 `#f8fafd` | **奶茶米 `#faf7f4`** |
| 圆角风格 | 小圆角 `4-6px` | 小圆角 `4-6px` | **大圆角 `12-20px`** |
| 系列标签 | 矩形 `2px` | 矩形 `2px` | **胶囊 `20px`** |
| 关键词 | 小圆角矩形 | 小圆角矩形 | **胶囊圆角** |
| 字体 | 系统无衬线 | Georgia 衬线 | **系统无衬线** |
| 适用内容 | 技术深度解读 | 综述/基础科学 | **科普轻读/小红书风** |
| 顶部色带 | 单层橙 `8px` | 双层蓝 `6+2px` | **双层玫瑰+矿绿 `5+3px`** |
