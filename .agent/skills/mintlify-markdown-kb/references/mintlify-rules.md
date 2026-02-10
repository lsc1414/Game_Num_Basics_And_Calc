# Mintlify Markdown Rules

## 1. Frontmatter

```yaml
---
title: "文档标题"
description: "简短说明用途与范围"
sidebarTitle: "侧边栏标题" # 可选
icon: "rocket" # 可选
---
```

规则:
- 保持 YAML 合法，避免 tab 缩进。
- `title` 与 `description` 必填。

## 2. `.md` vs `.mdx`

- 默认使用 `.md`。
- 只有在必须使用 Mintlify React 组件时用 `.mdx`。
- `.md` 可用标准 Markdown、GitHub Alerts、Mermaid、表格、数学公式。

## 3. 提示块语法

- 目标语法: GitHub Alert

```markdown
> [!NOTE]
> 说明文字
```

- 迁移方向: `!!! note` -> `> [!NOTE]`。

## 4. 数学公式规则

- 行内公式写法: `$expr$`，不要写 `$ expr $`。
- 块公式 `$$...$$` 前后留空行，避免和列表或段落粘连。
- 连续块公式之间加空行。
- 函数名在公式内建议使用 `\text{}` 包裹，例如：

```latex
$$f = \text{lerp}(a,b,t)$$
```

## 5. 常见兼容性修复

- 使用 `<br />`，不要裸 `<br>`。
- 比较表达中的 `<` 需要避免被当作 HTML 标签。
- 清理旧 Liquid 标签: `{% raw %}` / `{% endraw %}`。
- 旧 HTML 注释按需要转为 MDX 注释。

## 6. 导航注册

1. 查看分类:
```bash
python scripts/mintlify_helper.py list-cats
```
2. 添加页面:
```bash
python scripts/mintlify_helper.py add <文件路径> --tab "<Tab名称>" --group "<Group名称>"
```

## 7. 自动化检查与修复

单文件:
```bash
python scripts/mintlify_helper.py lint <文件路径> --fix
```

批量（PowerShell）:
```powershell
Get-ChildItem docs -Recurse -Filter *.md | ForEach-Object {
  python scripts/mintlify_helper.py lint $_.FullName --fix
}
```
