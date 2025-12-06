# 🏰 构建《王权陨落》类极简策略游戏知识图谱 (Minimalist Strategy Knowledge Map)

这份文档旨在拆解《Thronefall》、《Kingdom Two Crowns》、《Bad North》这类“极简策略”游戏背后的设计理论与核心知识体系。

## 📚 1. 理论基础 (Theoretical Basis)

### 1.1 认知负荷理论 (Cognitive Load Theory) 与 减法设计
设计此类游戏的核心不是“加法”，而是极致的“减法”。
*   **核心定义**: 玩家的工作记忆是有限的（通常只能同时处理 4-7 个信息块）。极简策略游戏的目标是将 RTS 复杂的“微操”和“宏操”压缩到极低的认知成本中。
*   **操作压缩 (Input Compression)**:
    *   **传统 RTS**: `选中单位` -> `点击技能` -> `选择目标` -> `确认` (4步)。
    *   **Thronefall**: `移动到位置` (1步，英雄自动攻击，单位自动跟随)。
*   **设计心理学**: **"Flow through Mastery"**。当操作不再是障碍，玩家的心流将完全集中在“位置选择”和“经济决策”上。

### 1.2 日夜循环经济学 (Day/Night Cycle Economics)
这是此类游戏的核心循环引擎。
*   **模型**: **投资 (Day)** vs **验证 (Night)**。
*   **白天 (Safe Phase)**: 纯粹的经济决策。不仅是造塔，更是“用金币换取未来的金币”（如造磨坊）。
    *   **公式**: $Reward = Investment \times (1 + InterestRate)^{Time}$
    *   **风险**: 投资经济 = 削弱当前防守。贪婪是第一驱动力。
*   **夜晚 (Danger Phase)**: 纯粹的战斗验证和操作。
*   **理论应用**: 必须严格分割这两个阶段，**严禁在夜晚进行建设**，这保证了玩家的情绪张力有松（白天）有驰（夜晚）。

### 1.3 自动机与群体行为 (Automata & Boids)
由于玩家不能微操每一个士兵，单位的 AI 必须足够聪明且可预测。
*   **Boids 算法**: 模拟鸟群行为，包含三个力：
    1.  **分离 (Separation)**: 避免挤在一起。
    2.  **对齐 (Alignment)**: 跟着大家的朝向走。
    3.  **内聚 (Cohesion)**: 保持在群体中心附近。
*   **应用**: 玩家只需要控制“集结号”（Hero 的位置），士兵会自动通过 Boids 算法形成阵型。

---

## 🛠️ 2. 实践应用 (Practical Implementation)

### 2.1 Vampirefall 适配：混合设计的挑战
*   **英雄定位**: 在 Thronefall 中，英雄是“最强的塔”也是“唯一的修塔工”。在 Vampirefall 中，我们要避免英雄过于忙碌。
*   **极简 UI**: 既然是极简设计，就不要做复杂的 HUD。
    *   **世界空间 UI (World Space UI)**: 血条、金币消耗直接飘在单位头上，而不是显示在屏幕角落。

### 2.2 关键算法：自动目标选择 (Auto-Targeting Utility)
玩家不点击目标，系统如何知道玩家想打谁？需要一套评分系统。

```csharp
// 自动攻击权重计算
public float CalculateTargetScore(Enemy enemy, Hero hero) {
    float score = 0;
    
    // 1. 距离权重 (越近分越高)
    float dist = Vector3.Distance(enemy.transform.position, hero.transform.position);
    score += (1.0f / dist) * weightDistance;
    
    // 2. 威胁权重 (正在攻击基地的怪分高)
    if (enemy.IsAttackingBase) score += weightThreat;
    
    // 3. 残血权重 (优先补刀)
    if (enemy.Health / enemy.MaxHealth < 0.3f) score += weightKillConfirm;
    
    return score;
}
```

### 2.3 寻路与聚怪 (Pathfinding & Flow Fields)
大量单位移动不应使用 NavMeshAgent（太耗费），建议使用 **流场寻路 (Flow Fields)**。
*   **原理**: 将地图网格化，每个格子存储一个“指向目标的方向向量”。
*   **优势**: 1000 个单位只需要读取各自脚下的向量即可移动，性能开销 O(N) -> O(1)。

---

## 🌟 3. 业界优秀案例 (Industry Best Practices)

### 3.1 Thronefall (王权陨落)
*   **核心机制**: 极简的 Build 搭配。每局开始前只选 3-4 个 perk，局内不再有复杂的技能树。
*   **借鉴点**: **"武器即职业"**。换把弓就是弓箭手，换把剑就是战士。Vampirefall 可以借鉴通过更换“法杖核心”来彻底改变攻击模式。

### 3.2 Kingdom Two Crowns (王国：两位君主)
*   **核心机制**: **一维极简**。只有左右移动 + 扔钱。
*   **优缺点**:
    *   *优*: 学习成本几乎为零。
    *   *缺*: 缺乏纵深，难以通过走位秀操作。
*   **借鉴点**: 它的金币有“物理实体”（金币袋满了会掉出来），这增加了资源的真实感和紧迫感。

### 3.3 Bad North (北境之地)
*   **核心机制**: 岛屿格防御。
*   **借鉴点**: 它的“单位疲劳”机制（用过的队伍本轮不能再用）强迫玩家轮换阵容，值得参考用于我们的“防御塔维护”系统。

---

## 🔗 4. 参考资料 (References)
*   📺 **GDC**: [Minimalism in Game Design: Architecture & Psychology](https://www.youtube.com/watch?v=example)
*   📄 **Paper**: [Reynolds Flocking (Boids) Algorithm](https://www.red3d.com/cwr/boids/)
*   🌐 **Blog**: [Flow Fields Pathfinding Explained](https://leifnode.com/2013/12/flow-field-pathfinding/)
*   **书籍**: 《The Design of Everyday Things》 (关于示能性 Affordance 的理解)
