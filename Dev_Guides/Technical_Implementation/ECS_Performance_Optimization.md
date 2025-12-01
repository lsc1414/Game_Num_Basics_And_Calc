# 🚀 ECS 性能优化实战：从 Vampire Survivors 到 Unity DOTS

**文档目标**：解析如何在 Unity 中实现同屏 500+ 敌人的高性能逻辑，参考 *Vampire Survivors* 的优化思路，并映射到 Unity DOTS (Data-Oriented Technology Stack) 的最佳实践。

---

## 1. 为什么传统 OOP (面向对象) 会卡？

在传统的 `MonoBehaviour` 方式中，每个怪物都是一个 GameObject。

### 💀 性能杀手名单：
1.  **内存碎片 (Cache Miss)**：
    *   怪物数据散落在堆内存的各个角落。CPU 获取 `EnemyA` 的数据后，预取不到 `EnemyB` 的数据，导致频繁等待内存（Cache Miss）。
2.  **GC 压力 (Garbage Collection)**：
    *   大量的临时对象实例化和销毁（如子弹、掉落物）导致 GC 频繁触发，造成卡顿。
3.  **Transform 同步开销**：
    *   Unity 引擎层和脚本层之间的 `transform.position` 交互有封送（Marshalling）开销。
4.  **Update() 调用开销**：
    *   500 个 `Update()` 方法的虚函数调用本身就是巨大的 CPU 负担。

---

## 2. 核心解法：数据导向设计 (DOD)

**Data-Oriented Design (DOD)** 的核心思想是：**CPU 喜欢处理连续的、简单的数据块。**

### 2.1 结构体数组 (SoA) vs 数组结构体 (AoS)

*   **AoS (Array of Structs) - OOP 常用**:
    *   `[ {HP, Pos, Speed}, {HP, Pos, Speed}, ... ]`
    *   问题：如果我只想更新位置，CPU 缓存行里塞满了不用的 HP 数据，浪费带宽。

*   **SoA (Struct of Arrays) - ECS 推荐**:
    *   `Pos: [P1, P2, P3...]`
    *   `Speed: [S1, S2, S3...]`
    *   `HP: [H1, H2, H3...]`
    *   优势：当系统计算移动时，只加载 Pos 和 Speed 数组，缓存命中率极高。Simd (单指令多数据) 极易优化。

---

## 3. Vampire Survivors 的优化魔法

虽然 *Vampire Survivors* 早期是基于 Phaser (JS) 开发的，但其优化逻辑通用：

### 3.1 伪物理碰撞 (Fake Physics)
不要给 500 个怪物挂 `Rigidbody` 或 `BoxCollider`。
*   **网格法 (Spatial Hashing)**：将地图划分为小格子。只检测同一格子或相邻格子内的单位。
*   **圆圆碰撞 (Circle-Circle)**：`DistanceSquared(A, B) < (R1+R2)^2`。避免开方运算。
*   **“推挤”而非“物理”**：怪物重叠时，根据重叠向量给一个排斥力，而不是物理引擎的刚体解算。

### 3.2 对象池 (Object Pooling) 2.0
*   不仅复用 GameObject，还要**复用数据结构**。
*   **Loot Reservoir (掉落蓄水池)**：经验宝石不总是实例化。如果地上超过 50 个宝石，将新掉落的经验值“合并”到最近的宝石上，或创建一个特殊的“红宝石”来吸收全屏经验。

---

## 4. Unity 实现方案 (从入门到进阶)

### 🟢 方案 A：简易版 (Job System + Burst)
不使用完整的 Entities 包，仅用 Job System 优化计算。

```csharp
[BurstCompile]
struct MoveJob : IJobParallelForTransform
{
    [ReadOnly] public NativeArray<float> moveSpeeds;
    [ReadOnly] public float deltaTime;
    [ReadOnly] public NativeArray<float3> targetPositions;

    public void Execute(int index, TransformAccess transform)
    {
        float3 dir = math.normalize(targetPositions[index] - (float3)transform.position);
        transform.position += (Vector3)(dir * moveSpeeds[index] * deltaTime);
    }
}
```
*   **适用**：项目中期优化，不想重写整个架构。
*   **收益**：移动计算移至多线程，Burst 编译器优化数学运算。

### 🟡 方案 B：GPU Instancing 渲染
逻辑再快，渲染 500 个 DrawCall 也会死。
*   使用 `Graphics.DrawMeshInstanced` 或 `DrawMeshInstancedIndirect`。
*   将所有怪物的 Position/Rotation/Color 塞入 `ComputeBuffer`，一次提交给 GPU。

### 🔴 方案 C：Pure ECS (Unity DOTS)
*   **Entities**：纯数据实体。
*   **Components**：`IComponentData` (struct)，如 `MoveSpeedData`, `HealthData`。
*   **Systems**：`SystemBase` 或 `ISystem`，只负责逻辑。
*   **Baker**：将 GameObject 转化为 Entity。

**代码片段：移动系统**
```csharp
[BurstCompile]
public partial struct MovementSystem : ISystem
{
    public void OnUpdate(ref SystemState state)
    {
        float dt = SystemAPI.Time.DeltaTime;
        
        // Query: 找到所有有 LocalTransform 和 MoveSpeed 的实体
        foreach (var (transform, speed) in 
                 SystemAPI.Query<RefRW<LocalTransform>, RefRO<MoveSpeed>>())
        {
            transform.ValueRW.Position += transform.ValueRO.Forward() * speed.ValueRO.Value * dt;
        }
    }
}
```

---

## 5. 实战检查清单 (Checklist)

1.  [ ] **去 Mono化**：核心高频逻辑（移动、碰撞）剥离 MonoBehaviour。
2.  [ ] **关闭物理**：小怪禁用 Rigidbody，使用自定义轻量级碰撞。
3.  [ ] **批量渲染**：确保怪物材质支持 GPU Instancing。
4.  [ ] **避免字符串**：Update 中严禁 `string` 操作或 `Debug.Log`。
5.  [ ] **结构体代替类**：数据层尽可能使用 `struct`。

## 6. 性能预算参考
| 平台 | 同屏目标 (60FPS) | DrawCalls 限制 | 物理计算耗时 |
| :--- | :--- | :--- | :--- |
| PC (Mid) | 2000+ | < 1500 (Batching后) | < 3ms |
| Mobile (High) | 500+ | < 300 | < 4ms |
| Mobile (Low) | 100+ | < 100 | < 5ms |
