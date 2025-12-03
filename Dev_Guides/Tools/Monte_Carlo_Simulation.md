# 蒙特卡洛模拟 (Monte Carlo Simulation)

> [!WARNING]
> **Excel 的陷阱**: 静态表格无法模拟“运气”的连续性、复杂的技能触发链以及玩家的非理性行为。只有通过海量的随机模拟，才能看到系统的真实面貌。

在 Vampirefall 这种数值敏感的游戏中，蒙特卡洛模拟是验证设计意图的终极手段。

---

## 1. 为什么需要模拟? (Why Simulate?)

### 1.1 大数定律 (Law of Large Numbers)
设计师设定掉率为 1%。
*   **Excel**: 期望值是 100 次掉 1 个。
*   **现实**: 有人 1 次就掉 (欧皇)，有人 300 次都不掉 (非酋)。
*   **模拟**: 运行 100万次，你会发现非酋的体验极差，从而引入“保底机制” (Pity System)。

### 1.2 涌现性平衡 (Emergent Balance)
技能 A (击杀回血) + 技能 B (满血加攻) + 技能 C (攻击减CD)。
这种联动效果很难用公式计算。模拟器可以让这套 Build 自动运行 1000 小时，看它是否无敌。

---

## 2. 模拟器架构 (Simulator Architecture)

### 2.1 无头模式 (Headless Mode)
为了速度，模拟器必须剥离所有图形渲染、UI 和音频。
*   **纯数据层**: 只有 `GameData`、`CombatLogic` 和 `RNG`。
*   **虚拟时间**: 不使用 `Time.deltaTime`，而是使用 `Tick()`。

### 2.2 并行计算 (Parallelism)
利用多核 CPU。
*   **Unity Job System**: 适合处理大量并行的战斗计算。
*   **独立 C# 进程**: 如果逻辑与 Unity 引擎解耦较好，可以直接编译一个 Console App 运行模拟，速度比 Unity Editor 快 100 倍。

---

## 3. 关键指标与可视化 (Metrics & Visualization)

模拟结束后，我们需要分析 CSV 数据并生成图表。

### 3.1 TTK 分布 (Time To Kill Distribution)
*   **X轴**: 击杀时间 (秒)。
*   **Y轴**: 出现的次数。
*   **目标**: 应该是正态分布。如果出现双峰 (Bimodal)，说明有些怪物对特定 Build 过于克制。

### 3.2 生存曲线 (Survival Curve)
*   模拟 1000 次地牢探索。
*   记录玩家在第几层死亡。
*   **理想曲线**: 随着层数增加，存活率平滑下降。如果第 3 层存活率突然从 90% 跌到 10%，说明第 3 层难度断层。

### 3.3 经济通胀 (Economic Inflation)
*   模拟玩家 30 天的游戏行为。
*   监控金币的总产出 vs 总消耗。
*   防止后期金币溢出导致货币贬值。

---

## 4. 实践案例：掉落验证器 (Loot Validator)

```csharp
public class LootSimulator {
    public void SimulateDrops(int iterations) {
        Dictionary<string, int> dropCounts = new Dictionary<string, int>();
        int totalRuns = 0;

        // 模拟 100万次
        Parallel.For(0, iterations, i => {
            var loot = LootTable.Roll(); // 你的掉落逻辑
            lock (dropCounts) {
                if (!dropCounts.ContainsKey(loot.id)) dropCounts[loot.id] = 0;
                dropCounts[loot.id]++;
            }
        });

        // 输出报告
        foreach (var kvp in dropCounts) {
            float rate = (float)kvp.Value / iterations * 100f;
            Console.WriteLine($"Item: {kvp.Key}, Rate: {rate:F4}% (Expected: {GetExpectedRate(kvp.Key)}%)");
        }
    }
}
```

### 4.2 战斗模拟 (Combat Sim)
*   **输入**: 玩家属性 (攻击 100, 暴击 20%)，怪物属性 (血量 5000)。
*   **过程**: 循环 `Tick()` 直到一方死亡。
*   **输出**: 胜率、剩余血量百分比。

---

## 5. 扩展阅读
*   [Machinations.io](https://machinations.io/): 专业的游戏经济系统模拟工具。
*   [Diablo 3 Loot 2.0 Postmortem](https://www.youtube.com/watch?v=GqYjS2rtqS8): 暗黑3如何通过模拟拯救了掉落系统。
