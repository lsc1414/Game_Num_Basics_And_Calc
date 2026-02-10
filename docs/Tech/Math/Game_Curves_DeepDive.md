---
sidebarTitle: "游戏中的曲线艺术"
title: "游戏中的曲线艺术"
---
> **摘要**：本文聚焦「游戏中的曲线艺术」，梳理核心概念、关键方法与落地实践。

> [!TIP] > **"God does not build in straight lines."** (上帝不造直线) — Prometheus
> 在游戏开发中，直线通常代表着机械与僵硬，而曲线则赋予了生命、动感与平衡。

本文档旨在系统性地梳理游戏开发中涉及的各类“曲线”，从微观的动画插值到宏观的数值成长。

## 1. 🌊 缓动函数 (Easing Functions) - 赋予运动以质感

最基础的曲线，用于描述一个数值如何从 A 变化到 B。

### 1.1 📏 线性 (Linear) vs 〰️ 非线性

- **Linear (`t`)**: 匀速运动。感觉机械、无聊。
- **Ease In (`t^2`)**: 加速。模拟重力下落，或车辆启动。
- **Ease Out (`1 - (1-t)^2`)**: 减速。模拟摩擦力停止，最常用的 UI 动画曲线。
- **Ease In Out**: 先加速后减速。模拟生物的自然运动。

### 1.2 🧮 常用公式 (Math)

```csharp
public static class Easing {
    // 1. Sine (正弦) - 柔和
    public static float EaseInSine(float t) => 1 - Mathf.Cos((t * Mathf.PI) / 2);
    public static float EaseOutSine(float t) => Mathf.Sin((t * Mathf.PI) / 2);

    // 2. Power Curves (Quad, Cubic, Quart, Quint) - 力度递增
    public static float EaseInQuad(float t) => t * t;
    public static float EaseOutQuad(float t) => 1 - (1 - t) * (1 - t);

    public static float EaseInCubic(float t) => t * t * t;
    public static float EaseOutCubic(float t) => 1 - Mathf.Pow(1 - t, 3);

    public static float EaseInQuart(float t) => t * t * t * t;
    public static float EaseOutQuart(float t) => 1 - Mathf.Pow(1 - t, 4);

    public static float EaseInQuint(float t) => t * t * t * t * t;
    public static float EaseOutQuint(float t) => 1 - Mathf.Pow(1 - t, 5);

    // 3. Expo (指数) - 爆发
    public static float EaseInExpo(float t) => t == 0 ? 0 : Mathf.Pow(2, 10 * t - 10);
    public static float EaseOutExpo(float t) => t == 1 ? 1 : 1 - Mathf.Pow(2, -10 * t);

    // 4. Circ (圆形) - 突然
    public static float EaseInCirc(float t) => 1 - Mathf.Sqrt(1 - Mathf.Pow(t, 2));
    public static float EaseOutCirc(float t) => Mathf.Sqrt(1 - Mathf.Pow(t - 1, 2));

    // 5. Back (回弹) - 预备/过冲
    public static float EaseInBack(float t) {
        float c1 = 1.70158f; float c3 = c1 + 1;
        return c3 * t * t * t - c1 * t * t;
    }
    public static float EaseOutBack(float t) {
        float c1 = 1.70158f; float c3 = c1 + 1;
        return 1 + c3 * Mathf.Pow(t - 1, 3) + c1 * Mathf.Pow(t - 1, 2);
    }

    // 6. Elastic (弹簧) - 弹性
    public static float EaseOutElastic(float t) {
        float c4 = (2 * Mathf.PI) / 3;
        return t == 0 ? 0 : t == 1 ? 1 : Mathf.Pow(2, -10 * t) * Mathf.Sin((t * 10 - 0.75f) * c4) + 1;
    }

    // 7. Bounce (弹跳) - 撞击
    public static float EaseOutBounce(float t) {
        float n1 = 7.5625f; float d1 = 2.75f;
        if (t < 1 / d1) return n1 * t * t;
        else if (t < 2 / d1) return n1 * (t -= 1.5f / d1) * t + 0.75f;
        else if (t < 2.5f / d1) return n1 * (t -= 2.25f / d1) * t + 0.9375f;
        else return n1 * (t -= 2.625f / d1) * t + 0.984375f;
    }
}
```

---

### 1.4 ⚡ 速查表 (Cheat Sheet) - 哪种情况用哪种？

|        Easing 类型               |        曲线示意 (Shape)        |        感觉描述 (Feel)                                                               |        典型应用场景 (Use Case)                                                       |
|        :-----------------        |        :---------------        |        :---------------------------------------------------------------------        |        :---------------------------------------------------------------------        |
|        **Sine (正弦)**           |        `  /`                   |        **最柔和**。变化非常细微，几乎感觉不到加速/减速的过程。                       |        云朵飘动、呼吸灯、背景元素的缓慢移动。                                        |
|        **Quad (二次方)**         |        ` _/`                   |        **自然**。有明显的加速或减速感，但不过分。最常用的标准曲线。                  |        UI 窗口弹出 (Out)、角色起跑 (In)、普通物体的移动。                            |
|        **Cubic (三次方)**        |        ` __/`                  |        **有力**。比 Quad 更强烈的加减速。                                            |        赛车加速、更有“重量感”的 UI 交互。                                            |
|        **Quart (四次方)**        |        `\_\_\_                 |        `                                                                             |        **剧烈**。起步非常慢，或者刹车非常急。                                        |
|        **Quint (五次方)**        |        `                       |        `                                                                             |        **极度剧烈**。几乎是瞬间完成大部分位移，只在最后一点点时间里缓慢到位。        |
|        **Expo (指数)**           |        `                       |        `                                                                             |        **机械感**。基于 2 的幂。起步极慢，然后突然爆发。                             |
|        **Circ (圆形)**           |        `⌒`                     |        **突然**。基于半圆。加速极快，给人一种“突然动起来”的感觉。                    |        某种机械装置的卡扣、急转弯。                                                  |
|        **Back (回弹)**           |        ` ~/`                   |        **预备动作/过冲**。In: 先向后退一点再冲出去；Out: 冲过头一点再缩回来。        |        强调动作的力度。UI 按钮点击 (Out)、怪物蓄力攻击 (In)。                        |
|        **Elastic (弹簧)**        |        `↝`                     |        **弹性**。像橡皮筋一样来回摆动，幅度逐渐减小。                                |        绳索挂载的物体、果冻效果、卡通风格的 UI 出现。                                |
|        **Bounce (弹跳)**         |        ` /\/`                  |        **撞击**。像皮球掉在地上的反弹轨迹。                                          |        物体落地、菜单板子掉落下来。                                                  |

**In vs Out vs InOut**:

- **🚀 In**: 从 0 加速。适合“进入视野”或“开始运动”。(如：火箭升空)
- **🛑 Out**: 减速到 0。适合“停在某处”或“进入待机”。(如：UI 弹窗停在屏幕中间)
- **🔄 InOut**: 先加速后减速。适合“从 A 移动到 B”。(如：摄像机运镜)

---

## 2. ✒️ 贝塞尔曲线 (Bezier Curves) - 路径与轨迹

用于定义复杂的路径，如导弹轨迹、赛道形状或 UI 连线。

### 2.1 原理

贝塞尔曲线本质上是“线性插值的线性插值” (Lerp of Lerps)。

- **二阶 (Quadratic)**: 需要 3 个点 (起点 P0, 控制点 P1, 终点 P2)。
    - 先在 P0-P1 间 Lerp 出 A，在 P1-P2 间 Lerp 出 B。
    - 再在 A-B 间 Lerp 出最终点。
- **三阶 (Cubic)**: 需要 4 个点。Unity 的 `AnimationCurve` 内部就是分段的三阶贝塞尔。

### 2.2 代码实现

```csharp
// 二阶贝塞尔
public static Vector3 GetPoint(Vector3 p0, Vector3 p1, Vector3 p2, float t) {
    t = Mathf.Clamp01(t);
    float oneMinusT = 1f - t;
    return oneMinusT * oneMinusT * p0 +
           2f * oneMinusT * t * p1 +
           t * t * p2;
}
```

---

## 3. 📊 数值成长曲线 (Gameplay Progression Curves)

用于 RPG 升级、经济膨胀或难度控制。

### 3.1 🚀 幂函数 (Power Curve)

$$y = Base \times x^p$$

- **应用**: 升级所需经验值。
- **特点**: 早期平缓，后期陡峭。让玩家前期快速升级获得爽感，后期升级变慢延长游戏寿命。

### 3.2 🛡️ 对数函数 (Logarithmic Curve)

$$y = C \times \ln(x)$$

- **应用**: 护甲减伤公式 (Diminishing Returns)。
    - `DamageReduction = Armor / (Armor + Constant)`
- **特点**: 收益递减。防止玩家堆叠单一属性导致无敌。

### 3.3 🪜 阶梯函数 (Step Function)

- **应用**: 装备解锁、技能质变。
- **特点**: 只有达到特定等级，能力才会有跃升。

---

## 4. 🎮 Unity 中的 AnimationCurve

Unity 内置的 `AnimationCurve` 是极其强大的工具，不仅用于动画，还可用于逻辑配置。

### 4.1 🎯 技巧：归一化采样

不要在 Curve 里填具体数值 (如 0 到 1000 伤害)。

- **做法**: Curve 的 X 和 Y 都保持在 0-1 区间。
- **代码**: `float damage = maxDamage * curve.Evaluate(currentLevel / maxLevel);`
- **优点**: 策划调整数值上限时，不需要重画曲线。

### 4.2 🎲 技巧：作为概率分布

可以用 Curve 来模拟非均匀随机分布。

- **X 轴**: 随机数 (0-1)。
- **Y 轴**: 实际输出值。
- **形状**: 如果曲线是“S”型，那么输出值会集中在中间；如果曲线是“U”型，输出值集中在两端。

---

## 5. 🛠️ 塑形函数 (Shaping Functions)

在 Shader 和程序化生成中，我们需要更高级的数学来“重塑”信号。

### 5.1 🗺️ Remap (重映射)

将一个区间的值映射到另一个区间。

```csharp
float Remap(float value, float from1, float to1, float from2, float to2) {
    return (value - from1) / (to1 - from1) * (to2 - from2) + from2;
}
```

### 5.2 🌫️ SmoothStep

比 Lerp 更平滑的插值，两端斜率为 0。常用于地形混合、纹理边缘处理。

$$y = x^2(3 - 2x)$$

### 5.3 🏓 PingPong

让数值在 0 和 1 之间往复运动。
`Mathf.PingPong(Time.time, 1f)`

---

## 6. 📚 扩展阅读

- [The Book of Shaders: Shaping Functions](https://thebookofshaders.com/05/) - 必读，图形学中的曲线圣经。
- [GDC: Math for Game Developers](https://www.youtube.com/watch?v=s7V7K8y8X2c)
