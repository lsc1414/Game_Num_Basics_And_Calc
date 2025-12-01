# 🏰 Project Vampirefall - 服务端与数值核心

[English Version](README.md) | [中文版本](README_CN.md)

欢迎来到 **Project Vampirefall** 的核心设计与计算仓库。
本项目是一款融合了 **塔防 (Tower Defense)**、**肉鸽 (Roguelike)** 和 **刷宝 (Looter)** 机制的混合品类游戏。

本目录是所有数学模型、设计哲学和技术标准的“单一真理来源” (Single Source of Truth)。

---

## 📚 文档导览 (Documentation Map)

### 1. 🧠 游戏设计 (The "Soul")
#### 核心机制
*   **[数值设计手册](Design/Numerical_Manual.md):** 数学的“圣经” (伤害公式、防御模型)。
*   **[战斗系统详解](Design/Mechanics/Combat_System.md):** 伤害类型、异常状态、韧性/硬直机制。
*   **[塔防建筑机制](Design/Mechanics/Tower_Defense_System.md):** 塔的分类、建造规则、人塔协同。
*   **[肉鸽强化系统](Design/Mechanics/Roguelike_Perks.md):** 局内成长、词条池、诅咒机制。

#### 系统与经济
*   **[装备与物品化](Design/Systems/Itemization.md):** 装备部位、词缀池结构、暗金设计。
*   **[掉落规则](Design/Systems/Loot_Table_Rules.md):** 掉落蓄水池、智能掉落、宝箱类型。
*   **[局外成长](Design/Systems/Meta_Progression.md):** 星盘天赋树、基地建设。

#### 内容与世界
*   **[怪物图鉴](Design/Content/Enemy_Bestiary.md):** 怪物分级、AI 行为模板、特殊词缀。
*   **[关卡设计](Design/Content/Level_Design_Guide.md):** 地图生成逻辑、波次节奏控制。

#### 理论基础
*   **[设计哲学](Design/Philosophy_And_Systems.md):** 核心循环、玩家心理模型。
*   **[案例分析](Design/Industry_CaseStudies.md):** 竞品分析 (PoE, Vampire Survivors)。

---

### 2. 🛠️ 技术架构 (The "Brain")
*   **[FSM 状态机设计](Tech/FSM_Design_Patterns.md):** 怪物 AI 逻辑、防御塔循环、代码实现模式。
*   **[移动端优化指南](Tech/Mobile_Optimization_Guide.md):** 发热控制、包体瘦身、海量单位渲染。
*   **[Luban 配表指南](Tech/Luban_Config_Guide.md):** ID 命名规范、枚举与多态应用。
*   **[存档系统](Tech/Save_System_Architecture.md):** 数据结构、序列化方案、反作弊。
*   **[性能预算](Tech/Performance_Budget.md):** CPU/GPU 限制、60FPS 优化标准。
*   **[输入系统](Tech/Input_System_Design.md):** 输入映射表、手柄支持、辅助功能。

---

### 3. 🎨 美术与表现 (The "Skin")
*   **[摄像机深度指南](Art/Camera_DeepDive_And_Settings.md):** FOV 原理、Clipping 精度、Cinemachine 调优。
*   **[Unity 画质指南](Art/Visual_Quality_Guide.md):** URP 设置、后处理、LOD 策略。
*   **[UI/UX 规范](Art/UI_UX_Guidelines.md):** 视觉风格、层级结构、交互反馈。
*   **[特效规范](Art/VFX_Standards.md):** 视觉分级、颜色编码、性能优化。
*   **[音频指南](Audio/Practical_Guide.md):** 声音分级、混音技巧、代码实现。

---

### 4. 📋 生产与规范 (The "Law")
*   **[文档路线图](Design/Documentation_Roadmap.md):** 所有文档的开发总纲。
*   **[目录结构规范](Unity_Standards/Folder_Structure.md):** Unity 工程组织结构。
*   **[资产命名规范](Unity_Standards/Asset_Naming.md):** 严格的命名约定 (`T_`, `M_`, `P_`)。
*   **[资产管理指南](Unity_Standards/Asset_Management.md):** 导入设置与最佳实践。
*   **[开发避坑指南](Dev_Guides/Production_Lessons.md):** 避免项目失败的经验教训。
*   **[Unity 实战技巧](Dev_Guides/Unity_Practical_Tips.md):** 编程与调试技巧。

---

## 🚀 快速开始

### 📊 可视化数学模型
我们提供了一个交互式的 HTML 仪表盘，用于模拟和验证数值模型。
1.  找到 `Design/Calculator/index.html`。
2.  使用任意现代浏览器打开它。

### 👮 执行标准
1.  将 `Unity_Standards/Tools/AssetNamingValidator.cs` 复制到 Unity 的 `Assets/Editor` 文件夹。
2.  它会自动标记任何违反命名规范的资产。

---

## 🤖 AI 上下文
*   **[GEMINI.md](GEMINI.md)**: 专为 AI 代理生成的项目上下文摘要。

---

*Project maintained by the Vampirefall Team.*