# 📱 移动端深度优化指南 (Mobile Optimization Guide)

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
