# 🏭 Factorio (异星工厂) 深度研究：极致优化与自动化

## 📚 1. 理论基础 (Theoretical Basis)

### 1.1 数据导向设计 (Data-Oriented Design, DOD)
*   **核心定义**: 关注数据的内存布局而非对象模型。通过提高 CPU 缓存命中率 (Cache Locality) 来最大化性能。
*   **数学模型**: 
    *   **Amdahl's Law**: 并行计算的加速比受限于串行部分。Factorio 实际上大部分逻辑是单线程的，但通过极致的单核优化达到了惊人的规模。
*   **设计心理学**:
    *   **确定性 (Determinism)**: 玩家相信系统是稳定可靠的。输入 A 永远得到输出 B。这是构建复杂自动化流水线的心理基石。

### 1.2 确定性锁步模拟 (Deterministic Lockstep Simulation)
*   **核心定义**: 游戏逻辑与渲染完全分离。逻辑更新频率固定（如 60 UPS），且在任何机器上运行结果完全一致。
*   **关键技术**:
    *   **定点数/软浮点**: 避免不同 CPU 浮点运算微小差异导致的蝴蝶效应。
    *   **输入同步**: 联机时仅同步玩家操作指令，而非同步所有单位位置。

---

## 🛠️ 2. 实践应用 (Practical Implementation)

### 2.1 Vampirefall 适配 (TD + Roguelike)
*   **海量怪物优化**:
    *   Vampirefall 后期可能有数百个怪物和弹幕。
    *   **借鉴**: 不要使用 Unity 的 `MonoBehaviour` 处理每个怪物。使用 `struct` 数组存储怪物数据。
*   **回放系统**:
    *   Roguelike 游戏常需要“上一局回顾”或“种子分享”。
    *   **借鉴**: 记录玩家每一帧的操作（造塔位置、释放技能时间）和初始 Seed，即可完美重现整局游戏，且文件极小。

### 2.2 数据结构建议 (C# / Unity DOTS)

```csharp
// ❌ 面向对象 (OOP) - 缓存不友好
public class Enemy : MonoBehaviour {
    public float Health;
    public Vector3 Position;
    public EnemyType Type;
    // ... 包含大量引用和虚函数表
}

// ✅ 数据导向 (DOD) - 结构数组 (SoA)
public struct EnemyData {
    // 仅包含核心数据，内存连续
    public float Health;
    public float2 Position; 
    public int TypeId;
}

// 管理器
public class EnemyManager {
    // 使用 NativeArray 在 Job System 中并行处理
    public NativeArray<EnemyData> ActiveEnemies;
    
    public void UpdateEnemies() {
        // 批量更新逻辑，极高的 Cache 命中率
    }
}
```

### 2.3 传送带逻辑 (Belt Logic) - 离散化移动
*   Factorio 的传送带不是物理模拟，而是离散的“槽位”或距离计算。
*   **Vampirefall 应用**: 塔防中的怪物移动路径也可以预计算。
    *   怪物不是在 update 中 `pos += dir * speed`。
    *   而是 `distanceOnPath += speed * dt`，然后根据 `distance` 插值求位置。这样可以避免物理碰撞检测的开销。

---

## 🌟 3. 业界优秀案例 (Industry Best Practices)

### 3.1 Factorio - 传送带优化 (The Belt Optimization)
*   **案例分析**: 早期 Factorio 每个物品都是独立实体。后期改为“传输线 (Transport Line)”模型。
*   **优化**: 一条满载的传送带被视为一个整体，只需更新首尾物品，中间物品相对静止。
*   **借鉴**: 当怪物排队行进且无干扰时，可以将其视为一个“队列对象”统一移动，而非计算每个个体。

### 3.2 Dyson Sphere Program (戴森球计划) - 极致 GPU 渲染
*   **案例分析**: 同屏数万运输船。
*   **优化**: 使用 `DrawMeshInstancedIndirect`。所有位置计算在 Compute Shader 中完成，CPU 仅负责提交指令。
*   **借鉴**: Vampirefall 的弹幕系统应完全 GPU 化。

### 3.3 Mindustry - 移动端适配
*   **案例分析**: 类似 Factorio 但在手机上流畅运行。
*   **优缺点**: 简化了物流系统（管道代替机械臂），牺牲了部分深度换取操作便利性和性能。
*   **借鉴**: 移动端塔防操作要简化，避免精确点击像素级目标。

---

## 🔗 4. 参考资料 (References)

*   📄 **Factorio Friday Facts #176 - Belts optimization**: [Factorio Blog](https://www.factorio.com/blog/post/fff-176)
*   📄 **Factorio Friday Facts #366 - The only simulation**: [Factorio Blog](https://www.factorio.com/blog/post/fff-366) - *关于确定性模拟的深度好文*
*   📺 **GDC: Data-Oriented Design in C++**: [YouTube Link](https://www.youtube.com/watch?v=rX0ItVEVjHc)
*   🌐 **Unity DOTS Documentation**: [Unity ECS](https://unity.com/dots)

<script type="module">
  import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.esm.min.mjs';
  mermaid.initialize({ startOnLoad: false });
  await mermaid.run({
    querySelector: '.language-mermaid',
  });
</script>
