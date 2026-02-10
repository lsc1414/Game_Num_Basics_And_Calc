---
sidebarTitle: "仇恨系统与 AI 目标选择"
title: "💢 仇恨系统与 AI 目标选择"
---



# 💢 仇恨系统与 AI 目标选择

仇恨系统（Aggro/Threat System）是连接怪物 AI 与玩家行为的桥梁。在 Project Vampirefall 中，由于融合了 **Action Roguelike**（玩家移动）与 **Tower Defense**（固定防御），仇恨系统必须在“被动寻路”与“主动反击”之间找到平衡。

---

## 1. 理论基础：感知与威胁 (Perception & Threat)

### 1.1 感知层 (Perception Layer)
怪物在决定攻击谁之前，首先必须“感知”到目标。感知机制是各种仇恨类型的触发基础。

*   **全局寻路目标 (Global Goal):** 所有怪物的默认目标是 **基地核心 (Nexus)**。如果没有受到干扰，它们会沿着最短路径直奔基地。这是一个隐式的静态仇恨源。
*   **警戒半径 (Aggro Radius):** 一个圆形的侦测范围（如 10米）。当玩家或防御塔进入此范围，怪物进入“战斗状态”，开始主动侦测仇恨。
*   **视觉锥形 (View Cone):** 部分精英怪拥有前方 60° 的视野。潜行 (Stealth) 状态下的玩家不会触发警戒半径，但会被视觉锥形发现。
*   **听觉范围 (Audio Radius):** 特定行为（如玩家技能、防御塔开火、爆炸）可在更大范围内吸引怪物注意，即使目标不可见。

### 1.2 仇恨列表 (Threat Table) - 动态仇恨管理
当怪物进入战斗状态后，它会维护一个 **仇恨列表**。列表中包含所有对它造成过伤害或产生过仇恨行为的实体。

*   **Target A:** 100 Threat
*   **Target B:** 50 Threat
怪物默认攻击列表中 Threat 最高的单位。

#### 1.2.1 仇恨类型细分 (Aggro Types)

|          仇恨类型          |          触发方式          |          初始仇恨值          |          衰减模式          |          优先级影响          |
|          :---          |          :---          |          :---          |          :---          |          :---          |
|          **基础寻路仇恨 (Base Pathfinding Threat)**          |          怪物诞生时，自动对“基地核心”生成。          |          极高（无限趋近）          |          无衰减          |          只有当其他仇恨源足够高时才转移目标。          |
|          **伤害仇恨 (Damage Threat)**          |          对怪物造成伤害。          |          1 伤害 = 1 Threat          |          线性衰减（脱战后清零）          |          随伤害量动态变化。          |
|          **治疗仇恨 (Healing Threat)**          |          治疗队友或玩家自身。          |          治疗量 * 0.5 Threat          |          线性衰减          |          对所有感知范围内的怪物生效。          |
|          **嘲讽仇恨 (Taunt Threat)**          |          嘲讽技能。          |          目标当前最高仇恨值 + 固定值 (如 100)          |          短暂爆发，快速衰减          |          强制改变目标，优先级最高。          |
|          **环境仇恨 (Environmental Threat)**          |          破坏怪物附近的阻挡物（如墙壁、陷阱）。          |          固定值（如 50）          |          无衰减          |          优先级低于动态仇恨，高于基础寻路。          |
|          **技能仇恨 (Ability Threat)**          |          释放特定技能（如范围控场）。          |          根据技能强度计算          |          线性衰减          |          特定技能可附带额外仇恨修正。          |

---

## 2. 混合机制设计 (Hybrid Mechanics)

Project Vampirefall 的特殊性在于：玩家不仅要杀怪，还要保护塔。因此，我们设计了多层次的优先级决策。

### 2.1 优先级金字塔 (Target Priority Pyramid)
除了动态的仇恨值，我们引入**静态优先级系数**来修正怪物的行为倾向。这个系数会乘以最终计算出的仇恨值，形成怪物的**“最终威胁值” (Final Threat)**。

$$FinalThreat = (RawDynamicThreat + BasePathfindingThreat + EnvironmentalThreat) \times EntityTypePriorityMod \times DistanceFactor$$

|          实体类型 (EntityType)          |          仇恨计算公式          |          Priority Mod          |          行为逻辑          |
|          :---          |          :---          |          :---          |          :---          |
|          **基地核心 (Nexus)**          |          仅 `BasePathfindingThreat`          |          10.0x          |          所有怪物的默认且最终目标。只有当其他目标提供足够高的 `FinalThreat` 才会转移。          |
|          **嘲讽单位 (Tank Tower)**          |          `DynamicThreat` (含嘲讽)          |          5.0x          |          强制吸引火力。高额 `PriorityMod` 确保其能稳稳地拉住仇恨。          |
|          **玩家 (Player)**          |          `DynamicThreat`          |          2.0x          |          怪物倾向于攻击高威胁的玩家。玩家的机动性是其优势，但高输出会快速积累仇恨。          |
|          **防御塔 (Standard Tower)**          |          `DynamicThreat`          |          1.0x          |          正常优先级。怪物会在 Nexus、玩家和防御塔之间平衡选择。          |
|          **召唤物 (Minions)**          |          `DynamicThreat`          |          0.5x          |          除非挡路或仇恨值极高，否则怪物懒得理会。          |
|          **阻挡物 (Wall/Obstacle)**          |          仅 `EnvironmentalThreat`          |          0.8x          |          仅当路径受阻时才成为目标，其仇恨值仅影响破拆速度而非优先追击。          |

### 2.2 风筝限制 (Anti-Kiting)
为了防止玩家利用高移速将怪物无限拉离防线（导致塔防失效），引入 **Leash (牵引绳)** 机制。

*   **Leash Radius:** 怪物离开其“出生点”或“当前路径点”的最大距离（如 30米）。
*   **Reset:** 一旦超过 Leash 距离，怪物会**无敌并满速跑回**原来的路径点，清空所有仇恨列表。
*   **例外:** Boss 通常没有 Leash 限制，或者是整个房间范围。

---

## 3. 仇恨计算公式 (Calculation)

### 3.1 原始仇恨值 (Raw Threat Calculation)
每种仇恨类型独立计算，然后叠加。

*   **伤害仇恨:** `DamageThreat = ActualDamageDealt * DamageThreatModifier`
    *   `DamageThreatModifier`：不同单位对仇恨贡献不同（如玩家的攻击制造更多仇恨）。
*   **治疗仇恨:** `HealingThreat = ActualHealingDone * HealingThreatModifier`
    *   对所有怪物生效，且只计算一次。
*   **嘲讽仇恨:** `TauntThreat = MaxThreatOnMonster + FixedTauntValue`
    *   `MaxThreatOnMonster`：怪物当前仇恨列表中最高的值。
    *   `FixedTauntValue`：嘲讽技能额外增加的仇恨。

### 3.2 距离权重 (Distance Factor)
为了避免怪物无视脸上的坦克去追远处的弓箭手，距离会影响仇恨判定。

$$DistanceFactor = 1 + \frac{K}{Distance}$$

*   $K$：距离敏感系数（近战怪 K 值高，远程怪 K 值低）。
*   `EffectiveThreat = RawThreat * DistanceFactor`。
*   **近战怪:** 对近距离目标极其敏感（K值如 10），倾向于攻击最近且仇恨值高的目标。
*   **远程怪:** 对距离不敏感（K值如 2），倾向于攻击输出最高的目标。

### 3.3 切换目标阈值 (Switch Threshold)
为了防止怪物在两个仇恨相近的目标间频繁转头（Ping-Ponging），切换目标需要满足**阈值**。

*   **In-Combat Range:** 只有当新目标的 `FinalThreat` > 当前目标 `FinalThreat` 的 **110%** 时，才切换。
*   **Out-of-Combat Range:** 如果当前目标超出攻击范围，或已死亡，则选择仇恨列表中 `FinalThreat` 最高的新目标。

---

## 4. 特殊 AI 行为 (Behavior Profiles)

不同类型的怪物使用不同的仇恨逻辑模板，通过配置 `EntityTypePriorityMod` 和其他参数实现。

### 4.1 攻城者 (Sieger)
*   **特点:** 无视玩家和普通塔，眼里只有墙和基地。
*   **逻辑:** `EntityTypePriorityMod(Wall) = 10.0`, `EntityTypePriorityMod(Player) = 0.0`。它们对 `EnvironmentalThreat` 的响应权重极高。
*   **对策:** 玩家必须用身体卡位或使用击退技能将它们推离基地。

### 4.2 刺客 (Assassin)
*   **特点:** 优先攻击血量最低或正在施法的目标（通常是玩家或后排输出塔）。
*   **逻辑:** 忽略 `DistanceFactor`，直接锁定 `LowestHP` 或 `CastingTarget`，并可能拥有特殊的路径规划能力（如跳跃、闪现）。

### 4.3 狂暴者 (Berserker)
*   **特点:** 谁打我最疼，我就打谁。
*   **逻辑:** 受到暴击时，攻击者的 `DamageThreatModifier` x 2.0，短时间内只会追击此目标。

### 4.4 干扰者 (Disruptor)
*   **特点:** 不以造成伤害为主，而是专注于控制或削弱玩家/防御塔。
*   **逻辑:** 拥有低 `DamageThreat` 但高 `AbilityThreat`。其技能可能附带强制嘲讽或强制转火效果。

---

## 5. 实践指南 (Implementation Guide)

### 5.1 Unity 组件结构
建议使用 `IAggroTarget` 接口和 `AggroAgent` 组件。

```csharp
public interface IAggroTarget {
    float GetThreatModifier(AggroType aggroType); // 不同仇恨类型可有不同修正
    EntityType GetEntityType(); // 返回实体类型 (Player, TankTower, Nexus)
    bool IsValid(); // 是否死亡、隐身或不可作为目标
    Vector3 Position { get; }
    // 可以添加获取当前血量、是否施法等信息的方法
}

public enum EntityType { Player, TankTower, StandardTower, Minion, Nexus, Obstacle }
public enum AggroType { Damage, Healing, Taunt, Environmental, Ability }

public class AggroAgent : MonoBehaviour { // 挂在怪物身上
    // 仇恨列表：Key=目标 (IAggroTarget), Value=当前仇恨值
    private Dictionary<IAggroTarget, float> threatTable = new Dictionary<IAggroTarget, float>();
    
    public EntityType monsterType; // 配置怪物自身类型，用于特殊行为

    // 在怪物受到伤害、感知到治疗、被嘲讽等时调用
    public void AddThreat(IAggroTarget source, AggroType type, float rawValue) {
        float threat = rawValue;
        // 应用来源的 GetThreatModifier
        threat *= source.GetThreatModifier(type);
        
        if (!threatTable.ContainsKey(source)) threatTable[source] = 0;
        threatTable[source] += threat;
        
        CleanThreatTable(); // 清理无效目标
        CheckSwitchTarget(); // 检查是否需要切换目标
    }

    // ... (Previous code)

    private IAggroTarget FindBestTarget() {
        IAggroTarget bestTarget = null;
        float highestThreat = -1f;

        foreach (var entry in threatTable) {
            var target = entry.Key;
            float rawThreat = entry.Value;
            
            if (!target.IsValid()) continue;

            // 1. 计算 EntityType 优先级修正
            float priorityMod = GetPriorityModifier(target.GetEntityType());
            
            // 2. 计算距离权重修正
            float distance = Vector3.Distance(transform.position, target.Position);
            float distanceFactor = 1f + (distanceSensitivityK / Mathf.Max(distance, 0.1f)); // 防止除以0
            
            // 3. 合成最终仇恨
            float finalThreat = rawThreat * priorityMod * distanceFactor;

            if (finalThreat > highestThreat) {
                highestThreat = finalThreat;
                bestTarget = target;
            }
        }
        return bestTarget;
    }

    private void CheckSwitchTarget() {
        IAggroTarget potentialTarget = FindBestTarget();
        if (potentialTarget == null || potentialTarget == currentTarget) return;

        float currentFinalThreat = CalculateFinalThreat(currentTarget);
        float newFinalThreat = CalculateFinalThreat(potentialTarget);

        // 阈值判定：防止 Ping-Ponging
        float thresholdMultiplier = (IsMeleeRange(potentialTarget)) ? 1.1f : 1.3f;
        
        if (newFinalThreat > currentFinalThreat * thresholdMultiplier) {
            SetTarget(potentialTarget);
        }
    }

    private float GetPriorityModifier(EntityType type) {
        // 这里可以配置化，或者读取 ScriptableObject 配置
        switch (type) {
            case EntityType.TankTower: return 5.0f;
            case EntityType.Player: return 2.0f;
            case EntityType.Nexus: return 10.0f; // 特殊处理
            default: return 1.0f;
        }
    }
}
```

### 5.2 可视化调试
在 Scene View 中绘制线条：

*   **红色线:** 当前锁定的目标。
*   **黄色线:** 仇恨列表中第二顺位的目标。
*   **文字:** 在怪物头顶显示当前目标的 `FinalThreat` 数值和 `EntityType`。
*   **色彩编码:** 不同怪物类型（攻城者、刺客）用不同颜色描边。

---

## 6. 常见问题与解决方案

*   **Q: 怪物被塔堵住了怎么办？**
    *   A: 如果通往 Nexus 的路径被堵死 (Path Invalid)，怪物进入 **Breach Mode (破拆模式)**，攻击最近的阻挡物（墙或塔），直到路径打通。其 `BasePathfindingThreat` 会临时转嫁到阻挡物上。
*   **Q: 玩家隐身了怎么办？**
    *   A: 玩家的 `DamageThreat` 和 `AbilityThreat` 清零（或暂时冻结）。怪物转向仇恨列表中的第二目标（通常是塔）。如果列表为空，回满血跑回巡逻路径。隐身状态的 `IAggroTarget.IsValid()` 返回 `false`。
*   **Q: 如何处理群体仇恨？**
    *   A: 对于 AoE 技能造成的伤害，可以将其仇恨值分配给所有被击中的怪物。某些 Boss 可能拥有“群体嘲讽免疫”或“软嘲讽”机制，仅对仇恨列表前几位的目标生效。

---
