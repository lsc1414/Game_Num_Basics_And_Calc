---
sidebarTitle: "决策系统综合指南"
---

# 决策系统综合指南

> 本文档由以下文件合并生成 (2026-01-09)



---


{/* 来源: Tech\Architecture\Unified_Decision_System.md */}

## 🧠 通用加权决策系统 (Unified Weighted Decision System)

本文档旨在抽�?Project Vampirefall 中多个核心系统的底层逻辑，构建一�?*通用的、基于上下文的加权选择�?(Context-Aware Weighted Selector)**�?

通过统一仇恨 (Aggro)、塔防索�?(Tower Targeting) �?肉鸽抽卡 (Perk Drafting) 的决策代码，我们可以减少重复逻辑，提高系统的可维护性和扩展性�?

---

## 1. 系统概述 (Overview)

在游戏中，我们经常面临这样的问题�?*“从一堆选项中，根据当前情况，选择最合适的一个（或几个）。�?*

- **仇恨系统:** 从一堆怪物中，选出威胁最大的攻击�?
- **塔防索敌:** 从射程内的敌人中，选出价值最高的击杀�?
- **Perk 抽取:** 从几百个强化词条中，选出最适合玩家当前流派的展示�?

这三个看似无关的系统，本质上都遵�?**`Input -> Scoring -> Selection`** 的模式�?

---

## 2. 核心架构 (Core Architecture)

### 2.1 流程�?(Flowchart)

```mermaid
graph LR
    Pool("候选池 Candidates") */} Filter("过滤�?Filter")
    Context("环境上下�?Context") */} Filter
    Filter */} Scorer("评分引擎 Scoring Engine")
    Context */} Scorer
    Scorer */} Weight("最终权重列�?)
    Weight */} Mode{"选择模式"}
    Mode */}|"Top 1"| ResultA("最优解 (Aggro/Tower)")
    Mode */}|"Weighted Random"| ResultB("随机�?(Perk/Loot)")
```

### 2.2 核心组件 (Components)

1.  **候选人 (Candidate `T`):** 待选择的对象（Enemy, Tower, PerkData）�?
2.  **上下�?(Context `C`):** 决策时的环境信息（距离、玩�?HP、已拥有�?Tags）�?

3.  **评分�?(Scorer `IScorer<T, C>`):** 一个独立的逻辑单元，负责计算单项分数�?

4.  **选择�?(Selector):** 负责运行所有评分器并汇总结果�?

---

## 3. 评分器策略库 (Scorer Strategy Library)

通过组合不同的评分器，我们可以“拼装”出不同�?AI 行为，而无需重写代码�?

### 3.1 基础评分�?

|          评分器名�?                      |          逻辑描述                                              |          适用场景                            |
|          :----------------------          |          :-------------------------------------------          |          :-------------------------          |
|          **DistanceScorer**               |          距离越近，分数越�?(线性或指数衰减)�?                |          仇恨(近战�?、塔�?近程�?          |
|          **HealthScorer**                 |          生命值越低，分数越高 (斩杀逻辑)�?                    |          刺客型怪物、收割型防御�?           |
|          **TagSynergyScorer**             |          拥有相同标签 (Tag) 数量越多，分数越高�?              |          Perk 抽取、战利品生成               |
|          **FixedPriorityScorer**          |          基于硬编码的优先�?(Boss > Elite > Minion)�?         |          塔防(优先打大�?                    |
|          **MemoryScorer**                 |          之前互动�?(造成伤害/被选中) 则加分�?                |          仇恨(反击逻辑)、连击系�?           |

### 3.2 评分公式

标准的归一化评分公式：

$$FinalScore = \sum (RawScore_i \times Multiplier_i) + FlatBonus$$

- **Multiplier (乘区):** 用于调整权重（例如：刺客怪的 `HealthScorer` 权重�?5.0，�?`DistanceScorer` 权重�?0.5）�?
- **FlatBonus (加算):** 用于强制覆盖（例如：嘲讽状态直�?+10000 分）�?

---

## 4. 实战应用配置 (Configuration Examples)

### Case A: 怪物仇恨 (Aggro System)

- **目标:** 选一个攻击目标�?
- **选择模式:** `Top 1` (确定�?�?
- **配置:**
    - `DamageReceivedScorer`: 权重 1.0 (谁打我，我打�?�?
    - `DistanceScorer`: 权重 2.0 (谁离我近，我打谁)�?
    - `TauntStatusScorer`: 权重 100.0 (嘲讽强制最�?�?

### Case B: 狙击塔索�?(Sniper Tower Targeting)

- **目标:** 选一个敌人开火�?
- **选择模式:** `Top 1` (确定�?�?
- **配置:**
    - `DistanceScorer`: 权重 **-1.0** (反向，优先打远的)�?
    - `HealthScorer`: 权重 2.0 (优先打残血，确保击杀)�?
    - `ArmorTypeScorer`: 若目标是重甲，权�?0.5 (打不�?；若轻甲，权�?1.5�?

### Case C: 肉鸽 Perk 抽取 (Perk Drafting)

- **目标:** �?3 �?Perk 给玩家�?
- **选择模式:** `Weighted Random` (加权随机)�?
- **配置:**
    - `RarityBaseScorer`: 传说(5) < 史诗(15) < 稀�?30) < 普�?50)�?
    - `TagSynergyScorer`: 玩家若有[Fire]，火�?Perk 权重 x 1.5�?
    - `BanListFilter`: 若玩家选了[NoMagic]，剔除所有法�?Perk�?
    - `PityTimerScorer`: 若连�?10 次没出传说，传说权重 x 10�?

---

## 5. 代码实现参�?(C# Implementation)

为了保证性能（避免每�?GC），建议使用结构体或预分配内存�?

```csharp
// 1. 定义评分上下�?
public struct DecisionContext {
    public Vector3 Origin; // 决策者位�?
    public EntityType SelfType; // 决策者类�?
    public List<string> PlayerTags; // 玩家当前的流派标�?
    // ... 其他共享数据
}

// 2. 评分器接�?
public interface IScorer<T> {
    float Evaluate(T candidate, DecisionContext context);
}

// 3. 具体评分器实现：距离评分
public class DistanceScorer : IScorer<Enemy> {
    private float _weight;
    public DistanceScorer(float weight) { _weight = weight; }

    public float Evaluate(Enemy target, DecisionContext context) {
        float dist = Vector3.Distance(context.Origin, target.Position);
        // 距离越近分越高，使用 1/x 曲线
        return (1f / Mathf.Max(dist, 0.1f)) * _weight;
    }
}

// 4. 决策引擎
public class DecisionEngine<T> {
    private List<IScorer<T>> _scorers = new List<IScorer<T>>();

    public void AddScorer(IScorer<T> scorer) { _scorers.Add(scorer); }

    // 模式 A: 选最好的 (用于 AI)
    public T SelectBest(List<T> candidates, DecisionContext context) {
        T bestCandidate = default;
        float bestScore = float.MinValue;

        foreach (var candidate in candidates) {
            float currentScore = 0f;
            foreach (var scorer in _scorers) {
                currentScore += scorer.Evaluate(candidate, context);
            }

            \text{if} (currentScore > bestScore) {
                bestScore = currentScore;
                bestCandidate = candidate;
            }
        }
        return bestCandidate;
    }

    // 模式 B: 加权随机 (用于抽卡)
    public T SelectRandom(List<T> candidates, DecisionContext context) {
        // 实现标准的加权随机算�?(Roulette Wheel Selection)
        // ...
        return default;
    }
}
```

## 6. 性能优化指南 (Optimization)

由于 AI 决策可能每一帧都在跑，必须注意开销�?

1.  **分帧计算 (Time-Slicing):** 不要让所有怪物在同一帧跑决策逻辑。将怪物分组，每帧只更新一组�?
2.  **空间划分 (Spatial Partitioning):** 在运�?`DistanceScorer` 之前，先通过四叉�?(QuadTree) 或网格系统获取附近的候选人，避免遍历全图�?

3.  **脏标�?(Dirty Flags):** 对于 Perk 系统，只有当玩家获得�?Perk 或进入新房间时才重新计算权重，而不是每帧计算�?

4.  **提前退�?(Early Exit):** 在寻�?`SelectBest` 时，如果发现一个“绝对优先”的目标（如嘲讽），直接返回，跳过后续计算�?




---


{/* 来源: Tech\Architecture\Decision_System_Diagrams.md */}

## 🏗�?通用决策系统架构�?(Unified Decision System Architecture)

本文档作为系统的工程蓝图，详细定义了类结构、接口关系及运行时序�?

## 1. 类图结构 (Class Diagram)

该图展示了核心泛型引擎与具体业务系统（仇恨、塔防、Perk）的继承与组合关系�?

```mermaid
classDiagram
    %% --- Core Framework ---
    class DecisionEngine~T~ {
        -List~IScorer~T~~ _scorers
        -IFilter~T~ _filter
        +AddScorer(IScorer~T~ scorer)
        +SetFilter(IFilter~T~ filter)
        +SelectBest(List~T~ candidates, Context ctx) T
        +SelectRandom(List~T~ candidates, Context ctx) T
    }

    class IScorer~T~ {
        <<interface>>
        +Evaluate(T candidate, Context ctx) float
    }

    class IFilter~T~ {
        <<interface>>
        +IsValid(T candidate, Context ctx) bool
    }

    class DecisionContext {
        +Vector3 Origin
        +EntityType SourceType
        +Dictionary~string, object~ Blackboard
        +GetTag(string key)
    }

    %% --- Relationships ---
    DecisionEngine o-- IScorer
    DecisionEngine o-- IFilter
    DecisionEngine ..> DecisionContext : Uses

    %% --- Common Implementations ---
    class DistanceScorer {
        +float Weight
        +Evaluate()
    }
    class HealthScorer {
        +bool Inverse
        +Evaluate()
    }
    class TagSynergyScorer {
        +List~string~ TargetTags
        +Evaluate()
    }
    
    IScorer <|.. DistanceScorer
    IScorer <|.. HealthScorer
    IScorer <|.. TagSynergyScorer

    %% --- Business Layer: Aggro System ---
    class MonsterAI {
        -DecisionEngine~IAggroTarget~ _brain
        +UpdateTarget()
    }
    class AggroTargetWrapper {
        <<Interface>> IAggroTarget
    }
    
    MonsterAI */} DecisionEngine : Uses
    MonsterAI ..> AggroTargetWrapper : Selects

    %% --- Business Layer: Tower Defense ---
    class TowerController {
        -DecisionEngine~Enemy~ _targeting
        +ScanAndFire()
    }
    
    TowerController */} DecisionEngine : Uses

    %% --- Business Layer: Perk System ---
    class PerkDraftingSystem {
        -DecisionEngine~PerkData~ _drafter
        +RollOptions()
    }
    
    PerkDraftingSystem */} DecisionEngine : Uses
```

---

## 2. 运行时序�?(Sequence Diagram)

### 2.1 怪物索敌流程 (AI Select Best)

展示了怪物如何通过多重评分器选出最佳攻击目标�?

```mermaid
sequenceDiagram
    participant Monster as 🧟 MonsterAI
    participant Engine as 🧠 DecisionEngine
    participant Filter as 🛡�?IFilter
    participant Scorer1 as 📏 DistanceScorer
    participant Scorer2 as 🩸 HealthScorer
    participant Scorer3 as 💢 ThreatScorer

    Note over Monster: Update Tick (0.5s)
    Monster->>Monster: Get Nearby Targets (Physics.Overlap)
    Monster->>Engine: SelectBest(Candidates, Context)
    
    loop For Each Candidate
        Engine->>Filter: IsValid(Candidate)?
        alt Invalid
            Filter*/}>Engine: False (Skip)
        else Valid
            Engine->>Scorer1: Evaluate(Candidate)
            Scorer1*/}>Engine: Score (e.g., 50)
            
            Engine->>Scorer2: Evaluate(Candidate)
            Scorer2*/}>Engine: Score (e.g., 20)
            
            Engine->>Scorer3: Evaluate(Candidate)
            Scorer3*/}>Engine: Score (e.g., 100)
            
            Engine->>Engine: Sum Scores (170)
        end
    end
    
    Engine->>Engine: Find Max Score
    Engine*/}>Monster: Return BestTarget
    Monster->>Monster: Set Attack Target
```

### 2.2 Perk 抽取流程 (Weighted Random Draft)

展示了如何根据玩家流派权重抽�?Perk�?

```mermaid
sequenceDiagram
    participant UI as 🃏 DraftUI
    participant System as 🎲 PerkSystem
    participant Engine as 🧠 DecisionEngine
    participant TagScorer as 🏷�?TagSynergyScorer

    UI->>System: RequestPerks(Count=3)
    System->>System: Prepare Context (Player Tags: [Fire, Crit])
    System->>Engine: SelectRandom(AllPerks, Context)
    
    loop For All Perks in Pool
        Engine->>TagScorer: Evaluate(Perk)
        note right of TagScorer: Has [Fire]? Weight * 1.5
        TagScorer*/}>Engine: Final Weight
    end
    
    Engine->>Engine: Build Cumulative Distribution Table (CDF)
    
    loop 3 Times
        Engine->>Engine: Random.Range(0, TotalWeight)
        Engine->>Engine: Pick Perk by CDF
        Engine->>Engine: Remove from Pool (Optional)
    end
    
    Engine*/}>System: Return [Perk A, Perk B, Perk C]
    System*/}>UI: Display Options
```

---

## 3. 数据流设�?(Data Flow Specs)

为了支持通用�?`Context`，我们需要一个灵活的黑板机制�?

### 3.1 Context Blackboard 结构
`DecisionContext` 不仅仅是位置信息，它包含了一�?`Dictionary<string, object>` 或强类型�?`Blackboard` 结构，用于传递特定业务参数�?

|          Key (String)          |          Type          |          Description          |          Used By          |
|          :---          |          :---          |          :---          |          :---          |
|          `"AttackerPos"`          |          `Vector3`          |          发起者的位置          |          DistanceScorer          |
|          `"PlayerHP"`          |          `float`          |          玩家当前血量百分比          |          MercyScorer (低血量降低怪物攻击欲望)          |
|          `"PlayerTags"`          |          `List<string>`          |          玩家拥有的流派标�?         |          SynergyScorer          |
|          `"PityCounter"`          |          `int`          |          保底计数�?         |          RarityScorer          |
|          `"LastTarget"`          |          `Entity`          |          上一次攻击的目标          |          StickinessScorer (粘性评分，防止频繁切换)          |

## 4. 优化策略 (Optimization Plan)

在架构层面预留性能优化接口�?

1.  **`IJob` 兼容�?** 设计 `IScorer` 时尽量使�?`struct` �?`NativeArray`，以便未来可以将计算繁重的评分逻辑放入 Unity Job System 并行处理�?
2.  **预分配列�?(Pre-allocation):** `DecisionEngine` 内部维护静态或对象池化�?`List<float> scores`，避免在 `SelectBest` 中产�?GC Alloc�?





---


{/* 来源: Tech\Code_Snippets\DecisionSystem_Core_Classes.md */}

## 💻 核心代码定义 (Core Code Definitions)

本文档定义了通用决策系统的关�?C# 接口与类结构，包括核心引擎和一组标准评分器�?

---

## 0. 基础数据接口 (Core Data Interfaces)

为了让评分器能够通用，候选对�?`T` 需要实现这些接口，以暴露必要的数据�?

### `IPositionable`
```csharp
using UnityEngine;

namespace Vampirefall.DecisionSystem
{
    /// <summary>
    /// 可定位的物体，用�?DistanceScorer
    /// </summary>
    public interface IPositionable
    {
        Vector3 Position { get; }
    }
}
```

### `IHealth`
```csharp
namespace Vampirefall.DecisionSystem
{
    /// <summary>
    /// 具有生命值的物体，用�?HealthScorer
    /// </summary>
    public interface IHealth
    {
        float CurrentHealth { get; }
        float MaxHealth { get; }
        bool IsAlive { get; }
    }
}
```

### `IHasTags`
```csharp
using System.Collections.Generic;

namespace Vampirefall.DecisionSystem
{
    /// <summary>
    /// 具有标签列表的物体，用于 TagSynergyScorer
    /// </summary>
    public interface IHasTags
    {
        List<string> Tags { get; }
    }
}
```

### `IHasEntityType`
```csharp
using System.Collections.Generic;

namespace Vampirefall.DecisionSystem
{
    // 假设 EntityType 是一个全局定义的枚举，例如�?
    public enum EntityType { Player, TankTower, StandardTower, Minion, Nexus, Obstacle, Boss, Elite }

    /// <summary>
    /// 具有实体类型的物体，用于 PriorityScorer
    /// </summary>
    public interface IHasEntityType
    {
        EntityType EntityType { get; }
    }
}
```

---

## 1. 基础接口 (Interfaces)

### `DecisionContext` (上下�?
用于在评分过程中传递环境数据。使�?`Dictionary` 实现灵活的黑板模式，同时也提供常用属性的快捷访问�?

```csharp
using UnityEngine;
using System.Collections.Generic;

namespace Vampirefall.DecisionSystem
{
    /// <summary>
    /// 决策上下文：包含决策所需的所有环境信�?
    /// </summary>
    public class DecisionContext
    {
        // --- 常用属�?(热数据，避免查字�? ---
        public Vector3 Origin { get; set; }         // 决策发起者的位置
        public GameObject Source { get; set; }      // 决策发起者实�?
        
        // --- 扩展数据 (黑板) ---
        private Dictionary<string, object> _blackboard = new Dictionary<string, object>();

        public void Set<T>(string key, T value)
        {
            _blackboard[key] = value;
        }

        public T Get<T>(string key, T defaultValue = default)
        {
            \text{if} (_blackboard.TryGetValue(key, out object val))
            {
                return (T)val;
            }
            return defaultValue;
        }
        
        // 复用池接�?(可�?
        public void Reset() {
            _blackboard.Clear();
            Origin = Vector3.zero;
            Source = null;
        }
    }
}
```

### `IScorer<T>` (评分�?
核心逻辑单元�?

```csharp
namespace Vampirefall.DecisionSystem
{
    /// <summary>
    /// 评分器接口：对单个候选人进行评分
    /// </summary>
    /// <typeparam name="T">候选人类型 (Enemy, PerkData, etc.)</typeparam>
    public interface IScorer<T>
    {
        /// <summary>
        /// 计算分数�?
        /// </summary>
        /// <param name="candidate">待评估的目标</param>
        /// <param name="ctx">当前上下�?/param>
        /// <returns>分数 (可以是负�?</returns>
        float Evaluate(T candidate, DecisionContext ctx);
    }
}
```

### `IFilter<T>` (过滤�?
用于在评分前剔除无效目标（硬性门槛）�?

```csharp
namespace Vampirefall.DecisionSystem
{
    public interface IFilter<T>
    {
        /// <summary>
        /// 是否保留该候选人�?
        /// </summary>
        bool IsValid(T candidate, DecisionContext ctx);
    }
}
```

---

## 2. 核心引擎 (Core Engine)

### `DecisionEngine<T>`
负责组装评分器并执行选择逻辑�?

```csharp
using System.Collections.Generic;
using UnityEngine;
using System.Linq; // for OrderByDescending

namespace Vampirefall.DecisionSystem
{
    public class DecisionEngine<T>
    {
        private readonly List<IScorer<T>> _scorers = new List<IScorer<T>>();
        private readonly List<IFilter<T>> _filters = new List<IFilter<T>>();

        // --- 配置方法 ---
        public DecisionEngine<T> AddScorer(IScorer<T> scorer)
        {
            _scorers.Add(scorer);
            return this; // 链式调用
        }

        public DecisionEngine<T> AddFilter(IFilter<T> filter)
        {
            _filters.Add(filter);
            return this;
        }

        // --- 核心逻辑 A: 选出最优解 (Best Choice) ---
        // 适用于：AI索敌、自动拾�?
        public T SelectBest(IEnumerable<T> candidates, DecisionContext ctx)
        {
            T bestCandidate = default;
            float maxScore = float.MinValue;
            bool foundAny = false;

            foreach (var candidate in candidates)
            {
                // 1. 过滤 (Hard Filter)
                \text{if} (!PassesFilters(candidate, ctx)) continue;

                // 2. 评分 (Scoring)
                float currentScore = 0f;
                for (int i = 0; i < _scorers.Count; i++)
                {
                    currentScore += _scorers[i].Evaluate(candidate, ctx);
                }

                // 3. 比较 (Comparison)
                \text{if} (currentScore > maxScore)
                {
                    maxScore = currentScore;
                    bestCandidate = candidate;
                    foundAny = true;
                }
            }

            return foundAny ? bestCandidate : default;
        }

        // --- 核心逻辑 B: 加权随机 (Weighted Random) ---
        // 适用于：掉落、抽�?
        public T SelectRandom(IEnumerable<T> candidates, DecisionContext ctx)
        {
            // 临时列表用于存储通过过滤的候选项及其权重
            // 注意：生产环境应使用 ListPool 避免 GC
            List<T> validCandidates = new List<T>();
            List<float> weights = new List<float>();
            float totalWeight = 0f;

            foreach (var candidate in candidates)
            {
                \text{if} (!PassesFilters(candidate, ctx)) continue;

                float weight = 0f;
                for (int i = 0; i < _scorers.Count; i++)
                {
                    weight += _scorers[i].Evaluate(candidate, ctx);
                }

                // 权重必须非负
                \text{if} (weight <= 0) continue;

                validCandidates.Add(candidate);
                weights.Add(weight);
                totalWeight += weight;
            }

            \text{if} (validCandidates.Count == 0) return default;

            // 轮盘赌算�?(Roulette Wheel Selection)
            float randomValue = Random.Range(0f, totalWeight);
            float runningTotal = 0f;

            for (int i = 0; i < weights.Count; i++)
            {
                runningTotal += weights[i];
                \text{if} (randomValue <= runningTotal)
                {
                    return validCandidates[i];
                }
            }
            // Fallback for floating point inaccuracies or if randomValue is exactly totalWeight
            return validCandidates.LastOrDefault(); 
        }

        private bool PassesFilters(T candidate, DecisionContext ctx)
        {
            for (int i = 0; i < _filters.Count; i++)
            {
                \text{if} (!_filters[i].IsValid(candidate, ctx)) return false;
            }
            return true;
        }
    }
}
```

---

## 3. 标准评分器实�?(Standard Scorer Implementations)

### `DistanceScorer` (距离评分)
通用性极强，用于 AI �?塔防�?

```csharp
using UnityEngine;
using System; // For Func

namespace Vampirefall.DecisionSystem
{
    public class DistanceScorer<T> : IScorer<T> // where T : IPositionable // No direct interface constraint here for flexibility
    {
        private float _weight;
        private float _maxDistance; // 超过此距离分数为0，或按最大距离计�?
        private bool _inverse;      // true: 越远分越�? false: 越近分越�?
        private Func<T, Vector3> _getPositionFunc; // 动态获取T的位�?

        /// <summary>
        /// 构造函�?
        /// </summary>
        /// <param name="weight">评分权重</param>
        /// <param name="getPositionFunc">一个委托，用于从候选对象T获取其Vector3位置</param>
        /// <param name="maxDistance">最大考量距离，超出按此距离计算，或直接返�?</param>
        /// <param name="inverse">是否反向：true为越远分越高，false为越近分越高</param>
        public DistanceScorer(float weight, Func<T, Vector3> getPositionFunc, float maxDistance = 20f, bool inverse = false)
        {
            _weight = weight;
            _getPositionFunc = getPositionFunc ?? throw new ArgumentNullException(nameof(getPositionFunc));
            _maxDistance = maxDistance;
            _inverse = inverse;
        }

        public float Evaluate(T candidate, DecisionContext ctx)
        {
            Vector3 candidatePos = _getPositionFunc(candidate);
            float dist = Vector3.Distance(candidatePos, ctx.Origin);
            
            // 超出最大距离则直接不给�?(或者按最远距离计�?
            \text{if} (dist > _maxDistance) return 0f; // 也可�?return (_inverse ? _maxDistance : 0f) * _weight;

            // 归一化距�?(0~1)
            float normalizedDist = dist / _maxDistance;
            
            float score;
            \text{if} (_inverse)
            {
                score = normalizedDist; // 越远分越�?
            }
            else
            {
                score = 1f - normalizedDist; // 越近分越�?
            }

            return score * _weight;
        }
    }
}
```

### `HealthScorer` (生命值评�?
根据生命值高低进行评分�?

```csharp
using System; // For Func

namespace Vampirefall.DecisionSystem
{
    public enum HealthScoreMode { Lowest, Highest, PercentageRemaining }

    public class HealthScorer<T> : IScorer<T> // where T : IHealth
    {
        private float _weight;
        private HealthScoreMode _mode;
        private Func<T, IHealth> _getHealthFunc; // 动态获取T的IHealth接口

        /// <summary>
        /// 构造函�?
        /// </summary>
        /// <param name="weight">评分权重</param>
        /// <param name="getHealthFunc">一个委托，用于从候选对象T获取其IHealth接口</param>
        /// <param name="mode">评分模式：最低血量优先，最高血量优先，或剩余百分比</param>
        public HealthScorer(float weight, Func<T, IHealth> getHealthFunc, HealthScoreMode mode = HealthScoreMode.Lowest)
        {
            _weight = weight;
            _getHealthFunc = getHealthFunc ?? throw new ArgumentNullException(nameof(getHealthFunc));
            _mode = mode;
        }

        public float Evaluate(T candidate, DecisionContext ctx)
        {
            IHealth health = _getHealthFunc(candidate);
            \text{if} (health == null || !health.IsAlive) return 0f; // 已死亡或无生命值属性则不给�?

            float score = 0f;
            float healthRatio = health.CurrentHealth / health.MaxHealth; // 0-1之间

            switch (_mode)
            {
                case HealthScoreMode.Lowest:
                    score = 1f - healthRatio; // 血量越低，比值越小，1-比值越�?
                    break;
                case HealthScoreMode.Highest:
                    score = healthRatio; // 血量越高，比值越�?
                    break;
                case HealthScoreMode.PercentageRemaining:
                    score = healthRatio; // 直接按百分比
                    break;
            }
            return score * _weight;
        }
    }
}
```

### `TagSynergyScorer` (标签协同评分)
用于 Perk 系统，根据标签匹配度评分�?

```csharp
using System.Collections.Generic;
using System.Linq; // For .Contains() and .Intersect()
using System; // For Func

namespace Vampirefall.DecisionSystem
{
    public class TagSynergyScorer<T> : IScorer<T> // where T : IHasTags
    {
        private float _weight;
        private Func<T, IHasTags> _getTagsFunc; // 动态获取T的IHasTags接口
        private List<string> _synergyTags; // 用于匹配的标签，可从Context或构造函数传�?

        /// <summary>
        /// 构造函�?
        /// </summary>
        /// <param name="weight">评分权重</param>
        /// <param name="getTagsFunc">一个委托，用于从候选对象T获取其IHasTags接口</param>
        /// <param name="synergyTags">期望匹配的协同标签列�?/param>
        public TagSynergyScorer(float weight, Func<T, IHasTags> getTagsFunc, List<string> synergyTags = null)
        {
            _weight = weight;
            _getTagsFunc = getTagsFunc ?? throw new ArgumentNullException(nameof(getTagsFunc));
            _synergyTags = synergyTags; // 可以通过Context覆盖
        }

        public float Evaluate(T candidate, DecisionContext ctx)
        {
            IHasTags candidateTags = _getTagsFunc(candidate);
            \text{if} (candidateTags == null || candidateTags.Tags == null || candidateTags.Tags.Count == 0) return 0f;

            // 优先�?Context 获取协同标签，如�?Context 没有，则使用构造函数传入的
            List<string> currentSynergyTags = ctx.Get<List<string>>("PlayerSynergyTags", _synergyTags);
            \text{if} (currentSynergyTags == null || currentSynergyTags.Count == 0) return 0f;

            int matchCount = candidateTags.Tags.Intersect(currentSynergyTags).Count();
            
            // 简单地按匹配数量给�?
            return matchCount * _weight;
        }
    }
}
```

### `PriorityScorer` (优先级评�?
根据实体类型给定固定分数�?

```csharp
using System.Collections.Generic;
using System; // For Func

namespace Vampirefall.DecisionSystem
{
    // EntityType 枚举已在 IHasEntityType 定义处提�?
    
    public class PriorityScorer<T> : IScorer<T> // where T : IHasEntityType
    {
        private float _weight;
        private Func<T, IHasEntityType> _getEntityTypeFunc; // 动态获取T的IHasEntityType接口
        private Dictionary<EntityType, float> _priorityMap;

        /// <summary>
        /// 构造函�?
        /// </summary>
        /// <param name="weight">基础评分权重</param>
        /// <param name="getEntityTypeFunc">一个委托，用于从候选对象T获取其IHasEntityType接口</param>
        /// <param name="priorityMap">EntityType 到分数的映射</param>
        public PriorityScorer(float weight, Func<T, IHasEntityType> getEntityTypeFunc, Dictionary<EntityType, float> priorityMap)
        {
            _weight = weight;
            _getEntityTypeFunc = getEntityTypeFunc ?? throw new ArgumentNullException(nameof(getEntityTypeFunc));
            _priorityMap = priorityMap ?? throw new ArgumentNullException(nameof(priorityMap));
        }

        public float Evaluate(T candidate, DecisionContext ctx)
        {
            IHasEntityType entityType = _getEntityTypeFunc(candidate);
            \text{if} (entityType == null) return 0f;

            \text{if} (_priorityMap.TryGetValue(entityType.EntityType, out float basePriority))
            {
                return basePriority * _weight;
            }
            return 0f; // 未知实体类型不给�?
        }
    }
}
```



---


{/* 来源: Tech\Code_Snippets\DecisionSystem_Performance_Demo.md */}

## 🚀 决策系统性能优化示例 (Decision System Performance Optimization Demo)

本文档展示了如何将时间分�?(Time-Slicing) 和空间划�?(Spatial Partitioning) 策略集成�?`DecisionEngine` 的工作流中，以确保游戏在高并发计算时依然流畅�?

---

## 1. 时间分片 (Time-Slicing)

在游戏中，有数百�?AI 同时进行索敌或决策是非常常见的。如果所有单位都在同一帧内更新�?`DecisionEngine`，会导致帧率骤降。时间分片通过在多帧之间分配计算负载来解决这个问题�?

### 1.1 `IDecisionRequester` 接口

定义一个接口，任何需要定期执行决策的 AI 或塔都应实现它�?

```csharp
using Vampirefall.DecisionSystem; // 引入DecisionSystem命名空间

namespace Vampirefall.DecisionSystem.Performance
{
    /// <summary>
    /// 任何需要DecisionScheduler调度的决策请求�?
    /// </summary>
    public interface IDecisionRequester
    {
        void PerformDecision(DecisionContext sharedContext);
        bool IsActive { get; } // 是否还需要继续调�?
        int Priority { get; }  // 调度优先�?(可�?
    }
}
```

### 1.2 `DecisionScheduler` (决策调度�?

一个单�?(Singleton) 或全局服务，负责管理和调度所�?`IDecisionRequester`�?

```csharp
using UnityEngine;
using System.Collections.Generic;
using System.Linq; // For OrderBy

namespace Vampirefall.DecisionSystem.Performance
{
    public class DecisionScheduler : MonoBehaviour
    {
        public static DecisionScheduler Instance { get; private set; }

        [SerializeField] private int _requestsPerFrame = 10; // 每帧处理多少个决策请�?

        private List<IDecisionRequester> _requesters = new List<IDecisionRequester>();
        private int _currentIndex = 0;

        void Awake()
        {
            \text{if} (Instance != null && Instance != this)
            {
                Destroy(gameObject);
            }
            else
            {
                Instance = this;
                DontDestroyOnLoad(gameObject);
            }
        }

        void Update()
        {
            \text{if} (_requesters.Count == 0) return;

            // 用于所有决策请求的共享上下文（减少GC，并在多个请求间传递通用数据�?
            // 在实际使用中，可能每个请求都会填充一些特定的上下文数�?
            DecisionContext sharedContext = new DecisionContext();

            for (int i = 0; i < _requestsPerFrame; i++)
            {
                \text{if} (_requesters.Count == 0) break; // 防止列表为空

                _currentIndex = (_currentIndex + 1) % _requesters.Count;
                IDecisionRequester currentRequester = _requesters[_currentIndex];

                \text{if} (currentRequester.IsActive)
                {
                    sharedContext.Reset(); // 重置上下文，准备下一个请�?
                    currentRequester.PerformDecision(sharedContext);
                }
                else
                {
                    // 如果请求者不再活跃，将其移除
                    _requesters.RemoveAt(_currentIndex);
                    _currentIndex--; // 移除后索引需要调�?
                    \text{if} (_currentIndex < 0) _currentIndex = 0;
                }

                \text{if} (_requesters.Count == 0) break;
            }
        }

        public void RegisterRequester(IDecisionRequester requester)
        {
            \text{if} (!_requesters.Contains(requester))
            {
                _requesters.Add(requester);
                // 可以根据优先级进行排序：_requesters = _requesters.OrderByDescending(r => r.Priority).ToList();
            }
        }

        public void UnregisterRequester(IDecisionRequester requester)
        {
            _requesters.Remove(requester);
        }
    }
}
```

### 1.3 `AggroAgent` (或其他AI) 集成调度�?

```csharp
using UnityEngine;
using System.Collections.Generic;
using Vampirefall.DecisionSystem;
using Vampirefall.DecisionSystem.Performance;
using System.Linq; // for Select

// 假设 AggroAgent 已经像之前示例一样被重构�?
public partial class AggroAgent : MonoBehaviour, IDecisionRequester
{
    // ... 其他 AggroAgent 字段和方�?...
    
    // IDecisionRequester 接口实现
    public bool IsActive => gameObject.activeInHierarchy && _currentTarget != null && _currentTarget.IsAlive; // 怪物存活且有目标

    public int Priority => (int)(Vector3.Distance(transform.position, _currentTarget.Position)); // 优先处理近距离目�?

    void OnEnable() {
        // 注册到调度器
        DecisionScheduler.Instance?.RegisterRequester(this);
    }

    void OnDisable() {
        // 从调度器注销
        DecisionScheduler.Instance?.UnregisterRequester(this);
    }

    // 将原先的 FindBestTarget 逻辑放入 PerformDecision
    public void PerformDecision(DecisionContext sharedContext)
    {
        // 1. 获取所有潜在候选人 (使用空间划分，下一节讨�?
        List<IAggroTargetRefactored> allTargets = GameManager.GetAllAggroTargetsInRadius(transform.position, aggroRange);

        // 2. 准备决策上下�?(填充当前请求者的特定数据)
        sharedContext.Origin = transform.position;
        sharedContext.Source = gameObject;
        sharedContext.Set("AggroThreatTable", _threatTable); // 将自身的仇恨表放入上下文供ThreatScorer使用

        // 3. 执行决策
        IAggroTargetRefactored newTarget = _decisionEngine.SelectBest(allTargets, sharedContext);

        // 4. 切换目标逻辑
        \text{if} (newTarget != null && ShouldSwitchTarget(newTarget, _currentTarget))
        {
            _currentTarget = newTarget;
            // TODO: 通知 NavMeshAgent 新目�?
        }
        else \text{if} (newTarget == null && _currentTarget != null && !_currentTarget.IsAlive)
        {
            _currentTarget = null; // 当前目标死亡
        }
    }

    // Note: 原来�?Update 方法只需要处理移�?攻击动画，不再需�?FindBestTarget()
}
```

---

## 2. 空间划分 (Spatial Partitioning)

空间划分系统是提�?`Candidates` 列表�?`DecisionEngine` 的关键优化。它将整个游戏世界划分为多个区域，从而将“遍历所有敌人”的操作变为“查询局部区域的敌人”�?

### 2.1 概念：Grid �?QuadTree

*   **Grid System (网格系统):**
    *   **原理:** 将世界地图划分为均匀的网格，每个网格单元存储其中的所有单位引用�?
    *   **查询:** 塔或 AI 只需查询其射程覆盖的几个网格单元，就能获得潜在目标列表�?
    *   **适用:** 地形平坦、单位分布相对均匀�?2D 或伪 3D 游戏（如标准塔防）�?
*   **QuadTree (四叉�?八叉�?:**
    *   **原理:** 递归地将空间划分为更小的象限，直到每个象限内的单位数量达到某个阈值�?
    *   **查询:** 快速定位到包含查询区域的象限，并只检索这些象限内的单位�?
    *   **适用:** 单位分布稀疏、地图广阔、有垂直高度�?3D 游戏�?

### 2.2 伪代码：优化 `GetAllAggroTargetsInRadius`

这个方法现在应该由一个专门的 **空间管理服务** 提供，而不是遍历一个大列表�?

```csharp
using UnityEngine;
using System.Collections.Generic;
using System.Linq;

// 假设我们有一个全局空间管理服务
public static class SpatialManager // 这是一个概念性的Manager，实际会更复�?
{
    // ... 内部管理 Grid �?QuadTree 数据结构 ...

    public static List<IAggroTargetRefactored> GetEntitiesInRadius(Vector3 origin, float radius)
    {
        // 实际实现�?
        // 1. 根据 origin �?radius 计算出需要查询的网格单元或四叉树节点�?
        // 2. 从这些单�?节点中高效地检索出所�?IAggroTargetRefactored�?
        // 3. 严格地说，Physics.OverlapSphereNonAlloc �?Unity 提供的加速结构�?
        //    List<Collider> results = new List<Collider>();
        //    Physics.OverlapSphereNonAlloc(origin, radius, results, targetLayerMask);
        //    return results.Select(c => c.GetComponent<IAggroTargetRefactored>()).ToList();
        
        // 为了演示，我们继续使用简化的 GameManager.GetAllAggroTargetsInRadius
        // 但请记住，真实项目会替换它�?
        return GameManager.GetAllAggroTargetsInRadius(origin, radius);
    }
}

// 之前�?GameManager 伪代码中�?GetAllAggroTargetsInRadius 会被调用
// class GameManager { ... } // �?AggroSystem_Refactor_Demo.md
```

### 2.3 `AggroAgent` 中的应用

�?`AggroAgent.PerformDecision` 被调用时，它不再依赖一个全局�?`_allAggroTargets` 列表�?

```csharp
// AggroAgent.PerformDecision 方法的一部分
public void PerformDecision(DecisionContext sharedContext)
{
    // **优化点：通过 SpatialManager 获取候选人列表**
    List<IAggroTargetRefactored> allTargets = SpatialManager.GetEntitiesInRadius(transform.position, aggroRange);

    // ... 后续逻辑不变 ...
}
```

---



