# PCG 算法综合指南

> 本文档由以下文件合并生成 (2026-01-09)



---


<!-- 来源: Tech\Algorithms\Procedural_Generation_Guide.md -->

## 🧙‍♂️ 关卡生成算法(PCG)深度研究

## 📚 1. 理论基础 (Theoretical Basis)

### 🎯 核心定义

**程序化内容生成 (Procedural Content Generation, PCG)** 是通过算法自动创建游戏内容的技术。对于Roguelike游戏，PCG是核心支柱。

**PCG的优势**:

1. **无限内容** - 避免重复感
2. **降低成本** - 减少手工设计工作量

3. **增加寿命** - 每次游玩都不同

**PCG的挑战**:

1. **质量控制** - 生成结果可能不可玩
2. **性能开销** - 生成算法可能很慢

3. **平衡性** - 难度/奖励可能失衡

### 📐 核心算法分类

#### 1. WFC (Wave Function Collapse) - 波函数坍缩

**原理**: 基于约束传播的瓦片拼接算法。

```
基本流程:
1. 定义瓦片集合及其相邻规则
2. 随机选择一个位置，坍缩为确定状态
3. 传播约束到邻居
4. 重复直到所有位置确定

示例 - 简单地牢:
瓦片类型: 墙、地板、门
规则:
- 墙只能邻接墙或门
- 地板只能邻接地板或门
- 门必须连接墙和地板
```

**优点**:

- ✅ 生成结果始终符合规则
- ✅ 适合复杂约束
- ✅ 可以生成有机感的关卡

**缺点**:

- ❌ 可能陷入无解状态（需要回溯）
- ❌ 性能较慢
- ❌ 规则定义复杂

#### 2. BSP (Binary Space Partitioning) - 二叉空间分割

**原理**: 递归分割空间，创建房间和走廊。

```
基本流程:
1. 从整个区域开始
2. 随机选择水平或垂直分割
3. 递归分割子区域
4. 在叶节点创建房间
5. 连接相邻房间

示例:
┌─────────────────┐
│     房间A       │ ← 叶节点1
├────────┬────────┤
│ 房间B  │ 房间C  │ ← 叶节点2、3
└────────┴────────┘
   ↑ 走廊连接
```

**优点**:

- ✅ 简单易实现
- ✅ 生成速度快
- ✅ 房间分布均匀

**缺点**:

- ❌ 生成结果较规整（缺乏有机感）
- ❌ 走廊可能冗长
- ❌ 不够随机

#### 3. Cellular Automata - 元胞自动机

**原理**: 基于简单规则的迭代演化。

```
经典规则 (4-5规则):
- 如果邻居墙 >= 5: 变成墙
- 如果邻居墙 <= 4: 变成地板

迭代过程:
初始: 随机噪声 (50% 墙)
  ■□■■□
  □■□□■
  ■■■□□

迭代1: 应用规则
  ■■■■□
  ■■■□■
  ■■■■□

迭代5: 收敛
  ■■■■■
  ■□□□■
  ■■■■■
  ↑ 生成洞穴状结构
```

**优点**:

- ✅ 生成自然的洞穴/有机形状
- ✅ 实现简单
- ✅ 参数易调

**缺点**:

- ❌ 不保证连通性
- ❌ 难以控制具体形状
- ❌ 需要后处理（连通性检测）

---

## 🛠️ 2. 实践应用 (Practical Implementation)

### 🎮 Vampirefall 地图生成框架

#### 混合生成策略

Vampirefall的塔防+肉鸽特性需要**手工设计 + 程序生成**混合：

```
┌─────────────────────────────────────┐
│ 第1层：手工模板（塔防布局）          │
│ - 预设路径节点                      │
│ - 关键塔位标记                      │
├─────────────────────────────────────┤
│ 第2层：程序变化（肉鸽随机性）        │
│ - 敌人刷新点随机                    │
│ - 资源点分布                        │
│ - 地形障碍物                        │
├─────────────────────────────────────┤
│ 第3层：词条修饰（肉鸽增强）          │
│ - "迷雾战场"（降低视野）            │
│ - "狭窄通道"（路径变窄）            │
└─────────────────────────────────────┘
```

### 🗂️ 数据结构

#### MapTemplate.cs

```csharp
[CreateAssetMenu(fileName = "MapTemplate", menuName = "PCG/Map Template")]
public class MapTemplate : ScriptableObject
{
    [Header("模板信息")]
    public string templateName = "森林地图";
    public Vector2Int size = new Vector2Int(50, 50);
    
    [Header("路径定义")]
    public PathNode[] pathNodes;  // 敌人行走路径
    
    [Header("塔位定义")]
    public TowerSlot[] towerSlots;  // 可建塔位置
    
    [Header("生成规则")]
    public GenerationRule[] rules;
}

[System.Serializable]
public class PathNode
{
    public Vector2Int position;
    public PathNode[] nextNodes;  // 支持分支路径
}

[System.Serializable]
public class TowerSlot
{
    public Vector2Int position;
    public TowerSlotType type;  // Normal, Strategic(战略点位)
}

[System.Serializable]
public class GenerationRule
{
    public RuleType type;
    public float probability;  // 触发概率
    public string parameters;  // JSON参数
}

public enum RuleType
{
    SpawnObstacle,    // 生成障碍物
    SpawnResource,    // 生成资源点
    ModifyPath,       // 修改路径
    AddEnemySpawn     // 添加刷怪点
}
```

#### ProceduralMapGenerator.cs

```csharp
public class ProceduralMapGenerator : MonoBehaviour
{
    public MapTemplate template;
    private int seed;
    
    public GeneratedMap Generate(int seed)
    {
        this.seed = seed;
        Random.InitState(seed);
        
        var map = new GeneratedMap
        {
            size = template.size,
            tiles = new TileType[template.size.x, template.size.y]
        };
        
        // 1. 初始化基础地形
        InitializeBaseTerrain(map);
        
        // 2. 放置路径
        PlacePaths(map, template.pathNodes);
        
        // 3. 放置塔位
        PlaceTowerSlots(map, template.towerSlots);
        
        // 4. 应用生成规则
        ApplyGenerationRules(map, template.rules);
        
        // 5. 验证可玩性
        if (!ValidateMap(map))
        {
            Debug.LogWarning($"[PCG] 地图生成失败(种子:{seed})，重新生成");
            return Generate(seed + 1);  // 换一个种子
        }
        
        return map;
    }
    
    private void InitializeBaseTerrain(GeneratedMap map)
    {
        for (int x = 0; x < map.size.x; x++)
        {
            for (int y = 0; y < map.size.y; y++)
            {
                map.tiles[x, y] = TileType.Ground;
            }
        }
    }
    
    private void PlacePaths(GeneratedMap map, PathNode[] nodes)
    {
        foreach (var node in nodes)
        {
            // 从节点到下一个节点绘制路径
            foreach (var next in node.nextNodes)
            {
                DrawPath(map, node.position, next.position);
            }
        }
    }
    
    private void DrawPath(GeneratedMap map, Vector2Int from, Vector2Int to)
    {
        // A* 或 Bresenham 算法绘制路径
        var points = CalculatePathPoints(from, to);
        
        foreach (var point in points)
        {
            if (IsInBounds(map, point))
            {
                map.tiles[point.x, point.y] = TileType.Path;
                
                // 加一点随机宽度
                if (Random.value < 0.3f)
                {
                    var offset = new Vector2Int(Random.Range(-1, 2), Random.Range(-1, 2));
                    var widePoint = point + offset;
                    if (IsInBounds(map, widePoint))
                    {
                        map.tiles[widePoint.x, widePoint.y] = TileType.Path;
                    }
                }
            }
        }
    }
    
    private bool ValidateMap(GeneratedMap map)
    {
        // 1. 检查路径连通性
        if (!IsPathConnected(map))
            return false;
        
        // 2. 检查塔位可达性
        if (!AreTowerSlotsValid(map))
            return false;
        
        // 3. 检查敌人无法到达塔位
        if (!IsTowerSafety(map))
            return false;
        
        return true;
    }
    
    private bool IsPathConnected(GeneratedMap map)
    {
        // BFS/DFS 检查从起点到终点是否连通
        var start = FindStartPoint(map);
        var end = FindEndPoint(map);
        
        return BFS(map, start, end);
    }
}

public class GeneratedMap
{
    public Vector2Int size;
    public TileType[,] tiles;
    public List<Vector2Int> towerSlots;
    public List<Vector2Int> enemySpawns;
    public int seed;
}

public enum TileType
{
    Ground,
    Path,
    Obstacle,
    TowerSlot,
    Resource
}
```

### 🎨 路径保证算法

**问题**: 程序生成可能产生不可通行的路径。

**解决方案**: 路径优先生成 + 验证 + 修复。

```csharp
public class PathGuarantee
{
    public static bool EnsurePathExists(GeneratedMap map, Vector2Int start, Vector2Int end)
    {
        // 1. A* 寻找路径
        var path = AStar.FindPath(map, start, end);
        
        if (path != null)
            return true;  // 路径已存在
        
        // 2. 强制打通路径
        path = ForceCreatePath(map, start, end);
        
        // 3. 应用到地图
        foreach (var point in path)
        {
            map.tiles[point.x, point.y] = TileType.Path;
        }
        
        return true;
    }
    
    private static List<Vector2Int> ForceCreatePath(GeneratedMap map, Vector2Int start, Vector2Int end)
    {
        var path = new List<Vector2Int>();
        var current = start;
        
        while (current != end)
        {
            path.Add(current);
            
            // 简单策略：每次移动到更接近终点的方向
            var toEnd = end - current;
            
            if (Mathf.Abs(toEnd.x) > Mathf.Abs(toEnd.y))
            {
                current += new Vector2Int(toEnd.x > 0 ? 1 : -1, 0);
            }
            else
            {
                current += new Vector2Int(0, toEnd.y > 0 ? 1 : -1);
            }
            
            // 防止无限循环
            if (path.Count > map.size.x * map.size.y)
                break;
        }
        
        path.Add(end);
        return path;
    }
}
```

---

## 🌟 3. 业界优秀案例 (Industry Best Practices)

### 🎮 案例 1: **Spelunky - 模板拼接大师**

#### 核心机制

Spelunky使用**预制房间模板 + 智能拼接**生成关卡。

**生成流程**:

```
1. 生成4x4房间网格
   [A][B][C][D]
   [E][F][G][H]
   [I][J][K][L]
   [M][N][O][P]
2. 标记关键房间
   入口: A
   出口: P
   商店: 随机1个
   暗室: 随机1-2个
3. 确保连通性
   A → ... → P 必须可达
   使用BFS生成主路径
4. 填充房间模板
   从模板库中随机选择符合规则的房间
5. 添加细节

   - 陷阱放置
   - 敌人刷新
   - 宝箱分布
```

**模板库设计**:

```
房间标签:
- 入口房 (ENT)
- 出口房 (EXIT)
- 普通房 (NORMAL)
- 陷阱房 (TRAP)
- 宝藏房 (TREASURE)

连接规则:
- 每个房间4个门（上下左右）
- 门必须对齐
- 每个门有"必须"或"可选"属性
```

**Vampirefall 借鉴**:

- 预制塔防模板（不同地形）
- 模板库分类（简单/困难/Boss）
- 主路径保证算法

---

### 🎮 案例 2: **The Binding of Isaac - 房间库系统**

#### 核心机制

Isaac使用**大量手工设计房间 + 随机组合**。

**房间库规模**:

```
普通房: 500+ 个
Boss房: 50+ 个
商店: 20+ 个
宝藏房: 30+ 个
秘密房: 20+ 个

总计: 600+ 个手工房间
```

**房间选择算法**:

```csharp
Room SelectRoom(RoomType type, int difficulty, HashSet<int> usedRooms)
{
    // 1. 筛选候选房间
    var candidates = roomDatabase
        .Where(r => r.type == type)
        .Where(r => r.difficulty <= difficulty)
        .Where(r => !usedRooms.Contains(r.id))
        .ToList();
    
    // 2. 权重随机选择
    var weights = candidates.Select(r => r.weight).ToArray();
    var selected = WeightedRandom.Select(candidates, weights);
    
    // 3. 标记已使用（避免重复）
    usedRooms.Add(selected.id);
    
    return selected;
}
```

**设计哲学**:
> "程序生成不是为了减少工作量，而是为了增加重玩价值。"

**Vampirefall 借鉴**:

- 建立塔防场景库（100+）
- 基于难度分级
- 避免同一局重复

---

### 🎮 案例 3: **Enter the Gungeon - 程序化地牢**

#### 核心机制

Gungeon结合了**BSP分割 + 手工房间 + 特殊规则**。

**生成算法**:

```
1. BSP生成房间布局
   ├ 分割次数: 5-7次
   ├ 房间数量: 15-25个
   └ 房间大小: 10x10 到 30x30
2. 分配房间类型
   ├ 1个Boss房（必须在边缘）
   ├ 1个商店
   ├ 1-2个宝藏房
   ├ 2-3个挑战房
   └ 其余为普通战斗房
3. 生成走廊
   ├ 最短路径连接
   ├ 添加环路（30%概率）
   └ 秘密房间连接（需要炸墙）
4. 填充内容
   ├ 房间从模板库选择
   ├ 敌人根据难度曲线生成
   └ 物品根据掉落表放置
```

**特殊规则**:

```
- Boss房必须从入口走最远路径
- 商店必须在主路径上
- 宝藏房可能在分支
- 秘密房邻接至少2个房间
```

**Vampirefall 借鉴**:

- BSP用于大区域划分
- 关键房间（Boss/商店）位置规则
- 秘密区域设计

---

## 🔗 4. 参考资料 (References)

### 📄 理论

1. **Procedural Content Generation in Games**  
    作者: Noor Shaker, Julian Togelius, Mark J. Nelson  
    [书籍链接](http://pcgbook.com/)

2. **Wave Function Collapse Algorithm**  
    *Maxim Gumin*  
    [GitHub](https://github.com/mxgmn/WaveFunctionCollapse)

### 📺 GDC

1. **[GDC 2017] Spelunky Level Generation**  
    演讲者: Derek Yu  
    [YouTube](https://www.youtube.com/watch?v=Uqk5Zf0tw3o)

2. **[GDC 2015] Diablo's Dungeon Generation**  
    演讲者: Mike Barlow (Blizzard)  
    [GDC Vault](https://www.gdcvault.com/play/diablo_dungeon)

### 🌐 博客

1. **The Binding of Isaac Room Design**  
    [Edmund McMillen Blog](https://edmundm.com/post/isaac-room-design)

2. **Procedural Map Generation Techniques**  
    [RogueBasin Wiki](http://www.roguebasin.com/index.php?title=Articles)

---

## 🎯 附录：Vampirefall PCG实施检查清单

### ✅ 阶段1: 模板系统（必须）
- [ ] 创建10+塔防地图模板
- [ ] 定义路径节点和塔位
- [ ] 建立模板库管理器

### ✅ 阶段2: 生成算法（必须）
- [ ] 实现BSP或房间拼接
- [ ] 路径保证算法
- [ ] 连通性验证

### ✅ 阶段3: 随机性（推荐）
- [ ] 障碍物随机放置
- [ ] 资源点分布
- [ ] 敌人刷新点变化

### ✅ 阶段4: 验证系统（必须）
- [ ] 可玩性检测
- [ ] 难度评估
- [ ] 种子记录（用于bug复现）

### ✅ 阶段5: 调试工具（推荐）
- [ ] 可视化生成过程
- [ ] 种子输入功能
- [ ] 性能监控

---

**最后更新**: 2025-12-04  
**维护者**: Vampirefall 设计团队




---


<!-- 来源: Dev_Guides\Technical_Implementation\Procedural_Generation_WFC.md -->

## 波函数坍缩 (WFC) 生成 (Wave Function Collapse)

> [!NOTE]
> **核心思想**: WFC 是一种基于**约束 (Constraint)** 的生成算法。它不是告诉计算机“怎么画”，而是告诉它“什么不能画”。

在 Roguelike 地牢生成中，WFC 能比传统的“房间+走廊”算法生成更自然、更有机的结构。

---

## 1. 核心概念 (Core Concepts)

### 1.1 叠加态 (Superposition)
在算法开始时，地图上的每一个格子都同时处于“所有可能状态”的叠加中。

*   例如：一个格子既可能是“草地”，也可能是“墙壁”，也可能是“水”。

### 1.2 熵 (Entropy)
熵是衡量不确定性的指标。

*   **高熵**: 该格子有很多种可能性 (例如：草地/墙/水/路)。
*   **低熵**: 该格子只有很少的可能性 (例如：只能是墙)。
*   **熵为0**: 该格子状态已确定 (坍缩)。

### 1.3 坍缩 (Collapse)
观测导致坍缩。我们人为地（或随机地）选择一个格子，将其状态固定下来。

### 1.4 约束传播 (Constraint Propagation)
一旦一个格子确定了（例如变成了“水”），它的邻居就不可能是“岩浆”（假设水火不容）。这种约束会像波纹一样向四周传播，减少邻居的熵。

---

## 2. 算法流程 (Algorithm Flow)

1.  **初始化**: 将网格中所有单元格设为叠加态 (包含所有可能的 Tile)。
2.  **寻找最小熵**: 找到当前网格中熵最小（可能性最少）但尚未坍缩的单元格。

    *   如果有多个最小熵，随机选一个。
3.  **观测/坍缩**: 根据权重随机选择该单元格的一个状态，将其固定。

4.  **传播**: 

    *   更新该单元格的所有邻居。
    *   如果邻居的可能性减少了，继续更新邻居的邻居 (递归或堆栈)。
    *   如果在传播过程中某个单元格的可能性变为 0 (无解)，则生成失败，需要回溯或重试。
5.  **循环**: 重复步骤 2-4，直到所有单元格都坍缩完成。

---

## 3. 实现指南 (Implementation Guide)

### 3.1 定义 Tile 与 Socket (接口)
为了判断两个 Tile 是否能相邻，我们需要定义它们的边缘接口 (Socket)。

假设我们有 4 个方向：上、下、左、右。

*   **草地 Tile**: `[Grass, Grass, Grass, Grass]`
*   **海岸 Tile**: `[Water, Grass, Coast, Coast]` (假设)

**规则**: Tile A 的“右”接口必须与 Tile B 的“左”接口匹配 (可以是相同 ID，也可以是定义的对称 ID)。

### 3.2 旋转与镜像
为了节省美术资源，我们可以自动生成旋转变体。

*   一个不对称的 Tile 可以生成 4 个旋转版本。
*   接口数据也需要随之旋转。

### 3.3 回溯与重试 (Backtracking)
WFC 可能会遇到“死胡同” (Contradiction)。

*   **简单策略**: 遇到冲突直接清空整个地图重来 (对于小地图非常快)。
*   **高级策略**: 记录每一步的状态，遇到冲突回退到上一步，并标记导致冲突的分支为不可行。

### 3.4 性能优化
*   **最小堆 (Min-Heap)**: 用最小堆维护所有格子的熵，以便 O(1) 取出最小熵格子。
*   **脏标记 (Dirty Flags)**: 传播时只处理受影响的区域。

---

## 4. Unity 代码片段 (伪代码)

```csharp
public class WFCGenerator : MonoBehaviour {
    struct Cell {
        public bool Collapsed;
        public List<Tile> PossibleTiles;
        public int Entropy => PossibleTiles.Count;
    }

    void RunWFC() {
        // 1. Init
        InitializeGrid();

        while (IsAnyCellUncollapsed()) {
            // 2. Find Min Entropy
            Vector2Int coords = GetMinEntropyCell();
            
            // 3. Collapse
            CollapseCell(coords);
            
            // 4. Propagate
            PropagateConstraints(coords);
        }
        
        DrawMap();
    }
    
    void PropagateConstraints(Vector2Int startNode) {
        Stack<Vector2Int> stack = new Stack<Vector2Int>();
        stack.Push(startNode);
        
        while (stack.Count > 0) {
            var current = stack.Pop();
            foreach (var neighbor in GetNeighbors(current)) {
                if (Constrain(current, neighbor)) {
                    stack.Push(neighbor); // 如果邻居被修改了，继续传播
                }
            }
        }
    }
}
```

---

## 5. 业界案例 (Industry Cases)

### Townscaper
*   **特点**: 极其流畅的实时 WFC。
*   **机制**: 玩家点击只是“观测”了一个格子，算法自动计算周围格子的最优解（屋顶、地基、楼梯）。

### Bad North (北方绝境)
*   **特点**: 微型岛屿生成。
*   **应用**: 保证岛屿边缘总是平滑的海岸线，且高低差有梯子连接。

### Caves of Qud
*   **特点**: 极其复杂的文本描述生成。
*   **应用**: 利用 WFC 生成历史传说和地貌描述。

---

## 6. 扩展阅读
*   [Maxim Gumin's Original WFC Repo](https://github.com/mxgmn/WaveFunctionCollapse)
*   [Oskar Stålberg (Townscaper) Talks](https://www.youtube.com/watch?v=0bcZb-SsnrA)


