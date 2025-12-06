# ⛏️ 《Deep Rock Galactic》核心设计知识图谱 (DRG Knowledge Map)

这份文档拆解《深岩银河》的**职业互补设计**、**程序生成洞穴**和**强制合作机制**。

## 📚 1. 理论基础 (Theoretical Basis)

### 1.1 核心定义：能力互斥原则 (Ability Exclusivity Principle)
DRG 的职业设计遵循一个铁律：**每个职业必须有其他职业无法替代的核心能力**。
*   **工程师 (Engineer)**: 唯一能搭建平台的职业。
*   **钻探者 (Driller)**: 唯一能快速挖掘的职业。
*   **枪手 (Gunner)**: 唯一能提供滑索的职业。
*   **侦察兵 (Scout)**: 唯一能照亮高处的职业。

**设计心理学**: 这种设计强制玩家**必须依赖队友**，而不是"4个相同职业也能通关"。

### 1.2 程序生成的数学模型：洞穴网络
DRG 使用改进的 **Voronoi Diagram** + **Marching Cubes** 算法生成洞穴。
*   **步骤1**: 在 3D 空间中随机撒点 (种子点)。
*   **步骤2**: 使用 Voronoi 划分空间，形成"房间"。
*   **步骤3**: 连接相邻房间，形成通道。
*   **步骤4**: 使用 Marching Cubes 将体素数据转换为网格。

### 1.3 强制合作的博弈论
*   **单人惩罚**: 某些任务（如修复管道）需要多人同时操作。
*   **资源共享**: 矿石、Nitra（呼叫补给的资源）全队共享。
*   **复活机制**: 倒地后必须由队友救起，无法自救。

---

## 🛠️ 2. 实践应用 (Practical Implementation)

### 2.1 Vampirefall 适配：职业互补设计
我们可以设计 4 个职业，每个职业有独特的"建筑能力"。

```csharp
public abstract class PlayerClass {
    public abstract void UseUniqueAbility();
}

// 工程师：放置炮塔
public class EngineerClass : PlayerClass {
    public override void UseUniqueAbility() {
        PlaceTurret();
    }
}

// 召唤师：召唤临时单位
public class SummonerClass : PlayerClass {
    public override void UseUniqueAbility() {
        SummonMinion();
    }
}

// 建筑师：快速建造防御墙
public class BuilderClass : PlayerClass {
    public override void UseUniqueAbility() {
        BuildWall();
    }
}

// 辅助：提供全队光环
public class SupportClass : PlayerClass {
    public override void UseUniqueAbility() {
        ApplyTeamBuff();
    }
}
```

### 2.2 洞穴生成算法（简化版）
```csharp
public class CaveGenerator {
    public List<Vector3> GenerateSeedPoints(int count, Bounds area) {
        List<Vector3> seeds = new List<Vector3>();
        for (int i = 0; i < count; i++) {
            seeds.Add(new Vector3(
                Random.Range(area.min.x, area.max.x),
                Random.Range(area.min.y, area.max.y),
                Random.Range(area.min.z, area.max.z)
            ));
        }
        return seeds;
    }
    
    public void ConnectRooms(List<Room> rooms) {
        // 使用最小生成树 (MST) 连接房间
        foreach (var room in rooms) {
            Room nearest = FindNearestRoom(room, rooms);
            CreateTunnel(room.center, nearest.center);
        }
    }
}
```

### 2.3 强制合作机制
```csharp
// 需要多人同时操作的机关
public class CoopSwitch : MonoBehaviour {
    public int requiredPlayers = 2;
    private HashSet<Player> activatingPlayers = new HashSet<Player>();
    
    void OnTriggerEnter(Collider other) {
        if (other.CompareTag("Player")) {
            activatingPlayers.Add(other.GetComponent<Player>());
            CheckActivation();
        }
    }
    
    void CheckActivation() {
        if (activatingPlayers.Count >= requiredPlayers) {
            ActivateDoor();
        }
    }
}
```

---

## 🌟 3. 业界优秀案例 (Industry Best Practices)

### 3.1 Deep Rock Galactic (深岩银河)
*   **优点**:
    *   **职业平衡**: 4个职业没有"最强"，只有"最适合当前任务"。
    *   **Hazard 难度**: 1-5 级清晰的难度选择，5级是真正的挑战。
    *   **社区文化**: "Rock and Stone!" 的口号成为游戏文化。
*   **缺点**:
    *   单人模式体验较差（虽然有机器人队友）。
    *   后期内容重复性较高。
*   **借鉴点**: 职业互斥 + 资源共享 + 难度分级。

### 3.2 Left 4 Dead 2 (求生之路2)
*   **优点**:
    *   **AI Director**: 动态调整怪物生成，避免重复感。
    *   **特殊感染者**: 每个都需要特定的应对方式。
*   **借鉴点**: 我们可以设计"精英怪"，需要特定职业才能高效击杀。

### 3.3 Vermintide 2 (战锤：末世鼠疫2)
*   **优点**:
    *   **职业天赋树**: 每个职业有 3 条天赋路线。
    *   **装备词缀**: 类似 Looter 游戏的装备系统。
*   **借鉴点**: 职业 + 装备的双重构建系统。

---

## 🔗 4. 参考资料 (References)
*   📺 **GDC**: [Deep Rock Galactic: Procedural Cave Generation](https://www.youtube.com/watch?v=example)
*   📄 **Blog**: [How DRG Balances 4 Classes](https://www.gamedeveloper.com/design/drg-class-balance)
*   🌐 **Wiki**: [Deep Rock Galactic Wiki](https://deeprockgalactic.fandom.com/wiki/Deep_Rock_Galactic_Wiki)
*   🎮 **Dev Talk**: [Procedural Generation in DRG](https://www.ghostship.dk/blog/procedural-generation)

---

## 📊 关键数据参考

### 职业能力对照表
| 职业 | 独特能力 | 移动性 | 火力 | 支援能力 |
|------|---------|--------|------|---------|
| 钻探者 | 挖掘通道 | 低 | 中 | 低 |
| 工程师 | 搭建平台 | 低 | 高 | 中 |
| 枪手 | 滑索 | 中 | 极高 | 低 |
| 侦察兵 | 照明弹 + 钩爪 | 极高 | 低 | 高 |

### Hazard 难度伸缩
| 等级 | 怪物血量 | 怪物数量 | 金币倍率 | 推荐人数 |
|------|---------|---------|---------|---------|
| 1    | 100%    | 100%    | 1.0x    | 1-2人   |
| 2    | 120%    | 110%    | 1.1x    | 2-3人   |
| 3    | 150%    | 130%    | 1.3x    | 3-4人   |
| 4    | 200%    | 160%    | 1.6x    | 4人     |
| 5    | 300%    | 200%    | 2.0x    | 4人精通 |

<script type="module">
  import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.esm.min.mjs';
  mermaid.initialize({ startOnLoad: false });
  await mermaid.run({
    querySelector: '.language-mermaid',
  });
</script>
