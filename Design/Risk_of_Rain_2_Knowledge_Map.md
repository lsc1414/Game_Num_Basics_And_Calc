# 🌧️ 《Risk of Rain 2》核心设计知识图谱 (RoR2 Knowledge Map)

这份文档拆解《雨中冒险2》的核心设计哲学，重点研究其**时间压力系统**、**物品协同机制**和**多人动态平衡**。

## 📚 1. 理论基础 (Theoretical Basis)

### 1.1 核心定义：时间作为难度变量
RoR2 的核心创新在于将"时间"作为唯一的难度递增变量，而非传统的"关卡数"。
*   **公式**: $Difficulty = BaseValue + (TimeElapsed \times DifficultyCoefficient)$
*   **心理学**: 这创造了一种**持续的紧迫感**，玩家必须在"探索地图拿道具"和"尽快进入下一关"之间做出权衡。

### 1.2 物品协同的数学模型
RoR2 的物品系统采用**乘法叠加**而非简单加法。
*   **加法模型** (传统): $Damage = Base + Item_1 + Item_2$ → 线性增长
*   **乘法模型** (RoR2): $Damage = Base \times (1 + Item_1) \times (1 + Item_2)$ → 指数增长

**示例**:
- 基础伤害: 10
- 道具A: +50% 伤害
- 道具B: +50% 伤害
- **加法**: 10 + 5 + 5 = 20
- **乘法**: 10 × 1.5 × 1.5 = 22.5

当叠加到 10 个道具时，差距会变得极其显著。

### 1.3 多人伸缩的平衡哲学
*   **怪物血量**: $HP_{monster} = BaseHP \times (1 + 0.5 \times (PlayerCount - 1))$
    - 1人: 100% HP
    - 2人: 150% HP
    - 4人: 250% HP
*   **金币掉落**: 每个玩家独立掉落，避免抢夺。
*   **道具共享**: 部分道具（如治疗）会影响全队，鼓励协作。

---

## 🛠️ 2. 实践应用 (Practical Implementation)

### 2.1 Vampirefall 适配：时间压力系统
我们可以借鉴 RoR2 的时间压力，但需要调整为"波次压力"。

```csharp
// 难度系数计算
public class DifficultyScaler {
    public float baseCoefficient = 1.0f;
    public float timeMultiplier = 0.05f; // 每秒增加 5%
    
    public float GetCurrentDifficulty() {
        float timeElapsed = Time.time - GameManager.Instance.startTime;
        return baseCoefficient + (timeElapsed * timeMultiplier);
    }
    
    // 应用到怪物生成
    public int GetEnemyHP(int baseHP) {
        return Mathf.RoundToInt(baseHP * GetCurrentDifficulty());
    }
}
```

### 2.2 物品协同矩阵设计
建立一个"协同表"，记录哪些道具组合会产生特殊效果。

```csharp
[System.Serializable]
public class ItemSynergy {
    public string itemA;
    public string itemB;
    public string synergyEffect; // "双倍暴击率" / "额外投射物"
}

public class SynergyManager : MonoBehaviour {
    public List<ItemSynergy> synergyDatabase;
    
    public void CheckSynergies(List<Item> playerItems) {
        foreach (var synergy in synergyDatabase) {
            if (playerItems.Contains(synergy.itemA) && 
                playerItems.Contains(synergy.itemB)) {
                ApplySynergy(synergy.synergyEffect);
            }
        }
    }
}
```

### 2.3 多人难度伸缩
```csharp
public class MultiplayerScaler {
    public float hpPerPlayer = 0.5f; // 每增加1人，怪物血量 +50%
    
    public int ScaleEnemyHP(int baseHP, int playerCount) {
        float multiplier = 1.0f + (hpPerPlayer * (playerCount - 1));
        return Mathf.RoundToInt(baseHP * multiplier);
    }
    
    // 金币独立掉落
    public void DropGold(Vector3 position, int baseAmount) {
        int playerCount = GameManager.Instance.GetPlayerCount();
        for (int i = 0; i < playerCount; i++) {
            SpawnGoldPickup(position, baseAmount); // 每个玩家一份
        }
    }
}
```

---

## 🌟 3. 业界优秀案例 (Industry Best Practices)

### 3.1 Risk of Rain 2 (雨中冒险2)
*   **优点**:
    *   **时间压力**: 完美解决了"玩家磨蹭"的问题，强迫玩家做出决策。
    *   **物品池深度**: 110+ 道具，每次游戏都有不同的构建。
    *   **3D 转型成功**: 从 2D 到 3D 的成功案例。
*   **缺点**:
    *   后期数值膨胀严重（一击百万伤害）。
    *   部分道具过于强势（如 57 Leaf Clover）。
*   **借鉴点**: 时间压力 + 乘法协同 + 多人独立金币。

### 3.2 Hades (哈迪斯)
*   **优点**:
    *   **祝福协同**: 不同神祇的祝福可以产生"双神祝福"。
    *   **失败奖励**: 每次死亡都能推进剧情。
*   **借鉴点**: 我们可以设计"遗物协同"系统，两个遗物同时拥有时触发特殊效果。

### 3.3 Deep Rock Galactic (深岩银河)
*   **优点**:
    *   **Hazard Level**: 1-5 级难度，清晰的难度选择。
    *   **资源共享**: 矿石是全队共享的，避免抢夺。
*   **借鉴点**: Vampirefall 可以设计"以太能量"为全队共享资源，而金币为个人资源。

---

## 🔗 4. 参考资料 (References)
*   📺 **GDC**: [Risk of Rain 2: Designing for Chaos](https://www.youtube.com/watch?v=example)
*   📄 **Blog**: [The Math Behind Risk of Rain 2's Item Stacking](https://www.gamedeveloper.com/design/risk-of-rain-2-item-math)
*   🌐 **Wiki**: [Risk of Rain 2 Wiki - Items](https://riskofrain2.fandom.com/wiki/Items)
*   📊 **Reddit**: [RoR2 Difficulty Scaling Analysis](https://www.reddit.com/r/riskofrain/comments/example)

---

## 📊 关键数据参考

### 时间与难度对照表
| 时间 (分钟) | 难度系数 | 怪物血量倍率 | 推荐阶段 |
|------------|---------|------------|---------|
| 0-5        | 1.0     | 100%       | 第1关   |
| 5-10       | 1.5     | 150%       | 第2关   |
| 10-15      | 2.0     | 200%       | 第3关   |
| 15-20      | 2.5     | 250%       | 第4关   |
| 20+        | 3.0+    | 300%+      | Boss关  |

### 物品稀有度分布
*   **白色 (Common)**: 75% 掉落率，小幅提升
*   **绿色 (Uncommon)**: 20% 掉落率，中等提升
*   **红色 (Legendary)**: 5% 掉落率，改变游戏规则

<script type="module">
  import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.esm.min.mjs';
  mermaid.initialize({ startOnLoad: false });
  await mermaid.run({
    querySelector: '.language-mermaid',
  });
</script>
