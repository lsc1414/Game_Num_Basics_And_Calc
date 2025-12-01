# 🛡️ 装备与物品化设计 (Itemization System)

装备是 RPG 的核心驱动力。本系统参考 *Path of Exile* 和 *Diablo II* 的词缀机制，强调随机性与深度的结合。

---

## 1. 装备部位 (Equipment Slots)

*   **主手 (Main Hand):** 武器 (剑、杖、弓)。决定基础攻击力与攻击模式。
*   **副手 (Off Hand):** 盾牌、法球、箭袋。提供防御或特殊属性。
*   **头部 (Helm):** 
*   **胸甲 (Chest):** 提供大量防御值 (Armor/Evasion)。
*   **手套 (Gloves):** 进攻向防具 (攻速、命中)。
*   **鞋子 (Boots):** 移动速度的主要来源。
*   **饰品 (Accessories):** 戒指 x2, 项链 x1。主要提供抗性与属性修正。

## 2. 稀有度体系 (Rarity)

| 稀有度 | 颜色 | 词缀槽位 (Affix Slots) | 说明 |
| :--- | :--- | :--- | :--- |
| **普通 (Normal)** | ⚪ 白 | 0 | 仅有基础属性 (Base Stats)。可用作打造底材。 |
| **魔法 (Magic)** | 🔵 蓝 | 1-2 | 1前缀 或 1后缀 或 1前1后。数值通常较高。 |
| **稀有 (Rare)** | 🟡 黄 | 3-6 | 最多3前缀3后缀。后期的主力装备。 |
| **传奇 (Unique)** | 🟠 橙 | 固定 | 拥有特殊机制词条，无法随机生成。 |

## 3. 词缀池结构 (Affix Pool)

### 3.1 前缀 (Prefixes) - *决定基础数值*
*   **Local Modifiers:** 增加武器物理伤害%、增加护甲值+。
*   **Defensive:** 生命值+、魔力值+。
*   **Elemental Damage:** 附加火焰/冰霜/闪电点伤。

### 3.2 后缀 (Suffixes) - *决定辅助属性*
*   **Resistances:** 火焰抗性%、混沌抗性%。
*   **Stats:** 力量、敏捷、智力。
*   **Utility:** 攻击速度、暴击率、移动速度。

### 3.3 物品等级 (Item Level - iLvl)
*   词缀有不同的 **Tier (T1~T10)**。
*   高 iLvl 的物品才能随机出高 Tier 的词缀。
*   *例:* T1 生命值 (+90-100) 需要 iLvl 84+。

## 4. 传奇装备设计理念 (Uniques)

传奇装备不应该只是“数值大”。它们应该提供**构建流派 (Build-Defining)** 的机制。

*   **案例: [烈阳纹章 (Crest of the Sun)]**
    *   *基础:* 盾牌。
    *   *属性:* +50 火焰抗性。
    *   *特效:* **你造成的点燃伤害不再造成持续伤害，而是瞬间结算剩余总伤害的 80%。**
    *   *点评:* 彻底改变了点燃流派的玩法，从“挂DOT跑路”变成“高频爆发”。

## 5. 物品生成算法 (Generation Algo)

```csharp
// 伪代码
Item GenerateItem(int monsterLevel, Rarity rarity) {
    Item baseItem = SelectBaseItem(monsterLevel); // 选底材
    baseItem.iLvl = monsterLevel;
    
    int affixCount = DetermineAffixCount(rarity); // 蓝:1-2, 黄:3-6
    
    for(int i=0; i<affixCount; i++) {
        // 确保前缀/后缀平衡
        bool isPrefix = BalancePrefixSuffix(baseItem); 
        Affix affix = RollAffix(baseItem.Tags, baseItem.iLvl, isPrefix);
        baseItem.AddAffix(affix);
    }
    
    return baseItem;
}
```
