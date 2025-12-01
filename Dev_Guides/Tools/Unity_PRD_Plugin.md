# 🛠️ Unity PRD 算法插件：伪随机分布的 C# 实现

**文档目标**：提供一个开箱即用的 C# 类库，用于在 Unity 中替换 `Random.value`，实现“暴击/闪避”等概率事件的“保底”与“防连黑”。

---

## 1. 为什么需要 PRD？

在真随机 (True Random) 中，`25%` 的暴击率意味着你可能连续 10 次不暴击（体验极差），也可能连续 10 次暴击（平衡崩坏）。
**PRD (Pseudo-Random Distribution)** 通过动态调整概率 `C` 值，让“期望概率”稳定在 25%，且几乎不会出现长连黑或长连爆。

*参考：Dota 2 / Warcraft 3 算法。*

---

## 2. 核心算法原理

每次攻击：
*   `P_actual = C * N`
    *   `C`: 预计算的基础常数（对应目标概率）。
    *   `N`: 连续未触发的次数（从 1 开始）。
*   如果触发：重置 `N = 1`。
*   如果未触发：`N++`。

---

## 3. C# 代码实现 (PRD.cs)

将此脚本放入 `Assets/Scripts/Utils`。

```csharp
using System.Collections.Generic;
using UnityEngine;

public static class PRD
{
    // 预计算的 C 值查找表 (Key: 目标概率 0~1, Value: C常数)
    // 常用值：25% -> 0.085, 15% -> 0.032, etc.
    // 实际项目中建议预计算存入 Dictionary 或 Array
    private static readonly Dictionary<int, float> C_Constants = new Dictionary<int, float>()
    {
        { 5, 0.0038f },
        { 10, 0.0147f },
        { 15, 0.0322f },
        { 20, 0.0557f },
        { 25, 0.0847f },
        { 30, 0.1189f },
        { 35, 0.1579f },
        { 40, 0.2015f },
        { 45, 0.2493f },
        { 50, 0.3021f },
        { 60, 0.4226f },
        { 70, 0.5714f },
        { 80, 0.7500f },
        // 更多值可查阅 Design/Numerical_Manual.md 或在线计算
    };

    /// <summary>
    /// PRD 状态追踪器
    /// 每个需要计算 PRD 的实体（如一个英雄的暴击）都需要一个实例
    /// </summary>
    public class Tracker
    {
        private int _counter = 1;
        
        /// <summary>
        /// 尝试触发事件
        /// </summary>
        /// <param name="targetProbability">目标概率 (0.0 ~ 1.0)</param>
        /// <returns>是否触发</returns>
        public bool Roll(float targetProbability)
        {
            // 1. 获取 C 值 (简单起见，这里做线性插值或直接取整查找)
            // 实际优化：可以将 targetProbability 转为 int (0-100) 查表
            float c = GetC(targetProbability);
            
            // 2. 计算当前概率
            float currentP = c * _counter;
            
            // 3. 随机判定
            if (Random.value < currentP)
            {
                _counter = 1; // 重置
                return true;
            }
            else
            {
                _counter++; // 累积
                return false;
            }
        }
    }

    private static float GetC(float p)
    {
        int pInt = Mathf.RoundToInt(p * 100);
        if (C_Constants.TryGetValue(pInt, out float c)) return c;
        
        // 简单回退：如果查不到表，使用真随机作为兜底
        // 或者实现二分查找插值
        return p; // 这里仅作示例，实际上应当报错或计算
    }
}
```

---

## 4. 使用示例

```csharp
public class HeroCombat : MonoBehaviour
{
    public float CritRate = 0.25f; // 25%
    private PRD.Tracker _critTracker = new PRD.Tracker();

    void Attack()
    {
        bool isCrit = _critTracker.Roll(CritRate);
        
        if (isCrit)
        {
            // 暴击逻辑
            Debug.Log("CRIT!");
        }
        else
        {
            // 普通伤害
            Debug.Log("Normal hit");
        }
    }
}
```

---

## 5. 性能优化版 (Struct + Job System)

如果是 ECS 架构，不要使用 Class。

```csharp
public struct PrdState
{
    public int Counter;
    
    public bool Roll(float targetProb, ref Unity.Mathematics.Random random)
    {
        float c = LookupC(targetProb);
        float p = c * Counter;
        
        if (random.NextFloat() < p)
        {
            Counter = 1;
            return true;
        }
        else
        {
            Counter++;
            return false;
        }
    }
}
```
---
*注：完整的 C 常数表请参考数值策划文档，或使用 `Design/Calculator/index.html` 工具生成。*
