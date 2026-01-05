# 🐙 GitHub 工作流与 PR 最佳实践 (GitHub Flow & PR Guide)

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
