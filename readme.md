# 🧛 Project Vampirefall
> **"当《王国保卫战》遇见《流放之路》与《吸血鬼幸存者》"**
> 一个融合了 **塔防策略 (TD)**、**Roguelike 变数** 与 **刷宝驱动 (Loot)** 的海量同屏动作塔防游戏。

---

## 🚀 快速接入 (Start Here)

**我是...**

### 🧠 新人策划 (Designer)
1.  **搞懂咱们玩什么**: 阅读 **[设计哲学](Design/Philosophy_And_Systems.md)**，理解核心循环。
2.  **搞懂数值怎么填**: 查阅 **[数值设计手册](Design/Numerical_Manual.md)**，这是我们的数学圣经。
3.  **搞懂关卡怎么摆**: 学习 **[关卡设计理论](Design/Content/Level_Design_Theory.md)**。

### 💻 新人程序 (Programmer)
1.  **绝对红线**: 熟读 **[全员速查表](Dev_Guides/Project_Cheat_Sheet.md)**，别犯低级错误。
2.  **核心架构**: 理解 **[统一决策系统](Tech/Architecture/Unified_Decision_System.md)** (AI/塔/弹道)。
3.  **调试工具**: 学会使用 **[调试指令与GM工具](Dev_Guides/Tools/Debug_Console_And_Cheats.md)** 提高效率。

### 🎨 新人美术 (Artist)
1.  **画风对齐**: 阅读 **[视觉质量指南](Art/Visual_Quality_Guide.md)**。
2.  **乱而不杂**: 学习 **[视觉层级与混乱管理](Art/Visual_Hierarchy_In_Chaos.md)**，防止光污染。
3.  **资源规范**: 遵守 **[资源命名规范](Unity_Standards/Asset_Naming.md)**。

---

## 💎 游戏三大支柱 (Core Pillars)

| 🛡️ 塔防 (The Bones) | 🎲 肉鸽 (The Meat) | ⚔️ 刷宝 (The Soul) |
| :--- | :--- | :--- |
| **确定性策略** | **随机性变化** | **长期积累** |
| 地形、塔位、克制关系 | 词条构建、局内进化 | 暗金装备、Build验证 |
| *参考: Kingdom Rush* | *参考: Loop Hero* | *参考: Path of Exile* |

---

## 📚 完整知识库 (The Codex)

<details>
<summary><strong>📂 点击展开：1. 游戏设计 (Design)</strong></summary>

### ⚔️ 核心机制 (Core Mechanics)
*   **[数值设计手册](Design/Numerical_Manual.md):** 数学的“圣经”。
*   **[战斗系统详解](Design/Mechanics/Combat_System.md):** 伤害类型、韧性机制。
*   **[塔防建筑机制](Design/Mechanics/Tower_Defense_System.md):** 建造规则、人塔协同。
*   **[元素反应机制](Design/Mechanics/Elemental_Reaction_System.md):** 状态连携 (油火爆燃)。
*   **[肉鸽强化系统](Design/Mechanics/Roguelike_Perks.md):** 词条池、诅咒机制。
*   **[仇恨系统](Design/Mechanics/Aggro_System.md):** 目标选择逻辑。

### 💰 系统与经济 (Systems & Economy)
*   **[装备与物品化](Design/Systems/Itemization.md):** 词缀结构、暗金设计。
*   **[掉落规则](Design/Systems/Loot_Table_Rules.md):** 掉落蓄水池、智能掉落。
*   **[POE 门票机制](Design/Systems/POE_Map_Fragment_Design.md):** 高风险门票与经济循环。
*   **[局外成长](Design/Systems/Meta_Progression.md):** 天赋树、基地建设。
*   **[经济模型](Design/Systems/Economy_And_Inflation_Model.md):** 资源产出消耗。

### 🗺️ 内容与世界 (Content & World)
*   **[怪物图鉴](Design/Content/Enemy_Bestiary.md):** AI 行为模板。
*   **[关卡设计指南](Design/Content/Level_Design_Guide.md):** 波次节奏控制。
*   **[关卡设计理论](Design/Content/Level_Design_Theory.md):** 空间结构与隐性引导。

### 🎓 理论与策略 (Theory & Strategy)
*   **[设计哲学](Design/Philosophy_And_Systems.md):** 玩家心理模型。
*   **[三位一体利弊](Design/Philosophy_And_Systems/Hybrid_Genre_Analysis.md):** 混合品类权衡。
*   **[游戏心理学](Design/Game_Psychology_DeepDive.md):** 心流与爽点公式。
*   **[案例分析](Design/Industry_CaseStudies.md):** 竞品研究集合。

### 📅 运营 (LiveOps)
*   **[通行证经济](Design/LiveOps/Battle_Pass_Economy.md):** 40天周期设计。
*   **[活动排期](Design/LiveOps/Event_Cadence_Strategy.md):** 宏观/微观活动。
*   **[Wiki构建](Design/LiveOps/Wiki_And_Strategy_Station_Guide.md):** 社区攻略站策略。

</details>

<details>
<summary><strong>📂 点击展开：2. 技术架构 (Tech)</strong></summary>

### 🏗️ 核心架构
*   **[GAS 技能系统](Tech/Gameplay_Ability_System_Design.md):** 技能系统设计。
*   **[NavMesh 寻路](Tech/Mechanics/NavMesh_Pathfinding_Guide.md):** 动态避障。
*   **[3D vs 平面地形](Dev_Guides/Technical_Implementation/Terrain_3D_vs_2D_Analysis.md):** 选型分析。
*   **[弹道系统](Tech/Mechanics/Projectile_System_DeepDive.md):** 对象池与射线检测。
*   **[网络架构](Tech/Network_Architecture.md):** 状态同步。
*   **[存档系统](Tech/Save_System_Architecture.md):** 持久化方案。

### 🤖 AI 与算法
*   **[AI 效用系统](Tech/AI_Utility_System.md):** Utility AI。
*   **[状态机模式](Tech/FSM_Design_Patterns.md):** FSM 实践。
*   **[游戏曲线](Tech/Math/Game_Curves_DeepDive.md):** 数学缓动。

### 🚀 性能与工具
*   **[移动端优化](Tech/Mobile_Optimization_Guide.md):** 渲染与内存。
*   **[性能预算](Tech/Performance_Budget.md):** 机型红线。
*   **[自动化Wiki](Dev_Guides/Tools/Automated_Wiki_Generation.md):** 自动图鉴生成。
*   **[调试指令](Dev_Guides/Tools/Debug_Console_And_Cheats.md):** GM工具集。
*   **[Luban配置](Tech/Luban_Config_Guide.md):** 导表工作流。

</details>

<details>
<summary><strong>📂 点击展开：3. 美术与音频 (Art & Audio)</strong></summary>

### 🎨 美术标准
*   **[视觉质量指南](Art/Visual_Quality_Guide.md):** 风格标准。
*   **[视觉层级](Art/Visual_Hierarchy_In_Chaos.md):** 混乱管理与轮廓线。
*   **[新手引导](Design/UX/FTUE_Best_Practices.md):** 洋葱皮教学与FTUE。
*   **[UI/UX 指南](Art/UI_UX_Guidelines.md):** 交互规范。
*   **[特效标准](Art/VFX_Standards.md):** 粒子性能限制。
*   **[相机设置](Art/Camera_DeepDive_And_Settings.md):** 震动与跟随。
*   **[游戏手感](Art/Game_Feel_And_Juice.md):** 顿帧与打击感。

### 🎵 音频工程
*   **[音频实践](Audio/Practical_Guide.md):** 基础混音。
*   **[轻量级框架](Audio/Lightweight_Audio_Framework.md):** 纯代码管理方案。
*   **[挂载策略](Audio/AudioListener_Placement_Guide.md):** 俯视角听感修正。
*   **[音效技巧](Audio/Audio_System_Design_and_Tricks.md):** 变调与侧链。
*   **[Wwise指南](Audio/Wwise_Middleware_Guide.md):** 中间件对比。

</details>

<details>
<summary><strong>📂 点击展开：4. 生产与发行 (Production)</strong></summary>

*   **[Steam 发行](Dev_Guides/Publishing/Steam_Strategy.md):** 商店页与新品节。
*   **[TapTap 发行](Dev_Guides/Publishing/TapTap_Strategy.md):** 篝火测试。
*   **[敏捷开发](Dev_Guides/Collaboration/Agile_For_Indie_Teams.md):** 冲刺规划。
*   **[成功案例](Design/Industry_CaseStudies.md):** 行业标杆分析。
*   **[失败复盘](Dev_Guides/Failure_Cases/Anthem_Failure_Analysis.md):** 避坑指南。

</details>

---

## 🔗 快速链接
*   **[Unity 标准目录结构](Unity_Standards/Folder_Structure.md)**
*   **[美术资源导出规范](Dev_Guides/Art_Pipeline/Art_Asset_Export_Standards.md)**
*   **[AI 助手上下文 (GEMINI.md)](GEMINI.md)**

---
*Project maintained by the Vampirefall Team.*
