# 🧙‍♂️ 游戏常用算法深度研究 (Common Game Algorithms)

## 📚 1. 理论基础 (Theoretical Basis)

### 1.1 寻路算法 (Pathfinding)
*   **核心定义**: 在图或网格中寻找从起点到终点的最优路径。
*   **数学模型**:
    *   **A* (A-Star)**: $f(n) = g(n) + h(n)$。最通用的寻路算法，结合了Dijkstra的广度优先和贪婪最佳优先搜索。
    *   **Dijkstra**: 适用于计算移动范围或无启发式信息的图。
    *   **Flow Field (流场)**: 适用于大量单位移动到同一目标（如塔防游戏中的怪物群）。通过计算全图到目标的矢量场，避免对每个单位单独寻路。
*   **设计心理学**: 
    *   **智能感**: 怪物不卡墙、能绕路，给玩家带来"敌人很聪明"的压力。
    *   **预期性**: 玩家预判怪物路径进行塔防布局，路径显示必须准确。

### 1.2 空间划分 (Spatial Partitioning)
*   **核心定义**: 将空间划分为子区域，以加速碰撞检测、视锥剔除等查询。
*   **常用结构**:
    *   **Quadtree (四叉树)**: 适用于2D空间，动态对象较少或分布不均时。
    *   **Spatial Hashing (空间哈希)**: 将空间划分为网格，通过哈希函数映射。适用于大量动态对象（如弹幕游戏）。
    *   **BVH (层次包围盒)**: 适用于复杂形状的物理检测。

### 1.3 随机与噪声 (RNG & Noise)
*   **核心定义**: 生成不可预测但可控的数值或结构。
*   **算法**:
    *   **Perlin/Simplex Noise**: 生成平滑连续的随机值，用于地形生成。
    *   **Fisher-Yates Shuffle**: 洗牌算法，用于随机掉落或卡牌抽取。
    *   **Weighted Random**: 加权随机，用于Looter游戏的掉落表。

---

## 🛠️ 2. 实践应用 (Practical Implementation)

### 2.1 Vampirefall 适配 (TD + Roguelike + Looter)
*   **塔防 (TD) - 流场寻路**:
    *   由于怪物数量巨大（数百/千），对每个怪物运行 A* 是性能杀手。
    *   **方案**: 维护一张全局 `Vector2[,]` 流场图。每当玩家改变地形（造塔）时，重新计算一次流场。所有怪物每帧只需读取当前格子的向量即可。
*   **弹幕与碰撞 - 空间哈希**:
    *   大量子弹和怪物碰撞。
    *   **方案**: 使用 `Dictionary<int, List<Entity>>` 或扁平数组作为 Grid。Grid 大小设为最大单位直径的 1-2 倍。
*   **Roguelike - 伪随机 (PRNG)**:
    *   使用种子 (Seed) 驱动所有随机。确保同一局游戏（Seed相同）的回放完全一致。
    *   **C#**: 避免使用 `System.Random` (不可控)，推荐使用 `Unity.Mathematics.Random` 或自定义 `Xorshift`。

### 2.2 数据结构建议 (C#)

```csharp
// 简单的空间哈希网格接口
public interface ISpatialGrid<T>
{
    void Insert(T item, Vector2 position);
    void Remove(T item, Vector2 position);
    void Query(Vector2 position, float radius, List<T> results);
}

// 流场节点
public struct FlowNode
{
    public Vector2 Direction; // 移动方向
    public int Distance;      // 距离目标的步数（用于Dijkstra生成流场）
    public bool IsBlocked;    // 是否阻挡
}
```

### 2.3 Unity 实现注意事项
*   **Jobs System & Burst Compiler**:
    *   寻路和空间查询是计算密集型任务，**必须**使用 Job System 并开启 Burst 编译。
    *   避免在 Job 中分配内存（GC Alloc），使用 `NativeArray`。
*   **分帧处理**:
    *   如果流场计算过重，可以分帧更新（Time Slicing），虽然会有短暂的路径延迟，但能保证帧率平滑。

---

## 🌟 3. 业界优秀案例 (Industry Best Practices)

### 3.1 Factorio (异星工厂) - 极致优化
*   **机制**: 传送带和大量虫群的模拟。
*   **优点**: 极其高效的内存布局和缓存命中率（Data-Oriented Design）。
*   **借鉴**: 我们的怪物数据应尽量紧凑（Struct of Arrays），便于批量处理。

### 3.2 Rimworld (环世界) - 实用主义 AI
*   **机制**: 复杂的环境交互和寻路。
*   **优点**: 使用区域（Region）分层寻路，先在大区域间寻路，再在区域内精细寻路。
*   **借鉴**: 如果地图过大，流场计算太慢，可以引入分层图。

### 3.3 Vampire Survivors (吸血鬼幸存者) - 简单暴力
*   **机制**: 同屏成千上万怪物。
*   **优点**: 简单的物理碰撞（圆与圆），极简的 AI（直奔玩家）。
*   **借鉴**: 对于普通怪物，不要做复杂的避障，直接挤开（Boids/Steering Behaviors）效果更好且性能更高。

---

## 🔗 4. 参考资料 (References)

*   📄 **Flow Fields for Pathfinding**: [Leif Erkenbrach's Blog](https://leifnode.com/2013/12/flow-field-pathfinding/)
*   📺 **GDC: AI Pathfinding in Unity**: [YouTube Link](https://www.youtube.com/watch?v=j1k438m0DRc)
*   🌐 **Red Blob Games (算法宝藏)**: [Introduction to A*](https://www.redblobgames.com/pathfinding/a-star/introduction.html) - *强烈推荐，包含交互式演示*
*   📄 **Unity DOTS Physics**: [Unity Documentation](https://docs.unity3d.com/Packages/com.unity.physics@1.0/manual/index.html)

<script type="module">
  import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.esm.min.mjs';
  mermaid.initialize({ startOnLoad: false });
  await mermaid.run({
    querySelector: '.language-mermaid',
  });
</script>
