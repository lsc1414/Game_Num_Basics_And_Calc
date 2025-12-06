# 🌤️ Bloom 后处理深度研究 (Bloom Post-Processing)

> **"没有 Bloom，霓虹灯只是一块带颜色的板子。"**
>
> 很多开发者认为“发光”就是把颜色调亮，其实发光是由 **Shader (自发光)** 和 **Post-Processing (Bloom)** 共同完成的物理欺骗。

---

## 📚 1. 理论基础 (Theoretical Basis)

### 💡 什么是 Bloom (泛光)？
在真实世界中，当极亮的光源进入摄像机（或人眼）时，光线会在晶状体或镜头内发生**散射 (Scattering)**，导致光源周围出现朦胧的光晕。
*   **渲染原理:** 
    1.  **提取 (Pre-filter):** 找出屏幕上所有亮度超过 `Threshold` (阈值) 的像素。
    2.  **降采样 (Downsample):** 把这些亮像素缩小（变糊）。
    3.  **高斯模糊 (Blur):** 横向纵向多次模糊。
    4.  **叠加 (Upsample + Combine):** 把糊掉的亮光叠加回原图。

### 🌈 HDR 与发光的本质
**用户提问：Bloom 都是靠 Shader 中的发光属性来实现的吗？**
*   **答案：是，但也不全是。**
    *   **源头 (Source):** 必须由 Shader 提供**超过 1.0 亮度的颜色** (HDR Color)。
    *   **筛选 (Filter):** Bloom 必须设置一个 `Threshold`（比如 1.2）。
    *   **结果:** 只有 Shader 中亮度 > 1.2 的部分，才会被 Bloom 系统捕获并产生光晕。
    *   *如果 Shader 亮度只有 0.8（不发光），哪怕你是纯白色，Bloom 也不会理你。*

### 🎞️ 为什么需要 Tone Mapping (色调映射)
如果开启了 HDR，亮度可能高达 10.0。但显示器（大部分）只能显示 0.0 ~ 1.0 (LDR)。
*   **直接裁切 (Clamping):** 大于 1.0 的全变白色 (1.0)。会导致亮部细节全丢，变成死白。
*   **Tone Mapping (ACES):** 把 (0.0 ~ 无限大) 映射回 (0.0 ~ 1.0) 的 S 曲线。
    *   **作用:** 保留亮部细节（高光不惨白），同时增强对比度，让画面更有“电影感”。
    *   **流程:** `Shader(HDR) -> Bloom(泛光) -> ToneMapping(压回LDR) -> 显示器`。

---

## 🛠️ 2. 实践应用 (Practical Implementation)

### 🎛️ 核心参数详解 (Settings Logic)
在 Unity Post-Processing Volume 中，Bloom 的参数设置逻辑如下：

#### 1. Threshold (阈值) - "门卫"
*   **定义:** 只有亮度超过这个值的像素才会发光。
*   **设置建议:** **0.8 ~ 1.2**。
    *   如果设为 0：全屏幕都会发光（梦幻滤镜）。
    *   如果设为 1.5：只有极亮的光源（太阳、激光）会发光。
*   **Vampirefall 策略:** 设为 **1.1**。让普通的白色 UI (亮度 1.0) 保持清晰不发光，只让特效发光。

#### 2. Intensity (强度) - "增益"
*   **定义:** 光晕的亮度倍率。
*   **设置建议:** **0.5 ~ 2.0**。
*   **误区:** 不要把 Intensity 调得巨高来强行发光，这会导致画面过曝（全白）。应该去调 Shader 的 Emission Intensity。

#### 3. Scatter (散射/扩散) - "范围"
*   **定义:** 光晕扩散的半径。
*   **设置建议:** **0.3 ~ 0.5**。
    *   过大：画面会变得很“脏”，像没擦干净镜头。
    *   过小：光晕太聚拢，像贴图错误。

#### 4. Tint (染色)
*   **定义:** 强行改变光晕颜色。
*   **设置建议:** **白色 (不染色)**。除非你做赛博朋克风格（统一染成紫色）。

### 🎨 Shader 设置工作流
如何让一个物体发光？

1.  **Shader:** 使用 `URP/Lit` 或 `Particles/Standard`。
2.  **Emission:** 勾选 Emission。
3.  **HDR Color:** 点击颜色，你需要关注 **Intensity** (下方的小滑块) 或者直接输入 RGB 值。
    *   **R: 191, G: 0, B: 0** -> 暗红色，不发光。
    *   **R: 191, G: 0, B: 0, Intensity: 2.0** (即 R: 382) -> **亮红色，带红色光晕**。
    *   **R: 191, G: 0, B: 0, Intensity: 10.0** -> **中心变白（过曝），周围是大红光晕**。
    *   *物理现象:* 亮度极高时，核心会因为显示器最大只能显示 255 而变成白色 (Tone Mapping)，但 Bloom 依然能通过模糊保留边缘的颜色。

### 📱 移动端性能优化 (Mobile Optimization)
Bloom 是移动端最昂贵的后处理之一。
1.  **High Quality Filtering:** **关掉 (Uncheck)**。用双线性过滤代替双三次过滤，手机看不出区别。
2.  **Downsample:** 无论如何 Bloom 都是在低分辨率下计算的，不用太担心分辨率。
3.  **Fast Mode:** 如果是 URP，确保开启 Fast Mode (如果有)。
4.  **Clamp:** 设置为 **5.0 ~ 10.0**。防止某个像素亮度异常（比如 10000），导致整个屏幕闪白 (Fireflies artifact)。

---

## 🌟 3. 业界优秀案例 (Industry Best Practices)

### 🌃 Cyberpunk 2077 (赛博朋克 2077)
*   **色散 (Chromatic Aberration) + Bloom:** 让光晕边缘带有红蓝色的色散偏移，模拟义眼故障或廉价镜头的感觉。
*   **Dirt Texture (镜头脏迹):** 给 Bloom 加一张贴图。当你看向强光时，光晕会照亮屏幕上的灰尘。**这极大地增加了真实感。**

### 🗡️ Hollow Knight (空洞骑士)
*   **局部 Bloom:** 并非全屏 Bloom。很多发光效果（如路灯）其实是**一张自带模糊的半透明贴图 (Sprite)** 贴在上面。
*   **优点:** 0 性能消耗 (Mobile Friendly)。
*   **缺点:** 或者是作为 Bloom 的补充。在低端机上这也是一种替代方案。

---

## 🔗 4. 参考资料 (References)
*   📄 **[VFX Optimization Guide](../VFX/VFX_Optimization_Guide.md):** 特效性能指南。
*   📄 **[Unity Manual - Bloom]:** 官方文档关于 URP Bloom 的说明。
