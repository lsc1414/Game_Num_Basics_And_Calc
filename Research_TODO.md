# 🎯 游戏知识图谱研究待办清单 (Research TODO List)

> **目标**: 系统性地研究业界标杆游戏，提取核心设计知识，为 Vampirefall 项目提供理论支撑。

---

## ✅ 已完成 (Completed)

- [x] **《杀戮尖塔》(Slay the Spire)** - DBG + Roguelike 核心机制
  - 文档: `Design/Roguelike_Deckbuilder_Knowledge_Map.md`
  - 完成时间: 2025-12-06
  
- [x] **《王权陨落》(Thronefall)** - 极简策略设计
  - 文档: `Design/Minimalist_Strategy_Design_Knowledge.md`
  - 完成时间: 2025-12-06

- [x] **《Risk of Rain 2》(雨中冒险2)** - 时间压力 + 物品协同 + 多人平衡
  - 文档: `Design/Risk_of_Rain_2_Knowledge_Map.md`
  - 完成时间: 2025-12-06

- [x] **《Deep Rock Galactic》(深岩银河)** - 职业互补 + 程序生成 + 合作机制
  - 文档: `Design/Deep_Rock_Galactic_Knowledge_Map.md`
  - 完成时间: 2025-12-06

- [x] **《Enter the Gungeon》(挺进地牢)** - 武器多样性 + 弹道系统 + 房间生成
  - 文档: `Design/Enter_the_Gungeon_Knowledge_Map.md`
  - 完成时间: 2025-12-06

- [x] **《Dead Cells》(死亡细胞)** - 颜色词缀 + 关卡分支 + 打击感
  - 文档: `Design/Dead_Cells_Knowledge_Map.md`
  - 完成时间: 2025-12-06

- [x] **《Dome Keeper》(圆顶守护者)** - 双阶段循环 + 资源管理
  - 文档: `Design/Dome_Keeper_Knowledge_Map.md`
  - 完成时间: 2025-12-06

- [x] **《Binding of Isaac》(以撒的结合)** - 道具协同 + 诅咒机制
  - 文档: `Design/Binding_of_Isaac_Knowledge_Map.md`
  - 完成时间: 2025-12-06

- [x] **《They Are Billions》(亿万僵尸)** - 经济螺旋 + 大规模优化
  - 文档: `Design/They_Are_Billions_Knowledge_Map.md`
  - 完成时间: 2025-12-06

- [x] **《Noita》(诺伊塔)** - 法术构建 + 物理模拟
  - 文档: `Design/Noita_Knowledge_Map.md`
  - 完成时间: 2025-12-06

- [x] **《Darkest Dungeon》(暗黑地牢)** - 压力系统 + 永久损失
  - 文档: `Design/Darkest_Dungeon_Knowledge_Map.md`
  - 完成时间: 2025-12-06

---

## 🔥 第一优先级 (High Priority) - 核心混合品类参考

### 1. 《Risk of Rain 2》(雨中冒险2)
- [ ] **状态**: 待研究
- **研究重点**:
  - ⏱️ 时间压力机制 (Difficulty Scaling Over Time)
  - 🔗 物品协同系统 (Item Synergy Matrix)
  - 👥 多人动态平衡 (1-4 Player Scaling)
  - 📊 伤害数值模型 (Exponential vs Linear Growth)
- **文档路径**: `Design/Risk_of_Rain_2_Knowledge_Map.md`
- **预计章节**:
  - 理论: 时间作为难度变量的数学模型
  - 实践: 物品池设计与概率控制
  - 案例: Artifact 系统与可选难度

### 2. 《Deep Rock Galactic》(深岩银河)
- [ ] **状态**: 待研究
- **研究重点**:
  - 🎭 职业互补设计 (Class Interdependence)
  - 🗺️ 程序生成洞穴 (Procedural Cave Generation)
  - 🤝 合作机制强制性 (Forced Cooperation Mechanics)
  - 📈 任务多样性系统 (Mission Variety Framework)
- **文档路径**: `Design/Deep_Rock_Galactic_Knowledge_Map.md`
- **预计章节**:
  - 理论: 职业设计的"能力互斥原则"
  - 实践: 3D 洞穴生成算法 (Marching Cubes)
  - 案例: Hazard Level 难度伸缩模型

### 3. 《Enter the Gungeon》(挺进地牢)
- [ ] **状态**: 待研究
- **研究重点**:
  - 🔫 武器多样性设计 (200+ Unique Guns)
  - 🎯 弹道系统优化 (Projectile Pooling)
  - 🏠 房间生成算法 (Room Layout Generation)
  - 💥 弹幕模式设计 (Bullet Pattern Design)
- **文档路径**: `Design/Enter_the_Gungeon_Knowledge_Map.md`
- **预计章节**:
  - 理论: 武器设计的"机制优先于数值"原则
  - 实践: 对象池与碰撞优化
  - 案例: Boss 弹幕的可读性设计

---

## ⚡ 第二优先级 (Medium Priority) - 特定系统深化

### 4. 《Dead Cells》(死亡细胞)
- [ ] **状态**: 待研究
- **研究重点**:
  - 🎨 武器词缀系统 (Color-Coded Affixes)
  - 🗺️ 关卡分支设计 (Branching Paths)
  - ✊ 打击感与手感 (Game Feel & Juice)
  - 🔄 Meta Progression 平衡 (Permanent Upgrades)
- **文档路径**: `Design/Dead_Cells_Knowledge_Map.md`

### 5. 《Dome Keeper》(圆顶守护者)
- [ ] **状态**: 待研究
- **研究重点**:
  - ⏰ 双阶段循环 (Mining vs Defending)
  - 💎 资源管理博弈 (Resource Allocation)
  - 🛡️ 塔防与采集结合 (Hybrid Loop Design)
  - 📉 时间压力递增 (Escalating Threat)
- **文档路径**: `Design/Dome_Keeper_Knowledge_Map.md`

### 6. 《Binding of Isaac》(以撒的结合)
- [ ] **状态**: 待研究
- **研究重点**:
  - 🧪 道具协同数学 (Multiplicative Synergies)
  - 🎲 房间布局生成 (Room Generation)
  - 😈 诅咒与祝福机制 (Risk/Reward Balance)
  - 🔢 数值膨胀控制 (Power Creep Management)
- **文档路径**: `Design/Binding_of_Isaac_Knowledge_Map.md`

---

## 🎨 第三优先级 (Low Priority) - 特殊维度参考

### 7. 《They Are Billions》(亿万僵尸)
- [ ] **状态**: 待研究
- **研究重点**:
  - 🏭 经济螺旋设计 (Economic Snowball)
  - 🧟 大规模单位优化 (10000+ Units Performance)
  - 💀 失败惩罚机制 (Permadeath Impact)
- **文档路径**: `Design/They_Are_Billions_Knowledge_Map.md`

### 8. 《Noita》(诺伊塔)
- [ ] **状态**: 待研究
- **研究重点**:
  - 🪄 法术模块化系统 (Spell Crafting)
  - 🌊 像素级物理模拟 (Pixel Physics)
  - 🎭 涌现式玩法 (Emergent Gameplay)
- **文档路径**: `Design/Noita_Knowledge_Map.md`

### 9. 《Darkest Dungeon》(暗黑地牢)
- [ ] **状态**: 待研究
- **研究重点**:
  - 😰 压力系统设计 (Stress Mechanics)
  - 💀 永久损失机制 (Permadeath & Replacement)
  - 📖 叙事与机制结合 (Narrative-Driven Mechanics)
- **文档路径**: `Design/Darkest_Dungeon_Knowledge_Map.md`

---

## 📋 执行规范 (Execution Standards)

每个研究文档必须包含以下章节：

### 1. 📚 理论基础 (Theoretical Basis)
- 核心定义
- 数学模型（如适用）
- 设计心理学

### 2. 🛠️ 实践应用 (Practical Implementation)
- Vampirefall 适配建议
- 数据结构设计
- 伪代码/算法逻辑
- Unity 实现要点

### 3. 🌟 业界优秀案例 (Industry Best Practices)
- 案例分析（2-3 个同类游戏）
- 优缺点对比
- 借鉴点与规避点

### 4. 🔗 参考资料 (References)
- 📄 相关论文
- 📺 GDC 演讲
- 🌐 技术博客/Wiki

---

## 📊 进度追踪 (Progress Tracking)

- **总计**: 11 个游戏
- **已完成**: 11 个 (100%) ✅
- **进行中**: 0 个
- **待开始**: 0 个

---

## 🎉 任务完成！(Mission Accomplished)

所有游戏知识图谱研究已完成！共创建了 **11 份深度研究文档**，涵盖：
- 卡牌构建 (DBG)
- 极简策略
- 时间压力系统
- 职业互补设计
- 武器多样性
- 打击感优化
- 双阶段循环
- 道具协同数学
- 经济螺旋
- 法术模块化
- 压力系统

所有文档均已索引到 `readme.md` 的 **"🎓 理论与策略"** 章节。

---

## 🎯 下一步行动 (Next Action)

**立即开始**: 《Risk of Rain 2》知识图谱研究

**命令**: `@/make-document 《Risk of Rain 2》的核心设计知识`

---

*最后更新: 2025-12-06*
