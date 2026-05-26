# 学术深蓝主题 · 完整内联样式规范

## 设计系统

| 变量 | 值 | 用途 |
|------|----|------|
| `bg_page` | `#eef2f7` | 页面外背景 |
| `bg_card` | `#f8fafd` | 主容器底色 |
| `accent` | `#1e3a5f` | 主强调色（深海军蓝，标题线、编号） |
| `accent_mid` | `#2563eb` | 次强调色（按钮、高亮） |
| `accent_light` | `#93c5fd` | 浅蓝边框色 |
| `accent_pale` | `#dbeafe` | 极浅蓝底（标注框、标签） |
| `bg_callout` | `#eff6ff` | 标注框底色 |
| `bg_stat` | `#f0f7ff` | 数据卡底色 |
| `bg_figure` | `#e8f0fb` | 图片块底色 |
| `text_main` | `#0f172a` | 正文主色 |
| `text_body` | `#1e293b` | 正文段落色 |
| `text_meta` | `#334e7a` | 导语/副标题色 |
| `text_muted` | `#4a6fa5` | 数据卡说明文字 |
| `text_gray` | `#94a3b8` | 期号/次要信息 |
| `text_toc` | `#1e3a5f` | 目录条目色 |
| `text_keyword` | `#1e40af` | 关键词标签文字 |
| `border_main` | `#bfdbfe` | 主边框色 |
| `border_light` | `#e0eaff` | 浅边框色 |

---

## 页面外壳

```html
<body style="margin:0;padding:0;background:#eef2f7;font-family:'Georgia','Times New Roman','Songti SC','SimSun',serif;color:#0f172a;line-height:1.85;">

<div style="max-width:680px;margin:0 auto;background:#f8fafd;">

<!-- 顶部色带（深蓝 + 细线） -->
<div style="background:#1e3a5f;height:6px;"></div>
<div style="background:#2563eb;height:2px;"></div>
```

---

## 页眉

```html
<div style="padding:14px 28px 12px;display:flex;justify-content:space-between;align-items:center;border-bottom:1px solid #bfdbfe;">
  <span style="font-size:11px;font-weight:700;color:#1e3a5f;letter-spacing:0.12em;font-family:-apple-system,sans-serif;">RNAscript · 学术综述</span>
  <span style="font-size:11px;color:#94a3b8;font-family:-apple-system,sans-serif;">Vol.XX · 202X</span>
</div>
```

---

## 封面区域

```html
<div style="padding:28px 28px 0;">
  <!-- 系列标签 -->
  <span style="display:inline-block;background:#1e3a5f;color:#fff;font-size:10px;font-weight:700;letter-spacing:0.1em;padding:4px 12px;border-radius:2px;margin-bottom:16px;font-family:-apple-system,sans-serif;">REVIEW ARTICLE</span>

  <!-- H1 大标题 -->
  <h1 style="font-size:22px;font-weight:700;color:#0f172a;line-height:1.4;margin:0 0 14px;padding-bottom:16px;border-bottom:3px solid #1e3a5f;font-family:Georgia,'Songti SC',serif;">
    [文章主标题]
  </h1>

  <!-- 导语副标题 -->
  <p style="font-size:14px;color:#334e7a;line-height:1.65;margin:0 0 14px;font-style:italic;font-family:Georgia,'Songti SC',serif;">
    [导语说明文字]
  </p>

  <!-- 文献来源 -->
  <div style="font-size:11px;color:#94a3b8;background:#e8f0fb;border-left:3px solid #2563eb;padding:8px 12px;border-radius:0 4px 4px 0;margin-bottom:24px;font-family:-apple-system,sans-serif;">
    Source：[引用信息]
  </div>
</div>
```

---

## 数据统计卡片行

```html
<div style="display:flex;gap:12px;margin:0 28px 24px;">
  <div style="flex:1;background:#f0f7ff;border:1px solid #bfdbfe;border-radius:6px;padding:14px 10px;text-align:center;">
    <div style="font-size:24px;font-weight:700;color:#1e3a5f;line-height:1;margin-bottom:4px;font-family:Georgia,serif;">257%</div>
    <div style="font-size:10px;color:#4a6fa5;line-height:1.4;font-family:-apple-system,sans-serif;">指标说明<br>第二行</div>
  </div>
</div>
```

---

## 摘要框

```html
<div style="margin:0 28px 20px;background:#f0f7ff;border:1px solid #bfdbfe;border-radius:6px;padding:16px 20px;">
  <div style="font-size:10px;font-weight:700;color:#1e3a5f;letter-spacing:0.12em;text-transform:uppercase;margin-bottom:8px;font-family:-apple-system,sans-serif;">ABSTRACT · 摘要</div>
  <p style="font-size:13px;color:#1e293b;line-height:1.8;margin:0;font-family:Georgia,'Songti SC',serif;">[摘要内容]</p>
</div>
```

---

## 关键词标签

```html
<div style="padding:0 28px 20px;display:flex;flex-wrap:wrap;gap:6px;">
  <span style="font-size:11px;padding:3px 10px;background:#dbeafe;border:1px solid #93c5fd;color:#1e40af;border-radius:3px;font-family:-apple-system,sans-serif;">关键词</span>
</div>
```

---

## 目录

```html
<div style="margin:0 28px 28px;border:1px solid #bfdbfe;border-radius:6px;overflow:hidden;">
  <div style="background:#1e3a5f;color:#fff;font-size:11px;font-weight:700;letter-spacing:0.1em;padding:8px 16px;text-transform:uppercase;font-family:-apple-system,sans-serif;">CONTENTS · 目录</div>

  <!-- 主章节 -->
  <div style="display:flex;justify-content:space-between;align-items:center;padding:9px 16px;border-bottom:1px solid #e0eaff;font-size:13px;color:#1e3a5f;">
    <span>一、章节名称</span>
    <span style="font-size:11px;font-weight:700;color:#2563eb;">§1</span>
  </div>

  <!-- 子节（偶数行加底色） -->
  <div style="display:flex;justify-content:space-between;padding:5px 16px 5px 28px;border-bottom:1px solid #e0eaff;font-size:11px;color:#4a6fa5;background:#f4f8ff;">
    <span>1.1 子节名称</span>
    <span style="color:#2563eb;">§1.1</span>
  </div>
</div>
```

---

## 章节分隔线

```html
<div style="height:2px;background:linear-gradient(to right,#1e3a5f 30%,#dbeafe 100%);margin:0 28px 28px;border-radius:1px;"></div>
```

---

## H2 章节标题

```html
<h2 style="font-size:18px;font-weight:700;color:#0f172a;line-height:1.4;margin:0 0 16px;padding-bottom:10px;border-bottom:2px solid #1e3a5f;font-family:Georgia,'Songti SC',serif;">
  <span style="color:#2563eb;font-size:13px;font-weight:700;display:block;margin-bottom:4px;font-family:-apple-system,sans-serif;letter-spacing:0.05em;">§ N</span>
  章节正文标题
</h2>
```

---

## H3 子节标题

```html
<h3 style="font-size:15px;font-weight:700;color:#1e3a5f;margin:0 0 12px;padding-left:10px;border-left:3px solid #2563eb;font-family:Georgia,'Songti SC',serif;">
  子节标题
</h3>
```

---

## 正文段落

```html
<p style="font-size:15px;color:#1e293b;line-height:1.9;margin:0 0 16px;text-align:justify;font-family:Georgia,'Songti SC',serif;">
  段落内容
</p>
```

---

## 标注/引用框（Callout）

```html
<div style="background:#eff6ff;border:1px solid #bfdbfe;border-left:4px solid #2563eb;border-radius:0 6px 6px 0;padding:14px 18px;margin:18px 0;">
  <div style="font-size:10px;font-weight:700;color:#1e3a5f;text-transform:uppercase;letter-spacing:0.1em;margin-bottom:6px;font-family:-apple-system,sans-serif;">NOTE · 编者注</div>
  <div style="font-size:14px;color:#334e7a;line-height:1.75;font-family:Georgia,'Songti SC',serif;">[标注内容]</div>
</div>
```

---

## 图片块

```html
<div style="background:#e8f0fb;border-radius:6px;padding:12px;margin:20px 0;">
  <img src="data:image/jpeg;base64,[BASE64]" style="width:100%;display:block;border-radius:4px;" alt="图N">
  <p style="font-size:11px;color:#4a6fa5;text-align:center;margin:8px 0 0;line-height:1.4;font-family:-apple-system,sans-serif;">Figure N · [图注文字]</p>
</div>
```

---

## 数据对比卡片

```html
<div style="border:1px solid #bfdbfe;border-radius:8px;overflow:hidden;margin:16px 0;">
  <div style="background:#dbeafe;border-bottom:1px solid #bfdbfe;padding:10px 16px;">
    <strong style="font-size:14px;color:#1e3a5f;font-family:Georgia,'Songti SC',serif;">蛋白质/主题名称</strong>
    <span style="font-size:11px;color:#4a6fa5;margin-left:8px;font-family:-apple-system,sans-serif;">副标题</span>
  </div>
  <div style="padding:12px 16px;background:#f8fafd;">
    <p style="font-size:14px;color:#1e293b;line-height:1.75;margin:0 0 8px;font-family:Georgia,'Songti SC',serif;">[正文内容]</p>
    <div style="font-size:12px;color:#334e7a;background:#eff6ff;border-left:3px solid #93c5fd;padding:6px 10px;border-radius:0 4px 4px 0;font-family:-apple-system,sans-serif;">
      ℹ️ 注意事项
    </div>
  </div>
</div>
```

---

## 列表

```html
<ul style="margin:0 0 16px;padding-left:20px;">
  <li style="font-size:14px;color:#1e293b;line-height:1.85;margin-bottom:6px;font-family:Georgia,'Songti SC',serif;">列表项内容</li>
</ul>
```

---

## 底部色带

```html
<div style="background:#2563eb;height:2px;margin-top:8px;"></div>
<div style="background:#1e3a5f;height:6px;"></div>
```

---

## 二维码 / 关注区

```html
<div style="padding:24px 28px;text-align:center;background:#f0f7ff;border-top:1px solid #bfdbfe;">
  <p style="font-size:13px;color:#334e7a;margin:0 0 12px;font-family:-apple-system,sans-serif;">扫码关注 · 获取最新内容</p>
  <img src="data:image/jpeg;base64,[QR_BASE64]"
       style="width:160px;height:160px;border:3px solid #2563eb;border-radius:8px;display:block;margin:0 auto 12px;"
       alt="公众号二维码">
  <p style="font-size:11px;color:#94a3b8;margin:0;font-family:-apple-system,sans-serif;">RNAscript · mRNA技术洞察</p>
</div>
```

若无二维码，使用占位框：
```html
<div style="width:160px;height:160px;border:3px solid #2563eb;border-radius:8px;display:flex;align-items:center;justify-content:center;margin:0 auto 12px;background:#dbeafe;">
  <span style="font-size:11px;color:#1e3a5f;text-align:center;padding:8px;font-family:-apple-system,sans-serif;">扫码关注<br>公众号</span>
</div>
```
