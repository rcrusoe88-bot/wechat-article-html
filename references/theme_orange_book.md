# 橙皮书主题 · 完整内联样式规范

## 设计系统

| 变量 | 值 | 用途 |
|------|----|------|
| `bg_page` | `#f5f0e8` | 页面外背景 |
| `bg_card` | `#fffbf0` | 主容器底色 |
| `accent` | `#e85d04` | 主强调色（标题线、按钮、编号） |
| `accent_light` | `#f97316` | 次强调色（关键词边框、QR 边框） |
| `accent_pale` | `#fcd9b6` | 浅调边框色 |
| `bg_callout` | `#fff3e0` | 标注框底色 |
| `bg_stat` | `#fff8f0` | 数据卡底色 |
| `bg_figure` | `#f5ece0` | 图片块底色 |
| `text_main` | `#1a0800` | 正文主色 |
| `text_body` | `#2a1000` | 正文段落色 |
| `text_meta` | `#7a4020` | 导语/副标题色 |
| `text_muted` | `#a05030` | 数据卡说明文字 |
| `text_gray` | `#999` | 期号/次要信息 |
| `text_toc` | `#3a1a08` | 目录条目色 |
| `text_keyword` | `#c2410c` | 关键词标签文字 |

---

## 页面外壳

```html
<!-- 页面 body -->
<body style="margin:0;padding:0;background:#f5f0e8;font-family:-apple-system,'PingFang SC','Helvetica Neue',Arial,sans-serif;color:#1a0800;line-height:1.8;">

<!-- 主容器 -->
<div style="max-width:680px;margin:0 auto;background:#fffbf0;">

<!-- 顶部色带 -->
<div style="background:#e85d04;height:8px;"></div>
```

---

## 页眉

```html
<div style="padding:16px 28px 14px;display:flex;justify-content:space-between;align-items:center;border-bottom:1px solid #f0e8d8;">
  <span style="font-size:11px;font-weight:700;color:#e85d04;letter-spacing:0.1em;">RNAscript · 技术白皮书</span>
  <span style="font-size:11px;color:#999;">Vol.XX · 202X</span>
</div>
```

---

## 封面区域

```html
<div style="padding:28px 28px 0;">
  <!-- 系列标签 -->
  <span style="display:inline-block;background:#e85d04;color:#fff;font-size:11px;font-weight:700;letter-spacing:0.08em;padding:4px 12px;border-radius:2px;margin-bottom:16px;">博士论文深度解读</span>

  <!-- H1 大标题 -->
  <h1 style="font-size:22px;font-weight:800;color:#1a0800;line-height:1.35;margin:0 0 12px;padding-bottom:16px;border-bottom:3px solid #e85d04;">
    [文章主标题]
  </h1>

  <!-- 导语副标题 -->
  <p style="font-size:14px;color:#7a4020;line-height:1.6;margin:0 0 14px;font-style:italic;">
    [导语说明文字]
  </p>

  <!-- 文献来源 -->
  <div style="font-size:11px;color:#999;background:#f5ece0;border-left:3px solid #f97316;padding:8px 12px;border-radius:0 4px 4px 0;margin-bottom:24px;">
    文献来源：[引用信息]
  </div>
</div>
```

---

## 数据统计卡片行

```html
<div style="display:flex;gap:12px;margin:0 28px 24px;">
  <div style="flex:1;background:#fff8f0;border:1px solid #fcd9b6;border-radius:6px;padding:14px 10px;text-align:center;">
    <div style="font-size:26px;font-weight:800;color:#e85d04;line-height:1;margin-bottom:4px;">257%</div>
    <div style="font-size:10px;color:#a05030;line-height:1.4;">指标说明<br>第二行</div>
  </div>
  <!-- 重复 2-3 个 -->
</div>
```

---

## 摘要框

```html
<div style="margin:0 28px 20px;background:#fff8f0;border:1px solid #fcd9b6;border-radius:6px;padding:16px 20px;">
  <div style="font-size:10px;font-weight:700;color:#e85d04;letter-spacing:0.1em;text-transform:uppercase;margin-bottom:8px;">摘要 Abstract</div>
  <p style="font-size:13px;color:#4a2010;line-height:1.75;margin:0;">[摘要内容]</p>
</div>
```

---

## 关键词标签

```html
<div style="padding:0 28px 20px;display:flex;flex-wrap:wrap;gap:6px;">
  <span style="font-size:11px;padding:3px 10px;background:#fff3e0;border:1px solid #f97316;color:#c2410c;border-radius:3px;">关键词</span>
</div>
```

---

## 目录

```html
<div style="margin:0 28px 28px;border:1px solid #e8d0b0;border-radius:6px;overflow:hidden;">
  <!-- 目录头 -->
  <div style="background:#e85d04;color:#fff;font-size:11px;font-weight:700;letter-spacing:0.08em;padding:8px 16px;text-transform:uppercase;">目录 Contents</div>

  <!-- 主章节条目 -->
  <div style="display:flex;justify-content:space-between;align-items:center;padding:9px 16px;border-bottom:1px solid #f0e4d0;font-size:13px;color:#3a1a08;">
    <span>一、章节名称</span>
    <span style="font-size:11px;font-weight:700;color:#e85d04;">§1</span>
  </div>

  <!-- 子节条目（缩进，偶数行加底色） -->
  <div style="display:flex;justify-content:space-between;padding:5px 16px 5px 28px;border-bottom:1px solid #f0e4d0;font-size:11px;color:#888;background:#fffaf4;">
    <span>1.1 子节名称</span>
    <span style="color:#e85d04;">§1.1</span>
  </div>
</div>
```

---

## 章节分隔线

```html
<div style="height:2px;background:linear-gradient(to right,#e85d04 30%,#fcd9b6 100%);margin:0 28px 28px;border-radius:1px;"></div>
```

---

## H2 章节标题

```html
<h2 style="font-size:18px;font-weight:800;color:#1a0800;line-height:1.4;margin:0 0 16px;padding-bottom:10px;border-bottom:2px solid #e85d04;">
  <span style="color:#e85d04;font-size:14px;font-weight:700;display:block;margin-bottom:4px;">§ N 节号</span>
  章节正文标题
</h2>
```

---

## H3 子节标题

```html
<h3 style="font-size:15px;font-weight:700;color:#e85d04;margin:0 0 12px;padding-left:10px;border-left:3px solid #e85d04;">
  子节标题
</h3>
```

---

## 正文段落

```html
<p style="font-size:15px;color:#2a1000;line-height:1.9;margin:0 0 16px;text-align:justify;">
  段落内容
</p>
```

---

## 标注/引用框（Callout）

```html
<div style="background:#fff3e0;border:1px solid #fcd9b6;border-left:4px solid #e85d04;border-radius:0 6px 6px 0;padding:14px 18px;margin:18px 0;">
  <div style="font-size:11px;font-weight:700;color:#e85d04;text-transform:uppercase;letter-spacing:0.08em;margin-bottom:6px;">编者按</div>
  <div style="font-size:14px;color:#7a3010;line-height:1.7;">[标注内容，可含 <strong style="color:#e85d04;font-weight:800;">加粗强调</strong>]</div>
</div>
```

---

## 图片块

```html
<div style="background:#f5ece0;border-radius:6px;padding:12px;margin:20px 0;">
  <img src="data:image/jpeg;base64,[BASE64]" style="width:100%;display:block;border-radius:4px;" alt="图N">
  <p style="font-size:11px;color:#a05030;text-align:center;margin:8px 0 0;line-height:1.4;">图N · [图注文字]</p>
</div>
```

---

## 数据对比表格行

```html
<div style="border:1px solid #fcd9b6;border-radius:8px;overflow:hidden;margin:16px 0;">
  <!-- 表头 -->
  <div style="background:#fff3e0;border-bottom:1px solid #fcd9b6;padding:10px 16px;">
    <strong style="font-size:14px;color:#e85d04;">蛋白质名称</strong>
    <span style="font-size:11px;color:#a05030;margin-left:8px;">副标题</span>
  </div>
  <!-- 内容 -->
  <div style="padding:12px 16px;">
    <p style="font-size:14px;color:#3a1a08;line-height:1.7;margin:0 0 8px;">[正文内容]</p>
    <div style="font-size:12px;color:#7a4020;background:#fffbf0;border-left:3px solid #fcd9b6;padding:6px 10px;border-radius:0 4px 4px 0;">
      ⚠️ 注意事项
    </div>
  </div>
</div>
```

---

## 列表

```html
<ul style="margin:0 0 16px;padding-left:20px;">
  <li style="font-size:14px;color:#2a1000;line-height:1.8;margin-bottom:6px;">列表项内容</li>
</ul>
```

---

## 底部色带

```html
<!-- 底部色带 -->
<div style="background:#e85d04;height:8px;margin-top:8px;"></div>
```

---

## 二维码 / 关注区

```html
<div style="padding:24px 28px;text-align:center;background:#fff8f0;border-top:1px solid #fcd9b6;">
  <p style="font-size:13px;color:#7a4020;margin:0 0 12px;">扫码关注 · 获取最新内容</p>
  <img src="data:image/jpeg;base64,[QR_BASE64]"
       style="width:160px;height:160px;border:3px solid #f97316;border-radius:8px;display:block;margin:0 auto 12px;"
       alt="公众号二维码">
  <p style="font-size:11px;color:#999;margin:0;">RNAscript · mRNA技术洞察</p>
</div>
```

若无二维码图片，使用占位框：
```html
<div style="width:160px;height:160px;border:3px solid #f97316;border-radius:8px;display:flex;align-items:center;justify-content:center;margin:0 auto 12px;background:#fff3e0;">
  <span style="font-size:11px;color:#e85d04;text-align:center;padding:8px;">扫码关注<br>公众号</span>
</div>
```
