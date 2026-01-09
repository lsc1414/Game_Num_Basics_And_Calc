---
sidebarTitle: "🎯 索敌机制详解与实战"
---

# 🎯 索敌机制详解与实战 (Targeting System Deep Dive)

本文档基于 [Unified Decision System](../Architecture/Unified_Decision_System.md) 架构，深入解析 Project Vampirefall 中的索敌逻辑。索敌（Targeting）是塔防与 ARPG 的核心交互体验，它决定了玩家感受到的“智能”程度。

---

## 1. 核心原理：从“寻找”到“评分” (From Search to Score)

初级索敌逻辑通常是：“找到最近的敌人”。
但在本作中，索敌是一个 **加权决策过程 (Weighted Decision Process)**。

### 1.1 标准流程
每一次索敌计算 (`Tick`) 都遵循以下管道：

1.  **圈地 (Broad Phase):** 快速获取射程内的所有潜在目标（利用空间划分，如 QuadTree 或 Physics.OverlapSphere）。
2.  **初筛 (Filtering):** 剔除无效目标（无敌状态、隐身状态、已死亡、阻挡视线）。

3.  **评分 (Scoring):** 对剩下的每个目标运行一组 `Scorer`，计算总分。

4.  **择优 (Selection):** 选取分数最高的 Top 1 作为目标。

### 1.2 为什么需要评分制？
*   **防呆:** 防止狙击塔把高额伤害浪费在还有 1HP 的杂兵上（Overkill）。
*   **集火:** 让特定的塔优先攻击被“破甲”或“被标记”的敌人。
*   **风格:** 区分“狂战士”（打最近的）与“刺客”（打最脆的）的行为模式。

---

## 2. 评分维度详解 (Scoring Dimensions)

我们在代码中通过组合不同的 `IScorer` 来实现复杂的战术逻辑。

### 📏 2.1 距离评分 (Distance Scoring)
*   **逻辑:** 距离越近/越远，分数越高。
*   **曲线:** 建议使用非线性曲线。
    *   `Score = 1 / Distance` (极度偏好近身)
    *   `Score = Distance` (偏好远程，如迫击炮无法攻击近身)
*   **应用:** 基础箭塔、近战怪物。

### 🩸 2.2 生命值评分 (Health Scoring)
*   **低血量优先 (Execute / Cleanup):**
    *   **逻辑:** `Score = 1 - (CurrentHP / MaxHP)`。
    *   **用途:** 快速收割残血，减少场上怪物数量，触发击杀特效。
*   **高血量优先 (Giant Slayer):**
    *   **逻辑:** `Score = CurrentHP` 或 `Score = CurrentHP / MaxHP`。
    *   **用途:** 破甲塔、百分比伤害技能，确保高伤打在肉盾上。

### 👑 2.3 优先级评分 (Priority Scoring)
*   **逻辑:** 根据 `EntityType` 给定固定分值。
*   **配置表:**
    *   `Boss`: 1000分
    *   `Elite`: 500分
    *   `Special (炸弹人)`: 2000分 (绝对优先处理)
    *   `Minion`: 10分
*   **用途:** 所有的塔都应该默认带一点优先级，避免被召唤的小怪吸走火力。

### 🌪️ 2.4 状态协同评分 (Status Synergy Scoring)
*   **逻辑:** “趁你病要你命”。如果目标身上有特定的 Debuff，加分。
*   **Combo:**
    *   **雷电塔:** 对 `[Soaked]` (湿润) 的目标评分 x 2.0。
    *   **处决者:** 对 `[Stunned]` (眩晕) 的目标评分 x 3.0。
*   **用途:** 引导玩家构建元素反应链。

---

## 3. 实战案例 (Use Cases)

以下是游戏中几种典型单位的索敌配置方案。

### 🏹 Case A: 基础箭塔 (Basic Ballista)
*定位：清理冲到脸上的杂兵，防漏怪。*

|          评分器          |          权重 (Weight)          |          说明          |
|          :---          |          :---          |          :---          |
|          **DistanceScorer**          |          **3.0**          |          极度优先攻击最近的单位。          |
|          **FixedPriorityScorer**          |          0.5          |          稍微偏好精英怪，但主要还是看距离。          |
|          **HealthScorer (Low)**          |          1.0          |          优先补刀残血。          |

### 🔫 Case B: 狙击塔 (Sniper Turret)
*定位：高单发伤害，极慢攻速。必须避免伤害溢出。*

|          评分器          |          权重 (Weight)          |          说明          |
|          :---          |          :---          |          :---          |
|          **Filter: Overkill**          |          N/A          |          **[关键]** 如果目标的 `HP < 塔攻击力`，直接剔除（防止大炮打蚊子）。          |
|          **FixedPriorityScorer**          |          **5.0**          |          必须优先打 Boss 和 Elite。          |
|          **HealthScorer (High)**          |          2.0          |          在同级怪物中，选血最多的打。          |
|          **DistanceScorer**          |          -0.5          |          稍微偏好远处的（反向权重），避免转火频繁。          |

### ⚡ Case C: 特斯拉电圈 (Tesla Coil)
*定位：AOE 连锁攻击，依赖元素反应。*

|          评分器          |          权重 (Weight)          |          说明          |
|          :---          |          :---          |          :---          |
|          **TagSynergyScorer**          |          **4.0**          |          寻找带有 `[Wet]` 或 `[Conductive]` 标签的敌人。          |
|          **ClusterScorer**          |          2.0          |          **[高级]** 寻找周围敌人最密集的那个点作为主目标（最大化弹射收益）。          |

### 👹 Case D: 刺客型怪物 (Assassin Enemy)
*定位：切后排，恶心玩家。*

|          评分器          |          权重 (Weight)          |          说明          |
|          :---          |          :---          |          :---          |
|          **FixedPriorityScorer**          |          **10.0**          |          `Player` > `SupportTower` > `TankTower`。          |
|          **HealthScorer (Low)**          |          3.0          |          专挑血少的打。          |
|          **DistanceScorer**          |          0.0          |          **无视距离**。哪怕要绕路，也要去切后排。          |

---

## 4. 代码实现片段 (Implementation Snippet)

如何在 Unity 中配置一个“狙击塔”的决策引擎：

```csharp
public class SniperTower : MonoBehaviour 
{
    private DecisionEngine<Enemy> _targetingSystem;
    
    void Start() {
        _targetingSystem = new DecisionEngine<Enemy>();
        
        // 1. 过滤：必须在射程内，且活着
        _targetingSystem.AddFilter(new RangeFilter(transform, 50f));
        _targetingSystem.AddFilter(new AliveFilter());
        
        // 2. 过滤：防止伤害溢出 (Overkill Protection)
        // 假设塔攻击力是 500
        _targetingSystem.AddFilter(new MinHealthFilter(500f)); 

        // 3. 评分：优先打 Boss (权重极高)
        _targetingSystem.AddScorer(new EntityTypeScorer()
            .SetScore(EntityType.Boss, 1000f)
            .SetScore(EntityType.Elite, 500f));

        // 4. 评分：优先打满血的 (权重中等)
        _targetingSystem.AddScorer(new HealthScorer(HealthScorerMode.Highest, 10f));
    }

    void Update() {
        if (Time.frameCount % 10 == 0) { // 分帧优化
            var enemies = EnemyManager.GetAllEnemies();
            var target = _targetingSystem.SelectBest(enemies, GetContext());
            if (target != null) Fire(target);
        }
    }
}
```

## 5. 性能优化与粘性 (Optimization & Stickiness)

### 5.1 目标粘性 (Target Stickiness)
为了防止塔的炮口在两个分数相近的敌人之间疯狂抽搐（Ping-Pong），我们需要引入“粘性”。

*   **机制:** 给 `LastTarget` (上一次锁定的目标) 一个额外的分数加成。
*   **公式:** `Score += (target == LastTarget) ? StickinessBonus : 0;`
*   **效果:** 除非新目标的威胁值显著高于当前目标（例如超过 20%），否则不切换目标。

### 5.2 空间划分 (Spatial Partitioning)
千万不要遍历全图 `EnemyManager.GetAllEnemies()`。

*   使用 **Grid System** 或 **QuadTree**。
*   塔只获取其 `Range` 覆盖的 Grid 内的敌人列表作为 `Candidates`。

### 5.3 协同程序 (Coroutines) / Job System
索敌不需要每帧都跑。

*   每 0.1秒 ~ 0.2秒 更新一次即可。
*   对于大量单位，使用 Unity Job System 并行计算分数。

---
