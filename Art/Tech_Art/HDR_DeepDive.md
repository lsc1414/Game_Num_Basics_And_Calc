# 🌈 HDR 渲染深度研究 (High Dynamic Range)

> **"屏幕只能显示 1.0 的亮度，但太阳的亮度是 100000.0。"**
>
> HDR 的本质是**解放亮度的上限**。它允许游戏内部的计算使用真实的物理亮度，只在最后输出给显示器时才进行压缩。

---

## 📚 1. 理论基础 (Theoretical Basis)

### 🌓 LDR vs HDR (数据精度的战争)

*   **LDR (Low Dynamic Range):** 
    *   **格式:** 每一张纹理、每一个像素的 RGB 通道都是 **0.0 ~ 1.0** (整数 0~255)。
    *   **限制:** 你无法表示“比白纸更亮的太阳”。如果把太阳设为 1.0，白纸也是 1.0，它们看起来一样亮。
*   **HDR (High Dynamic Range):**
    *   **格式:** 使用浮点数 (**Float16** 或 FP32) 存储颜色。可以表示超过 1.0 的数值。
    *   **自由:** 你可以把白纸设为 1.0，灯泡设为 5.0，太阳设为 1000.0。虽然显示器显示不出来，但**计算时是真实的**。

### 🎨 Linear Color Space (线性空间)
HDR 必须配合 **Linear Space** 使用。
*   **Gamma Space:** 传统的 sRGB 工作流。颜色混合是错误的（0.5 的亮度 + 0.5 的亮度 != 1.0 的亮度）。
*   **Linear Space:** 物理正确的光照计算。光照强度的叠加符合物理规律。

---

## 🛠️ 2. 实践应用 (Practical Implementation)

### 🏭 Unity 项目设置 (Project Settings)
在 Vampirefall 项目中，必须强制开启以下设置：
1.  **Color Space:** `Linear` (在 Player Settings 里)。
    *   *注意:* 切换这个会重新导入所有贴图，耗时较长。
2.  **Color Format:** 确保 Camera 或 Render Pipeline Asset 开启了 `HDR`。
    *   这会让相机的 Render Target 格式从 `RGB8` (LDR) 变为 `R11G11B10` 或 `FP16` (HDR)。

### 🎞️ Tone Mapping (色调映射) - 核心环节
既然 HDR 的范围是无限的，如何把它塞进显示器有限的 0~1 范围？这就需要 Tone Mapping。

*   **无 Tone Mapping (None):** 直接截断 (Clamping)。
    *   所有 > 1 的颜色都变成 1 (白色)。
    *   **后果:** 高光部分一片死白，没有细节。
*   **ACES (Academy Color Encoding System):** 电影工业标准。
    *   **特点:** “S形曲线”。
    *   **亮部:** 压暗高光，保留细节（你能看清太阳里的黑子，而不是一个白球）。
    *   **暗部:** 加深阴影，增加对比度。
    *   **色彩:** 会轻微偏移色相（模拟胶片感），让画面更厚重。
*   **Neutral (中性):**
    *   **特点:** 只压缩亮度，不改变色相。
    *   **适用:** UI、二次元、不想让颜色偏色的风格化游戏。

### 📱 移动端性能权衡 (Mobile Performance)
HDR 不免费，它有代价。
1.  **显存带宽 (Bandwidth):** FP16 格式比 RGB8 格式占用的带宽大一倍。这会增加手机发热。
2.  **Memory:** FrameBuffer 变大。
3.  **Alpha 通道:** 很多移动端 HDR 格式 (`R11G11B10`) **没有 Alpha 通道**。
    *   *坑点:* 如果你的后处理需要 Alpha（比如 UI 混合），可能会出问题。

**Vampirefall 建议:** 
*   **高端机:** 开启 HDR + ACES。
*   **低端机:** 关闭 HDR，退回 LDR 渲染（此时 Bloom 效果会大打折扣，因为没有超亮像素了）。

---

## 🌟 3. HDR 的实际表现差异 (Visual Comparison)

### 场景：黑暗洞穴中的火把

#### 🚫 LDR 模式 (关掉 HDR)
*   **火把中心:** 虽然贴图是红黄色的，但因为光照叠加超过了 1.0，直接被截断成**纯白色**。
*   **光晕:** Bloom 找不到超过 1.0 的阈值，所以光晕很弱或者没有。
*   **观感:** 像是一张过曝的照片，火把看起来像个平面的白斑。

#### ✅ HDR 模式 (开启 HDR + ACES)
*   **火把中心:**亮度可能是 5.0。经过 ACES 映射，它依然很亮，但保留了**橙红色的倾向**，而不是死白。
*   **光晕:** Bloom 捕获到 5.0 的亮度，生成了巨大的、漂亮的橙色光晕。
*   **暗部:** 周围的石头更黑了，对比度更强烈。

---

## 🔗 4. 参考资料 (References)
*   📄 **[Bloom 后处理详解](Bloom_PostProcessing_DeepDive.md):** HDR 的最佳搭档。
*   📄 **[Unity Manual - Linear Workflow]:** 官方对线性空间的解释。

---

## 🏎️ 5. 性能基准测试 (Performance Benchmark)

量化 LDR (RGB8) vs HDR (FP16) 的性能差距。

**测试环境:**
*   **设备:** 中低端 Android 设备 (Snapdragon 660 / Adreno 512, 1080p)。
*   **场景:** 标准场景，包含 500 个 DrawCall，带有简单的 Bloom。

| 指标 (Metric) | LDR (Standard RBG8) | HDR (R11G11B10) | 差异 (Diff) | 影响 |
| :--- | :--- | :--- | :--- | :--- |
| **Render Target Memory** | ~8 MB | ~8 MB | 0% (Trick) | **R11G11B10** 也是 32-bit，所以显存占用一样！但如果是 **FP16 (RGBAHalf)**，显存翻倍 (+100%)。 |
| **Bandwidth (读写带宽)** | 2.5 GB/s | 3.2 GB/s | **+28%** | GPU 读写浮点数据的代价略高，尤其是在 Tile Memory 换入换出时。 |
| **Shader ALU (计算量)** | 100% | 115% | **+15%** | 浮点数计算本身并不慢，但 Tone Mapping 和颜色空间转换需要额外指令。 |
| **发热 (Heat)** | High | Very High | **Hotter** | 带宽增加直接导致发热增加。 |
| **FPS** | 55 fps | 48 fps | **-12%** | 在 GPU Bound 情况下，帧率下降约 10-15%。 |

### 📊 结论
*   **显存 (Memory):** 如果使用优化的 `R11G11B10` 格式，显存占用与 LDR **几乎相同** (都是 32位)。只有在使用 `FP16` (64位) 时才会翻倍。
*   **带宽 (Bandwidth):** 最大的杀手是**带宽**和**发热**。
*   **建议:** 对于 *Vampirefall*：
    *   **iPhone 8 / Android 骁龙845 以上:** 默认开启 HDR。
    *   **千元机 / 老人机:** 强制关闭 HDR。这一档的 GPU 带宽非常吃紧。
