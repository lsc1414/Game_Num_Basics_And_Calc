# 游戏开发 101 (Project Vampirefall)

> **"当《王国保卫战》遇见《流放之路》与《吸血鬼幸存者》"**
>
> 这是一个 **从立项到上线** 的实战生存指南。记录开发高品质 **混合品类 (Hybrid Genre)** 游戏的关键决策与标准。

---

## 🚀 快速接入 (Start Here)

| 入口 | 说明                         | 链接                                                   |
| :--: | :--------------------------- | :----------------------------------------------------- |
|  👶  | **我是新人** (Newcomer)      | 👉 **[点击进入新人向导 (Start Here)](START_HERE.md)**  |
|  🔍  | **交互式搜索** (Interactive) | 👉 **[点击进入交互式知识库 (index.html)](index.html)** |

---

## 💎 游戏三大支柱 (Core Pillars)

| 🛡️ 塔防 (The Bones)  | 🎲 肉鸽 (The Meat) | ⚔️ 刷宝 (The Soul)   |
| :------------------- | :----------------- | :------------------- |
| **确定性策略**       | **随机性变化**     | **长期积累**         |
| 地形、塔位、克制关系 | 词条构建、局内进化 | 暗金装备、Build 验证 |

---

## 📚 知识库目录 (Directory)

> _提示：推荐使用上方 **[交互式知识库](index.html)** 进行搜索和筛选。下方为完整文件列表。_

<details>
<summary><strong>📐 数值与公式 (Math & Mechanics)</strong></summary>

- 📐 **[数值设计手册](Design/Numerical_Manual.md):** 数学的“圣经”。
- 📐 **[通用数值速查表](Design/Mechanics/Unity_General_Numeric_Quick_Reference.md):** 移动速度、物理经验值。
- 📐 **[数值框架构建](Design/Numerical/Numerical_Framework_Methodology.md):** TTK、经济循环。
- 📐 **[难度曲线](Design/Mechanics/Difficulty_And_DDA_System.md):** DDA 动态难度。
- 📐 **[数值膨胀控制](Design/Systems/Power_Creep_Management.md):** 线性 vs 指数增长。
- 📐 **[经济模型](Design/Systems/Economy_And_Inflation_Model.md):** 资源产出消耗。
</details>

<details>
<summary><strong>⚔️ 战斗与机制 (Combat & Systems)</strong></summary>

- ⚔️ **[战斗系统详解](Design/Mechanics/Combat_System.md):** 伤害类型、韧性。
- ⚔️ **[塔防建筑机制](Design/Mechanics/Tower_Defense_System.md):** 建造规则、人塔协同。
- ⚔️ **[元素反应机制](Design/Mechanics/Elemental_Reaction_System.md):** 状态连携。
- ⚔️ **[肉鸽强化系统](Design/Mechanics/Roguelike_Perks.md):** 词条池、诅咒。
- ⚔️ **[仇恨系统](Design/Mechanics/Aggro_System.md):** 目标选择逻辑。
- ⚔️ **[物品化系统](Design/Systems/Itemization.md):** 装备与词缀结构。
- ⚔️ **[权衡词条库](Design/Systems/TradeOff_Affix_Library.md):** 100 个特色词条。
- ⚔️ **[弹道系统](Tech/Mechanics/Projectile_System_DeepDive.md):** 对象池与检测。
</details>

<details>
<summary><strong>🏗️ 架构与系统 (Architecture)</strong></summary>

- 🏗️ **[统一决策系统](Tech/Architecture/Unified_Decision_System.md):** 核心决策层设计。
- 🏗️ **[ECS 架构](Tech/Architecture/ECS_Theory_And_Practice.md):** 数据驱动设计。
- 🏗️ **[网络架构](Tech/Network_Architecture.md):** 状态同步。
- 🏗️ **[GAS 技能系统](Tech/Gameplay_Ability_System_Design.md):** 技能系统设计。
- 🏗️ **[存盘系统](Tech/Save_System_Architecture.md):** 持久化方案。
- 🏗️ **[C# 进阶优化](Tech/Optimization/Unity_Advanced_CSharp_Performance.md):** 堆栈、缓存与底层原理。
- 🏗️ **[代码反模式](Tech/Architecture/Unity_Anti_Patterns.md):** 单例/协程/Linq 避坑。
</details>

<details>
<summary><strong>🤖 AI 与算法 (Artificial Intelligence)</strong></summary>

- 🤖 **[AI 效用系统](Tech/AI_Utility_System.md):** Utility AI 评分。
- 🤖 **[Roguelike 随机](Tech/Algorithms/Roguelike_RNG_Systems.md):** 动态概率模型。
- 🤖 **[WFC 生成](Dev_Guides/Technical_Implementation/Procedural_Generation_WFC.md):** 波函数坍缩。
- 🤖 **[NavMesh 寻路](Tech/Mechanics/NavMesh_Pathfinding_Guide.md):** 动态避障。
- 🤖 **[掉落算法](Dev_Guides/Technical_Implementation/Loot_Reservoir_Algorithm.md):** 动态概率蓄水池。
</details>

<details>
<summary><strong>🎮 游戏设计 (Game Design)</strong></summary>

- 🎮 **[设计哲学](Design/Philosophy_And_Systems.md):** 玩家心理模型。
- 🎮 **[游戏心理学](Design/Game_Psychology_DeepDive.md):** 心流与爽点。
- 🎮 **[极简策略设计](Design/Minimalist_Strategy_Design_Knowledge.md):** 认知负荷管理。
- 🎮 **[怪物图鉴](Design/Content/Enemy_Bestiary.md):** AI 行为模板。
- 🎮 **[关卡设计](Design/Content/Level_Design_Guide.md):** 波次节奏。
- 🎮 **[叙事与包装](Design/Narrative/Game_Narrative_And_Presentation.md):** 环境叙事。
</details>

<details>
<summary><strong>📖 知识图谱 (Knowledge Maps)</strong></summary>

- 📖 **[杀戮尖塔图谱](Design/Roguelike_Deckbuilder_Knowledge_Map.md)**
- 📖 **[Risk of Rain 2 图谱](Design/Risk_of_Rain_2_Knowledge_Map.md)**
- 📖 **[吸血鬼幸存者性能](Dev_Guides/Industry_Cases/Vampire_Survivors_Performance.md)**
- 📖 **[Hades 构建多样性](Dev_Guides/Industry_Cases/Hades_Build_Diversity.md)**
- 📖 **以及更多竞品研究...**
</details>

<details>
<summary><strong>🎨 美术与音频 (Art & Audio)</strong></summary>

- 🎨 **[视觉质量指南](Art/Visual_Quality_Guide.md):** 风格统一性。
- 🎨 **[资源验证标准](Art/Tech_Art/Asset_Validation_Standards.md):** 性能红线。
- 🎨 **[特效优化](Art/VFX/VFX_Optimization_Guide.md):** Overdraw 杀手。
- 🎨 **[SpriteAtlas](Tech/Graphics/Unity_SpriteAtlas_DeepDive.md):** 图集优化。
- 🎵 **[音频实践](Audio/Practical_Guide.md):** 基础混音。
- 🎵 **[动态音乐](Audio/Adaptive_Music_System.md):** 自适应强度。
</details>

<details>
<summary><strong>🛠️ 工具与流程 (Tools)</strong></summary>

- 🛠️ **[调试指令](Dev_Guides/Tools/Debug_Console_And_Cheats.md):** GM 工具库。
- 🛠️ **[Luban 配置](Tech/Luban_Config_Guide.md):** 导表工作流。
- 🛠️ **[福尔摩斯调试](Dev_Guides/Debugging/Sherlock_Holmes_Debugging_Guide.md):** 内存侦探。
- 🛠️ **[AI 平衡测试](Dev_Guides/Tools/AI_Balance_Testing.md):** 自动化测试。
</details>

<details>
<summary><strong>🚀 发行与运营 (Production)</strong></summary>

- 🚀 **[上线生死清单](Dev_Guides/Publishing/Launch_Readiness_Checklist.md):** 发射前夜必查。
- 🚀 **[Steam 发行指南](Dev_Guides/Publishing/Steam_Unity_Indie_Game_Guide.md):** 流程闭环。
- 🚀 **[Steam 质量标准](Dev_Guides/Publishing/Steam_Unity_Quality_Standards.md):** 这里的下限是及格线，上限是神作线。
- 🚀 **[通行证经济](Design/LiveOps/Battle_Pass_Economy.md):** 周期设计。
- 🚀 **[社区危机公关](Dev_Guides/Community/Community_Crisis_Management.md):** 应对 SOP。
</details>

<details>
<summary><strong>📋 规范与标准 (Standards)</strong></summary>

- 📋 **[资源命名规范](Unity_Standards/Asset_Naming.md):** 全员必读。
- 📋 **[Git 提交规范](Dev_Guides/Collaboration/Git_Commit_Standards.md):** Commit Log 模板。
- 📋 **[Unity 标准目录](Unity_Standards/Folder_Structure.md):** 项目结构。
</details>

<details>
<summary><strong>💀 失败复盘 (Post-Mortems)</strong></summary>

- 💀 [Anthem](Dev_Guides/Failure_Cases/Anthem_Failure_Analysis.md)
- 💀 [Battleborn](Dev_Guides/Failure_Cases/Battleborn_Failure_Analysis.md)
- 💀 [Concord](Dev_Guides/Failure_Cases/Concord_Failure_Analysis.md)
</details>

---

## 🔗 其他链接

- **[AI 助手上下文 (GEMINI.md)](GEMINI.md)**

---

_Project maintained by the Vampirefall Team._
