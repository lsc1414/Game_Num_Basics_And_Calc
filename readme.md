# 游戏开发的100件事 
# The 100 Steps to Launch
> **"当《王国保卫战》遇见《流放之路》与《吸血鬼幸存者》"**
>
> 这不仅仅是一个文档库，而是一份 **从立项到上线 (Zero to Hero)** 的实战生存指南。我们在这里记录下开发高品质 **混合品类 (Hybrid Genre)** 游戏所需的 100 个关键决策与技术标准。

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
1.  **画风对齐**: 阅读 **[视觉质量指南](Art/Visual_Quality_Guide.md)** 和 **[美术风格一致性指南](Art/Art_Direction_Guide.md)**。
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

<details markdown="1" open>
<summary><strong>📂 点击展开：1. 游戏设计 (Design)</strong></summary>

### ⚔️ 核心机制 (Core Mechanics)
*   **[数值框架构建指南](Design/Numerical/Numerical_Framework_Methodology.md):** 从零开始确立TTK、经济循环与成长曲线。
*   **[数值设计手册](Design/Numerical_Manual.md):** 数学的“圣经”。
*   **[战斗系统详解](Design/Mechanics/Combat_System.md):** 伤害类型、韧性机制。
*   **[塔防建筑机制](Design/Mechanics/Tower_Defense_System.md):** 建造规则、人塔协同。
*   **[元素反应机制](Design/Mechanics/Elemental_Reaction_System.md):** 状态连携 (油火爆燃)。
*   **[肉鸽强化系统](Design/Mechanics/Roguelike_Perks.md):** 词条池、诅咒机制。
*   **[仇恨系统](Design/Mechanics/Aggro_System.md):** 目标选择逻辑。
*   **[难度曲线与 DDA 系统](Design/Mechanics/Difficulty_And_DDA_System.md):** 心流理论、动态难度调整算法。

### 💰 系统与经济 (Systems & Economy)
*   **[装备与物品化](Design/Systems/Itemization.md):** 词缀结构、暗金设计。
*   **[权衡词条库](Design/Systems/TradeOff_Affix_Library.md):** 100个“缺陷即特色”的词条灵感。
*   **[关卡词条库](Design/Systems/Map_Affix_Library.md):** 100+个中英文对照的地图特效。
*   **[塔防词条库](Design/Systems/Tower_Defense_Affix_Library.md):** 100+个塔防专用词条。
*   **[掉落规则](Design/Systems/Loot_Table_Rules.md):** 掉落蓄水池、智能掉落。
*   **[POE 门票机制](Design/Systems/POE_Map_Fragment_Design.md):** 高风险门票与经济循环。
*   **[局外成长](Design/Systems/Meta_Progression.md):** 天赋树、基地建设。
*   **[经济模型](Design/Systems/Economy_And_Inflation_Model.md):** 资源产出消耗。
*   **[数值膨胀控制论](Design/Systems/Power_Creep_Management.md):** 线性vs指数增长与数值压缩。
*   **[邮件系统](Design/Systems/Mail_System_Design.md):** 公告与奖励发放。
*   **[成就与收集系统](Design/Systems/Achievement_And_Collection_System.md):** 成就设计、图鉴系统、完成主义心理学。
*   **[技能树设计](Design/Systems/Skill_Tree_Design.md):** 线性/分支/网格树、Build多样性、重置机制。
*   **[多人协作平衡](Design/Systems/Coop_Balance_Design.md):** 难度伸缩、资源分配(金币独立/以太共享)、职业互补。

### 🗺️ 内容与世界 (Content & World)
*   **[怪物图鉴](Design/Content/Enemy_Bestiary.md):** AI 行为模板。
*   **[关卡设计指南](Design/Content/Level_Design_Guide.md):** 波次节奏控制。
*   **[关卡设计理论](Design/Content/Level_Design_Theory.md):** 空间结构与隐性引导。
*   **[Boss 设计哲学](Design/Content/Boss_Design_Philosophy.md):** 柱阶段系统、电报机制、业界案例分析。
*   **[游戏剧情与包装](Design/Narrative/Game_Narrative_And_Presentation.md):** 环境叙事、Lore 系统、肉鸽叙事设计。

### 🎓 理论与策略 (Theory & Strategy)
*   **[设计哲学](Design/Philosophy_And_Systems.md):** 玩家心理模型。
*   **[三位一体利弊](Design/Philosophy_And_Systems/Hybrid_Genre_Analysis.md):** 混合品类权衡。
*   **[横竖屏策略](Design/Product_Strategy/Screen_Orientation_Strategy.md):** 用户场景分析。
*   **[游戏心理学框架](Design/Game_Psychology_DeepDive.md):** 心流通道、爽点设计公式、流失归因。
*   **[斯金纳箱理论](Design/Psychology/Skinner_Box_and_Addiction.md):** 随机奖励 (VR) 与固定奖励 (FR) 的成瘾机制。

### 🧠 交互与体验 (UX)
*   **[无障碍设计标准](Design/UX/Accessibility_Standards.md):** 色盲模式/防晕/改键 (Steam Deck/主机必读)。

### 🏆 案例分析 (Case Studies)
*   **[行业标杆](Design/Industry_CaseStudies.md):** 竞品研究集合。
*   **[正中靶心深度解析](Design/CaseStudies/BangBangSurvivor_DeepDive.md):** 居中UI与权衡机制拆解。
*   **[Bloons TD6](Dev_Guides/Industry_Cases/Bloons_TD6_Damage_Matrix.md):** 伤害矩阵设计。
*   **[Brotato](Dev_Guides/Industry_Cases/Brotato_Numerical_Analysis.md):** 属性加成与负属性博弈。
*   **[Hades](Dev_Guides/Industry_Cases/Hades_Build_Diversity.md):** 构建多样性分析。
*   **[Kingdom Rush](Dev_Guides/Industry_Cases/Kingdom_Rush_Numerical_Model.md):** 经典塔防数值。
*   **[Loop Hero](Dev_Guides/Industry_Cases/Loop_Hero_Loop_Mechanics.md):** 循环机制解构。
*   **[Palworld](Dev_Guides/Industry_Cases/Palworld_Production_Model.md):** 缝合生产模式。
*   **[Thronefall](Dev_Guides/Industry_Cases/Thronefall_Minimalist_Hybrid.md):** 极简混合设计。
*   **[吸血鬼幸存者](Dev_Guides/Industry_Cases/Vampire_Survivors_Performance.md):** 性能与爽感。

### 💀 失败复盘 (Post-Mortems)
*   **[Anthem](Dev_Guides/Failure_Cases/Anthem_Failure_Analysis.md):** 发行灾难分析。
*   **[Battleborn](Dev_Guides/Failure_Cases/Battleborn_Failure_Analysis.md):** 定位模糊之殇。
*   **[Concord](Dev_Guides/Failure_Cases/Concord_Failure_Analysis.md):** 服务型游戏困境。
*   **[Paragon](Dev_Guides/Failure_Cases/Paragon_Complexity_Trap.md):** 复杂性陷阱。
*   **[The Day Before](Dev_Guides/Failure_Cases/The_Day_Before_Failure_Analysis.md):** 营销骗局警示。

### 📅 运营 (LiveOps)
*   **[通行证经济](Design/LiveOps/Battle_Pass_Economy.md):** 40天周期设计。
*   **[活动排期](Design/LiveOps/Event_Cadence_Strategy.md):** 宏观/微观活动。
*   **[高级运营系统](Design/LiveOps/Advanced_LiveOps_Systems.md):** 动态礼包与回归系统。
*   **[Wiki构建](Design/LiveOps/Wiki_And_Strategy_Station_Guide.md):** 社区攻略站策略。

</details>

<details markdown="1" open>
<summary><strong>📂 点击展开：2. 技术架构 (Tech)</strong></summary>

### 🏗️ 核心架构
*   **[GAS 技能系统](Tech/Gameplay_Ability_System_Design.md):** 技能系统设计。
*   **[Mod 系统架构](Tech/Modding_System_Architecture.md):** 数据驱动与 Lua 脚本支持。
*   **[NavMesh 寻路](Tech/Mechanics/NavMesh_Pathfinding_Guide.md):** 动态避障。
*   **[3D vs 平面地形](Dev_Guides/Technical_Implementation/Terrain_3D_vs_2D_Analysis.md):** 选型分析。
*   **[弹道系统](Tech/Mechanics/Projectile_System_DeepDive.md):** 对象池与射线检测。
*   **[网络架构](Tech/Network_Architecture.md):** 状态同步。
*   **[存档系统](Tech/Save_System_Architecture.md):** 持久化方案。
*   **[热更与资源](Tech/Hot_Update_And_Resources.md):** 资源管理与热更策略。
*   **[输入系统](Tech/Input_System_Design.md):** 跨平台输入映射。
*   **[ECS 架构](Tech/Architecture/ECS_Theory_And_Practice.md):** 数据驱动设计理论。
*   **[统一决策系统](Tech/Architecture/Unified_Decision_System.md):** 核心决策层设计。
*   **[决策系统图解](Tech/Architecture/Decision_System_Diagrams.md):** 架构可视化。
*   **[Unity 代码毒药](Tech/Architecture/Unity_Anti_Patterns.md):** 毁灭项目的反模式 (单例/协程/Linq)。

### 🤖 AI 与算法
*   **[AI 效用系统](Tech/AI_Utility_System.md):** Utility AI。
*   **[Roguelike 随机算法](Tech/Algorithms/Roguelike_RNG_Systems.md):** 标签加权与动态概率模型。
*   **[状态机模式](Tech/FSM_Design_Patterns.md):** FSM 实践。
*   **[游戏曲线](Tech/Math/Game_Curves_DeepDive.md):** 数学缓动。
*   **[设计模式](Tech/Architecture/Game_Design_Patterns_Practice.md):** 常用模式实战。
*   **[Shader 数学](Tech/Graphics/Shader_Math_Patterns.md):** 图形学基础公式。
*   **[WFC 生成](Dev_Guides/Technical_Implementation/Procedural_Generation_WFC.md):** 波函数坍缩算法。
*   **[掉落算法](Dev_Guides/Technical_Implementation/Loot_Reservoir_Algorithm.md):** 动态概率控制。
*   **[PRD 算法](Dev_Guides/Technical_Implementation/PRD_Algorithm_Complete.md):** 伪随机分布详解。
*   **[程序化生成指南](Tech/Algorithms/Procedural_Generation_Guide.md):** WFC、BSP、Cellular Automata、地图生成算法。

*   **[自动化Wiki](Dev_Guides/Tools/Automated_Wiki_Generation.md):** 自动图鉴生成。
*   **[福尔摩斯调试法](Dev_Guides/Debugging/Sherlock_Holmes_Debugging_Guide.md):** 二分法与内存侦探。
*   **[调试指令](Dev_Guides/Tools/Debug_Console_And_Cheats.md):** GM工具集。
*   **[Luban配置](Tech/Luban_Config_Guide.md):** 导表工作流。
*   **[ECS 优化](Dev_Guides/Technical_Implementation/ECS_Performance_Optimization.md):** 实体系统性能调优。
*   **[游戏埋点](Dev_Guides/Technical_Implementation/Game_Analytics_Guide.md):** 数据采集方案。
*   **[最佳实践](Dev_Guides/Technical_Implementation/Game_Dev_Best_Practices.md):** 通用开发规范。
*   **[GPU Instancing](Dev_Guides/Technical_Implementation/GPU_Instancing_Guide.md):** 批量渲染优化。
*   **[配置表工作流](Dev_Guides/Technical_Implementation/ScriptableObject_vs_Excel_Workflow.md):** 数据导表对比。
*   **[技能动画](Dev_Guides/Technical_Implementation/Skill_Animation_Pipeline.md):** 动画状态机管线。
*   **[本地化系统](Dev_Guides/Technical_Implementation/Skill_Text_Localization_System.md):** 多语言实现。
*   **[战斗模拟](Dev_Guides/Tools/Combat_Simulation_System.md):** 离线战斗验证。
*   **[蒙特卡洛](Dev_Guides/Tools/Monte_Carlo_Simulation.md):** 概率模拟工具。
*   **[数值模板](Dev_Guides/Tools/Excel_Numerical_Templates.md):** Excel 计算表。
*   **[计算器套件](Dev_Guides/Tools/Numerical_Calculator_Suite.md):** 综合计算工具。
*   **[性能监控](Dev_Guides/Tools/Performance_Monitoring_Scripts.md):** 运行时性能分析。
*   **[工具链指南](Dev_Guides/Tools/Game_Dev_Toolchain_Guide.md):** 自动化与管线加速。
*   **[Odin Inspector 高级技巧](Dev_Guides/Tools/Odin_Inspector_Advanced_Techniques.md):** 自定义验证、动态下拉、性能优化等非官方 Demo 技巧。
*   **[Odin + Luban 集成指南](Dev_Guides/Tools/Odin_Luban_Integration_Guide.md):** 可视化编辑 + 配置表生成的双向工作流。
*   **[PRD 插件](Dev_Guides/Tools/Unity_PRD_Plugin.md):** Unity 随机工具。
*   **[AI 平衡测试](Dev_Guides/Tools/AI_Balance_Testing.md):** 自动化平衡性测试。
*   **[Roguelike 组合测试](Dev_Guides/Testing/Roguelike_Rapid_Testing_System.md):** (木头人/Build代码/热重载) 快速验证方案。


</details>

<details markdown="1" open>
<summary><strong>📂 点击展开：3. 美术与音频 (Art & Audio)</strong></summary>

### 🎨 技术美术 (Tech Art)
*   **[资源验证标准](Art/Tech_Art/Asset_Validation_Standards.md):** 纹理/模型/材质的性能红线。
*   **[HDR 渲染机制](Art/Tech_Art/HDR_DeepDive.md):** 线性空间、Tone Mapping 与 FP16 精度。
*   **[Bloom 后处理详解](Art/Tech_Art/Bloom_PostProcessing_DeepDive.md):** 阈值设置、HDR颜色与性能优化。
*   **[特效优化黑魔法](Art/VFX/VFX_Optimization_Guide.md):** Overdraw 杀手与粒子性能调优。
*   **[粒子系统详解](Art/VFX/Unity_Particle_System_DeepDive.md):** Shader/Blender工作流与C#动态控制。
*   **[视觉质量指南](Art/Visual_Quality_Guide.md):** 风格统一性。
*   **[混乱管理](Art/Visual_Hierarchy_In_Chaos.md):** 视觉降噪。
*   **[相机设置](Art/Camera_DeepDive_And_Settings.md):** 震动与跟随。
*   **[游戏手感](Art/Game_Feel_And_Juice.md):** 顿帧与打击感。

### 🎵 音频工程 (Audio)
*   **[音频实践](Audio/Practical_Guide.md):** 基础混音。
*   **[轻量级框架](Audio/Lightweight_Audio_Framework.md):** 纯代码管理方案。
*   **[挂载策略](Audio/AudioListener_Placement_Guide.md):** 俯视角听感修正。
*   **[音效技巧](Audio/Audio_System_Design_and_Tricks.md):** 变调与侧链。
*   **[动态音乐系统](Audio/Adaptive_Music_System.md):** 垂直分层、水平切换、自适应强度。
*   **[Wwise指南](Audio/Wwise_Middleware_Guide.md):** 中间件对比。

</details>

<details markdown="1">
<summary><strong>📂 点击展开：4. 生产与发行 (Production)</strong></summary>

### 🗓️ 流程与管理 (Process & Management)
*   **[上线生死清单](Dev_Guides/Publishing/Launch_Readiness_Checklist.md):** 发射前夜必查 (FTUE/合规/包体)。
*   **[社区危机公关](Dev_Guides/Community/Community_Crisis_Management.md):** 差评如潮时的应对 SOP 与赎罪指南。
*   **[Steam 发行](Dev_Guides/Publishing/Steam_Strategy.md):** 商店页与新品节。
*   **[TapTap 发行](Dev_Guides/Publishing/TapTap_Strategy.md):** 篝火测试。
*   **[敏捷开发](Dev_Guides/Collaboration/Agile_For_Indie_Teams.md):** 冲刺规划、每日站会。
*   **[生产经验](Dev_Guides/Production_Lessons.md):** 团队踩坑记录。
*   **[里程碑规划](Dev_Guides/Collaboration/Milestone_Planning.md):** 版本节点控制。
*   **[Beta 测试](Dev_Guides/Collaboration/Beta_Testing_Guide.md):** 测试流程管理。
*   **[远程协作](Dev_Guides/Collaboration/Remote_Collaboration.md):** 异地办公指南。
*   **[高效开发指南](Design/Production/Efficient_Game_Dev_Guide.md):** 拒绝返工与项目规划。
*   **[文档模板](Design/Production/Design_Document_Templates.md):** 策划文档标准模板库。

### 🤝 协作规范 (Collaboration)
*   **[Git 版本管理](Dev_Guides/Collaboration/Git_Commit_Standards.md):** Commit Log 模板与分支策略。
*   **[Git 极客指南](Dev_Guides/Collaboration/Git_Advanced_Guide_For_Programmers.md):** 命令行与冲突解决。
*   **[GitHub PR](Dev_Guides/Collaboration/GitHub_PR_Workflow.md):** Code Review 礼仪。
*   **[SVN转Git](Dev_Guides/Collaboration/SVN_vs_Git_Migration_Guide.md):** 迁移与上手手册。
*   **[Unity 技巧](Dev_Guides/Unity_Practical_Tips.md):** 引擎使用小贴士。
*   **[独立美术策略](Dev_Guides/Art_Pipeline/Indie_Team_Art_Strategy.md):** 资源生产管线。
*   **[UI 制作精通](Dev_Guides/Art_Pipeline/UI_Production_Mastery.md):** 从手工到自动化的 UI 工业化指南。
*   **[白盒工作流](Dev_Guides/Art_Pipeline/Unity_Greybox_Workflow.md):** 关卡验证流程。



</details>

---

## 🔗 快速链接
*   **[Unity 标准目录结构](Unity_Standards/Folder_Structure.md)**
*   **[资源管理标准](Unity_Standards/Asset_Management.md)**
*   **[标准资源工作流](Unity_Standards/Standard_Resource_Workflow.md)**
*   **[美术资源导出规范](Dev_Guides/Art_Pipeline/Art_Asset_Export_Standards.md)**
*   **[Roguelike 深度分析](Research/Roguelike强化系统深度分析报告.md)**
*   **[AI 助手上下文 (GEMINI.md)](GEMINI.md)**

---
*Project maintained by the Vampirefall Team.*
