# 🐙 Git 版本管理与 Commit Log 规范 (Git Standards)

> **核心理念**: **Commit Log 是写给人看的，不是写给机器看的。**
> 一个好的 Commit Log 应该能回答三个问题：
> 1.  **改了什么？** (What)
> 2.  **为什么改？** (Why)
> 3.  **怎么改的？** (How - 可选，如果是复杂逻辑)

## 1. Commit Message 格式规范

采用业界标准的 **Angular Commit Convention**，结构如下：

```text
<type>(<scope>): <subject>

<body>

<footer>
```

### 1.1 Type (必填)
用一个词描述改动的性质：
*   **feat**: 新功能 (Feature)。
*   **fix**: 修补 Bug。
*   **docs**: 仅修改了文档 (如 README)。
*   **style**: 格式修改 (不影响代码运行的变动，如空格、缩进)。
*   **refactor**: 重构 (即不是新增功能，也不是修改 bug 的代码变动)。
*   **perf**: 性能优化。
*   **test**: 增加测试或修改测试。
*   **chore**: 构建过程或辅助工具的变动 (如 .gitignore, package.json)。
*   **art**: 美术资源提交 (贴图、模型、预制体)。

### 1.2 Scope (选填)
用括号说明影响的范围 (模块/功能)：
*   `feat(Tower)`: 塔防模块。
*   `fix(UI)`: 界面模块。
*   `art(VFX)`: 特效资源。

### 1.3 Subject (必填)
简短的描述，不超过 50 个字符。
*   **原则**: 动词开头，使用祈使句。
*   *Good*: "Add double jump mechanic" (添加二段跳机制)
*   *Bad*: "Fixed some bugs" (修了一些bug -> **修了啥？？**)

### 1.4 Body (选填，但推荐)
详细描述。
*   解释**为什么**要做这个修改？
*   解释**之前**是怎么样的，**现在**是怎么样的？
*   如果是修复 Bug，描述**复现步骤**或**根因**。

### 1.5 Footer (选填)
*   关联的 Issue 或任务 ID。
*   `Closes #123`
*   `BREAKING CHANGE`: 如果有破坏性更新（如改了存档格式），必须大写注明！

## 2. 📝 标准 Commit Log Demo (抄作业区)

请团队成员直接复制以下模板修改。

### 场景 A: 修复了一个 Bug
```text
fix(Combat): 修复箭塔攻速过快导致伤害丢失的问题

原因: 
之前的攻击冷却计时器使用 Time.deltaTime 累加，在低帧率下会有浮点误差。

修改:
改用 Time.time 时间戳进行冷却判定。

Closes #405
```

### 场景 B: 开发了一个新功能
```text
feat(Roguelike): 新增天赋 "火焰精通"

效果:
所有造成物理伤害的防御塔，现在有 30% 概率附加点燃效果。

技术细节:
1. 在 DamageCalculator 中新增了 ElementCheck 逻辑。
2. 新增了 Buff_Ignite 脚本。
```

### 场景 C: 提交美术资源
```text
art(Enemy): 提交 Level 3 精英怪 "石头人" 资源

包含:
1. 模型: Golem_L3.fbx (带 LOD)
2. 贴图: T_Golem_D/N/M_01.png (ASTC 压缩)
3. 动画: Anim_Golem_Walk/Attack/Die

注意:
材质球使用了新的 Toon Shader，请程序确认是否支持 GPU Instancing。
```

### 场景 D: 性能优化
```text
perf(Pathfinding): 优化大量单位寻路时的 CPU 占用

之前使用 NavMeshAgent.SetDestination 每帧调用，导致主线程卡顿。
现在改为每 10 帧 (0.2s) 更新一次路径，并启用了 Job System 进行距离计算。

性能提升:
同屏 500 单位时，Update 耗时从 8ms 降至 1.5ms。
```

## 3. 分支管理策略 (Branching Strategy)

### 3.1 分支命名
*   **master / main**: 随时可发布的稳定版本。**绝对禁止直接 Push**。
*   **develop**: 开发主分支。所有 Feature 分支合入这里。
*   **feat/xxx**: 功能分支。如 `feat/login_system`。
*   **fix/xxx**: 修复分支。如 `fix/crash_on_start`。
*   **art/xxx**: 美术资源分支。

### 3.2 工作流 (Workflow)
1.  接到任务 "开发登录系统"。
2.  基于 `develop` 切出 `feat/login`。
3.  开发... 提交... (多次 Commit)。
4.  开发完毕，推送到远程。
5.  发起 **Pull Request (PR)** 合入 `develop`。
6.  **Code Review**: 同事检查代码，确认无误后 Approve。
7.  合并。

## 4. 工具强制约束 (Enforcement)

为了防止人为偷懒，建议部署 **Git Hooks**。

### 4.1 commit-msg Hook
在 `.git/hooks/commit-msg` 中添加脚本，使用正则表达式检查 Commit Message 格式。如果不符合 `<type>(<scope>): <subject>` 格式，直接拒绝提交。

### 4.2 pre-commit Hook
在提交前自动运行：
*   代码格式化 (CSharpier / Format)。
*   简单的静态检查 (如有无带 `Debug.Log` 的代码)。

---

**最后通牒**: 
"Update", "Fix bug", "Backup", "..." 这种 Commit Message 一经发现，**请请全组喝奶茶**。

---

## 📚 扩展阅读与参考标准 (References)

### 🌍 行业标准
*   **[Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/)**
    *   本文档基于此规范。它是目前最流行的 Commit Message 标准，被 Angular, React, Electron 等数万个开源项目采用。
*   **[Semantic Versioning 2.0.0](https://semver.org/)** (语义化版本控制)
    *   解释了为什么 `BREAKING CHANGE` 会导致大版本号 +1 (v1.0.0 -> v2.0.0)。

### 🔧 自动化工具
*   **[Husky](https://github.com/typicode/husky)**
    *   最流行的 Git Hooks 工具。可以用它在 `git commit` 之前自动运行 Lint 检查。
*   **[Commitlint](https://github.com/conventional-changelog/commitlint)**
    *   一个命令行工具，用来检查 Commit Message 是否符合 Conventional Commits 规范。建议集成到 CI/CD 流程中。

### 📖 深度文章
*   **[How to Write a Git Commit Message](https://cbea.ms/git-commit/)** (Chris Beams)
    *   这篇博客被无数人引用，详细解释了“为什么要用祈使句”、“为什么首行不能超过50个字符”。
