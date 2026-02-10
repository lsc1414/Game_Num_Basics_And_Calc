---
sidebarTitle: "掉落规则与战利品系统"
title: "掉落规则与战利品系统"
---
> **摘要**：本文档定义了怪物死亡或宝箱开启时，生成战利品的算法。核心目标是平衡“惊喜感”与“经济稳定”。

## 1. 掉落预算系统 (Drop Budget System)

为了防止割草游戏中成千上万的怪物导致满地垃圾（性能杀手+视觉污染），我们不使用“每只怪单独Roll点”的逻辑。

### 1.1 蓄水池机制 (The Bucket)
*   玩家击杀怪物时，不直接掉落物品，而是累积 **[掉落点数 (Drop Points)]**。
*   `Points += MonsterRarity * PlayerMF`。
*   当 `Points >= Threshold` 时，触发一次真实的掉落判定 (Roll)。
*   **优势:** 杀 100 只小怪和杀 1 只精英怪，最终期望收益一致，且避免了同屏几百个物品渲染。

## 2. 掉落表结构 (Loot Table Structure)

掉落表是分层嵌套的。

*   **Master Table (全局表):**
    *   -> `Currency` (通货): 30%
    *   -> `Equipment` (装备): 20%
    *   -> `Consumables` (消耗品): 10%
    *   -> `Nothing` (空气): 40%

*   **Sub-Table: Equipment:**
    *   -> `Weapon`: 40%
    *   -> `Armor`: 40%
    *   -> `Jewelry`: 20%

## 3. 智能掉落 (Smart Loot)

为了减少垃圾时间，系统会根据玩家当前职业/属性微调掉落。

*   **机制:** 每次掉落装备时，有 **15%** 的概率触发 Smart Loot。
*   **效果:**
    1.  **底材适配:** 必定掉落当前角色可用的武器类型（如法师不掉大斧）。
    2.  **主属性锁定:** 必定包含角色的主属性（如法师装备必带智力）。

*   *注意:* 比例不能太高 (15-20%)，否则玩家无法为其他小号积累装备，失去了“刷宝给小号”的乐趣。

## 4. 物品过滤与自动拾取 (Filter & Auto-Loot)

*   **自动拾取:** 金币、材料 (Scrap) 等非占用背包格子的资源，范围内自动吸附。
*   **装备过滤:** 允许玩家设置 Loot Filter。
    *   *规则:* `Hide Normal Items`, `Show Legendary`, `Highlight 'Fire Damage'`.
    *   被过滤的物品在掉落时**不渲染模型**，也不播放音效，极大节省性能。

## 5. 宝箱类型 (Chest Types)

*   **普通宝箱:** 标准掉落表。
*   **华丽宝箱 (Ornate):** 必定掉落至少一件稀有 (Rare) 装备。
*   **军火库 (Arsenal):** 只掉落武器。
*   **奥术保险箱 (Arcane Strongbox):** 受到怪物守护。开启时并在周围生成一波精英怪。清完怪后掉落大量通货。

---

## 6. 算法伪代码 (Algorithm)

```python
def OnMonsterDie(monster, player):
    # 1. 累积预算
    player.DropBucket += monster.DropValue * (1 + player.ItemRarity)
    
    # 2. 检查阈值
    if player.DropBucket >= DROP_THRESHOLD:
        player.DropBucket -= DROP_THRESHOLD
        
        # 3. 执行掉落
        LootItem item = RollLootTable(monster.Level)
        
        # 4. 智能掉落修正
        if Random() < 0.15:
            item = ApplySmartLoot(item, player.Class)
            
        SpawnItemWorldObject(item, monster.Position)
```
