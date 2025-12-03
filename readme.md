# 🏰 游戏开发全案 (The Game Development Codex)
`游戏核心设计、数值模型与技术标准的单一真理来源 (Single Source of Truth)。`
## 📚 文档导览 (Documentation Map)

### 1. 🧠 游戏设计 (Design - The "Soul")

#### ⚔️ 核心机制 (Core Mechanics)
*   **[数值设计手册](Design/Numerical_Manual.md):** 数学的“圣经” (伤害公式、防御模型)。
*   **[战斗系统详解](Design/Mechanics/Combat_System.md):** 伤害类型、异常状态、韧性/硬直机制。
*   **[塔防建筑机制](Design/Mechanics/Tower_Defense_System.md):** 塔的分类、建造规则、人塔协同。
*   **[肉鸽强化系统](Design/Mechanics/Roguelike_Perks.md):** 局内成长、词条池、诅咒机制。
*   **[仇恨系统](Design/Mechanics/Aggro_System.md):** 仇恨计算与目标选择逻辑。

#### 💰 系统与经济 (Systems & Economy)
*   **[装备与物品化](Design/Systems/Itemization.md):** 装备部位、词缀池结构、暗金设计。
*   **[掉落规则](Design/Systems/Loot_Table_Rules.md):** 掉落蓄水池、智能掉落、宝箱类型。
*   **[POE 门票机制解析](Design/Systems/POE_Map_Fragment_Design.md):** 碎片化积累、高风险门票与经济循环。
*   **[局外成长](Design/Systems/Meta_Progression.md):** 星盘天赋树、基地建设。
*   **[邮件系统](Design/Systems/Mail_System_Design.md):** 异步通信、生命周期管理 (TTL)。
*   **[经济与通胀模型](Design/Systems/Economy_And_Inflation_Model.md):** 资源产出消耗循环。
*   **[LiveOps 运营](Design/LiveOps/Advanced_LiveOps_Systems.md):**
    *   **[战斗通行证经济](Design/LiveOps/Battle_Pass_Economy.md):** 40天周期、价值锚定。
    *   **[活动排期策略](Design/LiveOps/Event_Cadence_Strategy.md):** 宏观/微观活动分层。
    *   **[Wiki与攻略站构建](Design/LiveOps/Wiki_And_Strategy_Station_Guide.md):** 内容架构、UGC激励与技术实现。

#### 🗺️ 内容与世界 (Content & World)
*   **[怪物图鉴](Design/Content/Enemy_Bestiary.md):** 怪物分级、AI 行为模板、特殊词缀。
*   **[关卡设计指南](Design/Content/Level_Design_Guide.md):** 地图生成逻辑、波次节奏控制。
*   **[关卡设计理论](Design/Content/Level_Design_Theory.md):** 空间结构、起承转合与视觉引导。

#### 🎓 理论与策略 (Theory & Strategy)
*   **[设计哲学](Design/Philosophy_And_Systems.md):** 核心循环、玩家心理模型。
*   **[三位一体利弊分析](Design/Philosophy_And_Systems/Hybrid_Genre_Analysis.md):** 肉鸽+塔防+刷宝的设计权衡。
*   **[游戏心理学框架](Design/Game_Psychology_DeepDive.md):** 心流通道、爽点设计公式、流失归因。
*   **[竖屏 vs 横屏策略](Design/Product_Strategy/Screen_Orientation_Strategy.md):** 用户场景分析与品类选择建议。
*   **[行业案例分析](Design/Industry_CaseStudies.md):** 竞品分析 (PoE, Vampire Survivors)。

---

### 2. � 技术架构 (Tech - The "Brain")

#### 🏗️ 核心架构 (Architecture)
*   **[Gameplay Ability System](Tech/Gameplay_Ability_System_Design.md):** 技能系统设计 (GAS)。
    *   **[NavMesh 寻路指南](Tech/Mechanics/NavMesh_Pathfinding_Guide.md):** 动态避障与性能调优。
    *   **[3D地形 vs 平面地形](Dev_Guides/Technical_Implementation/Terrain_3D_vs_2D_Analysis.md):** 寻路性能与美术成本的权衡分析。
    *   **[弹道系统深度解析](Tech/Mechanics/Projectile_System_DeepDive.md)::** 抛物线、射线与对象池。
*   **[网络架构](Tech/Network_Architecture.md):** 状态同步与断线重连。
*   **[存档系统](Tech/Save_System_Architecture.md):** 数据持久化方案。
*   **[输入系统](Tech/Input_System_Design.md):** 跨平台输入映射。

#### 🤖 AI 与算法 (AI & Algorithms)
*   **[AI 效用系统](Tech/AI_Utility_System.md):** Utility AI 决策模型。
*   **[状态机模式](Tech/FSM_Design_Patterns.md):** 有限状态机设计模式。
*   **[游戏曲线数学](Tech/Math/Game_Curves_DeepDive.md):** 贝塞尔曲线、缓动函数应用。

#### 🚀 性能与工具 (Performance & Tools)
*   **[移动端优化指南](Tech/Mobile_Optimization_Guide.md):** 渲染管线、内存管理。
*   **[性能预算](Tech/Performance_Budget.md):** 各机型性能指标红线。
*   **[热更与资源管理](Tech/Hot_Update_And_Resources.md):** YooAsset 资源更新方案。
*   **[自动化Wiki生成](Dev_Guides/Tools/Automated_Wiki_Generation.md):** 从工程资源自动提取图鉴数据的方案。
*   **[Luban 配置指南](Tech/Luban_Config_Guide.md):** 导表工具使用规范。

---

### 3. 🎨 美术与音频 (Art & Audio - The "Face")

#### 🖌️ 美术管线 (Pipeline)
*   **[独立团队美术策略](Dev_Guides/Art_Pipeline/Indie_Team_Art_Strategy.md):** 风格化渲染、TCP2 协议、低成本方案。
*   **[Unity 灰盒工作流](Dev_Guides/Art_Pipeline/Unity_Greybox_Workflow.md):** ProBuilder 建模、度量衡标准。
*   **[美术资源出图规范](Dev_Guides/Art_Pipeline/Art_Asset_Export_Standards.md):** 命名规范、模型/贴图规则。

#### 📐 标准与规范 (Standards)
*   **[视觉质量指南](Art/Visual_Quality_Guide.md):** 风格统一性标准。
*   **[UI/UX 指南](Art/UI_UX_Guidelines.md):** 交互设计规范。
*   **[特效标准](Art/VFX_Standards.md):** 粒子系统性能限制。
*   **[相机设置](Art/Camera_DeepDive_And_Settings.md):** FOV、震动与跟随。
*   **[游戏手感 (Juice)](Art/Game_Feel_And_Juice.md):** 打击感、屏幕震动、顿帧。

#### 🎵 音频 (Audio)
*   **[音频实践指南](Audio/Practical_Guide.md):** 音效管理与混音。
*   **[AudioListener 挂载策略](Audio/AudioListener_Placement_Guide.md):** 解决俯视角游戏声音定位错误的方案。
*   **[Unity 轻量级音频框架](Audio/Lightweight_Audio_Framework.md):** 纯代码实现的音效管理方案 (对象池+变奏)。
*   **[音效设计与技巧](Audio/Audio_System_Design_and_Tricks.md):** 动态音阶算法、侧链压缩与防爆音策略。
*   **[Wwise 中间件指南](Audio/Wwise_Middleware_Guide.md):** 核心概念 (Event/RTPC) 与 Unity 原生音频对比。
*   **[音效设计与技巧](Audio/Audio_System_Design_and_Tricks.md):** 动态音阶算法、侧链压缩与防爆音策略。
*   **[Wwise 中间件指南](Audio/Wwise_Middleware_Guide.md):** 核心概念 (Event/RTPC) 与 Unity 原生音频对比。
*   **[Wwise 中间件指南](Audio/Wwise_Middleware_Guide.md):** 核心概念 (Event/RTPC) 与 Unity 原生音频对比。

---

### 4. 📈 生产与发行 (Production - The "Muscle")

#### 📢 发行策略 (Publishing)
*   **[Steam 发行策略](Dev_Guides/Publishing/Steam_Strategy.md):** 愿望单、商店页优化、新品节。
*   **[TapTap 发行策略](Dev_Guides/Publishing/TapTap_Strategy.md):** 评分维护、篝火测试、0分成模式。

#### 🤝 团队协作 (Collaboration)
*   **[敏捷开发指南](Dev_Guides/Collaboration/Agile_For_Indie_Teams.md):** 冲刺规划、每日站会。
*   **[里程碑规划](Dev_Guides/Collaboration/Milestone_Planning.md):** 版本节点控制。
*   **[远程协作](Dev_Guides/Collaboration/Remote_Collaboration.md):** 沟通工具与规范。
*   **[Beta 测试指南](Dev_Guides/Collaboration/Beta_Testing_Guide.md):** 用户测试流程。

#### 📚 案例复盘 (Case Studies)
*   **失败案例**: [Battleborn](Dev_Guides/Failure_Cases/Battleborn_Failure_Analysis.md) | [Anthem](Dev_Guides/Failure_Cases/Anthem_Failure_Analysis.md) | [Concord](Dev_Guides/Failure_Cases/Concord_Failure_Analysis.md) | [The Day Before](Dev_Guides/Failure_Cases/The_Day_Before_Failure_Analysis.md) | [Paragon](Dev_Guides/Failure_Cases/Paragon_Complexity_Trap.md)
*   **成功案例**: [Vampire Survivors](Dev_Guides/Industry_Cases/Vampire_Survivors_Performance.md) | [Hades](Dev_Guides/Industry_Cases/Hades_Build_Diversity.md) | [Kingdom Rush](Dev_Guides/Industry_Cases/Kingdom_Rush_Numerical_Model.md) | [Bloons TD6](Dev_Guides/Industry_Cases/Bloons_TD6_Damage_Matrix.md) | [Palworld](Dev_Guides/Industry_Cases/Palworld_Production_Model.md) | [Thronefall](Dev_Guides/Industry_Cases/Thronefall_Minimalist_Hybrid.md) | [Loop Hero](Dev_Guides/Industry_Cases/Loop_Hero_Loop_Mechanics.md)

#### 📏 Unity 标准 (Standards)
*   **[资源命名规范](Unity_Standards/Asset_Naming.md):** 文件命名规则。
*   **[目录结构](Unity_Standards/Folder_Structure.md):** 项目工程目录规范。
*   **[资源工作流](Unity_Standards/Standard_Resource_Workflow.md):** 导入设置预设。

---

### 5. 👮 执行标准 (Execution Standards)

*   **[全员速查表 (Must/Must Not)](Dev_Guides/Project_Cheat_Sheet.md):** 程序员/美术/策划/PM 的绝对红线与核心原则。
*   **[AI 上下文 (GEMINI.md)](GEMINI.md):** 专为 AI 代理生成的项目上下文摘要。

---

*Project maintained by the Vampirefall Team.*