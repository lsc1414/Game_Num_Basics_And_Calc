现代游戏开发全景：从核心架构到数值经济的深度技术与生产方法论


摘要

游戏开发作为一门融合了计算机科学、认知心理学、视觉艺术与经济学的综合性学科，其复杂性随着硬件性能的提升与市场竞争的加剧而呈指数级增长。本报告旨在构建一个全方位的技术与生产框架，涵盖从底层的内存管理架构（如实体组件系统 ECS）到顶层的数值平衡设计（如战斗公式与经济模型），再到工业化生产流程中的经验教训（Post-mortem）。通过对 Unity DOTS、Unreal Gameplay Ability System (GAS)、REDengine 4 等前沿技术的解构，结合《赛博朋克 2077》、《星鸣特攻》（Concord）、《圣歌》（Anthem）及《黑帝斯》（Hades）等案例的深度剖析，本文为专业开发者提供了一份详尽的行业洞察与实践指南。

1. 核心数值架构与游戏平衡设计

游戏平衡并非追求绝对的数学均等，而是通过数值与机制的耦合，创造出具有动态张力的体验空间。数值设计不仅决定了战斗的节奏，更是构建玩家心流（Flow）与长期留存的基石。

1.1 战斗公式的数学模型与体验映射

战斗公式是RPG与策略游戏的心脏。开发者需要在“减法公式”与“乘除法公式”之间做出根本性的选择，这决定了游戏的数值膨胀速度与策略深度。

1.1.1 线性减法公式的边际效应递减

经典RPG（如《黄金太阳》、《火焰纹章》）常采用直观的线性公式：$伤害 = 攻击 - 防御$。这种设计的核心特征在于其边际效应递减。假设一名角色的攻击力随等级线性增长，从等级2提升至等级3时，攻击力可能增加50%（从10到15），带来的伤害提升极其显著；然而，当从等级50提升至51时，同样的数值增量（从250到255）仅带来约2%的提升 1。
这种数学特性并非设计缺陷，而是有意为之的平衡手段。它服务于两个相互冲突的设计目标：
低等级时的自由度：允许新手玩家通过“练级”（Grinding）产生数值压制，从而通过操作门槛较高的关卡。
高等级时的策略强制：随着等级提升，单纯的数值堆砌收益急剧下降，迫使玩家转向探索装备搭配、技能连携与属性克制等横向策略 1。
然而，减法公式存在“不破防”问题（即攻击<防御时伤害为0或1）。为解决此问题，现代设计常引入“保底伤害”或分段函数，例如设定 $Damage = \max(1, Attack - Defense)$，或者引入穿透属性。

1.1.2 乘除法公式与“有效生命值”模型

为了避免减法公式在数值膨胀后的极端表现，MOBA类游戏（如《英雄联盟》、《Smite》）及现代MMO倾向于使用乘除法公式。其典型形态为：


$$实际伤害 = 理论伤害 \times \frac{C}{C + 防御值}$$

其中 $C$ 为常数（如100）。在此模型下，防御力不再直接抵消伤害，而是提供“有效生命值”（Effective HP, EHP）。每一店防御力提升的生存收益是线性的，不会出现“不破防”或“一击必杀”的阈值突变 2。
这种模型对数值策划极其友好，因为它允许无限的数值成长而不会导致系统崩溃。无论攻击力膨胀到何种程度，只要防御力按比例提升，伤害减免百分比始终由于边际效应控制在合理区间（永远趋近但无法达到100%）。

1.1.3 “50% 陷阱”与非传递性平衡

在平衡性调整中，新手设计师常陷入“50% 陷阱”，即认为所有选项的胜率都应趋近于50%才是完美的平衡。实际上，这种追求会导致游戏体验的同质化（Homogenization）3。
优秀的游戏平衡往往依赖于**非传递性（Intransitivity）**关系，即类似于“剪刀-石头-布”的循环克制：策略A克制B，B克制C，C克制A。这种动态不平衡（Perfect Imbalance）驱使Meta（主流战术环境）不断流动，防止游戏僵化。暴雪娱乐的罗布·帕尔多（Rob Pardo）曾指出，玩家最享受的状态并非“势均力敌”，而是“在此刻拥有微弱优势”，这种“不公平”的快感是游戏娱乐性的来源 3。

> **💡 Vampirefall 应用启示**
> *   **公式选择**: 鉴于 Vampirefall 是塔防+肉鸽，后期数值膨胀不可避免。建议采用 **1.1.2 乘除法公式** (`Dmg = Atk * C / (C + Def)`) 以保证后期防御塔和怪物的数值在可控范围内，避免一击必杀。
> *   **非传递性设计**: 在塔防属性相克中引入 **循环克制** (如: 物理 > 魔法盾 > 元素甲 > 物理)，而非单纯的数值强弱，迫使玩家在构建防线时保持多样性。

1.2 概率算法与扭蛋经济学

在免费游戏（F2P）与服务型游戏（GaaS）中，随机性（RNG）是控制资源产出与玩家情绪的核心机制。

1.2.1 真随机与伪随机分布（PRD）

“真随机”在游戏体验中往往被视为“不公平”。例如，25%的暴击率在真随机下可能出现连续10次不暴击的情况，导致玩家挫败感。为了修正这种体验偏差，游戏（如《Dota 2》、《魔兽争霸3》）采用了伪随机分布（Pseudo-Random Distribution, PRD） 4。
在PRD算法下，显示的25%暴击率实际上对应一个较低的初始概率 $C$（约8.5%）。每次攻击若未触发暴击，下一次的概率会累加 $C$（即第2次为17%，第3次为25.5%...），直到触发暴击后概率重置。这种算法收束了方差，消除了极端的好运或厄运，使实际体验更符合人类对“25%”的直觉认知。

1.2.2 扭蛋（Gacha）概率与保底机制

扭蛋系统的数学模型通常基于伯努利试验的二项分布，获得至少一次稀有物品的概率公式为 $P = 1 - (1-p)^n$，其中 $p$ 为单次概率，$n$ 为抽取次数 5。为了防止“非酋”玩家流失，现代Gacha普遍引入“保底机制”（Pity System）：
硬保底（Hard Pity）：在第 $N$ 次抽取时，若此前未获得目标，则概率强制变为100%。这种设计透明但缺乏过程激励。
软保底（Soft Pity/Ramping Probability）：如《原神》或《明日方舟》的设计。在达到某个阈值（如74抽）前，概率保持低位（0.6%）；超过阈值后，单次概率线性暴增（如每抽增加6%），直至必中。这种S型曲线设计利用了赌徒谬误，让玩家在接近保底时产生强烈的“即将中奖”的心理预期，从而刺激付费 6。

> **💡 Vampirefall 应用启示**
> *   **PRD 实施**: 游戏内的暴击、闪避、特殊词条触发 **必须** 使用 PRD 算法。参考 `Dev_Guides/Technical_Implementation/PRD_Algorithm_Complete.md` 中的实现。
> *   **保底设计**: 针对肉鸽局外抽取（如有），应设计 **软保底** 机制，利用 S 型概率曲线提升玩家在接近保底时的期待感和留存率。

1.3 经济系统模型与通胀控制

虚拟经济系统本质上是一个通过“源头”（Sources/Taps）与“汇点”（Sinks/Drains）控制资源流动的封闭或半封闭系统 8。

1.3.1 通胀的必然性与对抗手段

与现实经济不同，游戏中的资源通常是凭空产生的（如击杀怪物掉落金币），这导致恶性通胀是MMORPG的宿命。如果缺乏有效的回收机制，货币贬值将摧毁交易系统。
有效的对抗手段包括：
动态汇点（Dynamic Sinks）：随着玩家资产增加，消耗呈指数级上升。例如，装备强化从+9到+10的费用可能是+1到+2的千倍，且伴随失败碎装备的风险（资产销毁）9。
交易损耗（Transaction Tax）：拍卖行收取的手续费是控制流通速度的关键手段。
拾取绑定（Bind on Pickup/Equip）：强行将高价值资产移出流通领域，防止其无限转手导致的市场饱和。

> **💡 Vampirefall 应用启示**
> *   **监控体系**: 从项目初期建立 **Sources vs Sinks** 埋点，实时监控每日产出销毁比（目标值应维持在 0.9~1.1 区间，活动期可波动）。
> *   **动态回收**: 强化系统应设计 **指数级消耗曲线**，作为后期的主要金币回收口。

2. 现代游戏引擎的架构范式与工程实践

随着开放世界规模的扩大和同屏单位数量的激增，传统的面向对象编程（OOP）已难以满足性能需求。面向数据设计（Data-Oriented Design, DOD）的兴起标志着游戏工程架构的重大转型。

2.1 实体组件系统（ECS）与内存布局优化

传统的“Actor-Component”模式在内存中是离散存储的，导致CPU在遍历对象时频繁发生缓存未命中（Cache Miss），严重制约性能。ECS架构通过重新组织内存布局解决了这一问题。

2.1.1 核心概念与内存连续性

ECS 将游戏对象解构为三个部分：
Entity（实体）：仅是一个唯一的ID，不包含数据或逻辑。
Component（组件）：纯数据结构（Struct），如 Position、Velocity，不包含任何函数。
System（系统）：纯逻辑，负责处理拥有特定组件集合的实体。
这种架构允许将同一类型的组件（如所有实体的 Velocity 数据）在内存中连续紧密排列。当系统遍历这些数据时，CPU 可以利用预取（Prefetching）机制高效地将数据块加载到L1/L2缓存中，极大提升了处理速度，并便于SIMD（单指令多数据流）指令的向量化运算 12。

> **💡 Vampirefall 应用启示**
> *   **怪物海优化**: 核心战斗中的大量怪物（500+ 同屏）应采用 **Unity DOTS (ECS)** 技术栈实现，确保在移动端也能稳定 60FPS。
> *   **内存布局**: 遵循 **Data-Oriented** 原则，将高频访问的组件（如位置、血量）紧凑排列，利用 `Burst Compiler` 优化计算密集型逻辑。

2.2 Gameplay Ability System (GAS) 的深度解析

Unreal Engine 的 Gameplay Ability System (GAS) 是目前工业界处理复杂战斗逻辑（尤其是MMORPG和MOBA）的标准解决方案。它提供了一套高度解耦且支持网络复制的框架 19。

2.2.1 架构组件详解

Ability System Component (ASC)：核心组件，作为所有技能交互的中枢，挂载在角色（Avatar）上。
AttributeSet：存储浮点数属性（如生命值、法力值、攻击力）。它不仅是数据容器，还负责属性变更时的逻辑钩子。
GameplayEffect (GE)：改变属性的唯一途径。GE 定义了修改方式（加法、乘法、覆盖）、持续时间（瞬时、无限、时限）以及叠加规则。GE 是纯数据资产，不包含逻辑代码，保证了设计师在调整数值时的安全性 19。
GameplayTag：层级化的标签系统（如 State.Debuff.Stun）。GAS 利用标签进行极其高效的交互判定。

> **💡 Vampirefall 应用启示**
> *   **技能架构**: 即使不使用 UE，也应参考 GAS 的设计思想。实现一套 **基于 Tag 的状态判断系统** 和 **纯数据驱动的 Effect 系统**。
> *   **Buff 管理**: 所有的 Buff/Debuff 应统一管理，通过 Tag 处理互斥（如“免疫冰冻” Tag 自动免疫所有带有“冰冻” Tag 的 Effect）。

2.3 网络同步策略：帧同步与状态同步

多人游戏的网络架构选择取决于游戏类型对延迟和一致性的容忍度。

2.3.1 帧同步（Lockstep）
原理：客户端仅发送操作指令，所有客户端执行完全相同的逻辑。
优势：极低带宽，防作弊，适合 RTS/格斗。
劣势：确定性地狱，手感“粘滞”。

2.3.2 状态同步（State Sync）
原理：服务器模拟世界，发送快照。
优势：抗网络抖动，断线重连，适合 FPS/MMO。

> **💡 Vampirefall 应用启示**
> *   **模式选择**: 若为纯 PVE 塔防，**状态同步** 是更稳妥的选择，便于防作弊和逻辑拓展。若包含高频竞技场，可考虑局部帧同步，但考虑到开发成本，推荐优先完善 **状态同步 + 客户端预测**。

3. 技术美术与渲染管线的极致优化

技术美术（Technical Artist, TA）是连接艺术创意与硬件算力的桥梁。在现代3D流程中，TA不仅要编写Shader，还需构建资产管线并进行极其严苛的性能优化。

3.1 Shader 编程中的核心向量数学

3.1.1 点积（Dot Product）
光照计算、边缘光、视野检测。
3.1.2 叉积（Cross Product）
法线计算、坐标系构建。
3.1.3 插值与平滑（Smoothstep）
程序化纹理抗锯齿、软溶解。

3.2 移动端Shader优化指南

移动GPU（如Adreno, Mali）通常采用**TBDR（Tile-Based Deferred Rendering）**架构。
避免Overdraw（过度绘制）：透明物体在TBDR下极其昂贵。
精度控制：强制使用 half（16位浮点）代替 float。
计算转移：将计算从像素着色器转移到顶点着色器。

> **💡 Vampirefall 应用启示**
> *   **移动端规范**: 严格执行 Shader 精度审查，除位置坐标外，颜色、UV 等计算强制使用 `half/min16float`。
> *   **特效优化**: 粒子特效需严格控制 Overdraw，对于大面积半透明效果（如毒圈），考虑使用 **Mesh 替代 Billboard** 或 **低分辨率渲染目标**。

4. 工业化生产流程与项目复盘（Post-Mortem）

4.1 失败案例剖析：管理混乱与市场错位

4.1.1 《圣歌》（Anthem）
**教训**: 引擎错配（Frostbite 不适合 RPG）与预制作（Pre-production）缺失。
4.1.2 《星鸣特攻》（Concord）
**教训**: 市场迟钝（进入饱和 Hero Shooter 市场）与角色设计平庸（缺乏剪影辨识度）。
4.1.3 《浩劫前夕》（The Day Before）
**教训**: 营销诈骗与资产翻模（Asset Flipping），缺乏底层技术支撑。

4.2 成功案例：迭代主义与系统深度

4.2.1 《黑帝斯》（Hades）
**经验**: “游戏本身就是设计文档”，利用 Early Access 进行高频迭代，代码架构支持极高的模块化（Boons 组合）。

> **💡 Vampirefall 应用启示**
> *   **原型先行**: 在进入量产前，必须完成 **Vertical Slice (垂直切片)**，验证核心玩法循环的乐趣。
> *   **市场定位**: 避免盲目追逐热点，深耕 **塔防 + Roguelike** 的垂直细分领域，注重玩法的深度而非单纯的画面堆砌。
> *   **角色设计**: 角色必须通过 **剪影测试**，确保在移动端小屏幕上依然具有高辨识度。

5. 实时运营（LiveOps）与游戏即服务（GaaS）

5.1 经济通胀的监控与干预
像中央银行一样监控 Sources vs. Sinks，使用动态定价和活动回收控制通胀。

5.2 战斗通行证（Battle Pass）的40天平衡法则
周期设计：40天覆盖两个发薪周期。
价值锚定：8-10倍返利，转化低付费用户。

5.3 活动日历（Event Calendar）的分层策略
宏观活动（赛季）、微观活动（双倍掉落）、变现活动（礼包）交错安排。

> **💡 Vampirefall 应用启示**
> *   **LiveOps 规划**: 运营活动不应是上线后才考虑的，需在 **立项阶段** 就规划好活动排期框架。
> *   **Battle Pass**: 设计双轨制 Battle Pass，免费线提供 **核心游戏体验道具**（如基础防御塔），付费线提供 **外观与加速道具**，避免 Pay-to-Win 导致的口碑崩盘。

6. 结论与未来展望

现代游戏开发已不再是单一维度的挑战。一个成功的项目需要架构的前瞻性、数值的严谨性、流程的迭代性和市场的敏锐度。未来的游戏开发将更加依赖工具化和自动化，但核心的系统设计能力依然是不可替代的。

参考文献索引

数值与平衡：.1
架构与编程：.12
美术与渲染：.27
生产与案例：.40
引用的著作
(参考文献列表同原文，此处省略以节省篇幅)
mathematics - How do RPGs balance linear damage formulas ..., 访问时间为 十二月 2, 2025， https://gamedev.stackexchange.com/questions/112021/how-do-rpgs-balance-linear-damage-formulas
What are common damage formulas for games that have attack and defense stats? - Reddit, 访问时间为 十二月 2, 2025， https://www.reddit.com/r/gamedesign/comments/pxhx8d/what_are_common_damage_formulas_for_games_that/
Video Game Balance: A Definitive Guide - Game Design Skills, 访问时间为 十二月 2, 2025， https://gamedesignskills.com/game-design/game-balance/
The Two Types of Random | Game Maker's Toolkit - Reddit, 访问时间为 十二月 2, 2025， https://www.reddit.com/r/Games/comments/eor5j6/the_two_types_of_random_game_makers_toolkit/
Calculating Gacha Rates (or, Why 1-(1-p)^n is Your Best Friend) - Reddit, 访问时间为 十二月 2, 2025， https://www.reddit.com/r/DragaliaLost/comments/esxdky/calculating_gacha_rates_or_why_11pn_is_your_best/
Mapping out Gacha Pull Probabilities using Python and Google Colaboratory, 访问时间为 十二月 2, 2025， https://dev.to/sr229/mapping-out-gacha-pull-probabilities-in-google-colaboratory-3ij9
Gacha Simulation using Monte Carlo Method in R | Towards Data Science, 访问时间为 十二月 2, 2025， https://towardsdatascience.com/gacha-simulation-using-monte-carlo-method-in-r-3897ce611458/
Game Economy Design: Understanding the Art of Balance - 300Mind, 访问时间为 十二月 2, 2025， https://300mind.studio/blog/what-is-game-economy-design/
19 tips to successfully improve your Game Economy - Machinations.io, 访问时间为 十二月 2, 2025， https://machinations.io/articles/19-tips-to-successfully-improve-your-game-economy
Games Design Diagram Examples: Build The Perfect Player Experience - Machinations.io, 访问时间为 十二月 2, 2025， https://machinations.io/articles/games-design-diagram-examples
Machinations, A New way to Design Game Mechanics, 访问时间为 十二月 2, 2025， http://www.designersnotebook.com/Columns/116_Machinations/116_machinations.htm
Entity component system - Wikipedia, 访问时间为 十二月 2, 2025， https://en.wikipedia.org/wiki/Entity_component_system
SanderMertens/ecs-faq: Frequently asked questions about Entity Component Systems, 访问时间为 十二月 2, 2025， https://github.com/SanderMertens/ecs-faq
Deep-diving into Entity Component System (ECS) Architecture and Data Oriented Programming - PRDeving, 访问时间为 十二月 2, 2025， https://prdeving.wordpress.com/2023/12/14/deep-diving-into-entity-component-system-ecs-architecture-and-data-oriented-programming/
How to Optimize Performance for Large Open Worlds in Unity? - Reddit, 访问时间为 十二月 2, 2025， https://www.reddit.com/r/unity/comments/1ozcic8/how_to_optimize_performance_for_large_open_worlds/
Simulating 5000 Zombies Using Mass Entity ECS Framework : r/unrealengine - Reddit, 访问时间为 十二月 2, 2025， https://www.reddit.com/r/unrealengine/comments/1o1rvo3/simulating_5000_zombies_using_mass_entity_ecs/
Megafunk/MassSample: My understanding of Unreal Engine 5's experimental ECS plugin with a small sample project. - GitHub, 访问时间为 十二月 2, 2025， https://github.com/Megafunk/MassSample
Mass Framework in Unreal Engine - Vrealmatic.com, 访问时间为 十二月 2, 2025， https://vrealmatic.com/unreal-engine/mass
Overview - Gamedev Guide, 访问时间为 十二月 2, 2025， https://ikrima.dev/ue4guide/gameplay-programming/gameplay-ability-system/epic-technical-brief/
tranek/GASDocumentation: My understanding of Unreal ... - GitHub, 访问时间为 十二月 2, 2025， https://github.com/tranek/GASDocumentation
Mastering the Gameplay Ability System: Epic's Guide for Your RPG - Biunivoca, 访问时间为 十二月 2, 2025， https://www.biunivoca.com/en/blog/mastering-the-gameplay-ability-system-epic-s-guide-for-your-rpg
Unreal Engine 5 - The truth of the Gameplay Ability System - Devtricks, 访问时间为 十二月 2, 2025， https://vorixo.github.io/devtricks/gas/
Understanding Gameplay Effect Execution Calculations! - The Games Dev, 访问时间为 十二月 2, 2025， https://www.thegames.dev/?p=119
Game server synchronization of large amounts of data in a battle ..., 访问时间为 十二月 2, 2025， https://engineering.monstar-lab.com/en/post/2021/02/09/Game-server-Synchronization/
How do multiplayer games sync their state? Part 1 | by Qing Wei Lim - Medium, 访问时间为 十二月 2, 2025， https://medium.com/@qingweilim/how-do-multiplayer-games-sync-their-state-part-1-ab72d6a54043
Shader Basics - A Primer On Needed Mathematics, 访问时间为 十二月 2, 2025， https://shader-tutorial.dev/basics/mathematics/
Basic Math for Shaders – Linden Reid, 访问时间为 十二月 2, 2025， https://lindenreidblog.com/2018/08/25/basic-math-for-shaders/
Dot Product is the coolest math in shaders | by Mikołaj Fabjański - Medium, 访问时间为 十二月 2, 2025， https://medium.com/@adder1812/dot-product-is-the-coolest-math-in-shaders-e5baa66a9bbf
The Cross Product - For 3D Artists - Andy Green, 访问时间为 十二月 2, 2025， https://andytech.art/the-cross-product-for-3d-artists
Math + Art | Dot and Cross Product Made Easy! - YouTube, 访问时间为 十二月 2, 2025， https://www.youtube.com/watch?v=t8uQoJGEafg
Math Material Expressions in Unreal Engine - Epic Games Developers, 访问时间为 十二月 2, 2025， https://dev.epicgames.com/documentation/en-us/unreal-engine/math-material-expressions-in-unreal-engine
Building Night City: The Technology of 'Cyberpunk 2077' - GDC Vault, 访问时间为 十二月 2, 2025， https://www.gdcvault.com/play/1028734/Building-Night-City-The-Technology
Anatomy of a frame in Cyberpunk 2077: Phantom Liberty - GDC Vault, 访问时间为 十二月 2, 2025， https://uat.gdcvault.com/play/mediaProxy.php?sid=1034333
The Job System in 'Cyberpunk 2077': Scaling Night City on the CPU - GDC Vault, 访问时间为 十二月 2, 2025， https://gdcvault.com/play/1034296/The-Job-System-in-Cyberpunk
Art optimization tips for mobile game developers part 1 - Unity, 访问时间为 十二月 2, 2025， https://unity.com/how-to/mobile-game-optimization-tips-part-1
Automated Asset Optimization for Mobile Games with Simplygon - Microsoft Developer, 访问时间为 十二月 2, 2025， https://developer.microsoft.com/en-us/games/articles/2025/10/automated-asset-optimization-for-mobile-games-with-simplygon/
Mobile Game Rendering Optimization On Android: Expert Tips, 访问时间为 十二月 2, 2025， https://www.plsevery.com/blog/mobile-game-rendering-optimization-on
Materials and Shaders | Android Developers, 访问时间为 十二月 2, 2025， https://developer.android.com/games/optimize/materials
Optimize shaders - Unity - Manual, 访问时间为 十二月 2, 2025， https://docs.unity3d.com/6000.2/Documentation/Manual/SL-ShaderPerformance.html
Former BioWare Executive Producer Breaks Down 'What Really Happened' to Anthem - IGN, 访问时间为 十二月 2, 2025， https://www.ign.com/articles/former-bioware-executive-producer-breaks-down-what-really-happened-to-anthem
TLDR summary of Jason Schreier Kotaku article about ANTHEM development. : r/AnthemTheGame - Reddit, 访问时间为 十二月 2, 2025， https://www.reddit.com/r/AnthemTheGame/comments/b8myma/tldr_summary_of_jason_schreier_kotaku_article/
Concord's Failure: Why Did the PlayStation Game Flop? - Smart.DHgate – Trusted Buying Guides for Global Shoppers, 访问时间为 十二月 2, 2025， https://smart.dhgate.com/concords-failure-why-did-the-playstation-game-flop-4/
Case Study: Why Concord Failed - Burhan Zamri - Medium, 访问时间为 十二月 2, 2025， https://burhanzamri.medium.com/case-study-why-concord-failed-61d611c092a7
Why Concord Failed: A Game Developer Explains Character Design : r/KotakuInAction, 访问时间为 十二月 2, 2025， https://www.reddit.com/r/KotakuInAction/comments/1fab04u/why_concord_failed_a_game_developer_explains/
Concord, Fighting Games, and Why Character Designs Matter…A Lot | by Letters From the Arcade, 访问时间为 十二月 2, 2025， https://lettersfromthearcade.medium.com/concord-fighting-games-and-why-character-designs-matter-a-lot-2f0584869500
The Day Before Devs Explain Why The Game Failed - TheGamer, 访问时间为 十二月 2, 2025， https://www.thegamer.com/the-day-before-failure-explained-by-devs-marketing/
Why The Day Before Is Something Much Worse Than The Worst Game of 2023, 访问时间为 十二月 2, 2025， https://www.denofgeek.com/games/why-the-day-before-is-something-much-worse-than-the-worst-game-of-2023/
"The game is the design document": Hades 2 devs don't have "long, elaborate" plans that "lay out the future of the things we're making" because Supergiant is "a heavily iterative studio" - GamesRadar, 访问时间为 十二月 2, 2025， https://www.gamesradar.com/games/hades/the-game-is-the-design-document-hades-2-devs-dont-have-long-elaborate-plans-that-lay-out-the-future-of-the-things-were-making-because-supergiant-is-a-heavily-iterative-studio/
A detailed look at the development of Hades and how Supergiant Games designed it with Early Access in mind from the very beginning. : r/gamedev - Reddit, 访问时间为 十二月 2, 2025， https://www.reddit.com/r/gamedev/comments/pngmth/a_detailed_look_at_the_development_of_hades_and/
The 2024 Indie Game Landscape: Why Luck Plays a Major Role in Success on Steam, 访问时间为 十二月 2, 2025， https://shahriyarshahrabi.medium.com/the-2024-indie-game-landscape-why-luck-plays-a-major-role-in-success-on-steam-c6cbc1868c35
Global Indie Games Market Report 2024, 访问时间为 十二月 2, 2025， https://app.sensortower.com/vgi/assets/reports/VGI_Global_Indie_Games_Market_Report_2024.pdf
Game systems: Battle passes and how to balance them - Machinations.io, 访问时间为 十二月 2, 2025， https://machinations.io/articles/battle-passes-and-how-to-balance-them
Get Ready For Winter 2025: LiveOps Tactics That Worked - AppMagic, 访问时间为 十二月 2, 2025， https://appmagic.rocks/blog/Winter-LiveOps-2025
Render pipelines - Unity - Manual, 访问时间为 十二月 2, 2025， https://docs.unity3d.com/6000.2/Documentation/Manual/render-pipelines.html
Art optimization tips for mobile game developers part 2 - Unity, 访问时间为 十二月 2, 2025， https://unity.com/how-to/mobile-game-optimization-tips-part-2
Sony shutting down Seattle-area game developer Firewalk Studios - GeekWire, 访问时间为 十二月 2, 2025， https://www.geekwire.com/2024/sony-shutting-down-seattle-area-game-developer-firewalk-studios/

<script type="text/javascript" id="MathJax-script" async
  src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js">
</script>
<script>
  MathJax = {
    tex: {
      inlineMath: [['$', '$'], ['\\(', '\\)']]
    }
  };
</script>