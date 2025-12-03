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
*   **[📧 邮件系统](Design/Systems/Mail_System_Design.md):** 异步通信、生命周期管理 (TTL)、一键领取交互。
*   **[LiveOps 运营](Design/LiveOps/Advanced_LiveOps_Systems.md):** 
    *   **[战斗通行证经济](Design/LiveOps/Battle_Pass_Economy.md):** 40天周期、价值锚定。
    *   **[活动排期策略](Design/LiveOps/Event_Cadence_Strategy.md):** 宏观/微观活动分层。

#### 内容与世界
*   **[怪物图鉴](Design/Content/Enemy_Bestiary.md):** 怪物分级、AI 行为模板、特殊词缀。
*   **[关卡设计](Design/Content/Level_Design_Guide.md):** 地图生成逻辑、波次节奏控制。

#### 理论基础
*   **[设计哲学](Design/Philosophy_And_Systems.md):** 核心循环、玩家心理模型。
*   **[竖屏 vs 横屏策略](Design/Product_Strategy/Screen_Orientation_Strategy.md):** 用户场景分析与品类选择建议。
*   **[案例分析](Design/Industry_CaseStudies.md):** 竞品分析 (PoE, Vampire Survivors)。

### 2. 📈 生产与指南 (The "Muscle")
#### 技术实现
*   **[ECS 性能优化](Dev_Guides/Technical_Implementation/ECS_Performance_Optimization.md):** DOTS 实践、内存布局优化。
*   **[Gameplay Ability System](Tech/Gameplay_Ability_System_Design.md):** 技能系统设计。


---

*Project maintained by the Vampirefall Team.*