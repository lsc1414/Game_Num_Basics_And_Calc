# 🧙‍♂️ Unity 粒子系统深度研究 (Particle System Deep Dive)

> **"特效是游戏的化妆术，但也可能是显卡的火葬场。"**
>
> 本文档旨在解构 Unity 粒子系统 (Shuriken)，从美术制作管线 (Blender/Shader) 到程序控制 (C#)，再到设计分类。

---

## 📚 1. 理论基础 (Theoretical Basis)

### 🎇 特效分类学 (VFX Taxonomy)

在 _Vampirefall_ 中，我们把特效分为三个层级，优先级递减：

1.  **Gameplay 关键特效 (High Priority)**
    - **定义:** 玩家必须看到的逻辑反馈。
    - **例子:** 怪物受击飙血、Boss 技能预警圈 (Telegraph)、玩家升级金光、掉落传说装备的光柱。
    - **特点:** 高亮度、高饱和度、永远渲染 (Always Simulate)。
2.  **环境氛围特效 (Medium Priority)**

    - **定义:** 增强沉浸感，但如果不显示也不影响玩。
    - **例子:** 场景中的火把、漂浮的尘埃、远处的雷电、雨雪。
    - **特点:** 只有在视野内渲染，低透明度。
3.  **修饰性特效 (Low Priority)**

    - **定义:** 纯粹的 "Juice"。
    - **例子:** 跑步脚下的烟尘、UI 按钮的流光、子弹拖尾的微弱扰动。
    - **特点:** 性能吃紧时第一个被剔除。

### 🎨 节奏与动态 (Timing & Dynamics)

一个好的粒子特效通常遵循 **"预备-爆发-消散"** 的动画原则：

1.  **Anticipation (预备):** 聚气、发光变亮。 (0.1 - 0.3s)
2.  **Climax (爆发):** 粒子瞬间大量发射 (Burst)、冲击波扩散。 (1 帧 - 0.2s)

3.  **Dissipation (消散):** 速度减缓、透明度渐变至 0、体积变大。 (0.5s - 2s)

---

## 🛠️ 2. 实践应用 (Practical Implementation)

### 🏭 制作管线：Blender, Shader 与 Unity 的协奏

单纯靠 Unity 自带的“小球”做不出 3A 特效。现代工作流是三位一体的：

#### A. Blender: 形状的缔造者

粒子系统不仅能发射 Quad (面片)，还能发射 Mesh (模型)。

- **碎块 (Debris):** 在 Blender 中破碎一个石头模型，导入 Unity 作为粒子发射的 `Renderer -> Mesh`。
- **特殊光效形状:**
    - 制作一个半球体或圆锥体模型。
    - 在 Unity 中给它上一个溶解 Shader。
    - 通过粒子系统控制其旋转和缩放，做出“旋风斩”或“护盾”效果。
    - _UV 技巧:_ 在 Blender 展 UV 时将 UV 拉直，可以让纹理在 Unity 里沿着模型“流动”。

#### B. Shader: 灵魂注入

不要只用 `Particles/Standard Surface`。

- **溶解 (Dissolve):** 配合噪声图 (Noise Texture) 控制 Alpha Clip，做出灰飞烟灭的效果。
- **畸变 (Distortion/Heat Haze):** 使用 `GrabPass` 或 URP 的 `CameraOpaqueTexture` 扭曲背景，表现爆炸的热浪或剑气的冲击波动。
- **菲涅尔 (Fresnel):** 让粒子边缘发光，中间透明，极大地增强能量体的“体积感”。

#### C. Unity C#: 让粒子“活”起来 (Data-Driven VFX)

这是程序与美术的交汇点。**不要把特效做死 Prefab，要让它随数值变化。**

**案例：根据攻击力改变火球大小和颜色**

```csharp
using UnityEngine;

[RequireComponent(typeof(ParticleSystem))]
public class DynamicFireball : MonoBehaviour
{
    private ParticleSystem _ps;
    private ParticleSystem.MainModule _main;
    private ParticleSystem.EmissionModule _emission;

    void Awake()
    {
        _ps = GetComponent<ParticleSystem>();
        _main = _ps.main;
        _emission = _ps.emission;
    }

    /// <summary>
    /// 初始化火球状态
    /// </summary>
    /// <param name="damage">伤害值（影响大小）</param>
    /// <param name="isCrit">是否暴击（影响颜色）</param>
    public void Setup(float damage, bool isCrit)
    {
        // 1. 根据伤害值线性放大粒子
        // 基础大小 1.0，每 100 点伤害增加 0.5 倍大小
        float scaleFactor = 1.0f + (damage / 100.0f) * 0.5f;

        // ⚠️ 注意：不要直接改 transform.localScale，因为会被粒子系统覆盖。
        // 要改 StartSize。如果是 3D 粒子可能还需要改 startSize3D。
        _main.startSizeMultiplier = scaleFactor;

        // 2. 暴击改变颜色
        if (isCrit)
        {
            // 暴击变紫火
            _main.startColor = new ParticleSystem.MinMaxGradient(Color.purple);

            // 暴击增加粒子数量 (Burst)
            // 这里的 GetBurst(0) 假设你 Prefab 里至少配置了一个 Burst
            var burst = _emission.GetBurst(0);
            burst.count = new ParticleSystem.MinMaxCurve(20, 30); // 增加爆裂感
            _emission.SetBurst(0, burst);
        }
    }
}
```

### 🧬 Vampirefall 核心模块速查

1.  **Emission (发射):**
    - `Rate over Time`: 持续喷射（如喷火器）。
    - `Bursts`: 瞬间爆发（如爆炸、开枪）。**打击感来源**。
2.  **Shape (形状):**

    - `Cone`: 最常用，调节 Angle 可以变成扇形或圆柱。
    - `Mesh`: 从模型表面发射（如全身燃烧的效果）。
3.  **Velocity over Lifetime:**

    - 模拟空气阻力（Linear Drag）。
    - `Orbital`: 制作围绕中心旋转的魔法粒子。
4.  **Size over Lifetime:**

    - **必调曲线:** 同样是 `0 -> 1 -> 0` (从小变大再消失)，这比突然消失要自然得多。
5.  **Render Mode:**

    - `Billboard`: 永远朝向摄像机（性能最好）。
    - `Stretched Billboard`: 速度越快拉得越长（模拟速度线、火花）。

---

## 🌟 3. 业界优秀案例 (Industry Best Practices)

### ⚔️ Hades (哈迪斯)

- **清晰度优先:** 即使满屏弹幕，Hades 的特效也非常“克制”。敌人的子弹通常是**高对比度的纯色轮廓**，没有多余的模糊光晕，确保玩家一眼就能识别判定范围。
- **受击闪白 (Flash):** 敌人受击时，Sprite 会瞬间变全白 (Material Property Block)，叠加少量的 Sparks 粒子。这种“微特效”反馈极好且不掉帧。

### 💀 Dead Cells (死亡细胞)

- **像素粒子:** 既然是像素风游戏，粒子也是一个个大的正方形像素。千万别在像素游戏里放高清辉光烟雾，会极度违和。
- **顿帧 (Hit Stop):** 粒子爆发的一瞬间，游戏逻辑暂停 0.1 秒。这让特效看起来更有“力度”。

---

## 🔗 4. 参考资料 (References)

- 📺 **Mirza (YouTube):** Unity VFX 教程大神，尤其擅长 Shader + Particle 结合。
- 📺 **Gabriel Aguiar Prod:** 很多具体的技能特效教程（火球、刀光）。
- 🌐 **RealtimeVFX:** 全球特效美术师论坛，寻找灵感的宝库。
- 📄 **[VFX Optimization Guide[特效优化](VFX_Optimization_Guide.md):** 本项目的特效性能红线（必读）。

---

## 🔍 5. 粒子特效关键字速查表 (VFX Keyword Library)

做游戏找素材时，用英语搜索远比中文准确。请使用以下关键字组合搜索 Unity Asset Store 或文件名。

### 🔥 元素与属性 (Element & Type)

|          元素 (CN)              |          关键字 (EN)              |          关联词 (Related)                                               |
|          :------------          |          :--------------          |          :----------------------------------------------------          |
|          **火**                 |          `Fire`, `Flame`          |          `Burn`, `Ignite`, `Heat`, `Hell`                               |
|          **冰/水**              |          `Ice`, `Frost`           |          `Freeze`, `Cold`, `Snow`, `Water`, `Splash`, `Bubble`          |
|          **电**                 |          `Lightning`              |          `Electric`, `Spark`, `Thunder`, `Shock`, `Zap`                 |
|          **毒**                 |          `Poison`                 |          `Acid`, `Toxic`, `Venom`, `Goo`, `Slime`                       |
|          **神圣/光**            |          `Holy`                   |          `Divine`, `Light`, `Shine`, `Angel`, `Heal`                    |
|          **暗影/邪恶**          |          `Dark`                   |          `Shadow`, `Evil`, `Curse`, `Void`, `Abyss`                     |
|          **血**                 |          `Blood`                  |          `Gore`, `Bleed`, `Red`                                         |
|          **土/石**              |          `Earth`                  |          `Rock`, `Stone`, `Debris`, `Dust`, `Sand`                      |
|          **风**                 |          `Wind`                   |          `Tornado`, `Swirl`, `Air`, `Breeze`                            |

### 💥 动作与功能 (Action & Function)

|          动作 (CN)              |          关键字 (EN)           |          描述                                                     |
|          :------------          |          :-----------          |          :----------------------------------------------          |
|          **抛射物**             |          `Projectile`          |          `Missile`, `Bullet`, `Shot` (火球、箭矢)                 |
|          **命中/受击**          |          `Hit`                 |          `Impact`, `Strike`, `Damage` (打中目标的瞬间)            |
|          **爆炸**               |          `Explosion`           |          `Bomb`, `Blast`, `Boom` (范围伤害)                       |
|          **增益**               |          `Buff`                |          `PowerUp`, `Boost`, `Aura` (身上的光环)                  |
|          **减益**               |          `Debuff`              |          `Curse`, `Stun`, `Slow` (头顶的晕眩星星)                 |
|          **蓄力**               |          `Charge`              |          `Gather`, `Load` (技能释放前的聚气)                      |
|          **施法**               |          `Cast`                |          `Spell`, `Skill`, `Attack` (挥手瞬间的光效)              |
|          **死亡**               |          `Die`                 |          `Death`, `Disappear`, `Soul` (怪物消失)                  |
|          **刀光**               |          `Slash`               |          `Trail`, `Sword`, `Cut`, `Swipe` (近战挥砍轨迹)          |

### 📐 形状与动态 (Shape & Motion)

|          形状 (CN)                |          关键字 (EN)          |          视觉特征                                                    |
|          :--------------          |          :----------          |          :-------------------------------------------------          |
|          **光环**                 |          `Aura`               |          围绕角色身体的持续光效 (升级、狂暴)。                       |
|          **新星/冲击波**          |          `Nova`               |          `Shockwave`, `Ripple`, `Ring` (向四周扩散的圆环)。          |
|          **光束**                 |          `Beam`               |          `Laser`, `Ray` (持续连接两点的激光)。                       |
|          **拖尾**                 |          `Trail`              |          `Ribbon` (跟随运动物体的尾巴)。                             |
|          **护盾**                 |          `Shield`             |          `Barrier`, `Dome`, `Sphere` (半球体防护罩)。                |
|          **区域**                 |          `Zone`               |          `Area`, `Ground`, `Circle` (地面的法阵/预警圈)。            |
|          **漩涡**                 |          `Vortex`             |          `Portal`, `Blackhole` (旋转的传送门)。                      |

### 🎨 风格 (Style)

|          风格 (CN)              |          关键字 (EN)          |          备注                                                            |
|          :------------          |          :----------          |          :-----------------------------------------------------          |
|          **卡通**               |          `Toon`               |          `Cartoon`, `Stylized`, `Cel-Shaded` (适合 Vampirefall)          |
|          **写实**               |          `Realistic`          |          `Cinematic` (通常粒子数过多，慎用)                              |
|          **像素**               |          `Pixel`              |          `Retro`, `8-bit`, `Voxel` (适合像素游戏)                        |
|          **低多边形**           |          `LowPoly`            |          `Flat` (棱角分明)                                               |
|          **发光/霓虹**          |          `Glow`               |          `Neon`, `Cyberpunk` (赛博朋克风)                                |

---

## 🎨 6. 常用粒子 Shader 详解 (Common VFX Shaders)

粒子系统本身只是发射器，真正决定“看起来像什么”的是 Shader。

### 🔥 1. Additive vs Alpha Blend (基础混合)

- **Additive (线性减淡):**
    - **原理:** `SrcAlpha One`。将像素亮度**叠加**到背景上。
    - **用途:** 光效、火焰、魔法、激光。
    - **特点:** **越叠越亮**，永远不会产生黑色。不会有排序问题（不用管谁在前谁在后）。
- **Alpha Blend (透明混合):**
    - **原理:** `SrcAlpha OneMinusSrcAlpha`。标准的透明度混合。
    - **用途:** 黑烟、灰尘、碎片、深色魔法。
    - **缺点:** 有排序问题 (Sorting Issue)，如果两个烟雾重叠，很容易穿帮。

### 🌫️ 2. Dissolve / Erosion (溶解/侵蚀)

- **原理:** 读取一张**噪声图 (Noise Texture)**，根据一个 `Cutoff` 值裁剪像素。
    - `if (noise_value < cutoff) discard;`
- **用途:**
    - **消失:** 火球消散、传送门关闭。
    - **形状变化:** 用圆形 mask 配合噪声，可以做出边缘不规则的火球。
    - **Remap:** 将溶解边缘映射为发光色 (Edge Color)，做出燃烧殆尽的余烬效果。

### 😵 3. Distortion / Refraction (扭曲/热扰动)

- **原理:**
    - **GrabPass:** 先把当前屏幕截图。
    - **Offset:** 根据法线贴图 (Normal Map) 偏移 UV 采样屏幕截图。
- **用途:** 爆炸时的热浪 (Heat Haze)、剑气划过空气的波动、水波纹。
- **性能警示:** 尤其在移动端，GrabPass 开销很大。URP 下建议使用 Opaque Texture。

### 🔆 4. Fresnel / Rim (菲涅尔/边缘光)

- **原理:** `dot(Normal, ViewDir)`。计算表面法线和视线角度的点积。
- **用途:**
    - **能量罩:** 边缘亮，中间透。
    - **体积感:** 让球形粒子看起来像个球，而不是平面圆。

### 🌊 5. UV Scroll / Flow (UV 流动)

- **原理:** `UV += Time * Speed`。
- **用途:**
    - **激光:** 纹理快速在一根极长的 Quad 上流动。
    - **熔岩/水流:** 缓慢流动。
    - **拖尾:** 让剑光的纹理动起来，而不是僵硬的拖拽。

### 🌉 6. Soft Particles (软粒子/深度消隐)

- **原理:** 读取 `SceneDepth` (场景深度) 和当前像素 Deepth 对比。如果非常接近，则把 Alpha 设为 0。
- **用途:** 解决粒子和地面/墙壁相交时的“硬切边” (Hard Edge) 问题，让烟雾与地面融合更自然。

### 🎞️ 7. Flipbook (序列帧)

- **原理:** 不改变 Shader，而是由粒子系统控制 UV 跳变。
- **用途:**
    - **爆炸:** 从 4x4 或 8x8 的图集中播放一段手绘动画。
    - **性能:** 相比发射 64 个粒子模拟爆炸，播放 1 个序列帧粒子虽然显存占用高点，但 CPU/GPU 运算压力极小。

---

## ⚗️ 7. 混合模式深度解析 (Blend Modes Deep Dive)

"混合" (Blending) 是指 GPU 如何将当前画的像素 (Source) 与屏幕上已有的像素 (Destination) 结合。理解这个数学公式是成为高级特效师的关键。

### 📐 核心公式

> **FinalColor = (SrcColor _ SrcFactor) + (DstColor _ DstFactor)**

- **Src (Source):** 当前粒子的颜色。
- **Dst (Destination):** 屏幕背景的颜色。
- **Factor:** 混合系数。

### 🧬 四大常用模式

#### 1. Additive (叠加/线性减淡)

- **公式:** `Src * SrcAlpha + Dst * 1`
- **Shader:** `Blend SrcAlpha One`
- **效果:** 总是变亮。黑色 (0,0,0) 会变成透明。
- **适用:** 火焰、光球、激光、全息投影。
- **优点:** **没有排序问题 (No Sorting Issue)**。因为 `A+B` 和 `B+A` 结果一样，所以粒子谁前谁后无所谓。

#### 2. Alpha Blend (正常透明)

- **公式:** `Src * SrcAlpha + Dst * (1 - SrcAlpha)`
- **Shader:** `Blend SrcAlpha OneMinusSrcAlpha`
- **效果:** 像玻璃或烟雾一样遮挡背景。
- **适用:** 泥土、灰尘、浓烟、石头。
- **缺点:** **排序敏感 (Sorting Dependent)**。
    - 必须**从后往前**画。如果先画了前面的烟雾，深度写入了缓冲区，后面的烟雾因为深度测试失败就不画了，会导致“切边”。
    - _优化:_ 通常关闭 Alpha Blend 粒子的 Z-Write (深度写入) 来缓解切边，但会导致透视关系错误。

#### 3. Premultiplied Alpha (预乘 Alpha)

- **公式:** `Src * 1 + Dst * (1 - SrcAlpha)`
- **Shader:** `Blend One OneMinusSrcAlpha`
- **原理:** 在纹理制作阶段，已经把 RGB 乘以了 Alpha。
- **适用:** 同时需要“发光”和“遮挡”的效果（如带黑边的火焰）。也是 UI 标准混合模式。
- **优点:** 解决了 Alpha Blend 在纹理边缘出现的“黑边”或“白边”问题。

#### 4. Multiply (乘法/正片叠底)

- **公式:** `Src * Dst + Dst * 0` (简化版: `Src * Dst`)
- **Shader:** `Blend DstColor Zero`
- **效果:** 总是变暗。白色 (1,1,1) 是透明。
- **适用:** 黑色魔法、地面焦痕、阴影。

### 🔧 混合模式决策树

- 想要变亮？ -> **Additive**
- 想要变暗？ -> **Multiply**
- 想要遮挡背景？ -> **Alpha Blend**
- 想要发光但我也想让它黑一点？ -> **Premultiplied** 或 **Alpha Blend** (但可以调整颜色即 HDR)

---

## 🎨 8. 颜色控制的双重奏 (Color: Shader vs Particle System)

很多新手会困惑：Shader 里有个 `Color` (或 `Tint`)，粒子组件里也有 `Start Color` 和 `Color over Lifetime`，到底改哪个？

### ✖️ 核心逻辑：乘法 (Multiplication)

GPU 计算最终颜色通常遵循这个公式：

> **FinalColor = TextureColor _ ShaderColor _ ParticleVertexColor**

- **TextureColor:** 你的贴图颜色（比如火焰纹理本身是橘黄色的）。
- **ShaderColor:** 材质球上设置的 `Main Color` / `Tint Color`。
- **ParticleVertexColor:** 粒子系统面板里的 `Start Color` 或 `Color over Lifetime`。

这意味着：**任何一项是黑色的，结果就是黑色的。任何一项是透明的 (Alpha=0)，结果就是完全看不见。**

### ⚔️ 职责分工 (Best Practices)

#### 1. Shader Color (材质色) -> "基调"

- **设置:** 在 Material 面板里设置。
- **用法:**
    - 通常设为 **纯白 (255, 255, 255, 255)**。
    - **为什么？** 因为白色是乘法的“单位元” (`1 * x = x`)。设为白色意味着完全由粒子系统来接管颜色控制。
    - _例外:_ 如果你想统一调整整个特效的亮度（比如夜间模式整体变暗），可以改这里。

#### 2. Particle System Color (顶点色) -> "动态"

- **设置:** `Start Color`, `Color over Lifetime`, `Color by Speed`。
- **用法:** **绝大多数颜色变化都在这里做。**
    - **Start Color:** 用于做随机性（比如随机出红色火和黄色火）。
    - **Color over Lifetime:** 这一项至关重要。
        - **Fade In/Out:** 必须把两端的 Alpha 设为 0，让粒子产生淡入淡出的效果，避免生硬的出现和消失。
        - **变色:** 火焰从中心（黄色）飞向边缘变成（红色）再变成烟雾（灰色）。

### ⚠️ 常见坑点

1.  **Shader 设了颜色，粒子也设了颜色：** 结果颜色变脏或变得过暗。
    - _例:_ Shader 是红色，粒子是绿色 -> 结果是黑色/深棕色 (R _ 0 + 0 _ G)。
2.  **材质不支持顶点色 (Vertex Color):**

    - 如果你自己写 Shader，必须在 Vertex Shader 里把 `appdata.color` 传给 Fragment Shader，并在 Fragment Shader 里乘上去。
    - _症状:_ 无论怎么调 `Color over Lifetime`，粒子颜色都不变。说明你的 Shader 忘了乘 Vertex Color。
    - _Unity 自带 Shader:_ `Particles/Standard` 默认是支持的。

### 💡 颜色设置黄金法则

1.  **贴图 (Texture):** 尽量用**黑白灰 (Grayscale)**。
    - 如果是黑白图，你可以在粒子系统里随便把它染成红色、蓝色、绿色。
    - 如果是红色的火贴图，你就很难把它染成蓝色（只能得到紫色或黑色）。
2.  **材质 (Material):** 设为**白色**。

3.  **粒子 (System):** 在这里尽情挥洒颜色。

---

## 🐞 9. 调试与迭代 (Debugging & Iteration)

当粒子特效多起来，且触发条件各异（比如“暴击时”、“半血时”、“死亡时”）时，如果每次都运行游戏去测，效率太低。我们需要更聪明的调试方法。

### ⏱️ 1. 场景视图调试 (Scene View Debugging)

Unity Scene 窗口右下角有一个粒子控制面板（选中带 ParticleSystem 的物体时出现）。

- **Simulate Layers:** 勾选它可以让你拖动父物体时，子物体粒子也跟着动（预览拖尾效果必开）。
- **Playback Speed:** 设为 **0.1**。慢放是检查“穿帮”神技。你可以看清粒子是从哪里变出来的，或者有没有莫名其妙的跳变。
- **Resimulate:** 如果你的粒子用了 `Random Seed`，点击这个可以看到不同的随机结果。

### 🎛️ 2. 自制 VFX 预览器 (The VFX Jukebox)

不要为了测一个“Boss 死亡特效”去打十分钟 Boss。写一个简单的 Editor 工具。

**VFXPreviewWindow.cs (简易版思路):**

```csharp
// 在 Editor 文件夹下
public class VFXPreviewWindow : EditorWindow
{
    GameObject _vfxPrefab;

    void OnGUI()
    {
        _vfxPrefab = (GameObject)EditorGUILayout.ObjectField("VFX Prefab", _vfxPrefab, typeof(GameObject), false);

        if (GUILayout.Button("Play Effect"))
        {
            var instance = Instantiate(_vfxPrefab, Vector3.zero, Quaternion.identity);
            // 5秒后自动销毁，保持场景干净
            DestroyImmediate(instance, 5.0f);
        }
    }
}
```

### ⚡ 3. 使用 Odin Inspector 快速测试 (Odin Workflow)

如果项目里有 Odin Inspector，可以在 `DynamicFireball.cs` 脚本里直接加测试按钮。这比写 EditorWindow 更快。

```csharp
public class DynamicFireball : MonoBehaviour
{
    // ... 之前的代码 ...

    [Button("Test Low Energy (Small/Blue)"), GUIColor(0, 1, 1)]
    void TestLow()
    {
        Setup(damage: 10, isCrit: false);
        GetComponent<ParticleSystem>().Play();
    }

    [Button("Test ULTIMATE (Big/Purple)"), GUIColor(1, 0, 1)]
    void TestHigh()
    {
        Setup(damage: 9999, isCrit: true);
        GetComponent<ParticleSystem>().Play();
    }
}
```

**优势:** 甚至可以在**运行时** (Play Mode) 点击这个按钮，直接修改当前飞出去的火球，观察效果。

### 🛑 4. 边界框调试 (Bounding Box)

有时候粒子在屏幕边缘会突然消失。这是因为 Unity 认为它“出界”了所以剔除了它。

- **选中粒子系统 -> Renderer -> Max Particle Size:** 如果粒子很大，把这个值调大。
- **Scene View Gizmos:** 勾选 `Show Bounds`。如果看到橙色的框比你看到的粒子画面小，那就是 Bounds 没更新。
- **解决方法:** 在面板里点 `Culling Mode -> Always Simulate` (最贵但最稳) 或者定时调用 `RecalculateBounds()`。
