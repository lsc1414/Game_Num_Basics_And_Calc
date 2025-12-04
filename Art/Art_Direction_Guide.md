# 🎨 美术风格一致性指南 (Art Direction Guide)

> **研究归属**: Project Vampirefall - Art/Direction  
> **创建日期**: 2025-12-04  
> **优先级**: ⭐⭐⭐ (中)

---

## 📑 目录

1.  [理论基础 (Theoretical Basis)](#-1-理论基础-theoretical-basis)
2.  [实践应用 (Practical Implementation)](#️-2-实践应用-practical-implementation)
3.  [业界优秀案例 (Industry Best Practices)](#-3-业界优秀案例-industry-best-practices)
4.  [参考资料 (References)](#-4-参考资料-references)

---

## 📚 1. 理论基础 (Theoretical Basis)

### 1.1 核心定义

**美术风格一致性 (Art Consistency)** 不仅仅是"画得像"，而是指所有视觉元素（角色、场景、UI、特效）遵循同一套**视觉语言**和**设计逻辑**。对于 Vampirefall 这种混合品类游戏，一致性是防止画面崩坏（Visual Clutter）的第一道防线。

关键维度：
- **Shape Language (形状语言)**: 圆形（友好/安全）、方形（稳定/坚固）、三角形（危险/攻击性）。
- **Color Palette (色板)**: 限制用色数量，建立色彩层级。
- **Detail Density (细节密度)**: 焦点区域高密度，背景区域低密度（留白）。

### 1.2 色彩心理学与功能性

在游戏设计中，色彩首先是**功能性**的，其次才是装饰性的。

| 颜色 | 心理暗示 | Vampirefall 功能定义 |
| :--- | :--- | :--- |
| 🔴 **红** | 危险、生命、愤怒 | 敌人血条、Boss 攻击预警、吸血特效 |
| 🟢 **绿** | 安全、恢复、毒素 | 玩家生命恢复、毒属性塔、友军单位 |
| 🔵 **蓝** | 魔法、冷静、护盾 | 玩家法力值、护盾特效、冰霜塔 |
| 🟡 **黄** | 警告、高价值、神圣 | 暴击伤害数字、精英怪光环、金币掉落 |
| 🟣 **紫** | 神秘、诅咒、暗影 | 诅咒状态、暗影伤害、稀有掉落 (Epic) |

### 1.3 视觉层级 (Visual Hierarchy)

当屏幕上同时存在 100 个单位时，玩家应该先看哪里？

1.  **Tier 1 (最高级)**: 玩家角色、Boss 核心、致命攻击预警 (Telegraphs)。
2.  **Tier 2 (次级)**: 精英怪、高威胁小怪、关键掉落物。
3.  **Tier 3 (普通)**: 普通小怪、塔防建筑、伤害数字。
4.  **Tier 4 (背景)**: 地图地块、装饰物、尸体。

---

## 🛠️ 2. 实践应用 (Practical Implementation)

### 2.1 Vampirefall 风格定义

**关键词**: `Gothic Noir` (哥特黑色电影) + `Neon Pop` (霓虹波普)

- **基调**: 黑暗、压抑的背景（低饱和度、冷色调）。
- **高光**: 高饱和度、高亮度的特效（技能、弹幕）。
- **对比度**: 极高的明暗对比 (Chiaroscuro)，强调光影。

#### 🎨 限制性色板 (Restricted Palette)

我们不使用全色域，而是限制在特定的色相环上：
- **主色**: 深蓝灰色 (背景)、血红色 (核心视觉)。
- **辅色**: 幽灵绿 (死灵法术)、闪电金 (神圣伤害)。
- **禁忌色**: 纯黑 (#000000) 和纯白 (#FFFFFF) —— 永远使用深蓝黑或米白色代替。

### 2.2 混乱管理 (Managing Chaos)

在塔防后期，屏幕会非常混乱。我们需要技术手段来维持可读性。

#### 1. 动态对比度调整 (Dynamic Contrast)

```hlsl
// Post-processing Shader 伪代码
float4 Frag(v2f i) : SV_Target
{
    float4 sceneColor = tex2D(_MainTex, i.uv);
    
    // 如果屏幕上特效过多（通过全局变量传入 intensity），降低背景饱和度
    float desaturationAmount = _GlobalChaosLevel * 0.5; 
    float3 grayScale = Dot(sceneColor.rgb, float3(0.3, 0.59, 0.11));
    sceneColor.rgb = lerp(sceneColor.rgb, grayScale, desaturationAmount);
    
    return sceneColor;
}
```

#### 2. 轮廓线 (Rim Light / Outline)

所有可交互单位（玩家、敌人、塔）必须有**轮廓光**，将其与背景剥离。
- **玩家**: 始终有白色/金色轮廓。
- **敌人**: 受伤时闪烁红色轮廓。
- **塔**: 建造/升级时高亮轮廓。

### 2.3 Unity 实施标准

#### 📄 材质规范

所有 3D 模型必须使用统一的 Toon Shader（卡通渲染），禁止混用 PBR 和 Unlit 材质。

- **Ramp Texture**: 使用统一的阶梯光照贴图，确保阴影硬度一致。
- **Emission**: 自发光通道仅用于关键视觉元素（眼睛、武器符文）。

#### 💡 灯光设置

- **主光 (Key Light)**: 模拟月光，冷色调 (Blue-ish)，产生主要阴影。
- **补光 (Fill Light)**: 暖色调 (Purple/Red)，照亮暗部，增加体积感。
- **雾效 (Fog)**: 使用距离雾将远处背景压暗，突出前景。

---

## 🌟 3. 业界优秀案例 (Industry Best Practices)

### 3.1 Hades (Supergiant Games)

#### ✅ 风格分析：漫画书式的清晰度

- **黑色轮廓**: 所有角色都有手绘风格的黑色轮廓线，使其从复杂的背景中跳脱出来。
- **色彩编码**: 每个神祗都有专属色（宙斯=黄，波塞冬=绿/蓝，阿瑞斯=红），玩家一眼就能识别技能属性。
- **背景压暗**: 场景虽然精美，但对比度远低于角色，且大量使用冷色调后退色。

#### 🎯 Vampirefall 借鉴点

- **神祗配色** -> **塔防属性配色**：物理塔=灰/橙，魔法塔=蓝/紫，毒塔=绿。
- **UI 整合**: UI 边框使用与场景相同的哥特风格纹理，但亮度更高。

### 3.2 Hollow Knight (Team Cherry)

#### ✅ 风格分析：氛围与单色调

- **区域色调**: 每个地图区域有一个主色调（十字路=蓝，苍绿之径=绿，真菌荒地=黄褐）。
- **视差滚动**: 多层背景营造深邃的空间感，前景遮挡物增加沉浸感。
- **简单形状**: 角色设计极其简洁（圆形为主），动作清晰可读。

#### 🎯 Vampirefall 借鉴点

- **区域差异化**: 不同的关卡（墓地、城堡、血池）应有截然不同的主色调 LUT。
- **前景遮挡**: 在屏幕边缘增加模糊的前景元素（树枝、铁栏），增加窥视感。

### 3.3 Ori and the Will of the Wisps (Moon Studios)

#### ✅ 风格分析：光之绘画

- **自发光**: 角色本身就是光源，照亮周围环境。
- **软粒子**: 特效极其柔和，大量使用 Additive 混合模式，产生梦幻感。

#### 🎯 Vampirefall 借鉴点

- **玩家光源**: 吸血鬼主角应自带红色微光，照亮周围的黑暗区域（战争迷雾）。
- **拾取物高亮**: 掉落的装备和金币应有明显的光柱效果。

---

## 🔗 4. 参考资料 (References)

### 📄 必读文章

1.  **"Visual Clarity in League of Legends"**  
    - 来源: Riot Games Engineering Blog  
    - 重点: 极其详尽地解释了如何通过形状、色彩和层级来保证竞技游戏的清晰度。

2.  **"Art Direction of Hades"**  
    - 来源: Supergiant Games (Jen Zee)  
    - 重点: 角色设计与背景设计的平衡。

### 📺 视频分析

1.  **"Good Design, Bad Design: Visual Hierarchy"**  
    - 频道: Design Doc  
    - 链接: [YouTube](https://www.youtube.com/watch?v=l9x53q5AdwM)

2.  **"The Art of Color in Games"**  
    - 频道: Game Maker's Toolkit  
    - 重点: 色彩如何引导玩家和传达情绪。

### 🛠️ 工具与资源

1.  **Adobe Color**  
    - 在线配色工具，用于生成和谐的色板。

2.  **Unity Post Processing Stack v2**  
    - 必用的后处理插件（Bloom, Color Grading, Vignette）。

---

## 📊 总结

### 🎯 Vampirefall 实施建议

1.  **制定色板**: 必须产出一份 `Vampirefall_Color_Palette.png`，规定所有阵营和属性的标准色值。
2.  **Shader 统一**: 编写一个标准 `ToonLit` Shader，强制所有美术资产使用。
3.  **层级测试**: 每周进行一次"眯眼测试" (Squint Test) —— 眯起眼睛看游戏截图，如果还能分清主角和敌人，说明层级合格。
4.  **光污染控制**: 严格限制粒子特效的 Overdraw 和亮度，避免"瞎眼"特效。

---

**文档版本**: v1.0  
**最后更新**: 2025-12-04  
**维护者**: Vampirefall Art Team
