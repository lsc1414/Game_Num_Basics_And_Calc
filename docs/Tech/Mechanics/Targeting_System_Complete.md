---
sidebarTitle: "索敌系统综合指南"
---

# 索敌系统综合指南

> 本文档由以下文件合并生成 (2026-01-09)



---


{/* 来源: Tech\Mechanics\Targeting_System_DeepDive.md */}

## 🎯 索敌机制详解与实�?(Targeting System Deep Dive)

本文档基�?[Unified Decision System](../Architecture/Unified_Decision_System.md) 架构，深入解�?Project Vampirefall 中的索敌逻辑。索敌（Targeting）是塔防�?ARPG 的核心交互体验，它决定了玩家感受到的“智能”程度�?

---

## 1. 核心原理：从“寻找”到“评分�?(From Search to Score)

初级索敌逻辑通常是：“找到最近的敌人”�?
但在本作中，索敌是一�?**加权决策过程 (Weighted Decision Process)**�?

### 1.1 标准流程
每一次索敌计�?(`Tick`) 都遵循以下管道：

1.  **圈地 (Broad Phase):** 快速获取射程内的所有潜在目标（利用空间划分，如 QuadTree �?Physics.OverlapSphere）�?
2.  **初筛 (Filtering):** 剔除无效目标（无敌状态、隐身状态、已死亡、阻挡视线）�?

3.  **评分 (Scoring):** 对剩下的每个目标运行一�?`Scorer`，计算总分�?

4.  **择优 (Selection):** 选取分数最高的 Top 1 作为目标�?

### 1.2 为什么需要评分制�?
*   **防呆:** 防止狙击塔把高额伤害浪费在还�?1HP 的杂兵上（Overkill）�?
*   **集火:** 让特定的塔优先攻击被“破甲”或“被标记”的敌人�?
*   **风格:** 区分“狂战士”（打最近的）与“刺客”（打最脆的）的行为模式�?

---

## 2. 评分维度详解 (Scoring Dimensions)

我们在代码中通过组合不同�?`IScorer` 来实现复杂的战术逻辑�?

### 📏 2.1 距离评分 (Distance Scoring)
*   **逻辑:** 距离越近/越远，分数越高�?
*   **曲线:** 建议使用非线性曲线�?
    *   `Score = 1 / Distance` (极度偏好近身)
    *   `Score = Distance` (偏好远程，如迫击炮无法攻击近�?
*   **应用:** 基础箭塔、近战怪物�?

### 🩸 2.2 生命值评�?(Health Scoring)
*   **低血量优�?(Execute / Cleanup):**
    *   **逻辑:** `Score = 1 - (CurrentHP / MaxHP)`�?
    *   **用�?** 快速收割残血，减少场上怪物数量，触发击杀特效�?
*   **高血量优�?(Giant Slayer):**
    *   **逻辑:** `Score = CurrentHP` �?`Score = CurrentHP / MaxHP`�?
    *   **用�?** 破甲塔、百分比伤害技能，确保高伤打在肉盾上�?

### 👑 2.3 优先级评�?(Priority Scoring)
*   **逻辑:** 根据 `EntityType` 给定固定分值�?
*   **配置�?**
    *   `Boss`: 1000�?
    *   `Elite`: 500�?
    *   `Special (炸弹�?`: 2000�?(绝对优先处理)
    *   `Minion`: 10�?
*   **用�?** 所有的塔都应该默认带一点优先级，避免被召唤的小怪吸走火力�?

### 🌪�?2.4 状态协同评�?(Status Synergy Scoring)
*   **逻辑:** “趁你病要你命”。如果目标身上有特定�?Debuff，加分�?
*   **Combo:**
    *   **雷电�?** �?`[Soaked]` (湿润) 的目标评�?x 2.0�?
    *   **处决�?** �?`[Stunned]` (眩晕) 的目标评�?x 3.0�?
*   **用�?** 引导玩家构建元素反应链�?

---

## 3. 实战案例 (Use Cases)

以下是游戏中几种典型单位的索敌配置方案�?

### 🏹 Case A: 基础箭塔 (Basic Ballista)
*定位：清理冲到脸上的杂兵，防漏怪�?

|          评分�?         |          权重 (Weight)          |          说明          |
|          :---          |          :---          |          :---          |
|          **DistanceScorer**          |          **3.0**          |          极度优先攻击最近的单位�?         |
|          **FixedPriorityScorer**          |          0.5          |          稍微偏好精英怪，但主要还是看距离�?         |
|          **HealthScorer (Low)**          |          1.0          |          优先补刀残血�?         |

### 🔫 Case B: 狙击�?(Sniper Turret)
*定位：高单发伤害，极慢攻速。必须避免伤害溢出�?

|          评分�?         |          权重 (Weight)          |          说明          |
|          :---          |          :---          |          :---          |
|          **Filter: Overkill**          |          N/A          |          **[关键]** 如果目标�?`HP < 塔攻击力`，直接剔除（防止大炮打蚊子）�?         |
|          **FixedPriorityScorer**          |          **5.0**          |          必须优先�?Boss �?Elite�?         |
|          **HealthScorer (High)**          |          2.0          |          在同级怪物中，选血最多的打�?         |
|          **DistanceScorer**          |          -0.5          |          稍微偏好远处的（反向权重），避免转火频繁�?         |

### �?Case C: 特斯拉电�?(Tesla Coil)
*定位：AOE 连锁攻击，依赖元素反应�?

|          评分�?         |          权重 (Weight)          |          说明          |
|          :---          |          :---          |          :---          |
|          **TagSynergyScorer**          |          **4.0**          |          寻找带有 `[Wet]` �?`[Conductive]` 标签的敌人�?         |
|          **ClusterScorer**          |          2.0          |          **[高级]** 寻找周围敌人最密集的那个点作为主目标（最大化弹射收益）�?         |

### 👹 Case D: 刺客型怪物 (Assassin Enemy)
*定位：切后排，恶心玩家�?

|          评分�?         |          权重 (Weight)          |          说明          |
|          :---          |          :---          |          :---          |
|          **FixedPriorityScorer**          |          **10.0**          |          `Player` > `SupportTower` > `TankTower`�?         |
|          **HealthScorer (Low)**          |          3.0          |          专挑血少的打�?         |
|          **DistanceScorer**          |          0.0          |          **无视距离**。哪怕要绕路，也要去切后排�?         |

---

## 4. 代码实现片段 (Implementation Snippet)

如何�?Unity 中配置一个“狙击塔”的决策引擎�?

```csharp
public class SniperTower : MonoBehaviour 
{
    private DecisionEngine<Enemy> _targetingSystem;
    
    void Start() {
        _targetingSystem = new DecisionEngine<Enemy>();
        
        // 1. 过滤：必须在射程内，且活着
        _targetingSystem.AddFilter(new RangeFilter(transform, 50f));
        _targetingSystem.AddFilter(new AliveFilter());
        
        // 2. 过滤：防止伤害溢�?(Overkill Protection)
        // 假设塔攻击力�?500
        _targetingSystem.AddFilter(new MinHealthFilter(500f)); 

        // 3. 评分：优先打 Boss (权重极高)
        _targetingSystem.AddScorer(new EntityTypeScorer()
            .SetScore(EntityType.Boss, 1000f)
            .SetScore(EntityType.Elite, 500f));

        // 4. 评分：优先打满血�?(权重中等)
        _targetingSystem.AddScorer(new HealthScorer(HealthScorerMode.Highest, 10f));
    }

    void Update() {
        \text{if} (Time.frameCount % 10 == 0) { // 分帧优化
            var enemies = EnemyManager.GetAllEnemies();
            var target = _targetingSystem.SelectBest(enemies, GetContext());
            \text{if} (target != null) Fire(target);
        }
    }
}
```

## 5. 性能优化与粘�?(Optimization & Stickiness)

### 5.1 目标粘�?(Target Stickiness)
为了防止塔的炮口在两个分数相近的敌人之间疯狂抽搐（Ping-Pong），我们需要引入“粘性”�?

*   **机制:** �?`LastTarget` (上一次锁定的目标) 一个额外的分数加成�?
*   **公式:** `Score += (target == LastTarget) ? StickinessBonus : 0;`
*   **效果:** 除非新目标的威胁值显著高于当前目标（例如超过 20%），否则不切换目标�?

### 5.2 空间划分 (Spatial Partitioning)
千万不要遍历全图 `EnemyManager.GetAllEnemies()`�?

*   使用 **Grid System** �?**QuadTree**�?
*   塔只获取�?`Range` 覆盖�?Grid 内的敌人列表作为 `Candidates`�?

### 5.3 协同程序 (Coroutines) / Job System
索敌不需要每帧都跑�?

*   �?0.1�?~ 0.2�?更新一次即可�?
*   对于大量单位，使�?Unity Job System 并行计算分数�?

---




---


{/* 来源: Tech\Mechanics\Targeting_Pipeline_DeepDive.md */}

## 🎯 索敌管道详解 (Targeting Pipeline Deep Dive)

本文档深入剖析索敌流程的每个阶段，重点关�?*性能优化**�?*复杂地形处理**�?

---

## 🔄 管道总览 (Pipeline Overview)

索敌不仅仅是 `Distance < Range` 那么简单。一个健壮的索敌管道需要处理几百个单位的高频查询�?

```mermaid
graph TD
    A[Tick Trigger] */} B{空间查询 Broad Phase}
    B */}|Grid/QuadTree| C[候选列�?Candidates]
    C */} D{视线检�?LOS Check}
    D */}|Raycast/Height| E[有效目标 Valid Targets]
    E */} F{评分引擎 Scoring}
    F */}|Weighted Sum| G[最优解 Best Target]
```

---

## 1. 圈地 (Broad Phase): 高效的空间查�?

这是第一步，也是对性能影响最大的一步�?*绝对禁止**使用 `FindObjectsOfType` 或遍历全�?`List<Enemy>`�?

### 1.1 2D 地图方案 (Grid System)
如果游戏地形平坦（标准塔防或俯视�?Roguelike），推荐使用 **均匀网格 (Uniform Grid)**�?

*   **原理:** 将地图划分为 2x2 �?5x5 的格子。每个格子维护一�?`List<Unit>`�?
*   **写入:** 单位移动时，更新自己所在的格子索引�?
*   **查询:** 塔只需要查询自己射程圆圈覆盖的几个格子�?
*   **优势:** 
    *   插入/删除极其�?O(1)�?
    *   内存访问连续，缓存友好�?
    *   �?QuadTree 更适合单位频繁移动的场景�?

### 1.2 3D 地形/稀疏地图方�?(QuadTree / Octree)
如果地图非常大且空旷，或者有显著的垂直结构（如空中单位），网格法会浪费大量内存�?

*   **QuadTree (四叉�?:** 适合大多数地�?3D 游戏�?
*   **Octree (八叉�?:** 仅当你有大量飞行单位且需要区分上下层时使用�?
*   **Unity 特有:** `Physics.OverlapSphereNonAlloc`�?
    *   这是利用 Unity 底层 PhysX 引擎的加速结构�?
    *   **技�?** 使用 `NonAlloc` 版本避免 GC�?
    *   **LayerMask:** 务必设置 LayerMask 仅检�?`EnemyLayer`，避免检测墙壁或地面�?

### 1.3 优化技巧：分帧与缓�?
*   **频率限制:** 索敌不需要每帧跑。每 0.2�?(10-12�? 跑一次足够�?
*   **交错执行 (Interleaving):**
    *   Frame 1: �?A, B, C 索敌�?
    *   Frame 2: �?D, E, F 索敌�?
    *   通过 `Time.frameCount % TotalGroups == GroupIndex` 来实现�?

---

## 2. 视线检�?(Line of Sight - LOS): 处理地形遮挡

在复杂的 3D 地图中，"在射程内" 不等�?"能打�?。墙壁、悬崖、障碍物都会阻挡攻击�?

### 2.1 2D / �?D (Top-Down)
*   **Raycast:** 从塔中心向目标发射一条射线�?
*   **Layer:** 射线只与 `Wall` / `Obstacle` 层碰撞�?
*   **高度差模�?** 即使�?2D，也可以给单位一�?`Height` 属性�?
    *   规则: `Target.Height >= Wall.Height` 视为可见（例如飞行单位飞过城墙）�?

### 2.2 �?3D 高低�?(Elevation)
这是最复杂的部分�?

*   **视点修正 (Eye Position):** 射线起点不是 `Tower.position` (脚底)，而是 `Tower.MuzzlePoint` (炮口)。终点是 `Enemy.Center` (胸口)�?
*   **俯仰角限�?(Pitch Limit):**
    *   坦克炮塔可能无法抬起超过 45度�?
    *   检�? `Vector3.Angle(TowerForward, DirectionToEnemy) < MaxPitch`�?
*   **死角 (Blind Spot):**
    *   位于高台上的塔，可能打不到脚底下的敌人（灯下黑）�?
    *   逻辑: `HorizontalDistance > MinRange`�?

---

## 3. 实例分析：高低差对战 (Case Study)

假设场景：玩家站在高台上，下方有一群僵尸�?

### 3.1 玩家 (High Ground) -> 僵尸 (Low Ground)
1.  **Broad Phase:** `OverlapSphere` 扫到了僵尸�?
2.  **LOS Check:** 射线从高台边缘射向僵尸，未被遮挡。通过�?

3.  **Range Check:** 3D 距离 `\text{sqrt}(dx*dx + dy*dy + dz*dz)` 可能大于 2D 投影距离�?

    *   *设计决策:* 你的射程是按“球体”算还是按“圆柱体”算�?
    *   *建议:* 使用球体距离，才符合物理直觉�?

### 3.2 僵尸 (Low Ground) -> 玩家 (High Ground)
1.  **Broad Phase:** 扫到了玩家�?
2.  **LOS Check:** 射线被高台边缘挡住了（如果僵尸太靠近墙根）�?

3.  **NavMesh:** 僵尸发现虽然直线距离近，但寻路距�?(Path Distance) 极远（需要绕路上楼）�?

    *   *决策:* 仇恨系统应使�?**寻路距离** 还是 **直线距离**�?
    *   *答案:* **混合权重**。如果直线距离很近但打不到，AI 应该倾向于寻找路径上楼，或者切换目标攻击墙壁�?

---

## 4. 过滤与评�?(Filtering & Scoring)

### 4.1 硬过�?(Hard Filters)
在评分之前，先用廉价的运算剔�?90% 的目标�?

*   `IsAlive`: 必须�?
*   `IsStealthed`: 隐身单位除非有反隐塔，否则直接剔除�?
*   `AngleCheck`: 某些塔只能攻击前�?90 度扇形区域�?

### 4.2 软评�?(Soft Scoring)
进入这里的通常只有 3-5 个目标�?

*   **性能敏感:** 这里是数学密集区�?
*   **避免:** 不要�?`Evaluate` 里做 `GetComponent` �?`Find`。数据应预取�?`Context` 中�?
*   **SIMD 优化:** 如果单位极多，可以将位置数据放入 `NativeArray<float3>`，用 Unity Job System 并行计算距离分数�?

---




