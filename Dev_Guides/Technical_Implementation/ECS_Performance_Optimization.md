# 🚀 ECS 性能优化实战：从 Vampire Survivors 到 Unity DOTS

**文档目标**：解析如何在 Unity 中实现同屏 500+ 敌人的高性能逻辑，参考 *Vampire Survivors* 的优化思路，并映射到 Unity DOTS (Data-Oriented Technology Stack) 的最佳实践。同时结合本项目特有的 **GAS (Gameplay Ability System)** 进行混合架构设计。

---

## 1. 为什么传统 OOP (面向对象) 会卡？

在传统的 `MonoBehaviour` 方式中，每个怪物都是一个 GameObject。

### 💀 性能杀手名单：
1.  **内存碎片与缓存未命中 (Cache Miss)**：
    *   **现象**: 怪物数据 (`Enemy` 类) 散落在堆内存的各个角落。
    *   **原理**: CPU 读取内存的速度远慢于计算速度。当 CPU 处理 `EnemyA` 时，它会将附近内存块加载到 L1/L2 缓存（Prefetching）。但如果 `EnemyB` 在内存的另一头，预取失效，CPU 必须停下来等待内存读取（Cache Miss）。这是性能的头号杀手。
2.  **GC 压力 (Garbage Collection)**：
    *   大量的临时对象实例化和销毁（如子弹、掉落物）导致 GC 频繁触发，造成卡顿。
3.  **Transform 同步开销**：
    *   Unity 引擎层 (C++) 和脚本层 (C#) 之间的 `transform.position` 交互有封送（Marshalling）开销。
4.  **Update() 调用开销**：
    *   500 个 `Update()` 方法的虚函数调用本身就是巨大的 CPU 负担。

---

## 2. 核心解法：数据导向设计 (DOD)

**Data-Oriented Design (DOD)** 的核心思想是：**CPU 喜欢处理连续的、简单的数据块。**

### 2.1 结构体数组 (SoA) vs 数组结构体 (AoS)

*   **AoS (Array of Structs) - OOP 常用**:
    *   `[ {HP, Pos, Speed}, {HP, Pos, Speed}, ... ]`
    *   **问题**：如果系统只想更新位置（Position += Speed * dt），CPU 缓存行里却被迫加载了不用的 HP 数据，浪费了宝贵的缓存带宽。

*   **SoA (Struct of Arrays) - ECS 推荐**:
    *   `Pos: [P1, P2, P3...]`
    *   `Speed: [S1, S2, S3...]`
    *   `HP: [H1, H2, H3...]`
    *   **优势**：
        1.  **缓存命中率极高**: 当移动系统运行时，只加载 Pos 和 Speed 数组，每一字节的数据都是有用的。
        2.  **SIMD 优化**: 现代 CPU 可以用一条指令同时处理 4 个或 8 个浮点数（Vectorization）。连续的数组天然适合 SIMD。

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
*   **适用**：项目中期优化，不想重写整个架构。
*   **收益**：移动计算移至多线程，Burst 编译器优化数学运算。

### 🟡 方案 B：GPU Instancing 渲染
逻辑再快，渲染 500 个 DrawCall 也会死。
*   使用 `Graphics.DrawMeshInstanced` 或 `DrawMeshInstancedIndirect`。
*   将所有怪物的 Position/Rotation/Color 塞入 `ComputeBuffer`，一次提交给 GPU。

### 🔴 方案 C：Pure ECS (Unity DOTS)
*   **Entities**：纯数据实体 ID。
*   **Components**：`IComponentData` (struct)，如 `MoveSpeedData`, `HealthData`。
*   **Systems**：`SystemBase` 或 `ISystem`，只负责逻辑。

---

## 5. 深度整合：ECS + GAS 混合架构

在 **Project Vampirefall** 中，我们结合 [Gameplay Ability System (GAS)](../../Tech/Gameplay_Ability_System_Design.md) 设计，采用混合架构。

### 5.1 架构图
*   **Hero / Boss**: `MonoBehaviour` + `AbilitySystemComponent (C# Class)`。处理复杂逻辑、动画状态机。
*   **Minions (500+)**: `ECS Entity` + `BuffBuffer (DynamicBuffer)`。处理移动、简单攻击、Buff 状态。

### 5.2 案例：特斯拉电塔 vs 虫群

**场景**: 特斯拉电塔释放“连锁闪电”，击中 50 个敌人，造成伤害并施加“感电” Debuff。

**流程**:
1.  **触发 (Mono)**: 电塔 (GameObject) 的 `GA_ChainLightning` 触发。
2.  **查询 (ECS)**: 通过 `EntityQuery` 瞬间找到范围内最近的 50 个带有 `Tag_Enemy` 的实体。
3.  **应用 (ECS Job)**:
    *   创建一个 `ApplyEffectJob`。
    *   并行写入：扣除 HP (`Health -= Damage`)。
    *   并行写入：向实体的 `BuffBuffer` 添加 `GE_Shock` (感电) 的 ID。
4.  **表现 (Hybrid)**:
    *   Job 输出被击中实体的坐标列表。
    *   主线程根据坐标生成 50 条闪电链 VFX (使用 ParticleSystem 或 LineRenderer)。

**代码片段：Buff 处理系统 (ECS)**
```csharp
[BurstCompile]
public partial struct BuffProcessingSystem : ISystem
{
    public void OnUpdate(ref SystemState state)
    {
        float dt = SystemAPI.Time.DeltaTime;
        
        // 遍历所有拥有 Buff 缓冲区的实体
        foreach (var buffBuffer in SystemAPI.Query<DynamicBuffer<ActiveBuff>>())
        {
            for (int i = 0; i < buffBuffer.Length; i++)
            {
                // 处理持续时间
                var buff = buffBuffer[i];
                buff.RemainingTime -= dt;
                
                // 处理 Buff 逻辑 (例如：每秒伤害)
                if (buff.TypeId == BuffIDs.Poison) {
                    // ... Apply Damage Logic ...
                }

                // 移除过期 Buff
                if (buff.RemainingTime <= 0) {
                    buffBuffer.RemoveAt(i);
                    i--;
                }
            }
        }
    }
}
```

---

## 6. 实战检查清单 (Checklist)

1.  [ ] **去 Mono化**：核心高频逻辑（移动、碰撞）剥离 MonoBehaviour。
2.  [ ] **关闭物理**：小怪禁用 Rigidbody，使用自定义轻量级碰撞。
3.  [ ] **批量渲染**：确保怪物材质支持 GPU Instancing。
4.  [ ] **结构体代替类**：数据层尽可能使用 `struct` 以利用 SoA 优势。
5.  [ ] **混合同步**：仅在必要时（如播放死亡动画）将 ECS 数据同步回 GameObject。

## 7. 性能预算参考
| 平台 | 同屏目标 (60FPS) | DrawCalls 限制 | 物理计算耗时 |
| :--- | :--- | :--- | :--- |
| PC (Mid) | 2000+ | < 1500 (Batching后) | < 3ms |
| Mobile (High) | 500+ | < 300 | < 4ms |
| Mobile (Low) | 100+ | < 100 | < 5ms |
