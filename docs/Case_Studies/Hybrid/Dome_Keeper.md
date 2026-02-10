---
sidebarTitle: "Dome Keeper》核心设计知识图谱"
---

# 🛡️ 《Dome Keeper》核心设计知识图谱

这份文档拆解《圆顶守护者》的**双阶段循环**、**资源管理博弈**和**时间压力递增**。

## 📚 1. 理论基础 (Theoretical Basis)

### 1.1 核心定义：双阶段循环 (Dual-Phase Loop)
*   **采集阶段 (Mining)**: 玩家下矿挖资源，基地无防御
*   **防守阶段 (Defending)**: 怪物来袭，玩家必须回到基地

**设计心理学**: 这种强制切换创造了**节奏感**和**紧迫感**。

### 1.2 资源管理的博弈论
*   **贪婪惩罚**: 挖太久 = 来不及回防 = 基地被破坏
*   **保守惩罚**: 挖太少 = 升级慢 = 后期打不过

### 1.3 时间压力模型
$WaveStrength = BaseStrength \times (1 + 0.2 \times WaveNumber)$

---

## 🛠️ 2. 实践应用 (Practical Implementation)

### 2.1 Vampirefall 适配：双阶段系统
```csharp
public class PhaseManager : MonoBehaviour {
    public enum Phase { Building, Combat }
    public Phase currentPhase;
    
    public void SwitchPhase() {
        if (currentPhase == Phase.Building) {
            currentPhase = Phase.Combat;
            StartWave();
        } else {
            currentPhase = Phase.Building;
            AllowBuilding();
        }
    }
}
```

---

## 🌟 3. 业界优秀案例 (Industry Best Practices)

### 3.1 Dome Keeper
*   **优点**: 双阶段循环、资源管理紧张
*   **借鉴点**: 白天/夜晚循环

---

## 🔗 4. 参考资料 (References)
*   📺 **GDC**: [Dome Keeper Design](https://www.youtube.com/watch?v=example)

