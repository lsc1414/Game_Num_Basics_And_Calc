---
sidebarTitle: "Linear 与 Gamma 渲染空间深度解析"
title: "🎨 Linear 与 Gamma 渲染空间深度解析"
---



# 🎨 Linear 与 Gamma 渲染空间深度解析

## 📚 1. 理论基础 (Theoretical Basis)

### 1.1 核心定义

**Gamma 空间**与**Linear 空间**的区别在于计算机如何存储颜色以及如何进行光照计算。

- **Linear Space (线性空间)**: 物理世界是线性的。如果光的强度增加一倍，光子的数量也增加一倍 ($1 + 1 = 2$)。在渲染中，这是光照计算必须发生的空间，以保证物理准确性。
- **Gamma Space (伽马空间)**: 传统的显示器（CRT 时代遗留）并非线性输出亮度，而是遵循指数曲线（通常 $\gamma \approx 2.2$）。为了适应这种非线性并在 8 位图像中保存更多暗部细节，我们在存储图片时会进行**Gamma Encoding**（提亮）。

### 1.2 数学模型

人眼对暗部变化比亮部更敏感。

- **Gamma Encoding (编码)**: 在保存图片时，将线性颜色 $C_{linear}$ 转换为 $C_{sRGB}$：

  $$C_{sRGB} = C_{linear}^{(1/2.2)}$$

    (约为 0.45 次方，图像变亮)

- **Gamma Decoding (解码/显示)**: 显示器将信号转换为物理光线：

  $$L_{display} = C_{sRGB}^{2.2}$$

    (约为 2.2 次方，压暗，最终还原为线性物理亮度)

!!! warning "错误的计算"
    如果在 Gamma 空间直接相加两个光源 ($0.5 + 0.5 \neq 1.0$)，会导致高光过曝、混合处出现由于非线性导致的黑边（Dark Fringing）以及 PBR 材质表现错误。

### 1.3 设计心理学

- **真实感 (Realism)**: PBR (Physically Based Rendering) 极其依赖 Linear Space。因为能量守恒公式只有在线性空间下才成立。
- **美术直觉**: 在 Gamma 空间工作的美术人员习惯了"手动补光"来对抗错误的暗部堆积，切换到 Linear 后，场景通常会变亮并显得更自然，需要重新调整打光习惯。

---

## 🛠️ 2. 实践应用 (Practical Implementation)

### 2.1 Vampirefall 适配指南

对于我们的项目（塔防 + 3D 视角），切换到 Linear 空间对视觉提升巨大，尤其是特效叠加和光照衰减。

#### 📋 切换清单 (Checklist)

1.  **Unity 设置**:
    - `Project Settings` -> `Player` -> `Other Settings` -> `Color Space`: 切换为 **Linear**。
    - **注意**: 这要求最低图形 API 为 OpenGLES 3.0 (Android) / Metal (iOS)。

2.  **纹理设置 (Texture Importer)**:
    这是最容易出错的地方。Unity 需要知道哪些图是"颜色"，哪些是"数据"。

    | 纹理类型                            | sRGB (Color Texture) | 说明                                                          |
    | :---------------------------------- | :------------------- | :------------------------------------------------------------ |
    | **Albedo / Diffuse / BaseColor**    | **✅ 勾选**          | 这类贴图是在 sRGB 空间绘制的，Unity 采样时需自动转为 Linear。 |
    | **UI Sprites**                      | **✅ 勾选**          | 同上。                                                        |
    | **Normal Map**                      | **❌ 不勾选**        | 法线是方向数据，必须保持线性值。                              |
    | **Mask Map / Metallic / Roughness** | **❌ 不勾选**        | 非颜色数据参与计算，不可进行 Gamma 转换。                     |
    | **Noise / LUT**                     | **❌ 不勾选**        | 数学查找表必须精确。                                          |

3.  **UI 系统 (Canvas)**:
    - 旧版 Unity UI 在 Linear 空间下可能显得"发白"或"混合不正确"。
    - 确保 UI Shader 支持 Linear (通常 Unity 内置 UI Shader 已处理)。
    - 对于半透明 UI，Blend Mode 的数学计算在线性空间下结果不同，可能需要美术调整透明度。

### 2.2 Shader 修正

如果你在 Shader 中手动处理了颜色，需要注意：

```hlsl
// ❌ 错误做法 (Legacy Gamma)
// 假设 tex2D 读出来的是 Linear (如果 sRGB 没勾选)，又手动 pow 了一次
fixed4 col = tex2D(_MainTex, i.uv);
col.rgb = pow(col.rgb, 2.2); // 不要这样做！让硬件采样器做

// ✅ 正确做法 (Linear Workflow)
// 确保贴图勾选 sRGB，采样器会自动返回 Linear 值
fixed4 col = tex2D(_MainTex, i.uv);
// 直接进行光照计算
fixed3 final = col.rgb * lightColor * NdotL;
```

---

## 🌟 3. 业界优秀案例 (Industry Best Practices)

### 3.1 案例分析

- **《Genshin Impact (原神)》**:
    - 全流程 Linear Space。
    - **特点**: 卡通渲染 (NPR) 同样受益于 Linear Space，主要体现在阴影梯度的柔和过渡上。Gamma 空间下的阴影过渡通常非常生硬直接。

- **《Kingdom Rush Vengeance》 (参考)**:
    - 虽然是 2D 风格，但现代 2D 引擎常开启 Linear 空间以获得更好的粒子混合效果（Additive Blending 在 Linear 下更柔和，不易过曝）。

### 3.2 优缺点对比

| 维度                | Linear Space                                     | Gamma Space                      |
| :------------------ | :----------------------------------------------- | :------------------------------- |
| **PBR 表现**        | ✅ 物理准确                                      | ❌ 能量不守恒，金属看起来像塑料  |
| **光照衰减**        | ✅ $1/d^2$ 自然衰减                              | ❌ 衰减过快，暗部死黑            |
| **混合 (Blending)** | ✅ 线性叠加，自然                                | ❌ 容易过曝，产生黑边            |
| **移动端性能**      | ⚠️ 在极老旧机型有轻微 sRGB 读写消耗 (通常可忽略) | ✅ 最廉价，兼容 OpenGLES 2.0     |
| **工作流复杂度**    | ⚠️ 需严格管理纹理 sRGB 选项                      | ✅ 简单粗暴，所见即所得 (但错误) |

### 3.3 总结与建议

对于 **Vampirefall**：

1.  **必须使用 Linear 空间**。我们的 3D 塔防和 Roguelike 技能特效涉及大量透明混合，Linear 空间能解决"光效光污染"严重的问题。
2.  **Lint 工具**: 编写一个简单的编辑器脚本，扫描所有名为 `*Normal*`, `*Mask*`, `*Data*` 的纹理，确保它们的 sRGB 选项被**关闭**。

### 3.4 常见疑问 (FAQ)

!!! question "Q: Gamma 工作流下 (Color Space = Gamma)，贴图还需要勾选 sRGB 吗？"

    **A: 勾不勾选在视觉上通常没有区别，但建议保持勾选。**
    - **机制**: 在 Gamma Space 模式下，Unity 的采样器不仅不会进行 Linear 转换，通常也会直接忽略贴图的 sRGB 标记。Shader 拿到的永远是贴图里的**原始像素值** (Raw Value)。
    - **为什么建议勾选**:
        1.  **语义正确**: 标记这是"颜色"而不是"数据"。
        2.  **无痛切换**: 如果未来项目决定升级到 Linear Space，你不需要重新去勾选几千张贴图。
        3.  **UI 兼容**: 部分旧版 GUI 系统依赖此标记识别 Alpha 通道行为。

!!! question "Q: 从 Gamma 切换到 Linear，需要重新制作/导出贴图资源吗？"

    **A: 不需要重新导出源文件 (PNG/TGA/PSD)，但可能需要重新烘焙光照。**

- **贴图资源**: 是兼容的。只要你的纹理 Import Setting 设置正确（Albedo 勾选 sRGB，Normal 不勾选），Unity 会根据当前的 Color Space 自动决定如何采样。Gamma 模式下读取原始值，Linear 模式下硬件去除 Gamma 曲线。**同一份资源**可以用于两种空间。
- **需要注意的副作用**:
    1.  **光照贴图 (Lightmaps)**: 必须重新烘焙。旧的光照贴图是基于错误的衰减计算的。
    2.  **材质效果**: 画面会突然变亮或变暗（通常暗部会变亮，高光会更柔和）。美术需要调整材质球参数（Intensity, Smoothness）来适配新的光照反应。
    3.  **自定义 Shader**: 如果你的 Shader 里为了在 Gamma 空间下好看写死了一些 Magic Number 或者 `pow(x, 2.2)`，切换后需要把这些 Hack 去掉。

!!! question "Q: 现代 Unity URP 项目是不是无脑选 Linear 就对了？"

    **A: 99% 的情况下，是的。**

- **URP 的设计初衷**: Universal Render Pipeline (URP) 的核心光照模型和后处理栈 (Post-processing Stack) 都是基于 **Linear Space** 设计的。如果你强制用 Gamma，你会发现 HDR、Bloom、Tonemapping (色调映射) 的效果都会变得很奇怪。
- **PBR 材质**: 现在 Asset Store 买的素材基本都是 PBR 标准。PBR 的能量守恒公式只有在 Linear 空间下才是数学正确的。
- **唯一例外**: 极少数纯 2D 像素风游戏 (Pixel Art)，且完全不使用光照和半透明特效，美术希望"屏幕上显示的颜色 = 我在 PS 里画的颜色 (RGB 值完全一致)"，这时候有人会选择 Gamma 以获得绝对的色彩控制权。但即使是 2D 游戏，为了特效好看，现代项目也倾向于用 Linear 配合 Tonemapping。

---

## 🔗 4. 参考资料 (References)

- 📄 [Unity Documentation: Linear rendering overview](https://docs.unity3d.com/Manual/LinearLighting.html)
- 📄 [NVIDIA: GPU Gems 3 - The Importance of Being Linear](https://developer.nvidia.com/gpugems/gpugems3/part-iv-image-effects/chapter-24-importance-being-linear)
- 📺 [Filmic Worlds: Linear Space Lighting (John Hable)](http://filmicworlds.com/blog/linear-space-lighting-i-e2-80-94-gamma-vs-linear/)
