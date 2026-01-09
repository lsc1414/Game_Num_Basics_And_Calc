---
sidebarTitle: "🏗️ 通用决策系统架构图"
---

# 🏗️ 通用决策系统架构图

本文档作为系统的工程蓝图，详细定义了类结构、接口关系及运行时序。

## 1. 类图结构 (Class Diagram)

该图展示了核心泛型引擎与具体业务系统（仇恨、塔防、Perk）的继承与组合关系。

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
    
    MonsterAI --> DecisionEngine : Uses
    MonsterAI ..> AggroTargetWrapper : Selects

    %% --- Business Layer: Tower Defense ---
    class TowerController {
        -DecisionEngine~Enemy~ _targeting
        +ScanAndFire()
    }
    
    TowerController --> DecisionEngine : Uses

    %% --- Business Layer: Perk System ---
    class PerkDraftingSystem {
        -DecisionEngine~PerkData~ _drafter
        +RollOptions()
    }
    
    PerkDraftingSystem --> DecisionEngine : Uses
```

---

## 2. 运行时序图 (Sequence Diagram)

### 2.1 怪物索敌流程 (AI Select Best)

展示了怪物如何通过多重评分器选出最佳攻击目标。

```mermaid
sequenceDiagram
    participant Monster as 🧟 MonsterAI
    participant Engine as 🧠 DecisionEngine
    participant Filter as 🛡️ IFilter
    participant Scorer1 as 📏 DistanceScorer
    participant Scorer2 as 🩸 HealthScorer
    participant Scorer3 as 💢 ThreatScorer

    Note over Monster: Update Tick (0.5s)
    Monster->>Monster: Get Nearby Targets (Physics.Overlap)
    Monster->>Engine: SelectBest(Candidates, Context)
    
    loop For Each Candidate
        Engine->>Filter: IsValid(Candidate)?
        alt Invalid
            Filter-->>Engine: False (Skip)
        else Valid
            Engine->>Scorer1: Evaluate(Candidate)
            Scorer1-->>Engine: Score (e.g., 50)
            
            Engine->>Scorer2: Evaluate(Candidate)
            Scorer2-->>Engine: Score (e.g., 20)
            
            Engine->>Scorer3: Evaluate(Candidate)
            Scorer3-->>Engine: Score (e.g., 100)
            
            Engine->>Engine: Sum Scores (170)
        end
    end
    
    Engine->>Engine: Find Max Score
    Engine-->>Monster: Return BestTarget
    Monster->>Monster: Set Attack Target
```

### 2.2 Perk 抽取流程 (Weighted Random Draft)

展示了如何根据玩家流派权重抽取 Perk。

```mermaid
sequenceDiagram
    participant UI as 🃏 DraftUI
    participant System as 🎲 PerkSystem
    participant Engine as 🧠 DecisionEngine
    participant TagScorer as 🏷️ TagSynergyScorer

    UI->>System: RequestPerks(Count=3)
    System->>System: Prepare Context (Player Tags: [Fire, Crit])
    System->>Engine: SelectRandom(AllPerks, Context)
    
    loop For All Perks in Pool
        Engine->>TagScorer: Evaluate(Perk)
        note right of TagScorer: Has [Fire]? Weight * 1.5
        TagScorer-->>Engine: Final Weight
    end
    
    Engine->>Engine: Build Cumulative Distribution Table (CDF)
    
    loop 3 Times
        Engine->>Engine: Random.Range(0, TotalWeight)
        Engine->>Engine: Pick Perk by CDF
        Engine->>Engine: Remove from Pool (Optional)
    end
    
    Engine-->>System: Return [Perk A, Perk B, Perk C]
    System-->>UI: Display Options
```

---

## 3. 数据流设计 (Data Flow Specs)

为了支持通用的 `Context`，我们需要一个灵活的黑板机制。

### 3.1 Context Blackboard 结构
`DecisionContext` 不仅仅是位置信息，它包含了一个 `Dictionary<string, object>` 或强类型的 `Blackboard` 结构，用于传递特定业务参数。

|          Key (String)          |          Type          |          Description          |          Used By          |
|          :---          |          :---          |          :---          |          :---          |
|          `"AttackerPos"`          |          `Vector3`          |          发起者的位置          |          DistanceScorer          |
|          `"PlayerHP"`          |          `float`          |          玩家当前血量百分比          |          MercyScorer (低血量降低怪物攻击欲望)          |
|          `"PlayerTags"`          |          `List<string>`          |          玩家拥有的流派标签          |          SynergyScorer          |
|          `"PityCounter"`          |          `int`          |          保底计数器          |          RarityScorer          |
|          `"LastTarget"`          |          `Entity`          |          上一次攻击的目标          |          StickinessScorer (粘性评分，防止频繁切换)          |

## 4. 优化策略 (Optimization Plan)

在架构层面预留性能优化接口。

1.  **`IJob` 兼容性:** 设计 `IScorer` 时尽量使用 `struct` 和 `NativeArray`，以便未来可以将计算繁重的评分逻辑放入 Unity Job System 并行处理。
2.  **预分配列表 (Pre-allocation):** `DecisionEngine` 内部维护静态或对象池化的 `List<float> scores`，避免在 `SelectBest` 中产生 GC Alloc。

