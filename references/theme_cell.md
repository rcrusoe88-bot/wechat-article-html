# Cell 主题 · 完整内联样式规范

## 设计理念

期刊封面风，灵感来自 Cell 期刊。色块分区、层次丰富、大胆的视觉对比，深蓝章节头色块搭配白色正文区域形成强烈的区域划分感。

**结构特征**：无目录、无数据统计卡片、深蓝章节头色块（SECTION NN）、蓝色圆点 H3 标记、阴影图片容器。

## 设计系统

| 变量 | 值 | 用途 |
|------|----|------|
| `bg_page` | `#edf2f7` | 页面外背景 |
| `bg_card` | `#fff` | 主容器底色 |
| `accent` | `#1e3a5f` | 主强调色（深海军蓝） |
| `accent_mid` | `#2563eb` | 次强调色（亮蓝） |
| `accent_light` | `#93c5fd` | 浅蓝文字色 |
| `accent_pale` | `#eff6ff` | 极浅蓝底 |
| `border_main` | `#e2e8f0` | 主边框色 |
| `bg_abstract` | `#f8fafc` | 摘要框底色 |
| `text_main` | `#0f172a` | 正文主色 |
| `text_body` | `#334155` | 正文段落色 |
| `text_meta` | `#64748b` | 导语/副标题色 |
| `text_muted` | `#94a3b8` | 次要信息色 |
| `text_keyword` | `#1e40af` | 关键词文字色 |
| `border_keyword` | `#bfdbfe` | 关键词边框色 |
| `font_sans` | `-apple-system, Helvetica Neue, PingFang SC` | 主无衬线体 |
| `font_serif` | `Georgia, Songti SC` | 正文衬线体 |

---

## 页面外壳

```html
<body style="margin:0;padding:0;background:#edf2f7;font-family:-apple-system,'Helvetica Neue','PingFang SC',sans-serif;color:#0f172a;line-height:1;">
<div style="max-width:640px;margin:0 auto;background:#fff;box-shadow:0 0 40px rgba(0,0,0,0.06);">

<!-- 顶部装饰条 -->
<div style="height:6px;background:#1e3a5f;"></div>
```

---

## 页眉

```html
<div style="padding:16px 32px;display:flex;justify-content:space-between;align-items:center;border-bottom:2px solid #e2e8f0;">
  <span style="font-size:11px;font-weight:800;color:#1e3a5f;letter-spacing:0.15em;">RNAscript</span>
  <span style="font-size:11px;color:#94a3b8;">Vol.XX · 202X</span>
</div>
```

---

## 封面区域

```html
<div style="padding:32px 32px 0;">
  <!-- 蓝色竖线 + 系列标签 -->
  <div style="display:flex;align-items:center;gap:8px;margin-bottom:16px;">
    <div style="width:4px;height:20px;background:#2563eb;border-radius:2px;"></div>
    <span style="font-size:10px;font-weight:700;color:#2563eb;letter-spacing:0.12em;text-transform:uppercase;">深度解读</span>
  </div>

  <!-- H1 大标题 — 粗体无衬线 -->
  <h1 style="font-size:23px;font-weight:800;color:#0f172a;line-height:1.35;margin:0 0 14px;letter-spacing:-0.01em;">
    [文章主标题]
  </h1>

  <!-- 导语副标题 -->
  <p style="font-size:14px;color:#64748b;line-height:1.6;margin:0 0 20px;">
    [导语说明文字]
  </p>

  <!-- 文献来源 — 灰色药丸 -->
  <div style="display:inline-block;font-size:11px;color:#64748b;background:#f1f5f9;padding:6px 12px;border-radius:4px;margin-bottom:24px;">
    [来源信息]
  </div>
</div>
```

---

## 摘要框

```html
<div style="margin:20px 32px;padding:18px 20px;background:#f8fafc;border:1px solid #e2e8f0;border-radius:8px;">
  <div style="font-size:9px;font-weight:800;color:#2563eb;letter-spacing:0.15em;text-transform:uppercase;margin-bottom:8px;">ABSTRACT</div>
  <p style="font-size:13px;color:#334155;line-height:1.8;margin:0;font-family:Georgia,'Songti SC',serif;">[摘要内容]</p>
</div>
```

---

## 关键词

蓝色药丸带边框：

```html
<div style="padding:0 32px 20px;display:flex;flex-wrap:wrap;gap:6px;">
  <span style="font-size:10px;padding:4px 10px;background:#eff6ff;color:#1e40af;border-radius:20px;font-weight:600;border:1px solid #bfdbfe;">关键词</span>
</div>
```

---

## H2 章节标题 — 深蓝色块

```html
<div style="margin-top:36px;padding:0 32px;">
  <div style="background:#1e3a5f;margin:0 -32px;padding:16px 32px;margin-bottom:20px;border-radius:0 12px 0 0;">
    <div style="display:flex;align-items:center;gap:14px;">
      <div style="font-size:13px;font-weight:800;color:#93c5fd;letter-spacing:0.05em;">SECTION 01</div>
      <div style="flex:1;height:1px;background:rgba(255,255,255,0.15);"></div>
    </div>
    <h2 style="font-size:18px;font-weight:700;color:#fff;margin:8px 0 0;line-height:1.3;">
      章节正文标题
    </h2>
  </div>
</div>
```

参考资料特殊渲染：

```html
<div style="padding:8px 32px;">
  <div style="width:40px;height:2px;background:#2563eb;border-radius:1px;margin-bottom:12px;"></div>
  <h2 style="font-size:15px;font-weight:800;color:#0f172a;margin:0 0 12px;">
    参考资料
  </h2>
</div>
```

---

## H3 子节标题 — 蓝色圆点标记

```html
<div style="padding:0 32px;margin-top:20px;">
  <div style="display:flex;align-items:center;gap:8px;">
    <div style="width:8px;height:8px;background:#2563eb;border-radius:50%;flex-shrink:0;"></div>
    <h3 style="font-size:14px;font-weight:700;color:#1e3a5f;margin:0;">
      子节标题
    </h3>
  </div>
</div>
```

---

## 正文段落

```html
<div style="padding:0 32px;">
  <p style="font-size:14.5px;color:#334155;line-height:1.85;margin:0 0 13px;text-align:justify;font-family:Georgia,'Songti SC',serif;">
    段落内容
  </p>
</div>
```

---

## 图片块

阴影容器 + 圆角裁切：

```html
<div style="padding:0 32px;margin:16px 0;">
  <div style="border-radius:8px;overflow:hidden;box-shadow:0 2px 8px rgba(30,58,95,0.08);">
    <img src="data:image/jpeg;base64,[BASE64]" style="width:100%;display:block;" alt="">
  </div>
</div>
```

---

## 列表

```html
<ul style="margin:0 32px 13px;padding-left:20px;">
  <li style="font-size:14px;color:#334155;line-height:1.85;margin-bottom:6px;font-family:Georgia,'Songti SC',serif;">
    列表项内容
  </li>
</ul>
```

---

## 底部 — 深蓝 Footer 色块

```html
<div style="margin-top:32px;background:#1e3a5f;padding:28px 32px;text-align:center;border-radius:12px 12px 0 0;">
  <p style="font-size:12px;color:#93c5fd;margin:0 0 16px;font-weight:600;letter-spacing:0.08em;">FOLLOW US</p>
  <img src="data:image/jpeg;base64,[QR_BASE64]"
       style="width:140px;height:140px;display:block;margin:0 auto 12px;border-radius:8px;border:2px solid rgba(255,255,255,0.15);"
       alt="">
  <p style="font-size:10px;color:#64748b;margin:0;letter-spacing:0.06em;">RNAscript · 信使引擎</p>
</div>
```

占位框：

```html
<div style="width:140px;height:140px;border:2px solid rgba(255,255,255,0.2);border-radius:8px;display:flex;align-items:center;justify-content:center;margin:0 auto 12px;">
  <span style="font-size:11px;color:#93c5fd;text-align:center;">扫码关注<br>公众号</span>
</div>
```

---

## 适用场景

- 临床数据解读（AACR/ESMO/ASCO）
- 产品管线分析
- 行业格局报告
- 需要视觉冲击力和层次感的深度内容
