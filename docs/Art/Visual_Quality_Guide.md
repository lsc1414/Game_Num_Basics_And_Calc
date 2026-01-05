# 🎥 Unity URP 画面表现与镜头设计指南 (Visual Quality Guide)

本文档基于 Unity URP (Universal Render Pipeline) 编写，旨在指导如何构建**手游性能预算下**的高品质画面。

---

## 1. 摄像机美学 (Camera Aesthetics)

摄像机不仅仅是玩家的“眼睛”，它是导演。

### 1.1 黄金机位参数 (The Isometric Gold Standard)
对于俯视角 ARPG / 塔防游戏，机位决定了纵深感。

*   **投影模式 (Projection):** 
    *   推荐使用 **Perspective (透视)** 而非 Orthographic (正交)。透视能带来更好的纵深感和视差效果，让场景更立体。
*   **FOV (Field of View):** 
    *   推荐值: **40 - 50** (Vertical)。
    *   *原理:* 过大的 FOV (60+) 会导致透视畸变严重，边缘拉伸；过小的 FOV (<30) 会让画面扁平化，丢失距离感。
*   **角度 (Pitch/Angle):**
    *   **55° - 60°** (俯仰角)。这个角度能兼顾角色的头身比展示（不至于全是头顶）和战场视野覆盖。

### 1.2 镜头运动 (Cinemachine Magic)
**拒绝硬切 (Hard Cut) 和死板的跟随。** 必须使用 **Cinemachine** 插件。

*   **阻尼 (Damping):**
    *   设置 `Body: Transposer` 的 `X/Y/Z Damping` 为 **0.5 ~ 1.0**。
    *   *效果:* 角色移动时，镜头会平滑地“飘”过去，而不是像钉子一样死死钉在角色头上。这能极大减少画面抖动带来的晕眩感。
*   **打击感震动 (Impulse Shake):**
    *   使用 `Cinemachine Impulse Source`。
    *   **微震:** 普攻命中。 `Amplitude: 0.1`, `Duration: 0.1s`.
    *   **重震:** 暴击/被击。 `Amplitude: 0.5`, `Duration: 0.2s`.
    *   *注意:* 震动要短促有力，不要像果冻一样晃个不停。
*   **目标编组 (Target Group):**
    *   当 Boss 出现时，动态切换到 `Target Group` 模式，将镜头焦点同时锁定在“玩家”和“Boss”之间，自动拉远距离以囊括两者。

---

## 2. 手游后处理策略 (URP Post-Processing)

后处理是提升画质最快的方法，也是手机发热的元凶。**Less is More.**

### ✅ 必开项 (High Value, Low Cost)
1.  **Tonemapping (色调映射):** **必须开启!**
    *   Mode: **ACES**。
    *   *作用:* 将 HDR 的高动态范围颜色正确映射到屏幕上。没有它，你的亮部只会是一片惨白，开启后亮部会有丰富的色彩层次（如火焰中心的橙黄过渡）。
2.  **Bloom (泛光):** 
    *   *设置:* Threshold (0.9), Intensity (0.2 - 0.5), Scatter (0.4)。
    *   *性能:* 开启 `High Quality Filtering` 会很耗，手游建议关掉高品质过滤，适当调低 `Downsample`。
    *   *作用:* 让“发光”的东西真正发光（如技能特效、霓虹灯）。避免全局泛光，只让高亮部分泛光。
3.  **Vignette (暗角):**
    *   *设置:* Intensity (0.25), Smoothness (0.4)。
    *   *作用:* 压暗四角，引导玩家视线集中在屏幕中心，极其廉价的“电影感”来源。

### ⚠️ 慎用项 (High Cost)
1.  **Depth of Field (景深):**
    *   **性能杀手。** 尤其是在 Bokeh (散景) 模式下。
    *   *建议:* 仅在 UI 对话界面、特写镜头或 Build Mode（静止时）开启。战斗中关闭。
2.  **Color Grading (调色):**
    *   使用 `Lift, Gamma, Gain` 微调环境氛围。
    *   *性能:* 只要开了 Tonemapping，Color Grading 几乎是免费的（它们在同一个 Pass 处理）。但不要调得太重口味。

### ❌ 禁区 (Avoid on Mobile)
1.  **Motion Blur (动态模糊):** 手游上采样率不足会导致画面脏糊，且消耗巨大。
2.  **Ambient Occlusion (SSAO):** 屏幕空间环境光遮蔽在手机上极耗 GPU。
    *   *替代:* 使用烘焙的 Lightmap AO 或者材质自带的 AO 贴图。

---

## 3. 画质提升技巧 (Lighting & Details)

### 3.1 线性空间 (Linear Color Space)
*   **Project Settings -> Player -> Color Space:** 必须设为 **Linear**。
*   Gamma 空间下的光照混合是错误的，会导致亮部过曝、暗部死黑。Linear 空间才是物理正确的光照计算基础。

### 3.2 阴影策略 (Shadows)
*   **主光源 (Main Light):** 开启软阴影 (Soft Shadows)，Resolution 设为 Medium (1024)。
*   **点光源 (Add'l Lights):** **关闭阴影 (No Shadows)**。
    *   手游承受不起多个光源投射实时阴影。
*   **烘焙 (Baking):** 
    *   场景静态物体（墙壁、地板）必须烘焙 Lightmap。
    *   动态物体（角色）使用 Light Probes（光照探针）来接受烘焙光照的影响。**Light Probes 是让角色融入场景的关键。**

### 3.3 渲染比例 (Render Scale)
*   在 URP Asset 设置中。
*   **高端机:** 1.0 (原生分辨率) + MSAA 4x。
*   **中低端机:** 0.7 - 0.8 + MSAA 2x。
    *   将渲染分辨率降低到 70%，再用 UI 覆盖上去，肉眼很难察觉，但 FPS 能大幅提升。

---

## 4. 总结：高画质公式

**高画质 = 线性空间 + ACES Tonemapping + 恰当的 Bloom + 柔和的阴影 + 动态阻尼镜头**

不要盲目堆特效。好的画面是**干净、通透、重点突出**的。
