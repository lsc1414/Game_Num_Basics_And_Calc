# Git 指南综合指南

> 本文档由以下文件合并生成 (2026-01-09)



---


<!-- 来源: Dev_Guides\Collaboration\Git_Advanced_Guide_For_Programmers.md -->

## 🐙 Git 极客生存指南：从命令行到私有云搭建

> **面向对象**: 程序员 (Programmers)。
> **目标**: 掌握 Git 的“黑魔法”，处理复杂的分支管理、冲突解决，并学会搭建团队的私有代码仓库。

## 1. 常用命令速查 (The Cheat Sheet)

### 1.1 基础操作
```bash
git init                    # 初始化仓库
git clone <url>             # 克隆远程仓库
git status                  # 查看当前状态 (必用!)
git add .                   # 添加所有修改到暂存区
git commit -m "feat: xxx"   # 提交
git pull                    # 拉取更新 (相当于 fetch + merge)
git push                    # 推送修改
```

### 1.2 分支操作 (Branching)
```bash
git branch                  # 列出本地分支
git branch -a               # 列出所有分支 (含远程)
git checkout -b feature/A   # 创建并切换到 feature/A 分支
git checkout develop        # 切换回 develop
git merge feature/A         # 把 feature/A 合并进当前分支
git branch -d feature/A     # 删除分支
```

### 1.3 后悔药 (Undo)
```bash
git checkout -- file.cs     # 丢弃工作区的修改 (还没 add)
git reset HEAD file.cs      # 把暂存区的修改撤回工作区 (add 了但没 commit)
git reset --soft HEAD^      # 撤销最近一次 commit (代码保留在暂存区)
git reset --hard HEAD^      # 彻底回退到上个版本 (代码全部丢弃，慎用!)
git commit --amend          # 修改最近一次 commit 的注释
```

### 1.4 暂存现场 (Stash)
当你正在修 Bug，突然老板让你切分支去改另一个紧急 Bug：
```bash
git stash                   # 把当前未提交的修改“藏”起来
git checkout hotfix/001     # 切分支去修 Bug...
# ... 修完回来 ...
git checkout develop
git stash pop               # 把“藏”起来的代码还原回来
```

## 2. 进阶技巧 (Advanced Skills)

### 2.1 Rebase (变基) vs Merge
*   **Merge**: 保留真实的历史记录，会有 "Merge branch 'xxx'" 的提交。适合公共分支合并。
*   **Rebase**: 把你的提交“接”在目标分支的最新提交后面。历史记录是一条直线，非常干净。
    *   `git pull --rebase`: 拉取代码时自动变基 (推荐配置)。
    *   `git rebase develop`: 在 feature 分支上，把 develop 的最新代码垫在下面。

### 2.2 Cherry-pick (摘樱桃)
只想要某个分支里的**某一次**提交，而不是整个分支？
```bash
git log                     # 找到那个 commit 的 hash (例如 a1b2c3d)
git cherry-pick a1b2c3d     # 把这个 commit 复制到当前分支
```

### 2.3 解决冲突 (Conflict Resolution)

#### A. 文本文件冲突
1.  **定位**: 打开冲突文件，找到 `<<<<<<<`, `=======`, `>>>>>>>` 标记。
2.  **修改**: 决定保留哪部分代码（或者都保留），删除标记符号。

3.  **提交**: `git add` + `git commit`。

#### B. 二进制文件冲突 (Binary Conflict) - **关键！**
图片、模型、DLL 无法合并内容，必须**二选一**。

**命令行方案**:

*   **保留我的 (Mine)**: 我改了图，我要覆盖服务器的。
    ```bash
    git checkout --ours path/to/image.png
    git add path/to/image.png
    ```

*   **保留他的 (Theirs)**: 别人的图是对的，我放弃我的修改。
    ```bash
    git checkout --theirs path/to/image.png
    git add path/to/image.png
    ```

*   注意：在 `git merge` 时，`--ours` 是指当前分支，`--theirs` 是指要合并进来的分支。但在 `git rebase` 时，逻辑是反的！务必先备份。

**GUI 方案 (Sourcetree / TortoiseGit)**:

1.  在冲突文件上右键。
2.  选择 `Resolve using 'Mine'` (使用我的版本) 或 `Resolve using 'Theirs'` (使用远程版本)。

3.  工具会自动执行上述命令并标记为已解决。

**终极方案: 锁定 (Locking)**
为了避免二进制冲突，最好的办法是**不要让冲突发生**。

*   使用 LFS 的锁定功能: `git lfs lock image.png`。
*   这样当你在修改时，别人无法推送这个文件，直到你 `unlock`。

## 3. 搭建私有 Git 服务器 (Self-Hosted Git)

对于不想把代码放在 GitHub/Gitee 的团队，推荐搭建 **Gitea** (轻量级) 或 **GitLab** (功能全)。

### 3.1 方案 A: Gitea (推荐，极轻量)
适合小团队，一个二进制文件搞定，内存占用极低。

**搭建步骤 (Windows/Linux)**:

1.  **下载**: 去 [Gitea 官网](https://gitea.io) 下载对应系统的可执行文件。
2.  **运行**: 直接双击运行 (会启动 Web 服务器，默认端口 3000)。

3.  **配置**: 浏览器访问 `localhost:3000`，首次运行会进入安装向导。

    *   数据库选 `SQLite3` (最简单，无需安装 MySQL)。
    *   设置管理员账号。
4.  **局域网访问**: 确保防火墙开放 3000 端口。队友可以通过 `http://192.168.x.x:3000` 访问。

### 3.2 方案 B: 局域网裸仓库 (Bare Repo)
最原始的方法，不需要任何 Web 界面。

1.  **服务器端 (找台电脑做主机)**:
    ```bash
    mkdir vampirefall.git
    cd vampirefall.git
    git init --bare  # 初始化裸仓库 (没有工作区，只有数据库)
    ```

2.  **共享**: 将 `vampirefall.git` 文件夹设置为**网络共享文件夹** (Windows SMB)。

3.  **客户端**:
    ```bash
    git clone //SERVER_IP/Shared/vampirefall.git
    ```

## 4. Unity 项目的 .gitignore (必抄)

```gitignore
# Unity folders
/[Ll]ibrary/
/[Tt]emp/
/[Oo]bj/
/[Bb]uild/
/[Bb]uilds/
/[Ll]ogs/
/[Mm]emoryCaptures/

# Visual Studio / JetBrains
.vs/
.idea/
*.sln
*.csproj
*.unityproj

# OS
.DS_Store
Thumbs.db
```

## 5. LFS 配置 (大文件存储)

对于大于 100MB 的文件 (PSD, FBX)，必须用 LFS。

1.  **安装**: `git lfs install`
2.  **配置**:
    ```bash
    git lfs track "*.psd"
    git lfs track "*.fbx"
    git lfs track "*.wav"
    ```

3.  **提交**: 这会生成一个 `.gitattributes` 文件，务必把它提交上去。

---

**一句话忠告**: 
**永远不要在主分支 (master/develop) 上直接写代码。**
**Commit 早，Commit 勤。**



---


<!-- 来源: Dev_Guides\Collaboration\Git_Commit_Standards.md -->

## 🐙 Git 版本管理与 Commit Log 规范 (Git Standards)

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




---


<!-- 来源: Dev_Guides\Collaboration\GitHub_PR_Workflow.md -->

## 🐙 GitHub 工作流与 PR 最佳实践 (GitHub Flow & PR Guide)

> **核心理念**: **主分支 (main/develop) 是神圣不可侵犯的**。任何代码想要进入主分支，必须经过至少一双眼睛的检查 (Code Review)。这个过程就叫 **Pull Request (PR)**。

## 1. 标准工作流 (The Flow)

### 1.1 Fork vs Branch
*   **开源模式 (Fork)**: 你没有原仓库的写权限。你把仓库 `Fork` 到你自己名下，改完后向原仓库发起 PR。
*   **团队模式 (Branch)**: 你有写权限。你直接在原仓库里切一个 `feature/xxx` 分支，改完后向 `develop` 发起 PR。
*   **Vampirefall 推荐**: **团队模式**。效率更高。

### 1.2 完整生命周期
1.  **新建分支**: 基于最新 `develop` 创建 `feat/tower_fire`。
2.  **提交代码**: 在 `feat/tower_fire` 上 commit。

3.  **发起 PR**: 在 GitHub/Gitea 网页上点击 "New Pull Request"。

    *   *Source*: `feat/tower_fire`
    *   *Target*: `develop`
4.  **Code Review**: 你的同事收到通知，进来检查代码，写评论。

5.  **修改反馈**: 根据同事的建议，继续在 `feat/tower_fire` 上提交修改。

6.  **合并 (Merge)**: 同事点赞 (Approve) 后，点击 "Squash and Merge"。

7.  **删除分支**: 完事后删掉 `feat/tower_fire`。

## 2. 如何写一个优秀的 PR 描述？

PR 的描述决定了 Reviewer 的心情和审核速度。

### 2.1 标题 (Title)
*   格式: `<Type>: <Subject>` (同 Commit Message)
*   例子: `feat: 实现火焰塔的燃烧逻辑`

### 2.2 模板 (Template)
建议在仓库根目录建一个 `.github/PULL_REQUEST_TEMPLATE.md`，内容如下：

```markdown
## 📝 改动摘要
实现了火焰塔的基础逻辑，包括 DoT 伤害和视觉特效。

## 📸 截图/GIF (选填)
[这里放一张火焰塔攻击怪物的 GIF，胜过千言万语]

## 🔗 关联 Issue
Closes #102

## ✅ 自测清单
- [x] 塔能正常攻击
- [x] 燃烧伤害数值正确
- [x] 怪物死亡后特效消失
- [x] 没有产生 GC Alloc
```

## 3. Code Review 礼仪与标准

### 3.1 Reviewer (审核者) 的职责
*   **看逻辑**: 代码是否实现了需求？有没有明显的 Bug？
*   **看规范**: 变量名是否规范？有没有写注释？
*   **看性能**: 有没有在 Update 里 `new List`？有没有死循环风险？
*   **语气**: **对事不对人**。
    *   *Bad*: "你这代码写得太烂了。"
    *   *Good*: "这里可能会产生 GC，建议改用对象池。"

### 3.2 Submitter (提交者) 的心态
*   **不要玻璃心**: 别人指出的问题是为了项目好，不是针对你。
*   **解释**: 如果你不认同 Reviewer 的意见，请在评论里解释你的理由，或者线下沟通。
*   **及时响应**: 别发了 PR 就不管了，别人提了意见赶紧改。

## 4. Merge 策略：Squash vs Merge

点击 Merge 按钮时，有三种选项：

### 4.1 Create a merge commit (普通合并)
*   保留所有历史记录。如果你的分支上有 100 个 "fix typo" 的垃圾提交，它们都会进入主分支。
*   **评价**: ❌ **脏**。不推荐。

### 4.2 Squash and merge (压缩合并) - **推荐**
*   把你分支上的 100 个提交**压缩成 1 个**提交，合入主分支。
*   **评价**: ✅ **干净**。主分支的历史记录非常清晰，一个功能对应一个 Commit。

### 4.3 Rebase and merge (变基合并)
*   把你的提交直接接到主分支后面，像从来没分叉过一样。
*   **评价**: ⚠️ **高风险**。如果不仅保留了垃圾提交，还没有 Merge 节点，出问题很难回退。

## 5. 常见问题

*   **PR 冲突了怎么办？**: 
    *   在本地 `git pull origin develop` (把主分支最新代码拉下来)。
    *   本地解冲突。
    *   `git push` 更新你的 PR 分支。GitHub 会自动更新状态。
*   **PR 太大了怎么办？**: 
    *   如果一个 PR 改了 50 个文件，没人愿意看。
    *   **拆分**: 先提一个 `feat/tower_base` (只有基类)，合入后再提 `feat/tower_fire`。

---

**一句话总结**: 
**PR 是代码质量的守门员。**
**没有 Review 的代码，就是埋在项目里的雷。**




---


<!-- 来源: Dev_Guides\Collaboration\SVN_vs_Git_Migration_Guide.md -->

## 🐢 SVN vs 🐙 Git：深度对比与极简上手指南

> **写在前面**: 很多团队（尤其是美术同学）习惯了 SVN 的“直观”，对 Git 感到恐惧。其实 Git 并没有那么难，只是逻辑变了。
> **核心区别**: **SVN 是集中式的 (服务器坏了大家都得停工)，Git 是分布式的 (每个人电脑里都有一份完整的版本库)。**

## 1. 深度对比分析 (Analysis)

### 1.1 为什么美术喜欢 SVN？
*   **文件锁定 (Locking)**: SVN 可以在你编辑 `Hero.psd` 时“锁住”它，别人就不能改了。这对二进制文件（图片、模型）至关重要，防止冲突。Git 默认没有锁（需要 LFS 插件）。
*   **局部检出**: SVN 可以只下载项目的 `Art/Characters` 文件夹。Git 必须把整个仓库（包括你不关心的代码和文档）全拉下来。
*   **权限控制**: SVN 可以精确控制“美术只能读写 Art 目录，不能碰 Code 目录”。Git 通常是仓库级别的权限（要么都能读写，要么都不能）。

### 1.2 为什么程序喜欢 Git？
*   **分支 (Branching)**: Git 切分支是秒级的。每个功能一个分支，互不影响。SVN 切分支很重，而且合并代码简直是噩梦。
*   **离线工作**: Git 可以在没网的时候提交代码（Commit 到本地），等有网了再推送到服务器。SVN 没网就废了。
*   **安全性**: Git 每个人的电脑里都有完整备份。服务器炸了，随便找台电脑就能恢复。SVN 服务器炸了且没备份，项目就没了。

### 1.3 结论：Vampirefall 该选谁？
*   **代码/配置**: **必须用 Git**。分支管理和合并是多人协作的刚需。
*   **美术大资源 (PSD/MAX)**: 
    *   方案 A: 继续用 SVN 管理源文件，导出后的资源 (FBX/PNG) 进 Git。
    *   方案 B: 全面转 Git，但必须开启 **Git LFS (Large File Storage)** 并配置文件锁。

---

## 2. 🐙 Git 极简上手指南 (美术/策划专用版)

**忘掉命令行！** 我们推荐使用 **Sourcetree** 或 **GitHub Desktop** 或 **TortoiseGit** (小乌龟，长得跟 SVN 很像)。

### 2.1 核心概念对应表 (SVN -> Git)

|          你在 SVN 做的操作          |          在 Git 里的对应操作          |          区别          |
|          :---          |          :---          |          :---          |
|          **Update** (更新)          |          **Pull** (拉取)          |          没区别，都是把服务器的东西拉下来。          |
|          **Commit** (提交)          |          **Commit** (提交) + **Push** (推送)          |          **这是最大的坑！** <br>SVN 提交就完事了。<br>Git 提交只是存到**你自己电脑**里，必须再点一下 **Push** 才能传到服务器给别人看。          |
|          **Revert** (还原)          |          **Discard** / **Reset**          |          放弃修改，还原到上次提交的状态。          |
|          **Lock** (锁定)          |          **LFS Lock**          |          需要专门配置 LFS 才能用。          |

### 2.2 傻瓜式工作流 (Daily Workflow)

假设你使用 **TortoiseGit** (因为它和 SVN 操作最像)：

#### 第一步：早上开工 (Pull)
1.  在项目文件夹上右键 -> `TortoiseGit` -> `Pull`。
2.  点 `OK`。

3.  **目的**: 确保你拿到的是最新版本，防止和别人冲突。

#### 第二步：干活 (Work)
*   改 Excel，画图，改场景... 随便弄。

#### 第三步：下班提交 (Commit + Push)
1.  右键 -> `Git Commit -> "master"`。
2.  **勾选**你修改的文件。

3.  在 Message 框里写：`art: 修改了吸血鬼主角的模型贴图`。

4.  点击 `Commit`。

5.  **关键动作**: 此时弹窗左下角会有一个 `Push` 按钮，**一定要点一下！** (或者 Commit 完单独右键 -> `Push`)。

6.  **目的**: 只有 Push 成功了，你的东西才算真正提交了。

### 2.3 遇到冲突怎么办？ (Conflict)
*   **现象**: Push 失败，提示 `Updates were rejected`。
*   **原因**: 你改了 `Data.xlsx`，小王也改了 `Data.xlsx`，而且他比你先 Push。
*   **解决**:
    1.  先点 `Pull`。Git 会试图合并。
    2.  如果合并失败，文件上会有个感叹号。

    3.  **策划/美术**: 别慌！直接找程序帮忙，或者**备份你的文件**，还原 (Revert)，拉取最新 (Pull)，再把你的改动覆盖上去。

    4.  **程序**: 使用 Merge Tool 解决冲突。

## 3. 🚀 给主程的建议：如何平滑迁移？

1.  **保留 SVN 习惯**: 给美术装 **TortoiseGit**，因为右键菜单的操作习惯和 SVN 几乎一样，学习成本最低。
2.  **忽略文件配置 (.gitignore)**:

    *   务必把 `Library/`, `Temp/`, `Logs/`, `.vs/` 屏蔽掉。SVN 以前可能把这些垃圾都传上去了，Git 绝对不行。
3.  **LFS 强制开启**:

    *   配置 `.gitattributes`，把 `*.psd`, `*.fbx`, `*.png`, `*.wav` 全部走 LFS。否则 1个月后你的 Git 仓库会大到拉不下来。

---

**一句话总结**: 
**Git = SVN + "本地仓库"**。
以前是 `写完 -> 上传`。
现在是 `写完 -> 存本地 (Commit) -> 上传 (Push)`。
多了一步，但更安全。


