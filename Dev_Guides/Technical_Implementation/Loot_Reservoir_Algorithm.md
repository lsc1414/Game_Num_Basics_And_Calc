# 💰 掉落蓄水池算法 (Loot Reservoir Algorithm)：恒定 DPM 的 0GC 实现

**文档目标**：解决高频战斗（每秒死亡 50+ 怪物）下的掉落性能问题，并实现策划对“掉落节奏”的精确控制。

---

## 1. 传统掉落的痛点

在传统的 RPG 中，每个怪物死亡时都会跑一次 Loot Table：
```csharp
// ❌ 坏味道：每秒跑 50 次，GC 爆炸
void OnDie() {
    if (Random.value < 0.01f) DropItem(); // 1% 几率
}
```

**问题：**
1.  **性能开销**：每秒 50 次 `Random` 调用 + 复杂的 Loot Table 权重计算。
2.  **方差过大**：可能连续 10 分钟不掉落，然后 1 秒内掉 5 个。
3.  **无法控制总量**：如果玩家用修改器加速杀怪，经济系统会崩溃。

---

## 2. 蓄水池模型 (The Reservoir Model)

我们不再问“这个怪掉不掉？”，而是问“**现在该不该掉？**”。

### 2.1 核心概念：掉落预算 (Drop Budget)
策划定义的不是“几率”，而是 **DPM (Drops Per Minute)**。
*   假设 DPM = 2.0（每分钟掉 2 个金装）。
*   那么每秒钟，蓄水池增加 `2.0 / 60 = 0.033` 的“掉落势能”。

### 2.2 算法逻辑
1.  有一个全局 float 变量 `_dropBudget`。
2.  每帧（或每秒）：`_dropBudget += dropRatePerSecond * Time.deltaTime`。
3.  当怪物死亡时：
    *   检查 `_dropBudget >= 1.0f`？
    *   **是**：触发掉落，`_dropBudget -= 1.0f`。
    *   **否**：只掉落普通金币（或不掉落），贡献一点点“运气值”给蓄水池（可选）。

---

## 3. 进阶：加权蓄水池 (Weighted Reservoir)

为了让“杀精英怪”比“杀小怪”更有价值，我们引入 **Score**。

### 3.1 怪物分值
*   小怪 (Minion): 1 分
*   精英 (Elite): 10 分
*   Boss: 100 分

### 3.2 阈值触发
设定一个 **Drop Threshold (掉落阈值)**，例如 500 分。
*   全局变量 `_currentScore`。
*   怪物死：`_currentScore += mob.Score`。
*   如果 `_currentScore > Threshold`：
    *   触发掉落。
    *   `_currentScore = 0` (或者保留溢出部分 `_currentScore -= Threshold`)。
    *   **动态阈值**：下次阈值可以在 `450 ~ 550` 之间浮动，避免节奏太死板。

---

## 4. 0 GC C# 实现代码

```csharp
public class LootSystem : MonoBehaviour
{
    // 策划配置：期望每杀多少分的怪掉一件装备
    public float ScorePerDrop = 100f;
    
    // 当前积累的分数
    private float _accumulatedScore = 0f;
    
    // 单例访问
    public static LootSystem Instance;

    public void OnEnemyKilled(float enemyScore, Vector3 pos)
    {
        _accumulatedScore += enemyScore;

        // 检查是否满足掉落条件
        // 使用 while 处理“一刀秒全屏”导致瞬间分数暴涨的情况
        while (_accumulatedScore >= ScorePerDrop)
        {
            SpawnLoot(pos);
            _accumulatedScore -= ScorePerDrop;
            
            // 可选：每次掉落后略微增加下一次的阈值，防止通货膨胀
            // ScorePerDrop *= 1.05f; 
        }
    }

    private void SpawnLoot(Vector3 pos)
    {
        // 从对象池获取掉落物，零 GC
        var item = PoolManager.Get(PrefabID.LegendaryItem);
        item.transform.position = pos;
    }
}
```

---

## 5. 优势总结

| 特性 | 传统概率法 | 蓄水池/预算算法 |
| :--- | :--- | :--- |
| **掉落节奏** | 极不稳定 (可能连黑) | **平滑且可控** |
| **性能开销** | 高 (每次死亡都 Roll) | **极低 (仅加法运算)** |
| **经济控制** | 难 (怪越多掉越多) | **完美 (恒定产出)** |
| **玩家体验** | "这游戏爆率太低" | "杀够怪一定会掉" (保底心理) |

---

## 6. 适用场景
*   **Vampire Survivors 类**：满屏怪，必须用此算法控制性能和产出。
*   **暗黑类 (Diablo)**：用于控制“传奇装备”的保底掉落。
*   **放置类**：挂机收益计算的核心逻辑。
