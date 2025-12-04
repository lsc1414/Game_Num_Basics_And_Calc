# 👥 多人协作平衡 (Co-op Balance Design) 深度研究

> **研究归属**: Project Vampirefall - Design/Systems  
> **创建日期**: 2025-12-04  
> **优先级**: ⭐⭐⭐ (中)

---

## 📑 目录

1.  [理论基础 (Theoretical Basis)](#-1-理论基础-theoretical-basis)
2.  [实践应用 (Practical Implementation)](#️-2-实践应用-practical-implementation)
3.  [业界优秀案例 (Industry Best Practices)](#-3-业界优秀案例-industry-best-practices)
4.  [参考资料 (References)](#-4-参考资料-references)

---

## 📚 1. 理论基础 (Theoretical Basis)

### 1.1 核心定义

**多人协作平衡**旨在解决"1+1 > 2"的问题，同时避免"1+1 < 1"（即猪队友体验）。在塔防+肉鸽的混合品类中，协作不仅是火力的叠加，更是**资源管理**和**空间控制**的分配。

关键挑战：
- **Scaling (伸缩性)**: 怪物强度如何随人数线性或非线性增长？
- **Economy (经济)**: 金币是共享的还是独立的？谁来造塔？
- **Synergy (协同)**: 不同角色/Build 之间如何产生化学反应？

### 1.2 数学模型：难度伸缩公式

通常采用 **非线性血量增长** 和 **线性伤害增长** 的组合。

```
EnemyHP = BaseHP * (1 + (PlayerCount - 1) * HP_Scale_Factor)
EnemyDmg = BaseDmg * (1 + (PlayerCount - 1) * Dmg_Scale_Factor)

推荐系数:
- HP_Scale_Factor: 0.7 ~ 0.9 (每多一人，怪血量增加 70%-90%，让杀怪稍微变快一点点，产生爽感)
- Dmg_Scale_Factor: 0.1 ~ 0.2 (伤害不宜增加太多，否则容易被秒杀)
```

**怪物数量 (Spawn Rate)**:
```
SpawnRate = BaseRate * (1 + (PlayerCount - 1) * 0.5)
// 4人联机时，怪数量是单人的 2.5 倍，而不是 4 倍（受限于性能和屏幕混乱度）
```

### 1.3 设计心理学

#### 🤝 互赖性 (Interdependence)

好的协作设计强迫玩家互相依赖，而不是"四个人各玩各的"。
- **软互赖**: 一个人也能打，但两个人打得更快（如：集火）。
- **硬互赖**: 必须配合才能解决机制（如：一人引怪，一人背刺；或一人破盾，一人输出）。

Vampirefall 倾向于 **软互赖**，但在 Boss 战引入少量 **硬互赖** 机制。

---

## 🛠️ 2. 实践应用 (Practical Implementation)

### 2.1 Vampirefall 协作机制

#### 💰 经济系统：混合模式

- **金币 (Gold)**: **独立掉落 (Instanced)**。每个人看到的金币都是自己的，互不抢夺。
- **以太 (Aether)**: **共享资源 (Shared)**。用于建造防御塔的特殊资源。
  - **设计意图**: 金币用于强化个人（Roguelike部分），以太用于强化团队防线（塔防部分）。这迫使玩家交流："我这波钱够升级主塔了，你留着钱买陷阱。"

#### 🏰 建造权限

- **所有权**: 谁造的塔，谁拥有该塔的 Buff 加成。
- **操作权**: 队友可以**升级**或**维修**你的塔，但不能**拆除**你的塔（防止恶意破坏）。

#### 💀 复活机制

- **倒地 (Downed)**: 玩家血量归零后进入倒地状态，可以缓慢爬行，可以使用手枪（低伤害）。
- **救助 (Revive)**: 队友需站定引导 3 秒救起。
- **死亡 (Dead)**: 倒地超时后死亡，需消耗全队共享的 **"灵魂石" (Soul Stone)** 复活，或等待当前波次结束自动复活。

### 2.2 角色定位 (Class Synergy)

Vampirefall 的角色设计应天然互补：

| 角色原型 | 塔防定位 | 战斗定位 | 协同效应 |
| :--- | :--- | :--- | :--- |
| **鲜血领主** (Tank) | 建造高血量路障 | 聚怪、承受伤害 | 将怪聚在队友的AOE塔下 |
| **暗影刺客** (DPS) | 建造单体高伤塔 | 切后排、秒杀精英 | 处理漏网之鱼 |
| **死灵法师** (Support) | 建造减速/削弱塔 | 召唤炮灰、削甲 | 放大队友伤害 |
| **炼金术士** (Tech) | 建造光环/Buff塔 | 埋雷、大范围AOE | 提供控制链 |

### 2.3 动态难度调整 (Dynamic Scaling)

如果一名玩家掉线或死亡，难度应如何调整？

```csharp
public void OnPlayerCountChanged(int newCount)
{
    // 实时调整下一波怪物的生成参数
    currentWaveConfig.hpMultiplier = 1f + (newCount - 1) * 0.8f;
    
    // 已经在场上的怪物血量通常不调整（避免突兀），或者按比例削减当前HP
    // 但为了实现简单，通常只影响新生成的怪
}
```

---

## 🌟 3. 业界优秀案例 (Industry Best Practices)

### 3.1 Deep Rock Galactic (Ghost Ship Games)

#### ✅ 核心机制：职业工具互补

- **机制**: 工程师造平台，侦察兵用钩爪上平台挖矿；钻机手开路，枪手放滑索。
- **启示**: 这种"物理层面的互补"比单纯的"数值互补"（战法牧）更有趣且更直观。

#### 🎯 Vampirefall 借鉴点

- **物理互补**: 鲜血领主可以制造"血墙"改变怪物路径，引导怪物走进炼金术士的"毒沼"区域。

### 3.2 Risk of Rain 2 (Hopoo Games)

#### ✅ 核心机制：抢装备与分配

- **机制**: 装备掉落是共享的，谁捡到归谁。
- **优缺**: 增加了竞争和由于分配不均导致的争吵，但也增加了"让装备"的社交时刻。
- **神器**: 开启"神器"后可以选择装备，减少随机性。

#### 🎯 Vampirefall 借鉴点

- 我们采用 **独立掉落** 避免争吵，但在 Boss 战后掉落 **"诅咒圣物"**（全队唯一，副作用巨大但加成极高），需要团队讨论谁来承担这个诅咒。

### 3.3 Left 4 Dead 2 (Valve)

#### ✅ 核心机制：AI Director

- **机制**: AI 导演根据玩家状态（血量、弹药、位置）动态控制刷怪节奏。如果玩家配合紧密，给予喘息；如果玩家落单，刷特感（Smoker/Hunter）惩罚。

#### 🎯 Vampirefall 借鉴点

- **惩罚落单**: 在大地图中，如果玩家距离队友过远，增加"刺客型"敌人的刷新率，强迫玩家抱团。

---

## 🔗 4. 参考资料 (References)

### 📄 必读文章

1.  **"Designing Co-op: The 4 Keys to Success"**  
    - 来源: Gamasutra  
    - 重点: 互补性、沟通、共享目标、去中心化。

2.  **"Left 4 Dead: The Director"**  
    - 来源: Valve Publications  
    - 重点: 动态节奏控制算法。

### 📺 视频分析

1.  **"What Makes a Good Co-op Game?"**  
    - 频道: Game Maker's Toolkit  
    - 链接: [YouTube](https://www.youtube.com/watch?v=sJd2f763VCA)

2.  **"How Deep Rock Galactic Solves the Co-op Problem"**  
    - 频道: Snoman Gaming  
    - 重点: 职业工具的设计。

---

## 📊 总结

### 🎯 Vampirefall 实施建议

1.  **资源分离**: 坚守"金币独立，以太共享"的原则，这是平衡个人爽感与团队策略的关键。
2.  **物理互补**: 设计至少 3 种能够改变地形或怪物路径的技能，促进物理层面的配合。
3.  **动态伸缩**: 编写 `DifficultyScaler` 模块，支持热插拔（中途加入/退出）。
4.  **社交标记**: 实现类似 Apex Legends 的 **Ping 系统**（"这里造塔"、"集火这个怪"），降低沟通成本。

---

**文档版本**: v1.0  
**最后更新**: 2025-12-04  
**维护者**: Vampirefall Design Team
