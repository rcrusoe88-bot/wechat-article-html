# Nature 主题 · 完整内联样式规范

## 设计理念

极简学术编辑风，灵感来自 Nature 期刊排版。克制的色彩、大量留白、衬线体主导，一条极细黑线撑起整个层次结构。

**结构特征**：无目录、无数据统计卡片、大号装饰章节编号、极简 H3 左竖线。

## 设计系统

| 变量 | 值 | 用途 |
|------|----|------|
| `bg_page` | `#fafafa` | 页面外背景 |
| `bg_card` | `#fff` | 主容器底色 |
| `accent` | `#1a1a1a` | 主强调色（黑） |
| `accent_light` | `#e0e0e0` | 装饰章节编号色 |
| `accent_muted` | `#999` | 次要文字色 |
| `border_main` | `#e5e5e5` | 主分隔线色 |
| `border_light` | `#ccc` | 辅助分隔线色 |
| `bg_abstract` | `#f7f7f7` | 摘要框底色 |
| `text_main` | `#1a1a1a` | 正文主色 |
| `text_body` | `#2a2a2a` | 正文段落色 |
| `text_meta` | `#666` | 导语/副标题色 |
| `font_serif` | `Georgia, Palatino, Songti SC, SimSun` | 正文衬线体 |
| `font_sans` | `-apple-system, Helvetica Neue, PingFang SC` | UI 无衬线体 |

---

## 页面外壳

```html
<body style="margin:0;padding:0;background:#fafafa;font-family:'Georgia','Palatino','Songti SC','SimSun',serif;color:#1a1a1a;line-height:1;">
<div style="max-width:640px;margin:0 auto;background:#fff;">

<!-- 顶线 — 3px 黑 -->
<div style="height:3px;background:#1a1a1a;"></div>
```

---

## 页眉

```html
<div style="padding:20px 32px 16px;border-bottom:1px solid #e5e5e5;">
  <div style="display:flex;justify-content:space-between;align-items:baseline;">
    <span style="font-size:10px;font-weight:700;color:#1a1a1a;letter-spacing:0.18em;text-transform:uppercase;font-family:-apple-system,sans-serif;">RNAscript</span>
    <span style="font-size:10px;color:#999;font-family:-apple-system,sans-serif;letter-spacing:0.05em;">Vol.XX · 202X</span>
  </div>
</div>
```

---

## 封面区域

```html
<div style="padding:36px 32px 0;">
  <!-- 系列标签 — 纯文字，无背景 -->
  <span style="display:inline-block;font-size:10px;font-weight:600;color:#666;letter-spacing:0.1em;text-transform:uppercase;margin-bottom:20px;font-family:-apple-system,sans-serif;">深度解读</span>

  <!-- H1 大标题 — 衬线、轻字重、大号 -->
  <h1 style="font-size:26px;font-weight:400;color:#1a1a1a;line-height:1.35;margin:0 0 20px;letter-spacing:-0.01em;font-family:'Georgia','Palatino','Songti SC','SimSun',serif;">
    [文章主标题]
  </h1>

  <!-- 导语副标题 — 斜体 -->
  <p style="font-size:15px;color:#666;line-height:1.6;margin:0 0 24px;font-style:italic;font-family:'Georgia','Palatino','Songti SC','SimSun',serif;">
    [导语说明文字]
  </p>

  <!-- 文献来源 — 左竖线 -->
  <div style="font-size:11px;color:#999;border-left:2px solid #ccc;padding:6px 12px;margin-bottom:28px;font-family:-apple-system,sans-serif;">
    [来源信息]
  </div>
</div>
```

---

## 摘要框

```html
<div style="margin:0 32px 24px;padding:16px 20px;background:#f7f7f7;border-radius:4px;">
  <div style="font-size:9px;font-weight:700;color:#999;letter-spacing:0.15em;text-transform:uppercase;margin-bottom:8px;font-family:-apple-system,sans-serif;">ABSTRACT</div>
  <p style="font-size:13px;color:#333;line-height:1.8;margin:0;font-family:'Georgia','Palatino','Songti SC','SimSun',serif;">[摘要内容]</p>
</div>
```

---

## 关键词

下划线文字风格（非药片/标签式）：

```html
<div style="padding:0 32px 24px;display:flex;flex-wrap:wrap;gap:8px;">
  <span style="font-size:11px;color:#666;padding:3px 0;border-bottom:1px solid #ccc;font-family:-apple-system,sans-serif;">关键词</span>
</div>
```

---

## 分隔线

```html
<div style="margin:0 32px 28px;height:1px;background:#e5e5e5;"></div>
```

---

## H2 章节标题 — 装饰大号编号

```html
<div style="margin:0 32px;margin-top:36px;">
  <div style="display:flex;align-items:baseline;gap:12px;margin-bottom:20px;">
    <span style="font-size:32px;font-weight:300;color:#e0e0e0;line-height:1;font-family:'Georgia','Palatino','Songti SC','SimSun',serif;">01</span>
    <h2 style="font-size:19px;font-weight:400;color:#1a1a1a;margin:0;line-height:1.3;letter-spacing:-0.005em;">
      章节正文标题
    </h2>
  </div>
</div>
```

参考资料特殊渲染（无编号）：

```html
<div style="margin:0 32px;">
  <h2 style="font-size:16px;font-weight:400;color:#1a1a1a;margin:0 0 16px;padding-bottom:8px;border-bottom:1px solid #e5e5e5;letter-spacing:0.02em;">
    参考资料
  </h2>
</div>
```

---

## H3 子节标题 — 极简左竖线

```html
<div style="margin:0 32px;margin-top:20px;">
  <h3 style="font-size:14px;font-weight:600;color:#1a1a1a;margin:0 0 12px;padding-left:14px;border-left:2px solid #1a1a1a;font-family:-apple-system,sans-serif;letter-spacing:0.01em;">
    子节标题
  </h3>
</div>
```

---

## 正文段落

```html
<div style="margin:0 32px;">
  <p style="font-size:15px;color:#2a2a2a;line-height:1.9;margin:0 0 14px;text-align:justify;font-family:'Georgia','Palatino','Songti SC','SimSun',serif;">
    段落内容
  </p>
</div>
```

---

## 图片块

极简无底色，仅轻微圆角：

```html
<div style="margin:20px 32px;">
  <img src="data:image/jpeg;base64,[BASE64]" style="width:100%;display:block;border-radius:2px;" alt="">
</div>
```

---

## 列表

```html
<ul style="margin:0 32px 14px;padding-left:20px;">
  <li style="font-size:14px;color:#2a2a2a;line-height:1.8;margin-bottom:6px;font-family:'Georgia','Palatino','Songti SC','SimSun',serif;">
    列表项内容
  </li>
</ul>
```

---

## 底部分隔线

```html
<div style="margin:0 32px 20px;height:1px;background:#e5e5e5;"></div>
```

## 二维码 / 关注区

```html
<div style="padding:28px 32px;text-align:center;">
  <p style="font-size:12px;color:#999;margin:0 0 16px;font-family:-apple-system,sans-serif;letter-spacing:0.05em;">FOLLOW US</p>
  <img src="data:image/jpeg;base64,[QR_BASE64]"
       style="width:140px;height:140px;display:block;margin:0 auto 12px;border-radius:2px;"
       alt="">
  <p style="font-size:10px;color:#bbb;margin:0;font-family:-apple-system,sans-serif;letter-spacing:0.08em;">RNAscript · 信使引擎</p>
</div>
```

占位框：

```html
<div style="width:140px;height:140px;border:2px solid #e0e0e0;border-radius:2px;display:flex;align-items:center;justify-content:center;margin:0 auto 12px;">
  <span style="font-size:11px;color:#999;text-align:center;font-family:-apple-system,sans-serif;">扫码关注<br>公众号</span>
</div>
```

## 底线

```html
<div style="height:3px;background:#1a1a1a;"></div>
```

---

## 适用场景

- 文献深度解读、数据解读
- 学术论文分析报告
- 严肃的长篇综述
- 需要大量留白和阅读舒适度的内容
