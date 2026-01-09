---
sidebarTitle: "🗺️ 关卡与波次设计指南"
---

# 🗺️ 关卡与波次设计指南

本文档指导如何构建游戏地图以及控制刷怪节奏 (Pacing)。

---

## 1. 地图生成逻辑 (Map Generation)

本作不使用完全随机的迷宫，而采用 **“模块化拼图” (Modular Tiles)** 系统，兼顾战术深度与随机性。

### 1.1 核心结构

- **基地 (Hub):** 地图中心，不可破坏，玩家必须守护的核心。
- **主路 (Lanes):** 连接刷怪点 (Spawners) 和基地的主要路径。
- **空地 (Plots):** 允许玩家建造防御塔的区域。
  - _高地 (High Ground):_ 放置在此处的塔获得 +20% 射程。
  - _能量节点 (Power Nodes):_ 放置在此处的塔攻速 +30%，但造价翻倍。

### 1.2 地形阻挡与迷宫 (Mazing)

- 地图初始是开放的。
- 玩家可以通过建造“墙壁”或“阻挡塔”来改变怪物的寻路。
- **限制:** 系统必须保证至少有一条从刷怪点到基地的通路（不能完全堵死）。如果完全堵死，怪物进入“狂暴模式”，攻击力翻倍并开始拆墙。

## 2. 波次节奏控制 (Wave Pacing)

一局游戏标准时长为 20 分钟，分为若干波次。

### 2.1 强度曲线 (Intensity Curve)

- 采用 **正弦波** 模式：
  - _Build Up:_ 少量杂兵，给玩家送钱造塔。
  - _Peak:_ 高密度刷怪，混合精英。
  - _Climax:_ Boss 战或超高压波次。
  - _Rest:_ 只有零星小怪，给玩家整理装备、升级塔的时间。

### 2.2 刷怪配置 (Spawn Patterns)

- **线性流 (Stream):** 连续不断地刷单一兵种。测试单体输出。
- **爆发流 (Burst):** 瞬间刷出一大群低血量怪。测试 AoE 能力。
- **钳形攻势 (Pincer):** 两个相反方向的刷怪点同时激活。强迫玩家分兵或构建全向防御。

## 3. 动态难度调整 (Dynamic Difficulty - Director)

参考《求生之路》的 AI Director。

- **监测指标:** 玩家血量、塔的损毁率、DPS 统计。
- **调整:**
  - 如果玩家过于轻松（满血，塔未受损），下一波提前刷新，或者增加精英怪数量。
  - 如果玩家濒死，下一波刷怪间隔延长，或掉落回复球。

## 4. 地图事件 (Map Events)

为了打破枯燥，随机触发地图事件。

- **血月 (Blood Moon):** 所有怪物攻速 +30%，但掉落稀有度提升。
- **虚空裂隙 (Void Rift):** 地图随机位置开启传送门，刷出偷袭基地的怪物。玩家必须去关闭它。
- **流浪商队 (Wandering Trader):** 一个无敌的 NPC 经过地图，玩家可以购买急需的消耗品。

---

## 5. 敌人 AI 寻路系统 (Enemy Pathfinding)

### 5.1 寻路算法选择

**Unity NavMesh vs A\* vs Flow Field**

| 算法              | 适用场景                       | 优点                   | 缺点                     |
| ----------------- | ------------------------------ | ---------------------- | ------------------------ |
| **Unity NavMesh** | 地形复杂，怪物数量 < 100       | 自动烘焙，支持动态障碍 | 移动端性能差             |
| **A\***           | 网格地图，中等数量敌人         | 精确路径，易于理解     | 大量敌人时 CPU 消耗高    |
| **Flow Field**    | 大量敌人 (>500) 向同一目标移动 | 极高性能，适合塔防     | 实现复杂，不支持个体差异 |

**推荐方案**: 使用 **Flow Field** 作为主要算法。

### 5.2 Flow Field 原理

**核心思想**: 预先计算地图上每个格子的"流向"，所有怪物只需查表移动。

```csharp
// 1. 从目标点（基地）开始，反向 BFS
public void GenerateFlowField(Vector2Int goal)
{
    Queue<Vector2Int> queue = new Queue<Vector2Int>();
    queue.Enqueue(goal);
    distanceField[goal.x, goal.y] = 0;

    while (queue.Count > 0)
    {
        Vector2Int current = queue.Dequeue();
        foreach (Vector2Int neighbor in GetNeighbors(current))
        {
            if (IsWalkable(neighbor))
            {
                int newDist = distanceField[current.x, current.y] + 1;
                if (newDist < distanceField[neighbor.x, neighbor.y])
                {
                    distanceField[neighbor.x, neighbor.y] = newDist;
                    queue.Enqueue(neighbor);
                }
            }
        }
    }

    // 2. 根据距离场生成流向
    GenerateVectorField();
}

// 3. 怪物移动：直接查表
public Vector3 GetFlowDirection(Vector3 position)
{
    Vector2Int gridPos = WorldToGrid(position);
    return flowField[gridPos.x, gridPos.y];
}
```

**性能优化**:

- 只在地图变化时（玩家建塔/拆塔）重新计算。
- 使用 Job System + Burst Compiler 并行化计算。

### 5.3 动态阻挡处理

**问题**: 玩家建塔后，怪物的路径可能被堵死。

**解决方案**:

```csharp
public bool CanPlaceTower(Vector2Int position)
{
    // 临时标记这个格子为阻挡
    SetBlocked(position, true);

    // 重新计算 Flow Field
    GenerateFlowField(basePosition);

    // 检查所有刷怪点是否还能到达基地
    foreach (Vector2Int spawner in spawnerPositions)
    {
        if (distanceField[spawner.x, spawner.y] == int.MaxValue)
        {
            // 无法到达，不允许建塔
            SetBlocked(position, false);
            return false;
        }
    }

    return true;
}
```

> [!WARNING] > **狂暴模式触发条件**
>
> 如果玩家通过某种方式（如 Bug）完全堵死路径，怪物会进入**狂暴模式**：
>
> - 攻击力 +100%
> - 移速 +50%
> - 优先攻击阻挡物（塔或墙）
> - 持续破坏直到开辟出新路径

---

## 6. 波次编辑器详细配置 (Wave Editor)

### 6.1 波次类型 (Wave Type)

**定义不同的波次模板**:

```json
{
  "wave_types": {
    "Standard": {
      "enemy_count_range": [20, 50],
      "spawn_interval": 1.0,
      "spawner_count": 1
    },
    "Burst": {
      "enemy_count_range": [100, 200],
      "spawn_interval": 0.1,
      "spawner_count": 1,
      "description": "瞬间刷出大量弱怪"
    },
    "Pincer": {
      "enemy_count_range": [30, 60],
      "spawn_interval": 0.5,
      "spawner_count": 2,
      "spawners": ["North", "South"],
      "description": "双向夹击"
    },
    "Elite": {
      "enemy_count_range": [5, 10],
      "spawn_interval": 3.0,
      "elite_ratio": 1.0,
      "description": "所有怪都是精英"
    },
    "Boss": {
      "enemy_count_range": [1, 1],
      "spawn_interval": 0,
      "boss_id": "BossName"
    }
  }
}
```

### 6.2 强度曲线配置 (Intensity Curve)

**使用函数曲线控制难度**:

```json
{
  "intensity_curve": {
    "type": "sine_wave",
    "parameters": {
      "amplitude": 1.5,
      "frequency": 0.2,
      "baseline": 1.0
    }
  }
}
```

**对应的代码实现**:

```csharp
public float GetWaveIntensity(int waveNumber)
{
    float t = waveNumber * frequency;
    float intensity = baseline + amplitude * Mathf.Sin(t);
    return Mathf.Max(0.5f, intensity); // 最低 0.5x 难度
}

public int GetEnemyCount(int baseCount, int waveNumber)
{
    return Mathf.RoundToInt(baseCount * GetWaveIntensity(waveNumber));
}
```

---

## 7. 性能优化指南 (Performance Optimization)

### 7.1 对象池 (Object Pooling)

**问题**: 频繁生成/销毁敌人会导致 GC 卡顿。

**解决方案**:

```csharp
public class EnemyPool : MonoBehaviour
{
    private Dictionary<string, Queue<Enemy>> pools = new Dictionary<string, Queue<Enemy>>();

    public Enemy Spawn(string enemyId, Vector3 position)
    {
        if (!pools.ContainsKey(enemyId))
            pools[enemyId] = new Queue<Enemy>();

        Enemy enemy;
        if (pools[enemyId].Count > 0)
        {
            enemy = pools[enemyId].Dequeue();
            enemy.transform.position = position;
            enemy.gameObject.SetActive(true);
        }
        else
        {
            enemy = Instantiate(GetEnemyPrefab(enemyId), position, Quaternion.identity);
        }

        enemy.OnDeath += () => Recycle(enemyId, enemy);
        return enemy;
    }

    private void Recycle(string enemyId, Enemy enemy)
    {
        enemy.gameObject.SetActive(false);
        pools[enemyId].Enqueue(enemy);
    }
}
```

### 7.2 批量渲染 (GPU Instancing)

**启用 GPU Instancing**:

- 所有同类敌人使用**同一个 Material**。
- 在 Shader 中勾选 `Enable GPU Instancing`。

> [!TIP] > **移动端优化关键指标**
>
> - Draw Calls < 100
> - Batches < 50
> - 总三角面数 < 500K
> - 同屏敌人 < 200

---

## 8. 调试工具与技巧 (Debugging Tools)

### 8.1 关卡测试控制台

**运行时调试工具**:

```csharp
public class LevelDebugger : MonoBehaviour
{
    private void OnGUI()
    {
        GUILayout.BeginArea(new Rect(10, 10, 300, 500));

        GUILayout.Label($"Current Wave: {WaveManager.Instance.CurrentWave}");
        GUILayout.Label($"Enemies Alive: {EnemyManager.Instance.AliveCount}");

        if (GUILayout.Button("Skip to Wave +5"))
            WaveManager.Instance.SkipToWave(WaveManager.Instance.CurrentWave + 5);

        if (GUILayout.Button("Add 1000 Gold"))
            PlayerData.Gold += 1000;

        GUILayout.EndArea();
    }
}
```

### 8.2 寻路可视化

**绘制 Flow Field**:

```csharp
private void OnDrawGizmos()
{
    if (!Application.isPlaying || flowField == null) return;

    for (int x = 0; x < gridWidth; x++)
    {
        for (int y = 0; y < gridHeight; y++)
        {
            Vector3 worldPos = GridToWorld(new Vector2Int(x, y));
            Vector3 flow = flowField[x, y];

            // 绘制箭头
            Gizmos.color = Color.yellow;
            Gizmos.DrawLine(worldPos, worldPos + flow * 0.5f);
        }
    }
}
```

---

## 9. 常见错误与解决方案 (Common Pitfalls)

### 9.1 错误：怪物卡在墙里

**原因**: 寻路网格精度不足，或者移速过快导致穿墙。

**解决**:

```csharp
private void FixedUpdate()
{
    Vector3 desiredVelocity = GetFlowDirection(transform.position) * speed;
    rb.velocity = Vector3.Lerp(rb.velocity, desiredVelocity, 0.5f);

    // 检测穿墙
    if (Physics.Raycast(transform.position, rb.velocity.normalized, out hit, rb.velocity.magnitude * Time.fixedDeltaTime))
    {
        if (hit.collider.CompareTag("Wall"))
        {
            rb.velocity = Vector3.zero;
            RegeneratePathToGoal();
        }
    }
}
```

### 9.2 错误：动态难度系统过于敏感

**解决**: 使用**移动平均**平滑数据。

```csharp
private Queue<float> recentPerformance = new Queue<float>();

public float GetAveragePerformance()
{
    return recentPerformance.Average();
}

public void AdjustDifficulty()
{
    float avg = GetAveragePerformance();
    if (avg > 0.8f)
        difficultyMultiplier += 0.1f;
    else if (avg < 0.3f)
        difficultyMultiplier -= 0.1f;

    difficultyMultiplier = Mathf.Clamp(difficultyMultiplier, 0.5f, 2.0f);
}
```

> [!CAUTION] > **动态难度调整的副作用**
>
> 过于激进的难度调整可能让玩家感觉"系统在针对我"。建议：
>
> - 只在玩家**连续 3 波**表现过好/过差时才调整
> - 调整幅度不超过 ±10%
> - 在 UI 中**不要**明确告知玩家难度已调整

---

## 10. 关卡 JSON 示例

```json
{
  "level_id": "Lvl_Graveyard_01",
  "waves": [
    {
      "time_start": 0,
      "duration": 60,
      "spawners": ["North", "South"],
      "enemies": [
        { "id": "Zombie", "count": 50, "interval": 1.0 },
        { "id": "Skeleton_Archer", "count": 10, "interval": 5.0 }
      ]
    },
    {
      "time_start": 70,
      "type": "Rest",
      "duration": 30
    }
  ]
}
```

### 10.1 完整关卡配置示例

**包含所有配置项的高级示例**:

```json
{
  "level_id": "Lvl_Graveyard_Hard",
  "level_name": "墓地围攻：困难模式",
  "recommended_player_level": 10,

  "map_config": {
    "grid_size": { "x": 50, "y": 50 },
    "spawners": [
      { "id": "North", "position": { "x": 25, "y": 0 } },
      { "id": "South", "position": { "x": 25, "y": 49 } },
      { "id": "East", "position": { "x": 49, "y": 25 } }
    ],
    "base_position": { "x": 25, "y": 25 },
    "special_zones": [
      {
        "type": "HighGround",
        "area": [
          { "x": 10, "y": 10 },
          { "x": 15, "y": 15 }
        ],
        "bonus": "+20% Range"
      },
      {
        "type": "PowerNode",
        "position": { "x": 30, "y": 30 },
        "bonus": "+30% AttackSpeed",
        "cost_multiplier": 2.0
      }
    ]
  },

  "waves": [
    {
      "wave_number": 1,
      "type": "Standard",
      "time_start": 0,
      "duration": 60,
      "spawners": ["North"],
      "enemies": [
        { "id": "Zombie", "count": 30, "interval": 1.5 },
        { "id": "Skeleton", "count": 10, "interval": 3.0 }
      ]
    },
    {
      "wave_number": 2,
      "type": "Burst",
      "time_start": 70,
      "duration": 20,
      "spawners": ["North", "South"],
      "enemies": [{ "id": "Bat_Swarm", "count": 100, "interval": 0.2 }],
      "warning_message": "蝙蝠群来袭！"
    },
    {
      "wave_number": 3,
      "type": "Rest",
      "time_start": 100,
      "duration": 30,
      "special_event": "WanderingTrader"
    },
    {
      "wave_number": 4,
      "type": "Elite",
      "time_start": 140,
      "duration": 90,
      "spawners": ["North", "South", "East"],
      "enemies": [
        { "id": "Armored_Ghoul", "count": 15, "interval": 5.0 },
        { "id": "Necromancer", "count": 3, "interval": 20.0 }
      ],
      "map_event": { "type": "BloodMoon", "duration": 90 }
    },
    {
      "wave_number": 5,
      "type": "Boss",
      "time_start": 240,
      "spawners": ["North"],
      "enemies": [{ "id": "Boss_Lich_King", "count": 1, "interval": 0 }],
      "music_override": "Music_Boss_Theme",
      "camera_mode": "Cinematic"
    }
  ],

  "difficulty_settings": {
    "base_health_multiplier": 1.5,
    "base_damage_multiplier": 1.3,
    "gold_drop_multiplier": 1.2,
    "dynamic_adjustment": {
      "enabled": true,
      "max_multiplier": 2.0,
      "min_multiplier": 0.7
    }
  },

  "rewards": {
    "first_clear": [
      { "type": "Gold", "amount": 5000 },
      { "type": "Item", "id": "Relic_Death_Knight_Helm" }
    ],
    "perfect_clear": [
      { "type": "Achievement", "id": "No_Damage_Graveyard" },
      { "type": "Title", "id": "Undead_Slayer" }
    ]
  }
}
```

---

## 🔗 相关文档 (Related Documents)

本文档侧重于**具体实现**和配置。如需了解**设计理论**，请参阅：

> [!NOTE] > **理论基础**
>
> 查看 [🗺️ 关卡设计理论：节奏、空间与引导](/docs/Design/Content/Level_Design_Theory) 了解：
>
> - 空间结构理论（路径类型、扼守点）
> - 节奏控制理论（起承转合、心流通道）
> - 认知负荷理论（UI 设计原则）
> - 业界案例分析（Dark Souls、Hades）

**其他相关文档**:

- [⚔️ 战斗系统](/docs/Design/Mechanics/Combat_System) - 伤害类型和敌人韧性
- [🏰 塔防系统](/docs/Design/Mechanics/Tower_Defense_System) - 塔的升级和协同机制
- [💀 敌人图鉴](/docs/Design/Content/Enemy_Bestiary) - 所有敌人的 AI 行为
- [🎲 随机数与掉落](/docs/Design/Systems/Loot_Table_Rules) - 战利品掉落算法
- [📊 数值手册](/docs/Design/Numerical_Manual) - 核心数学公式
- [🤖 AI 实用系统](/docs/Tech/AI_Utility_System) - AI 决策评分曲线
