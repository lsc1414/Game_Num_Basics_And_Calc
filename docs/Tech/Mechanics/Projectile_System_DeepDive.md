---
sidebarTitle: "🏹 投射物系统深度解析"
---

# 🏹 投射物系统深度解析

本文档旨在构建一个**通用、高性能、高扩展性**的投射物系统理论框架。
在 Project Vampirefall 中，投射物（Projectiles）是塔防与战斗的核心交互载体。与 Hitscan（射线判定）不同，投射物拥有**飞行时间 (Travel Time)**、**独立轨迹**和**物理交互**。

---

## 1. 核心分类与定义 (Taxonomy)

### 1.1 逻辑分层
投射物不应该是一个简单的 `MonoBehaviour`，它应包含两个分离的层：

1.  **逻辑层 (Data/Simulation):** 处理位置、速度、碰撞检测、生命周期。为了性能，通常由 `ProjectileManager` 统一驱动（ECS 或 Struct-based）。
2.  **表现层 (View/Rendering):** 处理模型渲染、拖尾特效 (Trail)、粒子系统。只负责“跟随”逻辑层的位置。

### 1.2 运动模式 (Movement Types)

|          类型          |          描述          |          适用场景          |          数学模型          |
|          :---          |          :---          |          :---          |          :---          |
|          **直射 (Linear)**          |          沿直线匀速/变速飞行。          |          箭矢、子弹、激光束。          |          $P = P_0 + V \cdot t$          |
|          **抛射 (Lobbed)**          |          受重力影响，呈抛物线。          |          迫击炮、手雷、投石车。          |          $y = v_{0y}t - \frac{1}{2}gt^2$          |
|          **追踪 (Homing)**          |          动态调整速度向量指向目标。          |          魔法飞弹、制导导弹。          |          Steering Behavior (操纵行为)          |
|          **贝塞尔 (Bezier)**          |          沿预计算的曲线飞行，无物理模拟。          |          华丽的技能弹道、回旋镖。          |          Bezier Curve Interpolation          |
|          **环绕 (Orbital)**          |          围绕宿主或定点旋转。          |          护盾球、环绕法球。          |          Polar Coordinates (极坐标)          |
|          **垂直发射 (Javelin)**          |          先垂直升空，再转为追踪。          |          标枪导弹 (Javelin)、天降正义。          |          State Machine (Ascend -> Lock -> Homing)          |

---

## 2. 弹道数学与实现 (Trajectory Mathematics)

### 2.1 抛物线弹道 (Parabolic Arc)
给定起点 $S$、终点 $E$和飞行时间$T$（或高度 $H$），如何计算初速度 $V_0$？

**公式推导 (基于时间 $T$):**

1.  **水平速度:** $V_x = (E.x - S.x) / T$, $V_z = (E.z - S.z) / T$
2.  **垂直速度:** $V_y = (E.y - S.y - 0.5 \cdot g \cdot T^2) / T$(注意重力$g$通常为负值，公式中$g$取$-9.8$)

**代码片段:**
```csharp
public Vector3 CalculateLobVelocity(Vector3 start, Vector3 end, float time)
{
    Vector3 distance = end - start;
    Vector3 distanceXZ = distance;
    distanceXZ.y = 0;

    float sY = distance.y;
    float sXZ = distanceXZ.magnitude;

    float Vxz = sXZ / time;
    float Vy = (sY / time) + (0.5f * Mathf.Abs(Physics.gravity.y) * time);

    Vector3 result = distanceXZ.normalized;
    result *= Vxz;
    result.y = Vy;

    return result;
}
```

### 2.2 追踪算法 (Homing Logic)
简单的 `LookAt` 会导致导弹像苍蝇一样抽搐。优秀的追踪需要**转弯速度限制 (Turn Rate Limit)**。

**实现步骤:**

1.  计算理想速度向量: `DesiredVelocity = (TargetPos - CurrentPos).normalized * Speed`
2.  计算转向力: `Steering = DesiredVelocity - CurrentVelocity`

3.  限制转向力: `Steering = Vector3.ClampMagnitude(Steering, TurnRate * dt)`

4.  应用速度: `CurrentVelocity += Steering`

#### 2.2.1 旋转数学 (Rotation Math)
为了让导弹平滑转向目标，我们应使用四元数 (Quaternion)。

*   **Slerp:** `Quaternion.Slerp(currentRot, targetRot, turnSpeed * dt)`。适合平滑插值，但在大角度转向时可能不够直接。
*   **RotateTowards:** `Quaternion.RotateTowards(currentRot, targetRot, maxDegreesDelta)`。更精确地控制每帧最大转角，适合模拟导弹的机械限制。

### 2.3 高级预判算法 (Advanced Prediction)
**预瞄准理论 (Lead Aiming):**

*   目标位置 $P_T$，目标速度 $V_T$，子弹速度 $S_B$，子弹位置 $P_B$。
*   我们需要找到一个时间 $t$，使得 $Distance(P_B, P_T + V_T \cdot t) = S_B \cdot t$。
*   这转化为解方程：$| (P_T - P_B) + V_T \cdot t |^2 = (S_B \cdot t)^2$。
*   求解 $t$后，预测点$P_{Aim} = P_T + V_T \cdot t$。

**迭代求解 (Iterative Solver):**
当目标不是匀速直线运动（例如在做圆周运动或变速运动），解析解变得极其复杂。此时应使用迭代法：

1.  假设碰撞时间 $t_0 = Distance / Speed$。
2.  预测 $t_0$后的目标位置$P_1$。

3.  更新碰撞时间 $t_1 = Distance(Start, P_1) / Speed$。

4.  重复步骤 2-3，直到 $t_n - t_{n-1}$ 小于阈值。通常 3-5 次迭代即可获得极高精度。

### 2.4 物理模拟进阶 (Advanced Physics)
为了追求更真实或特殊的手感，我们需要引入空气动力学。

#### 空气阻力 (Drag)
真空中的抛物线是完美的对称图形，但在游戏中这看起来可能很“飘”。

*   **模型:** $F_d = -k \cdot v^2$ (阻力与速度平方成正比，方向相反)。
*   **效果:** 投射物会有一个“终端速度”，且下落轨迹比上升轨迹更垂直。

#### 数值积分 (Integration)
*   **Explicit Euler:** `Pos += Vel * dt; Vel += Acc * dt;` 简单但误差大，不推荐用于长距离高精度弹道。
*   **Velocity Verlet:** 能量守恒性更好，弹道更稳定。
    ```csharp
    Pos += Vel * dt + 0.5 * Acc * dt * dt;
    NewAcc = ComputeForces(Pos, Vel);
    Vel += 0.5 * (Acc + NewAcc) * dt;
    ```

---

## 3. 交互机制 (Interaction Mechanics)

当投射物检测到碰撞后，不仅是造成伤害，还可以触发复杂的后续行为。

### 3.1 穿透 (Piercing / Passthrough)
*   **逻辑:** 投射物击中敌人后不销毁，而是扣减 `PierceCount` 并继续飞行。
*   **关键痛点:** **霰弹枪效应 (Shotgunning)**。
    *   *问题:* 如果一帧内检测多次（射线步进），或者投射物体积很大，可能会在同一帧对同一敌人触发多次伤害。
    *   *解决:* 每个投射物维护一个 `List<int> hitInstanceIDs`。击中时检查 ID，若已存在则跳过。

### 3.2 弹射 (Ricochet / Bounce)
*   **逻辑:** 击中障碍物或敌人后，改变方向继续飞行。
*   **物理反射:**
    *   公式: $R = I - 2(I \cdot N)N$
    *   $I$: 入射向量 (Velocity.normalized)
    *   $N$: 碰撞面法线 (HitInfo.normal)
*   **智能弹射 (Chain/Smart Bounce):**
    *   *场景:* 闪电链，希维尔的弹射。
    *   *逻辑:* 不遵循物理反射。以命中点为中心，`OverlapSphere` 寻找最近的、未被击中过的敌人作为下一个目标方向。

### 3.3 垂直发射追踪 (Javelin Style)
这是一种两阶段弹道，常用于“攻顶”导弹。

**逻辑流程:**

1.  **升空阶段 (Ascend Phase):**
    *   给一个初始向上的速度 `Vector3.up * LaunchForce`。
    *   施加较小的重力或甚至反重力，使其快速爬升到指定高度（如 20米）。
    *   在此阶段忽略目标位置，纯粹向上。
2.  **巡航/下落阶段 (Cruise/Descend Phase):**

    *   当到达最高点或飞行时间 > $t_1$。
    *   开启 **Homing Logic**。
    *   设置极高的 `TurnRate`（或者直接 `Slerp` 旋转），让导弹头朝下对准目标。
    *   重力恢复正常，利用重力加速下落。

---

## 4. 碰撞检测方案 (Collision Detection)

在高性能要求下（同屏 1000+ 弹幕），不能给每个子弹挂 `Rigidbody` + `Collider`。

### 4.1 射线步进 (Raycast Step) —— *推荐标准*
*   **原理:** 每一帧，从“上一帧位置”向“当前帧位置”发射射线。
*   **公式:** `Physics.Raycast(prevPos, (currPos - prevPos).normalized, dist)`
*   **优点:** 
    *   **防穿模 (Anti-Tunneling):** 即使速度极快，射线也会覆盖整个路径，不会穿墙。
    *   **性能:** 比 Collider 物理引擎开销小得多。
*   **缺点:** 射线没有体积（对于很细的射线，可能穿过怪物的缝隙）。

### 4.2 球形步进 (SphereCast Step) —— *高宽容度*
*   **原理:** 同上，但使用 `Physics.SphereCast`。
*   **适用:** 炮弹、火球等大体积投射物。给予玩家更宽松的命中判定。

### 4.3 胶囊体步进 (CapsuleCast Step) —— *长条物体*
*   **适用:** 长矛、光剑、箭矢。
*   **原理:** `Physics.CapsuleCast`。相比射线，它有一个“粗细”；相比球体，它能更好地模拟长条物体的体积，避免“箭身”穿过敌人却没判定的情况。

### 4.4 延迟补偿 (Lag Compensation) - *网络同步*
虽然本项目偏单机，但若涉及联机，需理解：

*   服务器在判定命中时，会将所有敌人的位置“回滚”到客户端发射子弹的那个时间戳（Ping值前）。
*   这就是为什么你在本地看到打中了，服务器也认可打中了，即使现在敌人已经跑开了。

---

## 5. 性能架构设计 (Performance Architecture)

### 5.1 投射物管理器 (Projectile Manager)
不要让每个 Bullet 都有 `Update()`。

```csharp
public struct ProjectileData {
    public Vector3 position;
    public Vector3 velocity;
    public float gravityScale;
    public int pierceCount;
    public int targetMask;
    // ...
}

public class ProjectileManager : MonoBehaviour {
    private ProjectileData[] _projectiles; // 或 NativeArray
    private int _activeCount;

    void Update() {
        // 1. 批量更新位置 (Simulate Physics)
        for (int i = 0; i < _activeCount; i++) {
            UpdateProjectile(ref _projectiles[i], Time.deltaTime);
        }
        // 2. 批量处理碰撞 (Collision Query)
        // 3. 批量更新渲染实例 (GPU Instancing / Matrix List)
    }
}
```

### 5.2 对象池 (Object Pooling)
*   **必须:** 投射物的产生和销毁极其频繁。
*   **策略:** 
    *   逻辑数据池 (`ProjectileData`)
    *   视觉表现池 (`GameObject` 或 `VFX`)
    *   当逻辑结束时，回收视觉对象。注意处理 Trail Renderer 的拖尾残留问题（需调用 `Clear()`）。

---

## 6. 总结与最佳实践 (Best Practices)

1.  **分离逻辑与表现:** 永远不要让渲染卡顿影响子弹的判定。逻辑层可以跑在 FixedUpdate 或独立线程。
2.  **防穿模是底线:** 对于高速投射物，必须使用射线步进，严禁仅使用 `OnTriggerEnter`。

3.  **智能优于真实:** 塔防游戏中，如果箭矢因为物理反弹飞出地图是很糟糕的体验。优先使用智能弹射（必中下一个怪）。

4.  **性能分级:** 

    *   **Hero Projectiles:** 可以用粒子、模型、SphereCast。
    *   **Minion Projectiles:** 使用 Billboard 面片、Raycast。
    *   **Massive Projectiles:** 使用 GPU Instancing + 纯距离判定。

---
