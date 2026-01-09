---
sidebarTitle: "å³ç­ç³»ç»ç»¼åæå"
---

# å³ç­ç³»ç»ç»¼åæå

> æ¬ææ¡£ç±ä»¥ä¸æä»¶åå¹¶çæ (2026-01-09)



---


{/* æ¥æº: Tech\Architecture\Unified_Decision_System.md */}

## ð§  éç¨å æå³ç­ç³»ç» (Unified Weighted Decision System)

æ¬ææ¡£æ¨å¨æ½è±?Project Vampirefall ä¸­å¤ä¸ªæ ¸å¿ç³»ç»çåºå±é»è¾ï¼æå»ºä¸ä¸?*éç¨çãåºäºä¸ä¸æçå æéæ©å?(Context-Aware Weighted Selector)**ã?

éè¿ç»ä¸ä»æ¨ (Aggro)ãå¡é²ç´¢æ?(Tower Targeting) å?èé¸½æ½å¡ (Perk Drafting) çå³ç­ä»£ç ï¼æä»¬å¯ä»¥åå°éå¤é»è¾ï¼æé«ç³»ç»çå¯ç»´æ¤æ§åæ©å±æ§ã?

---

## 1. ç³»ç»æ¦è¿° (Overview)

å¨æ¸¸æä¸­ï¼æä»¬ç»å¸¸é¢ä¸´è¿æ ·çé®é¢ï¼?*âä»ä¸å éé¡¹ä¸­ï¼æ ¹æ®å½åæåµï¼éæ©æåéçä¸ä¸ªï¼æå ä¸ªï¼ãâ?*

- **ä»æ¨ç³»ç»:** ä»ä¸å æªç©ä¸­ï¼éåºå¨èæå¤§çæ»å»ã?
- **å¡é²ç´¢æ:** ä»å°ç¨åçæäººä¸­ï¼éåºä»·å¼æé«çå»æã?
- **Perk æ½å:** ä»å ç¾ä¸ªå¼ºåè¯æ¡ä¸­ï¼éåºæéåç©å®¶å½åæµæ´¾çå±ç¤ºã?

è¿ä¸ä¸ªçä¼¼æ å³çç³»ç»ï¼æ¬è´¨ä¸é½éµå¾?**`Input -> Scoring -> Selection`** çæ¨¡å¼ã?

---

## 2. æ ¸å¿æ¶æ (Core Architecture)

### 2.1 æµç¨å?(Flowchart)

```mermaid
graph LR
    Pool("åéæ±  Candidates") */} Filter("è¿æ»¤å?Filter")
    Context("ç¯å¢ä¸ä¸æ?Context") */} Filter
    Filter */} Scorer("è¯åå¼æ Scoring Engine")
    Context */} Scorer
    Scorer */} Weight("æç»æéåè¡?)
    Weight */} Mode{"éæ©æ¨¡å¼"}
    Mode */}|"Top 1"| ResultA("æä¼è§£ (Aggro/Tower)")
    Mode */}|"Weighted Random"| ResultB("éæºè§?(Perk/Loot)")
```

### 2.2 æ ¸å¿ç»ä»¶ (Components)

1.  **åéäºº (Candidate `T`):** å¾éæ©çå¯¹è±¡ï¼Enemy, Tower, PerkDataï¼ã?
2.  **ä¸ä¸æ?(Context `C`):** å³ç­æ¶çç¯å¢ä¿¡æ¯ï¼è·ç¦»ãç©å®?HPãå·²æ¥æç?Tagsï¼ã?

3.  **è¯åå?(Scorer `IScorer<T, C>`):** ä¸ä¸ªç¬ç«çé»è¾ååï¼è´è´£è®¡ç®åé¡¹åæ°ã?

4.  **éæ©å?(Selector):** è´è´£è¿è¡ææè¯åå¨å¹¶æ±æ»ç»æã?

---

## 3. è¯åå¨ç­ç¥åº (Scorer Strategy Library)

éè¿ç»åä¸åçè¯åå¨ï¼æä»¬å¯ä»¥âæ¼è£âåºä¸åç?AI è¡ä¸ºï¼èæ ééåä»£ç ã?

### 3.1 åºç¡è¯åå?

|          è¯åå¨åç§?                      |          é»è¾æè¿°                                              |          éç¨åºæ¯                            |
|          :----------------------          |          :-------------------------------------------          |          :-------------------------          |
|          **DistanceScorer**               |          è·ç¦»è¶è¿ï¼åæ°è¶é«?(çº¿æ§æææ°è¡°å)ã?                |          ä»æ¨(è¿ææ?ãå¡é?è¿ç¨å¡?          |
|          **HealthScorer**                 |          çå½å¼è¶ä½ï¼åæ°è¶é« (æ©æé»è¾)ã?                    |          åºå®¢åæªç©ãæ¶å²åé²å¾¡å¡?           |
|          **TagSynergyScorer**             |          æ¥æç¸åæ ç­¾ (Tag) æ°éè¶å¤ï¼åæ°è¶é«ã?              |          Perk æ½åãæå©åçæ               |
|          **FixedPriorityScorer**          |          åºäºç¡¬ç¼ç çä¼åçº?(Boss > Elite > Minion)ã?         |          å¡é²(ä¼åæå¤§æ?                    |
|          **MemoryScorer**                 |          ä¹åäºå¨è¿?(é æä¼¤å®³/è¢«éä¸­) åå åã?                |          ä»æ¨(åå»é»è¾)ãè¿å»ç³»ç»?           |

### 3.2 è¯åå¬å¼

æ åçå½ä¸åè¯åå¬å¼ï¼

$$FinalScore = \sum (RawScore_i \times Multiplier_i) + FlatBonus$$

- **Multiplier (ä¹åº):** ç¨äºè°æ´æéï¼ä¾å¦ï¼åºå®¢æªç `HealthScorer` æéæ?5.0ï¼è?`DistanceScorer` æéæ?0.5ï¼ã?
- **FlatBonus (å ç®):** ç¨äºå¼ºå¶è¦çï¼ä¾å¦ï¼å²è®½ç¶æç´æ?+10000 åï¼ã?

---

## 4. å®æåºç¨éç½® (Configuration Examples)

### Case A: æªç©ä»æ¨ (Aggro System)

- **ç®æ :** éä¸ä¸ªæ»å»ç®æ ã?
- **éæ©æ¨¡å¼:** `Top 1` (ç¡®å®æ?ã?
- **éç½®:**
    - `DamageReceivedScorer`: æé 1.0 (è°ææï¼ææè°?ã?
    - `DistanceScorer`: æé 2.0 (è°ç¦»æè¿ï¼ææè°)ã?
    - `TauntStatusScorer`: æé 100.0 (å²è®½å¼ºå¶æé«?ã?

### Case B: çå»å¡ç´¢æ?(Sniper Tower Targeting)

- **ç®æ :** éä¸ä¸ªæäººå¼ç«ã?
- **éæ©æ¨¡å¼:** `Top 1` (ç¡®å®æ?ã?
- **éç½®:**
    - `DistanceScorer`: æé **-1.0** (ååï¼ä¼åæè¿ç)ã?
    - `HealthScorer`: æé 2.0 (ä¼åææ®è¡ï¼ç¡®ä¿å»æ)ã?
    - `ArmorTypeScorer`: è¥ç®æ æ¯éç²ï¼æé?0.5 (æä¸å?ï¼è¥è½»ç²ï¼æé?1.5ã?

### Case C: èé¸½ Perk æ½å (Perk Drafting)

- **ç®æ :** é?3 ä¸?Perk ç»ç©å®¶ã?
- **éæ©æ¨¡å¼:** `Weighted Random` (å æéæº)ã?
- **éç½®:**
    - `RarityBaseScorer`: ä¼ è¯´(5) < å²è¯(15) < ç¨æ?30) < æ®é?50)ã?
    - `TagSynergyScorer`: ç©å®¶è¥æ[Fire]ï¼ç«ç³?Perk æé x 1.5ã?
    - `BanListFilter`: è¥ç©å®¶éäº[NoMagic]ï¼åé¤æææ³æ?Perkã?
    - `PityTimerScorer`: è¥è¿ç»?10 æ¬¡æ²¡åºä¼ è¯´ï¼ä¼ è¯´æé x 10ã?

---

## 5. ä»£ç å®ç°åè?(C# Implementation)

ä¸ºäºä¿è¯æ§è½ï¼é¿åæ¯å¸?GCï¼ï¼å»ºè®®ä½¿ç¨ç»æä½æé¢åéåå­ã?

```csharp
// 1. å®ä¹è¯åä¸ä¸æ?
public struct DecisionContext {
    public Vector3 Origin; // å³ç­èä½ç½?
    public EntityType SelfType; // å³ç­èç±»å?
    public List<string> PlayerTags; // ç©å®¶å½åçæµæ´¾æ ç­?
    // ... å¶ä»å±äº«æ°æ®
}

// 2. è¯åå¨æ¥å?
public interface IScorer<T> {
    float Evaluate(T candidate, DecisionContext context);
}

// 3. å·ä½è¯åå¨å®ç°ï¼è·ç¦»è¯å
public class DistanceScorer : IScorer<Enemy> {
    private float _weight;
    public DistanceScorer(float weight) { _weight = weight; }

    public float Evaluate(Enemy target, DecisionContext context) {
        float dist = Vector3.Distance(context.Origin, target.Position);
        // è·ç¦»è¶è¿åè¶é«ï¼ä½¿ç¨ 1/x æ²çº¿
        return (1f / Mathf.Max(dist, 0.1f)) * _weight;
    }
}

// 4. å³ç­å¼æ
public class DecisionEngine<T> {
    private List<IScorer<T>> _scorers = new List<IScorer<T>>();

    public void AddScorer(IScorer<T> scorer) { _scorers.Add(scorer); }

    // æ¨¡å¼ A: éæå¥½ç (ç¨äº AI)
    public T SelectBest(List<T> candidates, DecisionContext context) {
        T bestCandidate = default;
        float bestScore = float.MinValue;

        foreach (var candidate in candidates) {
            float currentScore = 0f;
            foreach (var scorer in _scorers) {
                currentScore += scorer.Evaluate(candidate, context);
            }

            if (currentScore > bestScore) {
                bestScore = currentScore;
                bestCandidate = candidate;
            }
        }
        return bestCandidate;
    }

    // æ¨¡å¼ B: å æéæº (ç¨äºæ½å¡)
    public T SelectRandom(List<T> candidates, DecisionContext context) {
        // å®ç°æ åçå æéæºç®æ³?(Roulette Wheel Selection)
        // ...
        return default;
    }
}
```

## 6. æ§è½ä¼åæå (Optimization)

ç±äº AI å³ç­å¯è½æ¯ä¸å¸§é½å¨è·ï¼å¿é¡»æ³¨æå¼éã?

1.  **åå¸§è®¡ç® (Time-Slicing):** ä¸è¦è®©æææªç©å¨åä¸å¸§è·å³ç­é»è¾ãå°æªç©åç»ï¼æ¯å¸§åªæ´æ°ä¸ç»ã?
2.  **ç©ºé´åå (Spatial Partitioning):** å¨è¿è¡?`DistanceScorer` ä¹åï¼åéè¿ååæ ?(QuadTree) æç½æ ¼ç³»ç»è·åéè¿çåéäººï¼é¿åéåå¨å¾ã?

3.  **èæ è®?(Dirty Flags):** å¯¹äº Perk ç³»ç»ï¼åªæå½ç©å®¶è·å¾æ?Perk æè¿å¥æ°æ¿é´æ¶æéæ°è®¡ç®æéï¼èä¸æ¯æ¯å¸§è®¡ç®ã?

4.  **æåéå?(Early Exit):** å¨å¯»æ?`SelectBest` æ¶ï¼å¦æåç°ä¸ä¸ªâç»å¯¹ä¼åâçç®æ ï¼å¦å²è®½ï¼ï¼ç´æ¥è¿åï¼è·³è¿åç»­è®¡ç®ã?




---


{/* æ¥æº: Tech\Architecture\Decision_System_Diagrams.md */}

## ðï¸?éç¨å³ç­ç³»ç»æ¶æå?(Unified Decision System Architecture)

æ¬ææ¡£ä½ä¸ºç³»ç»çå·¥ç¨èå¾ï¼è¯¦ç»å®ä¹äºç±»ç»æãæ¥å£å³ç³»åè¿è¡æ¶åºã?

## 1. ç±»å¾ç»æ (Class Diagram)

è¯¥å¾å±ç¤ºäºæ ¸å¿æ³åå¼æä¸å·ä½ä¸å¡ç³»ç»ï¼ä»æ¨ãå¡é²ãPerkï¼çç»§æ¿ä¸ç»åå³ç³»ã?

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

## 2. è¿è¡æ¶åºå?(Sequence Diagram)

### 2.1 æªç©ç´¢ææµç¨ (AI Select Best)

å±ç¤ºäºæªç©å¦ä½éè¿å¤éè¯åå¨éåºæä½³æ»å»ç®æ ã?

```mermaid
sequenceDiagram
    participant Monster as ð§ MonsterAI
    participant Engine as ð§  DecisionEngine
    participant Filter as ð¡ï¸?IFilter
    participant Scorer1 as ð DistanceScorer
    participant Scorer2 as ð©¸ HealthScorer
    participant Scorer3 as ð¢ ThreatScorer

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

### 2.2 Perk æ½åæµç¨ (Weighted Random Draft)

å±ç¤ºäºå¦ä½æ ¹æ®ç©å®¶æµæ´¾æéæ½å?Perkã?

```mermaid
sequenceDiagram
    participant UI as ð DraftUI
    participant System as ð² PerkSystem
    participant Engine as ð§  DecisionEngine
    participant TagScorer as ð·ï¸?TagSynergyScorer

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

## 3. æ°æ®æµè®¾è®?(Data Flow Specs)

ä¸ºäºæ¯æéç¨ç?`Context`ï¼æä»¬éè¦ä¸ä¸ªçµæ´»çé»æ¿æºå¶ã?

### 3.1 Context Blackboard ç»æ
`DecisionContext` ä¸ä»ä»æ¯ä½ç½®ä¿¡æ¯ï¼å®åå«äºä¸ä¸?`Dictionary<string, object>` æå¼ºç±»åç?`Blackboard` ç»æï¼ç¨äºä¼ éç¹å®ä¸å¡åæ°ã?

|          Key (String)          |          Type          |          Description          |          Used By          |
|          :---          |          :---          |          :---          |          :---          |
|          `"AttackerPos"`          |          `Vector3`          |          åèµ·èçä½ç½®          |          DistanceScorer          |
|          `"PlayerHP"`          |          `float`          |          ç©å®¶å½åè¡éç¾åæ¯          |          MercyScorer (ä½è¡ééä½æªç©æ»å»æ¬²æ)          |
|          `"PlayerTags"`          |          `List<string>`          |          ç©å®¶æ¥æçæµæ´¾æ ç­?         |          SynergyScorer          |
|          `"PityCounter"`          |          `int`          |          ä¿åºè®¡æ°å?         |          RarityScorer          |
|          `"LastTarget"`          |          `Entity`          |          ä¸ä¸æ¬¡æ»å»çç®æ           |          StickinessScorer (ç²æ§è¯åï¼é²æ­¢é¢ç¹åæ¢)          |

## 4. ä¼åç­ç¥ (Optimization Plan)

å¨æ¶æå±é¢é¢çæ§è½ä¼åæ¥å£ã?

1.  **`IJob` å¼å®¹æ?** è®¾è®¡ `IScorer` æ¶å°½éä½¿ç?`struct` å?`NativeArray`ï¼ä»¥ä¾¿æªæ¥å¯ä»¥å°è®¡ç®ç¹éçè¯åé»è¾æ¾å¥ Unity Job System å¹¶è¡å¤çã?
2.  **é¢åéåè¡?(Pre-allocation):** `DecisionEngine` åé¨ç»´æ¤éææå¯¹è±¡æ± åç?`List<float> scores`ï¼é¿åå¨ `SelectBest` ä¸­äº§ç?GC Allocã?





---


{/* æ¥æº: Tech\Code_Snippets\DecisionSystem_Core_Classes.md */}

## ð» æ ¸å¿ä»£ç å®ä¹ (Core Code Definitions)

æ¬ææ¡£å®ä¹äºéç¨å³ç­ç³»ç»çå³é?C# æ¥å£ä¸ç±»ç»æï¼åæ¬æ ¸å¿å¼æåä¸ç»æ åè¯åå¨ã?

---

## 0. åºç¡æ°æ®æ¥å£ (Core Data Interfaces)

ä¸ºäºè®©è¯åå¨è½å¤éç¨ï¼åéå¯¹è±?`T` éè¦å®ç°è¿äºæ¥å£ï¼ä»¥æ´é²å¿è¦çæ°æ®ã?

### `IPositionable`
```csharp
using UnityEngine;

namespace Vampirefall.DecisionSystem
{
    /// <summary>
    /// å¯å®ä½çç©ä½ï¼ç¨äº?DistanceScorer
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
    /// å·æçå½å¼çç©ä½ï¼ç¨äº?HealthScorer
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
    /// å·ææ ç­¾åè¡¨çç©ä½ï¼ç¨äº TagSynergyScorer
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
    // åè®¾ EntityType æ¯ä¸ä¸ªå¨å±å®ä¹çæä¸¾ï¼ä¾å¦ï¼?
    public enum EntityType { Player, TankTower, StandardTower, Minion, Nexus, Obstacle, Boss, Elite }

    /// <summary>
    /// å·æå®ä½ç±»åçç©ä½ï¼ç¨äº PriorityScorer
    /// </summary>
    public interface IHasEntityType
    {
        EntityType EntityType { get; }
    }
}
```

---

## 1. åºç¡æ¥å£ (Interfaces)

### `DecisionContext` (ä¸ä¸æ?
ç¨äºå¨è¯åè¿ç¨ä¸­ä¼ éç¯å¢æ°æ®ãä½¿ç?`Dictionary` å®ç°çµæ´»çé»æ¿æ¨¡å¼ï¼åæ¶ä¹æä¾å¸¸ç¨å±æ§çå¿«æ·è®¿é®ã?

```csharp
using UnityEngine;
using System.Collections.Generic;

namespace Vampirefall.DecisionSystem
{
    /// <summary>
    /// å³ç­ä¸ä¸æï¼åå«å³ç­æéçææç¯å¢ä¿¡æ?
    /// </summary>
    public class DecisionContext
    {
        // --- å¸¸ç¨å±æ?(ç­æ°æ®ï¼é¿åæ¥å­å? ---
        public Vector3 Origin { get; set; }         // å³ç­åèµ·èçä½ç½®
        public GameObject Source { get; set; }      // å³ç­åèµ·èå®ä¾?
        
        // --- æ©å±æ°æ® (é»æ¿) ---
        private Dictionary<string, object> _blackboard = new Dictionary<string, object>();

        public void Set<T>(string key, T value)
        {
            _blackboard[key] = value;
        }

        public T Get<T>(string key, T defaultValue = default)
        {
            if (_blackboard.TryGetValue(key, out object val))
            {
                return (T)val;
            }
            return defaultValue;
        }
        
        // å¤ç¨æ± æ¥å?(å¯é?
        public void Reset() {
            _blackboard.Clear();
            Origin = Vector3.zero;
            Source = null;
        }
    }
}
```

### `IScorer<T>` (è¯åå?
æ ¸å¿é»è¾ååã?

```csharp
namespace Vampirefall.DecisionSystem
{
    /// <summary>
    /// è¯åå¨æ¥å£ï¼å¯¹åä¸ªåéäººè¿è¡è¯å
    /// </summary>
    /// <typeparam name="T">åéäººç±»å (Enemy, PerkData, etc.)</typeparam>
    public interface IScorer<T>
    {
        /// <summary>
        /// è®¡ç®åæ°ã?
        /// </summary>
        /// <param name="candidate">å¾è¯ä¼°çç®æ </param>
        /// <param name="ctx">å½åä¸ä¸æ?/param>
        /// <returns>åæ° (å¯ä»¥æ¯è´æ?</returns>
        float Evaluate(T candidate, DecisionContext ctx);
    }
}
```

### `IFilter<T>` (è¿æ»¤å?
ç¨äºå¨è¯åååé¤æ æç®æ ï¼ç¡¬æ§é¨æ§ï¼ã?

```csharp
namespace Vampirefall.DecisionSystem
{
    public interface IFilter<T>
    {
        /// <summary>
        /// æ¯å¦ä¿çè¯¥åéäººï¼?
        /// </summary>
        bool IsValid(T candidate, DecisionContext ctx);
    }
}
```

---

## 2. æ ¸å¿å¼æ (Core Engine)

### `DecisionEngine<T>`
è´è´£ç»è£è¯åå¨å¹¶æ§è¡éæ©é»è¾ã?

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

        // --- éç½®æ¹æ³ ---
        public DecisionEngine<T> AddScorer(IScorer<T> scorer)
        {
            _scorers.Add(scorer);
            return this; // é¾å¼è°ç¨
        }

        public DecisionEngine<T> AddFilter(IFilter<T> filter)
        {
            _filters.Add(filter);
            return this;
        }

        // --- æ ¸å¿é»è¾ A: éåºæä¼è§£ (Best Choice) ---
        // éç¨äºï¼AIç´¢æãèªå¨æ¾å?
        public T SelectBest(IEnumerable<T> candidates, DecisionContext ctx)
        {
            T bestCandidate = default;
            float maxScore = float.MinValue;
            bool foundAny = false;

            foreach (var candidate in candidates)
            {
                // 1. è¿æ»¤ (Hard Filter)
                if (!PassesFilters(candidate, ctx)) continue;

                // 2. è¯å (Scoring)
                float currentScore = 0f;
                for (int i = 0; i < _scorers.Count; i++)
                {
                    currentScore += _scorers[i].Evaluate(candidate, ctx);
                }

                // 3. æ¯è¾ (Comparison)
                if (currentScore > maxScore)
                {
                    maxScore = currentScore;
                    bestCandidate = candidate;
                    foundAny = true;
                }
            }

            return foundAny ? bestCandidate : default;
        }

        // --- æ ¸å¿é»è¾ B: å æéæº (Weighted Random) ---
        // éç¨äºï¼æè½ãæ½å?
        public T SelectRandom(IEnumerable<T> candidates, DecisionContext ctx)
        {
            // ä¸´æ¶åè¡¨ç¨äºå­å¨éè¿è¿æ»¤çåéé¡¹åå¶æé
            // æ³¨æï¼çäº§ç¯å¢åºä½¿ç¨ ListPool é¿å GC
            List<T> validCandidates = new List<T>();
            List<float> weights = new List<float>();
            float totalWeight = 0f;

            foreach (var candidate in candidates)
            {
                if (!PassesFilters(candidate, ctx)) continue;

                float weight = 0f;
                for (int i = 0; i < _scorers.Count; i++)
                {
                    weight += _scorers[i].Evaluate(candidate, ctx);
                }

                // æéå¿é¡»éè´
                if (weight <= 0) continue;

                validCandidates.Add(candidate);
                weights.Add(weight);
                totalWeight += weight;
            }

            if (validCandidates.Count == 0) return default;

            // è½®çèµç®æ³?(Roulette Wheel Selection)
            float randomValue = Random.Range(0f, totalWeight);
            float runningTotal = 0f;

            for (int i = 0; i < weights.Count; i++)
            {
                runningTotal += weights[i];
                if (randomValue <= runningTotal)
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
                if (!_filters[i].IsValid(candidate, ctx)) return false;
            }
            return true;
        }
    }
}
```

---

## 3. æ åè¯åå¨å®ç?(Standard Scorer Implementations)

### `DistanceScorer` (è·ç¦»è¯å)
éç¨æ§æå¼ºï¼ç¨äº AI å?å¡é²ã?

```csharp
using UnityEngine;
using System; // For Func

namespace Vampirefall.DecisionSystem
{
    public class DistanceScorer<T> : IScorer<T> // where T : IPositionable // No direct interface constraint here for flexibility
    {
        private float _weight;
        private float _maxDistance; // è¶è¿æ­¤è·ç¦»åæ°ä¸º0ï¼æææå¤§è·ç¦»è®¡ç®?
        private bool _inverse;      // true: è¶è¿åè¶é«? false: è¶è¿åè¶é«?
        private Func<T, Vector3> _getPositionFunc; // å¨æè·åTçä½ç½?

        /// <summary>
        /// æé å½æ?
        /// </summary>
        /// <param name="weight">è¯åæé</param>
        /// <param name="getPositionFunc">ä¸ä¸ªå§æï¼ç¨äºä»åéå¯¹è±¡Tè·åå¶Vector3ä½ç½®</param>
        /// <param name="maxDistance">æå¤§èéè·ç¦»ï¼è¶åºææ­¤è·ç¦»è®¡ç®ï¼æç´æ¥è¿å?</param>
        /// <param name="inverse">æ¯å¦ååï¼trueä¸ºè¶è¿åè¶é«ï¼falseä¸ºè¶è¿åè¶é«</param>
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
            
            // è¶åºæå¤§è·ç¦»åç´æ¥ä¸ç»å?(æèææè¿è·ç¦»è®¡ç®?
            if (dist > _maxDistance) return 0f; // ä¹å¯ä»?return (_inverse ? _maxDistance : 0f) * _weight;

            // å½ä¸åè·ç¦?(0~1)
            float normalizedDist = dist / _maxDistance;
            
            float score;
            if (_inverse)
            {
                score = normalizedDist; // è¶è¿åè¶é«?
            }
            else
            {
                score = 1f - normalizedDist; // è¶è¿åè¶é«?
            }

            return score * _weight;
        }
    }
}
```

### `HealthScorer` (çå½å¼è¯å?
æ ¹æ®çå½å¼é«ä½è¿è¡è¯åã?

```csharp
using System; // For Func

namespace Vampirefall.DecisionSystem
{
    public enum HealthScoreMode { Lowest, Highest, PercentageRemaining }

    public class HealthScorer<T> : IScorer<T> // where T : IHealth
    {
        private float _weight;
        private HealthScoreMode _mode;
        private Func<T, IHealth> _getHealthFunc; // å¨æè·åTçIHealthæ¥å£

        /// <summary>
        /// æé å½æ?
        /// </summary>
        /// <param name="weight">è¯åæé</param>
        /// <param name="getHealthFunc">ä¸ä¸ªå§æï¼ç¨äºä»åéå¯¹è±¡Tè·åå¶IHealthæ¥å£</param>
        /// <param name="mode">è¯åæ¨¡å¼ï¼æä½è¡éä¼åï¼æé«è¡éä¼åï¼æå©ä½ç¾åæ¯</param>
        public HealthScorer(float weight, Func<T, IHealth> getHealthFunc, HealthScoreMode mode = HealthScoreMode.Lowest)
        {
            _weight = weight;
            _getHealthFunc = getHealthFunc ?? throw new ArgumentNullException(nameof(getHealthFunc));
            _mode = mode;
        }

        public float Evaluate(T candidate, DecisionContext ctx)
        {
            IHealth health = _getHealthFunc(candidate);
            if (health == null || !health.IsAlive) return 0f; // å·²æ­»äº¡ææ çå½å¼å±æ§åä¸ç»å?

            float score = 0f;
            float healthRatio = health.CurrentHealth / health.MaxHealth; // 0-1ä¹é´

            switch (_mode)
            {
                case HealthScoreMode.Lowest:
                    score = 1f - healthRatio; // è¡éè¶ä½ï¼æ¯å¼è¶å°ï¼1-æ¯å¼è¶å¤?
                    break;
                case HealthScoreMode.Highest:
                    score = healthRatio; // è¡éè¶é«ï¼æ¯å¼è¶å¤?
                    break;
                case HealthScoreMode.PercentageRemaining:
                    score = healthRatio; // ç´æ¥æç¾åæ¯
                    break;
            }
            return score * _weight;
        }
    }
}
```

### `TagSynergyScorer` (æ ç­¾ååè¯å)
ç¨äº Perk ç³»ç»ï¼æ ¹æ®æ ç­¾å¹éåº¦è¯åã?

```csharp
using System.Collections.Generic;
using System.Linq; // For .Contains() and .Intersect()
using System; // For Func

namespace Vampirefall.DecisionSystem
{
    public class TagSynergyScorer<T> : IScorer<T> // where T : IHasTags
    {
        private float _weight;
        private Func<T, IHasTags> _getTagsFunc; // å¨æè·åTçIHasTagsæ¥å£
        private List<string> _synergyTags; // ç¨äºå¹éçæ ç­¾ï¼å¯ä»Contextææé å½æ°ä¼ å?

        /// <summary>
        /// æé å½æ?
        /// </summary>
        /// <param name="weight">è¯åæé</param>
        /// <param name="getTagsFunc">ä¸ä¸ªå§æï¼ç¨äºä»åéå¯¹è±¡Tè·åå¶IHasTagsæ¥å£</param>
        /// <param name="synergyTags">ææå¹éçååæ ç­¾åè¡?/param>
        public TagSynergyScorer(float weight, Func<T, IHasTags> getTagsFunc, List<string> synergyTags = null)
        {
            _weight = weight;
            _getTagsFunc = getTagsFunc ?? throw new ArgumentNullException(nameof(getTagsFunc));
            _synergyTags = synergyTags; // å¯ä»¥éè¿Contextè¦ç
        }

        public float Evaluate(T candidate, DecisionContext ctx)
        {
            IHasTags candidateTags = _getTagsFunc(candidate);
            if (candidateTags == null || candidateTags.Tags == null || candidateTags.Tags.Count == 0) return 0f;

            // ä¼åä»?Context è·åååæ ç­¾ï¼å¦æ?Context æ²¡æï¼åä½¿ç¨æé å½æ°ä¼ å¥ç
            List<string> currentSynergyTags = ctx.Get<List<string>>("PlayerSynergyTags", _synergyTags);
            if (currentSynergyTags == null || currentSynergyTags.Count == 0) return 0f;

            int matchCount = candidateTags.Tags.Intersect(currentSynergyTags).Count();
            
            // ç®åå°æå¹éæ°éç»å?
            return matchCount * _weight;
        }
    }
}
```

### `PriorityScorer` (ä¼åçº§è¯å?
æ ¹æ®å®ä½ç±»åç»å®åºå®åæ°ã?

```csharp
using System.Collections.Generic;
using System; // For Func

namespace Vampirefall.DecisionSystem
{
    // EntityType æä¸¾å·²å¨ IHasEntityType å®ä¹å¤æä¾?
    
    public class PriorityScorer<T> : IScorer<T> // where T : IHasEntityType
    {
        private float _weight;
        private Func<T, IHasEntityType> _getEntityTypeFunc; // å¨æè·åTçIHasEntityTypeæ¥å£
        private Dictionary<EntityType, float> _priorityMap;

        /// <summary>
        /// æé å½æ?
        /// </summary>
        /// <param name="weight">åºç¡è¯åæé</param>
        /// <param name="getEntityTypeFunc">ä¸ä¸ªå§æï¼ç¨äºä»åéå¯¹è±¡Tè·åå¶IHasEntityTypeæ¥å£</param>
        /// <param name="priorityMap">EntityType å°åæ°çæ å°</param>
        public PriorityScorer(float weight, Func<T, IHasEntityType> getEntityTypeFunc, Dictionary<EntityType, float> priorityMap)
        {
            _weight = weight;
            _getEntityTypeFunc = getEntityTypeFunc ?? throw new ArgumentNullException(nameof(getEntityTypeFunc));
            _priorityMap = priorityMap ?? throw new ArgumentNullException(nameof(priorityMap));
        }

        public float Evaluate(T candidate, DecisionContext ctx)
        {
            IHasEntityType entityType = _getEntityTypeFunc(candidate);
            if (entityType == null) return 0f;

            if (_priorityMap.TryGetValue(entityType.EntityType, out float basePriority))
            {
                return basePriority * _weight;
            }
            return 0f; // æªç¥å®ä½ç±»åä¸ç»å?
        }
    }
}
```



---


{/* æ¥æº: Tech\Code_Snippets\DecisionSystem_Performance_Demo.md */}

## ð å³ç­ç³»ç»æ§è½ä¼åç¤ºä¾ (Decision System Performance Optimization Demo)

æ¬ææ¡£å±ç¤ºäºå¦ä½å°æ¶é´åç?(Time-Slicing) åç©ºé´åå?(Spatial Partitioning) ç­ç¥éæå?`DecisionEngine` çå·¥ä½æµä¸­ï¼ä»¥ç¡®ä¿æ¸¸æå¨é«å¹¶åè®¡ç®æ¶ä¾ç¶æµçã?

---

## 1. æ¶é´åç (Time-Slicing)

å¨æ¸¸æä¸­ï¼ææ°ç¾ä¸?AI åæ¶è¿è¡ç´¢ææå³ç­æ¯éå¸¸å¸¸è§çãå¦æææåä½é½å¨åä¸å¸§åæ´æ°å?`DecisionEngine`ï¼ä¼å¯¼è´å¸§çéª¤éãæ¶é´åçéè¿å¨å¤å¸§ä¹é´åéè®¡ç®è´è½½æ¥è§£å³è¿ä¸ªé®é¢ã?

### 1.1 `IDecisionRequester` æ¥å£

å®ä¹ä¸ä¸ªæ¥å£ï¼ä»»ä½éè¦å®ææ§è¡å³ç­ç AI æå¡é½åºå®ç°å®ã?

```csharp
using Vampirefall.DecisionSystem; // å¼å¥DecisionSystemå½åç©ºé´

namespace Vampirefall.DecisionSystem.Performance
{
    /// <summary>
    /// ä»»ä½éè¦DecisionSchedulerè°åº¦çå³ç­è¯·æ±è?
    /// </summary>
    public interface IDecisionRequester
    {
        void PerformDecision(DecisionContext sharedContext);
        bool IsActive { get; } // æ¯å¦è¿éè¦ç»§ç»­è°åº?
        int Priority { get; }  // è°åº¦ä¼åçº?(å¯é?
    }
}
```

### 1.2 `DecisionScheduler` (å³ç­è°åº¦å?

ä¸ä¸ªåä¾?(Singleton) æå¨å±æå¡ï¼è´è´£ç®¡çåè°åº¦ææ?`IDecisionRequester`ã?

```csharp
using UnityEngine;
using System.Collections.Generic;
using System.Linq; // For OrderBy

namespace Vampirefall.DecisionSystem.Performance
{
    public class DecisionScheduler : MonoBehaviour
    {
        public static DecisionScheduler Instance { get; private set; }

        [SerializeField] private int _requestsPerFrame = 10; // æ¯å¸§å¤çå¤å°ä¸ªå³ç­è¯·æ±?

        private List<IDecisionRequester> _requesters = new List<IDecisionRequester>();
        private int _currentIndex = 0;

        void Awake()
        {
            if (Instance != null && Instance != this)
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
            if (_requesters.Count == 0) return;

            // ç¨äºææå³ç­è¯·æ±çå±äº«ä¸ä¸æï¼åå°GCï¼å¹¶å¨å¤ä¸ªè¯·æ±é´ä¼ ééç¨æ°æ®ï¼?
            // å¨å®éä½¿ç¨ä¸­ï¼å¯è½æ¯ä¸ªè¯·æ±é½ä¼å¡«åä¸äºç¹å®çä¸ä¸ææ°æ?
            DecisionContext sharedContext = new DecisionContext();

            for (int i = 0; i < _requestsPerFrame; i++)
            {
                if (_requesters.Count == 0) break; // é²æ­¢åè¡¨ä¸ºç©º

                _currentIndex = (_currentIndex + 1) % _requesters.Count;
                IDecisionRequester currentRequester = _requesters[_currentIndex];

                if (currentRequester.IsActive)
                {
                    sharedContext.Reset(); // éç½®ä¸ä¸æï¼åå¤ä¸ä¸ä¸ªè¯·æ±?
                    currentRequester.PerformDecision(sharedContext);
                }
                else
                {
                    // å¦æè¯·æ±èä¸åæ´»è·ï¼å°å¶ç§»é¤
                    _requesters.RemoveAt(_currentIndex);
                    _currentIndex--; // ç§»é¤åç´¢å¼éè¦è°æ?
                    if (_currentIndex < 0) _currentIndex = 0;
                }

                if (_requesters.Count == 0) break;
            }
        }

        public void RegisterRequester(IDecisionRequester requester)
        {
            if (!_requesters.Contains(requester))
            {
                _requesters.Add(requester);
                // å¯ä»¥æ ¹æ®ä¼åçº§è¿è¡æåºï¼_requesters = _requesters.OrderByDescending(r => r.Priority).ToList();
            }
        }

        public void UnregisterRequester(IDecisionRequester requester)
        {
            _requesters.Remove(requester);
        }
    }
}
```

### 1.3 `AggroAgent` (æå¶ä»AI) éæè°åº¦å?

```csharp
using UnityEngine;
using System.Collections.Generic;
using Vampirefall.DecisionSystem;
using Vampirefall.DecisionSystem.Performance;
using System.Linq; // for Select

// åè®¾ AggroAgent å·²ç»åä¹åç¤ºä¾ä¸æ ·è¢«éæäº?
public partial class AggroAgent : MonoBehaviour, IDecisionRequester
{
    // ... å¶ä» AggroAgent å­æ®µåæ¹æ³?...
    
    // IDecisionRequester æ¥å£å®ç°
    public bool IsActive => gameObject.activeInHierarchy && _currentTarget != null && _currentTarget.IsAlive; // æªç©å­æ´»ä¸æç®æ 

    public int Priority => (int)(Vector3.Distance(transform.position, _currentTarget.Position)); // ä¼åå¤çè¿è·ç¦»ç®æ ?

    void OnEnable() {
        // æ³¨åå°è°åº¦å¨
        DecisionScheduler.Instance?.RegisterRequester(this);
    }

    void OnDisable() {
        // ä»è°åº¦å¨æ³¨é
        DecisionScheduler.Instance?.UnregisterRequester(this);
    }

    // å°ååç FindBestTarget é»è¾æ¾å¥ PerformDecision
    public void PerformDecision(DecisionContext sharedContext)
    {
        // 1. è·åæææ½å¨åéäºº (ä½¿ç¨ç©ºé´ååï¼ä¸ä¸èè®¨è®?
        List<IAggroTargetRefactored> allTargets = GameManager.GetAllAggroTargetsInRadius(transform.position, aggroRange);

        // 2. åå¤å³ç­ä¸ä¸æ?(å¡«åå½åè¯·æ±èçç¹å®æ°æ®)
        sharedContext.Origin = transform.position;
        sharedContext.Source = gameObject;
        sharedContext.Set("AggroThreatTable", _threatTable); // å°èªèº«çä»æ¨è¡¨æ¾å¥ä¸ä¸æä¾ThreatScorerä½¿ç¨

        // 3. æ§è¡å³ç­
        IAggroTargetRefactored newTarget = _decisionEngine.SelectBest(allTargets, sharedContext);

        // 4. åæ¢ç®æ é»è¾
        if (newTarget != null && ShouldSwitchTarget(newTarget, _currentTarget))
        {
            _currentTarget = newTarget;
            // TODO: éç¥ NavMeshAgent æ°ç®æ ?
        }
        else if (newTarget == null && _currentTarget != null && !_currentTarget.IsAlive)
        {
            _currentTarget = null; // å½åç®æ æ­»äº¡
        }
    }

    // Note: åæ¥ç?Update æ¹æ³åªéè¦å¤çç§»å?æ»å»å¨ç»ï¼ä¸åéè¦?FindBestTarget()
}
```

---

## 2. ç©ºé´åå (Spatial Partitioning)

ç©ºé´ååç³»ç»æ¯æä¾?`Candidates` åè¡¨ç»?`DecisionEngine` çå³é®ä¼åãå®å°æ´ä¸ªæ¸¸æä¸çååä¸ºå¤ä¸ªåºåï¼ä»èå°âéåæææäººâçæä½åä¸ºâæ¥è¯¢å±é¨åºåçæäººâã?

### 2.1 æ¦å¿µï¼Grid æ?QuadTree

*   **Grid System (ç½æ ¼ç³»ç»):**
    *   **åç:** å°ä¸çå°å¾ååä¸ºååçç½æ ¼ï¼æ¯ä¸ªç½æ ¼ååå­å¨å¶ä¸­çææåä½å¼ç¨ã?
    *   **æ¥è¯¢:** å¡æ AI åªéæ¥è¯¢å¶å°ç¨è¦ççå ä¸ªç½æ ¼ååï¼å°±è½è·å¾æ½å¨ç®æ åè¡¨ã?
    *   **éç¨:** å°å½¢å¹³å¦ãåä½åå¸ç¸å¯¹ååç?2D æä¼ª 3D æ¸¸æï¼å¦æ åå¡é²ï¼ã?
*   **QuadTree (ååæ ?å«åæ ?:**
    *   **åç:** éå½å°å°ç©ºé´ååä¸ºæ´å°çè±¡éï¼ç´å°æ¯ä¸ªè±¡éåçåä½æ°éè¾¾å°æä¸ªéå¼ã?
    *   **æ¥è¯¢:** å¿«éå®ä½å°åå«æ¥è¯¢åºåçè±¡éï¼å¹¶åªæ£ç´¢è¿äºè±¡éåçåä½ã?
    *   **éç¨:** åä½åå¸ç¨çãå°å¾å¹¿éãæåç´é«åº¦ç?3D æ¸¸æã?

### 2.2 ä¼ªä»£ç ï¼ä¼å `GetAllAggroTargetsInRadius`

è¿ä¸ªæ¹æ³ç°å¨åºè¯¥ç±ä¸ä¸ªä¸é¨ç **ç©ºé´ç®¡çæå¡** æä¾ï¼èä¸æ¯éåä¸ä¸ªå¤§åè¡¨ã?

```csharp
using UnityEngine;
using System.Collections.Generic;
using System.Linq;

// åè®¾æä»¬æä¸ä¸ªå¨å±ç©ºé´ç®¡çæå¡
public static class SpatialManager // è¿æ¯ä¸ä¸ªæ¦å¿µæ§çManagerï¼å®éä¼æ´å¤æ?
{
    // ... åé¨ç®¡ç Grid æ?QuadTree æ°æ®ç»æ ...

    public static List<IAggroTargetRefactored> GetEntitiesInRadius(Vector3 origin, float radius)
    {
        // å®éå®ç°ï¼?
        // 1. æ ¹æ® origin å?radius è®¡ç®åºéè¦æ¥è¯¢çç½æ ¼ååæååæ èç¹ã?
        // 2. ä»è¿äºåå?èç¹ä¸­é«æå°æ£ç´¢åºææ?IAggroTargetRefactoredã?
        // 3. ä¸¥æ ¼å°è¯´ï¼Physics.OverlapSphereNonAlloc æ?Unity æä¾çå éç»æã?
        //    List<Collider> results = new List<Collider>();
        //    Physics.OverlapSphereNonAlloc(origin, radius, results, targetLayerMask);
        //    return results.Select(c => c.GetComponent<IAggroTargetRefactored>()).ToList();
        
        // ä¸ºäºæ¼ç¤ºï¼æä»¬ç»§ç»­ä½¿ç¨ç®åç GameManager.GetAllAggroTargetsInRadius
        // ä½è¯·è®°ä½ï¼çå®é¡¹ç®ä¼æ¿æ¢å®ã?
        return GameManager.GetAllAggroTargetsInRadius(origin, radius);
    }
}

// ä¹åç?GameManager ä¼ªä»£ç ä¸­ç?GetAllAggroTargetsInRadius ä¼è¢«è°ç¨
// class GameManager { ... } // è§?AggroSystem_Refactor_Demo.md
```

### 2.3 `AggroAgent` ä¸­çåºç¨

å½?`AggroAgent.PerformDecision` è¢«è°ç¨æ¶ï¼å®ä¸åä¾èµä¸ä¸ªå¨å±ç?`_allAggroTargets` åè¡¨ã?

```csharp
// AggroAgent.PerformDecision æ¹æ³çä¸é¨å
public void PerformDecision(DecisionContext sharedContext)
{
    // **ä¼åç¹ï¼éè¿ SpatialManager è·ååéäººåè¡¨**
    List<IAggroTargetRefactored> allTargets = SpatialManager.GetEntitiesInRadius(transform.position, aggroRange);

    // ... åç»­é»è¾ä¸å ...
}
```

---



