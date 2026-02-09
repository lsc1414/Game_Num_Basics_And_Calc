# 索敌系统综合指南

> 本文档由以下文件合并生成 (2026-01-09)



---


<!-- 来源: Tech\Mechanics\Targeting_System_DeepDive.md -->

## 🎯 索敌机制详解与实战 (Targeting System Deep Dive)

本文档基于 [Unified Decision System](../Architecture/Unified_Decision_System.md) 架构，深入解析 Project Vampirefall 中的索敌逻辑。索敌（Targeting）是塔防与 ARPG 的核心交互体验，它决定了玩家感受到的“智能”程度。
## 1. 核心原理：从“寻找”到“评分” (From Search to Score)

初级索敌逻辑通常是：“找到最近的敌人”。
但在本作中，索敌是一个 **加权决策过程 (Weighted Decision Process)**。
### 1.1 标准流程
每一次索敌计算 (`Tick`) 都遵循以下管道：
1.  **圈地 (Broad Phase):** 快速获取射程内的所有潜在目标（利用空间划分，如 QuadTree 或 Physics.OverlapSphere）。
2.  **初筛 (Filtering):** 剔除无效目标（无敌状态、隐身状态、已死亡、阻挡视线）。

3.  **评分 (Scoring):** 对剩下的每个目标运行一组 `Scorer`，计算总分。
4.  **择优 (Selection):** 选取分数最高的 Top 1 作为目标。

### 1.2 为什么需要评分制？
*   **防呆:** 防止狙击塔把高额伤害浪费在还有 1HP 的杂兵上（Overkill）。
*   **集火:** 让特定的塔优先攻击被“破甲”或“被标记”的敌人。
*   **风格:** 区分“狂战士”（打最近的）与“刺客”（打最脆的）的行为模式。
## 2. 评分维度详解 (Scoring Dimensions)

我们在代码中通过组合不同的 `IScorer` 来实现复杂的战术逻辑。

### 📏 2.1 距离评分 (Distance Scoring)
*   **逻辑:** 距离越近/越远，分数越高。
*   **曲线:** 建议使用非线性曲线。
    *   `Score = 1 / Distance` (极度偏好近身)
    *   `Score = Distance` (偏好远程，如迫击炮无法攻击近身)
*   **应用:** 基础箭塔、近战怪物。

### 🩸 2.2 生命值评分 (Health Scoring)
*   **低血量优先 (Execute / Cleanup):**
    *   **逻辑:** `Score = 1 - (CurrentHP / MaxHP)`。
    *   **用途:** 快速收割残血，减少场上怪物数量，触发击杀特效。
*   **高血量优先 (Giant Slayer):**
    *   **逻辑:** `Score = CurrentHP` 或 `Score = CurrentHP / MaxHP`。
    *   **用途:** 破甲塔、百分比伤害技能，确保高伤打在肉盾上。

### 👑 2.3 优先级评分 (Priority Scoring)
*   **逻辑:** 根据 `EntityType` 给定固定分值。
*   **配置表:**
    *   `Boss`: 1000分
    *   `Elite`: 500分
    *   `Special (炸弹人)`: 2000分 (绝对优先处理)
    *   `Minion`: 10分
*   **用途:** 所有的塔都应该默认带一点优先级，避免被召唤的小怪吸走火力。

### 🌪️ 2.4 状态协同评分 (Status Synergy Scoring)
*   **逻辑:** “趁你病要你命”。如果目标身上有特定的 Debuff，加分。
    *   **雷电塔:** 对 `[Soaked]` (湿润) 的目标评分 x 2.0。
    *   **处决者:** 对 `[Stunned]` (眩晕) 的目标评分 x 3.0。
*   **用途:** 引导玩家构建元素反应链。

## 3. 实战案例 (Use Cases)
以下是游戏中几种典型单位的索敌配置方案。
### 🏹 Case A: 基础箭塔 (Basic Ballista)
*定位：清理冲到脸上的杂兵，防漏怪。*
|          评分器          |          权重 (Weight)          |          说明          |
|          **DistanceScorer**          |          **3.0**          |          极度优先攻击最近的单位。          |
|          **FixedPriorityScorer**          |          0.5          |          稍微偏好精英怪，但主要还是看距离。          |
|          **HealthScorer (Low)**          |          1.0          |          优先补刀残血。          |
### 🔫 Case B: 狙击塔 (Sniper Turret)
*定位：高单发伤害，极慢攻速。必须避免伤害溢出。*
|          评分器          |          权重 (Weight)          |          说明          |
|          **Filter: Overkill**          |          N/A          |          **[关键]** 如果目标的 `HP < 塔攻击力`，直接剔除（防止大炮打蚊子）。          |
|          **FixedPriorityScorer**          |          **5.0**          |          必须优先打 Boss 和 Elite。          |
|          **HealthScorer (High)**          |          2.0          |          在同级怪物中，选血最多的打。          |
|          **DistanceScorer**          |          -0.5          |          稍微偏好远处的（反向权重），避免转火频繁。          |
### ⚡ Case C: 特斯拉电圈 (Tesla Coil)
*定位：AOE 连锁攻击，依赖元素反应。*
|          评分器          |          权重 (Weight)          |          说明          |
|          **TagSynergyScorer**          |          **4.0**          |          寻找带有 `[Wet]` 或 `[Conductive]` 标签的敌人。          |
|          **ClusterScorer**          |          2.0          |          **[高级]** 寻找周围敌人最密集的那个点作为主目标（最大化弹射收益）。          |
### 👹 Case D: 刺客型怪物 (Assassin Enemy)
*定位：切后排，恶心玩家。*

|          评分器          |          权重 (Weight)          |          说明          |
|          **FixedPriorityScorer**          |          **10.0**          |          `Player` > `SupportTower` > `TankTower`。          |
|          **HealthScorer (Low)**          |          3.0          |          专挑血少的打。          |
|          **DistanceScorer**          |          0.0          |          **无视距离**。哪怕要绕路，也要去切后排。          |
## 4. 代码实现片段 (Implementation Snippet)
如何在 Unity 中配置一个“狙击塔”的决策引擎：
        // 1. 过滤：必须在射程内，且活着
        // 2. 过滤：防止伤害溢出 (Overkill Protection)
        // 假设塔攻击力是 500
        // 3. 评分：优先打 Boss (权重极高)
        // 4. 评分：优先打满血的 (权重中等)
        if (Time.frameCount % 10 == 0) { // 分帧优化

## 5. 性能优化与粘性 (Optimization & Stickiness)
### 5.1 目标粘性 (Target Stickiness)
为了防止塔的炮口在两个分数相近的敌人之间疯狂抽搐（Ping-Pong），我们需要引入“粘性”。
*   **机制:** 给 `LastTarget` (上一次锁定的目标) 一个额外的分数加成。
*   **公式:** `Score += (target == LastTarget) ? StickinessBonus : 0;`
*   **效果:** 除非新目标的威胁值显著高于当前目标（例如超过 20%），否则不切换目标。
### 5.2 空间划分 (Spatial Partitioning)
千万不要遍历全图 `EnemyManager.GetAllEnemies()`。
*   使用 **Grid System** 或 **QuadTree**。
*   塔只获取其 `Range` 覆盖的 Grid 内的敌人列表作为 `Candidates`。
### 5.3 协同程序 (Coroutines) / Job System
索敌不需要每帧都跑。
*   每 0.1秒 ~ 0.2秒 更新一次即可。
*   对于大量单位，使用 Unity Job System 并行计算分数。
<!-- 来源: Tech\Mechanics\Targeting_Pipeline_DeepDive.md -->
## 🎯 索敌管道详解 (Targeting Pipeline Deep Dive)
本文档深入剖析索敌流程的每个阶段，重点关注**性能优化**和**复杂地形处理**。
## 🔄 管道总览 (Pipeline Overview)
索敌不仅仅是 `Distance < Range` 那么简单。一个健壮的索敌管道需要处理几百个单位的高频查询。
    A[Tick Trigger] --> B{空间查询 Broad Phase}
    B -->|Grid/QuadTree| C[候选列表 Candidates]
    C --> D{视线检查 LOS Check}
    D -->|Raycast/Height| E[有效目标 Valid Targets]
    E --> F{评分引擎 Scoring}
    F -->|Weighted Sum| G[最优解 Best Target]
## 1. 圈地 (Broad Phase): 高效的空间查询
这是第一步，也是对性能影响最大的一步。**绝对禁止**使用 `FindObjectsOfType` 或遍历全图 `List<Enemy>`。
### 1.1 2D 地图方案 (Grid System)
如果游戏地形平坦（标准塔防或俯视角 Roguelike），推荐使用 **均匀网格 (Uniform Grid)**。
*   **原理:** 将地图划分为 2x2 或 5x5 的格子。每个格子维护一个 `List<Unit>`。
*   **写入:** 单位移动时，更新自己所在的格子索引。
*   **查询:** 塔只需要查询自己射程圆圈覆盖的几个格子。
*   **优势:** 
    *   插入/删除极其快 O(1)。
    *   内存访问连续，缓存友好。
    *   比 QuadTree 更适合单位频繁移动的场景。

### 1.2 3D 地形/稀疏地图方案 (QuadTree / Octree)
如果地图非常大且空旷，或者有显著的垂直结构（如空中单位），网格法会浪费大量内存。
*   **QuadTree (四叉树):** 适合大多数地面 3D 游戏。
*   **Octree (八叉树):** 仅当你有大量飞行单位且需要区分上下层时使用。
*   **Unity 特有:** `Physics.OverlapSphereNonAlloc`。
    *   这是利用 Unity 底层 PhysX 引擎的加速结构。
    *   **技巧:** 使用 `NonAlloc` 版本避免 GC。
    *   **LayerMask:** 务必设置 LayerMask 仅检测 `EnemyLayer`，避免检测墙壁或地面。
### 1.3 优化技巧：分帧与缓存
*   **频率限制:** 索敌不需要每帧跑。每 0.2秒 (10-12帧) 跑一次足够。
*   **交错执行 (Interleaving):**
    *   Frame 1: 塔 A, B, C 索敌。
    *   Frame 2: 塔 D, E, F 索敌。
    *   通过 `Time.frameCount % TotalGroups == GroupIndex` 来实现。
## 2. 视线检查 (Line of Sight - LOS): 处理地形遮挡
在复杂的 3D 地图中，"在射程内" 不等于 "能打到"。墙壁、悬崖、障碍物都会阻挡攻击。
### 2.1 2D / 伪3D (Top-Down)
*   **Raycast:** 从塔中心向目标发射一条射线。
*   **Layer:** 射线只与 `Wall` / `Obstacle` 层碰撞。
*   **高度差模拟:** 即使是 2D，也可以给单位一个 `Height` 属性。
    *   规则: `Target.Height >= Wall.Height` 视为可见（例如飞行单位飞过城墙）。
### 2.2 真 3D 高低差 (Elevation)
这是最复杂的部分。
*   **视点修正 (Eye Position):** 射线起点不是 `Tower.position` (脚底)，而是 `Tower.MuzzlePoint` (炮口)。终点是 `Enemy.Center` (胸口)。
*   **俯仰角限制 (Pitch Limit):**
    *   坦克炮塔可能无法抬起超过 45度。
    *   检查: `Vector3.Angle(TowerForward, DirectionToEnemy) < MaxPitch`。
*   **死角 (Blind Spot):**
    *   位于高台上的塔，可能打不到脚底下的敌人（灯下黑）。
    *   逻辑: `HorizontalDistance > MinRange`。

## 3. 实例分析：高低差对战 (Case Study)
假设场景：玩家站在高台上，下方有一群僵尸。
### 3.1 玩家 (High Ground) -> 僵尸 (Low Ground)
1.  **Broad Phase:** `OverlapSphere` 扫到了僵尸。
2.  **LOS Check:** 射线从高台边缘射向僵尸，未被遮挡。通过。

3.  **Range Check:** 3D 距离 `sqrt(dx*dx + dy*dy + dz*dz)` 可能大于 2D 投影距离。
    *   *设计决策:* 你的射程是按“球体”算还是按“圆柱体”算？
    *   *建议:* 使用球体距离，才符合物理直觉。
### 3.2 僵尸 (Low Ground) -> 玩家 (High Ground)
1.  **Broad Phase:** 扫到了玩家。
2.  **LOS Check:** 射线被高台边缘挡住了（如果僵尸太靠近墙根）。
3.  **NavMesh:** 僵尸发现虽然直线距离近，但寻路距离 (Path Distance) 极远（需要绕路上楼）。
    *   *决策:* 仇恨系统应使用 **寻路距离** 还是 **直线距离**？
    *   *答案:* **混合权重**。如果直线距离很近但打不到，AI 应该倾向于寻找路径上楼，或者切换目标攻击墙壁。
## 4. 过滤与评分 (Filtering & Scoring)
### 4.1 硬过滤 (Hard Filters)
在评分之前，先用廉价的运算剔除 90% 的目标。
*   `IsAlive`: 必须。
*   `IsStealthed`: 隐身单位除非有反隐塔，否则直接剔除。
*   `AngleCheck`: 某些塔只能攻击前方 90 度扇形区域。
### 4.2 软评分 (Soft Scoring)
进入这里的通常只有 3-5 个目标。
*   **性能敏感:** 这里是数学密集区。
*   **避免:** 不要在 `Evaluate` 里做 `GetComponent` 或 `Find`。数据应预取到 `Context` 中。
*   **SIMD 优化:** 如果单位极多，可以将位置数据放入 `NativeArray<float3>`，用 Unity Job System 并行计算距离分数。

*   **å¬å¼:** `Score += (target == LastTarget) ? StickinessBonus : 0;`
*   **ææ:** é¤éæ°ç®æ çå¨èå¼æ¾èé«äºå½åç®æ ï¼ä¾å¦è¶è¿ 20%ï¼ï¼å¦åä¸åæ¢ç®æ ã?

### 5.2 ç©ºé´åå (Spatial Partitioning)
åä¸ä¸è¦éåå¨å¾ `EnemyManager.GetAllEnemies()`ã?

*   ä½¿ç¨ **Grid System** æ?**QuadTree**ã?
*   å¡åªè·åå?`Range` è¦çç?Grid åçæäººåè¡¨ä½ä¸º `Candidates`ã?

### 5.3 ååç¨åº (Coroutines) / Job System
ç´¢æä¸éè¦æ¯å¸§é½è·ã?

*   æ¯?0.1ç§?~ 0.2ç§?æ´æ°ä¸æ¬¡å³å¯ã?
*   å¯¹äºå¤§éåä½ï¼ä½¿ç?Unity Job System å¹¶è¡è®¡ç®åæ°ã?

---




---


{/* æ¥æº: Tech\Mechanics\Targeting_Pipeline_DeepDive.md */}

## ð¯ ç´¢æç®¡éè¯¦è§£ (Targeting Pipeline Deep Dive)

æ¬ææ¡£æ·±å¥åæç´¢ææµç¨çæ¯ä¸ªé¶æ®µï¼éç¹å³æ³?*æ§è½ä¼å**å?*å¤æå°å½¢å¤ç**ã?

---

## ð ç®¡éæ»è§ (Pipeline Overview)

ç´¢æä¸ä»ä»æ¯ `Distance < Range` é£ä¹ç®åãä¸ä¸ªå¥å£®çç´¢æç®¡ééè¦å¤çå ç¾ä¸ªåä½çé«é¢æ¥è¯¢ã?

```mermaid
graph TD
    A[Tick Trigger] */} B{ç©ºé´æ¥è¯¢ Broad Phase}
    B */}|Grid/QuadTree| C[åéåè¡?Candidates]
    C */} D{è§çº¿æ£æ?LOS Check}
    D */}|Raycast/Height| E[ææç®æ  Valid Targets]
    E */} F{è¯åå¼æ Scoring}
    F */}|Weighted Sum| G[æä¼è§£ Best Target]
```

---

## 1. åå° (Broad Phase): é«æçç©ºé´æ¥è¯?

è¿æ¯ç¬¬ä¸æ­¥ï¼ä¹æ¯å¯¹æ§è½å½±åæå¤§çä¸æ­¥ã?*ç»å¯¹ç¦æ­¢**ä½¿ç¨ `FindObjectsOfType` æéåå¨å?`List<Enemy>`ã?

### 1.1 2D å°å¾æ¹æ¡ (Grid System)
å¦ææ¸¸æå°å½¢å¹³å¦ï¼æ åå¡é²æä¿¯è§è§?Roguelikeï¼ï¼æ¨èä½¿ç¨ **ååç½æ ¼ (Uniform Grid)**ã?

*   **åç:** å°å°å¾ååä¸º 2x2 æ?5x5 çæ ¼å­ãæ¯ä¸ªæ ¼å­ç»´æ¤ä¸ä¸?`List<Unit>`ã?
*   **åå¥:** åä½ç§»å¨æ¶ï¼æ´æ°èªå·±æå¨çæ ¼å­ç´¢å¼ã?
*   **æ¥è¯¢:** å¡åªéè¦æ¥è¯¢èªå·±å°ç¨ååè¦ççå ä¸ªæ ¼å­ã?
*   **ä¼å¿:** 
    *   æå¥/å é¤æå¶å¿?O(1)ã?
    *   åå­è®¿é®è¿ç»­ï¼ç¼å­åå¥½ã?
    *   æ¯?QuadTree æ´éååä½é¢ç¹ç§»å¨çåºæ¯ã?

### 1.2 3D å°å½¢/ç¨çå°å¾æ¹æ¡?(QuadTree / Octree)
å¦æå°å¾éå¸¸å¤§ä¸ç©ºæ·ï¼æèææ¾èçåç´ç»æï¼å¦ç©ºä¸­åä½ï¼ï¼ç½æ ¼æ³ä¼æµªè´¹å¤§éåå­ã?

*   **QuadTree (ååæ ?:** éåå¤§å¤æ°å°é?3D æ¸¸æã?
*   **Octree (å«åæ ?:** ä»å½ä½ æå¤§éé£è¡åä½ä¸éè¦åºåä¸ä¸å±æ¶ä½¿ç¨ã?
*   **Unity ç¹æ:** `Physics.OverlapSphereNonAlloc`ã?
    *   è¿æ¯å©ç¨ Unity åºå± PhysX å¼æçå éç»æã?
    *   **æå·?** ä½¿ç¨ `NonAlloc` çæ¬é¿å GCã?
    *   **LayerMask:** å¡å¿è®¾ç½® LayerMask ä»æ£æµ?`EnemyLayer`ï¼é¿åæ£æµå¢å£æå°é¢ã?

### 1.3 ä¼åæå·§ï¼åå¸§ä¸ç¼å­?
*   **é¢çéå¶:** ç´¢æä¸éè¦æ¯å¸§è·ãæ¯ 0.2ç§?(10-12å¸? è·ä¸æ¬¡è¶³å¤ã?
*   **äº¤éæ§è¡ (Interleaving):**
    *   Frame 1: å¡?A, B, C ç´¢æã?
    *   Frame 2: å¡?D, E, F ç´¢æã?
    *   éè¿ `Time.frameCount % TotalGroups == GroupIndex` æ¥å®ç°ã?

---

## 2. è§çº¿æ£æ?(Line of Sight - LOS): å¤çå°å½¢é®æ¡

å¨å¤æç 3D å°å¾ä¸­ï¼"å¨å°ç¨å" ä¸ç­äº?"è½æå?ãå¢å£ãæ¬å´ãéç¢ç©é½ä¼é»æ¡æ»å»ã?

### 2.1 2D / ä¼?D (Top-Down)
*   **Raycast:** ä»å¡ä¸­å¿åç®æ åå°ä¸æ¡å°çº¿ã?
*   **Layer:** å°çº¿åªä¸ `Wall` / `Obstacle` å±ç¢°æã?
*   **é«åº¦å·®æ¨¡æ?** å³ä½¿æ?2Dï¼ä¹å¯ä»¥ç»åä½ä¸ä¸?`Height` å±æ§ã?
    *   è§å: `Target.Height >= Wall.Height` è§ä¸ºå¯è§ï¼ä¾å¦é£è¡åä½é£è¿åå¢ï¼ã?

### 2.2 ç?3D é«ä½å·?(Elevation)
è¿æ¯æå¤æçé¨åã?

*   **è§ç¹ä¿®æ­£ (Eye Position):** å°çº¿èµ·ç¹ä¸æ¯ `Tower.position` (èåº)ï¼èæ¯ `Tower.MuzzlePoint` (ç®å£)ãç»ç¹æ¯ `Enemy.Center` (è¸å£)ã?
*   **ä¿¯ä»°è§éå?(Pitch Limit):**
    *   å¦åç®å¡å¯è½æ æ³æ¬èµ·è¶è¿ 45åº¦ã?
    *   æ£æ? `Vector3.Angle(TowerForward, DirectionToEnemy) < MaxPitch`ã?
*   **æ­»è§ (Blind Spot):**
    *   ä½äºé«å°ä¸çå¡ï¼å¯è½æä¸å°èåºä¸çæäººï¼ç¯ä¸é»ï¼ã?
    *   é»è¾: `HorizontalDistance > MinRange`ã?

---

## 3. å®ä¾åæï¼é«ä½å·®å¯¹æ (Case Study)

åè®¾åºæ¯ï¼ç©å®¶ç«å¨é«å°ä¸ï¼ä¸æ¹æä¸ç¾¤åµå°¸ã?

### 3.1 ç©å®¶ (High Ground) -> åµå°¸ (Low Ground)
1.  **Broad Phase:** `OverlapSphere` æ«å°äºåµå°¸ã?
2.  **LOS Check:** å°çº¿ä»é«å°è¾¹ç¼å°ååµå°¸ï¼æªè¢«é®æ¡ãéè¿ã?

3.  **Range Check:** 3D è·ç¦» `sqrt(dx*dx + dy*dy + dz*dz)` å¯è½å¤§äº 2D æå½±è·ç¦»ã?

    *   *è®¾è®¡å³ç­:* ä½ çå°ç¨æ¯æâçä½âç®è¿æ¯æâåæ±ä½âç®ï¼?
    *   *å»ºè®®:* ä½¿ç¨çä½è·ç¦»ï¼æç¬¦åç©çç´è§ã?

### 3.2 åµå°¸ (Low Ground) -> ç©å®¶ (High Ground)
1.  **Broad Phase:** æ«å°äºç©å®¶ã?
2.  **LOS Check:** å°çº¿è¢«é«å°è¾¹ç¼æ¡ä½äºï¼å¦æåµå°¸å¤ªé è¿å¢æ ¹ï¼ã?

3.  **NavMesh:** åµå°¸åç°è½ç¶ç´çº¿è·ç¦»è¿ï¼ä½å¯»è·¯è·ç¦?(Path Distance) æè¿ï¼éè¦ç»è·¯ä¸æ¥¼ï¼ã?

    *   *å³ç­:* ä»æ¨ç³»ç»åºä½¿ç?**å¯»è·¯è·ç¦»** è¿æ¯ **ç´çº¿è·ç¦»**ï¼?
    *   *ç­æ¡:* **æ··åæé**ãå¦æç´çº¿è·ç¦»å¾è¿ä½æä¸å°ï¼AI åºè¯¥å¾åäºå¯»æ¾è·¯å¾ä¸æ¥¼ï¼æèåæ¢ç®æ æ»å»å¢å£ã?

---

## 4. è¿æ»¤ä¸è¯å?(Filtering & Scoring)

### 4.1 ç¡¬è¿æ»?(Hard Filters)
å¨è¯åä¹åï¼åç¨å»ä»·çè¿ç®åé?90% çç®æ ã?

*   `IsAlive`: å¿é¡»ã?
*   `IsStealthed`: éèº«åä½é¤éæåéå¡ï¼å¦åç´æ¥åé¤ã?
*   `AngleCheck`: æäºå¡åªè½æ»å»åæ?90 åº¦æå½¢åºåã?

### 4.2 è½¯è¯å?(Soft Scoring)
è¿å¥è¿éçéå¸¸åªæ 3-5 ä¸ªç®æ ã?

*   **æ§è½ææ:** è¿éæ¯æ°å­¦å¯éåºã?
*   **é¿å:** ä¸è¦å?`Evaluate` éå `GetComponent` æ?`Find`ãæ°æ®åºé¢åå?`Context` ä¸­ã?
*   **SIMD ä¼å:** å¦æåä½æå¤ï¼å¯ä»¥å°ä½ç½®æ°æ®æ¾å¥ `NativeArray<float3>`ï¼ç¨ Unity Job System å¹¶è¡è®¡ç®è·ç¦»åæ°ã?

---




