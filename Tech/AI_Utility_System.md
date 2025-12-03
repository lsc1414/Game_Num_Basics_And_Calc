# Utility AI 决策系统 (Utility AI Decision System)

> [!IMPORTANT]
> **核心理念**: AI 不应该只是“处于”某种状态 (State)，而应该根据当前环境评估所有可能行为的“效用” (Utility)，并选择最优解。

Utility AI (效用 AI) 是一种基于**评分 (Scoring)** 的决策架构。与传统的 FSM (有限状态机) 或行为树相比，它在处理模糊逻辑和多目标权衡时表现出极高的涌现性 (Emergent Behavior)。

---

## 1. 为什么选择 Utility AI? (Why Utility AI?)

### FSM vs Utility AI
*   **FSM (有限状态机)**: 
    *   逻辑: `IF (Health < 30%) THEN Transition(Retreat)`
    *   缺点: 僵硬。如果血量 31% 但敌人拿着火箭筒怎么办？状态转换连线会变成“蜘蛛网”。
*   **Utility AI**:
    *   逻辑: `Score(Retreat) = Curve(Health) * Curve(EnemyThreat) * Curve(CoverDistance)`
    *   优点: 动态权衡。即使血量健康，如果威胁极大且掩体很近，AI 依然可能选择撤退。

### 适用场景
*   **模拟类游戏 (The Sims)**: 需求系统 (饿了吃，困了睡，但如果房子着火了，灭火的效用会瞬间超过睡觉)。
*   **战术射击 (Killzone/Halo)**: 复杂的战场评估 (掩体质量、侧翼包抄、武器射程)。
*   **RPG/RTS**: 复杂的技能释放优先级。

---

## 2. 数学模型 (The Mathematical Model)

Utility AI 的核心是将所有“考虑因素” (Considerations) 归一化为 `0.0` 到 `1.0` 之间的浮点数。

### 2.1 响应曲线 (Response Curves)
输入通常是原始游戏数据 (距离、血量、时间)，输出是 **效用 (Utility)**。我们需要通过曲线来映射这种关系。

| 曲线类型 | 形状描述 | 典型应用 |
| :--- | :--- | :--- |
| **Linear (线性)** | `/` 或 `\` | 简单的比例关系。如：金币越多越富有。 |
| **Quadratic (二次)** | `J` 型 | 极端值才重要。如：只有极度靠近悬崖时，恐惧感才急剧上升。 |
| **Logistic (S形)** | `S` 型 | 阈值敏感。如：血量在 40%-60% 之间时，治疗欲望从低急剧变高。 |
| **Logit (对数)** | 倒 `J` 型 | 边际递减。如：前 100 金币很珍贵，之后的一百万金币效用递减。 |

### 2.2 组合公式 (Aggregation)
如何将多个因素组合成一个最终分数？

*   **加权平均 (Weighted Average)**: $Score = w_1 C_1 + w_2 C_2$
    *   缺点: 容易被某个高分项“平均”掉，忽略了致命缺陷。
*   **乘法 (Multiplication)**: $Score = C_1 \times C_2 \times C_3$
    *   **推荐**: 只要有一项是 0 (例如：没有弹药)，总分即为 0 (无法射击)。这符合逻辑否决。
*   **补偿因子 (Compensation)**: $Score = (1 - (1-C_1) \times (1-C_2))$
    *   用于计算“至少满足一项”的逻辑。

---

## 3. 架构设计 (Architecture Design)

在 Unity 中，我们可以使用 `ScriptableObject` 构建高度模块化的 Utility 系统。

### 3.1 核心组件
1.  **Context (上下文)**: 包含 AI 自身、目标、世界状态的数据包。
2.  **Consideration (考虑因素)**: 
    *   输入: `Context`
    *   参数: `AnimationCurve` (响应曲线)
    *   输出: `0-1` 的 float
3.  **Action (行为)**: 
    *   包含一组 `Consideration`。
    *   最终得分 = 所有 `Consideration` 的乘积。
4.  **Brain (大脑/决策器)**:
    *   每帧(或每0.1秒)遍历所有 `Action`。
    *   执行得分最高的 `Action`。

### 3.2 代码结构示例

```csharp
// 1. 考虑因素基类
public abstract class Consideration : ScriptableObject {
    public AnimationCurve responseCurve;
    public abstract float Score(AIContext context);
    
    protected float Map(float rawValue) {
        return responseCurve.Evaluate(Mathf.Clamp01(rawValue));
    }
}

// 2. 具体实现：我的血量
[CreateAssetMenu(menuName = "AI/Considerations/My Health")]
public class HealthConsideration : Consideration {
    public override float Score(AIContext context) {
        // 归一化血量
        float rawHealth = context.self.currentHealth / context.self.maxHealth;
        // 如果曲线是反向的（血越少分越高），在编辑器里画一条从左上(0,1)到右下(1,0)的线
        return Map(rawHealth);
    }
}

// 3. 行为定义
[CreateAssetMenu(menuName = "AI/Action")]
public class UtilityAction : ScriptableObject {
    public string actionName;
    public List<Consideration> considerations;
    
    public float Evaluate(AIContext context) {
        float score = 1f;
        foreach (var con in considerations) {
            score *= con.Score(context);
            if (score == 0) return 0; // 剪枝优化
        }
        return score;
    }
}
```

---

## 4. 最佳实践与优化 (Best Practices)

### 4.1 惯性 (Inertia) / 滞后 (Hysteresis)
为了防止 AI 在两个分数相近的行为之间疯狂切换 (抖动)，需要引入“惯性”。
*   **规则**: 当前正在执行的行为，在下一帧评分时获得 **1.1x** 或 **+0.1** 的加成。
*   **效果**: 除非新行为的效用显著高于当前行为，否则保持现状。

### 4.2 双层架构 (Dual-Layer)
Utility AI 负责**决策 (Decision Making)**，FSM/行为树负责**执行 (Execution)**。
*   Utility AI 决定：“我现在应该**进攻**”。
*   FSM 执行：“播放拔剑动画 -> 寻路 -> 挥砍”。

### 4.3 性能优化
*   **分帧计算**: 不要每帧计算所有 AI。将 AI 分组，每帧只更新一组。
*   **LOD (Level of Detail)**: 远处的 AI 降低决策频率（例如 1秒一次），近处的 AI 高频决策（0.1秒一次）。

---

## 5. 业界案例 (Industry Cases)

### The Sims (模拟人生)
*   **机制**: 基于需求的 Utility AI。
*   **Interaction Object**: 椅子、冰箱等物体会“广播”它们能提供的效用。
    *   冰箱: 提供“饱腹感”。
    *   床: 提供“精力”。
*   **AI**: 遍历周围物体，寻找能最大化当前匮乏需求的物体。

### Killzone 2 (杀戮地带 2)
*   **机制**: 动态战术位置评分 (TPS)。
*   **实现**: 战场被划分为网格。每个格子根据掩体方向、视线遮挡、距离队友远近进行动态打分。
*   **结果**: AI 会自然地寻找最佳掩体，侧翼包抄，而不需要硬编码脚本。

---

## 6. 扩展阅读
*   [GDC 2015: Building a Better Centaur (Utility AI in Infinite Crisis)](https://www.gdcvault.com/play/1021848/Building-a-Better-Centaur-AI)
*   [Dave Mark's "Behavioral Mathematics for Game AI"](https://www.amazon.com/Behavioral-Mathematics-Game-AI-Applied/dp/1584506849)
