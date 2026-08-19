---
name: anything-to-html
description: 将 Word、Markdown 或纯文本转换为可复制到微信公众号编辑器的高质量全内联 HTML。适用于公众号排版、文章主题套版、docx 图片内嵌、HTML 主题选择与输出质量验证；不用于普通网站或需要 JavaScript 的交互页面。
---

# Anything to HTML

将内容转换为自包含、可审计的 HTML。默认输出会把文章实际使用的字体字形压缩成 WOFF2 子集并内嵌，适合浏览器、WorkBuddy 和 README 展示；需要复制到微信公众号编辑器时使用 `--wechat`。

## 工作流

1. 识别输入。支持 `.docx`、`.md`、`.markdown`、`.txt`；直接粘贴的内容先保存为 UTF-8 Markdown。
2. 选择主题。用户指定主题时尊重其选择；未指定时按内容类型从 [主题契约](references/themes.md) 选择，并在生成前用一句话说明判断。
3. 转换。执行：

   ```powershell
   python scripts/convert.py INPUT --theme THEME --output OUTPUT.html
   ```

   微信公众号版本执行：

   ```powershell
   python scripts/convert.py INPUT --theme THEME --output OUTPUT.wechat.html --wechat
   ```

4. 验证。转换器默认自动验证；手工修改后再次执行：

   ```powershell
   python scripts/validate_html.py OUTPUT.html --theme THEME
   ```

5. 按 [质量标准](references/quality.md) 检查内容节奏、移动端宽度、表格、图片、标题层级和文末模块。验证失败不得交付。

## 主题与兼容性

共有 10 个独立主题。旧参数保持兼容：`orange` 映射到 `vibrant`，`nature` 映射到 `minimal`，`blue` 映射到 `academic-blue`。执行 `python scripts/convert.py --list-themes` 查看完整列表。

## 不可破坏的约束

- `--wechat` 输出只能使用元素自身的 `style` 属性；禁止 `<style>`、外部样式表和脚本。
- 所有正文图片与二维码必须是 `data:image/...;base64,...`。缺少二维码时使用注释占位，不伪造路径。
- 禁止 `<thead>`、`<tbody>` 和 `<tr style="...">`；表格样式写在 `<th>`、`<td>` 上。
- 保留 3 条“往期精选”占位和一个关注/二维码模块。
- 不编造作者、日期、来源、引用或参考文献；缺少信息时省略或保留明确占位。
- 不把用户原始 HTML 当作可信代码；转换器必须转义正文文本并拒绝外链图片。

## 字体策略

主题使用用户提供的 `XuanZongTi`（玄宗体）作为中文主字体，`Caveat Bold` 只用于英文编号和装饰标签。两款字体位于 `assets/fonts/`。

默认输出以内嵌 `data:font/woff2` 加载两款字体，不依赖安装目录、网络或用户电脑字体。转换器只保留文章实际使用的字形，避免嵌入完整的 39 MB 中文字体。微信公众号会移除 `@font-face`，因此交付公众号时必须使用 `--wechat`；该模式保留确定性系统回退。`--preview-fonts` 是兼容旧流程的本地路径预览模式。

## 输出位置

用户未指定输出路径时，输出到输入文件同目录。不得硬编码个人工作区路径。
