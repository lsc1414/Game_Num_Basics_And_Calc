---
name: mintlify-markdown-kb
description: 为本仓库知识库创建、改写、批量修复 Markdown 文档并保证符合 Mintlify 规范。用户提到 Mintlify、docs.json、前言区(frontmatter)、文档导航注册、MkDocs 到 Mintlify 迁移、Admonition 语法转换、数学公式或 MD/MDX 兼容性修复时使用。
---

# Mintlify Markdown KB

将本仓库中的文档产出统一到 Mintlify 规范，优先复用现有脚本：`scripts/mintlify_helper.py`。

## 执行流程

1. 明确目标文件和输出类型
- 默认使用 `.md`。
- 仅在需要 Mintlify React 组件（如 `<Card>`、`<Steps>`）时使用 `.mdx`。

2. 生成或修正文档 frontmatter
- 统一包含：
  - `title`
  - `description`
- 按需添加：
  - `sidebarTitle`
  - `icon`
- 详细约束见 `references/mintlify-rules.md`。

3. 按 Mintlify 语法写作或迁移
- 将 MkDocs `!!!` 提示块改为 GitHub Alert 风格 `> [!NOTE]`。
- 保持数学公式与表格的可渲染格式。
- 修复常见 MDX 兼容问题（如 `<br />`、比较符 `<`）。
- 详细规则见 `references/mintlify-rules.md`。

4. 运行仓库脚本自动修复
- 单文件修复：
```bash
python scripts/mintlify_helper.py lint <文件路径> --fix
```
- 批量修复（PowerShell）：
```powershell
Get-ChildItem docs -Recurse -Filter *.md | ForEach-Object {
  python scripts/mintlify_helper.py lint $_.FullName --fix
}
```

5. 注册导航到 `docs.json`
- 先查看可用分类：
```bash
python scripts/mintlify_helper.py list-cats
```
- 再添加导航：
```bash
python scripts/mintlify_helper.py add <文件路径> --tab "<Tab名称>" --group "<Group名称>"
```

6. 验收并汇报
- 检查文档是否包含 frontmatter。
- 检查是否仍残留 `!!!` 语法或不合法链接格式。
- 汇报变更文件、执行命令、残留问题和建议下一步。

## 参考资料加载规则

- 先读 `references/mintlify-rules.md` 获取格式约束。
- 若用户要求“按项目既有流程”，再参考：
  - `.agent/workflows/make-mintlify-document.md`
  - `.agent/workflows/make-document.md`
- 仅在需要导航操作时读取 `docs.json` 与 `scripts/mintlify_helper.py`。

## 输出要求

- 始终给出可直接执行的命令。
- 始终标注改动的文件路径。
- 若存在无法自动修复项，明确列出阻塞点与手工处理建议。
