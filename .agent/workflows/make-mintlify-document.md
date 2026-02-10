---
description: 创建 Mintlify 风格的文档并自动配置导航
---

// turbo-all

# 📝 Workflow: Make Mintlify Document

这个工作流涵盖了从创建 Markdown 文档到自动化配置 docs.json 的全过程。

## 1. 准备工作

查看当前的目录结构和分类：

```bash
python scripts/mintlify_helper.py list-cats
```

## 2. 创建文档

在合适的目录下（通常是 `docs/` 下的子目录）创建一个新的 `.md` 文件。

> **推荐使用 `.md` 扩展名**：Mintlify 完全支持标准 Markdown，包括 GitHub Alerts、Mermaid 图表、表格等。只有在需要使用 Mintlify 的 React 组件（如 `<Card>`, `<Steps>`, `<Accordion>` 等）时，才使用 `.mdx` 扩展名。

### 📋 内容分类规则

**设计相关文档** (`Design/`, `Psychology/`, `Content/` 等):

- ✅ **重点**: 理论指南、设计哲学、最佳实践、心理学原理
- ✅ **案例**: 业界优秀案例分析、设计决策解读
- ✅ **可视化**: 图表、流程图、公式、对比表格
- ❌ **避免**: 大量代码实现、技术细节、API 参考
- 📝 **风格**: 深度分析为主,实现为辅

**技术/编码相关文档** (`Tech/`, `Architecture/`, `Tools/` 等):

- ✅ **重点**: 关键代码片段(精简)、技术架构、API 设计
- ✅ **代码**: 只提供核心逻辑和接口定义,避免完整实现
- ✅ **实践**: 使用示例、配置方法、工具使用
- ❌ **避免**: 过长的代码块(超过 30 行)、重复的样板代码
- 📝 **风格**: 简洁实用,点到即止

**Frontmatter 模板 (本仓库约定)**:

```markdown
---
sidebarTitle: "侧边栏标题 (可选)"
description: "简短的文档描述，用于 SEO 和预览"
icon: "emoji (可选，如 'rocket')"
---
```

规则:
- frontmatter 必须在文件最顶部。
- 本仓库默认不写 `title`，页面主标题统一使用正文 `# H1`（避免双标题）。

**内容模板 (Mintlify 风格)**:

```markdown
## 🌟 核心概念

使用二级标题开始你的内容。

> [!NOTE]
> 这是标准的 GitHub 风格提示块，Mintlify 完美支持。

> [!TIP]
> 使用提示块来强调技巧。

### 使用 Mintlify 组件（仅 .mdx 文件）

如果文件扩展名是 `.mdx`，你可以使用 Mintlify 的 React 组件：

<Card title="点击此处" icon="link" href="/docs/some/path">
  这是一个卡片组件示例。
</Card>

<Steps>
  <Step title="第一步">
    做这件事。
  </Step>
  <Step title="第二步">
    做那件事。
  </Step>
</Steps>

**常用组件**：`<Card>`, `<CardGroup>`, `<Steps>`, `<Step>`, `<Accordion>`, `<AccordionGroup>`

> 注意：`.md` 文件不支持这些组件，但支持 GitHub Alerts、Mermaid、表格等标准 Markdown 功能。
```

## 3. 标准化和修复

运行脚本自动修复格式（如转换旧的 Admonition 语法，修复数学公式）：

```bash
python scripts/mintlify_helper.py lint <文件路径> --fix
```

## 4. 注册到导航 (docs.json)

使用脚本将新通过添加到 `docs.json` 中。你需要指定 `Tab` (一级导航) 和 `Group` (二级分组)。

```bash
python scripts/mintlify_helper.py add <文件路径> --tab "<Tab名称>" --group "<Group名称>"
```

_示例_:
`python scripts/mintlify_helper.py add docs/Design/NewSystem.md --tab "🎮 设计" --group "核心系统"`

## 5. 验证

在本地启动 Mintlify 开发服务器查看效果（如果已安装）：

```bash
npx mintlify dev
```

或者提交更改后在 GitHub 上查看。
