# 🧙‍♂️ Unity 粒子系统深度研究 (Particle System Deep Dive)

> **"特效是游戏的化妆术，但也可能是显卡的火葬场。"**
>
> 本文档旨在解构 Unity 粒子系统 (Shuriken)，从美术制作管线 (Blender/Shader) 到程序控制 (C#)，再到设计分类。

---

## 📚 1. 理论基础 (Theoretical Basis)

### 🎇 特效分类学 (VFX Taxonomy)
在 *Vampirefall* 中，我们把特效分为三个层级，优先级递减：

1.  **Gameplay 关键特效 (High Priority)**
    *   **定义:** 玩家必须看到的逻辑反馈。
    *   **例子:** 怪物受击飙血、Boss 技能预警圈 (Telegraph)、玩家升级金光、掉落传说装备的光柱。
    *   **特点:** 高亮度、高饱和度、永远渲染 (Always Simulate)。
2.  **环境氛围特效 (Medium Priority)**
    *   **定义:** 增强沉浸感，但如果不显示也不影响玩。
    *   **例子:** 场景中的火把、漂浮的尘埃、远处的雷电、雨雪。
    *   **特点:** 只有在视野内渲染，低透明度。
3.  **修饰性特效 (Low Priority)**
    *   **定义:** 纯粹的 "Juice"。
    *   **例子:** 跑步脚下的烟尘、UI 按钮的流光、子弹拖尾的微弱扰动。
    *   **特点:** 性能吃紧时第一个被剔除。

### 🎨 节奏与动态 (Timing & Dynamics)
一个好的粒子特效通常遵循 **"预备-爆发-消散"** 的动画原则：
1.  **Anticipation (预备):** 聚气、发光变亮。 (0.1 - 0.3s)
2.  **Climax (爆发):** 粒子瞬间大量发射 (Burst)、冲击波扩散。 (1帧 - 0.2s)
3.  **Dissipation (消散):** 速度减缓、透明度渐变至0、体积变大。 (0.5s - 2s)

---

## 🛠️ 2. 实践应用 (Practical Implementation)

### 🏭 制作管线：Blender, Shader 与 Unity 的协奏

单纯靠 Unity 自带的“小球”做不出 3A 特效。现代工作流是三位一体的：

#### A. Blender: 形状的缔造者
粒子系统不仅能发射 Quad (面片)，还能发射 Mesh (模型)。
*   **碎块 (Debris):** 在 Blender 中破碎一个石头模型，导入 Unity 作为粒子发射的 `Renderer -> Mesh`。
*   **特殊光效形状:** 
    *   制作一个半球体或圆锥体模型。
    *   在 Unity 中给它上一个溶解 Shader。
    *   通过粒子系统控制其旋转和缩放，做出“旋风斩”或“护盾”效果。
    *   *UV 技巧:* 在 Blender 展 UV 时将 UV 拉直，可以让纹理在 Unity 里沿着模型“流动”。

#### B. Shader: 灵魂注入
不要只用 `Particles/Standard Surface`。
*   **溶解 (Dissolve):** 配合噪声图 (Noise Texture) 控制 Alpha Clip，做出灰飞烟灭的效果。
*   **畸变 (Distortion/Heat Haze):** 使用 `GrabPass` 或 URP 的 `CameraOpaqueTexture` 扭曲背景，表现爆炸的热浪或剑气的冲击波动。
*   **菲涅尔 (Fresnel):** 让粒子边缘发光，中间透明，极大地增强能量体的“体积感”。

#### C. Unity C#: 让粒子“活”起来 (Data-Driven VFX)
这是程序与美术的交汇点。**不要把特效做死 Prefab，要让它随数值变化。**

**案例：根据攻击力改变火球大小和颜色**

```csharp
using UnityEngine;

[RequireComponent(typeof(ParticleSystem))]
public class DynamicFireball : MonoBehaviour
{
    private ParticleSystem _ps;
    private ParticleSystem.MainModule _main;
    private ParticleSystem.EmissionModule _emission;

    void Awake()
    {
        _ps = GetComponent<ParticleSystem>();
        _main = _ps.main;
        _emission = _ps.emission;
    }

    /// <summary>
    /// 初始化火球状态
    /// </summary>
    /// <param name="damage">伤害值（影响大小）</param>
    /// <param name="isCrit">是否暴击（影响颜色）</param>
    public void Setup(float damage, bool isCrit)
    {
        // 1. 根据伤害值线性放大粒子
        // 基础大小 1.0，每 100 点伤害增加 0.5 倍大小
        float scaleFactor = 1.0f + (damage / 100.0f) * 0.5f;
        
        // ⚠️ 注意：不要直接改 transform.localScale，因为会被粒子系统覆盖。
        // 要改 StartSize。如果是 3D 粒子可能还需要改 startSize3D。
        _main.startSizeMultiplier = scaleFactor; 

        // 2. 暴击改变颜色
        if (isCrit)
        {
            // 暴击变紫火
            _main.startColor = new ParticleSystem.MinMaxGradient(Color.purple);
            
            // 暴击增加粒子数量 (Burst)
            // 这里的 GetBurst(0) 假设你 Prefab 里至少配置了一个 Burst
            var burst = _emission.GetBurst(0);
            burst.count = new ParticleSystem.MinMaxCurve(20, 30); // 增加爆裂感
            _emission.SetBurst(0, burst);
        }
    }
}
```

### 🧬 Vampirefall 核心模块速查

1.  **Emission (发射):**
    *   `Rate over Time`: 持续喷射（如喷火器）。
    *   `Bursts`: 瞬间爆发（如爆炸、开枪）。**打击感来源**。
2.  **Shape (形状):**
    *   `Cone`: 最常用，调节 Angle 可以变成扇形或圆柱。
    *   `Mesh`: 从模型表面发射（如全身燃烧的效果）。
3.  **Velocity over Lifetime:**
    *   模拟空气阻力（Linear Drag）。
    *   `Orbital`: 制作围绕中心旋转的魔法粒子。
4.  **Size over Lifetime:**
    *   **必调曲线:** 同样是 `0 -> 1 -> 0` (从小变大再消失)，这比突然消失要自然得多。
5.  **Render Mode:**
    *   `Billboard`: 永远朝向摄像机（性能最好）。
    *   `Stretched Billboard`: 速度越快拉得越长（模拟速度线、火花）。

---

## 🌟 3. 业界优秀案例 (Industry Best Practices)

### ⚔️ Hades (哈迪斯)
*   **清晰度优先:** 即使满屏弹幕，Hades 的特效也非常“克制”。敌人的子弹通常是**高对比度的纯色轮廓**，没有多余的模糊光晕，确保玩家一眼就能识别判定范围。
*   **受击闪白 (Flash):** 敌人受击时，Sprite 会瞬间变全白 (Material Property Block)，叠加少量的 Sparks 粒子。这种“微特效”反馈极好且不掉帧。

### 💀 Dead Cells (死亡细胞)
*   **像素粒子:** 既然是像素风游戏，粒子也是一个个大的正方形像素。千万别在像素游戏里放高清辉光烟雾，会极度违和。
*   **顿帧 (Hit Stop):** 粒子爆发的一瞬间，游戏逻辑暂停 0.1秒。这让特效看起来更有“力度”。

---

## 🔗 4. 参考资料 (References)

*   📺 **Mirza (YouTube):** Unity VFX 教程大神，尤其擅长 Shader + Particle 结合。
*   📺 **Gabriel Aguiar Prod:** 很多具体的技能特效教程（火球、刀光）。
*   🌐 **RealtimeVFX:** 全球特效美术师论坛，寻找灵感的宝库。
*   📄 **[VFX Optimization Guide](../VFX_Optimization_Guide.md):** 本项目的特效性能红线（必读）。
