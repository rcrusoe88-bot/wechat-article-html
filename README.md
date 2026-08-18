# anything-to-html

将 Word、Markdown 和纯文本转换为微信公众号兼容的全内联 HTML。

## 功能

- 10 个独立主题，兼容旧参数 `orange`、`blue`、`nature` 和 `morandi`
- Word 正文、表格和内嵌图片按文档顺序提取
- Markdown 标题、列表、引用、代码、表格和本地图片转换
- 正文图片与二维码自动转为 base64
- 发布版严格禁止外部 CSS、脚本、网络字体和外链图片
- 本地预览可加载 `Caveat Bold` 与 `XuanZongTi`（玄宗体）字体
- 转换完成后自动执行 HTML 与主题契约验证

## 使用

```powershell
pip install -r requirements.txt
python scripts/convert.py article.docx --theme academic-blue --output article.html
python scripts/convert.py article.md --theme magazine --output article.html
python scripts/convert.py --list-themes
```

本地字体预览：

```powershell
python scripts/convert.py article.md --theme classic --output article.preview.html --preview-fonts
```

转换器会自动计算输出文件到字体目录的相对路径。带 `--preview-fonts` 的文件包含 `<style>@font-face</style>`，仅用于浏览器验收，不能作为微信公众号发布版。

## 许可证

代码和文档使用 MIT License。`assets/fonts/` 中的字体由项目使用者提供，不随项目代码重新授权，详见 `THIRD_PARTY_NOTICES.md`。
