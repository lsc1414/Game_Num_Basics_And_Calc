# 🔱 Hades 构建多样性深度解析：从设计哲学到底层架构

**文档目标**：全方位解析 *Hades* 如何通过“双层标签”设计与“模块化代码”架构，在有限资源下创造出 **225+** 种差异巨大的核心战斗体验（Build）。本文档分为**设计篇**与**程序架构篇**。

---

# 第一部分：设计篇 - 组合爆炸的艺术

## 1. 组合爆炸的数学原理

如果游戏有 10 种武器，每种武器只有 1 种玩法，那只有 10 种体验。
*Hades* 的核心公式：
`Build = 武器形态 (4x6) * 核心祝福 (8) * 辅助祝福 (N) * 锤子变异 (2)`

但真正的魔法在于**标签系统 (Tag System)**。

---

## 2. 双层标签架构 (The Two-Layer Tag System)

Supergiant Games 没有为每两个神设计特定的硬代码逻辑，而是使用标签来解耦。

### 2.1 基础标签 (Primary Tags) - 状态施加
每个神的普通攻击/特殊攻击都会赋予敌人一种**状态**：
*   **Zeus**: `Chain-Lightning` (连锁)
*   **Poseidon**: `Knockback` (击退)
*   **Ares**: `Doom` (延迟伤害)
*   **Aphrodite**: `Weak` (虚弱)
*   **Dionysus**: `Hangover` (中毒DOT)

### 2.2 触发标签 (Trigger Tags) - 机制改变
有些祝福不是为了造成伤害，而是为了**响应**标签：
*   *例如：“对 `Weak` 状态的敌人造成额外伤害”*
*   *例如：“当你造成 `Knockback` 时，额外造成一次 `Rupture` (撕裂) 伤害”*

**设计精髓**：
这让 Poseidon 的击退不仅是位移控制，变成了触发 DOT 的开关。

---

## 3. 双神祝福 (Duo Boons)：构建的质变点

当玩家同时拥有神 A 和 神 B 的特定前置祝福时，会解锁 Duo Boon。这是 *Hades* 构建深度的巅峰。

### 3.1 逻辑分类
Duo Boons 通常遵循以下三种逻辑模板：

#### A. 机制融合 (Fusion)
*   **Ares (Doom) + Aphrodite (Weak) = Curse of Longing**
    *   *效果*：Doom 伤害结算后，不会消失，而是持续对 Weak 敌人造成 50% 的后续伤害。
    *   *分析*：将 Ares 的“爆发”变成了“持续输出”，完美契合 Aphrodite 的减伤站撸流。

#### B. 触发联动 (Trigger Chain)
*   **Poseidon (Knockback) + Zeus (Lightning) = Sea Storm**
    *   *效果*：每当敌人被击退，就落下一道闪电。
    *   *分析*：击退通常会降低 DPS（把怪推远了），但这个祝福把“负面位移”变成了“高频触发器”。攻速越快 -> 击退越多 -> 闪电越多。

#### C. 缺陷互补 (Coverage)
*   **Athena (Deflect) + Ares (Doom) = Merciful End**
    *   *效果*：反弹攻击会立刻结算 Doom 伤害。
    *   *分析*：解决了 Ares 伤害延迟的痛点，把“挂Debuff -> 等待”的节奏变成了“挂Debuff -> 主动引爆”的快节奏连招。

---

# 第二部分：程序架构篇 - 支撑无限可能的代码模式

Supergiant Games 摒弃了传统的长篇设计文档（GDD），采用了高度迭代的开发模式，其核心在于构建了一个**“容器（玩家/武器）”与“内容（恩赐/升级）”完全解耦**的系统。

## 1. 核心哲学：代码即文档 (The Code is the Doc)

*   **Lua 脚本驱动**：Hades 的底层引擎（C++）仅负责渲染、物理和核心循环。所有的数值、技能逻辑、AI 行为树、甚至 UI 流程都由 Lua 脚本编写。
*   **热重载 (Hot-Reloading)**：设计师可以直接修改 Lua 代码并立即在运行中的游戏生效。这意味着“编写文档”的时间被“直接编写逻辑”所取代。
*   **数据表即逻辑**：所有的恩赐（Boons）本质上是一张巨大的数据表（Table），定义了它会 Hook 什么事件、修改什么属性。

## 2. 恩赐系统 (The Boon System) 的架构解构

当玩家拾取一个恩赐时，代码层面绝不是简单的 `if (hasZeus) { ... }`。这是一个**装饰器模式**与**策略模式**的优雅结合。

### 2.1 装饰器模式 (Decorator Pattern) - 动态行为包裹

**原理**：允许在不改变原有对象结构的情况下，动态地给对象增加功能。
在 Hades 中，武器的攻击指令（Command）是被层层包裹的。

*   **基础层**：`SwordAttack` (造成 10 物理伤害)。
*   **装饰层 A (Ares)**：`DoomDecorator` 包裹了 `SwordAttack`。在执行完基础攻击后，额外给目标挂载一个延迟伤害触发器。
*   **装饰层 B (Athena)**：`DeflectDecorator` 包裹了上述整体。在攻击判定的 Hitbox 上增加了 `ReflectProjectiles` 标记。

**伪代码逻辑 (C# 概念模拟):** 
```csharp
interface IAttackCommand { void Execute(Target t); }

// 原始攻击
class BaseSwordAttack : IAttackCommand {
    public void Execute(Target t) { t.TakeDamage(10); }
}

// 装饰器基类
abstract class BoonDecorator : IAttackCommand {
    protected IAttackCommand _wrapped;
    public BoonDecorator(IAttackCommand wrapped) { _wrapped = wrapped; }
    public virtual void Execute(Target t) { _wrapped.Execute(t); }
}

// 宙斯恩赐：增加连锁闪电
class ZeusLightningDecorator : BoonDecorator {
    public override void Execute(Target t) {
        base.Execute(t); // 先造成基础剑伤
        SpawnChainLightning(t.Position); // 后触发闪电
    }
}

// 运行时组装
var attack = new ZeusLightningDecorator(new BaseSwordAttack());
```

### 2.2 策略模式 (Strategy Pattern) - 核心机制替换

**原理**：定义一系列算法，使其可以互相替换。
这通常用于 **Daedalus Hammer (代达罗斯之锤)** 这种改变武器形态的升级。

*   **插槽 (Slot)**：玩家身上有一个 `AttackSlot`，持有一个 `IAttackStrategy`。
*   **替换逻辑**：当获得“霰弹弓”锤子时，它不是“修饰”原有的弓箭逻辑，而是直接**卸载**了 `StandardBowShotStrategy`，装载了 `SpreadShotStrategy`。

### 2.3 属性修饰器管道 (Stat Modifier Pipeline)

RPG 数值膨胀不崩坏的关键在于**属性系统 (Attribute System)**。Hades 采用了类似 Unreal GAS 的属性计算方式。
任何数值（攻击力、暴击率、移动速度）都不是简单的变量，而是一个**计算管道**。

**公式模型：**
$$ FinalValue = (Base + \sum Additive) \times \prod Multipliers $$

*   **Base**: 武器基础伤害 (10)
*   **Additive**: 混沌恩赐 (+30%), 力量恩赐 (+10%) -> Base * (1 + 0.3 + 0.1)
*   **Multiplier**: 暴击 (x2.0), 背刺 (x1.5) -> 独立乘区

## 3. 事件驱动架构 (Event-Driven Architecture)

Hades 中复杂的连锁反应（如“海神+雷神：击退触发闪电”）依赖于**全局事件总线**。

*   **Hooks (钩子)**：游戏中的每个原子动作都会广播信号。
    *   `OnEnemyHit(target, damageInfo)`
    *   `OnDashStart`
    *   `OnKill(target)`
    *   `OnKnockbackApplied(target)`
*   **动态订阅**：
    *   当拾取 **Sea Storm** (海神雷神双重恩赐) 时，该恩赐脚本会自动订阅 `OnKnockbackApplied`。
    *   逻辑：`function OnKnockbackApplied(target) { SpawnLightning(target) }`
    *   这使得海神的击退系统完全不需要知道雷神系统的存在，两者通过事件解耦。

---

# 第三部分：Vampirefall 实战落地指南 (Unity C#)

鉴于 `Vampirefall` 是 **塔防 + Roguelike**，我们需要将上述架构应用到防御塔（Tower）与词条（Perk/Artifact）的结合中。

## 1. 建立 Modifier 管道 (Stat System)

不要直接修改防御塔的 `damage` 变量。创建一个通用的 `Stat` 类。

```csharp
[System.Serializable]
public class Stat {
    public float BaseValue;
    private List<StatModifier> modifiers = new List<StatModifier>();
    
    // 脏标记优化：只有当修饰器列表变动时才重新计算
    private bool _isDirty = true;
    private float _cachedValue;

    public float Value {
        get {
            if (_isDirty) Recalculate();
            return _cachedValue;
        }
    }

    public void AddModifier(StatModifier mod) {
        modifiers.Add(mod);
        _isDirty = true;
    }
}

public enum ModType { Flat, PercentAdd, PercentMult }
```

## 2. 使用 ScriptableObject 实现策略化恩赐

利用 Unity 的 `ScriptableObject` 作为恩赐的数据载体和逻辑入口。

```csharp
// 恩赐基类
public abstract class BoonEffect : ScriptableObject {
    public string boonId;
    public List<string> tags; // Tags: ["Lightning", "Status_Shock"]

    // 钩子函数：当塔攻击时触发
    public virtual void OnAttack(Tower tower, Enemy target) {}
    
    // 钩子函数：当塔击杀时触发
    public virtual void OnKill(Tower tower, Enemy victim) {}
    
    // 钩子函数：装备时修改数值
    public virtual void OnEquip(Tower tower) {
        tower.Stats.Attack.AddModifier(new StatModifier(0.1f, ModType.PercentAdd));
    }
}

// 宙斯类效果实现
[CreateAssetMenu(menuName = "Boons/LightningStrike")]
public class LightningBoon : BoonEffect {
    public GameObject lightningPrefab;
    
    public override void OnAttack(Tower tower, Enemy target) {
        // 生成闪电链逻辑
        Instantiate(lightningPrefab, target.transform.position, Quaternion.identity);
        // 广播事件，允许其他恩赐响应 "Lightning"
        EventManager.Trigger("OnLightningStrike", target);
    }
}
```

## 3. 标签系统 (Tag System) 的实现

为了实现 Duo Boons（双重恩赐），我们需要检查玩家是否凑齐了特定的标签组合。

*   **数据结构**：
    `Dictionary<string, int> globalTags;` // 记录当前拥有多少个 "Zeus", "Fire", "Melee" 标签
*   **检查逻辑**：
    当生成随机掉落池时：
    ```csharp
    bool CanSpawnSeaStorm() {
        return globalTags["Poseidon_Knockback"] > 0 && globalTags["Zeus_Lightning"] > 0;
    }
    ```
*   **应用场景**：
    *   防御塔变异：当塔拥有 `#Fire` 标签时，普通的物理箭矢自动替换为燃烧箭矢模型。
    *   元素反应：当攻击命中带有 `#Wet` 标签的敌人，且本次攻击带有 `#Lightning` 标签 -> 触发感电伤害。

## 4. 总结

| 架构层级 | 传统做法 (Bad) | Hades/Vampirefall 做法 (Good) |
| :--- | :--- | :--- |
| **数值叠加** | 直接修改 `tower.damage += 10` | 使用 `Stat.AddModifier()` 管道，保留溯源能力 |
| **特殊效果** | 在 Tower 类里写 `if (hasZeus) ...` | 塔持有 `List<BoonEffect>`，遍历调用接口 |
| **连锁反应** | 硬编码函数调用 `DoKnockbackThenLightning()` | 事件驱动 `OnKnockback` -> 订阅者响应 |
| **配置数据** | 散落在各个 Prefab 上 | 集中在 ScriptableObject 或 Lua/Excel 表中 |

---
*总结：真正的多样性不是来自于元素的数量，而是来自于元素之间连接方式的数量。通过良好的底层架构，让策划人员能够像搭积木一样自由组合玩法，而无需每次都请求程序修改代码。*