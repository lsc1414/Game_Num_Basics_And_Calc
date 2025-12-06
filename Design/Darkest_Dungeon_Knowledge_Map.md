# 😰 《Darkest Dungeon》核心设计知识图谱 (DD Knowledge Map)

这份文档拆解《暗黑地牢》的**压力系统设计**、**永久损失机制**和**叙事驱动机制**。

## 📚 1. 理论基础 (Theoretical Basis)

### 1.1 核心定义：压力系统 (Stress Mechanics)
*   **压力值 (Stress)**: 0-100，达到 100 触发"崩溃"或"顿悟"
*   **崩溃 (Affliction)**: 负面状态（恐惧、偏执、受虐狂等）
*   **顿悟 (Virtue)**: 正面状态（勇敢、专注等）

### 1.2 永久损失机制
*   **英雄死亡**: 永久失去，无法复活
*   **替换成本**: 需要重新招募和培养新英雄

### 1.3 叙事与机制结合
*   **怪物背景**: 每个怪物都有 Lore
*   **英雄台词**: 根据压力值变化

---

## 🛠️ 2. 实践应用 (Practical Implementation)

### 2.1 压力系统
```csharp
public class Hero {
    public int stress = 0;
    public bool isAfflicted = false;
    
    public void AddStress(int amount) {
        stress += amount;
        if (stress >= 100) {
            TriggerBreakdown();
        }
    }
    
    void TriggerBreakdown() {
        if (Random.value < 0.75f) {
            isAfflicted = true; // 75% 崩溃
        } else {
            ApplyVirtue(); // 25% 顿悟
        }
    }
}
```

---

## 🌟 3. 业界优秀案例 (Industry Best Practices)

### 3.1 Darkest Dungeon
*   **优点**: 压力系统独特、叙事深度
*   **缺点**: 节奏较慢
*   **借鉴点**: 压力系统 + 永久损失

---

## 🔗 4. 参考资料 (References)
*   📺 **GDC**: [Darkest Dungeon Stress System](https://www.youtube.com/watch?v=example)

<script type="module">
  import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.esm.min.mjs';
  mermaid.initialize({ startOnLoad: false });
  await mermaid.run({
    querySelector: '.language-mermaid',
  });
</script>
