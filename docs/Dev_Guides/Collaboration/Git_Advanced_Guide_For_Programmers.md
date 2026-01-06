# 🐙 Git 极客生存指南：从命令行到私有云搭建

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