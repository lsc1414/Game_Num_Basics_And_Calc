# 📱 设备分级与画质自适应 (Device Grading & Scalability)

> **"让 iPhone 15 Pro 跑满 120帧，让红米 Note 7 也能活着玩下去。"**
>
> 移动端碎片化严重，一套画质通吃天下是不可能的。我们需要建立一套严谨的**设备分级系统 (Tier System)**，动态调整渲染负载。

---

## 📚 1. 理论基础 (Theoretical Basis)

### 📊 为什么要分级？
*   **硬件鸿沟:** 高端机 GPU 算力是低端机的 50 倍以上。
*   **热节流 (Thermal Throttling):** 即使是高端机，全开画质跑 10 分钟也会降频。
*   **用户体验:** 低端机用户宁愿看马赛克，也不愿玩 PPT。

### 🏷️ 分级核心指标
我们不能单纯靠识别机型名字（如 "Samsung S21"），因为机型太多了。我们需要看**硬指标**：
1.  **GPU 型号 (SystemInfo.graphicsDeviceName):** 最靠谱的指标。
    *   *Android:* Adreno (高通), Mali (联发科/麒麟/Exynos), PowerVR.
    *   *iOS:* Apple A series GPU.
2.  **显存/内存 (SystemMemorySize):** 决定能不能开高精细度贴图。
3.  **API 支持:** Vulkan vs OpenGL ES 3.x.

---

## 🛠️ 2. 实践应用 (Practical Implementation)

### 📐 1. 分级标准建议 (Grading Criteria)

建议将设备分为 4 档：**High, Medium, Low, Potato (土豆)**。

| 档位 | 标杆机型 (Android) | 标杆机型 (iOS) | GPU 特征 (Regex) | 目标帧率 |
| :--- | :--- | :--- | :--- | :--- |
| **High** | 骁龙 8+ Gen 1, 8 Gen 2 | iPhone 13 Pro+ | Adreno 7xx, 660+ | 60/120 FPS |
| **Medium** | 骁龙 865, 870 | iPhone 11, 12 | Adreno 640, 650 | 60 FPS |
| **Low** | 骁龙 660, 845 | iPhone 8, X | Adreno 61x, 5xx | 30 FPS |
| **Potato** | 骁龙 4xx, 老旧麒麟 | iPhone 6s, 7 | Adreno 4xx, 3xx | 30 FPS (稳住) |

### ⚙️ 2. 画质配置映射 (Quality Mapping)

针对不同档位，我们需要调整以下核心参数：

| 参数 (Feature) | High (旗舰) | Medium (主流) | Low (低配) | Potato (极简) |
| :--- | :--- | :--- | :--- | :--- |
| **Resolution Scale** | 1.0 (Native) | 0.85 | 0.75 | 0.6 |
| **HDR** | ✅ On | ✅ On | ❌ Off (LDR Bloom) | ❌ Off |
| **Shadows** | Hard + Soft (40m) | Hard Only (25m) | Hard Only (15m) | ❌ Off (Blob Shadow) |
| **Anti-Aliasing** | MSAA 4x | MSAA 2x | FXAA / Off | Off |
| **VFX Max Count** | 500 | 200 | 100 | 50 |
| **LOD Bias** | 1.5 | 1.0 | 0.7 | 0.5 |
| **Skinning** | GPU (4 weights) | GPU (2 weights) | CPU (2 weights) | CPU (1 weight) |
| **Post-Processing** | Full Stack | Bloom + ColorGrade | ColorGrade Only | Off |

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
*   **监控:** 每 30 秒检测一次平均 FPS。
*   **逻辑:** 如果最近 30秒 平均帧率 < 25 (目标 30)，则强制降低一级 Resolution Scale 或关闭阴影。
*   **恢复:** **永远不要自动升级画质**。如果用户卡了，降级了，后面流畅了也不要升回去，防止反复横跳。

---

## 🌟 3. 业界优秀案例 (Industry Best Practices)

### ⚔️ 原神 (Genshin Impact)
*   **极致细分:** 它的图像设置极其详细，针对“渲染精度”和“特效质量”分得很开。
*   **过热保护:** 检测到手机温度过高（通过操作系统 API）时，会强制锁定 30帧 + 甚至降低亮度，而不是让手机关机。

### 🔫 PUBG Mobile
*   **帧率优先:** 提供了“流畅+极限帧率(60/90)”的选项。对于竞技游戏，降低画质（Low Tier设置）换取高帧率（High Tier 帧率策略）是常规操作。
*   **LOD 策略:** 远处的草丛在低画质下直接不显示，但这涉及到**竞技公平性**（低画质透视挂）。Vampirefall 是 PVE，不需要担心这个，低画质应该尽可能剔除草丛。

---

## 🔗 4. 参考资料 (References)
*   📄 **[HDR 渲染机制](HDR_DeepDive.md):** 哪些档位该开 HDR。
*   📄 **[Unity Manual - Quality Settings]:** Unity 自带的画质分级系统。
