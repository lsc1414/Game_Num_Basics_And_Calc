# 🎲 肉鸽强化系统 (Roguelike Perks & Boons)

本文档定义了局内成长系统（Level Up Bonuses），这是 Roguelike 体验的核心，决定了单局游戏的重玩价值。

---

## 1. 系统概述 (Overview)

*   **获取方式:** 角色升级 (EXP)、通过精英波次、打开诅咒宝箱。
*   **选择机制:** 典型的“三选一” (Drafting)。
*   **稀有度:** 普通 (Common) < 稀有 (Rare) < 史诗 (Epic) < 传说 (Legendary)。

## 2. 强化词条分类 (Perk Categories)

为了防止池子太杂，Perk 被分为标签化的“池子”。

### 2.1 基础属性类 (Stat Boosts)
*最通用，权重最高，但由于边际效应递减，后期收益低。*
*   **蛮力 (Brutality):** 增加 10% 物理伤害。
*   **迅捷 (Alacrity):** 增加 8% 攻击速度。
*   **坚韧 (Tenacity):** 增加 10% 最大生命值。

### 2.2 机制质变类 (Mechanic Alterations) - *传说级*
*这类 Perk 会改变玩法逻辑。*
*   **血魔法 (Blood Magic):** 技能不再消耗法力，改为消耗生命值。技能伤害 +30%。
*   **多重投射 (Multishot):** 投射物数量 +2，但伤害修正为 60%。
*   **连锁反应 (Chain Reaction):** 暴击时有 50% 几率触发闪电链。

### 2.3 塔防协同类 (Tower Synergy)
*强化“塔”与“人”的连接。*
*   **工匠精神 (Artificer):** 站在塔周围 5米 内，角色和塔的攻速都 +15%。
*   **废料回收 (Scrapper):** 敌人死在塔的射程内，掉落 Scrap 增加 20%。

## 3. 诅咒系统 (Curses)

高风险高回报机制。通常来源于“诅咒宝箱”或特殊祭坛。
*   **格式:** 获得一个强力 Buff，但永久背负一个 Debuff。
*   *例子:* **玻璃大炮 (Glass Cannon):** 造成伤害 +50%，但受到的伤害 +50%。
*   *例子:* **重力场 (Gravity):** 移速 -20%，但周围敌人也会被减速 20%。

## 4. 随机权重与算法 (RNG Weights)

为了避免“脸黑”导致无法通关，采用 **动态权重系统**。

1.  **标签偏好 (Tag Biasing):**
    *   如果玩家选择了“火焰”标签的 Perk，后续刷新出“火焰”相关 Perk 的权重 x 1.5。
    *   这有助于玩家构建流派 (Build)，而不是拿到一堆不相关的散件。
2.  **防脸黑 (Pity Timer):**
    *   每 5 次未出现“史诗”以上选项，下一次出现的概率翻倍。
3.  **重随 (Reroll):**
    *   消耗局内货币 (Gold) 刷新列表。价格随次数指数增长。

## 5. 数据结构参考 (JSON)

```json
{
  "id": "Perk_BloodMagic",
  "name": "Blood Magic",
  "rarity": "Legendary",
  "tags": ["Mana", "Life", "Keystone"],
  "description": "Skills cost Life instead of Mana. Deal 30% more Damage.",
  "modifiers": [
    { "stat": "ManaCost", "value": -100, "type": "More" },
    { "stat": "CostType", "value": "Life", "type": "Override" },
    { "stat": "GlobalDamage", "value": 0.3, "type": "More" }
  ],
  "weight": 50
}
```
