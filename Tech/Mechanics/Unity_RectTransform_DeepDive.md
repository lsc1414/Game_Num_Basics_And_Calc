# 📐 Unity RectTransform 深度解析 (The Math of UI)

`RectTransform` 是 Unity UGUI 系统的核心组件，继承自 `Transform`。虽然它保留了位置、旋转和缩放属性，但其**定位逻辑**与普通 3D 物体截然不同。

很多开发者在处理 UI 适配（分辨率变化）时感到痛苦，根源往往是对 **Anchors（锚点）**、**Pivot（轴心）** 和 **SizeDelta** 的数学定义理解不深。

---

## 1. 核心概念图解

### 1.1 Pivot (轴心) —— 自身的原点
*   **定义:** UI 元素自身的“中心点”，坐标范围通常是 (0,0) 到 (1,1)。
    *   (0.5, 0.5): 正中心。
    *   (0, 1): 左上角。
*   **作用:**
    1.  **旋转中心:** 物体绕着 Pivot 旋转。
    2.  **坐标原点:** `transform.position` 指的就是 Pivot 在世界空间的位置。
    3.  **缩放中心:** 物体向着 Pivot 收缩。

### 1.2 Anchors (锚点) —— 父级的参考系
*   **定义:** 由 4 个三角形组成（Inspector 中显示为 Min X, Min Y, Max X, Max Y）。
*   **本质:** 定义了该 UI 元素**相对于父级矩形**的哪一部分进行定位。
*   **坐标系:** 归一化坐标 (0~1)，相对于**父级**的宽高。
    *   Min(0,0) Max(0,0): 锚定在父级左下角。
    *   Min(1,1) Max(1,1): 锚定在父级右上角。
    *   Min(0,0) Max(1,1): **完全拉伸 (Stretch)**，锚点框住整个父级。

---

## 2. 两种形态：点模式 vs 拉伸模式

理解 `RectTransform` 最关键的一点是：**根据 Anchors 是否重合，属性面板显示的变量含义会完全改变！**

### 2.1 点模式 (Anchors 重合)
当 `Anchor Min` 等于 `Anchor Max` 时（例如都在中心），锚点是一个**点**。

*   **PosX / PosY / PosZ:** Pivot 相对于 **Anchor Point** 的距离。
*   **Width / Height:** 元素的固定宽和高（绝对像素值）。
*   **行为:** 父级变大时，该元素大小不变，位置随锚点移动。

### 2.2 拉伸模式 (Anchors 分离)
当 `Anchor Min` 不等于 `Anchor Max` 时（例如 Min(0,0) Max(1,0) 底边拉伸），锚点形成一个**矩形区域**。

*   **Left / Top / Right / Bottom:** 元素边缘距离 **Anchors 矩形边缘** 的距离（Padding）。
    *   这不再是 PosX/Y，而是类似 CSS 的 margin。
*   **Width / Height 消失了!** 变成了无法直接设置的值（由父级决定）。
*   **行为:** 父级变大时，该元素会随之拉伸。

---

## 3. 属性黑盒：SizeDelta 与 Offset

这是代码控制 UI 时最大的坑。

### 3.1 `sizeDelta` 的真相
很多人以为 `rectTransform.sizeDelta` 就是宽高。**大错特错！**

$$ sizeDelta = \text{ElementSize} - \text{AnchorSize} $$

*   **在点模式下:** AnchorSize 为 0，所以 `sizeDelta` **等于** 宽高。
*   **在拉伸模式下:** `sizeDelta` 代表**相对于锚点的距离差**。
    *   如果全屏拉伸 (Stretch All)，`sizeDelta` 为 (0,0) 时，代表填满父级。
    *   此时设置 `sizeDelta` 为 (100, 100)，意味着比父级**大** 100像素！(负边距)。

### 3.2 `offsetMin` 和 `offsetMax`
这两个属性是通用的，无论什么模式都能用。
*   `offsetMin`: 对应 (Left, Bottom) 的角相对于锚点的位移。
*   `offsetMax`: 对应 (Right, Top) 的角相对于锚点的位移。

**实战技巧：代码设置全屏拉伸**
```csharp
public static void StretchToFill(RectTransform rt) {
    rt.anchorMin = Vector2.zero; // 左下
    rt.anchorMax = Vector2.one;  // 右上
    rt.pivot = new Vector2(0.5f, 0.5f);
    
    // 将边距设为0，贴合父级
    rt.offsetMin = Vector2.zero; // Left, Bottom = 0
    rt.offsetMax = Vector2.zero; // Right, Top = 0
    // 或者: rt.sizeDelta = Vector2.zero; 
}
```

---

## 4. 坐标系转换神器：RectTransformUtility

不要自己算坐标！不要自己算坐标！不要自己算坐标！
Unity 提供了 `RectTransformUtility` 处理复杂的 Pivot 和 Canvas 缩放。

| API | 作用 | 典型场景 |
| :--- | :--- | :--- |
| `ScreenPointToLocalPointInRectangle` | 屏幕点 -> 局部点 | 鼠标点击 UI、物体飞向 UI |
| `WorldToScreenPoint` | 世界(UI) -> 屏幕 | UI 坐标转回屏幕 (跨 Canvas) |
| `ScreenPointToWorldPointInRectangle` | 屏幕点 -> 世界(UI) | 拖拽物体跟随鼠标 |
| `FlipLayoutOnAxis` | 翻转布局 | 镜像 UI |
| `PixelAdjustPoint` | 像素对齐 | 消除 UI 模糊 |

### 4.1 为什么需要 `Camera` 参数？
*   **Overlay Canvas:** 不需要 Camera（传 `null`），因为 UI 直接渲染在屏幕上。
*   **Camera Canvas:** 需要传入渲染该 Canvas 的摄像机 (`canvas.worldCamera`)，因为此时 UI 是 3D 世界的一部分，受透视影响。

---

## 5. 常见实战案例 (Cookbook)

### 5.1 案例 A: UI 元素始终位于屏幕右上角
*   **编辑器设置:**
    *   Anchors: Min(1,1), Max(1,1) (右上角点模式)
    *   Pivot: (1, 1) (自身的右上角)
    *   Pos: (0, 0)
*   **原理解析:**
    *   锚点定在父级右上角。
    *   自身轴心在右上角。
    *   位置偏移为0。
    *   结果：元素的右上角与父级右上角重合。

### 5.2 案例 B: 制作一个血条 (跟随 3D 物体)
这是一个极其高频的需求。

```csharp
public class HealthBarFollow : MonoBehaviour {
    public Transform target3D; // 3D 目标 (头顶)
    public RectTransform healthBarUI; // UI 元素
    public Canvas canvas; // 所在的 Canvas
    public Vector3 offset = new Vector3(0, 2.0f, 0); // 头顶偏移量

    void LateUpdate() {
        if (target3D == null) return;

        // 1. 3D 世界坐标 -> 屏幕坐标
        Vector3 screenPos = Camera.main.WorldToScreenPoint(target3D.position + offset);

        // 2. 屏幕坐标 -> UI 局部坐标
        // 处理 Canvas 缩放模式 (Scale With Screen Size) 的关键步骤
        Vector2 localPos;
        RectTransformUtility.ScreenPointToLocalPointInRectangle(
            canvas.transform as RectTransform, 
            screenPos, 
            canvas.worldCamera, // Overlay模式传null
            out localPos
        );

        // 3. 应用坐标
        healthBarUI.anchoredPosition = localPos;
    }
}
```

### 5.3 案例 C: 异形屏适配 (Safe Area)
处理 iPhone 刘海屏或挖孔屏。

```csharp
public class SafeAreaAdapter : MonoBehaviour {
    RectTransform panel;

    void Awake() {
        panel = GetComponent<RectTransform>();
        ApplySafeArea();
    }

    void ApplySafeArea() {
        Rect safeArea = Screen.safeArea;
        
        // 将 Safe Area 转换为归一化锚点 (0~1)
        Vector2 anchorMin = safeArea.position;
        Vector2 anchorMax = safeArea.position + safeArea.size;

        anchorMin.x /= Screen.width;
        anchorMin.y /= Screen.height;
        anchorMax.x /= Screen.width;
        anchorMax.y /= Screen.height;

        // 应用给全屏 Panel
        panel.anchorMin = anchorMin;
        panel.anchorMax = anchorMax;
    }
}
```

### 5.4 案例 D: 终极挑战——跨 Canvas 坐标同步
将一个 UI 元素（如物品栏里的图标）从 **Canvas A** 移动到 **Canvas B**，或者让 Canvas B 里的特效跟随 Canvas A 里的按钮。

**难点:**
*   Canvas A 可能是 `Screen Space - Overlay` (无 Camera)。
*   Canvas B 可能是 `Screen Space - Camera` (有 Camera, 且距离不同)。
*   两者的 `Scale Factor` 可能不同。

**通用解决方案:** 使用 **屏幕坐标 (Screen Space)** 作为绝对中介。

```csharp
/// <summary>
/// 将 sourceRect (在 sourceCanvas 下) 的中心点位置，转换为 targetCanvas 下的局部坐标
/// </summary>
public static Vector2 ConvertUiPosition(RectTransform sourceRect, Canvas sourceCanvas, RectTransform targetParent, Canvas targetCanvas) {
    // 1. 获取源 UI 的屏幕坐标
    Vector3 screenPos;
    Camera sourceCam = sourceCanvas.renderMode == RenderMode.ScreenSpaceOverlay ? null : sourceCanvas.worldCamera;
    
    // WorldToScreenPoint 处理了 Camera 模式下的透视和深度
    // 如果是 Overlay，sourceRect.position 本身就是屏幕像素坐标，但用此 API 更安全通用
    screenPos = RectTransformUtility.WorldToScreenPoint(sourceCam, sourceRect.position);

    // 2. 将屏幕坐标转为目标 Canvas 的局部坐标
    Vector2 localPos;
    Camera targetCam = targetCanvas.renderMode == RenderMode.ScreenSpaceOverlay ? null : targetCanvas.worldCamera;

    RectTransformUtility.ScreenPointToLocalPointInRectangle(
        targetParent, 
        screenPos, 
        targetCam, 
        out localPos
    );

    return localPos;
}

// 使用示例: 金币从背包(Overlay)飞到世界UI(Camera)
void Update() {
    Vector2 targetPos = ConvertUiPosition(inventoryIcon, inventoryCanvas, worldEffectContainer, worldCanvas);
    flyingCoin.anchoredPosition = Vector2.Lerp(flyingCoin.anchoredPosition, targetPos, Time.deltaTime * 5);
}
```

---

## 6. 性能优化 (Performance)

`RectTransform` 的变动（Re-layout）是非常昂贵的，它会触发布局系统的重建。

1.  **Canvas 分层:** 
    *   将**动态**元素（如血条、倒计时）和**静态**元素（如背景板、固定图标）放在**不同**的 Canvas (或 Sub-Canvas) 中。
    *   当一个 UI 元素变动时，同一个 Canvas 下的所有元素都可能需要重新生成网格。
2.  **少用 `LayoutGroup`:** 
    *   `VerticalLayoutGroup`, `GridLayoutGroup` 等自动布局组件性能开销大。
    *   如果是列表，务必使用 **对象池 (Object Pooling)** + **无限滚动 (Infinite Scroll)**，而不是实例化 100 个 Item。
3.  **Pixel Perfect:** 
    *   Canvas 上的 `Pixel Perfect` 选项会增加计算量，非像素风游戏通常不需要开启。

---

## 7. 速查表：我该用哪个属性？

| 我想改变... | 模式 | 使用属性 |
| :--- | :--- | :--- |
| **绝对位置** | 点模式 | `anchoredPosition` |
| **固定宽高** | 点模式 | `sizeDelta` |
| **贴边距离** | 拉伸模式 | `offsetMin` (左下), `offsetMax` (右上) |
| **全屏铺满** | 任意 | `anchorMin=0`, `anchorMax=1`, `offsetMin/Max=0` |
| **鼠标跟随** | 任意 | `RectTransformUtility.ScreenPointToLocalPointInRectangle` |
