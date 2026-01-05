---
description: 自动总结更改并提交到 GitHub (Add, Commit, Push)
---

这个工作流用于自动化 Git 提交过程，包括自动总结更改内容、提交和推送。

### 执行步骤：

1. **查看并暂存更改**：
   // turbo
   先确认当前分支状态，然后将所有变更加入暂存区。

   - `git status`
   - `git add -A`

2. **分析变更内容**：

   - 运行 `git diff --cached` 获取当前暂存区的详细差异。
   - **核心逻辑**：AI 需仔细阅读 `diff` 内容，识别出修改的功能、修复的错误或更新的文档。

3. **生成 Commit Message**：

   - 基于第 2 步的分析，生成一个符合规范的 Commit Message。
   - 格式建议：`<type>(<scope>): <subject>`（例如 `docs(arch): 更新统一决策系统文档`）。
   - 如果更改较多，可以增加详细的 Body 部分。

4. **执行本地提交**：
   // turbo
   使用生成的 Message 执行提交。

   - `git commit -m "<生成的消息>"`

5. **推送至远程仓库**：
   // turbo
   将代码推送至当前的 origin 分支。

   - `git push`

6. **结果汇报**：
   - 汇报提交的消息内容。
   - 确认推送是否成功。
