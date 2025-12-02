# 🎨 Shader 核心数学模式与实战指南 (The Math of Shaders)

Shader 编程的本质不是写代码，而是**数学建模**。
我们要做的就是把光照、纹理、时间等输入，通过数学公式，映射为屏幕上的每一个像素颜色。

本文档总结了游戏开发（特别是 Roguelike/塔防类）中最常用的 Shader 效果及其背后的理论公式。

---

## 1. 基础工具箱：核心函数 (The Toolkit)

在 Shader Graph 或 HLSL 中，以下 5 个函数构成了 90% 的特效基础。

### 1.1 `saturate(x)` —— 安全钳制
*   **公式:** $clamp(x, 0, 1)$
*   **作用:** 确保数值永远在 0 到 1 之间。
*   **为什么重要:** 颜色、透明度、UV 坐标通常都不应超过 1 或低于 0。任何光照计算后都建议加一个 saturate。

### 1.2 `lerp(a, b, t)` —— 线性插值
*   **公式:** $(1 - t) \cdot a + t \cdot b$
*   **作用:** 在 a 和 b 之间混合。
*   **几何直觉:** 当 t=0 是 a，t=1 是 b，t=0.5 是中间。
*   **应用:** 颜色混合、纹理混合、受击闪白 (`lerp(BaseColor, White, FlashStrength)`).

### 1.3 `step(edge, x)` & `smoothstep(min, max, x)` —— 边缘与过渡
*   **step:** 硬切。如果 $x < edge$ 返回 0，否则返回 1。
    *   *应用:* 溶解效果的硬边缘、卡通渲染的色阶。
*   **smoothstep:** 平滑过渡。在 min 和 max 之间生成一条 S 型曲线 (Hermite Interpolation)。
    *   *应用:* 软边缘、抗锯齿、能量护盾的边缘衰减。

### 1.4 `frac(x)` —— 周期循环
*   **公式:** $x - floor(x)$ (取小数部分)
*   **图像:** 锯齿波 (0 -> 1, 0 -> 1...)
*   **应用:** 制作条纹 (Stripes)、时间循环 (`frac(_Time.y * speed)`).

### 1.5 `pow(x, p)` —— 强度控制 (Gamma 曲线)
*   **作用:** 
    *   $p > 1$: 曲线下凹，暗部更暗，高光更集中（锐化）。
    *   $p < 1$: 曲线上凸，整体变亮（柔化）。
*   **应用:** 菲涅尔边缘光的宽度控制、高光范围控制。

---

## 2. 经典效果详解 (The Cookbook)

### 2.1 菲涅尔效应 (Fresnel / Rim Light)
**视觉:** 物体边缘发光（幽灵、能量盾、选中高亮）。
**理论:** 当视线方向 ($V$) 与表面法线 ($N$) 垂直时，反射最强。

*   **核心公式:** 
    $$ F = (1 - saturate(dot(N, V)))^P $$
*   **参数:** 
    *   $N$: World Normal (世界法线)
    *   $V$: View Direction (视线方向，Camera位置 - 像素位置)
    *   $dot(N, V)$: 越接近 1 代表正对着相机（中心），越接近 0 代表垂直相机（边缘）。
    *   $P$: Power (指数)，控制边缘光的宽窄。P 越大，光越细。

```hlsl
// HLSL 片段
float3 normal = normalize(i.normal);
float3 viewDir = normalize(_WorldSpaceCameraPos - i.worldPos);
float rim = 1.0 - saturate(dot(normal, viewDir));
rim = pow(rim, _RimPower);
return _RimColor * rim;
```

### 2.2 溶解/燃烧 (Dissolve / Burn)
**视觉:** 物体像纸烧焦一样消失，边缘有亮光。
**理论:** 使用一张噪点图 (Noise) 作为高度图，切掉 (Clip) 低于阈值的像素。

*   **核心逻辑:**
    1.  **采样:** $Height = tex2D(NoiseTexture, UV).r$
    2.  **裁剪:** $if (Height < _Cutoff) \ discard;$
    3.  **边缘光:** 处于裁剪边缘的像素 ($Height \approx _Cutoff$) 上色。

*   **数学技巧 (边缘带):**
    $$ Edge = step(Height - _Cutoff, _EdgeWidth) $$
    *   这表示：比阈值高一点点的那部分区域，返回 1 (发光)，其余为 0。

### 2.3 UV 流动与扭曲 (UV Scrolling & Distortion)
**视觉:** 滚动的岩浆、流动的水面、被热浪扭曲的背景。
**理论:** 在采样纹理**之前**，修改 UV 坐标。

*   **UV 滚动 (Scrolling):**
    $$ UV_{new} = UV + Speed \cdot Time $$
*   **UV 扭曲 (Distortion):**
    使用另一张噪点图来干扰当前的 UV。
    $$ UV_{distorted} = UV + tex2D(Noise, UV + Time).xy \cdot Strength $$
    *   *解释:* 就像透过凹凸不平的玻璃看东西，看到的像素位置被偏移了。

### 2.4 受击闪白 (Hit Flash)
**视觉:** 怪物受击时瞬间变全白。
**理论:** 简单的颜色插值，不涉及光照。

*   **公式:**
    $$ FinalColor = lerp(TextureColor, FlashColor, FlashStrength) $$
*   **注意:** `FlashStrength` 通常由 C# 脚本控制协程或 AnimationCurve 来驱动 (0 -> 1 -> 0)。

### 2.5 UI 去色 (Grayscale)
**视觉:** 技能冷却时图标变黑白。
**理论:** 人眼对绿色的敏感度最高，对蓝色最低。不能简单平均 RGB。

*   **亮度公式 (Luma):**
    $$ Gray = dot(Color.rgb, float3(0.299, 0.587, 0.114)) $$
*   **可控饱和度:**
    $$ Final = lerp(Gray, Color.rgb, _Saturation) $$

---

## 3. 顶点动画理论 (Vertex Displacement)

除了改变颜色（像素着色器），我们还可以改变形状（顶点着色器）。
**性能优势:** 计算量取决于顶点数，远少于像素数。适合大面积草地、水面波浪。

### 3.1 简单的旗帜飘动 (Sine Wave)
**理论:** 将顶点的 Y 轴高度作为输入，用正弦波偏移 X 或 Z 轴。

*   **公式:**
    $$ Offset.x = \sin(Vertex.y \cdot Frequency + Time \cdot Speed) \cdot Amplitude $$
    *   `Vertex.y` 作为相位偏移，确保旗帜不同高度的摆动不同步。

### 3.2 呼吸效果 (膨胀)
**理论:** 沿**法线方向**移动顶点。

*   **公式:**
    $$ Pos_{new} = Pos + Normal \cdot \sin(Time) \cdot Strength $$
*   **应用:** 史莱姆怪物的呼吸、选中目标时的脉冲框。

---

## 4. 常见渲染模式 (Rendering Modes)

理解这些决定了你的 Shader 能做什么，不能做什么。

| 模式 | 描述 | 深度写入 (ZWrite) | 渲染顺序 | 适用场景 |
| :--- | :--- | :--- | :--- | :--- |
| **Opaque (不透明)** | 最快。从前向后渲染 (利用 Early-Z 剔除)。 | On | 2000 | 角色、墙壁、地面 |
| **Cutout (镂空)** | 要么全透要么不透。硬边缘。 | On | 2450 | 草丛、铁丝网、溶解效果 |
| **Transparent (半透明)** | 最慢。从后向前渲染 (画家算法)。**不能写深度**。 | Off | 3000 | 玻璃、特效粒子、UI |

> ⚠️ **透明度排序问题:** 半透明物体如果不写入深度，经常会出现“在这个角度看是对的，转个角度就穿帮了”的问题。这是计算机图形学的经典难题。解决方法通常是：少用半透明，或者接受瑕疵。

---

## 5. 性能优化 (Optimization)

1.  **避免 `if-else` 吗?**
    *   现代 GPU 对分支预测已经做得很好。但如果是复杂的逻辑分支，且不同像素走向不同分支（Divergency），依然会降速。
    *   *技巧:* 尽量用 `step` 或 `lerp` 代替 `if`。
        *   *Bad:* `if (x > 0.5) col = white; else col = black;`
        *   *Good:* `col = lerp(black, white, step(0.5, x));`

2.  **纹理采样 (Texture Fetch) 是昂贵的:**
    *   尽量利用纹理的 RGBA 四个通道。比如 R放噪点，G放遮罩，B放高光强度。不要为了一个遮罩单独读一张图。

3.  **浮点精度:**
    *   在移动端 (Mobile)，`float` (32bit) 比 `half` (16bit) 慢且费电。
    *   位置、UV 用 `float`。
    *   颜色、法线、方向通常用 `half` 足够。

---

## 6. 2D Sprite 专用特效 (Sprite Magic)

在 2D 或 2.5D 游戏中，Sprite 的处理逻辑与 3D 物体不同。我们通常处理的是 `MainTex` (Sprite 图集) 和 `Color` (顶点色)。

### 6.1 2D 描边 (Outline)
**视觉:** 角色边缘有一圈亮色轮廓（选中效果）。
**理论:** 检测当前像素周围是否是透明像素。如果我是透明的，但我旁边有不透明的像素，那我就是“外轮廓”。

*   **采样公式 (十字采样法):**
    取上下左右 4 个点的 Alpha 值累加。
    $$ SumAlpha = A_{up} + A_{down} + A_{left} + A_{right} $$
    $$ Outline = step(_Threshold, SumAlpha) \cdot (1 - CurrentPixel.a) $$
*   **优化:** 仅仅采样 4 次可能不够平滑，高质量描边通常采样 8 次（米字型）。

### 6.2 2D 投影/斜切 (2D Planar Shadow)
**视觉:** 2D 角色脚下有一个倾斜的黑色影子。
**理论:** 利用顶点着色器，将顶点的 Y 轴映射到 X 轴偏移上。

*   **顶点变换:**
    $$ WorldPos.x += WorldPos.y \cdot \tan(Angle) $$
    $$ WorldPos.y = FloorHeight $$
*   **注意:** 需要两个 Pass。第一个 Pass 渲染影子（纯黑、半透、无 ZWrite），第二个 Pass 渲染角色本身。

---

## 7. 屏幕后处理数学 (Post-Processing Math)

后处理是在渲染完所有物体后，对整个屏幕图像 (`_MainTex`) 进行二次处理。

### 7.1 暗角 (Vignette)
**视觉:** 屏幕四角变暗，模拟相机镜头或压抑氛围（低血量）。
**理论:** 计算 UV 坐标距离中心 (0.5, 0.5) 的距离。

*   **公式:**
    $$ Dist = distance(i.uv, float2(0.5, 0.5)) $$
    $$ Mask = smoothstep(0.5, 1.0, Dist \cdot Intensity) $$
    $$ Final = Color \cdot (1 - Mask) $$

### 7.2 马赛克 (Pixelation)
**视觉:** 画面变模糊成大方块（眩晕、复古滤镜）。
**理论:** 降低 UV 的精度。将连续的 UV 坐标“量化”为台阶状。

*   **公式:**
    $$ UV_{new} = floor(UV \cdot Resolution) / Resolution $$
    *   *例子:* 如果 `Resolution` 是 100，那么 0.015 会变成 $floor(1.5)/100 = 0.01$。0.010 到 0.019 之间的所有 UV 都会变成同一个值，采到同一个颜色。

### 7.3 色差/故障风 (Chromatic Aberration / Glitch)
**视觉:** RGB 三色分离，像旧电视或赛博朋克干扰。
**理论:** 采样三次纹理，但每次给 R、G、B 通道不同的 UV 偏移。

*   **公式:**
    $$ R = tex2D(_MainTex, UV + Offset).r $$
    $$ G = tex2D(_MainTex, UV).g $$
    $$ B = tex2D(_MainTex, UV - Offset).b $$
*   **Glitch 进阶:** `Offset` 可以是一个随时间快速变化的随机数 (`frac(sin(time)*large_number)`).

---

## 8. 数学速查表 (Math Cheat Sheet)

| 想要做... | 用这个函数... |
| :--- | :--- |
| **循环/条纹** | `frac(x * scale)` |
| **硬边缘** | `step(edge, x)` |
| **软边缘** | `smoothstep(min, max, x)` |
| **闪烁/脉冲** | `sin(_Time.y * speed)` |
| **混合/过渡** | `lerp(a, b, t)` |
| **变亮/变暗 (非线性)** | `pow(x, power)` |
| **距离/圆** | `distance(uv, center)` 或 `length(vec)` |
| **旋转 UV** | 乘旋转矩阵 `[cos -sin; sin cos]` |

---

## 9. 程序化噪声与随机性 (Procedural Noise)

有时候我们不想用额外的纹理贴图（为了省内存），而是想直接在代码里生成“随机感”。

### 9.1 伪随机函数 (Pseudo-Random)
Shader 里没有 `Random.Range`。我们利用高频正弦波的 `frac` 部分来模拟随机。

*   **经典单次哈希 (One-line Hash):**
    $$ Rand(uv) = frac(\sin(dot(uv, float2(12.9898, 78.233))) \cdot 43758.5453) $$
    *   **原理:** 将 UV 坐标投影到一个大数上，取正弦波极其细碎的部分，看起来就像电视雪花。
    *   **应用:** 故障风特效的随机跳变、星星闪烁。

### 9.2 简单值噪声 (Value Noise)
如果把随机点平滑连接起来，就得到了“云”一样的效果。
*   **应用:** 动态水面、火焰扰动、不需要贴图的溶解遮罩。

---

## 10. 进阶 UI/道具特效 (Loot & Card Effects)

在 Loot 类游戏中，如何表现“传说装备”或“稀有卡牌”？全靠 Shader。

### 10.1 扫光/流光 (Sheen / Shiny Effect)
**视觉:** 一道亮光快速划过卡牌表面。
**理论:** 在 UV 空间定义一条倾斜的线，计算当前像素距离这条线的距离。

*   **数学推导:**
    1.  定义光带位置: $Pos = UV.x + UV.y$ (45度斜线)。
    2.  让光带移动: $Pos += _Time.y \cdot Speed$。
    3.  限制光带宽度: 使用 `smoothstep` 或 `pow` 提取中间亮的两边暗的区域。
    
    ```hlsl
    // 简易流光公式
    // 1. 倾斜 UV 坐标 (x + y * tan(angle))
    float sheenPos = i.uv.x + i.uv.y * 0.5; 
    // 2. 让它动起来，并循环 (frac)
    float timePos = frac(_Time.y * _Speed) * 2.0; // *2 是为了留出空隙
    // 3. 计算距离并边缘虚化
    float sheen = smoothstep(0.0, 0.2, 1.0 - abs(sheenPos - timePos));
    // 4. 叠加
    return col + sheen * _SheenColor;
    ```

### 10.2 圆形进度/冷却 (Radial Fill)
**视觉:** 技能 CD 转圈，或者圆环血条。
**理论:** 笛卡尔坐标 (x, y) 转 极坐标 (Angle, Distance)。

*   **核心函数:** `atan2(y, x)`
    *   返回值为 $(-\pi, \pi)$ (即 -3.14 到 3.14)。
*   **归一化角度:**
    $$ Angle = \frac{atan2(uv.y - 0.5, uv.x - 0.5)}{\pi \cdot 2} + 0.5 $$
    *   结果为 0 到 1 的线性增长值。
*   **判断逻辑:**
    $$ Mask = step(Angle, _FillAmount) $$
    *   如果当前角度小于填充量，显示颜色，否则透明。

### 10.3 全息投影/扫描网格 (Hologram / Scanline)
**视觉:** 科幻风格的 UI，有水平扫描线上下移动。
**理论:** 利用 WorldPos 或 ScreenPos 的 Y 轴分量，结合正弦波。

*   **公式:**
    $$ Scan = \sin(WorldPos.y \cdot Frequency + Time \cdot Speed) $$
    $$ Line = step(0.95, Scan) $$
    *   只取波峰最顶端的 5% 作为亮线。

---

## 11. HLSL 基础语法速查 (Syntax Cheat Sheet)

手写代码时的快速参考。

### 11.1 向量与矩阵 (Vectors & Matrices)
*   **声明:** `float` (32位), `half` (16位), `fixed` (11位, 仅旧硬件).
    *   `float4 v = float4(1, 0, 0, 1);`
    *   `float2 uv = v.xy;` (Swizzling: 随意组合分量)
    *   `float3 color = v.rgb;`
*   **构造:** `float3(uv, 1.0)`
*   **矩阵乘法:** `mul(MATRIX, vector)` (注意顺序!)
    *   `mul(unity_ObjectToWorld, v.vertex)`: 模型转世界

### 11.2 纹理采样 (Texture Sampling)
*   **2D 纹理:**
    *   声明: `sampler2D _MainTex;`
    *   采样: `fixed4 col = tex2D(_MainTex, i.uv);`
    *   纹理大小: `_MainTex_TexelSize` (x=1/w, y=1/h, z=w, w=h)

### 11.3 常用 Unity 宏 (Common Macros)
*   `UnityObjectToClipPos(v.vertex)`: 顶点着色器必须调用的，将模型点转为裁剪空间坐标。
*   `TRANSFORM_TEX(v.uv, _MainTex)`: 应用材质球上的 Tiling & Offset 设置。

### 11.4 常用数学函数
*   `abs(x)`: 绝对值
*   `ceil(x)` / `floor(x)`: 向上/向下取整
*   `round(x)`: 四舍五入
*   `min(a, b)` / `max(a, b)`: 最小值/最大值
*   `clamp(x, min, max)`: 钳制范围
*   `length(v)`: 向量长度
*   `distance(p1, p2)`: 两点距离
*   `normalize(v)`: 归一化 (变为长度为1的单位向量)
*   `dot(a, b)`: 点积
*   `cross(a, b)`: 叉积
*   `reflect(i, n)`: 计算反射向量

---

## 12. 终极实战模板 (The Ultimate Template)

这是一个包含 **菲涅尔边缘光**、**受击闪白**、**透明混合** 和 **基础光照** 的通用 Shader 模板。复制即用。

```hlsl
Shader "Custom/UniversalTemplate"
{
    Properties
    {
        [Header(Base)]
        _MainTex ("Texture", 2D) = "white" {}
        _Color ("Tint Color", Color) = (1,1,1,1)
        
        [Header(Effects)]
        _FlashColor ("Hit Flash Color", Color) = (1,1,1,1)
        _FlashAmount ("Flash Amount", Range(0,1)) = 0
        
        [Header(Rim Light)]
        [Toggle] _EnableRim ("Enable Rim", Float) = 0
        _RimColor ("Rim Color", Color) = (0,1,1,1)
        _RimPower ("Rim Power", Range(0.1, 10)) = 3.0
    }
    
    SubShader
    {
        // 透明物体设置: 渲染队列3000, 混合模式 Alpha Blending, 不写深度
        Tags { "Queue"="Transparent" "RenderType"="Transparent" "IgnoreProjector"="True" }
        LOD 100
        
        // 混合模式: SrcAlpha * Src + OneMinusSrcAlpha * Dst (标准透明)
        Blend SrcAlpha OneMinusSrcAlpha 
        ZWrite Off 
        Cull Back // 剔除背面

        Pass
        {
            CGPROGRAM
            #pragma vertex vert
            #pragma fragment frag
            // 开启雾效支持
            #pragma multi_compile_fog 
            
            #include "UnityCG.cginc"

            struct appdata
            {
                float4 vertex : POSITION;
                float2 uv : TEXCOORD0;
                float3 normal : NORMAL; // 需要法线来计算边缘光
            };

            struct v2f
            {
                float2 uv : TEXCOORD0;
                UNITY_FOG_COORDS(1)
                float4 vertex : SV_POSITION;
                float3 viewDir : TEXCOORD3; // 视线方向 (World Space)
                float3 normal : TEXCOORD4;  // 法线 (World Space)
            };

            sampler2D _MainTex;
            float4 _MainTex_ST; // 用于 Tiling & Offset
            fixed4 _Color;
            
            fixed4 _FlashColor;
            float _FlashAmount;
            
            float _EnableRim;
            fixed4 _RimColor;
            float _RimPower;

            v2f vert (appdata v)
            {
                v2f o;
                // 1. 顶点变换: 模型 -> 裁剪空间
                o.vertex = UnityObjectToClipPos(v.vertex);
                
                // 2. UV 变换
                o.uv = TRANSFORM_TEX(v.uv, _MainTex);
                
                // 3. 准备世界空间数据 (用于光照/边缘光)
                // 将顶点转到世界空间
                float3 worldPos = mul(unity_ObjectToWorld, v.vertex).xyz;
                // 计算视线方向: 相机位置 - 像素位置
                o.viewDir = normalize(_WorldSpaceCameraPos.xyz - worldPos);
                // 计算世界法线
                o.normal = UnityObjectToWorldNormal(v.normal);

                UNITY_TRANSFER_FOG(o,o.vertex);
                return o;
            }

            fixed4 frag (v2f i) : SV_Target
            {
                // A. 基础纹理 + 颜色叠加
                fixed4 col = tex2D(_MainTex, i.uv) * _Color;

                // B. 菲涅尔边缘光 (Fresnel / Rim)
                if (_EnableRim > 0.5)
                {
                    float3 normal = normalize(i.normal);
                    float3 viewDir = normalize(i.viewDir);
                    // N dot V: 1=中心, 0=边缘
                    float NdotV = saturate(dot(normal, viewDir)); 
                    // 反转并取指数: 边缘亮, 中心暗
                    float rim = pow(1.0 - NdotV, _RimPower);
                    
                    // 叠加方式: Additive (加法)
                    col.rgb += _RimColor.rgb * rim;
                }

                // C. 受击闪白 (Hit Flash)
                // 线性插值: 当前颜色 -> 闪光颜色
                col.rgb = lerp(col.rgb, _FlashColor.rgb, _FlashAmount);

                // D. 雾效应用
                UNITY_APPLY_FOG(i.fogCoord, col);
                
                return col;
            }
            ENDCG
        }
    }
}
```




