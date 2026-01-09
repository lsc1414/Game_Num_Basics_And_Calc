---
title: "游戏常用算法深度研究"
sidebarTitle: "🧙‍♂️ 常用算法与实践"
description: "Vampirefall 项目中使用的核心算法理论与 Unity 工程实践指南，涵盖寻路、空间管理、随机系统及性能优化。"
icon: "function"
---

# 🧙‍♂️ 游戏常用算法深度研究 (Common Game Algorithms)

本文档旨在作为 **Vampirefall** 项目的技术算法手册。我们不只罗列理论，更注重**理论与工程实践的结合**，特别是针对 Unity DOTS/Jobs System 的优化实现。

---

## 🗺️ 1. 寻路与导航 (Pathfinding & Navigation)

寻路是塔防(TD)和 Roguelike 游戏的核心。我们需要处理成千上万个单位的移动，同时保证性能。

### 1.1 理论基础：A\* 与 Dijkstra

> [!NOTE] > **A\* (A-Star)** 是在静态地图中寻找单体最优路径的标准解法。

- **公式**: $f(n) = g(n) + h(n)$
  - $g(n)$: 从起点到当前节点的实际代价。
  - $h(n)$: 启发函数(Heuristic)，预估从当前节点到终点的代价（通常用曼哈顿距离或欧几里得距离）。
- **适用场景**: 玩家寻路、精英怪寻路（数量少，精度要求高）。

### 1.2 实践：流场寻路 (Flow Field)

在 Vampirefall 中，我们需要处理海量怪物（Swarm）涌向同一个目标（基地）。对 500 个怪物运行 500 次 A\* 是极其浪费的。

**核心思想**:
不计算"怪物到终点"的路径，而是计算"地图上每个点到终点"的方向。所有怪物共享同一张流场图。

**实现步骤**:

1.  **生成热力图 (Integration Field)**: 使用 Dijkstra 算法，从终点扩散，计算全图每个格子到终点的步数（代价）。
    - 终点 = 0
    - 障碍物 = $\infty$
    - 相邻格 = +1 (或地形权重)
2.  **生成流场 (Vector Field)**: 遍历每个格子，指向其邻居中数值最小的那个格子。

**Unity 实践 (Job System)**:

```csharp
[BurstCompile]
public struct CalculateFlowFieldJob : IJob
{
    public int2 TargetPos;
    public int2 GridSize;
    [ReadOnly] public NativeArray<bool> Obstacles;
    public NativeArray<float2> FlowMap; // 输出结果

    public void Execute()
    {
        // 1. Dijkstra 广度优先搜索计算距离场
        // ... (省略队列实现细节)

        // 2. 根据距离场计算向量
        for (int x = 0; x < GridSize.x; x++)
        {
            for (int y = 0; y < GridSize.y; y++)
            {
                int index = x + y * GridSize.x;
                \text{if} (Obstacles[index])
                {
                    FlowMap[index] = float2.zero;
                    continue;
                }

                // 寻找距离最小的邻居
                FlowMap[index] = CalculateGradient(x, y);
            }
        }
    }
}
```

### 1.3 避障与群聚 (Steering Behaviors)

寻路解决了"怎么去"的问题，**Steering Behaviors** 解决"怎么动"的问题，避免怪物重叠。

- **Separation (分离)**: 离太近的邻居远一点。
- **Alignment (对齐)**: 和邻居保持相同方向（可选）。
- **Cohesion (凝聚)**: 往邻居的中心靠（可选）。

> [!TIP]
> 在吸血鬼幸存者类游戏中，只需要实现**强硬的分离 (Hard Separation)**。如果两个怪物碰撞，直接推开，性能最高且视觉效果足够。

---

## 📦 2. 空间管理 (Spatial Partitioning)

当屏幕上有 1000 个子弹和 500 个怪物时，暴力检测碰撞 ($O(N^2)$) 会导致卡死。我们需要空间划分算法将复杂度降至 $O(N)$ 或 $O(N \log N)$。

### 2.1 理论：空间哈希 (Spatial Hashing)

将 2D 空间划分为固定的网格（Grid），每个网格存储其中的物体列表。

- **优点**: 插入和查询接近 $O(1)$，实现极其简单。
- **缺点**: 网格大小选取敏感，跨网格物体处理稍繁琐。
- **适用**: 均匀分布的大量动态物体（如弹幕、怪物群）。

### 2.2 理论：四叉树 (Quadtree)

递归地将空间划分为四个象限，直到区域内物体数量少于阈值。

- **优点**: 适应非均匀分布（空旷区域不占用内存）。
- **缺点**: 动态物体频繁移动导致树结构重建开销大。
- **适用**: 静态物体管理（建筑物、地形），或物体移动不频繁的场景。

### 2.3 Vampirefall 实践：Flat Grid 优化

对于高频变动的 ECS 架构，可以使用**扁平化数组链表**实现空间哈希。

```csharp
// 概念伪代码
public struct SpatialMap
{
    // 单元格大小 (例如 2.0f)
    public float CellSize;
    // 这里的 Key 是 gridX + gridY * width
    // Value 是该个格子里第一个 Entity 的索引
    public NativeMultiHashMap<int, Entity> Map;

    public void Add(Entity entity, float2 pos)
    {
        int2 cell = (int2)math.\text{floor}(pos / CellSize);
        int key = GetHash(cell);
        Map.Add(key, entity);
    }

    // 查询附近的实体
    public void Query(float2 pos, float radius, NativeList<Entity> result)
    {
        // 计算覆盖的网格范围 (minCell 到 maxCell)
        // 遍历这些网格中的所有 Key
    }
}
```

---

## 🎲 3. 随机与概率 (RNG & Probability)

### 3.1 理论：真随机 vs 伪随机 (PRNG)

- **Input Randomness**: 在做决定前随机（如：地图生成）。
- **Output Randomness**: 在做决定后随机（如：攻击命中率）。**Roguelike 应尽量避免这种体验较差的随机，或者用"保底"机制修饰。**

### 3.2 实践：加权随机 (Weighted Random)

用于 Loot Table（掉落表）。

**算法**:

1. 计算总权重 (Total Weight)。
2. 生成 0 到 Total Weight 之间的随机数 `r`。
3. 遍历列表，`r -= 当前项权重`。
4. 当 `r <= 0` 时，选中当前项。

**优化 (Alias Method)**:
如果有大量且不变的权重表，预处理成 Alias Table 可将抽取复杂度降为 $O(1)$。但对于一般游戏，普通的 $O(N)$ 线性扫描足够。

```csharp
public static T GetWeightedRandom<T>(List<T> items, System.Func<T, float> weightSelector)
{
    float totalWeight = 0;
    foreach(var item in items) totalWeight += weightSelector(item);

    float r = UnityEngine.Random.Range(0, totalWeight);
    foreach(var item in items)
    {
        float w = weightSelector(item);
        \text{if} (r <= w) return item;
        r -= w;
    }
    return default;
}
```

### 3.3 实践：洗牌算法 (Fisher-Yates Shuffle)

用于抽卡或"俄罗斯方块式"的掉落（保证一轮内不重复）。

```csharp
public static void Shuffle<T>(IList<T> list)
{
    int n = list.Count;
    while (n > 1)
    {
        n--;
        int k = UnityEngine.Random.Range(0, n + 1);
        (list[k], list[n]) = (list[n], list[k]); // Swap
    }
}
```

---

## 📈 4. 数值插值与平滑 (Math & Interpolation)

### 4.1 线性与非线性插值

- **Lerp (Linear)**: $a + (b - a) * t$。简单，由于且仅用于位置直连。
- **Slerp (Spherical)**: 弧形插值，用于**旋转**，保证角速度恒定。
- **SmoothDamp**: 类似弹簧阻尼，用于摄像机跟随或 UI 动效，比 Lerp 更自然（Lerp 会在接近终点时无限变慢）。

### 4.2 缓动函数 (Easing Functions)

UI 动效的灵魂。不要只用线性变化。
推荐使用公式库（如 $t^2$, $t^3$, $1-(1-t)^2$ 等）。

---

## 🚀 5. 性能优化模式 (Optimization Patterns)

### 5.1 对象池 (Object Pooling)

**理论**:
内存分配 (Allocation) 和垃圾回收 (GC) 是 Unity 移动端卡顿的主因。对象池通过复用对象避免频繁的 `Instantiate` 和 `Destroy`。

**Vampirefall 规范**:

- 所有特效 (VFX)、伤害数字 (Popups)、子弹 (Projectiles) **必须**使用对象池。
- 只有关卡切换时才允许大规模销毁。

### 5.2 脏标记模式 (Dirty Flag)

**理论**:
避免每一帧都重新计算复杂数据。只在数据发生变化时标记为 `isDirty = true`，在获取数据时如果发现脏标记才重新计算，否则返回缓存值。

**应用**:

- **UI**: 只有当金币变化时才更新 Text 组件。
- **属性**: 只有当装备变动时才重新计算 `FinalAttack = Base + Buffs`。

```csharp
public class StatSystem
{
    private float _cacheValue;
    private bool _isDirty = true;

    public void AddBuff() { _isDirty = true; }

    public float Helpers
    {
        get
        {
            \text{if} (_isDirty) Recalculate();
            return _cacheValue;
        }
    }
}
```

---

## 🔗 参考资料

- 📄 **Game Programming Patterns**: 必读经典。
- 🌐 **Red Blob Games**: 几何与寻路算法的宝库。
- 📺 **GDC: "I Shot You First"**: 守望先锋网络同步与插值算法。
