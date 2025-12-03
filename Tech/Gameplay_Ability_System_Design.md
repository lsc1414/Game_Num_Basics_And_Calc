# ⚔️ Vampirefall 游戏技能系统 (GAS) 设计方案

## 1. 概述 (Overview)
**Gameplay Ability System (GAS)** 是一个用于处理交互、技能和属性变更的数据驱动框架。虽然它源自 Unreal Engine，但我们将把其核心设计哲学适配到 Unity 中，用于 **Project Vampirefall**。

### 为什么 Vampirefall 需要 GAS？
*   **塔防需求**: 防御塔需要高效地对数百个怪物施加 Buff/Debuff（如减速、燃烧、护甲粉碎）。
*   **肉鸽机制**: 局内强化（Perks）和神器（Artifacts）经常需要修改基础属性或赋予新的被动能力（例如：“攻击有 10% 概率触发连锁闪电”）。
*   **解耦**: 将“技能做什么”（数据）与“技能怎么执行”（逻辑）彻底分离。

---

## 2. 核心架构 (Core Architecture)

### 2.1 技能系统组件 (Ability System Component, ASC)
`AbilitySystemComponent` 是挂载在每个可交互实体（英雄、防御塔、怪物）上的核心大脑。
*   **职责**:
    *   管理 `AttributeSet`（生命值、攻击力、防御力）。
    *   作为 `GameplayTags` 的容器。
    *   处理传入的 `GameplayEffects`。
    *   授予并执行 `GameplayAbilities`。

### 2.2 属性集 (Attributes / AttributeSet)
属性是代表实体状态的浮点数值。
*   **基础值 (Base Value)**: 永久数值（例如：基础攻击力 = 10）。
*   **当前值 (Current Value)**: 经过 Buff/伤害计算后的临时值（例如：当前 HP = 50/100）。
*   **修饰器 (Modifiers)**: 加法 (`+10`)、乘法 (`*1.5`) 和 覆盖 (`=0`)。

**Vampirefall 的关键属性:**
*   `Health` (生命值), `MaxHealth` (最大生命值)
*   `Mana` (法力值 - 用于英雄技能)
*   `AttackPower` (攻击力)
*   `Defense` (物理/魔法防御)
*   `MoveSpeed` (移动速度 - 怪物核心属性)
*   `AttackSpeed` (攻击速度 - 防御塔核心属性)

### 2.3 游戏标签 (Gameplay Tags)
用于逻辑判断和状态管理的层级化字符串。为了性能，我们使用 `uint` 哈希或 `ScriptableObject` 引用。
*   **格式**: `Category.SubCategory.Specific`
*   **示例**:
    *   `State.Debuff.Stun` (状态.减益.眩晕)
    *   `State.Buff.Enrage` (状态.增益.狂暴)
    *   `Damage.Type.Fire` (伤害.类型.火)
    *   `Unit.Type.Flying` (单位.类型.飞行)

### 2.4 游戏效果 (Gameplay Effects, GE)
这是改变属性的 **唯一** 途径。GE 是纯数据对象 (ScriptableObject)。
*   **持续时间策略**:
    *   **Instant (瞬时)**: 永久改变（伤害、治疗）。
    *   **Infinite (无限)**: 持续直到被移除（装备属性、被动光环）。
    *   **Has Duration (有时限)**: 临时的 Buff/Debuff（眩晕 2秒，加速 5秒）。
*   **应用条件**: “目标必须拥有标签 `Unit.Type.Undead`”。
*   **授予标签**: “当激活时，授予标签 `State.Debuff.Slowed`”。

### 2.5 游戏技能 (Gameplay Abilities, GA)
定义动作的具体逻辑。
*   **消耗**: 法力、体力、冷却时间。
*   **标签交互**:
    *   `AbilityTags`: 描述技能本身的标签 (`Ability.Attack.Melee`)。
    *   `CancelAbilitiesWithTag`: “释放此技能会取消拥有 `State.Stealth` 的技能”。
    *   `BlockAbilitiesWithTag`: “如果持有者拥有 `State.Debuff.Stun`，则无法释放”。

---

## 3. 实现策略 (Unity DOTS/Hybrid)

鉴于 Vampirefall 的高实体数量（塔防特性），我们需要采用混合架构。

### 3.1 数据导向的效果处理 (DOTS)
对于海量单位（怪物），`GameplayEffects` 应当通过 **ECS** 处理。
*   **Buff Buffer**: 每个实体拥有一个动态缓冲区，存储当前激活的 Effect ID。
*   **Tag Component**: 一个位掩码或组件集，代表当前拥有的标签。
*   **System**: `EffectProcessingSystem` 遍历所有实体，每帧（或 Tick）更新持续时间并重新计算属性。

### 3.2 事件驱动的技能 (MonoBehaviour)
对于英雄和复杂的防御塔，我们可以使用包裹在 ECS 核心之上的轻量级事件驱动层。
*   **技能激活**: 由输入或 AI 触发。
*   **表现层**: VFX/SFX 作为 GameObject 生成，与逻辑解耦。

---

## 4. 工作流与工具 (Workflow & Tooling)

### 4.1 创建新技能示例：“冰霜新星” (Frost Nova)
1.  **创建 GE_FrostSlow (冰霜减速)**:
    *   类型: `HasDuration` (3秒)。
    *   修饰器: `MoveSpeed` * 0.5。
    *   授予标签: `State.Debuff.Cold`。
2.  **创建 GE_FrostDamage (冰霜伤害)**:
    *   类型: `Instant`。
    *   修饰器: `Health` - 50。
3.  **创建 GA_FrostNova (冰霜新星技能)**:
    *   逻辑: 半径 5米的球形检测。
    *   应用: 对所有带有 `Unit.Team.Enemy` 标签的目标应用 `GE_FrostSlow` 和 `GE_FrostDamage`。
    *   表现: 生成 VFX "FrostExplosion"。

### 4.2 调试工具
*   **Tag Viewer**: 编辑器窗口，显示选中实体的所有激活标签。
*   **Attribute Modifier Log**: 显示属性变更的堆栈追踪（例如：“速度被 GE_FrostSlow 降低了”）。

---

## 5. 与其他系统的集成
*   **战利品系统 (Loot)**: 装备在穿戴时简单地授予一个 "Infinite" 类型的 GE。
*   **肉鸽强化 (Roguelike Perks)**: 选择一个 Perk 会给玩家添加一个被动 GA 或应用一个永久 GE。
