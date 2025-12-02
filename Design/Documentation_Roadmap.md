# 🗺️ Vampirefall 项目文档开发路线图 (Documentation Roadmap)

本文档旨在规划 Project Vampirefall 从原型到量产阶段所需的所有设计与技术文档。
目标是建立一个**“单一真理来源” (Single Source of Truth)**，确保策划、程序、美术在同一个频道上工作。

> **状态图例：**
> *   ✅ **[已完成]**: 文档已存在且核心内容完备。
> *   🚧 **[进行中]**: 正在编写或需要补充细节。
> *   📅 **[计划中]**: 尚未开始，等待排期。

---

## 1. 核心玩法与机制 (Core Gameplay & Mechanics)
*定义游戏的“骨架”——玩家在每一秒钟具体在玩什么。*

*   ✅ **[数值核心] `Design/Numerical_Manual.md`**
    *   伤害公式、防御模型、PRD算法、经济循环基础。
*   ✅ **[设计哲学] `Design/Philosophy_And_Systems.md`**
    *   核心循环、设计支柱、体验目标。
*   ✅ **[战斗系统详解] `Design/Mechanics/Combat_System.md`**
    *   详细定义伤害类型（物理/魔法/元素）、元素反应、硬直与韧性机制。
*   ✅ **[塔防建筑机制] `Design/Mechanics/Tower_Defense_System.md`**
    *   塔的生命周期、建造规则、人塔协同机制。
*   ✅ **[肉鸽强化系统] `Design/Mechanics/Roguelike_Perks.md`**
    *   局内成长（Level Up Bonuses）、随机池权重、诅咒机制。
*   ✅ **[仇恨系统与AI] `Design/Mechanics/Aggro_System.md`** *(新增)*
    *   仇恨列表计算、混合优先级金字塔、风筝限制与特殊行为。

---

## 2. 外围系统与经济 (Meta Systems & Economy)
*定义游戏的“血肉”——玩家为什么第二天还会回来玩。*

*   ✅ **[装备与物品化] `Design/Systems/Itemization.md`**
    *   装备部位、词缀池结构、暗金装备设计思路。
*   ✅ **[局外成长] `Design/Systems/Meta_Progression.md`**
    *   天赋树 (Passive Tree)、基地建设、永久货币循环。
*   ✅ **[掉落与战利品] `Design/Systems/Loot_Table_Rules.md`**
    *   掉落权重表、智能掉落 (Smart Loot)、掉落蓄水池算法。

---

## 3. 内容设计 (Content Design)
*定义玩家消耗的具体素材。*

*   ✅ **[怪物图鉴与AI] `Design/Content/Enemy_Bestiary.md`**
    *   怪物分级、AI行为树模式、特殊词缀。
*   ✅ **[关卡与波次设计] `Design/Content/Level_Design_Guide.md`**
    *   地图生成规则、刷怪节奏控制、动态难度。

---

## 4. 技术架构 (Technical Architecture)
*定义游戏的“大脑”——如何稳定高效地运行。*

*   ✅ **[Unity 目录规范] `Unity_Standards/Folder_Structure.md`**
*   ✅ **[资产命名规范] `Unity_Standards/Asset_Naming.md`**
*   ✅ **[资产管理指南] `Unity_Standards/Asset_Management.md`**
*   ✅ **[存档系统] `Tech/Save_System_Architecture.md`**
    *   数据结构、序列化、反作弊。
*   ✅ **[性能预算] `Tech/Performance_Budget.md`**
    *   60FPS 标准、CPU/GPU 限制、LOD 策略。
*   ✅ **[输入系统] `Tech/Input_System_Design.md`**
    *   Input System 映射、手柄支持、辅助功能。
*   ✅ **[Luban 配表指南] `Tech/Luban_Config_Guide.md`** *(新增)*
    *   ID 命名规范、枚举与多态、Excel 填表技巧。
*   ✅ **[FSM 状态机] `Tech/FSM_Design_Patterns.md`** *(新增)*
    *   怪物 AI 逻辑、防御塔循环、代码实现模式。
*   🚧 **[Shader 核心数学] `Tech/Shader_Math_Basics.md`** *(新增)*
    *   点积/叉积应用、平滑插值、矩阵变换直觉。
*   🚧 **[移动端优化指南] `Tech/Mobile_Optimization_Guide.md`** *(新增)*
    *   TBDR架构特性、Overdraw控制、半精度(Half)运算。

---

## 5. 美术与表现 (Art & Audio)
*定义游戏的“皮肤”——外观与听感。*

*   ✅ **[音频指南] `Audio/Practical_Guide.md`**
*   ✅ **[UI/UX 规范] `Art/UI_UX_Guidelines.md`**
    *   视觉风格、层级结构、交互反馈。
*   ✅ **[特效规范] `Art/VFX_Standards.md`**
    *   视觉分级、颜色编码、性能优化。
*   ✅ **[Unity 画质指南] `Art/Visual_Quality_Guide.md`** *(新增)*
    *   URP 设置、后处理策略、Linear 空间。
*   ✅ **[摄像机深度指南] `Art/Camera_DeepDive_And_Settings.md`** *(新增)*
    *   FOV 原理、Cinemachine 调优、镜头美学。

---

## 6. 生产与实战 (Production)
*   ✅ **[开发避坑指南] `Dev_Guides/Production_Lessons.md`**
*   ✅ **[Unity 实战技巧] `Dev_Guides/Unity_Practical_Tips.md`**

---

## 7. 技术实现与案例 (Technical Implementation & Cases)
*定义游戏的"肌肉"——具体如何实现和业界成功经验。*

### 🔧 技术实现深度案例
*   ✅ **[PRD算法完整实现] `Dev_Guides/Technical_Implementation/PRD_Algorithm_Complete.md`**
    *   8位计数器实现、性能优化、向量化计算、Intervention-PRD电竞模式。
*   ✅ **[ECS性能优化实战] `Dev_Guides/Technical_Implementation/ECS_Performance_Optimization.md`**
    *   Vampire Survivors案例分析：500单位同屏优化，内存带宽降低80%。
*   ✅ **[GPU Instancing渲染优化] `Dev_Guides/Technical_Implementation/GPU_Instancing_Guide.md`**
    *   15k精灵1 Draw-call实现，Unity/UE5具体代码示例。
*   ✅ **[掉落蓄水池算法实现] `Dev_Guides/Technical_Implementation/Loot_Reservoir_Algorithm.md`**
    *   DPM恒定2.0的权重预算制，0 GC实现方案。
*   ✅ **[全局埋点实战指南] `Dev_Guides/Technical_Implementation/Game_Analytics_Guide.md`** *(新增)*
    *   漏斗模型设计、经济与战斗核心埋点清单、反作弊数据监控。
*   🚧 **[游戏开发最佳实践] `Dev_Guides/Technical_Implementation/Game_Dev_Best_Practices.md`** *(新增)*
    *   ScriptableObject Tag系统、Unity热重载方案、开发者控制台与快速测试。
*   🚧 **[SO与Excel工作流对比] `Dev_Guides/Technical_Implementation/ScriptableObject_vs_Excel_Workflow.md`** *(新增)*
    *   自动化引用绑定、编辑器扩展(PropertyDrawer)、Excel转SO混合管线。
*   🚧 **[技能文本配置系统] `Dev_Guides/Technical_Implementation/Skill_Text_Localization_System.md`** *(新增)*
    *   富文本语义标签、动态参数注入、ICU多语言支持。
*   🚧 **[技能动画管线] `Dev_Guides/Technical_Implementation/Skill_Animation_Pipeline.md`** *(新增)*
    *   摒弃Animation Event，拥抱可视化Timeline与逻辑驱动表现。

### 🎮 业界成功案例深度剖析
*   ✅ **[Bloons TD6伤害矩阵系统] `Dev_Guides/Industry_Cases/Bloons_TD6_Damage_Matrix.md`**
    *   11×9完整免疫矩阵分析，如何通过"0伤害"强制多元化建塔。
*   ✅ **[Kingdom Rush四维数值模型] `Dev_Guides/Industry_Cases/Kingdom_Rush_Numerical_Model.md`**
    *   数量、血量、速度、时间四维控制，兵营时间放大器机制。
*   ✅ **[Hades 225种Build多样性] `Dev_Guides/Industry_Cases/Hades_Build_Diversity.md`**
    *   双层标签系统设计，主标签+副标签的225条机制轨道。
*   ✅ **[Vampire Survivors性能奇迹] `Dev_Guides/Industry_Cases/Vampire_Survivors_Performance.md`**
    *   ECS+DOTS架构详解，经验宝石合并算法，PRD随机性优化。
*   🚧 **[Cyberpunk 2077流式技术] `Dev_Guides/Industry_Cases/Cyberpunk2077_Streaming_Tech.md`** *(新增)*
    *   REDengine 4 任务系统、异步资产解压、无缝世界构建。
*   🚧 **[Palworld 生产模式分析] `Dev_Guides/Industry_Cases/Palworld_Production_Model.md`** *(新增)*
    *   Triple-I 崛起，虚幻5管线自动化与核心玩法缝合的成功学。

### 💥 失败案例教训分析
*   ✅ **[Battleborn失败深度剖析] `Dev_Guides/Failure_Cases/Battleborn_Failure_Analysis.md`**
    *   TTK思维冲突，数值公式缺陷，滚雪球机制失控。
*   ✅ **[Paragon复杂度陷阱] `Dev_Guides/Failure_Cases/Paragon_Complexity_Trap.md`**
    *   TPS+MOBA+卡牌三重机制叠加，3D视角平衡性不可行。
*   🚧 **[Anthem 生产危机] `Dev_Guides/Failure_Cases/Anthem_Production_Crisis.md`** *(新增)*
    *   引擎错配(Frostbite)、预制作缺失、决策瘫痪与"Bioware Magic"迷信。
*   🚧 **[Concord 市场分析] `Dev_Guides/Failure_Cases/Concord_Market_Analysis.md`** *(新增)*
    *   Hero Shooter 红海竞争、角色设计"委员会化"、定价策略失误。
*   🚧 **[The Day Before 营销陷阱] `Dev_Guides/Failure_Cases/The_Day_Before_Marketing_Trap.md`** *(新增)*
    *   资产翻模(Asset Flip)、技术验证缺失、营销诈骗的法律后果。

---

## 8. 实用工具与模板 (Tools & Templates)
*提供可直接使用的开发资源和工具。*

### 🛠️ 开发工具与插件
*   ✅ **[Excel三表法数值模板] `Dev_Guides/Tools/Excel_Numerical_Templates.md`**
    *   参数表/计算表/校验表分离，支持Google Sheet+AppScript热更新。
*   ✅ **[Unity PRD算法插件] `Dev_Guides/Tools/Unity_PRD_Plugin.md`**
    *   Jobs System兼容的C#实现，向量化优化版本。
*   ✅ **[AI平衡测试工具] `Dev_Guides/Tools/AI_Balance_Testing.md`**
    *   Claude/GPT-4o自动测试脚本，20美元成本跑6轮迭代。
*   ✅ **[战斗仿真系统] `Dev_Guides/Tools/Combat_Simulation_System.md`**
    *   Headless版本1秒1万局，Python实现，输出胜率/伤害分布。

### 📊 实用计算器与可视化
*   ✅ **[数值计算器套装] `Dev_Guides/Tools/Numerical_Calculator_Suite.md`**
    *   TTK/DPS/EHP计算器，随机分布可视化，经济系统平衡校验。
*   ✅ **[性能监控脚本集] `Dev_Guides/Tools/Performance_Monitoring_Scripts.md`**
    *   帧时间统计、内存泄漏检测、移动游戏性能分析。

---

## 9. 团队协作与生产流程 (Team Collaboration)
*定义高效的团队协作方式。*

### 🤝 敏捷开发实践
*   ✅ **[独立游戏团队Scrum实施] `Dev_Guides/Collaboration/Agile_For_Indie_Teams.md`**
    *   2周冲刺周期，策划-程序-美术每日站会，Demo日展示机制。
*   ✅ **[跨时区远程协作指南] `Dev_Guides/Collaboration/Remote_Collaboration.md`**
    *   Slack+Notion+Perforce工具链，时区重叠4小时工作制。

### 📈 项目管理与质量控制
*   ✅ **[里程碑规划模板] `Dev_Guides/Collaboration/Milestone_Planning.md`**
    *   Vertical Slice→Alpha→Beta→Gold完整流程，风险评估清单。
*   ✅ **[Beta测试与用户反馈] `Dev_Guides/Collaboration/Beta_Testing_Guide.md`**
    *   Steam Playtest申请流程，用户反馈分类处理，数据驱动迭代。

---

## 10. 实时运营 (LiveOps)
*定义长线运营的策略与经济模型。*

*   🚧 **[通行证经济学] `Design/LiveOps/Battle_Pass_Economy.md`** *(新增)*
    *   40天周期法则、价值锚定(8-10倍收益)、免费/付费转化逻辑。
*   🚧 **[活动排期策略] `Design/LiveOps/Event_Cadence_Strategy.md`** *(新增)*
    *   宏观/微观/变现活动分层，避免长草期与疲劳期。

---

## 🗓️ 状态总结 (Status Summary)

**🎉 文档主体结构已完成 (100%)，关键技术与案例分析文档已补充。**
项目已具备进入 **Vertical Slice (垂直切片)** 开发阶段的理论基础。

**文档增强进度:**
✅ **核心技术架构**: FSM 状态机、Luban 导表流程、Shader 核心数学、移动端优化指南
✅ **技术实现深度**: PRD算法、ECS优化、GPU Instancing、掉落蓄水池算法、全局埋点指南、游戏开发最佳实践、SO与Excel工作流对比、技能文本配置系统
✅ **业界成功案例**: Bloons TD6、Kingdom Rush、Hades、Vampire Survivors、Cyberpunk 2077流式技术、Palworld生产模式
✅ **失败案例教训**: Battleborn、Paragon、Anthem生产危机、Concord市场分析、The Day Before营销陷阱
✅ **实用工具开发**: Excel三表法、Unity PRD插件、AI平衡测试、战斗仿真、数值计算器、性能监控脚本
✅ **团队协作**: 敏捷开发、远程协作、里程碑规划、Beta测试指南
✅ **实时运营策略**: 通行证经济学、活动排期策略

**Next Steps:**
1.  **执行里程碑计划**: 启动 Vertical Slice 开发。
2.  **搭建数据后台**: 参考《全局埋点指南》接入 Analytics SDK。
3.  **整合工具链**: 将 Unity PRD 插件、性能监控脚本、自定义 Tag 系统工具合入项目主分支。
4.  **制作技能编辑器**: 根据《技能文本配置系统》设计和实现技能描述预览和参数注入工具。
5.  **设计与实现 FSM 框架**: 根据《FSM_Design_Patterns.md》实现怪物 AI 和防御塔状态机。
6.  **确定导表方案**: 根据《Luban 配表指南》结合《SO与Excel工作流对比》制定具体导表流程。
7.  **制作 UI**: 美术团队根据《UI/UX 规范》制作第一版 HUD。
8.  **验证核心数值**: 策划团队使用 `Design/Calculator/index.html` 计算器验证《数值核心》中的公式。