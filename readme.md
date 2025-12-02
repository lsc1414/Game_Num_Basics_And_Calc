# 🏰 Project Vampirefall - 服务端与数值核心

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
*   **[通用决策系统](Tech/Architecture/Unified_Decision_System.md):** 模块化、可配置的 AI/索敌逻辑，适用于多种游戏系统。
*   **[移动端优化指南](Tech/Mobile_Optimization_Guide.md):** TBDR 架构、Overdraw 控制、半精度运算。
*   **[Shader 核心数学](Tech/Shader_Math_Basics.md):** 点积/叉积应用、矩阵变换。
*   **[Luban 配表指南](Tech/Luban_Config_Guide.md):** ID 命名规范、枚举与多态应用。
*   **[存档系统](Tech/Save_System_Architecture.md):** 数据结构、序列化方案、反作弊。
*   **[性能预算](Tech/Performance_Budget.md):** CPU/GPU 限制、60FPS 优化标准。
*   **[输入系统](Tech/Input_System_Design.md):** 输入映射表、手柄支持、辅助功能。

---

### 3. 🎨 美术与表现 (The "Skin")
*   **[UI/UX 规范](Art/UI_UX_Guidelines.md):** 视觉风格、层级结构、交互反馈。
*   **[特效规范](Art/VFX_Standards.md):** 视觉分级、颜色编码、性能优化。
*   **[音频指南](Audio/Practical_Guide.md):** 声音分级、混音技巧、代码实现。
*   **[画质指南](Art/Visual_Quality_Guide.md):** URP 设置、光照烘焙、后处理策略。
*   **[摄像机指南](Art/Camera_DeepDive_And_Settings.md):** FOV、Cinemachine 调优、屏幕震动。

---

### 4. 🔧 深度实现与案例 (The "Muscle")
#### 技术实现
*   **[索敌机制详解](Tech/Mechanics/Targeting_System_DeepDive.md):** AI 与塔防高级索敌管道，包括评分维度与实战案例。
*   **[NavMesh寻路指南](Tech/Mechanics/NavMesh_Pathfinding_Guide.md):** 寻路、状态控制与动态障碍物的详细指南。
*   **[ECS 性能优化](Dev_Guides/Technical_Implementation/ECS_Performance_Optimization.md):** 基于 DOTS/JobSystem 处理 500+ 单位。
*   **[GPU Instancing](Dev_Guides/Technical_Implementation/GPU_Instancing_Guide.md):** 1个 DrawCall 渲染万级精灵。
*   **[掉落蓄水池算法](Dev_Guides/Technical_Implementation/Loot_Reservoir_Algorithm.md):** 恒定 DPM 的 0GC 掉落系统。
*   **[全局埋点指南](Dev_Guides/Technical_Implementation/Game_Analytics_Guide.md):** 遥测数据、漏斗模型、反作弊监控。
*   **[游戏开发最佳实践](Dev_Guides/Technical_Implementation/Game_Dev_Best_Practices.md):** ScriptableObject Tag、热重载、快速测试。
*   **[SO与Excel工作流对比](Dev_Guides/Technical_Implementation/ScriptableObject_vs_Excel_Workflow.md):** 自动化引用绑定、混合管线。
*   **[技能文本配置系统](Dev_Guides/Technical_Implementation/Skill_Text_Localization_System.md):** 富文本语义标签、动态参数注入。

#### 业界案例深度剖析
*   **[Kingdom Rush](Dev_Guides/Industry_Cases/Kingdom_Rush_Numerical_Model.md):** 四维数值平衡模型 (血量/速度/数量/时间)。
*   **[Hades](Dev_Guides/Industry_Cases/Hades_Build_Diversity.md):** 双层标签系统与双神祝福设计。
*   **[Vampire Survivors](Dev_Guides/Industry_Cases/Vampire_Survivors_Performance.md):** 性能优化秘籍 (经验宝石合并)。
*   **[Bloons TD6](Dev_Guides/Industry_Cases/Bloons_TD6_Damage_Matrix.md):** 伤害类型 vs 防御类型矩阵。
*   **[Cyberpunk 2077流式技术](Dev_Guides/Industry_Cases/Cyberpunk2077_Streaming_Tech.md):** 任务系统、异步资产解压。
*   **[Palworld 生产模式](Dev_Guides/Industry_Cases/Palworld_Production_Model.md):** Triple-I 自动化管线分析。

#### 失败案例复盘
*   **[Battleborn](Dev_Guides/Failure_Cases/Battleborn_Failure_Analysis.md):** 视觉噪声与 TTK 认知失调。
*   **[Paragon](Dev_Guides/Failure_Cases/Paragon_Complexity_Trap.md):** 策略游戏中的 Z 轴陷阱。
*   **[Anthem 生产危机](Dev_Guides/Failure_Cases/Anthem_Production_Crisis.md):** 引擎错配与预制作缺失。
*   **[Concord 市场分析](Dev_Guides/Failure_Cases/Concord_Market_Analysis.md):** Hero Shooter 红海竞争与角色设计问题。
*   **[The Day Before 营销陷阱](Dev_Guides/Failure_Cases/The_Day_Before_Marketing_Trap.md):** 资产翻模与法律风险。

---

### 5. 🤝 协作与生产 (The "Workflow")
*   **[独立团队 Scrum](Dev_Guides/Collaboration/Agile_For_Indie_Teams.md):** 轻量级敏捷开发指南。
*   **[远程协作](Dev_Guides/Collaboration/Remote_Collaboration.md):** 异步工作流与黄金时段。
*   **[里程碑规划](Dev_Guides/Collaboration/Milestone_Planning.md):** 垂直切片 -> Alpha -> Gold 路线图。
*   **[Beta 测试](Dev_Guides/Collaboration/Beta_Testing_Guide.md):** Steam Playtest 流程与反馈分级。

---

### 6. 🛠️ 工具与标准 (The "Law")
*   **[文档路线图](Design/Documentation_Roadmap.md):** 所有文档的开发总纲。
*   **[目录结构规范](Unity_Standards/Folder_Structure.md):** Unity 工程组织结构。
*   **[资产命名规范](Unity_Standards/Asset_Naming.md):** 严格的命名约定 (`T_`, `M_`, `P_`)。
*   **[资产管理指南](Unity_Standards/Asset_Management.md):** 导入设置与最佳实践。
*   **[Unity PRD 插件](Dev_Guides/Tools/Unity_PRD_Plugin.md):** 伪随机分布的 C# 实现。
*   **[AI 平衡测试](Dev_Guides/Tools/AI_Balance_Testing.md):** 利用 LLM 进行自动化数值验收。
*   **[战斗仿真系统](Dev_Guides/Tools/Combat_Simulation_System.md):** Python 无头战斗模拟器。
*   **[性能监控脚本](Dev_Guides/Tools/Performance_Monitoring_Scripts.md):** 运行时 FPS/内存 HUD。
*   **[数值计算器](Dev_Guides/Tools/Numerical_Calculator_Suite.md):** TTK、EHP 和经济模拟工具。

---

### 7. 📈 实时运营 (LiveOps)
*   **[通行证经济学](Design/LiveOps/Battle_Pass_Economy.md):** 40天周期、价值锚定策略。
*   **[活动排期策略](Design/LiveOps/Event_Cadence_Strategy.md):** 宏观/微观活动分层。

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