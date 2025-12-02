# 🧭 NavMesh 寻路与状态控制指南 (NavMesh Pathfinding & CC Interaction)

本文档详细阐述 Project Vampirefall 中敌人如何利用 Unity NavMesh 系统进行寻路，重点解析**异常状态 (CC)** 下的寻路控制，以及**动态阻挡 (塔防)** 的实现细节。

---

## 1. 核心组件架构 (Core Components)

在 Unity 中，寻路不仅仅是 `SetDestination`。对于复杂的 ARPG + TD 游戏，我们需要精细控制 `NavMeshAgent`。

### 1.1 Agent 配置的最佳实践
*   **Acceleration (加速度):** 设为极高 (如 60-100)。防止怪物起步“滑步”或转弯“漂移”。我们需要响应灵敏的移动。
*   **Angular Speed (转速):** 设为 360 或更高。怪物应该能瞬间转身，而不是像坦克一样慢慢转。
*   **Auto Braking (自动刹车):** 
    *   **近战怪:** `True`。防止冲过头。
    *   **远程怪:** `False`。它们需要平滑地移动到射程边缘并停止。
*   **Avoidance Priority (避让优先级):**
    *   **Boss/Elite:** 0-20 (优先级高，推着别人走)。
    *   **Minion:** 50-99 (优先级低，会被挤开)。
    *   *技巧:* 动态调整优先级。当怪物进入攻击状态时，提高优先级，防止被路过的队友挤歪。

---

## 2. 状态控制与寻路交互 (CC & Pathfinding)

这是 ARPG 开发中最容易出 Bug 的地方：如何让 `NavMeshAgent` 正确响应“冰冻”、“击退”等物理效果？

### ❄️ 2.1 减速 (Slow)
*   **实现:** 直接修改 `agent.speed`。
*   **叠加规则:** 
    *   建议使用 **乘法叠加**：`FinalSpeed = BaseSpeed * (1 - SlowA) * (1 - SlowB)`。
    *   设置下限：`Mathf.Max(FinalSpeed, 0.5f)`，防止速度减为 0 导致动画播放异常。

### 🧊 2.2 定身/冰冻 (Root / Freeze)
*   **错误做法:** `agent.enabled = false`。这会导致怪物失去碰撞体积，或者瞬间重置路径。
*   **正确做法:** `agent.isStopped = true`。
    *   保留路径数据 (Path Pending)，只是暂停移动。
    *   同时禁用 `Animator` 的移动参数，防止原地太空步。
*   **恢复:** `agent.isStopped = false`。

### 💫 2.3 眩晕 (Stun)
*   **区别:** 定身时怪物还能攻击/转头，眩晕时完全瘫痪。
*   **实现:**
    1.  `agent.isStopped = true`。
    2.  `agent.updateRotation = false` (禁止转头)。
    3.  逻辑层禁用 AI 状态机 (`FSM.Pause()`)。

### 🥊 2.4 击退 (Knockback) —— *最难点*
`NavMeshAgent` 和 `Rigidbody` 是死对头。Agent 试图吸附在地面，Rigidbody 试图飞出去。

*   **标准流程:**
    1.  **Disable Agent:** `agent.enabled = false` (必须彻底关掉，否则它会强制把坐标拉回 NavMesh 上)。
    2.  **Add Force:** `rb.isKinematic = false`; `rb.AddForce(ExplosionForce)`.
    3.  **Wait:** 等待击退时间（如 0.5秒）或等待速度接近 0。
    4.  **Re-enable Agent:** 
        *   `rb.isKinematic = true`.
        *   `agent.Warp(transform.position)` (关键！告诉 Agent 我瞬移到了新位置).
        *   `agent.enabled = true`.
        *   `agent.SetDestination(Target)` (重新寻路).

---

## 3. 实用案例大全 (Practical Use Cases)

### ⚔️ Case A: 到达攻击距离 (Reaching Attack Range)
当怪物进入射程时，如何优雅地停下来攻击，而不是推着玩家走？

*   **核心逻辑:** 不要依赖 `StoppingDistance`，自己手动控制。
*   **流程:**
    1.  **Check:** 每帧检测 `Distance(Self, Target) <= AttackRange`。
    2.  **Stop:** 满足条件时，立即 `agent.isStopped = true`。
    3.  **Rotate:** 攻击时手动调用 `transform.LookAt(Target)` (或者插值旋转)，保证朝向正确。
    4.  **Resume:** 如果目标跑出射程 `Distance > AttackRange * 1.2` (迟滞阈值)，则 `agent.isStopped = false` 继续追击。

#### 体积修正 (Size Adjustment)
在塔防中，塔通常有很大的碰撞体积（如 `Radius = 2.0m`），而小怪只有 `Radius = 0.5m`。直接计算 `Vector3.Distance` (中心点距离) 会导致小怪贴着塔站，或者打不到塔。

*   **公式修正:** `EffectiveRange = AttackRange + TargetRadius + SelfRadius`。
    *   **Center-to-Center:** 默认距离计算是中心对中心。
    *   **Edge-to-Edge:** 我们希望的是“边缘对边缘”。
    *   通过加上双方半径，我们算出的是“为了让武器碰到对方边缘，两个中心点需要的最大距离”。
*   **近战判定:**
    *   对于近战攻击，**不需要**真实的物理碰撞（武器碰到塔）。
    *   **Hitbox Lag:** 依赖物理碰撞会导致因为动画延迟、帧率波动而造成的判定丢失。
    *   **最佳实践:** 只要在 `AttackAnimation` 的关键帧 (Impact Frame) 触发时，检测 `Distance <= EffectiveRange` 即可判定伤害。这是最稳定、手感最好的做法。

### 🧱 Case B: 动态阻挡与堵路检测 (Dynamic Blocking)
在塔防模式下，玩家放塔不能把怪物的路彻底堵死 (Maze Blocking Rule)。

*   **组件:** 塔预制体上挂 `NavMeshObstacle`。
*   **设置:** `Carve = true` (必须勾选，否则怪物会穿过去或被挤开，而不是绕路)。
*   **放置前检测算法:**
    1.  虚拟放置一个 Obstacle (不显示，只参与计算)。
    2.  调用 `NavMesh.CalculatePath(SpawnPoint, NexusPoint, AreaMask, pathResult)`。
    3.  检查 `pathResult.status == NavMeshPathStatus.PathComplete`。
    4.  如果是 `Partial` 或 `Invalid`，说明路被堵死了，禁止玩家建造。

### 🕷️ Case C: 爬墙/跳跃 (Off-Mesh Links)
让怪物像蜘蛛一样翻越城墙，或者跳过沟壑。

*   **场景:** 僵尸从地面跳上 2楼平台攻击玩家。
*   **实现:**
    1.  在地图关键连接点放置 `OffMeshLink` 组件。
    2.  当 Agent 走到 Link 入口时，`agent.isOnOffMeshLink` 变为 `true`。
    3.  **接管控制:** 
        *   `agent.autoTraverseOffMeshLink = false` (禁止自动瞬移)。
        *   播放“跳跃”动画。
        *   使用 `Coroutine` 平滑移动 Agent 的 `transform` 到 Link 的另一端。
        *   到达后，`agent.CompleteOffMeshLink()`，交还控制权。

### 🎭 Case D: 游击/风筝 (Kiting)
弓箭手不仅要追玩家，还要保持距离。

*   **笨办法:** 只要距离 < 5米，就向后跑。容易卡墙角。
*   **NavMesh 办法 (SamplePosition):**
    1.  计算反向向量: `Dir = (SelfPos - TargetPos).normalized`.
    2.  目标点: `FleePos = SelfPos + Dir * 5.0f`.
    3.  **采样有效性:** `NavMesh.SamplePosition(FleePos, out hit, 2.0f, AreaMask)`.
    4.  如果采样成功，`SetDestination(hit.position)`。
    5.  如果采样失败（背后是墙），则向侧面寻找向量（叉乘）重试。

### 🐜 Case E: 拥挤处理 (Crowd Separation)
几百个僵尸挤在一起，互相推挤导致卡顿。

*   **RVO (Reciprocal Velocity Obstacles):** Unity 内置的避障。
    *   *缺点:* 消耗 CPU，且容易让怪物看起来像醉汉乱晃。
*   **优化方案:**
    1.  **降低 RVO Quality:** 在 Project Settings 里把 Agent 的避障质量调低。
    2.  **关闭部分 RVO:** 只有前排怪物开启 Obstacle Avoidance，后排怪物关闭（反正它们只要跟着前排走）。
    3.  **流场 (Flow Field) 替代:** 如果同屏超过 200 个单位，**放弃 NavMeshAgent**。
        *   使用 `NavMesh.CalculatePath` 算出一口路径。
        *   所有怪物只根据路径上的“向量场”移动 `transform.Translate`。
        *   仅在攻击最后阶段启用 Agent 进行精确定位。

---

## 4. 代码片段：安全的击退处理

```csharp
public class NavMeshMovement : MonoBehaviour
{
    [SerializeField] private NavMeshAgent _agent;
    [SerializeField] private Rigidbody _rb;

    // 协程：处理击退
    public IEnumerator ApplyKnockback(Vector3 force, float duration)
    {
        // 1. 切断 NavMesh 连接
        _agent.isStopped = true; // 先停逻辑
        _agent.enabled = false;  // 再关组件 (重要顺序)
        _rb.isKinematic = false; // 开启物理

        // 2. 施加力
        _rb.AddForce(force, ForceMode.Impulse);

        // 3. 等待物理模拟
        yield return new WaitForSeconds(duration);

        // 4. 恢复 NavMesh
        _rb.velocity = Vector3.zero;
        _rb.isKinematic = true;
        
        // 寻找最近的有效地面，防止卡在墙里
        if (NavMesh.SamplePosition(transform.position, out NavMeshHit hit, 2.0f, NavMesh.AllAreas))
        {
            _agent.Warp(hit.position); // 瞬移回网格
            _agent.enabled = true;
            _agent.isStopped = false;
        }
        else
        {
            // 异常处理：被击飞出地图了，直接处死
            GetComponent<Health>().Kill(); 
        }
    }
}
```

---

## 5. 常见坑点速查 (Troubleshooting)

| 现象 | 原因 | 解决方案 |
| :--- | :--- | :--- |
| **怪物原地转圈** | 目标点在脚下，但因为 StoppingDistance 没停住。 | 增大 `StoppingDistance` 或检测 `agent.remainingDistance < Threshold` 手动 Stop。 |
| **怪物穿墙** | 速度太快，或 `NavMeshObstacle` 没有开 `Carve`。 | 开启 `Carve`；对于极快单位，改用 Raycast 检测前方障碍。 |
| **浮空/陷入地下** | Agent 的 `BaseOffset` 设置不对，或模型原点不在脚底。 | 调整 `BaseOffset`；确保美术模型的 Pivot 在脚底中心。 |
| **性能暴跌** | 每一帧都对 100 个怪调用 `SetDestination`。 | 必须限制频率！使用协程每 0.2s 更新一次路径，或仅当目标移动超过 1米时更新。 |
