# ✨ 特效优化黑魔法 (VFX Optimization Guide)

> **"好看的特效让人惊叹，好跑的特效让人留存。"**
>
> 很多游戏在中低端机上发热、降频、卡顿，罪魁祸首往往不是模型，而是**半透明特效 (Overdraw)**。

---

## 1. 核心大敌：Overdraw (像素重绘)

当多个半透明粒子（烟雾、火焰、光晕）重叠时，GPU 需要对同一个像素进行多次计算和混合。
*   **现象：** 屏幕变白（在 Overdraw View 模式下），手机瞬间发烫。
*   **红线标准：**
    *   **Mobile:** 单帧全屏 Overdraw 不超过 **3-5 层**。
    *   **PC:** 不超过 **10 层**。

### 📉 优化手段
1.  **减少粒子面积：** 尽量只让必要的像素半透明。不要用一张大大的空图，中间只有一小团烟雾。使用 **Mesh Emitter** 代替 Quad，裁剪掉空白区域 (Tight Geometry)。
2.  **粒子剔除 (Culling):** 屏幕外的粒子必须停止渲染。启用 Particle System 的 `Culling Mode: Pause and Catchup` 或 `Always Simulate` (但在屏幕外不渲染)。
3.  **避免全屏特效：** 尽量不要做全屏的受击红光或泛光，或者使用极低分辨率的 RT 实现。

---

## 2. 粒子系统设置 (Particle System Checklist)

每个特效 Prefab 提交前必须检查的清单。

*   [ ] **Max Particles:** 绝对不能是默认的 1000。
    *   普通命中：限制 **5-10** 个。
    *   大招：限制 **50-100** 个。
    *   *每一个粒子都是显存开销。*
*   [ ] **Mesh vs Billboard:**
    *   大量小粒子（火星、雨滴）使用 **Billboard** (GPU Instancing)。
    *   少量复杂形状使用 **Mesh**。
*   [ ] **Texture Sheet Animation:**
    *   使用序列帧动画代替大量粒子发射。一张 4x4 的序列帧烟雾，比发射 16 个烟雾粒子性能好得多。

---

## 3. 材质与 Shader (Material Magic)

*   **Add vs Blend:**
    *   **Additive (线性减淡):** 性能较好，不用排序。适合光效、火焰。
    *   **Alpha Blend (透明混合):** 性能较差，需要 CPU 排序（否则会有穿插问题）。只在必须要有“遮挡感”时使用（如浓烟）。
*   **Mobile Shader:**
    *   去把 **URP/Particles/Unlit** 作为默认 Shader。
    *   禁止在粒子 Shader 里使用复杂的光照计算、法线贴图或反射。

---

## 4. 预加载与池化 (Pooling)

特效的实例化 (Instantiate) 是极其昂贵的（因为要编译 Shader 变体、分配内存）。

*   **Warmup (预热):** 游戏开始时预加载所有常用特效（命中、开火）。
*   **Object Pooling:**
    *   特效播放完不要 Destroy，而是 `SetActive(false)` 放回池子。
    *   注意：放回池子前必须 `Stop()` 并 `Clear()` 粒子系统，防止复用时出现“残影”。

---

## 5. 显卡杀手：后处理 (Post-Processing)

*   **Bloom (泛光):** 很美，但很贵。移动端必须降级（降低 Iterations，使用 Fast Mode）。
*   **DOF (景深):** 除非只有在过场动画或暂停菜单，否则**移动端战斗中严禁开启景深**。
*   **Motion Blur (动态模糊):** 同上，为了性能请关掉。
