# 🏰 Project Vampirefall - 服务端与数值核心

[English Version](README.md) | [中文版本](README_CN.md)

欢迎来到 **Project Vampirefall** 的核心设计与计算仓库。
本项目是一款融合了 **塔防 (Tower Defense)**、**肉鸽 (Roguelike)** 和 **刷宝 (Looter)** 机制的混合品类游戏，设计灵感来源于《流放之路 (Path of Exile)》、《吸血鬼幸存者 (Vampire Survivors)》和《GemCraft》。

本目录作为项目的“大脑”，包含了驱动游戏平衡与架构的数学模型、设计哲学以及技术标准。

---

## 📚 文档导览 (Documentation Map)

### 1. 🧠 设计与数学 (The "Why" & "How")
*   **[数值设计手册](Numerical_Design_Manual.md)** (原 readme 重命名)
    *   **这是什么？** 游戏数学的“圣经”。
    *   **内容包含：** 伤害公式、PRD 算法、护甲 vs 闪避曲线、掉落蓄水池逻辑。
    *   **目标读者：** 数值策划、玩法程序。

*   **[游戏设计哲学](GameDesign_Philosophy_And_Systems.md)**
    *   **这是什么？** 关于“好玩”的理论。
    *   **内容包含：** 核心循环、协同效应 (1+1>2)、节奏控制、玩家心理画像。
    *   **目标读者：** 所有策划。

*   **[业界案例分析](IndustryCaseStudies.md)**
    *   **这是什么？** 顶尖游戏（暗黑、原神、星际战甲）的机制库。
    *   **内容包含：** 分析特定机制为什么好玩，以及如何将其适配到我们的游戏中。

### 2. 🛠️ 技术落地 (The "Code")
*   **[Unity 开发实战锦囊](Unity_Practical_Dev_Tips.md)**
    *   **内容包含：** 性能优化（对象池、合批）、架构设计（事件总线、SO）、调试技巧。
    *   **目标读者：** 客户端程序。

*   **[Unity 资产管理指南](Unity_Asset_Management_Tips.md)**
    *   **内容包含：** 导入设置、Addressables vs Resources、Git LFS 处理。
    *   **目标读者：** 技术美术 (TA)、程序。

*   **[资产命名规范](AssetNaming_Standards.md)**
    *   **内容包含：** 严格的命名约定（`T_`, `M_`, `P_`），保持项目整洁。
    *   **配套工具：** 包含 `AssetNamingValidator.cs` 脚本的链接。

*   **[文件夹结构规范](Unity_Folder_Structure_Standards.md)**
    *   **内容包含：** 推荐使用“混合式”结构 (`Features/` vs `Art/`) 进行模块化开发。

### 3. ☠️ 开发生存指南
*   **[游戏开发血泪史](GameDev_Production_Lessons.md)**
    *   **内容包含：** 关于范围蔓延 (Scope Creep)、本地化、UI/UX 和市场宣发的惨痛教训。**立项前必读，防止项目暴死。**

---

## 🚀 快速开始 (Quick Start)

### 📊 可视化数学模型
我们提供了一个交互式的 HTML 仪表盘，用于模拟和验证数值模型，无需编写代码。
1.  找到本目录下的 **`index.html`** 文件。
2.  使用任意现代浏览器 (Chrome/Edge) 打开它。
3.  你可以用它计算：
    *   **DPS 期望：** 观察 `Inc` (加法) 与 `More` (乘法) 对输出的影响。
    *   **防御曲线：** 可视化对比 线性护甲收益 vs 指数级闪避收益。
    *   **PRD 稳定性：** 对比真随机与伪随机的方差。

### 👮 执行标准
为了确保项目整洁：
1.  将 `AssetNamingValidator.cs` 复制到你 Unity 项目的 `Assets/Editor` 文件夹中。
2.  它会自动标记任何违反 `AssetNaming_Standards.md` 中定义的命名规范的资产。

---

## 🤖 AI 上下文
*   **[GEMINI.md](GEMINI.md)**: 该文件专为 AI 代理生成，帮助 AI 快速理解项目上下文。它总结了目录结构和关键文件内容。

---

*Project maintained by the Vampirefall Team.*
