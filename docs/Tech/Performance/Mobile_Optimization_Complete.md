---
sidebarTitle: "移动端深度优化指南"
---

# 移动优化综合指南

> 本文档由以下文件合并生成 (2026-02-10)
## 📱 移动端深度优化指南

**文档目标：** 让 Vampirefall 在 iPhone 8 / 小米 6 级别的设备上稳定运行，且**不烫手**。
**核心矛盾：** 塔防的海量单位 vs 手机可怜的散热能力。

---

## 1. 🔥 发热控制：你的游戏为什么烫手？

手机发热主要源于 **GPU 负载持续过高** 和 **CPU 密集运算**。一旦发热，系统强制降频，帧率从 60 瞬间跌到 15。

### 1.1 帧率封顶 (Target Frame Rate)
*   **菜单/UI界面:** 强制锁定 **30 FPS**。没人需要在背包界面看 60 帧的动画。
*   **战斗界面:** 默认 **30 FPS**。提供 "高帧率模式 (60 FPS)" 开关，但默认关闭。
    *   *理由:* 30 FPS 能节省 40% 的电量，大幅延缓发热。

### 1.2 动态分辨率 (Dynamic Resolution)
*   **原理:** 当检测到 GPU 压力大时，自动降低渲染分辨率，UI 保持高清。
*   **Unity设置:** `URP Asset -> Render Scale`.
*   **自适应脚本:**
    ```csharp
    void Update() {
        if (Time.deltaTime > 0.04f) { // 低于 25 FPS
            currentScale = Mathf.Max(0.7f, currentScale - 0.05f);
            URPAsset.renderScale = currentScale;
        }
    }
    ```

*   **效果:** 手机用户通常看不出 1080p 和 720p 的区别，但 GPU 负载减半。

### 1.3 物理降频 (Physics Throttling)
*   **默认:** `FixedTimestep = 0.02` (50Hz)。
*   **优化:** 塔防游戏不需要那么精确的碰撞。改为 **0.04 (25Hz)** 甚至 **0.05 (20Hz)**。
*   *收益:* CPU 物理计算开销直接减半。

---

## 2. 📦 包体瘦身 (App Size Optimization)

目标：APK < 100MB (不含资源热更)，首包越小，转化率越高。

### 2.1 纹理压缩 (Texture Compression)
这是包体的大头。

*   **Android:** 必须强制全员 **ASTC 6x6** (甚至 8x8)。
    *   *对比:* ETC2 质量差，ASTC 质量好且压缩率高。所有 2016 年后的安卓机都支持。
*   **iOS:** **ASTC 6x6**。
*   **禁忌:** 严禁使用 RGBA32 或 PNG 原图进包。

### 2.2 代码裁剪 (Code Stripping)
*   **设置:** `Player Settings -> Managed Stripping Level -> High`.
*   **原理:** Unity 会自动剔除那些你没用到的 C# 库代码。
*   **风险:** 反射 (Reflection) 可能会失效。如果用了 JSON 库或 Lua，需要配置 `link.xml` 白名单。

### 2.3 音频设置
*   **BGM:** 强制单声道 (Force to Mono)，码率 96kbps (Vorbis)。手机外放听不出 192kbps 的区别。
*   **SFX:** 短音效码率 70kbps (ADPCM)。

---

## 3. 🧱 内存防爆：2GB 内存生存指南

Android 低端机只有 2GB 内存，除去系统，分给游戏的只有 500MB - 700MB。

### 3.1 纹理流送 (Texture Streaming)
*   **设置:** `Quality -> Texture Streaming`.
*   **原理:** 游戏启动时只加载 1/8 尺寸的模糊贴图。当摄像机靠近物体时，才加载高清贴图。
*   **收益:** 显存占用减少 60%~80%。

### 3.2 杜绝 Resources
*   再次强调，不要把大图放 Resources。
*   **Addressables Duplicate Check:** 使用 Addressables 的分析工具检查有没有资源被打进了多个包里 (Duplicated Assets)。

### 3.3 Shader 变体爆炸
*   **现象:** 内存里加载了几十 MB 的 Shader Lab。
*   **原因:** URP 的 Shader 包含成千上万个变体 (Variants)。
*   **对策:** 使用 `Strip URPS` 脚本，剔除掉你没用到的变体（比如你没用点光源阴影，就剔除 Additional Light Shadow 变体）。

---

## 4. 🤖 专项：海量单位优化 (DOTS / GPU Instancing)

### 4.1 GPU Instancing
*   **材质设置:** 所有怪物的材质球必须勾选 **Enable GPU Instancing**。
*   **条件:** 只有使用**相同 Mesh** 和 **相同 Material** 的物体才能合批。
*   **技巧 (Property Block):** 
    *   如果想改变怪物颜色（如受击变红），**千万不要** `material.color = red` (这会破坏合批)。
    *   **必须使用** `MaterialPropertyBlock`：
    ```csharp
    block.SetColor("_BaseColor", Color.red);
    renderer.SetPropertyBlock(block);
    ```

### 4.2 动画烘焙 (Texture Skinning)
*   **痛点:** 500 个怪物的 `SkinnedMeshRenderer` 计算骨骼极其耗 CPU。
*   **解法:** 使用 **Animation Instancing** (GitHub 有开源库)。
    *   原理: 把动画帧烘焙成一张纹理 (Animation Texture)。
    *   运行: GPU 读取纹理来移动顶点。CPU 开销几乎为 0。

---

## 5. 📝 优化检查清单 (Pre-Launch Checklist)

*   [ ] **Scripting Backend:** 必须是 **IL2CPP** (ARM64)。不要用 Mono。
*   [ ] **Target Architectures:** Android 勾选 ARM64，取消 ARMv7 (Google Play 要求，且 v7 性能差)。
*   [ ] **Multithreaded Rendering:** 必须勾选。
*   [ ] **V-Sync:** 关闭 (在代码里手动限帧，更可控)。
*   [ ] **Accelerometer Frequency:** 如果不玩重力感应，设为 Disabled，省电。




---


## 📱 设备分级与画质自适应

> **"让 iPhone 15 Pro 跑满 120 帧，让红米 Note 7 也能活着玩下去。"**
>
> 移动端碎片化严重，一套画质通吃天下是不可能的。我们需要建立一套严谨的**设备分级系统 (Tier System)**，动态调整渲染负载。

---

## 📚 1. 理论基础 (Theoretical Basis)

### 📊 为什么要分级？

- **硬件鸿沟:** 高端机 GPU 算力是低端机的 50 倍以上。
- **热节流 (Thermal Throttling):** 即使是高端机，全开画质跑 10 分钟也会降频。
- **用户体验:** 低端机用户宁愿看马赛克，也不愿玩 PPT。

### 🏷️ 分级核心指标

我们不能单纯靠识别机型名字（如 "Samsung S21"），因为机型太多了。我们需要看**硬指标**：

1.  **GPU 型号 (SystemInfo.graphicsDeviceName):** 最靠谱的指标。
    - _Android:_ Adreno (高通), Mali (联发科/麒麟/Exynos), PowerVR.
    - _iOS:_ Apple A series GPU.
2.  **显存/内存 (SystemMemorySize):** 决定能不能开高精细度贴图。

3.  **API 支持:** Vulkan vs OpenGL ES 3.x.

---

## 🛠️ 2. 实践应用 (Practical Implementation)

### 📐 1. 分级标准建议 (Grading Criteria)

建议将设备分为 4 档：**High, Medium, Low, Potato (土豆)**。

|          档位                |          标杆机型 (Android)              |          标杆机型 (iOS)          |          GPU 特征 (Regex)          |          目标帧率               |
|          :---------          |          :---------------------          |          :-------------          |          :---------------          |          :------------          |
|          **High**            |          骁龙 8+ Gen 1, 8 Gen 2          |          iPhone 13 Pro+          |          Adreno 7xx, 660+          |          60/120 FPS             |
|          **Medium**          |          骁龙 865, 870                   |          iPhone 11, 12           |          Adreno 640, 650           |          60 FPS                 |
|          **Low**             |          骁龙 660, 845                   |          iPhone 8, X             |          Adreno 61x, 5xx           |          30 FPS                 |
|          **Potato**          |          骁龙 4xx, 老旧麒麟              |          iPhone 6s, 7            |          Adreno 4xx, 3xx           |          30 FPS (稳住)          |

### ⚙️ 2. 画质配置映射 (Quality Mapping)

针对不同档位，我们需要调整以下核心参数：

|          参数 (Feature)                |          High (旗舰)                |          Medium (主流)               |          Low (低配)                  |          Potato (极简)                 |
|          :-------------------          |          :----------------          |          :-----------------          |          :-----------------          |          :-------------------          |
|          **Resolution Scale**          |          1.0 (Native)               |          0.85                        |          0.75                        |          0.6                           |
|          **HDR**                       |          ✅ On                      |          ✅ On                       |          ❌ Off (LDR Bloom)          |          ❌ Off                        |
|          **Shadows**                   |          Hard + Soft (40m)          |          Hard Only (25m)             |          Hard Only (15m)             |          ❌ Off (Blob Shadow)          |
|          **Anti-Aliasing**             |          MSAA 4x                    |          MSAA 2x                     |          FXAA / Off                  |          Off                           |
|          **VFX Max Count**             |          500                        |          200                         |          100                         |          50                            |
|          **LOD Bias**                  |          1.5                        |          1.0                         |          0.7                         |          0.5                           |
|          **Skinning**                  |          GPU (4 weights)            |          GPU (2 weights)             |          CPU (2 weights)             |          CPU (1 weight)                |
|          **Post-Processing**           |          Full Stack                 |          Bloom + ColorGrade          |          ColorGrade Only             |          Off                           |

### 🖥️ 3. 代码实现逻辑 (C# Detection)

不要依赖云端数据库，直接在本地解析 GPU 字符串。

```csharp
public enum DeviceTier { Potato, Low, Medium, High }

public static class DeviceGrader
{
    public static DeviceTier GetTier()
    {
#if UNITY_IOS
        // iOS 比较简单，直接通过 SystemInfo.deviceModel 判断代数
        // iPhone14,x 是 iPhone 12 系列
        string model = SystemInfo.deviceModel;
        if (model.Contains("iPhone14") || model.Contains("iPad13")) return DeviceTier.High;
        if (model.Contains("iPhone11") || model.Contains("iPhone12")) return DeviceTier.Medium;
        return DeviceTier.Low;
#elif UNITY_ANDROID
        string gpu = SystemInfo.graphicsDeviceName; // e.g., "Adreno (TM) 650"

        if (gpu.Contains("Adreno"))
        {
            int series = ExtractNumber(gpu); // 解析出 650, 512 等数字
            if (series >= 730) return DeviceTier.High;
            if (series >= 640) return DeviceTier.Medium; // 骁龙855
            if (series >= 610) return DeviceTier.Low;
            return DeviceTier.Potato;
        }
        else if (gpu.Contains("Mali"))
        {
            // Mali 命名比较乱 (G71, G72, G76, G77...)
            // 通常 G7x MPx, 数字越大越好
            if (gpu.Contains("G710") || gpu.Contains("G78")) return DeviceTier.High;
            if (gpu.Contains("G77") || gpu.Contains("G76")) return DeviceTier.Medium;
            return DeviceTier.Low;
        }

        return DeviceTier.Low; // 无法识别的默认为低
#else
        return DeviceTier.High; // PC 默认高
#endif
    }
}
```

### 📉 4. 动态降级 (Auto-Scalability)

除了进游戏时定死画质，还应该支持**动态降级**。

- **监控:** 每 30 秒检测一次平均 FPS。
- **逻辑:** 如果最近 30 秒 平均帧率 < 25 (目标 30)，则强制降低一级 Resolution Scale 或关闭阴影。
- **恢复:** **永远不要自动升级画质**。如果用户卡了，降级了，后面流畅了也不要升回去，防止反复横跳。

---

## 🌟 3. 业界优秀案例 (Industry Best Practices)

### ⚔️ 原神 (Genshin Impact)

- **极致细分:** 它的图像设置极其详细，针对“渲染精度”和“特效质量”分得很开。
- **过热保护:** 检测到手机温度过高（通过操作系统 API）时，会强制锁定 30 帧 + 甚至降低亮度，而不是让手机关机。

### 🔫 PUBG Mobile

- **帧率优先:** 提供了“流畅+极限帧率(60/90)”的选项。对于竞技游戏，降低画质（Low Tier 设置）换取高帧率（High Tier 帧率策略）是常规操作。
- **LOD 策略:** 远处的草丛在低画质下直接不显示，但这涉及到**竞技公平性**（低画质透视挂）。Vampirefall 是 PVE，不需要担心这个，低画质应该尽可能剔除草丛。

---

## 🔗 4. 参考资料 (References)

- 📄 **[HDR 技术](../../Art/Tech_Art/HDR_DeepDive.md):** 哪些档位该开 HDR。
- 📄 **[Unity Manual - Quality Settings]:** Unity 自带的画质分级系统。






