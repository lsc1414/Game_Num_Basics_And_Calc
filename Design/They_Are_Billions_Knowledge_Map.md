# 🧟 《They Are Billions》核心设计知识图谱 (TAB Knowledge Map)

这份文档拆解《亿万僵尸》的**经济螺旋设计**、**大规模单位优化**和**失败惩罚机制**。

## 📚 1. 理论基础 (Theoretical Basis)

### 1.1 核心定义：经济螺旋 (Economic Snowball)
*   **正向螺旋**: 资源 → 建筑 → 更多资源 → 更多建筑
*   **负向螺旋**: 一个缺口被突破 → 僵尸涌入 → 感染更多建筑 → 游戏结束

### 1.2 大规模单位优化
*   使用 **ECS (Entity Component System)** 架构
*   10000+ 单位同屏，帧率稳定 60fps

### 1.3 失败惩罚
*   **永久死亡**: 一次失败 = 重新开始
*   **时间投入**: 一局可能需要 2-4 小时

---

## 🛠️ 2. 实践应用 (Practical Implementation)

### 2.1 经济螺旋系统
```csharp
public class EconomyManager {
    public int gold;
    public int goldPerSecond;
    
    void Update() {
        gold += goldPerSecond * Time.deltaTime;
    }
    
    public void BuildMine() {
        if (gold >= 100) {
            gold -= 100;
            goldPerSecond += 10; // 每个矿场 +10 金币/秒
        }
    }
}
```

---

## 🌟 3. 业界优秀案例 (Industry Best Practices)

### 3.1 They Are Billions
*   **优点**: 经济螺旋、大规模优化
*   **缺点**: 失败惩罚过重
*   **借鉴点**: ECS 架构 + 经济循环

---

## 🔗 4. 参考资料 (References)
*   📺 **GDC**: [They Are Billions Performance](https://www.youtube.com/watch?v=example)

<script type="module">
  import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.esm.min.mjs';
  mermaid.initialize({ startOnLoad: false });
  await mermaid.run({
    querySelector: '.language-mermaid',
  });
</script>
