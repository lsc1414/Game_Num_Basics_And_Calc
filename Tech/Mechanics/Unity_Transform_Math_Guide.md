# 📐 Unity Transform 数学变换与最佳实践 (The Math of Transform)

Transform 是 Unity 中最基础也最重要的组件，它定义了物体在空间中的**位置 (Position)**、**旋转 (Rotation)** 和 **缩放 (Scale)**。深刻理解其背后的线性代数原理，对于编写高性能、无 Bug 的代码至关重要。

---

## 1. 坐标空间 (Coordinate Spaces)

Unity 中存在多个嵌套的坐标系，理解它们之间的转换是所有变换的基础。

### 1.1 常用空间
*   **模型空间 (Local/Object Space):** 顶点相对于模型枢轴点 (Pivot) 的位置。
*   **世界空间 (World/Global Space):** 相对于游戏世界原点 (0,0,0) 的位置。
*   **观察空间 (View/Camera Space):** 相对于摄像机的位置。
*   **屏幕空间 (Screen Space):** 像素坐标 (x, y)，左下角为 (0,0)。
*   **视口空间 (Viewport Space):** 归一化屏幕坐标 (0~1)。

### 1.2 变换矩阵 (Transformation Matrix)
一个物体从模型空间变换到世界空间，本质上是乘以一个 $4 \times 4$ 矩阵 $M_{Local \to World}$。

$$ M = T \cdot R \cdot S $$

*   **顺序至关重要:** 先缩放 ($S$)，再旋转 ($R$)，最后平移 ($T$)。
*   **矩阵乘法不满足交换律:** $R \cdot T \neq T \cdot R$。如果顺序错了，物体会绕着世界原点旋转，而不是绕着自身旋转。

---

## 2. 旋转 (Rotation) —— 最大的坑

Unity 提供了三种方式来表示旋转，混用它们是 Bug 之源。

### 2.1 欧拉角 (Euler Angles) - `transform.eulerAngles`
*   **直观:** (x, y, z) 分别代表绕 X, Y, Z 轴旋转的角度。
*   **优点:** 人类易读，Inspector 面板里显示的就是这个。
*   **致命缺点:** **万向节死锁 (Gimbal Lock)**。当中间轴 (Y) 旋转 90 度时，X 轴和 Z 轴重合，失去一个自由度。
*   **最佳实践:** 仅在 UI 显示或简单的初始化设置时使用。**严禁**在 Update 中对欧拉角进行累加计算（如 `angles += speed * dt`）。

### 2.2 四元数 (Quaternion) - `transform.rotation`
*   **原理:** 复数扩展 $(x, y, z, w)$。
*   **优点:** 无死锁，插值平滑 (Slerp)，计算效率高。
*   **缺点:** 人类无法直观理解数值含义。
*   **常用 API:** 
    *   `Quaternion.Identity`: 无旋转。
    *   `Quaternion.Euler(x, y, z)`: 欧拉角 -> 四元数。
    *   `Quaternion.LookRotation(forward, up)`: 创建一个朝向 `forward` 的旋转。
    *   `Quaternion.Angle(q1, q2)`: 计算两个旋转间的夹角。

### 2.3 矩阵/向量法 (Vector Math)
*   **forward/up/right:** 直接操作轴向量。
*   **应用:** `transform.forward` 本质上是 `rotation * Vector3.forward`。

---

## 3. 空间变换 API 详解

### 3.1 点、向量与方向的区别
*   **Point (点):** 受位置、旋转、缩放影响。
    *   `TransformPoint()`: Local -> World
    *   `InverseTransformPoint()`: World -> Local
*   **Direction (方向):** **不受位置 (Translation) 影响**，受旋转影响。通常用于法线、速度方向。
    *   `TransformDirection()`: Local -> World
    *   `InverseTransformDirection()`: World -> Local
*   **Vector (向量):** 受旋转和**缩放**影响，不受位置影响。
    *   `TransformVector()`: Local -> World (带缩放)

### 3.3 特别篇：UI 坐标系转换 (The UI Coordinate Problem)
UI 系统 (`RectTransform`) 虽然继承自 Transform，但在坐标转换上有一个巨大的“断层”：**渲染模式 (Render Mode)**。

1.  **Screen Space - Overlay:** 
    *   UI 直接绘制在屏幕最上层。
    *   **没有世界坐标概念**（或者说，世界坐标 = 屏幕像素坐标）。
    *   `position.x` 就是屏幕上的像素 X。
    *   转换时**不需要** Camera 参数 (传 `null`)。

2.  **Screen Space - Camera / World Space:**
    *   UI 是 3D 世界中的实体板子，有确定的深度 (Z)。
    *   受透视 (Perspective) 影响：近大远小。
    *   转换时**必须**传入渲染该 Canvas 的 Camera，否则射线检测会偏离。

**核心理论:** 
在处理 UI 交互（如鼠标点击、物体飞向 UI）时，永远不要试图直接“加减坐标”。必须寻找一个**公共参考系**——通常是**屏幕空间 (Screen Space)**。
*   3D 世界 -> **屏幕** <- UI 局部
*   UI A -> **屏幕** <- UI B

---

### 3.2 最佳实践案例

#### 案例 A: 子弹发射位置
**错误:** `bullet.position = transform.position + new Vector3(0, 0, 1);`
**问题:** 只有当物体朝向世界 Z 轴且无缩放时才对。
**正确:** `bullet.position = transform.TransformPoint(new Vector3(0, 0, 1));`
**或者:** `bullet.position = transform.position + transform.forward * 1.0f;`

#### 案例 B: AI 相对坐标判断
判断 "敌人是否在我的右前方"。
**方法:** 将敌人坐标转换到我的局部空间。
```csharp
Vector3 localPos = transform.InverseTransformPoint(enemy.position);
if (localPos.z > 0 && localPos.x > 0) {
    // 在右前方 (Local Z是前, Local X是右)
}
```

#### 案例 C: 相对方向的力 (Relative Force)
一个物体向前发射一个力（例如玩家冲刺，冲刺方向是角色面向的方向）。
```csharp
// 错误: 会一直朝着世界Z轴方向冲刺
// rigidbody.AddForce(Vector3.forward * speed);

// 正确: 朝着物体的本地forward方向冲刺
rigidbody.AddForce(transform.forward * speed, ForceMode.Impulse); 
```

#### 案例 D: 旋转限制 (Rotation Constraint)
例如，摄像机绕着玩家旋转，但要保持摄像机 Y 轴始终指向世界 Y 轴（不倾斜）。
```csharp
// 错误: 简单LookAt会使摄像机Z轴指向玩家，但可能会倾斜
// transform.LookAt(player.position);

// 正确: 创建一个只在Y轴旋转的LookRotation
Vector3 directionToPlayer = player.position - transform.position;
Quaternion targetRotation = Quaternion.LookRotation(directionToPlayer, Vector3.up); // Vector3.up 强制Y轴向上
transform.rotation = Quaternion.Slerp(transform.rotation, targetRotation, Time.deltaTime * rotationSpeed);
```

#### 案例 E: 屏幕坐标到世界坐标 (Screen to World)
例如，点击屏幕发射射线或生成物体。
```csharp
// 1. 鼠标点击的屏幕坐标
Vector3 screenPos = Input.mousePosition;

// 2. 转换为世界坐标 (需要深度)
// 如果已知Z轴距离：
Vector3 worldPos = Camera.main.ScreenToWorldPoint(new Vector3(screenPos.x, screenPos.y, distanceToCamera));

// 如果需要射线检测 (更常见):
Ray ray = Camera.main.ScreenPointToRay(screenPos);
if (Physics.Raycast(ray, out RaycastHit hit)) {
    Debug.Log("Clicked at world position: " + hit.point);
    // 在 hit.point 位置生成物体
}
```

#### 案例 F: 绕点旋转 (Rotate Around Point)
让一个物体（如卫星、僚机）绕着另一个点（如行星、玩家）旋转。
```csharp
// 假设 this.transform 是卫星，targetTransform 是行星
// point: 旋转的中心点
Vector3 point = targetTransform.position; 
// axis: 旋转轴 (通常是Vector3.up，即绕Y轴)
Vector3 axis = Vector3.up; 
// angle: 每帧旋转的角度
float rotationSpeed = 50f; // 度/秒
float angle = rotationSpeed * Time.deltaTime;

transform.RotateAround(point, axis, angle);
```

#### 案例 G: 平滑 LookAt (Smooth LookAt)
让物体平滑地转向目标，而不是瞬时旋转。这对于摄像机跟随、炮塔转动等场景非常重要。
```csharp
// 假设 target 是要看向的目标
Vector3 directionToTarget = target.position - transform.position;
// 计算目标旋转，强制只在Y轴旋转，避免X/Z轴倾斜
Quaternion targetRotation = Quaternion.LookRotation(directionToTarget, Vector3.up);

// 使用 Slerp (球面线性插值) 或 RotateTowards 平滑过渡
float rotationSpeed = 5f; // 旋转速度
transform.rotation = Quaternion.Slerp(transform.rotation, targetRotation, Time.deltaTime * rotationSpeed);

// 或者使用 RotateTowards (更精确控制最大转角)
// float maxDegreesDelta = rotationSpeed * Time.deltaTime * 100f; // 假设每秒转100度
// transform.rotation = Quaternion.RotateTowards(transform.rotation, targetRotation, maxDegreesDelta);
```

#### 案例 H: 平滑移动 (Smooth Movement)
让物体平滑地移动到目标位置。
```csharp
// 假设 targetPos 是要移动到的目标位置
Vector3 targetPos = new Vector3(10, 0, 0); 
float moveSpeed = 5f; // 移动速度

// MoveTowards: 以恒定速度移动到目标，不会超过目标
transform.position = Vector3.MoveTowards(transform.position, targetPos, moveSpeed * Time.deltaTime);

// Lerp (线性插值): 每次移动目标和当前位置之间的一部分，越接近目标越慢
// float lerpFactor = 0.1f; // 每次移动当前距离的10%
// transform.position = Vector3.Lerp(transform.position, targetPos, lerpFactor);
```

#### 案例 I: 3D物体飞向UI (World Object to UI Fly Effect) - 进阶版
经典需求：怪物掉落金币（世界坐标），金币拾取后飞向 UI 上的金币栏（屏幕坐标）。
**初级陷阱:** 直接用 `position` 赋值，在不同分辨率或 UI 锚点设置下会偏移。
**核心原理:** 使用 `RectTransformUtility` 将屏幕坐标转换为**局部 UI 坐标**。

```csharp
// 场景假设：
// 1. worldCoin: 掉落在地上的金币 (3D)
// 2. uiGoldIcon: UI上的金币图标 (RectTransform, 可能有各种 Anchor 设置)
// 3. uiCoinPrefab: 飞行特效预制体 (UI元素)
// 4. effectsCanvas: 专门用于播放特效的 Canvas (Overlay 或 Camera 模式)

public void PlayCoinFlyEffect(Transform worldCoin) {
    // --- 第一步：确定起点 (World -> Screen -> Local UI) ---
    Vector3 screenPos = Camera.main.WorldToScreenPoint(worldCoin.position);
    
    // 将屏幕坐标转换为 effectsCanvas 下的局部坐标
    // 这样无论 Canvas 缩放模式如何，都能保证位置正确
    RectTransformUtility.ScreenPointToLocalPointInRectangle(
        (RectTransform)effectsCanvas.transform, 
        screenPos, 
        effectsCanvas.worldCamera, // 如果是 Overlay 模式，这里传 null
        out Vector2 startLocalPos
    );

    // --- 第二步：确定终点 (Target UI -> Screen -> Local UI) ---
    // 即使 uiGoldIcon 在另一个 Canvas 且有复杂的锚点，
    // 我们也先转成通用的屏幕坐标，再转回 effectsCanvas 的局部坐标
    
    // 1. 获取目标在屏幕上的绝对位置 (处理跨 Canvas 的关键)
    // 注意: 如果目标 UI 是 Overlay 模式，worldCamera 传 null
    Vector3 targetWorldPos = uiGoldIcon.position; 
    Vector2 targetScreenPos = RectTransformUtility.WorldToScreenPoint(
        uiGoldIconCanvas.worldCamera, 
        targetWorldPos
    );

    // 2. 转回特效层的局部坐标
    RectTransformUtility.ScreenPointToLocalPointInRectangle(
        (RectTransform)effectsCanvas.transform,
        targetScreenPos,
        effectsCanvas.worldCamera,
        out Vector2 endLocalPos
    );

    // --- 第三步：生成并飞行 ---
    GameObject flyingCoin = Instantiate(uiCoinPrefab, effectsCanvas.transform);
    RectTransform flyRect = flyingCoin.GetComponent<RectTransform>();
    
    // 重要: 重置锚点为中心，避免父级锚点影响
    flyRect.anchoredPosition = startLocalPos;
    flyRect.anchorMin = new Vector2(0.5f, 0.5f);
    flyRect.anchorMax = new Vector2(0.5f, 0.5f);
    flyRect.pivot = new Vector2(0.5f, 0.5f);

    StartCoroutine(FlyToTarget(flyRect, endLocalPos));
}

IEnumerator FlyToTarget(RectTransform coin, Vector2 targetPos) {
    // 使用 anchoredPosition 进行移动，保证在 UI 坐标系内的正确性
    float duration = 0.6f;
    float elapsed = 0;
    Vector2 startPos = coin.anchoredPosition;

    while (elapsed < duration) {
        elapsed += Time.deltaTime;
        float t = elapsed / duration;
        t = t * t * (3f - 2f * t); // SmoothStep
        
        coin.anchoredPosition = Vector2.Lerp(startPos, targetPos, t);
        yield return null;
    }
    
    Destroy(coin.gameObject);
    // AddGold();
}
```
**总结:** 解决 UI 坐标乱飞的终极法宝是 **"屏幕坐标 (Screen Point)" 作为中转站**，配合 `RectTransformUtility.ScreenPointToLocalPointInRectangle`。

> 💡 **深入学习 UI 数学:** 关于 Anchors、Pivot、SizeDelta 的深层原理及更多 UI 适配技巧，请参阅专门文档：
> **[Unity RectTransform 深度解析 (The Math of UI)](./Unity_RectTransform_DeepDive.md)**

---

## 4. 核心向量数学与几何直觉 (Vector Math Intuition)

在 Gameplay 编程中，理解向量的点乘和叉乘比记住公式更重要。它们是战斗逻辑（如视野、判定）的数学基石。

### 4.1 点积 (Dot Product) - `Vector3.Dot(A, B)`
*   **数学定义:** $|A||B|\cos\theta$
*   **几何意义:** 衡量两个向量的方向**相似程度**，或者向量 A 在向量 B 上的**投影长度**。
*   **应用场景:** 
    1.  **视野检测 (FOV):** 判断敌人是否在玩家前方夹角内。
        ```csharp
        Vector3 toEnemy = (enemy.position - transform.position).normalized;
        // Dot > 0.5f 大约意味着在前方 60度范围内 (cos(60)=0.5)
        // Dot > 0 在前方 180度范围内
        if (Vector3.Dot(transform.forward, toEnemy) > 0.5f) { /* 在视野内 */ }
        ```
    2.  **背刺判定 (Backstab):** 判断攻击是否来自敌人背后。
        *   如果 `Dot(enemy.forward, player.forward) > 0.8`，说明两人朝向基本一致，是背后攻击。
    3.  **光照计算:** 漫反射计算中，光线方向与法线的点积决定亮度。

### 4.2 叉积 (Cross Product) - `Vector3.Cross(A, B)`
*   **数学定义:** 生成一个同时垂直于 A 和 B 的新向量（法向量）。遵守右手定则。
*   **几何意义:** 确定两个向量构成的**平面**及其**法线**。
*   **应用场景:** 
    1.  **左右判断:** 判断敌人在我的左边还是右边。
        ```csharp
        Vector3 toEnemy = enemy.position - transform.position;
        Vector3 cross = Vector3.Cross(transform.forward, toEnemy);
        // 在 Unity (左手坐标系) 中:
        // cross.y > 0通常在右侧, cross.y < 0在左侧 (取决于具体轴向设定)
        ```
    2.  **构建坐标系:** 已知 Forward 和 Up，求 Right。
        *   `Right = Cross(Up, Forward)` (注意顺序影响方向)

---

## 5. 矩阵的“基向量”视角 (Basis Vectors)

不要把变换矩阵看作一堆枯燥的数字。4x4 矩阵的前三列，实际上就是该物体局部坐标轴在**世界空间**中的表示。

$$
\begin{bmatrix}
\color{red}{R_x} & \color{green}{U_x} & \color{blue}{F_x} & T_x \\
\color{red}{R_y} & \color{green}{U_y} & \color{blue}{F_y} & T_y \\
\color{red}{R_z} & \color{green}{U_z} & \color{blue}{F_z} & T_z \\
0 & 0 & 0 & 1
\end{bmatrix}
$$

*   **第一列 (Red):** 物体的 `transform.right` (局部 X 轴)
*   **第二列 (Green):** 物体的 `transform.up` (局部 Y 轴)
*   **第三列 (Blue):** 物体的 `transform.forward` (局部 Z 轴)
*   **第四列:** 物体的 `transform.position` (位移)

**深刻理解:** 旋转一个物体，本质上就是定义这三个基向量（Right, Up, Forward）指向哪里。

---

## 6. 物理与变换的冲突 (Physics vs Transform)

这是一个极易被忽视的理论陷阱。

*   **现象:** 直接修改带 `Rigidbody` 或 `Collider` 物体的 `transform.position`。
*   **理论后果 (Teleportation):** 
    *   物理引擎认为物体是**瞬移**过去的，速度为 0。
    *   **穿墙 (Tunneling):** 这一帧在墙前，下一帧在墙后，中间没有检测到碰撞。
    *   **破坏插值:** 导致刚体运动卡顿或抖动。
*   **正确做法:** 
    *   **瞬移:** 使用 `rigidbody.position = newPos` (类似 transform 但通知物理引擎)。
    *   **移动:** 使用 `rigidbody.MovePosition(newPos)` (平滑移动，会与沿途物体碰撞)。
    *   **施力:** 使用 `rigidbody.AddForce()`。

---

## 7. 层级关系 (Hierarchy) 与性能

### 7.1 肮脏标记 (Dirty Flag)
Unity 的 Transform 系统使用“肮脏标记”模式。
*   当你修改父物体的 Transform 时，所有子物体并不会立即重新计算世界坐标。
*   它们会被标记为 `Dirty`。
*   只有当你下次访问子物体的 `.position` 或 `.rotation` 时，才会触发递归计算 (Recursion)。

### 7.2 性能陷阱
*   **深度层级:** 层级越深，计算开销越大。
*   **频繁读写:** 在一帧内反复读取 `position` 会强制重算。
    *   *Bad:* `for(i) { x += transform.position.x; }`
    *   *Good:* `Vector3 pos = transform.position; for(i) { x += pos.x; }`
*   **缩放 (Scale):** 尽量保持 Scale 为 (1,1,1)。非统一缩放 (Non-uniform scale) 会导致物理引擎计算复杂化，并破坏批处理 (Batching)。

### 7.3 `transform.hasChanged`
*   **用途:** 极其高效地检查物体自上一帧以来是否移动过。
*   **场景:** 只有当物体移动时，才更新空间索引 (Grid/QuadTree)。
    ```csharp
    if (transform.hasChanged) {
        UpdateSpatialGrid();
        transform.hasChanged = false; // 必须手动重置
    }
    ```

---

## 8. 数学变换速查表 (Cheat Sheet)

| 需求 | 公式/API |
| :--- | :--- |
| **物体 A 朝向物体 B** | `transform.rotation = Quaternion.LookRotation(B.pos - A.pos);` |
| **平滑旋转向目标** | `transform.rotation = Quaternion.RotateTowards(current, target, speed * dt);` |
| **获取 B 在 A 坐标系下的位置** | `Vector3 localPos = A.InverseTransformPoint(B.position);` |
| **绕某个点 P 旋转** | `transform.RotateAround(P, axis, angle);` |
| **计算距离 (不开方)** | `(A - B).sqrMagnitude` (用于比较距离，性能优于 `.distance`) |
| **将向量投影到平面** | `Vector3.ProjectOnPlane(vector, planeNormal);` |
| **向量反射 (子弹反弹)** | `Vector3.Reflect(velocity, wallNormal);` |
| **检查是否在前方 (视野)** | `Vector3.Dot(transform.forward, (target - me).normalized) > 0` |
| **检查在左还是右** | `Vector3.Cross(transform.forward, targetDir).y` (>0 右, <0 左) |
| **两向量夹角** | `Vector3.Angle(dirA, dirB);` (返回 0~180 度) |
| **世界坐标转屏幕坐标** | `Camera.main.WorldToScreenPoint(worldPos)` |
| **屏幕坐标转世界 (带深度)** | `Camera.main.ScreenToWorldPoint(new Vector3(x, y, depth))` |

<script type="text/javascript" id="MathJax-script" async
  src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js">
</script>
<script>
  MathJax = {
    tex: {
      inlineMath: [['$', '$'], ['\\(', '\\)']]
    }
  };
</script>