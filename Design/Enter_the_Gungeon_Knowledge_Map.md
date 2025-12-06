# 🔫 《Enter the Gungeon》核心设计知识图谱 (EtG Knowledge Map)

这份文档拆解《挺进地牢》的**武器多样性设计**、**弹道系统优化**和**房间生成算法**。

## 📚 1. 理论基础 (Theoretical Basis)

### 1.1 核心定义：机制优先于数值 (Mechanics Over Numbers)
EtG 拥有 200+ 武器，但几乎没有两把武器的机制是相同的。
*   **传统设计**: 武器A = 10伤害/秒，武器B = 15伤害/秒 → 数值差异
*   **EtG 设计**: 武器A = 发射会反弹的子弹，武器B = 发射会分裂的子弹 → 机制差异

**设计心理学**: 玩家记住的不是"这把枪伤害高",而是"这把枪的子弹会追踪敌人"。

### 1.2 弹道系统的性能模型
EtG 每帧可能有 1000+ 个子弹在屏幕上，必须使用**对象池 (Object Pooling)** 和 **空间分区 (Spatial Partitioning)**。
*   **对象池**: 预先创建 1000 个子弹对象，循环使用。
*   **四叉树 (Quadtree)**: 将屏幕分为 4 个区域，只检测同区域内的碰撞。

### 1.3 房间生成的图论模型
*   **步骤1**: 生成一个**有向无环图 (DAG)**，代表房间连接关系。
*   **步骤2**: 为每个节点分配房间类型（战斗/宝箱/商店/Boss）。
*   **步骤3**: 使用 **Wave Function Collapse (WFC)** 算法生成具体的房间布局。

---

## 🛠️ 2. 实践应用 (Practical Implementation)

### 2.1 Vampirefall 适配：武器机制库
我们可以为每把武器定义"特殊机制"而非简单的数值。

```csharp
public abstract class WeaponMechanic : ScriptableObject {
    public abstract void OnProjectileSpawn(Projectile proj);
    public abstract void OnProjectileHit(Projectile proj, Enemy target);
}

// 示例：反弹机制
public class BounceMechanic : WeaponMechanic {
    public int maxBounces = 3;
    
    public override void OnProjectileHit(Projectile proj, Enemy target) {
        proj.bounceCount++;
        if (proj.bounceCount < maxBounces) {
            Enemy nextTarget = FindNearestEnemy(proj.transform.position);
            proj.Redirect(nextTarget.transform.position);
        } else {
            proj.Destroy();
        }
    }
}

// 示例:分裂机制
public class SplitMechanic : WeaponMechanic {
    public int splitCount = 3;
    
    public override void OnProjectileHit(Projectile proj, Enemy target) {
        for (int i = 0; i < splitCount; i++) {
            float angle = (360f / splitCount) * i;
            SpawnProjectile(proj.transform.position, angle);
        }
        proj.Destroy();
    }
}
```

### 2.2 对象池优化
```csharp
public class ProjectilePool : MonoBehaviour {
    public GameObject projectilePrefab;
    public int poolSize = 1000;
    private Queue<Projectile> pool = new Queue<Projectile>();
    
    void Start() {
        for (int i = 0; i < poolSize; i++) {
            GameObject obj = Instantiate(projectilePrefab);
            obj.SetActive(false);
            pool.Enqueue(obj.GetComponent<Projectile>());
        }
    }
    
    public Projectile Get() {
        if (pool.Count > 0) {
            Projectile proj = pool.Dequeue();
            proj.gameObject.SetActive(true);
            return proj;
        }
        return null; // 池子用完了
    }
    
    public void Return(Projectile proj) {
        proj.gameObject.SetActive(false);
        pool.Enqueue(proj);
    }
}
```

### 2.3 房间生成（简化版）
```csharp
public class RoomGenerator {
    public enum RoomType { Combat, Treasure, Shop, Boss }
    
    public class RoomNode {
        public RoomType type;
        public List<RoomNode> connections = new List<RoomNode>();
    }
    
    public RoomNode GenerateFloor() {
        // 1. 创建起始房间
        RoomNode start = new RoomNode { type = RoomType.Combat };
        
        // 2. 生成主路径（保证能到达 Boss）
        RoomNode current = start;
        for (int i = 0; i < 5; i++) {
            RoomNode next = new RoomNode { type = RoomType.Combat };
            current.connections.Add(next);
            current = next;
        }
        
        // 3. Boss 房间
        RoomNode boss = new RoomNode { type = RoomType.Boss };
        current.connections.Add(boss);
        
        // 4. 添加分支（宝箱/商店）
        AddBranches(start, 3);
        
        return start;
    }
}
```

---

## 🌟 3. 业界优秀案例 (Industry Best Practices)

### 3.1 Enter the Gungeon (挺进地牢)
*   **优点**:
    *   **武器创意**: 每把武器都有独特的"梗"（如"蜜蜂枪"发射蜜蜂）。
    *   **弹幕可读性**: 即使屏幕上有 100 个子弹，玩家也能清晰判断。
    *   **翻滚机制**: 完美的无敌帧设计。
*   **缺点**:
    *   前期难度过高，劝退新手。
    *   部分武器过于弱势。
*   **借鉴点**: 武器机制库 + 对象池 + 翻滚无敌帧。

### 3.2 Nuclear Throne (核子王座)
*   **优点**:
    *   **武器手感**: 每把武器的后坐力、射速都不同。
    *   **变异系统**: 类似 Roguelike 的升级系统。
*   **借鉴点**: 武器手感差异化。

### 3.3 Binding of Isaac (以撒的结合)
*   **优点**:
    *   **房间模板**: 预制了数百个房间模板，随机组合。
    *   **道具协同**: 道具之间的化学反应。
*   **借鉴点**: 房间模板库 + 道具协同。

---

## 🔗 4. 参考资料 (References)
*   📺 **GDC**: [Enter the Gungeon: Designing 200+ Guns](https://www.youtube.com/watch?v=example)
*   📄 **Blog**: [Object Pooling in Unity](https://learn.unity.com/tutorial/object-pooling)
*   🌐 **Wiki**: [Enter the Gungeon Wiki - Guns](https://enterthegungeon.fandom.com/wiki/Guns)
*   🎮 **Dev Talk**: [Procedural Room Generation](https://www.boristhebrave.com/2020/04/13/wave-function-collapse-explained/)

---

## 📊 关键数据参考

### 武器机制分类
| 机制类型 | 示例武器 | 特殊效果 |
|---------|---------|---------|
| 反弹 | Bouncer | 子弹击中后反弹到下一个敌人 |
| 分裂 | Shotgun | 一发分裂为多发 |
| 追踪 | Homing Bullet | 子弹自动追踪敌人 |
| 穿透 | Railgun | 穿透所有敌人 |
| 爆炸 | Grenade Launcher | 击中后产生 AOE 伤害 |
| 状态 | Freeze Ray | 冰冻敌人 |

### 对象池性能对比
| 方案 | 每帧实例化 | 对象池 |
|------|-----------|--------|
| CPU 开销 | 高 (GC 频繁) | 低 |
| 内存占用 | 波动大 | 稳定 |
| 适用场景 | 子弹少 (<50) | 子弹多 (>100) |

<script type="module">
  import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.esm.min.mjs';
  mermaid.initialize({ startOnLoad: false });
  await mermaid.run({
    querySelector: '.language-mermaid',
  });
</script>
