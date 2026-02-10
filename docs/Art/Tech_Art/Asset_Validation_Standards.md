---
sidebarTitle: "美术警察：资源验证标准"
title: "美术警察：资源验证标准"
---
> **摘要**：本文聚焦「美术警察：资源验证标准」，梳理核心概念、关键方法与落地实践。

---

> **"没有规范的美术资源是性能的核泄漏。"**
>
> 好的资源不仅要好看，还要好用、好跑。这里是 Vampirefall 项目的资源“红线”。

---

## 1. 🖼️ 纹理 (Textures)

纹理是安装包体积和内存占用的最大头目。

### 🛑 铁律

- **2 的幂次方 (Power of Two - POT):** 所有纹理长宽必须是 2 的 n 次幂 (256, 512, 1024, 2048)。
  - _为什么?_ 显卡喜欢 POT。非 POT 纹理无法压缩，无法 Mipmap，内存占用大几倍。
  - _特例:_ UI 图片如果是 Sprite Atlas 的一部分，可以用非 POT，但 Atlas 本身必须是 POT。
- **尺寸限制 (Max Size):**
  - **PC:** 主角/Boss 用 2048，普通怪/环境 1024/512。
  - **Mobile:** 主角/Boss 用 1024，普通怪 512，特效 256。
  - _禁止:_ 在手机上使用 4K 贴图。除了发热没有任何意义。

### 📦 压缩格式 (Compression)

- 不要使用 `RGB24` 或 `RGBA32` (除非是 UI 且必须要极致清晰)。这就好比用 BMP 格式存照片。
- **Android:** 统一使用 `ASTC 6x6` (平衡) 或 `ASTC 8x8` (体积小)。
- **iOS:** 同 Android (ASTC)。
- **PC:** 使用 `DXT5/BC3` (带透明) 或 `DXT1/BC1` (不带透明)。

---

## 2. 🗿 模型 (Models)

### 📊 面数预算 (Polycount Budget) - 单个模型三角形数

| 类型         | PC (High) | Mobile (Mid) | 备注                 |
| :----------- | :-------- | :----------- | :------------------- |
| **主角**     | 20k - 30k | 5k - 8k      | 毕竟玩家一直盯着看   |
| **普通怪**   | 5k - 10k  | 1.5k - 3k    | 同屏可能几十个       |
| **Boss**     | 15k - 25k | 5k - 10k     |                      |
| **环境物体** | 1k - 5k   | 500 - 1k     | 甚至可以用 Billboard |

### 🛠️ 制作规范

- **UV:** 必须全部在 0-1 空间内。不要重叠 (Overlapping) 除非是有意为之的共用 UV。
- **Pivot (轴心点):**
  - 角色/怪物的轴心点必须在 **双脚底部的中心** (0,0,0)。不要在腰上，不要在头顶。
  - 门/可交互物的轴心点应在旋转轴上。
- **Scale:** 导入 Unity 后 Scale 必须是 `(1,1,1)`。严禁在 Transform 里缩放模型，请在建模软件里应用缩放。

---

## 3. 🎨 材质与 Shader (Materials)

### ⚠️ Batching 杀手

- **变体控制:** 尽量让多个物体共用同一个材质球。此时启用 `GPU Instancing` 可以把 1000 个物体合为一个 DrawCall。
- **禁止 Standard Shader:** 在移动端，Unity 自带的 Standard Shader 是性能黑洞。
  - 请使用 **URP/Lit** 或 **URP/Simple Lit** (甚至 Unlit)。
  - 对于特效，使用 Particle Shader。

---

## 4. 🔊 音频 (Audio)

- **格式:**
  - **长音乐 (BGM):** `Vorbis` / `MP3`。勾选 `Load in Background`。
  - **短音效 (SFX):** `PCM` (极短) 或 `ADPCM`。
- **声道:**
  - **95% 的音效应该是 Mono (单声道)。** 只有 BGM 或某些特定环境音需要 Stereo。
  - _为什么?_ 单声道内存占用减半，且在 3D 空间化 (Spatial Blend) 时表现更好。

---

## 5. 🏷️ 命名规范 (The Law of Naming)

如果不按这个命名，自动化工具会把你的资源删掉。

- **T_Name_Suffux** (Texture)
  - `T_Hero_D` (Diffuse/Albedo)
  - `T_Hero_N` (Normal)
  - `T_Hero_M` (Mask/Metallic)
- **M_Name** (Material)
  - `M_Hero_Skin`
- **SM_Name** (Static Mesh)
- **SK_Name** (Skeletal Mesh)
- **A_Name** (Audio)
  - `A_BGM_Menu`
  - `A_SFX_Hit_01`

---

## 6. 🎬 动画 (Animation)

### 🎯 动画优化原则

- **压缩 (Compression):**
  - 使用 `Optimal` 压缩,误差阈值设为 `0.5-1.0`
  - 对于不重要的动画 (远景、小怪),可以用 `Keyframe Reduction`
- **采样率 (Sample Rate):**
  - 战斗动画: 30-60 FPS
  - 循环动画 (idle, walk): 24-30 FPS
  - 过场动画: 可以用 60 FPS
- **根运动 (Root Motion):**
  - 移动类动画 (冲刺、位移技能) 必须启用 Root Motion
  - 原地动画 (攻击、受击) 禁用 Root Motion

### ⚠️ 常见陷阱

- **烘焙位移 (Baked Position):** 如果动画本身含有 Y 轴位移,会导致角色"飘"或"陷入地面"
- **动画事件 (Animation Events):** 不要在一帧内触发多个事件,会导致逻辑执行顺序混乱

---

## 7. ✨ 粒子特效 (VFX / Particle Systems)

> [!WARNING]
> 粒子系统是移动端性能杀手第二名 (第一名是透明度叠加)。

### 📐 粒子数量限制

| 特效类型        | 最大粒子数 (Mobile) | 最大粒子数 (PC) |
| :-------------- | :------------------ | :-------------- |
| 技能特效        | 50-100              | 200-500         |
| 环境特效 (单个) | 20-30               | 50-100          |
| 同屏总量        | 300                 | 1000            |

### 🛠️ 制作建议

- **纹理复用:** 多个特效共用同一张 Texture Atlas
- **GPU Instancing:** 对于大量相同粒子,启用 GPU Instancing
- **禁用 `Collision`:** 粒子碰撞检测非常昂贵,除非美术效果必须
- **Sub Emitters 慎用:** 每增加一个子发射器,性能开销翻倍
- **使用 `Mesh Particles` 谨慎:** 如果必须用 Mesh,面数控制在 10 以内

---

## 8. 🔍 LOD (Level of Detail) 系统

### 📊 LOD 配置标准

对于主要角色和 Boss,必须配置 LOD:

- **LOD 0** (近景): 100% 细节
- **LOD 1** (中景): 60% 面数,1024 纹理
- **LOD 2** (远景): 30% 面数,512 纹理 (或 Billboard)

### 🎯 切换距离 (Transition Distance)

- **角色:**
  - LOD 0 → 1: 10-15 米
  - LOD 1 → 2: 30-50 米
- **环境物体:**
  - 更激进,5 米开始降级

---

## 9. 🛠️ 验证工具 (Validation Tools)

### Unity 内置工具

- **Profiler:** 实时查看渲染性能、内存占用、GC
- **Frame Debugger:** 逐帧查看每个 DrawCall 的渲染内容
- **Memory Profiler:** 分析纹理、网格的内存占用

### 自定义验证脚本

使用 `AssetPostprocessor` 自动检查:

```csharp
public class AssetValidationPostprocessor : AssetPostprocessor
{
    void OnPreprocessTexture()
    {
        TextureImporter importer = (TextureImporter)assetImporter;

        // 检查纹理尺寸是否为 2 的幂次方
        Texture2D texture = AssetDatabase.LoadAssetAtPath<Texture2D>(assetPath);
        if (!IsPowerOfTwo(texture.width) || !IsPowerOfTwo(texture.height))
        {
            Debug.LogError($"[资源验证失败] {assetPath} 尺寸非POT");
        }

        // 强制设置压缩格式
        if (assetPath.Contains("Textures/Characters"))
        {
            var androidSettings = importer.GetPlatformTextureSettings("Android");
            androidSettings.format = TextureImporterFormat.ASTC_6x6;
            androidSettings.maxTextureSize = 1024;
            importer.SetPlatformTextureSettings(androidSettings);
        }
    }

    bool IsPowerOfTwo(int x) => (x & (x - 1)) == 0;
}
```

---

## 10. 💀 常见错误 Case Study

### Case 1: UI 图集炸裂

**现象:** 某次更新后,游戏启动时内存暴增 500MB

**原因:** 美术导入了一张 `4096x4096` 的 UI 背景图,且设置为 `RGBA32` 未压缩

**计算:**

$$
4096 \times 4096 \times 4 \text{ bytes} = 64 \text{ MB (单张)}
$$

加上 Mipmap 和 Unity 内部缓存,实际占用 ~100MB

**解决:**

1. 将背景图拆分为可重复 tile 的小图
2. 使用 `ASTC 6x6` 压缩,降至 ~4MB

---

### Case 2: 透明度混合导致的 Overdraw

**现象:** 某个场景帧率骤降至 20 FPS (移动端)

**原因:** 多层半透明粒子特效叠加,单个像素被绘制了 30+ 次

**检测:** 使用 `Overdraw` 视图,发现屏幕大部分区域为红色/白色

**解决:**

1. 减少粒子层数
2. 使用 `Additive` 混合代替 `Alpha Blend`
3. 将部分粒子改为 `Opaque` (不透明)

---

### Case 3: 动画烘焙导致的"飘"

**现象:** 角色跳跃后落地时会悬浮 0.5 米

**原因:** 动画师在 Maya 中烘焙了角色的 Y 轴位移,导入 Unity 后与物理系统冲突

**解决:**

1. 在 Unity Importer 中禁用 `Bake Y Position`
2. 使用代码控制角色位移,动画只负责姿态

---

## 11. 🤖 自动化流程 (CI/CD Integration)

### Pre-Commit Hook

在 Git 提交前自动检查资源:

```bash
#!/bin/bash
## .git/hooks/pre-commit

echo "🔍 正在检查美术资源..."

## 检查纹理尺寸
python tools/validate_textures.py

if [ $? -ne 0 ]; then
    echo "❌ 资源验证失败,请修复后再提交"
    exit 1
fi

echo "✅ 资源验证通过"
```

### Jenkins 流水线

在每次打包前运行完整验证:

```groovy
stage('Asset Validation') {
    steps {
        script {
            sh 'unity -batchmode -executeMethod AssetValidator.RunFullCheck'

            // 读取验证报告
            def report = readJSON file: 'validation_report.json'
            if (report.errors > 0) {
                error("发现 ${report.errors} 个资源错误")
            }
        }
    }
}
```

---

## 12. ✅ 实战检查清单 (Checklist)

在提交资源前,请逐项检查:

### 纹理

- [ ] 尺寸为 2 的幂次方 (POT)
- [ ] 已设置正确的压缩格式 (ASTC/DXT)
- [ ] Max Size 符合平台限制
- [ ] 命名符合规范 (`T_Name_Suffix`)
- [ ] 未使用 `RGB24` 或 `RGBA32` (除非特殊需求)

### 模型

- [ ] 面数符合预算
- [ ] UV 在 0-1 范围内
- [ ] Pivot 位置正确 (角色在脚底)
- [ ] Scale 为 (1,1,1)
- [ ] 已移除多余的 UV 通道和顶点色

### 材质

- [ ] 使用 URP Shader (禁用 Standard)
- [ ] 启用 GPU Instancing (如适用)
- [ ] 纹理槽位未空置 (空槽会浪费内存)

### 动画

- [ ] 已设置压缩 (Optimal)
- [ ] 采样率合理 (24-60 FPS)
- [ ] Root Motion 设置正确
- [ ] 未包含冗余的 Curve (如 `m_LocalScale` 未变化但仍记录)

### 音频

- [ ] BGM 使用 `Vorbis/MP3`,勾选 `Streaming`
- [ ] SFX 使用 `ADPCM`,设为 `Decompress on Load`
- [ ] 95% 的 SFX 为 Mono (单声道)

### 特效

- [ ] 粒子数量在限制范围内
- [ ] 未使用粒子碰撞检测
- [ ] 纹理复用 (Atlas)
- [ ] Sub Emitters 数量 ≤ 2

---

## 13. 📚 延伸阅读

- [Unity 性能优化最佳实践](https://docs.unity3d.com/Manual/BestPracticeUnderstandingPerformanceInUnity.html)
- [URP 渲染管线](https://docs.unity3d.com/Packages/com.unity.render-pipelines.universal@latest)
- [移动端 GPU 架构 (TBDR)](../Tech/Mobile_Optimization_Guide.md)

---

## 📝 版本历史

| 版本 | 日期       | 修改内容                    |
| :--- | :--------- | :-------------------------- |
| 1.0  | 2026-01-01 | 初始版本                    |
| 1.1  | 2026-01-09 | 新增动画、LOD、验证工具章节 |
