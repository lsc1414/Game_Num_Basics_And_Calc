---
sidebarTitle: "《Dead Cells》核心设计知识图谱"
title: "《Dead Cells》核心设计知识图谱"
---
> **摘要**：本文档拆解《死亡细胞》的**颜色分级词缀系统**、**关卡分支设计**和**打击感优化**。

## 📚 1. 理论基础 (Theoretical Basis)

### 1.1 核心定义：颜色分级系统 (Color-Coded Progression)
Dead Cells 将所有装备和升级分为三个颜色：

*   **红色 (Brutality)**: 高伤害、低生存
*   **绿色 (Tactics)**: 远程、陷阱、暴击
*   **紫色 (Survival)**: 高血量、护盾、持续伤害

**数学模型**: $FinalDamage = BaseDamage \times (1 + ColorBonus)^{ColorLevel}$

- 如果你有 10 点红色属性,红色武器伤害 = Base × 1.15^10

### 1.2 关卡分支的风险/收益模型
*   **安全路线**: 少敌人、少奖励、快速通过
*   **危险路线**: 多敌人、多奖励、耗时长
*   **诅咒路线**: 极高风险（一击必死）、极高奖励

### 1.3 打击感的物理学
*   **顿帧 (Hit Stop)**: 击中瞬间暂停 0.1 秒
*   **屏幕震动 (Screen Shake)**: 根据伤害值震动
*   **粒子爆发 (Particle Burst)**: 血液飞溅效果

---

## 🛠️ 2. 实践应用 (Practical Implementation)

### 2.1 Vampirefall 适配：颜色属性系统
```csharp
public enum StatColor { Red, Green, Purple }

public class PlayerStats {
    public Dictionary<StatColor, int> colorLevels = new Dictionary<StatColor, int>();
    
    public float GetDamageMultiplier(StatColor weaponColor) {
        int level = colorLevels[weaponColor];
        return Mathf.Pow(1.15f, level); // 每级 +15%
    }
}

public class Weapon {
    public StatColor primaryColor;
    public int baseDamage;
    
    public int GetFinalDamage(PlayerStats stats) {
        float multiplier = stats.GetDamageMultiplier(primaryColor);
        return Mathf.RoundToInt(baseDamage * multiplier);
    }
}
```

### 2.2 关卡分支生成
```csharp
public class PathGenerator {
    public enum PathType { Safe, Risky, Cursed }
    
    public class PathNode {
        public PathType type;
        public int enemyCount;
        public int rewardMultiplier;
    }
    
    public List<PathNode> GeneratePaths() {
        return new List<PathNode> {
            new PathNode { type = PathType.Safe, enemyCount = 10, rewardMultiplier = 1 },
            new PathNode { type = PathType.Risky, enemyCount = 30, rewardMultiplier = 2 },
            new PathNode { type = PathType.Cursed, enemyCount = 50, rewardMultiplier = 5 }
        };
    }
}
```

### 2.3 打击感实现
```csharp
public class HitFeedback : MonoBehaviour {
    public void OnHit(int damage) {
        StartCoroutine(HitStop(0.1f));
        CameraShake(damage * 0.01f);
        SpawnBloodParticles();
    }
    
    IEnumerator HitStop(float duration) {
        Time.timeScale = 0;
        yield return new WaitForSecondsRealtime(duration);
        Time.timeScale = 1;
    }
    
    void CameraShake(float intensity) {
        Camera.main.transform.DOShakePosition(0.2f, intensity);
    }
}
```

---

## 🌟 3. 业界优秀案例 (Industry Best Practices)

### 3.1 Dead Cells (死亡细胞)
*   **优点**: 颜色系统简化了构建选择、打击感极佳
*   **缺点**: 后期数值膨胀严重
*   **借鉴点**: 颜色分级 + 关卡分支 + 顿帧

### 3.2 Hades (哈迪斯)
*   **优点**: 每次死亡都有剧情推进
*   **借鉴点**: 失败奖励机制

---

## 🔗 4. 参考资料 (References)
*   📺 **GDC**: [Dead Cells: Game Feel](https://www.youtube.com/watch?v=example)
*   📄 **Blog**: [Color-Coded Progression Systems](https://www.gamedeveloper.com)
