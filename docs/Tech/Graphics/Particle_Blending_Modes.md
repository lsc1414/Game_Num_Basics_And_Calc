---
sidebarTitle: "粒子特效材质透明度混合模式深度研究"
---

# 🧙‍♂️ 粒子特效材质透明度混合模式

## 📚 1. 理论基础 (Theoretical Basis)

### 核心定义

透明度混合（Alpha Blending）是计算机图形学中将前景颜色（Source）与背景颜色（Destination）结合以产生透明效果的过程。在渲染管线中，这一步发生在片元着色器（Fragment Shader）之后，写入帧缓冲区（Frame Buffer）之前。

### 数学模型

混合的核心公式如下：

$$C_{final} = C_{src} \times F_{src} + C_{dst} \times F_{dst}$$

其中：

- $C_{final}$ : 最终写入颜色缓冲区的颜色。
- $C_{src}$ : 当前片元着色器输出的颜色（Source Color）。
- $C_{dst}$ : 帧缓冲区中已经存在的颜色（Destination Color）。
- $F_{src}$ : 源混合因子（Source Blend Factor）。
- $F_{dst}$ : 目标混合因子（Destination Blend Factor）。

此外，混合操作符（Blend Op）通常默认为 **加法** ($+$)，但在某些特殊效果中可能会使用减法（RevSub）或最小值（Min）、最大值（Max）。

### 设计心理学

- **视觉层级**: 透明度用于区分主要信息（实心）与次要信息（半透明特效）。
- **能量传递**: "加法混合"（Additive）常用于表现高能量（如火焰、魔法），因为它会使结果更亮，暗示能量的叠加。
- **物理真实**: "Alpha 混合"（Alpha Blend）用于表现物理实体（如烟雾、玻璃），符合光线被遮挡的直觉。

## 🛠️ 2. 实践应用 (Practical Implementation)

### Vampirefall 适配指南

在 Vampirefall (塔防 + Roguelike) 中，屏幕上可能会同时存在大量单位和特效。错误的混合模式会导致严重的 **Overdraw**（过度绘制）或 **视觉混乱**。

### 混合模式速查表 (Unity / ShaderLab)

下表列出了常用的混合模式及其对应的混合因子配置：

| 模式名称                                | 视觉效果               | 混合因子 (Src, Dst)            | 适用场景                            | 备注                                                                  |
| :-------------------------------------- | :--------------------- | :----------------------------- | :---------------------------------- | :-------------------------------------------------------------------- |
| **Alpha Blending**<br>(常规透明)        | 正常的遮挡关系，半透明 | `SrcAlpha`, `OneMinusSrcAlpha` | 🌫️ 烟雾、灰尘、幽灵、玻璃           | 最符合直觉，但如果是大量重叠会导致变暗或排序问题。                    |
| **Additive**<br>(线性减淡 / 叠加)       | 越叠越亮，无黑色       | `SrcAlpha`, `One`              | 🔥 火焰、辉光、电火花、激光         | **最常用**的特效模式。黑色背景会被滤除。不会产生深度排序错误。        |
| **Soft Additive**<br>(柔和叠加)         | 比 Additive 更柔和     | `OneMinusDstColor`, `One`      | ✨ 柔和的光晕、残影                 | 类似 Photoshop 的"滤色" (Screen) 变种，不会过度曝光。                 |
| **Premultiplied**<br>(预乘 Alpha)       | 兼顾 Alpha 和 Additive | `One`, `OneMinusSrcAlpha`      | 🪄 复杂的魔法弹道、带发光边缘的实体 | 需要贴图制作时预先将 RGB 乘以 Alpha。可以同材质实现发光与半透明混合。 |
| **Multiplicative**<br>(乘法 / 正片叠底) | 变暗                   | `DstColor`, `Zero`             | 🌑 阴影、烧焦痕迹、黑暗魔法         | 使场景变暗。                                                          |

### 🎨 贴图制作指南 (Texture Authoring Guide)

混合模式与贴图的制作方式 **高度相关**。错误的贴图背景或通道设置会导致严重的视觉瑕疵（如黑边、去不掉的底色）。

| 混合模式           | 贴图背景底色           | Alpha 通道要求      | 制作要点 (Photoshop / Substance)                                                                                                                                    |
| :----------------- | :--------------------- | :------------------ | :------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **Alpha Blending** | **透明** (Transparent) | **必须** (Required) | Alpha 通道定义形状和透明度。RGB 通道定义颜色。<br>❌ 不要把背景涂黑，必须是透明的通过 Alpha 切割。                                                                  |
| **Additive**       | **纯黑** (Black)       | 可选 (Optional)     | **黑色 (0,0,0) = 透明**。颜色越亮，叠加效果越强。<br>✅ 制作时可以直接在黑色背景上通过明度控制透明度，不需要严格的 Alpha 通道。                                     |
| **Multiply**       | **纯白** (White)       | 不常用              | **白色 (1,1,1) = 透明**。颜色越深，变暗效果越强。<br>✅ 制作类似"AO 阴影"的贴图，背景必须保留纯白。                                                                 |
| **Premultiplied**  | **纯黑** (Black)       | **必须** (Required) | **关键点**: 导出时 RGB 必须乘以 Alpha。<br>例如 50% 透明度的红色，RGB 值应为 `(128, 0, 0)` 而不是 `(255, 0, 0)`。<br>✅ 解决 Alpha Blend 在线性空间下的"黑边"问题。 |

!!! tip "美术小贴士: Additive 为什么好用？"
    对于特效师来说，**Additive** 是最省事的模式。因为你不需要抠图（Alpha Channel）。只要把背景涂黑及任何你不想要的地方涂黑，它就自然透明了。这使得制作光效、辉光非常容易。

### 🔮 深度解析：什么是 Premultiplied Alpha？

这通常是美术和程序最容易产生误解的地方。简单来说，区别在于 **"透明度是在存贴图时乘，还是在渲染时乘？"**

#### 1. 直观理解 (Intuition)

- **Straight Alpha (常规)**: 颜色是颜色，透明是透明。
    - 像素: `(R=1, G=1, B=1, A=0.5)` $\rightarrow$ 代表 "50% 透明度的纯白色"。
    - 渲染时: GPU 计算 `RGB * A` $\rightarrow$ `(0.5, 0.5, 0.5)`。
- **Premultiplied Alpha (预乘)**: 颜色里已经包含了透明度信息。
    - 像素: `(R=0.5, G=0.5, B=0.5, A=0.5)` $\rightarrow$ 代表 "50% 透明度的纯白色"。
    - 渲染时: GPU 不需要再乘 Alpha，直接用。

#### 2. 为什么要这么麻烦？(Why use it?)

**原因 A: 解决"黑边"问题 (The Black Halo Artifact)**

在纹理采样（Bilinear Filtering）时，如果一个白色像素(1,1,1,1)旁边是一个透明像素(0,0,0,0)，线性插值的中点会变成 (0.5, 0.5, 0.5, 0.5)。

- **常规模式其实是错的**: GPU 拿到中点后，再乘 Alpha: `0.5 * 0.5 = 0.25`。你会得到一个 **0.25** 亮度的灰色，而不是预期的 0.5 亮度。这就导致物体边缘出现一圈黑晕。
- **预乘模式是对的**: 纹理存的就是 (0.5, 0.5, 0.5, 0.5)。GPU 直接用混合模式 `One`，取出 RGB (0.5)，结果正确。

**原因 B: 一个材质，两种效果 (Hybrid Mode)**

Premultiplied 最强大的地方在于它可以同时表现 **Additive** 和 **Alpha Blend**。

- 混合公式: `Src + Dst * (1 - SrcAlpha)`
- **如果你想要各种发光 (Additive)**: 把贴图 Alpha 设为 0，RGB 设为亮色。公式变成 `Src + Dst`。
- **如果你想要半透明 (Alpha Blend)**: 把贴图 RGB 和 Alpha 正常设置。
- **结果**: 你可以在同一个粒子特效里，中心是高亮的火焰 (Additive)，边缘是黑烟 (Alpha Blend)。这是常规模式做不到的。

### Unity Shader 实现示例

```shader
Shader "Vampirefall/Particles/Standard_Additive"
{
    Properties
    {
        _MainTex ("Texture", 2D) = "white" {}
        _TintColor ("Tint Color", Color) = (1,1,1,1)
    }
    SubShader
    {
        Tags { "Queue"="Transparent" "IgnoreProjector"="True" "RenderType"="Transparent" }

        // 关键部分：关闭深度写入，设置混合模式
        ZWrite Off
        Cull Off
        Blend SrcAlpha One  // Additive Blend

        Pass
        {
            CGPROGRAM
            // ... 顶点和片元着色器代码 ...
            fixed4 frag (v2f i) : SV_Target
            {
                fixed4 col = tex2D(_MainTex, i.uv);
                return col * _TintColor * i.color; // 顶点颜色用于粒子系统控制
            }
            ENDCG
        }
    }
}
```

### 什么时候用什么？(Decision Matrix)

1.  **如果是 "光" (本身发光)** $\rightarrow$ 使用 **Additive** (`SrcAlpha`, `One`)
    - _例子_: 法师的火球、塔的激光、爆炸的核心。
2.  **如果是 "物质" (反射光/遮挡背景)** $\rightarrow$ 使用 **Alpha Blending** (`SrcAlpha`, `OneMinusSrcAlpha`)
    - _例子_: 爆炸后的黑烟、扬起的尘土、怪物的半透明皮肤。
3.  **如果是 "暗物质" (吸收光)** $\rightarrow$ 使用 **Multiply** (`DstColor`, `Zero`)
    - _例子_: 地面上的焦痕、诅咒法阵的底纹。
4.  **如果既要有实体感又要发光** $\rightarrow$ 使用 **Premultiplied** (`One`, `OneMinusSrcAlpha`)
    - _例子_: 发光的魔法水晶（边缘半透明，中心亮）、UI 上的特效流光。

!!! warning "性能警示 (Performance Warning)"
    **Additive** 和 **Alpha Blending** 都会产生 Overdraw。在移动端（Mobile），如果粒子面积过大且层叠过多，会严重消耗 GPU 填充率（Fillrate）。
对于大面积的特效（如全屏迷雾），尽量减少粒子数量，或使用网格发射器（Mesh Emitter）代替默认的广告牌（Billboard）以减少透明像素面积。

## 🌟 3. 业界优秀案例 (Industry Best Practices)

### 案例 1: 《Hades》 (Supergiant Games)

- **特点**: 极度绚丽的色彩，大量的粒子特效。
- **分析**:
    - 攻击特效几乎全部使用 **Additive** 混合，保证在暗色调的地下城背景中极为醒目。
    - 环境特效（如雾气）使用 **Alpha Blending**，并严格控制粒子密度。
    - 使用了 **Premultiplied Alpha** 来处理手绘风格的特效贴图，避免了传统 Alpha Blending 常见的"黑边"问题。

### 案例 2: 《Diablo III / IV》 (Blizzard)

- **特点**: 清晰的战斗可读性 (Readability)。
- **分析**:
    - **优先级管理**: 技能特效的亮度与其伤害/威胁度成正比。普通攻击比较暗，大招极其明亮（Additive）。
    - **软粒子 (Soft Particles)**: 使用深度纹理（Depth Texture）计算淡入淡出，避免粒子与地面相交时产生生硬的切边线。

## 🔗 4. 参考资料 (References)

- 📄 [Unity Documentation: ShaderLab Blend](https://docs.unity3d.com/Manual/SL-Blend.html)
- 🌐 [OpenGL Blending Specification](https://www.khronos.org/opengl/wiki/Blending)
- 📺 [GDC: Visual Effects in Diablo III](https://www.youtube.com/watch?v=YRLA3aFVPE0)
