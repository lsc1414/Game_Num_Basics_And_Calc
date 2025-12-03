# 🔠 游戏字体排印指南 (Typography & Font Guide)

> **核心原则**: 
> 1.  **易读性 (Legibility)** > 风格 (Style)。看不清数字的塔防游戏是灾难。
> 2.  **一致性 (Consistency)**。全游戏主要字体不应超过 2 种。
> 3.  **版权安全 (License)**。必须使用商用免费字体。

## 1. 字体选型策略 (Font Selection Strategy)

### 1.1 标题/伤害数字 (Headlines & Damage Numbers)
**风格需求**: 冲击力强、硬朗、带有奇幻或哥特元素。
*   **推荐**: **粗衬线体 (Slab Serif)** 或 **厚重的无衬线体 (Heavy Sans)**。
*   **作用**: 用于 BOSS 血条、暴击数字、关卡标题 ("WAVE 10")。
*   **字体推荐 (免费商用)**:
    *   *中/西*: **Alimama ShuHeiTi (阿里妈妈数黑体)** - 极具科技感与力量感，适合伤害数字。
    *   *中/西*: **Unbounded** - 现代感强，适合科幻/肉鸽 UI。
    *   *西文*: **Bangers** / **Lilita One** - 典型的卡通/休闲游戏标题字。

### 1.2 正文/说明 (Body Text)
**风格需求**: 清晰、干净、在高分屏和低分屏上都能看清。
*   **推荐**: **无衬线体 (Sans Serif)**。绝对不要用衬线体（宋体）做正文，屏幕显示效果极差。
*   **作用**: 技能描述、剧情对话、菜单选项。
*   **字体推荐 (免费商用)**:
    *   *中/西*: **Noto Sans SC (思源黑体)** - 业界标准，字重全 (Thin 到 Black)，兼容性无敌。
    *   *中/西*: **HarmonyOS Sans (鸿蒙字体)** - 比思源黑体稍微现代一点，阅读体验极佳。

## 2. 粗体 vs 细体 (Bold vs Light)

### 2.1 粗体 (Bold / Black)
*   **用途**: **强调、肯定、能量**。
*   **场景**:
    *   **按钮**: "开始游戏"、"购买"。
    *   **关键数值**: "攻击力: **250**"。
    *   **标题**: "天赋选择"。
*   **心理学**: 粗体传递出“重要”和“实体感”。

### 2.2 细体 (Light / Regular)
*   **用途**: **优雅、次要、背景**。
*   **场景**:
    *   **辅助说明**: "攻击力: 250 *(+50 来自装备)*" —— 括号里的字用细体。
    *   **世界观文本**: 物品的背景故事 ("这把剑曾属于...")。
    *   **次要标签**: 版本号、页脚。
*   **禁忌**: **千万不要在深色背景上用太细的白色字体**。光晕效应 (Halation) 会让字变得模糊不清。

## 3. 中文字体特殊处理

### 3.1 繁简混用问题
*   Unity 的 `Font Fallback` 机制：如果主字体缺字，会自动找备用字体。
*   **风险**: 不同字体的字面大小、基线不一样。会导致一句话里“高低不平”。
*   **对策**: 使用 **TextMeshPro (TMP)**，并生成包含常用 3500/7000 汉字的 **SDF Font Asset**。尽量涵盖所有可能用到的字。

### 3.2 字重 (Weight)
*   中文字体通常不通过 `Bold` 按钮加粗（那是伪粗体，很难看）。
*   **正确做法**: 导入字体的不同字重文件 (Regular.ttf, Bold.ttf)，在 TMP 中设置 Font Weight 映射。

## 4. Vampirefall 字体方案建议

| UI 元素 | 建议字体 (免费商用) | 字重 | 颜色 | 备注 |
| :--- | :--- | :--- | :--- | :--- |
| **LOGO / 大标题** | **阿里妈妈刀隶体** 或 **方正黑变 (需授权)** | Heavy | 金色/血红 | 突出东方/奇幻韵味 |
| **伤害数字 (Crit)** | **Alimama ShuHeiTi** | Bold | 亮黄/橙 | 必须要是等宽数字 (Monospaced) |
| **普通伤害** | **Roboto Condensed** (仅数字) | Bold | 白色 | 紧凑，不挡视线 |
| **UI 标题** | **HarmonyOS Sans** | Bold | 浅灰 | |
| **技能描述** | **HarmonyOS Sans** | Regular | 白色 | 行间距设为 1.2 倍 |
| **Lore (故事)** | **Noto Serif SC (思源宋体)** | Regular | 暗金 | 宋体仅用于装饰性很强的长文本 |

## 5. TextMeshPro (TMP) 深度优化指南

### 5.1 减少 GC Alloc (Garbage Collection)
*   **问题**: `tmp.text = "Score: " + score;` 每一帧都会产生字符串垃圾，导致卡顿。
*   **解决方案**:
    1.  **使用 SetText()**: `tmp.SetText("Score: {0}", score);` (避免字符串拼接)。
    2.  **字符数组池**: 对于极高频更新的伤害数字，使用 `char[]` 缓存，直接操作数组内容。
    3.  **避免 Rich Text 解析**: 如果不需要颜色标签，勾选 `Parse Escape Characters` 关闭解析，能省一点 CPU。

### 5.2 Shader 选型与 DrawCall
*   **原则**: **同材质才能合批 (Batching)**。
*   **常见坑**:
    *   给每个 TMP 单独调了 `Face Color` (这是修改顶点色，**不打断**合批，是好的)。
    *   给每个 TMP 单独调了 `Outline` / `Softness` (这会创建材质实例 Instance，**打断**合批，是坏的)。
*   **Shader 选择**:
    *   **Mobile/Distance Field (推荐)**: 性能最好，兼容性最强。
    *   **Mobile/Distance Field Overlay**: 用于想要把字显示在 3D 模型前面的情况（关掉 ZTest）。
*   **材质管理**:
    *   如果需要两种描边样式（一种红描边，一种蓝描边），请手动创建两个 **Material Preset** (材质预设)，而不是在 Inspector 里直接改参数。这样所有用红描边的字只需 1 个 DrawCall。

### 5.3 动态字体 (Dynamic) vs 静态字体 (Static)
*   **Static (SDF)**: 预先烘焙好 7000 个常用字。
    *   *优点*: 性能极快，不占运行时 CPU。
    *   *缺点*: 遇到生僻字显示方块。
    *   *适用*: 绝大多数 UI 文本。
*   **Dynamic (OS)**: 运行时根据需要渲染字形。
    *   *优点*: 永远不缺字 (只要系统库里有)。
    *   *缺点*: 每次遇到新字都会触发纹理重建 (Texture Rebuild)，造成严重卡顿。
    *   *适用*: **玩家输入的聊天内容**、**随机生成的玩家名字**。
*   **混合策略 (Fallback)**:
    *   主字体用 **Static SDF** (涵盖 99% 的字)。
    *   Fallback 列表里放一个 **Dynamic** 的系统字体。当主字体缺字时，回退到动态生成，兼顾性能与覆盖率。

### 5.4 伤害数字特化 (Damage Text Optimization)
*Vampirefall* 同屏可能有 100 个伤害跳字。
*   **不要用 TMP_Text 组件**: 即使是 TMP 也很重。
*   **使用 Mesh 粒子系统**: 将数字 0-9 做成一张贴图，用 `ParticleSystem` 里的 `Texture Sheet Animation` 来根据数字切换 UV。
    *   *优点*: 100 个数字只需要 1 个 DrawCall，且粒子系统跑在子线程，性能吊打 TMP。
    *   *缺点*: 只能显示纯数字，不能显示文字。

## 6. TMP 描边艺术 (The Art of Outline)

### 6.1 Shader 描边 (SDF Outline) - 推荐
直接调整 Material 的 `Outline` 参数。
*   **优点**: 极快，边缘无限平滑（基于 SDF 距离场）。
*   **缺点**:
    *   如果 `Padding` 留得不够，描边会被切断（看起来字像被狗啃了）。**解决**: 生成字体时 Padding 至少设为 5，最好 10。
    *   描边会“吃掉”字的内部，导致字变细。**解决**: 调整 `Face Dilate` (扩充) 来补偿。

### 6.2 Underlay 描边 (投影模拟法)
在 Material 的 `Underlay` 面板，设置 Offset 为 0，Dilate 设大一点，Softness 设小。
*   **优点**: 真正的“外描边”，不会挤压字形。
*   **缺点**: 性能略低（多渲染一遍 Geometry）。
*   **适用**: 需要 **极粗描边** (卡通风格) 时。

### 6.3 常见穿帮与修复
*   **字变方块**: SDF 贴图分辨率太低。**解决**: 4096贴图，或改为 High Quality 采样。
*   **尖角刺**: 描边太粗时，字母的尖角（如 A, V）会刺出去。**解决**: 在 Font Asset Creator 里把采样模式改为 `SDF32` 或 `SDFAA`，能缓解。但最好的办法是不要用太极端的描边粗细。

## 7. Font Asset Creator 终极配置指南 (Best Settings)

打开 `Window > TextMeshPro > Font Asset Creator`，这是决定字体质量的战场。

### 7.1 关键参数推荐

| 参数 | 推荐值 (中文) | 推荐值 (英文/数字) | 解释 |
| :--- | :--- | :--- | :--- |
| **Character Set** | `Custom Characters` | `ASCII` | 英文选 ASCII 就够了。 |
| **Custom Character List** | *Common 3500/7000.txt* | - | 去网上找“常用汉字3500字表”贴进去。不要选 Unicode 全集，会炸内存。 |
| **Sampling Point Size** | **Auto Sizing** (或 40-60) | **Auto Sizing** | 让 TMP 自己算能塞下多大的字。 |
| **Padding** | **5 - 10** | **10 - 20** | **极其重要**。决定了描边能多粗。英文/数字通常需要更夸张的描边，所以 Padding 给大点。 |
| **Atlas Resolution** | **2048 x 2048** | **512 x 512** | 中文 2048 是起步，甚至需要 4096 (但要注意低端机内存)。 |
| **Render Mode** | **SDFAA** | **SDF** | **SDFAA** (SDF + Anti-Aliasing) 对尖角处理更好，虽然生成慢点，但运行时效果更佳。 |

### 7.2 常见误区 (Pitfalls)
*   **误区 1**: "Atlas 越大越好"。
    *   *真相*: 4096 的贴图在低端手机上可能直接导致闪退（内存占用大）。如果是像素风游戏，512 就够了。
*   **误区 2**: "Padding 越大越好"。
    *   *真相*: Padding 越大，意味着每个字占的像素越多，同样的 Atlas 能塞下的字就越少。如果在 2048 的图上塞 7000 个字，Padding 设太大字就会变得很模糊。
*   **误区 3**: "Multi Atlas Textures"。
    *   *真相*: 尽量不要开启多张纹理。多纹理意味着多 DrawCall。尽量把常用字塞进一张图。

### 7.3 针对 Vampirefall 的配置
*   **伤害数字字体**:
    *   Atlas: 512x512
    *   Padding: **20** (因为我们要给暴击数字加超粗的描边)
    *   Mode: SDF
*   **正文黑体**:
    *   Atlas: 2048x2048
    *   Padding: 5 (正文通常只有细描边或无描边，省空间给更多字)
    *   Mode: SDFAA