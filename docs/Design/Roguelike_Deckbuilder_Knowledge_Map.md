# 🧙‍♂️ 构建《杀戮尖塔》类游戏知识图谱 (The Knowledge Map of Slay the Spire)

这份文档旨在拆解 Rogue-like Deckbuilder (DBG) 游戏的核心设计知识体系，从数学模型到代码架构，为 Vampirefall 项目提供理论支撑。

## 📚 1. 理论基础 (Theoretical Basis)

### 1.1 核心定义：什么是 Roguelike DBG？

不仅仅是“抽卡打牌”，其核心在于 **“动态构建 (Dynamic Construction)”** 与 **“随机性管理 (Randomness Management)”** 的结合。

- **Deckbuilding (DBG)**: 玩家在游戏过程中不断向牌库添加/移除卡牌，优化卡组结构。
- **Roguelike**: 单向进程、随机遭遇、永久死亡。

### 1.2 数学模型：循环与概率 (The Math of Cycles)

在设计此类游戏时，几个关键的数学指标决定了体验的基调：

#### A. 牌库循环率 (Deck Cycling Rate)

衡量玩家多久能重新抽到核心卡牌。

$$CyclingRate = \frac{DrawPerTurn + ExtraDraw}{DeckSize}$$

- **StS 经验**: 初始卡组小（10-12 张），每回合抽 5 张，意味着大概 2-3 回合就能过穿一次牌库。这种**高频循环**是策略稳定性的来源。
- **Vampirefall 应用**: 我们的“塔防卡组”如果过大，玩家会从“构筑者”变成“赌徒”。建议保持小而精的卡池。

#### B. 输入随机性 vs 输出随机性 (Input vs Output Randomness)

- **输入随机性 (Input)**: 下一回合抽到什么牌？怪物要做什么？（StS: 已知怪物意图，已知手牌）-> **这是策略空间**。
- **输出随机性 (Output)**: 这张卡打出去造成 10-20 点伤害。（StS: 几乎没有）-> **这是挫败感来源**。
- **结论**: 尽可能消除输出随机性，最大化输入随机性的透明度。

### 1.3 设计心理学：权衡与博弈

- **损失厌恶 (Loss Aversion)**: 为什么“移除一张牌”往往比“获得一张金卡”更强？因为精简卡组能提高核心卡的上手率。
- **协同效应 (Synergy)**: 1+1 > 2 的快感。例如“毒”机制：叠毒层数 -> 翻倍毒层数。这种**指数级爆发**是玩家追求的终极快感。

### 1.4 Roguelike 宏观循环 (The Macro Loop)

一个成熟的 DBG 循环由微观（局内）和宏观（局外）两个闭环组成：

1.  **微观战斗 (The Encounter)**: 抽牌 -> 决策 -> 结算 -> 敌方行动。
2.  **中观构建 (The Run)**:

    - **战斗 (Combat)**: 验证当前卡组强度。
    - **奖励 (Reward)**: 获得新卡/遗物 (金币/卡牌/药水)。
    - **删减 (Removal)**: 去除杂质 (商店/事件)。
    - **强化 (Upgrade)**: 提升核心卡数值 (火堆)。
    - **决策 (Routing)**: 选择风险与收益的路径 (打精英还是回血？)。

### 1.5 数值膨胀控制模型 (Controlling Power Creep)

DBG 游戏的玩家伤害通常呈**指数级增长** (Exponential)，而传统 RPG 怪物血量通常是**线性增长** (Linear)。为了防止游戏在后期变得过于割草或不可战胜，需要引入以下控制模型：

- **怪物血量曲线 (HP Curve)**: 必须配合玩家的协同效应进行**分段指数增长**。
    - 第一阶段 (线性): Act 1，玩家卡组未成型。
    - 第二阶段 (指数): Act 2-3，玩家获得关键遗物/Key Card，伤害爆发。
- **软上限机制 (Soft Caps)**:
    - **伤害上限**: 单次伤害不超过 999 (如 StS 的心脏)。
    - **无敌机制**: 强制锁血或无敌回合 (Time Eater 的 12 张牌限制)。
- **怪物反制 (Counter-Play)**: 不仅仅加血量，而是针对特定流派的机制。
    - 针对高频攻击：反伤怪 (Spiker)。
    - 针对无限流：每回合出牌上限 (Time Eater)。
    - 针对高爆发：重生或多阶段 (Awakened One)。

---

## 🛠️ 2. 实践应用 (Practical Implementation)

### 2.1 Vampirefall 适配策略

本项目是 **塔防 + 肉鸽**，卡牌不仅是“攻击指令”，更是“资源分配”。

- **卡牌类型**:
    - **瞬间型 (Instant)**: 类似于法术，直接对场上怪物造成伤害/控制 (e.g., 火球术, 冻结)。
    - **由于型 (Persistent)**: 放置一座临时防御塔，或给予防御塔一个持续 30s 的 Buff。
    - **经济型 (Economy)**: 牺牲当前战力换取长远收益 (e.g., 献祭一座塔获得金币)。

### 2.2 数据结构 (C# Data Structures)

使用 **ScriptableObject** 构建高度模块化的卡牌系统。

```csharp
// 核心卡牌定义
[CreateAssetMenu(fileName = "NewCard", menuName = "Vampirefall/Card")]
public class CardData : ScriptableObject {
    public string id;
    public string cardName;
    public int energyCost;
    public CardType type;
    public Sprite artwork;
    public List<CardEffect> effects; // 效果链
}

// 效果定义（策略模式）
public abstract class CardEffect : ScriptableObject {
    public abstract void Execute(BattleContext context);
    public abstract string GetDescription();
}

// 具体效果示例：造成伤害
public class EffectDealDamage : CardEffect {
    public int baseDamage;
    public DamageType damageType;

    public override void Execute(BattleContext context) {
        // 计算最终伤害（含遗物/Buff加成）
        int finalDmg = DamageCalculator.Calculate(baseDamage, context.Source, context.Target);
        context.Target.TakeDamage(finalDmg);
    }
}
```

### 2.3 核心架构：命令队列系统 (Command Queue System)

为了解决复杂的结算顺序（例如：打出一张牌 -> 触发遗物 A -> 触发怪物被动 B -> 触发遗物 C），参考 StS 采用 **命令队列模式**。

- **ActionManager**: 维护一个 Queue<GameAction>`。
- **GameAction**: 所有游戏行为的基类（抽牌、造成伤害、获得格挡、等待）。
- **执行流程**:
    1.  玩家打出卡牌 -> 生成多个 Actions 入队。
    2.  队列依次 `Update()` 直到完成 (`isDone`).

    3.  若 Action 触发了新事件（如受伤触发反击），将新 Action **插入队首 (AddToTop)** 或 **队尾 (AddToBottom)**。

#### 伪代码逻辑

```csharp
class ActionManager {
    private List<GameAction> actions = new List<GameAction>();

    void Update() {
        if (actions.Count > 0) {
            var current = actions[0];
            if (!current.hasStarted) current.Start();
            current.Update();
            if (current.isDone) actions.RemoveAt(0);
        }
    }

    void AddToBottom(GameAction action) { actions.Add(action); }
    void AddToTop(GameAction action) { actions.Insert(0, action); }
}
```

---

## 🌟 3. 业界优秀案例 (Industry Best Practices)

### 3.1 Slay the Spire (杀戮尖塔)

- **优点**:
    - **意图系统 (Intent System)**: 极其清晰的信息展示，完全消除了“未知带来的恐惧”，让玩家专注于解题。
    - **遗物系统 (Relics)**: 改变游戏规则的被动道具，极大丰富了重玩价值。
- **借鉴点**: 我们必须在 UI 上明确显示下一波敌人的意图（攻击哪个塔？走哪条路？）。

### 3.2 Monster Train (怪物火车)

- **优点**:
    - **三层防线**: 将战场分为三层，增加了空间策略维度。
    - **英雄升级**: 核心单位（Champion）有多条升级路线。
- **借鉴点**: Vampirefall 的塔防地图本身就是多层/多路径的，可以借鉴其“防线崩溃后退守下一层”的概念。

### 3.3 Inscryption (邪恶冥刻)

- **优点**:
    - **叙事结合**: 打牌不仅仅是打牌，还是在与 DM (Dungeon Master) 博弈。
    - **牺牲机制**: 必须献祭弱小生物才能召唤强大生物。
- **借鉴点**: 我们的“回收塔”机制可以参考牺牲系统——回收一座低级塔，作为召唤高级塔的资源。

---

## 🔗 4. 参考资料 (References)

- 📺 **GDC**: [Slay the Spire: Metrics Driven Design and Balance](https://www.youtube.com/watch?v=0pLPlQ81iWo) (强烈推荐：数值平衡方法论)
- 📺 **GDC**: [The 10 Year Journey of Slay the Spire](https://www.youtube.com/watch?v=JmwcYqtsUj0)
- 📄 **Blog**: [The Design of Slay the Spire](https://www.gamedeveloper.com/design/the-design-of-slay-the-spire)
- 🌐 **Wiki**: [Slay the Spire Wiki - Mechanics](https://slay-the-spire.fandom.com/wiki/Slay_the_Spire_Wiki)
