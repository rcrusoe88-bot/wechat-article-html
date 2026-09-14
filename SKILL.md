---
name: anything-to-html
description: 将 Word、Markdown 或纯文本转换为可直接粘贴到微信公众号后台的全内联 HTML。适用于公众号文章排版、三套主题套版、docx 图片内嵌、二维码图片占位与版式稳定性验证。
---

# Anything to HTML

将内容转换为只面向微信公众号的 `*.wechat.html`。输出不声明 `font-family`，粘贴到公众号后台后由微信阅读端使用原生字体。

## 工作流

1. 识别输入。支持 `.docx`、`.md`、`.markdown`、`.txt`；直接粘贴的内容先保存为 UTF-8 Markdown。
2. 选择主题。用户指定主题时尊重其选择；未指定时按内容类型从 [主题契约](references/themes.md) 选择，并在生成前用一句话说明判断。
3. 转换。执行：

   ```powershell
   python scripts/convert.py INPUT --theme THEME
   ```

   未传 `--output` 时，默认写出 `INPUT_主题名.wechat.html`。

4. 验证。转换器默认自动验证；手工修改后再次执行：

   ```powershell
   python scripts/validate_html.py OUTPUT.wechat.html --theme THEME
   ```

5. 按 [质量标准](references/quality.md) 检查内容节奏、移动端宽度、表格、图片、标题层级和文末模块。验证失败不得交付。

## 主题与兼容性

固定提供 `kami`、`esther`、`punk` 三套独立主题。未指定主题时默认使用 `kami`；执行 `python scripts/convert.py --list-themes` 查看当前列表。

## 不可破坏的约束

- 只输出微信公众号版 `*.wechat.html`，不生成浏览器版或本地字体预览版。
- 禁止 `<style>`、外部样式表、脚本、事件属性和任何 `font-family`。不写 `PingFang SC`、微软雅黑或其他猜测性字体栈，直接使用微信读者端默认字体。
- 所有正文图片与二维码必须是 `data:image/...;base64,...`。未传入 `--qr` 时使用 `assets/images/qr-placeholder.png` 作为固定图片占位，不伪造外部路径。
- 禁止 `<thead>`、`<tbody>` 和 `<tr style="...">`；表格样式写在 `<th>`、`<td>` 上。
- 保留 3 条“往期精选”占位和一个关注/二维码模块。
- 不编造作者、日期、来源、引用或参考文献；缺少信息时省略或保留明确占位。
- 不把用户原始 HTML 当作可信代码；转换器必须转义正文文本并拒绝外链图片。

## 字体策略

生成过程中可以在内部渲染主题设计，但交付前必须移除全部字体声明。最终 HTML 不包含 `Caveat`、`XuanZongTi`、`@font-face`、WOFF2 data URI 或任何本地字体路径。公众号阅读端负责使用其原生字体。

## 输出位置

用户未指定输出路径时，输出到输入文件同目录。不得硬编码个人工作区路径。
