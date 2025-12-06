# 👮‍♂️ 美术警察：资源验证标准 (Tech Art Standards)

> **"没有规范的美术资源是性能的核泄漏。"**
>
> 好的资源不仅要好看，还要好用、好跑。这里是 Vampirefall 项目的资源“红线”。

---

## 1. 🖼️ 纹理 (Textures)

纹理是安装包体积和内存占用的最大头目。

### 🛑 铁律
*   **2的幂次方 (Power of Two - POT):** 所有纹理长宽必须是 2 的 n 次幂 (256, 512, 1024, 2048)。
    *   *为什么?* 显卡喜欢 POT。非 POT 纹理无法压缩，无法 Mipmap，内存占用大几倍。
    *   *特例:* UI图片如果是 Sprite Atlas 的一部分，可以用非 POT，但 Atlas 本身必须是 POT。
*   **尺寸限制 (Max Size):**
    *   **PC:** 主角/Boss 用 2048，普通怪/环境 1024/512。
    *   **Mobile:** 主角/Boss 用 1024，普通怪 512，特效 256。
    *   *禁止:* 在手机上使用 4K 贴图。除了发热没有任何意义。

### 📦 压缩格式 (Compression)
*   不要使用 `RGB24` 或 `RGBA32` (除非是 UI 且必须要极致清晰)。这就好比用 BMP 格式存照片。
*   **Android:** 统一使用 `ASTC 6x6` (平衡) 或 `ASTC 8x8` (体积小)。
*   **iOS:** 同 Android (ASTC)。
*   **PC:** 使用 `DXT5/BC3` (带透明) 或 `DXT1/BC1` (不带透明)。

---

## 2. 🗿 模型 (Models)

### 📊 面数预算 (Polycount Budget) - 单个模型三角形数
| 类型 | PC (High) | Mobile (Mid) | 备注 |
| :--- | :--- | :--- | :--- |
| **主角** | 20k - 30k | 5k - 8k | 毕竟玩家一直盯着看 |
| **普通怪** | 5k - 10k | 1.5k - 3k | 同屏可能几十个 |
| **Boss** | 15k - 25k | 5k - 10k | |
| **环境物体** | 1k - 5k | 500 - 1k | 甚至可以用 Billboard |

### 🛠️ 制作规范
*   **UV:** 必须全部在 0-1 空间内。不要重叠 (Overlapping) 除非是有意为之的共用 UV。
*   **Pivot (轴心点):**
    *   角色/怪物的轴心点必须在 **双脚底部的中心** (0,0,0)。不要在腰上，不要在头顶。
    *   门/可交互物的轴心点应在旋转轴上。
*   **Scale:** 导入 Unity 后 Scale 必须是 `(1,1,1)`。严禁在 Transform 里缩放模型，请在建模软件里应用缩放。

---

## 3. 🎨 材质与Shader (Materials)

### ⚠️ Batching 杀手
*   **变体控制:** 尽量让多个物体共用同一个材质球。此时启用 `GPU Instancing` 可以把 1000 个物体合为一个 DrawCall。
*   **禁止Standard Shader:** 在移动端，Unity 自带的 Standard Shader 是性能黑洞。
    *   请使用 **URP/Lit** 或 **URP/Simple Lit** (甚至 Unlit)。
    *   对于特效，使用 Particle Shader。

---

## 4. 🔊 音频 (Audio)

*   **格式:**
    *   **长音乐 (BGM):** `Vorbis` / `MP3`。勾选 `Load in Background`。
    *   **短音效 (SFX):** `PCM` (极短) 或 `ADPCM`。
*   **声道:**
    *   **95% 的音效应该是 Mono (单声道)。** 只有 BGM 或某些特定环境音需要 Stereo。
    *   *为什么?* 单声道内存占用减半，且在 3D 空间化 (Spatial Blend) 时表现更好。

---

## 5. 🏷️ 命名规范 (The Law of Naming)

如果不按这个命名，自动化工具会把你的资源删掉。

*   **T_Name_Suffux** (Texture)
    *   `T_Hero_D` (Diffuse/Albedo)
    *   `T_Hero_N` (Normal)
    *   `T_Hero_M` (Mask/Metallic)
*   **M_Name** (Material)
    *   `M_Hero_Skin`
*   **SM_Name** (Static Mesh)
*   **SK_Name** (Skeletal Mesh)
*   **A_Name** (Audio)
    *   `A_BGM_Menu`
    *   `A_SFX_Hit_01`
