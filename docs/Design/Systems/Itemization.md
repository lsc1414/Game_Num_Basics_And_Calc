---
sidebarTitle: "🛡️ 装备与物品化设计"
---

# 🛡️ 装备与物品化设计 (Itemization System)

装备是 RPG 的核心驱动力。本系统参考 *Path of Exile* 和 *Diablo II* 的词缀机制，强调随机性与深度的结合。

---

## 1. 装备部位 (Equipment Slots)

*   **主手 (Main Hand)**: 武器 (剑、杖、弓)。决定基础攻击力与攻击模式。
*   **副手 (Off Hand)**: 盾牌、法球、箭袋。提供防御或特殊属性。
*   **头部 (Helm)**: 提供生命值和主要属性。
*   **胸甲 (Chest)**: 提供大量防御值 (Armor/Evasion) 和抗性。
*   **手套 (Gloves)**: 进攻向防具 (攻速、命中)。
*   **鞋子 (Boots)**: 移动速度的主要来源。
*   **饰品 (Accessories)**: 戒指 x2, 项链 x1。主要提供抗性与属性修正。

---

## 2. 稀有度体系 (Rarity)

|          稀有度          |          颜色          |          词缀槽位 (Affix Slots)          |          说明          |
|          :---          |          :---          |          :---          |          :---          |
|          **普通 (Normal)**          |          ⚪ 白          |          0          |          仅有基础属性 (Base Stats)。可用作打造底材。          |
|          **魔法 (Magic)**          |          🔵 蓝          |          1-2          |          1前缀 或 1后缀 或 1前1后。数值通常较高。          |
|          **稀有 (Rare)**          |          🟡 黄          |          3-6          |          最多3前缀3后缀。后期的主力装备。          |
|          **传奇 (Unique)**          |          🟠 橙          |          固定          |          拥有特殊机制词条，无法随机生成。          |

---

## 3. 词缀池结构 (Affix Pool)

为了保证装备的随机性与平衡性，词缀被严格分为 **前缀 (Prefixes)** 和 **后缀 (Suffixes)**。

### 3.1 前缀 (Prefixes) - *决定基础数值*
通常增加装备的“本体属性”。

*   **Local Modifiers**: 增加武器物理伤害%、增加护甲值+。
*   **Defensive**: 生命值+、魔力值+。
*   **Elemental Damage**: 附加火焰/冰霜/闪电点伤。

### 3.2 后缀 (Suffixes) - *决定辅助属性*
通常提供“额外增益”。

*   **Resistances**: 火焰抗性%、混沌抗性%。
*   **Stats**: 力量、敏捷、智力。
*   **Utility**: 攻击速度、暴击率、移动速度、击中回复。

### 3.3 物品等级 (Item Level - iLvl)
*   词缀有不同的 **Tier (T1~T10)**。
*   高 **iLvl** 的物品才能随机出高 Tier 的词缀。
    *   *例*: T1 生命值 (+90-100) 需要 iLvl 84+。
    *   *设计意图*: 鼓励玩家挑战更高难度的关卡（掉落更高等级的底材）。

---

## 4. 传奇装备设计理念 (Uniques)

> **核心原则**: 传奇装备不应该只是“数值大”。它们应该提供**构建流派 (Build-Defining)** 的机制。

### 4.1 案例分析
*   **❌ 糟糕的设计**: "攻击力 +500"。
    *   *原因*: 只是数值堆砌，没有改变玩法。
*   **✅ 优秀的设计**: **[烈阳纹章 (Crest of the Sun)]**
    *   *基础*: 盾牌。
    *   *属性*: +50 火焰抗性。
    *   *特效*: **你造成的点燃伤害不再造成持续伤害，而是瞬间结算剩余总伤害的 80%。**
    *   *点评*: 彻底改变了点燃流派的玩法，从“挂DOT跑路”变成“高频爆发”。

---

## 5. 智能掉落 (Smart Loot) vs 纯随机

为了减少垃圾时间，采用**伪随机智能掉落**：

1.  **职业偏好**: 掉落的装备有 80% 几率偏向当前职业的主属性（如法师偏向智力）。
2.  **词缀互斥**: 不会生成完全冲突的词缀（如“物理伤害增加”和“法术伤害增加”出现在同一把剑上）。

---

## 6. 物品生成算法 (Generation Algorithm)

```csharp
// 伪代码：生成一件随机稀有装备
Item GenerateRareItem(int monsterLevel) {
    // 1. 随机选择底材 (Base Type)
    Item baseItem = SelectBaseItem(monsterLevel); 
    baseItem.iLvl = monsterLevel;
    
    // 2. 决定词缀数量 (3-6)
    int affixCount = Random.Range(3, 7); 
    
    // 3. 随机词缀
    int prefixCount = 0;
    int suffixCount = 0;
    
    while(baseItem.Affixes.Count < affixCount) {
        bool tryPrefix = Random.value > 0.5f;
        
        // 强制平衡前缀后缀 (最多3前3后)
        if (prefixCount >= 3) tryPrefix = false;
        if (suffixCount >= 3) tryPrefix = true;
        
        Affix newAffix;
        if (tryPrefix) {
            newAffix = AffixTable.RollPrefix(baseItem.Tags, baseItem.iLvl);
            prefixCount++;
        } else {
            newAffix = AffixTable.RollSuffix(baseItem.Tags, baseItem.iLvl);
            suffixCount++;
        }
        
        // 检查互斥组 (ModGroup)
        if (!baseItem.HasConflict(newAffix.Group)) {
            baseItem.AddAffix(newAffix);
        }
    }
    
    return baseItem;
}
```

---

## 7. 引用与参考 (References)

*   **数值体系**: `Design/Numerical_Manual.md` (定义了属性的权重和价值)。
*   **经济模型**: `Design/Systems/Economy_And_Inflation_Model.md` (定义了物品的回收和交易价值)。
*   **掉落规则**: `Design/Systems/Loot_Table_Rules.md` (定义了 Drop Table 和权重)。
*   **业界标杆**: 
    *   [Path of Exile Item Data](https://www.poewiki.net/wiki/Item_affix) - 极其复杂的词缀系统参考。
    *   [Diablo II Affixes](http://classic.battle.net/diablo2exp/items/magic/) - 经典的词缀前缀/后缀规则。