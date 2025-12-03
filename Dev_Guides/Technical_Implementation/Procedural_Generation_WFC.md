# 波函数坍缩 (WFC) 生成 (Wave Function Collapse)

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
