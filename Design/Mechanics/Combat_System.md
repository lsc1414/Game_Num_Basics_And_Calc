# ⚔️ 战斗系统详解 (Combat System Mechanics)

本文档定义了 Project Vampirefall 的核心战斗规则，包括伤害计算流程、属性相互作用、异常状态及控制机制。

---

## 1. 伤害类型与抗性 (Damage Types & Resistances)

为了保证战斗策略的深度，我们采用经典的“三系”分类。

### 1.1 物理 (Physical)
*   **特点:** 基础伤害高，暴击倍率通常较高。
*   **对抗属性:** **护甲 (Armor)**。
*   **穿透:** "Armor Penetration" 属性可忽视部分护甲。

### 1.2 元素 (Elemental)
*   **特点:** 附带异常状态 (Status Effects)，伤害波动较小。
*   **子类型:**
    *   🔥 **火焰 (Fire):** 纯伤害。DoT (持续伤害)。
    *   ❄️ **冰霜 (Cold):** 控制。减速 (Chill) / 冻结 (Freeze)。
    *   ⚡ **雷电 (Lightning):** 群体/爆发。感电 (Shock) 增加受到的伤害。
*   **对抗属性:** **元素抗性 (Elemental Resistance %)**。
    *   抗性上限默认为 75%。

### 1.3 混沌 (Chaos)
*   **特点:** 稀有伤害类型。无视能量护盾 (Energy Shield)。
*   **对抗属性:** **混沌抗性 (Chaos Resistance %)**。
    *   怪物通常混沌抗性较低。

---

### 🧠 理论原理：乘区理论与数值平衡

本部分解释了伤害类型与抗性系统的**数学基础**和**设计哲学**。

#### 🔢 数学基础：乘法 vs 减法公式

为什么物理伤害采用**除法公式**，而元素伤害采用**抗性减法公式**？这背后有深刻的数学考量：

1. **物理护甲（除法公式）：** `物理减伤 = 护甲 / (护甲 + K)`
   - **数学特性：** 护甲对有效生命值（EHP）的贡献是**线性增长**的，每3000点护甲将EHP翻倍
   - **设计意图：** 避免出现"不破防"的情况（攻击力 < 护甲 = 伤害为0），保证玩家总有进步空间
   - **K值选择：** K=3000时，3000护甲提供50%减伤，这是设计中的**黄金分割点**

2. **元素抗性（减法公式）：** `抗性倍率 = 1 - min((目标抗性 - 攻击者穿透), 75%)`
   - **数学特性：** 穿透属性直接做减法，鼓励玩家堆叠穿透来对抗高抗性敌人
   - **上限设计：** 抗性上限锁定为75%（减伤75%），防止无敌Build的出现
   - **穿透策略：** 玩家需要针对不同抗性的敌人调整穿透属性

#### 🏗️ 设计哲学：乘区理论（Bucket Theory）

引用自《数值手册》的**乘区理论**解释了伤害放大的根本机制：

- **增伤区（Inc - 加法稀释）：** 所有"增加XX%伤害"的词条相加，形成**第一个乘区**
  ```数学公式
  增伤总倍率 = 1 + Σ(增加伤害%)
  ```
  - **稀释效应：** 已有400%增伤时，再获得50%增伤的实际提升仅为10%

- **独立乘区（More - 独立放大）：** 每个"额外造成XX%伤害"都是**独立乘区**
  ```数学公式
  独立总倍率 = Π(1 + 额外伤害%)
  ```
  - **无稀释：** 无论已有多少增伤，20%独立增伤总是带来20%真实提升

- **天然乘区（维度攻击）：** 成功Build应在多个乘区同时投资
  | 乘区名称 | 作用原理 | 提升公式 |
  | :--- | :--- | :--- |
  | **基础区** | 技能倍率、点伤 | 直接增加底数 |
  | **增伤区** | Inc 词条 | `× (1 + Inc总和)` |
  | **攻速区** | 攻击频率 | `× APS` |
  | **暴击区** | 双倍伤害 | `× (1 + Rate × (Dmg - 1))` |
  | **易伤区** | 敌人受到的伤害 | `× (1 + EnemyTaken%)` |
  | **抗性区** | 穿透与减抗 | `× (1 - (Res - Pen))` |

**黄金法则：** `2 × 2 × 2 = 8`，而 `4 × 1 × 1 = 4`。均衡投资多个乘区收益更高。

#### 🎯 混沌伤害的设计哲学

为什么需要"混沌"这个伤害类型？
1. **机制定位：** 作为物理和元素的**补充维度**，提供第三种Build路线
2. **平衡考量：** 怪物混沌抗性普遍较低，给混沌Build独特的优势区间
3. **玩家体验：** 当玩家被物理/元素抗性墙卡住时，混沌提供破局思路

**混沌伤害的深层价值：** 它不仅是数值意义上的"第三系"，更是设计上的**安全阀**，防止玩家因抗性墙完全卡关。

#### 🔄 三系平衡的循环克制

参考《设计哲学文档》的**循环克制**理论：
- **物理 → 元素：** 高DPH（单发伤害）克制爆发脆皮
- **元素 → 混沌：** 状态效果克制低抗性敌人
- **混沌 → 物理：** 无视护盾克制堆甲单位

这种**三角克制关系**创造了动态的Build选择和装备需求，是长线内容消耗的关键设计。

---

### 🛠️ 实践举例：配置表设计与Excel计算

本部分提供可直接使用的**配置表示例**和**数值计算模板**。

#### 📊 伤害类型配置表（JSON格式）

```json
{
  "system": "damage_types",
  "version": "1.0",
  "last_updated": "2025-12-02",
  "damage_types": {
    "physical": {
      "display_name": "物理伤害",
      "icon": "icon_damage_physical",
      "resistance_attribute": "armor",
      "penetration_attribute": "armor_penetration",
      "base_critical_multiplier": 1.5,
      "color_code": "#FF6B35",
      "description": "基础伤害高，暴击倍率较高，受护甲减免",
      "special_rules": [
        "受护甲减伤公式影响",
        "可使用护甲穿透"
      ],
      "status_effect": "bleed",
      "status_chance_formula": "physical_status_chance"
    },
    "fire": {
      "display_name": "火焰伤害",
      "icon": "icon_damage_fire",
      "resistance_attribute": "fire_resistance",
      "penetration_attribute": "fire_penetration",
      "base_critical_multiplier": 1.3,
      "color_code": "#FF2E00",
      "description": "附带点燃效果，持续伤害",
      "special_rules": [
        "受元素抗性公式影响",
        "抗性上限75%",
        "可触发点燃状态"
      ],
      "status_effect": "ignite",
      "status_chance_formula": "fire_status_chance"
    },
    "cold": {
      "display_name": "冰霜伤害",
      "icon": "icon_damage_cold",
      "resistance_attribute": "cold_resistance",
      "penetration_attribute": "cold_penetration",
      "base_critical_multiplier": 1.2,
      "color_code": "#00D4FF",
      "description": "控制型伤害，减速和冻结",
      "special_rules": [
        "受元素抗性公式影响",
        "抗性上限75%",
        "可触发冰缓/冻结状态"
      ],
      "status_effect": "chill",
      "status_chance_formula": "cold_status_chance"
    },
    "lightning": {
      "display_name": "雷电伤害",
      "icon": "icon_damage_lightning",
      "resistance_attribute": "lightning_resistance",
      "penetration_attribute": "lightning_penetration",
      "base_critical_multiplier": 1.4,
      "color_code": "#FFE600",
      "description": "爆发型伤害，群体效果",
      "special_rules": [
        "受元素抗性公式影响",
        "抗性上限75%",
        "可触发感电状态"
      ],
      "status_effect": "shock",
      "status_chance_formula": "lightning_status_chance"
    },
    "chaos": {
      "display_name": "混沌伤害",
      "icon": "icon_damage_chaos",
      "resistance_attribute": "chaos_resistance",
      "penetration_attribute": "chaos_penetration",
      "base_critical_multiplier": 1.6,
      "color_code": "#AA00FF",
      "description": "稀有伤害类型，无视能量护盾",
      "special_rules": [
        "无视能量护盾（Energy Shield）",
        "怪物基础混沌抗性通常为0%",
        "抗性上限75%"
      ],
      "status_effect": null,
      "status_chance_formula": null
    }
  },
  "global_rules": {
    "resistance_cap": 0.75,
    "penetration_cap": 0.90,
    "minimum_damage_multiplier": 0.05,
    "armor_formula_constant": 3000
  }
}
```

#### 📈 抗性计算公式Excel模板

**Excel表格结构示例：**

| A | B | C | D | E | F | G | H |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **参数** | **数值** | **公式** | **说明** | **物理伤害** | **火焰伤害** | **冰霜伤害** | **雷电伤害** |
| 攻击力 | 500 | | 玩家基础攻击 | 500 | 500 | 500 | 500 |
| 技能倍率 | 150% | | 技能伤害系数 | 1.5 | 1.5 | 1.5 | 1.5 |
| 增伤总和 | 200% | | A类增伤总和 | 2.0 | 2.0 | 2.0 | 2.0 |
| 独立增伤 | 30% | | B类增伤 | 1.3 | 1.3 | 1.3 | 1.3 |
| 暴击期望 | 1.3 | `1+暴率*(爆伤-1)` | 暴击期望值 | 1.3 | 1.3 | 1.3 | 1.3 |
| 基础伤害 | 1125 | `攻击力*技能倍率` | 计算基础值 | 750 | 750 | 750 | 750 |
| 增伤后伤害 | 3375 | `基础*(1+增伤)` | A类增伤后 | 2250 | 2250 | 2250 | 2250 |
| 独立后伤害 | 4387.5 | `增伤后*独立增伤` | B类增伤后 | 2925 | 2925 | 2925 | 2925 |
| 暴击期望伤害 | 5703.75 | `独立后*暴击期望` | 暴击期望值 | 3802.5 | 3802.5 | 3802.5 | 3802.5 |
| 目标护甲 | 3000 | | 敌人护甲值 | 3000 | - | - | - |
| 护甲减伤 | 50% | `护甲/(护甲+3000)` | 物理减伤率 | 0.5 | - | - | - |
| 目标抗性 | 50% | | 元素抗性 | - | 0.5 | 0.5 | 0.5 |
| 穿透值 | 20% | | 玩家穿透属性 | - | 0.2 | 0.2 | 0.2 |
| 实际抗性 | 30% | `max(0,抗性-穿透)` | 计算后抗性 | - | 0.3 | 0.3 | 0.3 |
| 抗性上限 | 75% | | 抗性最大值 | - | 0.75 | 0.75 | 0.75 |
| 抗性倍率 | 70% | `1-min(实际抗性,上限)` | 最终倍率 | - | 0.7 | 0.7 | 0.7 |
| 最终伤害 | 2851.875 | `暴击期望*减伤倍率` | 实际造成伤害 | 1901.25 | 2661.75 | 2661.75 | 2661.75 |

**关键计算单元格公式（Excel格式）：**
- **物理减伤：** `=IF($B$11>0, $B$11/($B$11+$B$20), 0)`  // 护甲公式，K=3000
- **实际抗性：** `=MAX(0, $B$12-$B$13)`  // 抗性-穿透，最低为0
- **抗性倍率：** `=1-MIN($B$15, $B$14)`  // 考虑抗性上限
- **最终伤害：** `=IF(A4="物理", $B$9*(1-$B$10), $B$9*$B$16)`  // 分支计算

#### 🎮 Unity实现：伤害类型枚举与计算器

```csharp
// DamageType.cs - 伤害类型枚举
namespace Vampirefall.Combat
{
    /// <summary>
    /// 伤害类型枚举，用于标记伤害来源和抗性计算
    /// </summary>
    public enum DamageType
    {
        Physical = 0,    // 物理伤害
        Fire = 1,        // 火焰伤害
        Cold = 2,        // 冰霜伤害
        Lightning = 3,   // 雷电伤害
        Chaos = 4        // 混沌伤害
    }

    /// <summary>
    /// 伤害类型工具类，提供颜色、图标等元数据
    /// </summary>
    public static class DamageTypeUtility
    {
        private static readonly Dictionary<DamageType, DamageTypeInfo> _typeInfo = new()
        {
            { DamageType.Physical, new DamageTypeInfo {
                DisplayName = "物理伤害",
                Color = new Color(1f, 0.42f, 0.21f), // #FF6B35
                IconPath = "Icons/Damage/Physical",
                ResistanceAttribute = "Armor",
                PenetrationAttribute = "ArmorPenetration"
            }},
            { DamageType.Fire, new DamageTypeInfo {
                DisplayName = "火焰伤害",
                Color = new Color(1f, 0.18f, 0f), // #FF2E00
                IconPath = "Icons/Damage/Fire",
                ResistanceAttribute = "FireResistance",
                PenetrationAttribute = "FirePenetration"
            }},
            // ... 其他类型类似
        };

        public static DamageTypeInfo GetInfo(DamageType type) => _typeInfo[type];
    }

    public class DamageTypeInfo
    {
        public string DisplayName { get; set; }
        public Color Color { get; set; }
        public string IconPath { get; set; }
        public string ResistanceAttribute { get; set; }
        public string PenetrationAttribute { get; set; }
    }
}

// DamageCalculator.cs - 伤害计算核心
namespace Vampirefall.Combat
{
    public class DamageCalculator
    {
        // 物理伤害减伤计算
        public static float CalculateArmorReduction(float armor)
        {
            const float K = 3000f;
            return armor / (armor + K);
        }

        // 元素抗性倍率计算
        public static float CalculateResistanceMultiplier(float targetResistance, float attackerPenetration)
        {
            const float MAX_RESISTANCE = 0.75f;
            float effectiveResistance = Mathf.Max(0f, targetResistance - attackerPenetration);
            float clampedResistance = Mathf.Min(effectiveResistance, MAX_RESISTANCE);
            return 1f - clampedResistance;
        }

        // 完整伤害计算流程
        public static float CalculateFinalDamage(DamageRequest request)
        {
            // 1. 基础伤害计算
            float baseDamage = request.BaseDamage;

            // 2. 增伤区计算
            float increasedMultiplier = 1f + request.IncreasedDamageSum;
            baseDamage *= increasedMultiplier;

            // 3. 独立乘区计算
            foreach (float moreMultiplier in request.MoreMultipliers)
            {
                baseDamage *= (1f + moreMultiplier);
            }

            // 4. 暴击期望
            float critMultiplier = 1f + request.CritChance * (request.CritDamage - 1f);
            baseDamage *= critMultiplier;

            // 5. 防御减伤
            float defenseMultiplier = 1f;
            switch (request.DamageType)
            {
                case DamageType.Physical:
                    float armorReduction = CalculateArmorReduction(request.TargetArmor);
                    defenseMultiplier = 1f - armorReduction;
                    break;
                case DamageType.Fire:
                case DamageType.Cold:
                case DamageType.Lightning:
                case DamageType.Chaos:
                    float resistanceMultiplier = CalculateResistanceMultiplier(
                        request.TargetResistance,
                        request.AttackerPenetration
                    );
                    defenseMultiplier = resistanceMultiplier;
                    break;
            }

            // 6. 最终伤害
            float finalDamage = baseDamage * defenseMultiplier;

            // 7. 最低伤害保护
            const float MIN_DAMAGE_MULTIPLIER = 0.05f;
            float minimumDamage = request.BaseDamage * MIN_DAMAGE_MULTIPLIER;
            return Mathf.Max(finalDamage, minimumDamage);
        }
    }

    public class DamageRequest
    {
        public DamageType DamageType { get; set; }
        public float BaseDamage { get; set; }
        public float IncreasedDamageSum { get; set; }
        public List<float> MoreMultipliers { get; set; } = new();
        public float CritChance { get; set; }
        public float CritDamage { get; set; }
        public float TargetArmor { get; set; }
        public float TargetResistance { get; set; }
        public float AttackerPenetration { get; set; }
    }
}
```

#### 📁 配置文件组织结构

建议的项目文件结构：
```
Assets/
├── _Project/
│   ├── Core/
│   │   └── Combat/
│   │       ├── DamageType.cs
│   │       ├── DamageCalculator.cs
│   │       └── DamageRequest.cs
│   ├── Data/
│   │   └── Configs/
│   │       ├── DamageTypes.json
│   │       ├── Resistances.json
│   │       └── PenetrationCurves.json
│   └── Resources/
│       └── Combat/
│           ├── Icons/
│           │   ├── Damage/
│           │   │   ├── Physical.png
│           │   │   ├── Fire.png
│           │   │   └── ...
│           └── Materials/
│               ├── DamageVFX/
│               │   ├── M_Damage_Physical.mat
│               │   ├── M_Damage_Fire.mat
│               └── ...
```

#### 🧪 测试用例示例

```csharp
// DamageCalculatorTests.cs - 单元测试
using NUnit.Framework;

namespace Vampirefall.Tests.Combat
{
    [TestFixture]
    public class DamageCalculatorTests
    {
        [Test]
        public void CalculateArmorReduction_ZeroArmor_ReturnsZero()
        {
            float reduction = DamageCalculator.CalculateArmorReduction(0f);
            Assert.AreEqual(0f, reduction);
        }

        [Test]
        public void CalculateArmorReduction_KValueArmor_Returns50Percent()
        {
            float reduction = DamageCalculator.CalculateArmorReduction(3000f);
            Assert.AreEqual(0.5f, reduction, 0.01f);
        }

        [Test]
        public void CalculateResistanceMultiplier_FullPenetration_Returns100Percent()
        {
            float multiplier = DamageCalculator.CalculateResistanceMultiplier(50f, 50f);
            Assert.AreEqual(1f, multiplier);
        }

        [Test]
        public void CalculateResistanceMultiplier_OverPenetration_Returns100Percent()
        {
            float multiplier = DamageCalculator.CalculateResistanceMultiplier(30f, 50f);
            Assert.AreEqual(1f, multiplier);
        }

        [Test]
        public void CalculateFinalDamage_PhysicalWithArmor_CalculatesCorrectly()
        {
            var request = new DamageRequest
            {
                DamageType = DamageType.Physical,
                BaseDamage = 1000f,
                IncreasedDamageSum = 1f, // +100%增伤
                MoreMultipliers = new List<float> { 0.2f }, // +20%独立
                CritChance = 0.5f,
                CritDamage = 1.5f,
                TargetArmor = 3000f // 50%减伤
            };

            float damage = DamageCalculator.CalculateFinalDamage(request);

            // 计算验证：
            // 基础伤害: 1000
            // 增伤后: 1000 * (1+1) = 2000
            // 独立后: 2000 * 1.2 = 2400
            // 暴击期望: 2400 * (1+0.5*(1.5-1)) = 2400 * 1.25 = 3000
            // 护甲减伤: 3000 * (1-0.5) = 1500
            float expected = 1500f;
            Assert.AreEqual(expected, damage, 0.01f);
        }
    }
}
```

---

### 🏆 业界案例：PoE伤害系统深度分析

《流放之路》（Path of Exile）被认为是ARPG中**伤害系统设计的天花板**，其设计哲学对我们的塔防+肉鸽混合玩法有重要启示。

#### 🎯 PoE伤害系统的三大支柱

1. **乘区理论的极致运用**
   - **Inc（增伤）区：** 超过200种不同的"增加伤害"词条，但全部相加
   - **More（独立）区：** 珍稀的独立乘区，每个都是单独乘法
   - **天然乘区：** 伤害效用（Damage Effectiveness）、攻速、暴击、穿透、减抗等

   **关键启示：** PoE通过大量Inc词条制造**稀释效应**，引导玩家追求More词条和开辟新乘区。

2. **伤害类型的深度分化**
   - **物理伤害：** 基础值高，可转化为元素或混沌
   - **元素伤害：** 三系各有特色，火=持续，冰=控制，电=爆发
   - **混沌伤害：** 稀有但无视能量护盾，针对特定场景

   **关键启示：** 伤害类型不仅是特效差异，更是**策略选择**。玩家需要根据敌人抗性调整伤害类型。

3. **穿透与减抗的博弈**
   - **穿透（Penetration）：** 直接减法，简单粗暴
   - **减抗（Resistance Reduction）：** 百分比降低，对高抗性目标更有效
   - **暴露（Exposure）：** 施加debuff，团队共享

   **关键启示：** 多种抗性对抗手段创造了Build多样性，防止单一最优解。

#### 📊 PoE vs 我们设计的对比分析

| 设计维度 | PoE的实现 | 我们的调整（塔防+肉鸽） | 设计理由 |
| :--- | :--- | :--- | :--- |
| **物理伤害公式** | 减法公式 `max(伤害-护甲, 0)` | **除法公式** `伤害×护甲减伤` | 避免"不破防"的挫败感，更适合肉鸽的成长性 |
| **元素抗性上限** | 90%（通过天赋/装备） | **75%固定上限** | 控制数值膨胀，保证玩家总有破局手段 |
| **混沌伤害定位** | 稀有伤害，无视能量护盾 | **策略补充**，怪物低抗性 | 作为物理/元素Build的补充，防止卡关 |
| **穿透机制** | 多种方式：穿透、减抗、暴露 | **简化穿透**，直接减法 | 降低玩家认知成本，聚焦塔防策略 |
| **伤害转换** | 自由转换（物转火、火转混沌等） | **限制转换**，稀有词条 | 保持伤害类型的独特性，鼓励针对性Build |

#### 💡 从PoE吸取的核心教训

1. **稀释效应的正确使用**
   - **PoE成功之处：** 大量Inc词条让新手期成长感明显，后期引导追求More词条
   - **我们需要：** 在肉鸽局内成长中复制这种体验，前期给Inc，后期给More

2. **抗性墙的动态设计**
   - **PoE成功之处：** 不同地图有不同怪物抗性，强迫玩家调整Build
   - **我们需要：** 在塔防波次中引入"抗性波"，如第10波火抗+50%

3. **Build多样性的保障**
   - **PoE成功之处：** 任何伤害类型都有通关潜力
   - **我们需要：** 确保物理、元素、混沌都有**专属的强势场景**

#### 🎮 实战案例：PoE的"火焰陷阱"Build分析

**Build核心思路：**
1. **基础伤害：** 火焰陷阱技能，100%火焰伤害
2. **Inc区：** 火焰伤害%、法术伤害%、范围伤害%等，总计约+600%
3. **More区：** 陷阱伤害+40%、燃烧伤害+30%、对燃烧敌人伤害+20%
4. **穿透区：** 火焰穿透+40%，火焰暴露-25%抗性
5. **防御穿透：** 专注于降低敌人火抗

**对我们的启示：**
- **清晰的乘区划分：** 玩家明确知道要堆哪些属性
- **针对性的穿透策略：** 专门应对高火抗敌人
- **状态联动：** 燃烧状态触发额外增伤

#### ⚠️ PoE的失败教训：数值膨胀失控

**问题：** 后期赛季伤害数字达到**数十亿**，抗性数值完全失去意义

**我们的防范措施：**
1. **严格的数值上限：** 护甲K值锁定3000，抗性上限75%
2. **乘区数量限制：** More乘区不超过5个，防止指数爆炸
3. **关卡动态调整：** 根据玩家强度动态调整怪物抗性

#### 🔄 适配塔防肉鸽的改造方案

将PoE的伤害系统**简化并适配**到塔防+肉鸽玩法：

1. **简化乘区：** 3个核心乘区（基础、增伤、独立）代替PoE的10+个乘区
2. **视觉化反馈：** 塔的攻击特效明确显示伤害类型
3. **肉鸽式获取：** 每局随机获得伤害类型相关的祝福/词条
4. **塔防协同：** 不同伤害类型的塔产生化学反应（如冰塔减速+火塔爆击）

**最终目标：** 保留PoE的深度策略性，但大幅降低学习成本，让玩家在**一局游戏内**就能体验到Build成型的乐趣。

---

---

## 2. 异常状态 (Status Ailments)

异常状态不仅是视觉效果，更是 Build 构建的核心。

| 状态 | 元素来源 | 触发条件 | 效果详解 | 阈值/公式 |
| :--- | :--- | :--- | :--- | :--- |
| **点燃 (Ignite)** | 🔥 火焰 | 暴击 或 几率 | 4秒内造成 50% 基础点伤/秒。不可叠加，只取最高值。 | 伤害基于单次击中伤害 |
| **冰缓 (Chill)** | ❄️ 冰霜 | 任何冰霜伤害 | 减少 10%~30% 动作速度，持续 2秒。 | 取决于伤害占目标最大HP的比例 |
| **冻结 (Freeze)** | ❄️ 冰霜 | 暴击 或 几率 | 无法行动。持续 0.3s ~ 3s。 | 若冻结时间<0.3s则不触发 |
| **感电 (Shock)** | ⚡ 雷电 | 任何雷电伤害 | 受到的所有伤害增加 10%~50%。持续 2秒。 | 取决于伤害占目标最大HP的比例 |
| **流血 (Bleed)** | ⚔️ 物理 | 技能特定 | 移动时受到额外物理伤害。可叠加 3 层。 | 基础伤害的 30%/秒 |

*注意: 所有异常状态的计算逻辑需遵循 `Design/Numerical_Manual.md` 中的 PRD 随机分布。*

---

### 🧠 理论原理：状态机设计与PRD算法

异常状态系统不仅是视觉效果，更是游戏策略深度的核心体现。本部分从**数学原理**和**设计哲学**两个维度解析状态系统的设计。

#### 🔢 数学基础：状态持续时间与强度计算

1. **持续时间公式设计：**
   - **线性公式：** `最终时长 = 基础时长 × (1 + 状态强度%)`
     - *优点：* 直观易懂，计算简单
     - *缺点：* 强度堆叠可能导致时长失控
   - **对数公式：** `最终时长 = 基础时长 × log(1 + 状态强度%)`
     - *优点：* 防止数值爆炸，后期收益递减
     - *缺点：* 玩家感知不直观

   **我们的选择：** 采用线性公式，但通过**硬上限**控制（如冻结最长3秒）

2. **状态强度与触发率的数学关系：**
   - **触发率公式：** `最终触发率 = 基础触发率 × (1 + 幸运值%) × PRD修正`
   - **强度公式：** `最终强度 = 基础强度 × (1 + 状态效果%)`
   - **关键设计：** 触发率和强度**解耦**，允许玩家分别构建

3. **状态叠加的数学模型：**
   - **不可叠加（点燃）：** 只取最高值，数学期望稳定
     ```数学公式
     期望伤害 = max(状态1伤害, 状态2伤害, ...)
     ```
   - **可叠加（流血）：** 层数机制，边际收益递减
     ```数学公式
     总伤害 = 基础伤害 × (1 + 0.3 × min(层数, 3))
     ```

#### 🏗️ 设计哲学：状态机与玩家策略

引用自《设计哲学文档》的**状态机理论**：

1. **状态作为决策节点：**
   - 玩家看到敌人被**点燃** → 决策：追加火伤触发爆燃
   - 玩家看到敌人被**冰冻** → 决策：使用重击造成碎冰
   - 玩家看到敌人被**感电** → 决策：爆发输出最大化伤害

2. **状态协同的化学反应：**
   参考《设计哲学文档》的**协同效应三个层级**：
   - **C级（线性）：** 点燃+火焰伤害，简单叠加
   - **B级（乘法）：** 冰冻+碎冰伤害，倍率放大
   - **S级（质变）：** 感电+连锁闪电，机制改变

3. **状态抗性的动态平衡：**
   - **Boss韧性设计：** Boss拥有高状态抗性，防止被无限控制
   - **玩家Build专精：** 状态流Build通过堆叠"状态强度"和"状态持续时间"突破抗性
   - **动态难度调整：** 根据玩家状态强度动态调整怪物状态抗性

#### 🔄 PRD算法在状态系统的应用

为什么状态触发必须使用PRD（伪随机分布）？

1. **体验稳定性：**
   - **真随机问题：** 10%触发率可能连续10次不触发，玩家感觉"技能坏了"
   - **PRD解决方案：** 保证小样本下接近期望概率，每10次攻击大约触发1次

2. **PRD算法实现（引用自《数值手册》）：**
   ```csharp
   public class StatusPRD
   {
       private int _counter = 1;

       public bool CheckStatusTrigger(float baseChance)
       {
           float C = PRDTable.LookupC(baseChance); // 查表获得C值
           if (Random.value < C * _counter)
           {
               _counter = 1;
               return true;
           }
           else
           {
               _counter++;
               return false;
           }
       }
   }
   ```

3. **状态专属PRD表：**
   | 基础触发率 | C值 | 实际体验 |
   | :--- | :--- | :--- |
   | **5%** | 0.0038 | 大约每20次触发1次 |
   | **10%** | 0.014 | 大约每10次触发1次 |
   | **25%** | 0.084 | 大约每4次触发1次 |
   | **50%** | 0.302 | 大约每2次触发1次 |

#### 🎯 五类状态的设计定位

1. **伤害型状态（点燃）：**
   - **定位：** 持续输出，弥补爆发间隔
   - **数学特性：** 伤害基于单次击中，鼓励高DPH（单发伤害）
   - **策略价值：** 逼迫敌人移动或承受持续伤害

2. **控制型状态（冰缓/冻结）：**
   - **定位：** 战场控制，创造输出窗口
   - **数学特性：** 持续时间与伤害比例相关，鼓励集中火力
   - **策略价值：** 打断敌人技能，保护关键目标

3. **易伤型状态（感电）：**
   - **定位：** 伤害放大器，团队收益
   - **数学特性：** 增伤比例与伤害比例相关，鼓励高爆发
   - **策略价值：** 标记高优先级目标，集火秒杀

4. **移动惩罚状态（流血）：**
   - **定位：** 限制走位，区域控制
   - **数学特性：** 移动时触发额外伤害，惩罚闪避流
   - **策略价值：** 逼迫敌人站桩或承受额外伤害

5. **特殊状态（混沌专属）：**
   - **预留设计空间**，为未来扩展准备

---

### 🛠️ 实践举例：状态配置表与PRD计算

本部分提供可直接使用的**状态系统配置表**和**计算工具**。

#### 📊 异常状态配置表（JSON格式）

```json
{
  "system": "status_ailments",
  "version": "1.0",
  "last_updated": "2025-12-02",
  "status_effects": {
    "ignite": {
      "display_name": "点燃",
      "damage_type": "fire",
      "trigger_conditions": ["critical_hit", "chance_based"],
      "base_duration": 4.0,
      "damage_formula": "source_damage * 0.5 * (1 + status_potency)",
      "damage_interval": 1.0,
      "stacking_behavior": "refresh_max",
      "max_stacks": 1,
      "visual_effects": {
        "particle": "FX_Status_Ignite",
        "material_overlay": "M_Overlay_Burn",
        "sound_loop": "SFX_Burning_Loop"
      },
      "special_rules": [
        "伤害基于触发时的单次击中伤害（快照机制）",
        "不可叠加，新点燃覆盖旧点燃（取较高值）",
        "可被'免疫点燃'或'火焰抗性'抵抗"
      ],
      "prd_settings": {
        "use_prd": true,
        "base_chance": 0.10,
        "c_value": 0.014
      }
    },
    "chill": {
      "display_name": "冰缓",
      "damage_type": "cold",
      "trigger_conditions": ["any_cold_damage"],
      "base_duration": 2.0,
      "effect_formula": "slow_percentage = clamp(10 + 20 * (damage / target_max_hp), 10, 30)",
      "stacking_behavior": "refresh",
      "max_stacks": 1,
      "visual_effects": {
        "particle": "FX_Status_Chill",
        "material_overlay": "M_Overlay_Frost",
        "sound_loop": "SFX_Chill_Loop"
      },
      "special_rules": [
        "减速比例取决于伤害占目标最大HP的比例",
        "可与冻结状态共存，但效果不叠加",
        "可被'免疫缓速'或'冰霜抗性'抵抗"
      ],
      "prd_settings": {
        "use_prd": false,
        "trigger_guaranteed": true
      }
    },
    "freeze": {
      "display_name": "冻结",
      "damage_type": "cold",
      "trigger_conditions": ["critical_hit", "chance_based"],
      "duration_formula": "clamp(0.3 + 2.7 * (damage / target_max_hp), 0.3, 3.0)",
      "stacking_behavior": "refresh",
      "max_stacks": 1,
      "visual_effects": {
        "particle": "FX_Status_Freeze",
        "material_overlay": "M_Overlay_Ice",
        "sound_loop": "SFX_Freeze_Loop"
      },
      "special_rules": [
        "完全无法行动，包括移动、攻击、施法",
        "持续时间小于0.3秒时不触发视觉效果",
        "受到伤害时可能提前打破（碎冰机制）"
      ],
      "prd_settings": {
        "use_prd": true,
        "base_chance": 0.15,
        "c_value": 0.032
      }
    },
    "shock": {
      "display_name": "感电",
      "damage_type": "lightning",
      "trigger_conditions": ["any_lightning_damage"],
      "base_duration": 2.0,
      "effect_formula": "damage_taken_increase = clamp(10 + 40 * (damage / target_max_hp), 10, 50)",
      "stacking_behavior": "refresh_max",
      "max_stacks": 1,
      "visual_effects": {
        "particle": "FX_Status_Shock",
        "material_overlay": "M_Overlay_Electric",
        "sound_loop": "SFX_Shock_Loop"
      },
      "special_rules": [
        "增加目标受到的所有类型伤害",
        "增伤比例取决于伤害占目标最大HP的比例",
        "团队共享效果，所有玩家受益"
      ],
      "prd_settings": {
        "use_prd": false,
        "trigger_guaranteed": true
      }
    },
    "bleed": {
      "display_name": "流血",
      "damage_type": "physical",
      "trigger_conditions": ["skill_specific"],
      "base_duration": 5.0,
      "damage_formula": "source_damage * 0.3 * (1 + status_potency) / stack_count",
      "damage_interval": 1.0,
      "stacking_behavior": "stack",
      "max_stacks": 3,
      "visual_effects": {
        "particle": "FX_Status_Bleed",
        "material_overlay": "M_Overlay_Bleed",
        "sound_loop": "SFX_Bleed_Loop"
      },
      "special_rules": [
        "移动时触发额外伤害（原伤害的200%）",
        "层数独立计算持续时间",
        "可被'免疫流血'或'物理抗性'抵抗"
      ],
      "prd_settings": {
        "use_prd": true,
        "base_chance": 0.20,
        "c_value": 0.055
      }
    }
  },
  "global_settings": {
    "minimum_duration": 0.1,
    "status_resistance_formula": "final_duration = base_duration * (1 - min(status_resistance, 0.9))",
    "tenacity_formula": "final_duration = base_duration * (1 - min(tenacity, 0.75))",
    "boss_immunities": ["freeze", "stun"],
    "player_build_options": {
      "status_potency_max": 2.0,
      "duration_increase_max": 1.0,
      "chance_increase_max": 1.0
    }
  }
}
```

#### 📈 状态效果计算Excel模板

**Excel表格结构示例：**

| A | B | C | D | E | F | G |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **参数** | **数值** | **公式** | **说明** | **点燃** | **冰缓** | **流血** |
| 基础伤害 | 1000 | | 触发状态的单次伤害 | 1000 | 1000 | 1000 |
| 目标最大HP | 5000 | | 敌人最大生命值 | 5000 | 5000 | 5000 |
| 状态强度 | 50% | | 玩家状态强度属性 | 0.5 | 0.5 | 0.5 |
| 状态抗性 | 30% | | 敌人状态抗性 | 0.3 | 0.3 | 0.3 |
| 基础触发率 | 10% | | 技能基础触发率 | 0.1 | 1.0 | 0.2 |
| 玩家幸运值 | 20% | | 增加触发率 | 0.2 | - | 0.2 |
| **计算列** | **结果** | **公式** | **说明** | **数值** | **数值** | **数值** |
| 最终触发率 | 12% | `基础×(1+幸运)×PRD修正` | 实际触发率 | 0.12 | 1.0 | 0.24 |
| 状态持续时间 | 4.8秒 | `基础×(1+强度)×(1-抗性)` | 计算后时长 | 4.8 | 1.4 | 3.5 |
| 每秒伤害 | 750 | `基础×0.5×(1+强度)` | 点燃DPS | 750 | - | - |
| 总伤害 | 3600 | `DPS×持续时间` | 期望总伤害 | 3600 | - | - |
| 减速比例 | 14% | `10+20×(伤害/最大HP)` | 冰缓效果 | - | 0.14 | - |
| 层数伤害 | 450/秒 | `基础×0.3×(1+强度)` | 单层流血 | - | - | 450 |
| 三层伤害 | 1350/秒 | `单层×3` | 满层流血 | - | - | 1350 |
| 移动惩罚 | 2700/秒 | `三层×200%` | 移动时伤害 | - | - | 2700 |

**关键计算单元格公式（Excel格式）：**
- **最终触发率：** `=IF(PRD启用, PRD查表($B$6), $B$6*(1+$B$7))`
- **状态持续时间：** `=$B$4*(1+$B$3)*(1-MIN($B$5,0.9))`
- **点燃DPS：** `=$B$2*0.5*(1+$B$3)`
- **冰缓减速：** `=MIN(MAX(10+20*($B$2/$B$8),10),30)/100`
- **流血单层：** `=$B$2*0.3*(1+$B$3)`

#### 🎮 Unity实现：状态系统核心代码

```csharp
// StatusEffect.cs - 状态效果基类
namespace Vampirefall.Combat.Status
{
    public enum StatusType
    {
        Ignite,
        Chill,
        Freeze,
        Shock,
        Bleed
    }

    public enum StackingBehavior
    {
        Refresh,        // 刷新持续时间
        RefreshMax,     // 刷新并取最高值
        Stack,          // 叠加层数
        Independent     // 独立实例
    }

    public abstract class StatusEffect
    {
        public StatusType Type { get; protected set; }
        public float Duration { get; protected set; }
        public float RemainingTime { get; protected set; }
        public int Stacks { get; protected set; }
        public float Potency { get; protected set; } // 状态强度
        public StackingBehavior Stacking { get; protected set; }
        public int MaxStacks { get; protected set; }

        // 快照机制：记录施加时的伤害值
        public float SnapshotDamage { get; protected set; }

        protected CombatUnit _target;
        protected StatusSystem _system;

        public virtual void Apply(CombatUnit target, float sourceDamage, float statusPotency)
        {
            _target = target;
            SnapshotDamage = sourceDamage;
            Potency = statusPotency;

            // 根据堆叠行为处理
            switch (Stacking)
            {
                case StackingBehavior.Refresh:
                    RemainingTime = Duration;
                    break;
                case StackingBehavior.RefreshMax:
                    RemainingTime = Mathf.Max(RemainingTime, Duration);
                    break;
                case StackingBehavior.Stack:
                    if (Stacks < MaxStacks)
                    {
                        Stacks++;
                        RemainingTime = Duration;
                    }
                    break;
            }

            OnApply();
        }

        public virtual void Update(float deltaTime)
        {
            RemainingTime -= deltaTime;
            if (RemainingTime <= 0)
            {
                if (Stacking == StackingBehavior.Stack && Stacks > 1)
                {
                    Stacks--;
                    RemainingTime = Duration;
                }
                else
                {
                    Expire();
                }
            }
            else
            {
                OnUpdate(deltaTime);
            }
        }

        protected abstract void OnApply();
        protected abstract void OnUpdate(float deltaTime);
        protected abstract void OnExpire();

        public void Expire()
        {
            OnExpire();
            _system.RemoveStatus(this);
        }
    }

    // 具体状态实现：点燃
    public class IgniteStatus : StatusEffect
    {
        private float _damagePerSecond;
        private float _damageAccumulator;
        private const float DAMAGE_INTERVAL = 1.0f;

        public IgniteStatus()
        {
            Type = StatusType.Ignite;
            Duration = 4.0f;
            Stacking = StackingBehavior.RefreshMax;
            MaxStacks = 1;
        }

        protected override void OnApply()
        {
            // 快照机制：基于施加时的伤害计算DPS
            _damagePerSecond = SnapshotDamage * 0.5f * (1f + Potency);
            _damageAccumulator = 0f;

            // 视觉效果
            _target.PlayParticleEffect("FX_Status_Ignite");
            _target.ApplyMaterialOverlay("M_Overlay_Burn");
        }

        protected override void OnUpdate(float deltaTime)
        {
            _damageAccumulator += deltaTime;
            if (_damageAccumulator >= DAMAGE_INTERVAL)
            {
                int ticks = Mathf.FloorToInt(_damageAccumulator / DAMAGE_INTERVAL);
                for (int i = 0; i < ticks; i++)
                {
                    _target.TakeDamage(_damagePerSecond, DamageType.Fire, "ignite");
                }
                _damageAccumulator -= ticks * DAMAGE_INTERVAL;
            }
        }

        protected override void OnExpire()
        {
            _target.StopParticleEffect("FX_Status_Ignite");
            _target.RemoveMaterialOverlay("M_Overlay_Burn");
        }
    }

    // 具体状态实现：冰缓
    public class ChillStatus : StatusEffect
    {
        private float _slowPercentage;

        public ChillStatus()
        {
            Type = StatusType.Chill;
            Duration = 2.0f;
            Stacking = StackingBehavior.Refresh;
            MaxStacks = 1;
        }

        protected override void OnApply()
        {
            // 根据伤害比例计算减速比例
            float damageRatio = SnapshotDamage / _target.MaxHealth;
            _slowPercentage = Mathf.Clamp(10f + 20f * damageRatio, 10f, 30f) / 100f;

            _target.MovementSpeedMultiplier *= (1f - _slowPercentage);
            _target.AttackSpeedMultiplier *= (1f - _slowPercentage * 0.5f); // 攻击速度受影响较小

            _target.PlayParticleEffect("FX_Status_Chill");
        }

        protected override void OnUpdate(float deltaTime) { }

        protected override void OnExpire()
        {
            _target.MovementSpeedMultiplier /= (1f - _slowPercentage);
            _target.AttackSpeedMultiplier /= (1f - _slowPercentage * 0.5f);
            _target.StopParticleEffect("FX_Status_Chill");
        }
    }
}

// StatusSystem.cs - 状态管理系统
namespace Vampirefall.Combat.Status
{
    public class StatusSystem
    {
        private CombatUnit _owner;
        private Dictionary<StatusType, StatusEffect> _activeStatuses = new();
        private List<StatusEffect> _statusQueue = new();

        // PRD计数器（每个状态类型独立）
        private Dictionary<StatusType, PRDCounter> _prdCounters = new();

        public StatusSystem(CombatUnit owner)
        {
            _owner = owner;

            // 初始化PRD计数器
            foreach (StatusType type in Enum.GetValues(typeof(StatusType)))
            {
                _prdCounters[type] = new PRDCounter();
            }
        }

        public void Update(float deltaTime)
        {
            // 更新所有活跃状态
            foreach (var status in _activeStatuses.Values.ToList())
            {
                status.Update(deltaTime);
            }

            // 处理状态队列
            ProcessStatusQueue();
        }

        public bool TryApplyStatus(StatusType type, float sourceDamage, float statusPotency, float baseChance)
        {
            // 1. 检查免疫
            if (_owner.IsImmuneToStatus(type))
                return false;

            // 2. PRD判定
            bool triggered = _prdCounters[type].Check(baseChance);
            if (!triggered)
                return false;

            // 3. 抵抗判定
            float statusResistance = _owner.GetStatusResistance(type);
            float resistanceRoll = Random.value;
            if (resistanceRoll < statusResistance)
                return false;

            // 4. 创建状态实例
            StatusEffect status = CreateStatusInstance(type);
            if (status == null)
                return false;

            // 5. 加入队列（下一帧处理，避免迭代时修改集合）
            _statusQueue.Add(status);
            status.Apply(_owner, sourceDamage, statusPotency);

            return true;
        }

        private StatusEffect CreateStatusInstance(StatusType type)
        {
            return type switch
            {
                StatusType.Ignite => new IgniteStatus(),
                StatusType.Chill => new ChillStatus(),
                StatusType.Freeze => new FreezeStatus(),
                StatusType.Shock => new ShockStatus(),
                StatusType.Bleed => new BleedStatus(),
                _ => null
            };
        }

        private void ProcessStatusQueue()
        {
            foreach (var status in _statusQueue)
            {
                if (_activeStatuses.TryGetValue(status.Type, out var existing))
                {
                    // 根据堆叠行为处理
                    switch (status.Stacking)
                    {
                        case StackingBehavior.RefreshMax:
                            if (status.Potency > existing.Potency)
                            {
                                existing.Expire();
                                _activeStatuses[status.Type] = status;
                            }
                            break;
                        default:
                            _activeStatuses[status.Type] = status;
                            break;
                    }
                }
                else
                {
                    _activeStatuses[status.Type] = status;
                }
            }
            _statusQueue.Clear();
        }

        public void RemoveStatus(StatusEffect status)
        {
            _activeStatuses.Remove(status.Type);
        }

        public bool HasStatus(StatusType type) => _activeStatuses.ContainsKey(type);
        public StatusEffect GetStatus(StatusType type) => _activeStatuses.GetValueOrDefault(type);
    }

    // PRD计数器
    public class PRDCounter
    {
        private int _counter = 1;

        public bool Check(float targetProbability)
        {
            float C = PRDTable.GetC(targetProbability);
            if (Random.value < C * _counter)
            {
                _counter = 1;
                return true;
            }
            else
            {
                _counter++;
                return false;
            }
        }
    }
}
```

#### 📁 状态系统文件结构

```
Assets/
├── _Project/
│   ├── Core/
│   │   └── Combat/
│   │       ├── Status/
│   │       │   ├── StatusEffect.cs
│   │       │   ├── IgniteStatus.cs
│   │       │   ├── ChillStatus.cs
│   │       │   ├── FreezeStatus.cs
│   │       │   ├── ShockStatus.cs
│   │       │   ├── BleedStatus.cs
│   │       │   ├── StatusSystem.cs
│   │       │   └── PRDCounter.cs
│   │       └── ...
│   ├── Data/
│   │   └── Configs/
│   │       ├── StatusEffects.json
│   │       ├── StatusResistanceCurves.json
│   │       └── PRDTable.json
│   └── Resources/
│       └── Combat/
│           ├── VFX/
│           │   ├── Status/
│           │   │   ├── FX_Status_Ignite.prefab
│           │   │   ├── FX_Status_Chill.prefab
│           │   │   └── ...
│           └── Materials/
│               ├── Overlays/
│               │   ├── M_Overlay_Burn.mat
│               │   ├── M_Overlay_Frost.mat
│               └── ...
```

#### 🧪 测试用例示例

```csharp
// StatusSystemTests.cs - 单元测试
using NUnit.Framework;

namespace Vampirefall.Tests.Combat.Status
{
    [TestFixture]
    public class StatusSystemTests
    {
        [Test]
        public void IgniteStatus_AppliesDamageOverTime()
        {
            // 准备
            var target = new MockCombatUnit(maxHealth: 1000);
            var statusSystem = new StatusSystem(target);
            var ignite = new IgniteStatus();

            // 执行
            bool applied = statusSystem.TryApplyStatus(
                StatusType.Ignite,
                sourceDamage: 500f,
                statusPotency: 0.5f,
                baseChance: 1.0f
            );

            // 验证
            Assert.IsTrue(applied);
            Assert.IsTrue(statusSystem.HasStatus(StatusType.Ignite));

            // 模拟4秒更新
            for (int i = 0; i < 4; i++)
            {
                statusSystem.Update(1.0f);
            }

            // 期望伤害：500 * 0.5 * (1+0.5) = 375 DPS，4秒总计1500
            // 但由于目标只有1000血，实际伤害受限于目标血量
            Assert.IsTrue(target.CurrentHealth < 1000);
        }

        [Test]
        public void ChillStatus_ReducesMovementSpeed()
        {
            // 准备
            var target = new MockCombatUnit(maxHealth: 1000);
            target.MovementSpeed = 5.0f;
            var statusSystem = new StatusSystem(target);

            // 执行
            bool applied = statusSystem.TryApplyStatus(
                StatusType.Chill,
                sourceDamage: 250f, // 伤害占最大HP的25%
                statusPotency: 0f,
                baseChance: 1.0f
            );

            // 验证
            Assert.IsTrue(applied);

            // 期望减速：10 + 20 * 0.25 = 15%减速
            float expectedSpeed = 5.0f * (1f - 0.15f);
            Assert.AreEqual(expectedSpeed, target.MovementSpeed, 0.01f);

            // 2秒后状态结束
            statusSystem.Update(2.0f);
            Assert.IsFalse(statusSystem.HasStatus(StatusType.Chill));
            Assert.AreEqual(5.0f, target.MovementSpeed, 0.01f); // 速度恢复
        }

        [Test]
        public void StatusStacking_RefreshMax_KeepsHigherPotency()
        {
            // 准备
            var target = new MockCombatUnit(maxHealth: 1000);
            var statusSystem = new StatusSystem(target);

            // 第一次应用：低强度
            statusSystem.TryApplyStatus(
                StatusType.Ignite,
                sourceDamage: 300f,
                statusPotency: 0.2f,
                baseChance: 1.0f
            );

            // 第二次应用：高强度（应该替换）
            statusSystem.TryApplyStatus(
                StatusType.Ignite,
                sourceDamage: 500f,
                statusPotency: 0.8f,
                baseChance: 1.0f
            );

            // 验证
            var status = statusSystem.GetStatus(StatusType.Ignite) as IgniteStatus;
            Assert.IsNotNull(status);
            Assert.AreEqual(0.8f, status.Potency, 0.01f); // 保留高强度版本
        }

        [Test]
        public void StatusResistance_ReducesDuration()
        {
            // 准备
            var target = new MockCombatUnit(maxHealth: 1000);
            target.SetStatusResistance(StatusType.Ignite, 0.5f); // 50%状态抗性
            var statusSystem = new StatusSystem(target);

            // 执行
            bool applied = statusSystem.TryApplyStatus(
                StatusType.Ignite,
                sourceDamage: 500f,
                statusPotency: 0f,
                baseChance: 1.0f
            );

            // 验证
            Assert.IsTrue(applied);
            var status = statusSystem.GetStatus(StatusType.Ignite);

            // 基础持续时间4秒，50%抗性 => 2秒
            // 注意：实际实现中持续时间在Apply时计算
            Assert.IsTrue(status.RemainingTime <= 2.0f);
        }
    }
}
```

---

### 🏆 业界案例：Diablo状态系统深度分析

《暗黑破坏神》系列（特别是Diablo 3和Diablo 4）的状态系统设计对ARPG品类产生了深远影响。作为塔防+肉鸽混合玩法，我们可以从中吸取关键经验。

#### 🎯 Diablo状态系统的三大创新

1. **易伤状态（Vulnerable）的革命性设计**
   - **Diablo 4创新：** 将"易伤"从普通状态提升为**独立乘区**
   - **数学原理：** `最终伤害 = 基础伤害 × (1 + 易伤%)`，独立于其他增伤
   - **策略影响：** 易伤Build成为**必选项**而非可选项，引发平衡问题

   **我们的借鉴与调整：**
   - 保留易伤作为独立乘区，但**限制获取途径**
   - 设计"感电"状态为**团队共享易伤**，避免单人Build垄断

2. **控制递减机制（Diminishing Returns）**
   - **Diablo 3教训：** 无限控制导致Boss战无趣（无限冰法）
   - **解决方案：** 连续控制效果时间递减，最终免疫
   - **数学公式：** `第N次控制时长 = 基础时长 × 0.5^(N-1)`

   **我们的应用：**
   - 引入"韧性系统"（见第3部分）作为控制递减的视觉化表现
   - Boss拥有**控制抗性积累**，而非简单免疫

3. **状态协同的套装设计**
   - **Diablo 3成功：** 套装特效围绕状态构建（如塔拉夏的 meteor + hydra + blizzard）
   - **设计模式：** 状态A触发状态B，状态B强化状态C
   - **玩家体验：** 复杂的连锁反应带来深度满足感

   **我们的简化：**
   - 在肉鸽祝福中设计状态协同（如"冰冻敌人被击碎时爆炸"）
   - 塔防中设计塔的协同（冰塔冻结 → 火塔点燃 → 连锁爆炸）

#### 📊 Diablo vs 我们设计的对比分析

| 设计维度 | Diablo的实现 | 我们的调整（塔防+肉鸽） | 设计理由 |
| :--- | :--- | :--- | :--- |
| **易伤状态** | 独立乘区，后期必堆 | **限制性独立乘区**，稀有获取 | 防止易伤成为唯一最优解 |
| **控制递减** | 时间递减公式 | **韧性值系统**，视觉化表现 | 更直观的玩家反馈 |
| **状态叠加** | 多数不可叠加 | **分层设计**，点燃不叠加，流血可叠加 | 简化玩家认知，保持策略深度 |
| **状态触发** | 真随机+大量触发 | **PRD算法**+适度触发 | 保证体验稳定性，适合塔防节奏 |
| **Boss免疫** | 完全免疫控制 | **高韧性+短控**，不完全免疫 | 保留控制流的可行性 |

#### 💡 从Diablo吸取的核心教训

1. **易伤平衡的失败教训**
   - **Diablo 4问题：** 易伤成为伤害公式的**强制乘区**，非易伤Build弱30-50%
   - **我们的对策：** 感电状态提供易伤，但：
     - 持续时间短（2秒）
     - 触发要求高（需要雷电伤害）
     - 团队共享，鼓励协作

2. **控制多样性的成功经验**
   - **Diablo 3成功：** 不同职业有独特的控制方式（和尚致盲、巫医恐惧、法师冻结）
   - **我们的应用：** 不同伤害类型附带不同控制：
     - 冰霜：减速/冻结
     - 雷电：感电（易伤）
     - 物理：流血（移动惩罚）
     - 火焰：点燃（持续伤害）

3. **状态视觉反馈的演进**
   - **Diablo 2→4进化：** 从简单图标到全屏特效
   - **我们的设计：** 塔防需要清晰的视觉层级：
     - **第一层：** 伤害数字颜色（物理橙、火焰红、冰霜蓝）
     - **第二层：** 状态图标（头顶debuff标志）
     - **第三层：** 模型特效（燃烧、结冰、电击）

#### 🎮 实战案例：Diablo 3的"冰霜射线"Build分析

**Build核心机制：**
1. **主要技能：** 冰霜射线（Ray of Frost）
2. **状态触发：** 100%几率冰冻（短暂）
3. **套装加成：** 对冻结敌人伤害+1000%
4. **传奇特效：** 冰霜射线穿透冻结敌人

**设计亮点：**
- **状态与伤害循环：** 冰冻 → 增伤 → 更多冰冻
- **风险回报平衡：** 需要站桩输出，但伤害爆炸
- **视觉辨识度：** 蓝色光束 vs 冰冻敌人，清晰反馈

**对我们的启示：**
- **塔防应用：** 冰霜塔冻结敌人 → 其他塔获得对冻结伤害加成
- **肉鸽祝福：** "冰冻敌人被击碎时连锁冻结附近敌人"
- **玩家Build：** 专注冰霜伤害，堆叠冻结几率和持续时间

#### ⚠️ Diablo的失败教训：状态数值膨胀

**问题：** Diablo 3后期，状态伤害数字达到**万亿级别**，状态持续时间几乎无限

**我们的防范措施：**
1. **严格的数值上限：** 状态强度最多+100%，持续时间最多+100%
2. **状态抗性系统：** 怪物随波次增加状态抗性
3. **快照机制限制：** 状态伤害基于**施加时的快照**，不随实时面板增长

#### 🔄 适配塔防肉鸽的改造方案

将Diablo的状态系统**简化并强化**，适配塔防+肉鸽：

1. **状态触发简化：**
   - 每个伤害类型绑定1-2个主要状态
   - 触发条件明确（暴击、技能特定、固定几率）
   - PRD算法保证稳定性

2. **状态协同塔防化：**
   - **冰塔 + 火塔：** 冰冻敌人被火伤击中时爆炸
   - **电塔 + 物塔：** 感电增加物理伤害
   - **混沌塔 + 所有塔：** 降低敌人状态抗性

3. **肉鸽祝福集成：**
   - **常见祝福：** 状态持续时间+20%
   - **稀有祝福：** 状态可叠加额外1层
   - **传奇祝福：** 状态触发时连锁到附近敌人

**最终目标：** 保留Diablo状态系统的深度和爽快感，但通过塔防的**空间策略**和肉鸽的**随机构建**创造独特体验。

---

---

## 3. 硬直与韧性 (Stagger & Poise)

为了让打击感“拳拳到肉”，引入韧性系统 (类似于《黑暗之魂》或《只狼》的简化版)。

### 3.1 韧性值 (Poise)
*   所有单位（玩家和怪物）都有一个隐藏的 **Poise HP**。
*   每次受到攻击，扣除等于 `Damage * Impact_Factor` 的韧性值。
*   韧性值会随时间快速恢复 (若 2秒 内未受击)。

### 3.2 硬直状态 (Staggered)
*   当 **Poise <= 0** 时，单位进入 **硬直状态**。
*   **效果:**
    1.  打断当前正在施放的技能/攻击前摇。
    2.  播放受击动画 (Hit Reaction)。
    3.  Poise 瞬间回满，但短时间内 (3秒) 获得的 Poise Damage 减半 (防止无限晕锁)。

### 3.3 击退与击飞 (Knockback & Launch)
*   只有在目标 **Poise 被清零的这一击**，且攻击带有 `Force` 属性时，才会触发击退/击飞。
*   *设计目的:* 防止小技能无限推着 Boss 走。

---

### 🧠 理论原理：打击感数学模型与韧性恢复曲线

本部分从**数学原理**和**设计哲学**两个维度解析韧性系统的设计，解释为什么需要引入韧性值而非简单的硬直几率。

#### 🔢 数学基础：韧性公式与恢复曲线

1. **韧性伤害公式设计：**
   - **线性公式：** `韧性伤害 = 基础伤害 × 冲击系数 × (1 + 硬直强度%)`
     - *优点：* 直观易懂，计算简单
     - *缺点：* 冲击系数需要精细调整
   - **对数公式：** `韧性伤害 = 基础伤害 × log(1 + 冲击系数 × 伤害)`
     - *优点：* 防止大额伤害直接清空韧性，保护高韧性单位
     - *缺点：* 玩家感知不直观

   **我们的选择：** 采用线性公式，通过**冲击系数**控制不同攻击的硬直能力

2. **韧性恢复的数学模型：**
   - **线性恢复：** `每秒恢复 = 最大韧性 × 恢复率`
     - *公式：* `Poise(t) = min(MaxPoise, CurrentPoise + RecoveryRate × Δt)`
     - *特点：* 恢复速度恒定，容易预测
   - **指数恢复：** `恢复速度随当前韧性降低而减慢`
     - *公式：* `Poise(t) = MaxPoise × (1 - e^(-RecoveryRate × Δt)) + CurrentPoise × e^(-RecoveryRate × Δt)`
     - *特点：* 刚被击破后恢复慢，接近满值时恢复快，更有节奏感

   **我们的选择：** 采用线性恢复，但配合**恢复延迟机制**（2秒未受击才开始恢复）

3. **硬直时间计算：**
   - **基础公式：** `硬直时间 = 基础时间 + 超量韧性伤害 × 时间系数`
   - **保护机制：** 最小硬直时间 0.3秒，最大硬直时间 1.5秒
   - **连锁保护：** 刚结束硬直的单位获得3秒内韧性伤害减半，防止无限晕锁

#### 🏗️ 设计哲学：打击感的节奏控制

引用自《设计哲学文档》的**节奏控制理论**：

1. **打击感的时间窗口理论：**
   - **前摇 (Wind-up):** 攻击准备阶段，玩家预判
   - **命中帧 (Hit Frame):** 伤害判定时刻，需视觉/听觉反馈
   - **后摇 (Follow-through):** 攻击收尾阶段，可被硬直打断
   - **硬直窗口 (Stagger Window):** 受击反应时间，约0.3-1.5秒

   **关键洞察：** 硬直时间应**略长于**攻击后摇时间，才能让玩家感受到"打断"的快感。

2. **韧性系统的策略价值：**
   - **资源管理：** 韧性是隐藏的"第二血量"，玩家需控制攻击频率
   - **风险回报：** 高伤害技能通常冲击系数高，但冷却长
   - **Boss设计：** Boss拥有高韧性和快速恢复，防止被无限控制

3. **塔防适配的简化设计：**
   - **玩家单位：** 完整的韧性系统，强调动作性
   - **塔单位：** 简化为"建筑韧性"，受击有几率进入维修状态
   - **怪物单位：** 根据类型差异化配置（小怪低韧性，精英中韧性，Boss高韧性）

#### 🔄 击退物理的数学模拟

1. **击退力计算：**
   - **基础公式：** `击退力 = 攻击力 × 冲击系数 × (1 + 击退强度%)`
   - **方向向量：** 从攻击者位置指向被击者位置的单位向量
   - **质量影响：** `实际位移 = 击退力 / 目标质量`

2. **速度衰减曲线：**
   - **线性衰减：** `速度(t) = 初始速度 × max(0, 1 - 衰减率 × t)`
   - **指数衰减：** `速度(t) = 初始速度 × e^(-衰减率 × t)`
   - **我们的选择：** 指数衰减更符合物理直觉，视觉上更自然

3. **碰撞检测与地形互动：**
   - **撞墙判定：** 如果击退路径上有障碍物，提前结束击退
   - **撞墙伤害：** `撞墙伤害 = 剩余动能 × 撞墙系数`
   - **地形利用：** 玩家可将敌人击退到陷阱或悬崖，创造额外战术

#### 🎯 韧性系统的平衡考量

1. **数值调优参考表：**
   | 单位类型 | 最大韧性 | 恢复率/秒 | 硬直时间 | 设计意图 |
   | :--- | :--- | :--- | :--- | :--- |
   | **玩家英雄** | 100 | 20% | 0.5-1.0s | 强调操作，可被连击但能快速恢复 |
   | **小怪** | 30 | 10% | 0.3-0.5s | 易于控制，形成割草感 |
   | **精英怪** | 200 | 15% | 0.5-1.0s | 需要集中火力才能硬直 |
   | **Boss** | 500 | 25% | 1.0-1.5s | 难以控制，硬直即输出窗口 |

2. **冲击系数分级：**
   - **轻攻击：** 0.1-0.3（快速连击，积少成多）
   - **重攻击：** 0.5-0.8（高冲击，易造成硬直）
   - **控制技能：** 1.0-2.0（专为破韧设计）
   - **范围攻击：** 0.05-0.1（每个目标独立计算）

3. **硬直连锁保护公式：**
   ```数学公式
   实际韧性伤害 = 原始韧性伤害 × (1 - 保护系数 × min(1, 上次硬直结束时间/3))
   ```
   - **保护系数：** 0.5（即最多减半）
   - **时间衰减：** 硬直结束后随时间减弱保护效果

---

### 🛠️ 实践举例：韧性配置表与计算模板

本部分提供可直接使用的**韧性系统配置表**和**数值计算工具**。

#### 📊 韧性系统配置表（JSON格式）

```json
{
  "system": "poise_system",
  "version": "1.0",
  "last_updated": "2025-12-02",
  "poise_settings": {
    "global": {
      "max_poise_cap": 1000,
      "recovery_delay": 2.0,
      "recovery_rate_per_second": 0.2,
      "stagger_protection_duration": 3.0,
      "stagger_protection_multiplier": 0.5,
      "min_stagger_duration": 0.3,
      "max_stagger_duration": 1.5,
      "knockback_force_multiplier": 1.0,
      "knockback_decay_rate": 2.0
    },
    "unit_templates": {
      "player": {
        "display_name": "玩家英雄",
        "base_max_poise": 100,
        "poise_recovery_rate": 0.2,
        "mass": 1.0,
        "stagger_animation": "Anim_Stagger_Player",
        "knockback_resistance": 0.5,
        "description": "平衡型韧性配置，适合动作战斗"
      },
      "minion": {
        "display_name": "小怪",
        "base_max_poise": 30,
        "poise_recovery_rate": 0.1,
        "mass": 0.5,
        "stagger_animation": "Anim_Stagger_Minion",
        "knockback_resistance": 0.2,
        "description": "低韧性，易被控制"
      },
      "elite": {
        "display_name": "精英怪",
        "base_max_poise": 200,
        "poise_recovery_rate": 0.15,
        "mass": 2.0,
        "stagger_animation": "Anim_Stagger_Elite",
        "knockback_resistance": 0.7,
        "description": "中等韧性，需要集火"
      },
      "boss": {
        "display_name": "Boss",
        "base_max_poise": 500,
        "poise_recovery_rate": 0.25,
        "mass": 5.0,
        "stagger_animation": "Anim_Stagger_Boss",
        "knockback_resistance": 0.9,
        "description": "高韧性，硬直即输出窗口"
      }
    },
    "impact_factors": {
      "light_attack": {
        "display_name": "轻攻击",
        "base_factor": 0.2,
        "range": [0.1, 0.3],
        "description": "快速连击，积少成多"
      },
      "heavy_attack": {
        "display_name": "重攻击",
        "base_factor": 0.65,
        "range": [0.5, 0.8],
        "description": "高冲击，易造成硬直"
      },
      "cc_skill": {
        "display_name": "控制技能",
        "base_factor": 1.5,
        "range": [1.0, 2.0],
        "description": "专为破韧设计"
      },
      "aoe_attack": {
        "display_name": "范围攻击",
        "base_factor": 0.075,
        "range": [0.05, 0.1],
        "description": "每个目标独立计算"
      }
    }
  },
  "stagger_effects": {
    "staggered": {
      "display_name": "硬直",
      "interrupts_skills": true,
      "plays_hit_reaction": true,
      "movement_disabled": true,
      "attack_disabled": true,
      "skill_disabled": true,
      "visual_effects": {
        "particle": "FX_Stagger_Spark",
        "screen_shake": "LightShake",
        "sound": "SFX_Stagger_Hit"
      }
    },
    "knockback": {
      "display_name": "击退",
      "requires_force_attribute": true,
      "requires_poise_broken": true,
      "force_formula": "damage * impact_factor * force_multiplier / target_mass",
      "duration_formula": "min(1.0, force / 100)",
      "visual_effects": {
        "particle_trail": "FX_Knockback_Trail",
        "sound_loop": "SFX_Knockback_Loop"
      }
    }
  }
}
```

#### 📈 韧性计算Excel模板

**Excel表格结构示例：**

| A | B | C | D | E | F | G |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **参数** | **数值** | **公式** | **说明** | **玩家攻击小怪** | **玩家攻击精英** | **玩家攻击Boss** |
| 攻击力 | 500 | | 单次攻击伤害 | 500 | 500 | 500 |
| 冲击系数 | 0.5 | | 攻击的硬直能力 | 0.5 | 0.5 | 0.5 |
| 目标最大韧性 | - | | 敌人韧性上限 | 30 | 200 | 500 |
| 目标当前韧性 | - | | 战斗开始时 | 30 | 200 | 500 |
| 目标质量 | - | | 影响击退距离 | 0.5 | 2.0 | 5.0 |
| **计算列** | **结果** | **公式** | **说明** | **数值** | **数值** | **数值** |
| 韧性伤害 | 250 | `攻击力×冲击系数` | 本次攻击造成的韧性伤害 | 250 | 250 | 250 |
| 攻击后韧性 | -20 | `当前韧性-韧性伤害` | 扣除后韧性值 | -20 | -50 | 250 |
| 是否硬直 | 是 | `攻击后韧性≤0` | 触发硬直条件 | 是 | 是 | 否 |
| 硬直时间 | 0.8秒 | `基础0.3+超量×0.002` | 超量=绝对值(负韧性) | 0.8 | 0.4 | - |
| 击退力 | 500 | `攻击力×冲击系数×1.0` | 基础击退力 | 500 | 500 | 500 |
| 实际位移 | 1000 | `击退力/质量` | 单位距离 | 1000 | 250 | 100 |
| 恢复开始时间 | 2.0秒后 | | 恢复延迟 | 2.0 | 2.0 | - |
| 完全恢复时间 | 12.0秒 | `韧性差/恢复率` | 从负值恢复到满 | 12.0 | 16.7 | - |

**关键计算单元格公式（Excel格式）：**
- **韧性伤害：** `=$B$2*$B$3`
- **攻击后韧性：** `=MAX(-$B$4*2, $B$5-$B$9)` // 最低为最大韧性的-200%
- **是否硬直：** `=IF($B$10<=0, "是", "否")`
- **硬直时间：** `=IF($B$11="是", MIN($B$14, MAX($B$13, 0.3 + ABS($B$10)*0.002)), 0)`
- **击退力：** `=IF($B$11="是", $B$2*$B$3*$B$16, 0)`
- **实际位移：** `=$B$17/$B$6`

#### 🎮 Unity实现：韧性系统核心代码

```csharp
// PoiseSystem.cs - 韧性系统核心
namespace Vampirefall.Combat
{
    public class PoiseSystem
    {
        private float _currentPoise;
        private float _maxPoise;
        private float _recoveryRate; // 每秒恢复百分比
        private float _recoveryDelayTimer;
        private const float RECOVERY_DELAY = 2.0f;
        private float _staggerProtectionTimer;
        private const float STAGGER_PROTECTION_DURATION = 3.0f;
        private const float STAGGER_PROTECTION_MULTIPLIER = 0.5f;

        private CombatUnit _owner;
        private bool _isStaggered;
        private float _staggerTimer;

        public PoiseSystem(CombatUnit owner, float maxPoise, float recoveryRate)
        {
            _owner = owner;
            _maxPoise = maxPoise;
            _currentPoise = maxPoise;
            _recoveryRate = recoveryRate;
        }

        public void Update(float deltaTime)
        {
            // 更新硬直计时
            if (_isStaggered)
            {
                _staggerTimer -= deltaTime;
                if (_staggerTimer <= 0)
                {
                    EndStagger();
                }
                return; // 硬直期间不恢复韧性
            }

            // 更新恢复延迟计时
            if (_recoveryDelayTimer > 0)
            {
                _recoveryDelayTimer -= deltaTime;
            }
            else
            {
                // 开始恢复韧性
                _currentPoise = Mathf.Min(_maxPoise, _currentPoise + _maxPoise * _recoveryRate * deltaTime);
            }

            // 更新硬直保护计时
            if (_staggerProtectionTimer > 0)
            {
                _staggerProtectionTimer -= deltaTime;
            }
        }

        public bool TakePoiseDamage(float damage, float impactFactor, bool hasForce = false)
        {
            // 计算实际韧性伤害
            float poiseDamage = damage * impactFactor;

            // 应用硬直保护
            if (_staggerProtectionTimer > 0)
            {
                float protectionFactor = Mathf.Lerp(STAGGER_PROTECTION_MULTIPLIER, 1.0f,
                    _staggerProtectionTimer / STAGGER_PROTECTION_DURATION);
                poiseDamage *= protectionFactor;
            }

            // 扣除韧性
            _currentPoise -= poiseDamage;
            _recoveryDelayTimer = RECOVERY_DELAY; // 重置恢复延迟

            // 检查是否进入硬直
            if (_currentPoise <= 0 && !_isStaggered)
            {
                StartStagger(poiseDamage, hasForce);
                return true;
            }

            return false;
        }

        private void StartStagger(float poiseDamage, bool hasForce)
        {
            _isStaggered = true;

            // 计算硬直时间（基础0.3秒 + 超量伤害×0.002）
            float overkill = Mathf.Abs(_currentPoise);
            _staggerTimer = Mathf.Clamp(0.3f + overkill * 0.002f, 0.3f, 1.5f);

            // 韧性重置为最大值的一半（防止立即再次硬直）
            _currentPoise = _maxPoise * 0.5f;

            // 启动硬直保护
            _staggerProtectionTimer = STAGGER_PROTECTION_DURATION;

            // 触发硬直效果
            _owner.OnStaggered(_staggerTimer);

            // 检查击退
            if (hasForce)
            {
                ApplyKnockback(poiseDamage);
            }
        }

        private void EndStagger()
        {
            _isStaggered = false;
            _owner.OnStaggerEnd();
        }

        private void ApplyKnockback(float poiseDamage)
        {
            // 计算击退力
            float force = poiseDamage * _owner.KnockbackMultiplier;
            Vector3 direction = (_owner.transform.position - _owner.LastAttackerPosition).normalized;

            // 应用击退
            _owner.ApplyForce(direction * force);
        }

        // 属性访问器
        public float CurrentPoise => _currentPoise;
        public float MaxPoise => _maxPoise;
        public float PoisePercentage => _currentPoise / _maxPoise;
        public bool IsStaggered => _isStaggered;
        public float StaggerTimer => _staggerTimer;
    }
}

// CombatUnit.cs - 战斗单位基类扩展
namespace Vampirefall.Combat
{
    public partial class CombatUnit
    {
        [SerializeField] private float _baseMaxPoise = 100f;
        [SerializeField] private float _poiseRecoveryRate = 0.2f;
        [SerializeField] private float _mass = 1.0f;
        [SerializeField] private float _knockbackResistance = 0.5f;

        private PoiseSystem _poiseSystem;
        private Vector3 _lastAttackerPosition;

        protected virtual void Awake()
        {
            _poiseSystem = new PoiseSystem(this, _baseMaxPoise, _poiseRecoveryRate);
        }

        protected virtual void Update()
        {
            _poiseSystem.Update(Time.deltaTime);
        }

        public virtual void TakeDamage(float damage, DamageType damageType, string source, Vector3 attackerPosition, float impactFactor = 0.5f, bool hasForce = false)
        {
            // 记录攻击者位置（用于击退方向）
            _lastAttackerPosition = attackerPosition;

            // 计算韧性伤害
            bool staggered = _poiseSystem.TakePoiseDamage(damage, impactFactor, hasForce);

            // 计算实际伤害（受护甲/抗性减免）
            float finalDamage = DamageCalculator.CalculateFinalDamage(
                new DamageRequest
                {
                    DamageType = damageType,
                    BaseDamage = damage,
                    // ... 其他参数
                }
            );

            // 应用伤害
            CurrentHealth -= finalDamage;

            // 如果触发硬直，播放额外反馈
            if (staggered)
            {
                PlayStaggerFeedback();
            }
        }

        public virtual void OnStaggered(float duration)
        {
            // 打断当前技能
            InterruptCurrentAction();

            // 播放受击动画
            _animator.Play("Stagger", 0, 0f);

            // 屏幕震动
            CameraController.Instance.Shake(0.2f, 0.1f);

            // 音效
            AudioManager.PlaySFX("SFX_Stagger_Hit");

            // 粒子特效
            ParticleSystemPool.Get("FX_Stagger_Spark").PlayAt(transform.position);
        }

        public virtual void OnStaggerEnd()
        {
            // 恢复控制
            _animator.Play("Idle", 0, 0f);
        }

        public virtual void ApplyForce(Vector3 force)
        {
            // 应用击退力（考虑质量）
            Vector3 acceleration = force / _mass;

            // 如果单位有刚体，使用物理引擎
            if (_rigidbody != null)
            {
                _rigidbody.AddForce(acceleration, ForceMode.Impulse);
            }
            else
            {
                // 手动移动
                StartCoroutine(KnockbackRoutine(acceleration));
            }
        }

        private IEnumerator KnockbackRoutine(Vector3 acceleration)
        {
            float timer = Mathf.Min(1.0f, acceleration.magnitude / 100f);
            Vector3 velocity = acceleration;

            while (timer > 0)
            {
                // 指数衰减
                velocity *= Mathf.Exp(-2.0f * Time.deltaTime);
                transform.position += velocity * Time.deltaTime;

                timer -= Time.deltaTime;
                yield return null;
            }
        }
    }
}
```

#### 📁 韧性系统文件结构

```
Assets/
├── _Project/
│   ├── Core/
│   │   └── Combat/
│   │       ├── PoiseSystem.cs
│   │       ├── CombatUnit.cs (扩展)
│   │       └── DamageCalculator.cs (扩展)
│   ├── Data/
│   │   └── Configs/
│   │       ├── PoiseSettings.json
│   │       ├── ImpactFactors.json
│   │       └── UnitPoiseTemplates.json
│   └── Resources/
│       └── Combat/
│           ├── VFX/
│           │   ├── Stagger/
│           │   │   ├── FX_Stagger_Spark.prefab
│           │   │   └── FX_Knockback_Trail.prefab
│           └── Audio/
│               ├── SFX/
│               │   ├── SFX_Stagger_Hit.wav
│               │   └── SFX_Knockback_Loop.wav
```

#### 🧪 测试用例示例

```csharp
// PoiseSystemTests.cs - 单元测试
using NUnit.Framework;

namespace Vampirefall.Tests.Combat
{
    [TestFixture]
    public class PoiseSystemTests
    {
        [Test]
        public void TakePoiseDamage_ReducesCurrentPoise()
        {
            // 准备
            var unit = new MockCombatUnit();
            var poiseSystem = new PoiseSystem(unit, maxPoise: 100f, recoveryRate: 0.2f);

            // 执行
            bool staggered = poiseSystem.TakePoiseDamage(damage: 50f, impactFactor: 0.5f);

            // 验证
            Assert.AreEqual(75f, poiseSystem.CurrentPoise, 0.01f); // 100 - 50*0.5 = 75
            Assert.IsFalse(staggered); // 未触发硬直
        }

        [Test]
        public void TakePoiseDamage_WhenPoiseZero_TriggersStagger()
        {
            // 准备
            var unit = new MockCombatUnit();
            var poiseSystem = new PoiseSystem(unit, maxPoise: 30f, recoveryRate: 0.1f);

            // 执行
            bool staggered = poiseSystem.TakePoiseDamage(damage: 100f, impactFactor: 0.5f);

            // 验证
            Assert.IsTrue(staggered);
            Assert.IsTrue(poiseSystem.IsStaggered);
            Assert.IsTrue(poiseSystem.StaggerTimer > 0);
        }

        [Test]
        public void StaggerProtection_ReducesSubsequentPoiseDamage()
        {
            // 准备
            var unit = new MockCombatUnit();
            var poiseSystem = new PoiseSystem(unit, maxPoise: 50f, recoveryRate: 0.2f);

            // 第一次攻击触发硬直
            poiseSystem.TakePoiseDamage(damage: 200f, impactFactor: 0.5f);

            // 硬直结束后，韧性重置为25（50的一半）
            poiseSystem.ForceEndStagger(); // 测试辅助方法

            // 第二次攻击（在保护期内）
            bool staggered = poiseSystem.TakePoiseDamage(damage: 60f, impactFactor: 0.5f);

            // 验证：保护期伤害减半
            // 预期伤害：60 * 0.5 * 0.5 = 15
            // 当前韧性：25 - 15 = 10，未触发硬直
            Assert.IsFalse(staggered);
            Assert.AreEqual(10f, poiseSystem.CurrentPoise, 0.01f);
        }

        [Test]
        public void PoiseRecovery_StartsAfterDelay()
        {
            // 准备
            var unit = new MockCombatUnit();
            var poiseSystem = new PoiseSystem(unit, maxPoise: 100f, recoveryRate: 0.2f);

            // 造成伤害，触发恢复延迟
            poiseSystem.TakePoiseDamage(damage: 40f, impactFactor: 0.5f);
            float initialPoise = poiseSystem.CurrentPoise; // 100 - 20 = 80

            // 模拟2秒内更新（不恢复）
            for (int i = 0; i < 2; i++)
            {
                poiseSystem.Update(1.0f);
                Assert.AreEqual(initialPoise, poiseSystem.CurrentPoise, 0.01f);
            }

            // 2秒后开始恢复
            poiseSystem.Update(0.1f);
            Assert.Greater(poiseSystem.CurrentPoise, initialPoise);
        }

        [Test]
        public void Knockback_OnlyWhenPoiseBrokenAndHasForce()
        {
            // 准备
            var unit = new MockCombatUnit();
            unit.SetKnockbackMultiplier(1.0f);
            var poiseSystem = new PoiseSystem(unit, maxPoise: 30f, recoveryRate: 0.1f);

            // 不带Force的攻击，即使破韧也不击退
            bool staggered1 = poiseSystem.TakePoiseDamage(damage: 100f, impactFactor: 0.5f, hasForce: false);
            Assert.IsTrue(staggered1);
            Assert.IsFalse(unit.WasKnockedBack);

            // 重置测试
            unit.ResetTestState();
            poiseSystem = new PoiseSystem(unit, maxPoise: 30f, recoveryRate: 0.1f);

            // 带Force的攻击，破韧时击退
            bool staggered2 = poiseSystem.TakePoiseDamage(damage: 100f, impactFactor: 0.5f, hasForce: true);
            Assert.IsTrue(staggered2);
            Assert.IsTrue(unit.WasKnockedBack);
        }
    }
}
```

---

### 🏆 业界案例：黑暗之魂韧性系统深度分析

《黑暗之魂》系列（Dark Souls）被认为是**动作角色扮演游戏（ARPG）中韧性系统设计的教科书**。其设计哲学对现代动作游戏的打击感产生了深远影响。

#### 🎯 黑暗之魂韧性系统的三大支柱

1. **权重等级（Equip Load）与韧性联动**
   - **核心机制：** 装备重量决定角色**移动速度**和**翻滚无敌帧**，同时影响韧性值
   - **三级划分：**
     - **< 25% 负重：** 快速翻滚，无敌帧最长，但韧性最低
     - **25%-50% 负重：** 中速翻滚，无敌帧中等，韧性中等
     - **> 50% 负重：** 慢速翻滚，无敌帧最短，但韧性最高
   - **设计启示：** 韧性不是独立属性，而是**风险回报体系**的一部分

2. **韧性点数（Poise Points）的隐藏计算**
   - **隐藏属性：** 玩家看不到具体韧性值，只能通过装备描述感受"轻重"
   - **装备叠加：** 头盔+胸甲+护手+腿甲，每个部位提供固定韧性点数
   - **阈值设计：** 存在关键阈值（如 31、61、91），突破阈值质变
   - **设计启示：** **隐藏的数值深度**让玩家通过试错学习，增加探索感

3. **硬直恢复的动作窗口**
   - **受击动画分级：**
     - **小硬直：** 轻微后仰，可快速反击
     - **中硬直：** 明显后退，动作中断
     - **大硬直：** 被击倒，长时间失去控制
   - **恢复机制：** 硬直结束后有短暂**无敌帧**，防止连续受击
   - **设计启示：** 硬直不仅是惩罚，也是**节奏调节器**

#### 📊 黑暗之魂 vs 我们设计的对比分析

| 设计维度 | 黑暗之魂的实现 | 我们的调整（塔防+肉鸽） | 设计理由 |
| :--- | :--- | :--- | :--- |
| **韧性可见性** | **完全隐藏**，玩家试错 | **部分可见**（UI显示韧性条） | 降低学习成本，适合快节奏肉鸽 |
| **负重联动** | **强绑定**装备重量 | **解耦**，独立韧性属性 | 简化Build构建，聚焦塔防策略 |
| **硬直分级** | **3级硬直**（小/中/大） | **2级硬直**（普通/击倒） | 降低认知负担，保持动作清晰 |
| **恢复机制** | **固定恢复速度** | **延迟后指数恢复** | 创造"喘息窗口"，鼓励节奏控制 |
| **Boss韧性** | **极高但可破** | **高但快速恢复** | 保证Boss战挑战性，防止无限控制 |

#### 💡 从黑暗之魂吸取的核心教训

1. **韧性作为节奏控制工具**
   - **黑暗之魂成功之处：** 通过韧性控制战斗节奏，强迫玩家"回合制"思考
   - **我们的应用：** 在塔防中，韧性决定玩家能否"打断"怪物技能，创造输出窗口

2. **隐藏深度的教学方式**
   - **黑暗之魂成功之处：** 不教数值，让玩家通过死亡学习
   - **我们的调整：** 显示基础数值，但保留**高级机制**（如连锁保护）让玩家探索

3. **装备选择的战略意义**
   - **黑暗之魂成功之处：** 每件装备的韧性/重量比不同，创造Build多样性
   - **我们的应用：** 在肉鸽祝福中设计"韧性相关"选择，如：
     - **轻甲祝福：** 韧性-30%，移速+20%
     - **重甲祝福：** 韧性+50%，攻速-10%

#### 🎮 实战案例：黑暗之魂的"巨剑"Build分析

**Build核心思路：**
1. **装备选择：** 哈维尔套装（高韧性）+ 巨剑（高冲击力）
2. **韧性目标：** 堆到61点（关键阈值），免疫小怪轻攻击硬直
3. **战斗风格：** 放弃翻滚，硬吃伤害换输出
4. **风险点：** 负重>50%，翻滚慢，怕连续控制

**对我们的启示：**
- **阈值设计的重要性：** 31/61/91这些关键阈值创造了明确的Build目标
- **风险回报的平衡：** 高韧性Build放弃机动性，换取站桩输出能力
- **视觉反馈的清晰度：** 巨剑的沉重攻击有明显前摇，敌人能预判并躲避

#### ⚠️ 黑暗之魂的失败教训：韧性崩坏（Poise Break）

**问题：** 在《黑暗之魂3》中，韧性系统被大幅削弱，导致**重甲无用论**

**崩坏原因：**
1. **韧性只在攻击时生效：** 静止时韧性无效，重甲失去意义
2. **恢复速度过慢：** 一次破韧后，长时间失去韧性
3. **PVP失衡：** 轻武器无限连击，重武器无法反击

**我们的防范措施：**
1. **全时生效：** 韧性始终有效，无论攻击还是静止
2. **快速恢复：** 破韧后快速恢复基线韧性（50%最大值）
3. **连锁保护：** 防止无限硬直，保证反击机会

#### 🔄 适配塔防肉鸽的改造方案

将黑暗之魂的韧性系统**简化并强化**，适配塔防+肉鸽：

1. **可视化改造：**
   - **韧性条UI：** 显示在血条下方，玩家清晰看到破韧进度
   - **冲击反馈：** 攻击命中时显示"韧性伤害"数字
   - **破韧特效：** 韧性归零时全屏震动+慢动作特效

2. **肉鸽集成：**
   - **韧性祝福：**
     - **常见：** 最大韧性+20%
     - **稀有：** 韧性恢复速度+50%
     - **传奇：** 破韧时触发范围爆炸
   - **冲击祝福：**
     - **常见：** 冲击系数+0.1
     - **稀有：** 攻击有几率直接减少目标50%韧性
     - **传奇：** 破韧效果连锁到附近敌人

3. **塔防协同：**
   - **破韧塔：** 专门设计高冲击系数的塔，配合玩家输出
   - **控制链：** 玩家破韧 → 塔集火 → 快速击杀
   - **战术选择：** 集中破韧击杀精英，或分散控制小怪群

**最终目标：** 保留黑暗之魂韧性系统的**策略深度**和**节奏控制**，但通过可视化UI和肉鸽祝福降低学习成本，让玩家在**单局游戏内**体验到Build成型的乐趣。

---

## 4. 仇恨系统 (Aggro System)

由于有塔的存在，怪物的仇恨逻辑比纯 ARPG 复杂。

**优先级列表 (从高到低):**
1.  **嘲讽 (Taunt):** 被嘲讽技能命中，强制攻击施法者 3秒。
2.  **路径阻挡 (Body Block):** 如果无法移动到目标点，攻击阻挡路径的物体（通常是塔或墙）。
3.  **距离 + 伤害权重:** `Score = Damage_Dealt_Last_5s * 2 + (1 / Distance_Squared) * 10`。
    *   这意味着：虽然远程塔在打它，但如果玩家贴脸砍它，它会转头打玩家。

---

### 🧠 4.1 理论原理：塔防与ARPG的混合仇恨逻辑

仇恨系统是**塔防与ARPG混合玩法**的核心设计挑战。在纯ARPG中，怪物通常优先攻击玩家；在纯塔防中，怪物沿着固定路径前进，只攻击阻挡物。Vampirefall需要在这两种逻辑之间找到平衡点。

#### 📊 仇恨公式的数学推导

现有公式 `Score = Damage_Dealt_Last_5s * 2 + (1 / Distance_Squared) * 10` 包含两个关键维度：

1. **时间维度（伤害权重）**：
   ```
   伤害分数 = Σ(最近5秒内受到的伤害) × 2
   ```
   - **滑动窗口机制**：使用5秒窗口而非实时伤害，避免目标频繁切换
   - **指数衰减**：更近的伤害权重更高，可采用 `Weight(t) = e^(-λt)` 模型
   - **伤害类型权重**：不同伤害类型可设置不同仇恨系数（如嘲讽技能×10）

2. **空间维度（距离权重）**：
   ```
   距离分数 = (1 / 距离²) × 10
   ```
   - **平方反比定律**：距离越近，权重呈指数增长
   - **临界距离**：当距离 < 2米时，分数急剧上升，模拟"贴脸威胁"
   - **归一化处理**：防止距离过近导致分母为0，使用 `1/(距离² + ε)`

#### 🎯 优先级系统的设计哲学

**核心原则**：**"玩家是矛，塔是盾"**（Player is the spear, towers are the shield）

1. **嘲讽（最高优先级）**：
   - **强制转移**：无视所有其他权重，强制攻击施法者
   - **持续时间**：3秒是认知心理学上的"短期记忆窗口"
   - **冷却机制**：防止无限嘲讽，需要策略性使用

2. **路径阻挡（次高优先级）**：
   - **寻路中断**：当A*寻路算法无法找到路径时触发
   - **攻击最近阻挡物**：选择距离最近的塔或墙体
   - **破坏优先级**：优先攻击血量最低的阻挡物

3. **动态权重计算（默认逻辑）**：
   - **混合决策**：伤害权重（理性） + 距离权重（感性）
   - **阈值切换**：当玩家分数 > 塔分数 × 1.5时切换目标
   - **滞后效应**：防止在阈值附近频繁切换

#### ⚙️ 时间衰减与记忆机制

仇恨系统需要模拟**怪物的短期记忆**：

```
记忆衰减模型：
当前仇恨值 = Σ[伤害_i × e^(-λ × (当前时间 - 伤害时间_i))]
```

参数设计：
- **衰减常数 λ**：控制记忆持续时间（λ=0.2对应5秒半衰期）
- **伤害类型系数**：近战伤害×1.5，远程伤害×1.0，DoT伤害×0.7
- **最大记忆数量**：防止无限存储，只保留最近10次伤害记录

#### 🔄 状态机与行为树整合

仇恨系统需要与AI状态机深度整合：

```
仇恨状态机：
[空闲] → [检测伤害] → [计算仇恨] → [选择目标]
      ↑                    ↓
      └──[目标丢失] ← [攻击目标]
```

关键状态：
- **警戒状态**：检测到伤害，开始计算仇恨
- **决策状态**：比较所有潜在目标的仇恨分数
- **攻击状态**：锁定目标，执行攻击行为
- **重置状态**：目标死亡或超出范围，重置仇恨

#### 📈 数值平衡考量

1. **权重系数调整**：
   ```
   伤害权重系数：2.0（可配置）
   距离权重系数：10.0（可配置）
   嘲讽倍数：100.0（确保绝对优先级）
   ```

2. **距离曲线设计**：
   - **近战范围**（0-3米）：分数急剧上升，鼓励近战互动
   - **中程范围**（3-10米）：线性增长，平衡塔与玩家
   - **远程范围**（10+米）：分数趋近于0，塔成为主要目标

3. **难度调节**：
   - **简单难度**：降低距离权重，让玩家更容易拉怪
   - **困难难度**：增加伤害权重，怪物更"记仇"
   - **无尽模式**：随时间增加权重系数，提高挑战性

#### 🎮 玩家体验设计

仇恨系统直接影响**战斗节奏**和**策略深度**：

1. **可预测性**：玩家需要能预测怪物的行为
   - 显示仇恨条或目标指示器
   - 提供嘲讽技能的视觉反馈

2. **策略选择**：
   - **坦克Build**：高嘲讽频率，保护塔和队友
   - **刺客Build**：高爆发伤害，快速建立仇恨后撤离
   - **控场Build**：利用路径阻挡，引导怪物走向陷阱

3. **学习曲线**：
   - **新手期**：简化仇恨逻辑，怪物优先攻击最近目标
   - **熟练期**：引入完整权重系统
   - **专家期**：添加仇恨转移、仇恨共享等高级机制

#### 🔗 与其他系统的协同

仇恨系统不是孤立的，需要与多个系统协同工作：

1. **与韧性系统协同**：
   - 被硬直打击会**重置部分仇恨**
   - 高韧性怪物更难被嘲讽
   - 破韧瞬间仇恨清零，需要重新建立

2. **与状态系统协同**：
   - **冰冻状态**：仇恨计算暂停
   - **混乱状态**：随机攻击目标
   - **恐惧状态**：逃离当前仇恨目标

3. **与连击系统协同**：
   - 高连击数增加**仇恨生成**
   - 连击中断会**仇恨衰减**
   - 连击奖励可能包含仇恨相关效果

#### 📊 性能优化策略

实时计算所有怪物的仇恨分数可能成为性能瓶颈：

1. **计算频率优化**：
   - **按需计算**：只在状态改变时计算
   - **分层更新**：近处怪物每帧更新，远处怪物每秒更新
   - **批次处理**：使用Job System并行计算

2. **数据结构优化**：
   ```csharp
   // 环形缓冲区存储伤害记录
   struct DamageRecord {
       float damage;
       float timestamp;
       int sourceId;
   }

   // 空间分区加速距离查询
   SpatialHashGrid<Monster> proximityGrid;
   ```

3. **近似算法**：
   - 距离计算使用**曼哈顿距离**而非欧几里得距离
   - 伤害衰减使用**查表法**而非实时指数计算
   - 分数比较使用**锦标赛排序**而非完全排序

---

### 🛠️ 4.2 实践举例：AI权重配置与计算模板

#### 📋 4.2.1 JSON配置表设计

仇恨系统的所有参数都通过JSON配置表驱动，支持热更新和平衡调整：

```json
// Config/AggroConfig.json
{
  "version": "1.0",
  "description": "仇恨系统核心参数配置",

  "globalParameters": {
    "updateInterval": 0.5,
    "maxTargetsToEvaluate": 8,
    "hysteresisThreshold": 1.5,
    "defaultMemoryDuration": 5.0
  },

  "priorityWeights": {
    "taunt": {
      "baseMultiplier": 100.0,
      "duration": 3.0,
      "cooldown": 10.0,
      "visualEffect": "VFX_Taunt_Aura"
    },

    "bodyBlock": {
      "pathfindingTimeout": 2.0,
      "searchRadius": 5.0,
      "preferLowHealth": true,
      "healthThreshold": 0.3
    }
  },

  "damageWeights": {
    "timeWindow": 5.0,
    "decayLambda": 0.2,
    "maxRecords": 10,

    "damageTypeMultipliers": {
      "melee": 1.5,
      "ranged": 1.0,
      "area": 0.8,
      "dot": 0.7,
      "tauntSkill": 10.0,
      "environmental": 0.5
    },

    "sourceTypeMultipliers": {
      "player": 1.0,
      "tower": 0.8,
      "minion": 0.6,
      "trap": 0.4
    }
  },

  "distanceWeights": {
    "baseMultiplier": 10.0,
    "epsilon": 0.1,

    "rangeCurves": {
      "meleeRange": {
        "min": 0.0,
        "max": 3.0,
        "curveType": "exponential",
        "exponent": 2.0
      },
      "midRange": {
        "min": 3.0,
        "max": 10.0,
        "curveType": "linear",
        "slope": 0.5
      },
      "longRange": {
        "min": 10.0,
        "max": 50.0,
        "curveType": "logarithmic",
        "base": 10.0
      }
    }
  },

  "monsterTypeOverrides": {
    "boss": {
      "damageWeightMultiplier": 0.5,
      "tauntResistance": 0.7,
      "memoryDuration": 8.0
    },
    "swarmer": {
      "damageWeightMultiplier": 2.0,
      "distanceWeightMultiplier": 0.5,
      "maxRecords": 5
    },
    "ranged": {
      "preferRangedTargets": true,
      "distanceWeightMultiplier": 1.5
    }
  },

  "difficultySettings": {
    "easy": {
      "distanceWeightMultiplier": 0.7,
      "hysteresisThreshold": 2.0,
      "tauntDurationMultiplier": 1.2
    },
    "normal": {
      "distanceWeightMultiplier": 1.0,
      "hysteresisThreshold": 1.5
    },
    "hard": {
      "damageWeightMultiplier": 1.3,
      "distanceWeightMultiplier": 1.2,
      "tauntResistanceMultiplier": 1.5
    },
    "endless": {
      "scalingPerWave": 0.02,
      "maxScaling": 2.0
    }
  }
}
```

#### 📊 4.2.2 Excel计算模板

使用Excel进行仇恨分数的手动计算和平衡测试：

**仇恨计算表 (`Aggro_Calculator.xlsx`)**：

| 参数 | 值 | 说明 |
|------|-----|------|
| **时间窗口** | 5.0秒 | 伤害记忆持续时间 |
| **衰减常数λ** | 0.2 | 指数衰减速率 |
| **伤害权重** | 2.0 | 伤害分数乘数 |
| **距离权重** | 10.0 | 距离分数乘数 |
| **滞后阈值** | 1.5 | 切换目标所需倍数 |

**伤害记录表**：

| 时间戳 | 伤害值 | 伤害类型 | 来源 | 衰减权重 | 有效伤害 |
|--------|--------|----------|------|----------|----------|
| 0.0s | 100 | 近战 | 玩家 | 1.000 | 100.0 |
| 1.5s | 50 | 远程 | 塔 | 0.741 | 37.1 |
| 3.0s | 200 | 近战 | 玩家 | 0.549 | 109.9 |
| 4.5s | 75 | 区域 | 陷阱 | 0.407 | 30.5 |

**计算公式**：
```
衰减权重 = EXP(-λ × 时间差)
有效伤害 = 原始伤害 × 伤害类型系数 × 衰减权重
伤害分数 = Σ(有效伤害) × 伤害权重
```

**距离分数计算**：

| 距离(m) | 原始分数 | 曲线调整 | 最终分数 |
|---------|----------|----------|----------|
| 0.5 | 40.00 | ×2.25 | 90.00 |
| 2.0 | 2.50 | ×1.00 | 2.50 |
| 5.0 | 0.40 | ×0.75 | 0.30 |
| 10.0 | 0.10 | ×0.50 | 0.05 |

**总仇恨分数**：
```
总分数 = 伤害分数 + 距离分数
玩家分数 = 247.0 × 2.0 + 90.0 = 584.0
塔分数 = 37.1 × 2.0 + 0.3 = 74.5
```

**决策逻辑**：
```
if (玩家分数 > 塔分数 × 滞后阈值)
    目标 = 玩家
else
    目标 = 塔
```

#### 💻 4.2.3 Unity C#实现代码

**核心仇恨管理器**：

```csharp
// Scripts/AI/AggroManager.cs
using System.Collections.Generic;
using UnityEngine;

[System.Serializable]
public struct DamageRecord
{
    public float damage;
    public float timestamp;
    public int sourceId;
    public DamageType damageType;
    public SourceType sourceType;
}

public class AggroManager : MonoBehaviour
{
    [Header("配置引用")]
    [SerializeField] private AggroConfig config;

    [Header("运行时数据")]
    private Dictionary<int, List<DamageRecord>> damageHistory = new();
    private Dictionary<int, float> currentAggro = new();
    private int currentTargetId = -1;
    private float lastUpdateTime = 0f;

    // 环形缓冲区，避免GC分配
    private DamageRecord[] recordBuffer = new DamageRecord[10];
    private int bufferIndex = 0;

    void Update()
    {
        // 按配置间隔更新，减少计算频率
        if (Time.time - lastUpdateTime < config.globalParameters.updateInterval)
            return;

        lastUpdateTime = Time.time;
        UpdateAggroForAllMonsters();
    }

    public void RegisterDamage(int monsterId, DamageRecord record)
    {
        if (!damageHistory.ContainsKey(monsterId))
            damageHistory[monsterId] = new List<DamageRecord>();

        // 使用环形缓冲区避免List扩容
        var history = damageHistory[monsterId];
        if (history.Count >= config.damageWeights.maxRecords)
        {
            // 移除最旧的记录
            history.RemoveAt(0);
        }

        history.Add(record);

        // 立即更新该怪物的仇恨（按需计算）
        UpdateAggroForMonster(monsterId);
    }

    private void UpdateAggroForMonster(int monsterId)
    {
        if (!damageHistory.ContainsKey(monsterId))
            return;

        var history = damageHistory[monsterId];
        float currentTime = Time.time;

        // 1. 计算伤害分数（带时间衰减）
        float damageScore = 0f;
        for (int i = history.Count - 1; i >= 0; i--)
        {
            var record = history[i];
            float timeDiff = currentTime - record.timestamp;

            // 超出时间窗口的记录移除
            if (timeDiff > config.damageWeights.timeWindow)
            {
                history.RemoveAt(i);
                continue;
            }

            // 指数衰减权重
            float decayWeight = Mathf.Exp(-config.damageWeights.decayLambda * timeDiff);

            // 伤害类型权重
            float typeMultiplier = config.damageWeights.damageTypeMultipliers
                .GetValueOrDefault(record.damageType, 1.0f);

            // 来源类型权重
            float sourceMultiplier = config.damageWeights.sourceTypeMultipliers
                .GetValueOrDefault(record.sourceType, 1.0f);

            damageScore += record.damage * decayWeight * typeMultiplier * sourceMultiplier;
        }

        damageScore *= config.damageWeights.baseMultiplier;

        // 2. 计算距离分数
        float distanceScore = CalculateDistanceScore(monsterId);

        // 3. 检查特殊优先级（嘲讽、路径阻挡）
        float priorityScore = CheckPriorityConditions(monsterId);

        // 4. 应用怪物类型覆盖
        MonsterType monsterType = GetMonsterType(monsterId);
        var overrideConfig = config.monsterTypeOverrides.GetValueOrDefault(monsterType);
        if (overrideConfig != null)
        {
            damageScore *= overrideConfig.damageWeightMultiplier;
            distanceScore *= overrideConfig.distanceWeightMultiplier;
        }

        // 5. 应用难度设置
        var difficultyConfig = config.difficultySettings.GetValueOrDefault(GameManager.Instance.Difficulty);
        if (difficultyConfig != null)
        {
            damageScore *= difficultyConfig.damageWeightMultiplier;
            distanceScore *= difficultyConfig.distanceWeightMultiplier;
        }

        // 6. 无尽模式动态缩放
        if (GameManager.Instance.IsEndlessMode)
        {
            float waveScale = 1.0f + config.difficultySettings.endless.scalingPerWave
                * GameManager.Instance.CurrentWave;
            waveScale = Mathf.Min(waveScale, config.difficultySettings.endless.maxScaling);
            damageScore *= waveScale;
        }

        float totalScore = damageScore + distanceScore + priorityScore;
        currentAggro[monsterId] = totalScore;

        // 7. 决策：选择目标
        SelectTarget(monsterId, totalScore);
    }

    private float CalculateDistanceScore(int monsterId)
    {
        Vector3 monsterPos = GetMonsterPosition(monsterId);
        float minDistanceScore = float.MaxValue;
        int bestTargetId = -1;

        // 只评估有限数量的潜在目标（性能优化）
        var potentialTargets = GetPotentialTargets(monsterId, config.globalParameters.maxTargetsToEvaluate);

        foreach (var target in potentialTargets)
        {
            float distance = Vector3.Distance(monsterPos, target.position);

            // 防止除零
            distance = Mathf.Max(distance, 0.1f);

            // 基础距离分数
            float baseScore = 1.0f / (distance * distance + config.distanceWeights.epsilon);
            baseScore *= config.distanceWeights.baseMultiplier;

            // 应用距离曲线
            float curveMultiplier = GetDistanceCurveMultiplier(distance);
            float finalScore = baseScore * curveMultiplier;

            if (finalScore < minDistanceScore)
            {
                minDistanceScore = finalScore;
                bestTargetId = target.id;
            }
        }

        return minDistanceScore;
    }

    private float GetDistanceCurveMultiplier(float distance)
    {
        foreach (var curve in config.distanceWeights.rangeCurves)
        {
            if (distance >= curve.Value.min && distance <= curve.Value.max)
            {
                switch (curve.Value.curveType)
                {
                    case "exponential":
                        return Mathf.Pow(distance / curve.Value.max, curve.Value.exponent);
                    case "linear":
                        return 1.0f - (distance - curve.Value.min) /
                            (curve.Value.max - curve.Value.min) * (1.0f - curve.Value.slope);
                    case "logarithmic":
                        return Mathf.Log(1.0f + distance, curve.Value.baseValue);
                    default:
                        return 1.0f;
                }
            }
        }
        return 1.0f;
    }

    private void SelectTarget(int monsterId, float currentScore)
    {
        // 获取当前目标分数
        float currentTargetScore = currentTargetId >= 0 ?
            currentAggro.GetValueOrDefault(currentTargetId, 0f) : 0f;

        // 滞后阈值：需要显著超过当前目标才切换
        float switchThreshold = currentTargetScore * config.globalParameters.hysteresisThreshold;

        if (currentScore > switchThreshold)
        {
            // 切换目标
            int previousTarget = currentTargetId;
            currentTargetId = monsterId;

            // 触发事件
            EventManager.Instance.TriggerEvent(new AggroTargetChangedEvent
            {
                monsterId = monsterId,
                previousTargetId = previousTarget,
                newTargetId = currentTargetId
            });
        }
    }

    // 获取当前仇恨目标（供AI系统查询）
    public Transform GetCurrentTarget(int monsterId)
    {
        if (currentTargetId < 0)
            return null;

        return GetTargetTransform(currentTargetId);
    }

    // 清空指定怪物的仇恨记录
    public void ClearAggro(int monsterId)
    {
        if (damageHistory.ContainsKey(monsterId))
            damageHistory[monsterId].Clear();

        currentAggro.Remove(monsterId);

        if (currentTargetId == monsterId)
            currentTargetId = -1;
    }

    // 应用嘲讽效果
    public void ApplyTaunt(int monsterId, int taunterId, float duration)
    {
        // 强制设置目标
        currentTargetId = taunterId;

        // 添加临时的高优先级分数
        float tauntScore = config.priorityWeights.taunt.baseMultiplier * 1000f;
        currentAggro[monsterId] = tauntScore;

        // 设置定时器，持续时间后恢复
        StartCoroutine(RemoveTauntAfterDelay(monsterId, duration));
    }
}
```

**单元测试代码**：

```csharp
// Tests/EditMode/AggroManagerTests.cs
using NUnit.Framework;
using UnityEngine;
using UnityEngine.TestTools;

public class AggroManagerTests
{
    private AggroManager aggroManager;
    private TestAggroConfig config;

    [SetUp]
    public void SetUp()
    {
        // 创建测试配置
        config = ScriptableObject.CreateInstance<TestAggroConfig>();
        config.globalParameters = new GlobalParameters { updateInterval = 0.1f };
        config.damageWeights = new DamageWeights {
            timeWindow = 5f,
            decayLambda = 0.2f,
            baseMultiplier = 2f
        };

        // 创建管理器
        var go = new GameObject("AggroManager");
        aggroManager = go.AddComponent<AggroManager>();
        aggroManager.SetConfigForTesting(config);
    }

    [Test]
    public void TestDamageDecayOverTime()
    {
        // 记录一次伤害
        var record = new DamageRecord {
            damage = 100f,
            timestamp = 0f,
            damageType = DamageType.Melee,
            sourceType = SourceType.Player
        };

        aggroManager.RegisterDamage(1, record);

        // 立即检查：应该有权重1.0
        float score1 = aggroManager.GetAggroScoreForTesting(1);
        Assert.AreEqual(200f, score1, 0.1f); // 100 × 2.0

        // 模拟时间流逝（2.5秒后）
        aggroManager.SimulateTimePassing(2.5f);
        float score2 = aggroManager.GetAggroScoreForTesting(1);
        float expected = 100f * Mathf.Exp(-0.2f * 2.5f) * 2f;
        Assert.AreEqual(expected, score2, 0.1f);

        // 5秒后应该衰减到接近0
        aggroManager.SimulateTimePassing(5f);
        float score3 = aggroManager.GetAggroScoreForTesting(1);
        Assert.Less(score3, 1f);
    }

    [Test]
    public void TestTauntPriority()
    {
        // 玩家造成一些伤害
        var playerRecord = new DamageRecord {
            damage = 50f,
            timestamp = 0f,
            sourceType = SourceType.Player
        };

        // 塔造成更多伤害
        var towerRecord = new DamageRecord {
            damage = 200f,
            timestamp = 0f,
            sourceType = SourceType.Tower
        };

        aggroManager.RegisterDamage(1, playerRecord);
        aggroManager.RegisterDamage(1, towerRecord);

        // 正常情况下应该选择塔（伤害更高）
        int target1 = aggroManager.GetCurrentTargetForTesting(1);
        Assert.AreEqual(SourceType.Tower, GetSourceType(target1));

        // 应用嘲讽
        aggroManager.ApplyTaunt(1, 999, 3f); // 玩家ID 999

        // 现在应该选择玩家（嘲讽优先级最高）
        int target2 = aggroManager.GetCurrentTargetForTesting(1);
        Assert.AreEqual(SourceType.Player, GetSourceType(target2));
    }

    [Test]
    public void TestHysteresisThreshold()
    {
        // 设置滞后阈值为1.5
        config.globalParameters.hysteresisThreshold = 1.5f;

        // 当前目标分数为100
        aggroManager.SetCurrentTargetScoreForTesting(100f);

        // 新分数120（< 100×1.5=150），不应该切换
        bool shouldSwitch1 = aggroManager.ShouldSwitchTargetForTesting(120f);
        Assert.IsFalse(shouldSwitch1);

        // 新分数160（> 150），应该切换
        bool shouldSwitch2 = aggroManager.ShouldSwitchTargetForTesting(160f);
        Assert.IsTrue(shouldSwitch2);
    }

    [Test]
    public void TestMonsterTypeOverrides()
    {
        // 测试Boss类型：伤害权重减半
        config.monsterTypeOverrides = new Dictionary<MonsterType, MonsterOverride> {
            { MonsterType.Boss, new MonsterOverride { damageWeightMultiplier = 0.5f } }
        };

        var record = new DamageRecord { damage = 100f, timestamp = 0f };
        aggroManager.RegisterDamage(1, record);
        aggroManager.SetMonsterTypeForTesting(1, MonsterType.Boss);

        // Boss应该只得到一半的伤害分数
        float score = aggroManager.GetAggroScoreForTesting(1);
        Assert.AreEqual(100f, score); // 100 × 0.5 × 2.0 = 100
    }

    [TearDown]
    public void TearDown()
    {
        Object.DestroyImmediate(aggroManager.gameObject);
    }
}
```

**性能分析工具**：

```csharp
// Scripts/Debug/AggroProfiler.cs
using System.Diagnostics;
using UnityEngine;

public class AggroProfiler : MonoBehaviour
{
    private struct ProfileData
    {
        public int monsterCount;
        public float updateTimeMs;
        public float avgRecordsPerMonster;
        public int targetSwitches;
    }

    private Queue<ProfileData> history = new Queue<ProfileData>();
    private Stopwatch stopwatch = new Stopwatch();
    private int maxHistorySize = 100;

    void OnEnable()
    {
        EventManager.Instance.AddListener<AggroTargetChangedEvent>(OnTargetChanged);
    }

    void OnDisable()
    {
        EventManager.Instance.RemoveListener<AggroTargetChangedEvent>(OnTargetChanged);
    }

    public void StartProfiling()
    {
        stopwatch.Start();
    }

    public ProfileData EndProfiling(int monsterCount, AggroManager manager)
    {
        stopwatch.Stop();

        var data = new ProfileData
        {
            monsterCount = monsterCount,
            updateTimeMs = stopwatch.ElapsedMilliseconds,
            avgRecordsPerMonster = manager.GetAverageRecordsPerMonster(),
            targetSwitches = 0 // 从事件计数器中获取
        };

        history.Enqueue(data);
        if (history.Count > maxHistorySize)
            history.Dequeue();

        stopwatch.Reset();
        return data;
    }

    private void OnTargetChanged(AggroTargetChangedEvent evt)
    {
        // 统计目标切换次数
        // ...
    }

    public void DrawProfilerGUI()
    {
        GUILayout.BeginVertical("Box");
        GUILayout.Label("仇恨系统性能分析", EditorStyles.boldLabel);

        if (history.Count > 0)
        {
            var latest = history.Peek();
            GUILayout.Label($"怪物数量: {latest.monsterCount}");
            GUILayout.Label($"更新时间: {latest.updateTimeMs:F2}ms");
            GUILayout.Label($"平均记录数: {latest.avgRecordsPerMonster:F1}");
            GUILayout.Label($"目标切换: {latest.targetSwitches}/帧");

            // 绘制历史图表
            DrawHistoryChart();
        }

        GUILayout.EndVertical();
    }
}
```

#### 📱 4.2.4 可视化调试工具

在Unity编辑器中创建可视化调试界面，帮助设计和平衡仇恨系统：

```csharp
// Editor/AggroDebugWindow.cs
using UnityEditor;
using UnityEngine;

public class AggroDebugWindow : EditorWindow
{
    [MenuItem("Tools/Vampirefall/仇恨系统调试")]
    public static void ShowWindow()
    {
        GetWindow<AggroDebugWindow>("仇恨调试");
    }

    private AggroManager aggroManager;
    private Vector2 scrollPos;
    private bool autoRefresh = true;
    private float refreshInterval = 1f;
    private float lastRefreshTime;

    void OnGUI()
    {
        if (aggroManager == null)
            aggroManager = FindObjectOfType<AggroManager>();

        if (aggroManager == null)
        {
            EditorGUILayout.HelpBox("场景中未找到AggroManager", MessageType.Warning);
            return;
        }

        // 控制面板
        EditorGUILayout.BeginHorizontal();
        autoRefresh = EditorGUILayout.Toggle("自动刷新", autoRefresh);
        if (autoRefresh)
        {
            refreshInterval = EditorGUILayout.Slider("刷新间隔", refreshInterval, 0.1f, 5f);
        }
        if (GUILayout.Button("手动刷新"))
        {
            RefreshData();
        }
        EditorGUILayout.EndHorizontal();

        // 自动刷新逻辑
        if (autoRefresh && Time.realtimeSinceStartup - lastRefreshTime > refreshInterval)
        {
            RefreshData();
            lastRefreshTime = Time.realtimeSinceStartup;
        }

        scrollPos = EditorGUILayout.BeginScrollView(scrollPos);

        // 全局统计
        EditorGUILayout.Space();
        EditorGUILayout.LabelField("全局统计", EditorStyles.boldLabel);
        EditorGUILayout.LabelField($"活跃怪物数: {aggroManager.GetActiveMonsterCount()}");
        EditorGUILayout.LabelField($"总伤害记录数: {aggroManager.GetTotalDamageRecords()}");
        EditorGUILayout.LabelField($"最近目标切换: {aggroManager.GetRecentTargetSwitches()}");

        // 怪物列表
        EditorGUILayout.Space();
        EditorGUILayout.LabelField("怪物仇恨详情", EditorStyles.boldLabel);

        var monsters = aggroManager.GetAllMonsters();
        foreach (var monster in monsters)
        {
            DrawMonsterSection(monster);
        }

        EditorGUILayout.EndScrollView();
    }

    private void DrawMonsterSection(Monster monster)
    {
        EditorGUILayout.BeginVertical("Box");

        // 怪物基本信息
        EditorGUILayout.LabelField($"ID: {monster.Id} - {monster.Name}", EditorStyles.boldLabel);
        EditorGUILayout.LabelField($"类型: {monster.Type}");
        EditorGUILayout.LabelField($"当前位置: {monster.Position}");

        // 仇恨分数
        var scores = aggroManager.GetAggroScores(monster.Id);
        EditorGUILayout.LabelField("仇恨分数:", EditorStyles.boldLabel);

        EditorGUI.indentLevel++;
        foreach (var score in scores)
        {
            EditorGUILayout.BeginHorizontal();
            EditorGUILayout.LabelField($"{score.targetName}:");
            EditorGUILayout.LabelField($"{score.score:F1}", GUILayout.Width(80));

            // 进度条可视化
            float maxScore = aggroManager.GetMaxScore(monster.Id);
            if (maxScore > 0)
            {
                float percent = score.score / maxScore;
                EditorGUI.ProgressBar(GUILayoutUtility.GetRect(100, 16), percent, "");
            }

            EditorGUILayout.EndHorizontal();
        }
        EditorGUI.indentLevel--;

        // 伤害历史
        var history = aggroManager.GetDamageHistory(monster.Id);
        if (history.Count > 0)
        {
            EditorGUILayout.LabelField("伤害历史:", EditorStyles.boldLabel);

            EditorGUI.indentLevel++;
            foreach (var record in history)
            {
                string timeAgo = (Time.time - record.timestamp).ToString("F1");
                EditorGUILayout.LabelField(
                    $"+{timeAgo}s: {record.damage:F0} ({record.damageType} from {record.sourceType})"
                );
            }
            EditorGUI.indentLevel--;
        }

        // 当前目标
        var target = aggroManager.GetCurrentTarget(monster.Id);
        if (target != null)
        {
            EditorGUILayout.LabelField($"当前目标: {target.name}",
                target.sourceType == SourceType.Player ?
                EditorStyles.whiteLabel : EditorStyles.label);
        }

        EditorGUILayout.EndVertical();
    }

    private void RefreshData()
    {
        // 强制更新所有怪物的仇恨计算
        aggroManager.ForceUpdateAll();
        Repaint();
    }

    void OnInspectorUpdate()
    {
        if (autoRefresh)
        {
            Repaint();
        }
    }
}
```

#### 🎮 4.2.5 玩家反馈系统

为了让玩家理解仇恨机制，需要提供清晰的视觉和听觉反馈：

```csharp
// Scripts/UI/AggroFeedbackSystem.cs
using UnityEngine;
using UnityEngine.UI;

public class AggroFeedbackSystem : MonoBehaviour
{
    [Header("UI元素")]
    [SerializeField] private Image aggroBar;
    [SerializeField] private Text aggroText;
    [SerializeField] private GameObject targetIndicator;
    [SerializeField] private Color lowAggroColor = Color.green;
    [SerializeField] private Color highAggroColor = Color.red;

    [Header("视觉特效")]
    [SerializeField] private ParticleSystem tauntEffect;
    [SerializeField] private ParticleSystem loseAggroEffect;

    [Header("音频")]
    [SerializeField] private AudioClip tauntSound;
    [SerializeField] private AudioClip aggroLostSound;

    private AggroManager aggroManager;
    private AudioSource audioSource;

    void Start()
    {
        aggroManager = FindObjectOfType<AggroManager>();
        audioSource = GetComponent<AudioSource>();

        // 订阅事件
        EventManager.Instance.AddListener<AggroTargetChangedEvent>(OnTargetChanged);
        EventManager.Instance.AddListener<PlayerTauntedEvent>(OnPlayerTaunted);
    }

    void Update()
    {
        UpdateAggroUI();
    }

    private void UpdateAggroUI()
    {
        if (aggroManager == null) return;

        // 获取玩家对最近怪物的仇恨值
        float aggroValue = aggroManager.GetPlayerAggroToNearestMonster();
        float maxAggro = aggroManager.GetMaxAggroForDisplay();

        // 更新进度条
        if (aggroBar != null)
        {
            aggroBar.fillAmount = aggroValue / maxAggro;
            aggroBar.color = Color.Lerp(lowAggroColor, highAggroColor, aggroValue / maxAggro);
        }

        // 更新文本
        if (aggroText != null)
        {
            aggroText.text = $"仇恨: {(aggroValue / maxAggro * 100):F0}%";
            aggroText.color = aggroValue > maxAggro * 0.7f ? Color.red : Color.white;
        }

        // 显示/隐藏目标指示器
        if (targetIndicator != null)
        {
            bool hasAggro = aggroValue > maxAggro * 0.3f;
            targetIndicator.SetActive(hasAggro);

            if (hasAggro)
            {
                // 指向最近仇恨怪物的方向
                Vector3 monsterPos = aggroManager.GetNearestAggroMonsterPosition();
                if (monsterPos != Vector3.zero)
                {
                    Vector3 direction = (monsterPos - transform.position).normalized;
                    targetIndicator.transform.rotation = Quaternion.LookRotation(direction);
                }
            }
        }
    }

    private void OnTargetChanged(AggroTargetChangedEvent evt)
    {
        // 如果玩家失去了怪物的仇恨
        if (evt.previousTargetId == Player.Instance.Id && evt.newTargetId != Player.Instance.Id)
        {
            PlayLoseAggroFeedback();
        }
        // 如果玩家获得了怪物的仇恨
        else if (evt.newTargetId == Player.Instance.Id)
        {
            PlayGainAggroFeedback();
        }
    }

    private void OnPlayerTaunted(PlayerTauntedEvent evt)
    {
        PlayTauntFeedback();
    }

    private void PlayTauntFeedback()
    {
        // 视觉特效
        if (tauntEffect != null)
        {
            tauntEffect.Play();
        }

        // 音效
        if (audioSource != null && tauntSound != null)
        {
            audioSource.PlayOneShot(tauntSound);
        }

        // UI震动
        StartCoroutine(ShakeUI(0.3f, 10f));
    }

    private void PlayGainAggroFeedback()
    {
        // 轻微的红屏效果
        StartCoroutine(FlashScreen(Color.red, 0.1f, 0.3f));

        // 心跳音效
        // ...
    }

    private void PlayLoseAggroFeedback()
    {
        // 视觉特效
        if (loseAggroEffect != null)
        {
            loseAggroEffect.Play();
        }

        // 音效
        if (audioSource != null && aggroLostSound != null)
        {
            audioSource.PlayOneShot(aggroLostSound);
        }
    }

    System.Collections.IEnumerator ShakeUI(float duration, float intensity)
    {
        Vector3 originalPos = aggroBar.transform.localPosition;
        float elapsed = 0f;

        while (elapsed < duration)
        {
            float x = Random.Range(-1f, 1f) * intensity;
            float y = Random.Range(-1f, 1f) * intensity;
            aggroBar.transform.localPosition = originalPos + new Vector3(x, y, 0);

            elapsed += Time.deltaTime;
            yield return null;
        }

        aggroBar.transform.localPosition = originalPos;
    }

    System.Collections.IEnumerator FlashScreen(Color color, float flashIn, float flashOut)
    {
        // 实现屏幕闪红效果
        // ...
        yield return null;
    }
}
```

---

### 🌍 4.3 业界案例分析：MMORPG仇恨管理系统

仇恨系统是**MMORPG团队战斗的核心机制**，经过20多年的演进，形成了成熟的体系。以下是三个代表性游戏的仇恨系统分析，以及它们对Vampirefall的启示。

#### 🎮 4.3.1 魔兽世界 (World of Warcraft) - 经典的"坦克-治疗-输出"铁三角

**核心机制**：
1. **威胁值 (Threat) 系统**：
   ```
   威胁值 = 伤害 × 威胁系数 + 治疗 × 治疗系数 + 特殊技能威胁
   ```
   - 坦克职业：威胁系数 3.0-5.0
   - 输出职业：威胁系数 1.0
   - 治疗职业：治疗威胁系数 0.5

2. **OT (Over Threat) 机制**：
   - 当非坦克玩家的威胁值 > 坦克威胁值 × 110%时，怪物切换目标
   - 10%的缓冲区间防止频繁切换

3. **仇恨重置技能**：
   - 盗贼的"消失"：清空自身威胁值
   - 猎人的"假死"：清空自身威胁值
   - 法师的"隐身"：大幅降低威胁值

**设计哲学**：
- **角色分工明确**：坦克负责建立仇恨，输出负责控制仇恨，治疗负责维持团队
- **可预测性**：玩家需要精确计算自己的威胁值
- **团队协作**：需要沟通和协调仇恨转移

**对Vampirefall的启示**：
1. **明确的角色定位**：虽然Vampirefall是单人游戏，但可以借鉴"玩家是矛，塔是盾"的分工
2. **缓冲区间设计**：使用滞后阈值防止目标频繁切换
3. **仇恨管理工具**：提供嘲讽、清仇等技能，增加策略深度

#### ⚔️ 4.3.2 最终幻想14 (Final Fantasy XIV) - 现代化的仇恨管理系统

**核心改进**：
1. **仇恨条可视化**：
   - 每个怪物头顶显示所有玩家的仇恨条
   - 颜色编码：红色（主仇恨）、橙色（高仇恨）、黄色（中等）、绿色（低）
   - 实时更新，玩家可以直观看到自己的仇恨位置

2. **仇恨共享机制**：
   - 某些技能可以"借用"队友的仇恨值
   - 骑士的"干预"：暂时承担队友的部分仇恨
   - 学者的"鼓舞"：转移部分仇恨给宠物

3. **Boss的特殊仇恨逻辑**：
   - **随机目标**：某些技能随机选择目标，无视仇恨
   - **距离优先级**：某些技能优先攻击最远/最近的玩家
   - **时间轴仇恨**：按照固定时间表切换目标

**设计哲学**：
- **透明度**：让仇恨机制对玩家完全可见
- **灵活性**：提供多种仇恨管理工具
- **剧本化战斗**：Boss战有精心设计的仇恨模式

**对Vampirefall的启示**：
1. **可视化反馈**：为玩家提供清晰的仇恨指示器
2. **多样化的仇恨逻辑**：不同怪物类型使用不同的仇恨算法
3. **Boss的特殊规则**：打破常规仇恨逻辑，增加战斗变化

#### 🛡️ 4.3.3 激战2 (Guild Wars 2) - 去坦克化的仇恨系统

**核心创新**：
1. **无专职坦克**：
   - 所有职业都可以通过装备和技能获得"韧性"属性来承受伤害
   - 仇恨基于**距离、伤害、技能使用频率**的动态计算

2. **主动防御机制**：
   - **闪避**：消耗耐力条进行无敌帧躲避
   - **格挡**：特定技能可以完全抵挡伤害
   - **反击**：成功防御后可以立即反击

3. **状况仇恨 (Condition Damage)**：
   - DoT伤害产生较低的仇恨
   - 控制技能（眩晕、击倒）产生中等仇恨
   - 爆发伤害产生高仇恨

**设计哲学**：
- **动作导向**：强调玩家操作而非数值计算
- **个人责任**：每个玩家都需要管理自己的生存
- **动态角色**：玩家可以在战斗中切换"坦克"和"输出"角色

**对Vampirefall的启示**：
1. **动作化仇恨**：距离和移动影响仇恨值
2. **个人生存技能**：玩家需要主动管理仇恨而非依赖固定角色
3. **动态角色切换**：玩家可以在"拉怪"和"输出"之间切换

#### 📊 4.3.4 仇恨系统演进趋势分析

| 时期 | 代表游戏 | 核心机制 | 优点 | 缺点 |
|------|----------|----------|------|------|
| **早期 (2000s)** | 魔兽世界 | 威胁值计算，OT机制 | 角色明确，团队协作 | 学习曲线陡峭，容错率低 |
| **中期 (2010s)** | 最终幻想14 | 可视化仇恨条，共享机制 | 透明度高，工具丰富 | 系统复杂，新手困惑 |
| **现代 (2020s)** | 激战2 | 动态计算，主动防御 | 动作性强，个人责任 | 缺乏明确的团队分工 |

#### 🎯 4.3.5 Vampirefall的仇恨系统定位

基于以上分析，Vampirefall的仇恨系统应该定位为：

1. **混合型设计**：
   - **塔防层面**：路径阻挡优先级最高，确保塔防核心玩法
   - **ARPG层面**：动态权重计算，鼓励玩家主动参与战斗
   - **Roguelike层面**：通过祝福改变仇恨逻辑，增加Build多样性

2. **渐进式复杂度**：
   ```
   新手期：简单距离优先
   ↓
   熟练期：伤害+距离权重
   ↓
   专家期：完整优先级系统+特殊规则
   ```

3. **可视化与反馈**：
   - 怪物头顶显示当前目标（玩家/塔）
   - 仇恨条显示玩家与塔的仇恨比例
   - 技能提供明确的仇恨效果说明

4. **Build多样性支持**：
   - **坦克Build**：高嘲讽频率，保护塔
   - **刺客Build**：高爆发后清仇，快速撤离
   - **控场Build**：利用路径阻挡引导怪物

#### 🔄 4.3.6 仇恨系统与其他机制的协同

借鉴MMORPG的经验，仇恨系统需要与多个机制深度协同：

1. **与资源系统协同**：
   - 管理仇恨消耗**耐力**或**专注**资源
   - 高仇恨状态下资源恢复速度降低
   - 清仇技能消耗大量资源

2. **与状态系统协同**：
   - **隐身状态**：大幅降低仇恨值
   - **嘲讽状态**：强制吸引仇恨
   - **恐惧状态**：逃离当前仇恨目标

3. **与连击系统协同**：
   - 高连击数增加**仇恨生成速度**
   - 连击中断会**仇恨衰减加速**
   - 连击奖励包含仇恨管理效果

4. **与肉鸽祝福协同**：
   - **祝福：仇恨吸引**：所有伤害的仇恨系数×2
   - **祝福：隐形刺客**：首次攻击不产生仇恨
   - **诅咒：仇恨磁铁**：仇恨系数×3，但承受伤害×1.5

#### 📈 4.3.7 数值平衡参考

参考MMORPG的数值设计，建议以下平衡参数：

1. **基础仇恨系数**：
   ```
   近战伤害：1.5
   远程伤害：1.0
   区域伤害：0.8
   DoT伤害：0.7
   嘲讽技能：10.0（强制）
   ```

2. **距离权重曲线**：
   ```
   0-3米：指数增长（系数 2.0-4.0）
   3-10米：线性下降（系数 1.0-0.5）
   10+米：对数衰减（系数 <0.5）
   ```

3. **时间衰减参数**：
   ```
   衰减常数 λ = 0.2（5秒半衰期）
   最大记忆时间：8秒
   最小记忆时间：1秒
   ```

4. **难度调节系数**：
   ```
   简单：距离权重×0.7，滞后阈值×2.0
   普通：基准值
   困难：伤害权重×1.3，滞后阈值×1.2
   无尽：每波增加2%权重系数
   ```

#### 🎮 4.3.8 玩家学习曲线设计

借鉴MMORPG的教学方法，设计渐进式学习：

1. **教程阶段**：
   - 只使用**距离优先**的简单逻辑
   - 显示基本的仇恨指示器
   - 教学关卡介绍嘲讽技能

2. **早期游戏**：
   - 引入**伤害权重**计算
   - 显示仇恨条和百分比
   - 教学路径阻挡机制

3. **中期游戏**：
   - 完整的优先级系统
   - 特殊怪物的仇恨规则
   - 仇恨管理技能解锁

4. **后期游戏**：
   - Boss的特殊仇恨逻辑
   - 高级仇恨转移技巧
   - 肉鸽祝福改变仇恨系统

#### 🔧 4.3.9 技术实现建议

基于业界最佳实践，建议以下技术实现：

1. **性能优化**：
   - **空间分区**：只计算附近目标的仇恨
   - **按需更新**：只在状态改变时重新计算
   - **批次处理**：使用Job System并行计算

2. **数据结构**：
   ```csharp
   // 环形缓冲区存储伤害记录
   struct DamageRecord {
       float damage;
       float timestamp;
       DamageType type;
   }

   // 空间哈希表加速距离查询
   SpatialHashGrid<Entity> proximityGrid;
   ```

3. **配置驱动**：
   - 所有参数通过JSON配置
   - 支持热更新和平衡调整
   - 不同怪物类型使用不同配置

4. **调试工具**：
   - 编辑器内可视化调试窗口
   - 实时性能分析
   - 仇恨历史记录回放

#### 📝 4.3.10 总结与建议

**核心设计原则**：
1. **透明性**：让玩家理解仇恨机制
2. **可预测性**：玩家能够预测怪物行为
3. **策略深度**：提供多种仇恨管理选项
4. **性能友好**：支持大规模战斗场景

**具体建议**：
1. 采用**混合优先级系统**：嘲讽 > 路径阻挡 > 动态权重
2. 实现**可视化反馈系统**：仇恨条、目标指示器、技能特效
3. 设计**渐进式复杂度**：随着游戏进程解锁更多机制
4. 提供**Build多样性支持**：不同玩法风格有不同的仇恨策略
5. 确保**性能可扩展性**：支持100+怪物的实时计算

**最终目标**：创造一个既**深度**又**直观**的仇恨系统，让玩家在塔防与ARPG的混合玩法中，能够通过**策略**和**操作**来管理战斗节奏，而不是被复杂的数值计算所困扰。

---

## 5. 连击与评分 (Combo & Style)
*   **Combo 阶段:**
    *   *10 Hit:* 移速 +5%。
    *   *50 Hit:* 攻速 +10%，资源获取率 +10%。
    *   *100 Hit (Max):* 全伤害 +20%，并在周围产生电弧。
*   **中断:** 3秒未造成伤害，或受到一次硬直打击 (Stagger)，连击清零。

---

### 🧠 5.1 理论原理：连击系统的心理学与游戏设计

连击系统是**动作游戏的核心驱动力**，它通过心理学上的**操作条件反射**和**即时反馈**来创造心流体验。Vampirefall的连击系统需要平衡**风险与奖励**，鼓励玩家采取积极的进攻策略。

#### 🎯 5.1.1 连击系统的设计目标

1. **鼓励进攻性玩法**：奖励持续攻击而非保守防御
2. **创造节奏感**：3秒时间窗口形成自然的攻击节奏
3. **提供可视化反馈**：连击数、特效、音效的即时反馈
4. **增加策略深度**：连击奖励影响战斗决策
5. **支持Build多样性**：不同连击风格对应不同奖励

#### ⏱️ 5.1.2 时间窗口的心理学基础

**3秒时间窗口**的设计基于认知心理学原理：

1. **工作记忆容量**：人类短期记忆能保持约3-5秒的信息
2. **注意力周期**：3秒是维持专注力的自然节奏
3. **操作反馈循环**：攻击→观察结果→调整策略的完整周期

**时间衰减模型**：
```
连击衰减 = 1 - (当前时间 - 上次命中时间) / 3.0
```
当衰减值 ≤ 0时，连击中断。

#### 📊 5.1.3 连击阶段的数学设计

现有阶段设计（10/50/100）体现了**对数增长曲线**：

| 阶段 | 连击数 | 奖励 | 设计意图 |
|------|--------|------|----------|
| **入门阶段** | 10 | 移速+5% | 低门槛，快速获得成就感 |
| **熟练阶段** | 50 | 攻速+10%，资源+10% | 中期目标，提升战斗效率 |
| **专家阶段** | 100 | 全伤害+20%，电弧特效 | 高难度目标，显著改变战斗 |

**阶段间隔设计**：
- 10→50：5倍增长，学习曲线平缓
- 50→100：2倍增长，专家门槛更高
- 最大100：防止无限增长，保持平衡

#### 🔄 5.1.4 连击奖励的乘区理论

连击奖励应该使用**独立乘区**，避免与其他增益稀释：

```
最终伤害 = 基础伤害 × (1 + 增伤总和) × (1 + 连击伤害加成)
```

**奖励乘区分配**：
1. **移速加成**：独立乘区，不影响其他属性
2. **攻速加成**：独立乘区，与装备攻速加法计算
3. **资源获取**：独立乘区，与基础资源获取乘法计算
4. **全伤害加成**：独立乘区，最高优先级

#### 🎮 5.1.5 中断机制的设计哲学

**双重中断条件**提供了风险与决策：

1. **时间中断（3秒）**：
   - **主动风险**：玩家需要持续攻击
   - **策略选择**：可以故意中断连击来调整位置
   - **节奏控制**：强制玩家保持攻击节奏

2. **硬直中断（受击）**：
   - **被动风险**：玩家需要避免被击中
   - **防御重要性**：鼓励闪避和防御技能
   - **惩罚机制**：高风险高回报的平衡

**中断惩罚梯度**：
- **轻度中断**：3秒未命中 → 连击清零，无额外惩罚
- **重度中断**：被硬直打击 → 连击清零 + 短暂debuff

#### ⚡ 5.1.6 电弧特效的视觉设计

**100连击的电弧特效**不仅是视觉奖励，也是战术工具：

1. **视觉效果**：
   - **范围指示**：显示电弧影响范围（半径5米）
   - **强度反馈**：电弧亮度随连击数增加
   - **节奏脉冲**：每0.5秒脉冲一次，与攻击节奏同步

2. **战术功能**：
   - **范围伤害**：对范围内敌人造成连锁伤害
   - **控制效果**：低概率触发感电状态
   - **资源生成**：每次脉冲生成少量资源

3. **性能优化**：
   - **LOD系统**：远处使用简化特效
   - **批次渲染**：多个电弧合并渲染
   - **动态生成**：只在有敌人时生成电弧

#### 🔗 5.1.7 与其他系统的协同设计

连击系统需要与多个游戏系统深度整合：

1. **与伤害系统协同**：
   - 不同伤害类型产生**不同连击权重**
   - 近战攻击：权重1.0
   - 远程攻击：权重0.8
   - 区域攻击：权重0.5（防止快速刷连击）
   - DoT伤害：权重0.3（每跳单独计算）

2. **与状态系统协同**：
   - **感电状态**：连击获取速度×1.5
   - **冰冻状态**：连击时间窗口延长至5秒
   - **混乱状态**：连击可能随机重置

3. **与仇恨系统协同**：
   - 高连击数增加**仇恨生成**
   - 连击中断会**仇恨衰减**
   - 连击奖励包含仇恨管理效果

4. **与肉鸽祝福协同**：
   - **祝福：连击大师**：时间窗口延长至5秒
   - **祝福：无限连击**：最大连击数提升至200
   - **诅咒：脆弱连击**：连击奖励×2，但受击伤害×1.5

#### 📈 5.1.8 数值平衡考量

**基础参数设计**：
```
时间窗口：3.0秒（可配置）
连击衰减：线性衰减（可改为指数衰减）
最大连击：100（可配置）
阶段阈值：[10, 50, 100]（可配置）
```

**奖励数值平衡**：
```
阶段1（10连击）：
- 移速加成：5%（独立乘区）
- 获取难度：低（新手友好）

阶段2（50连击）：
- 攻速加成：10%（与装备攻速加法）
- 资源获取：10%（独立乘区）
- 获取难度：中（需要一定技巧）

阶段3（100连击）：
- 全伤害加成：20%（独立乘区）
- 电弧伤害：50%武器伤害（每0.5秒）
- 获取难度：高（专家级挑战）
```

**难度调节系数**：
```
简单难度：
- 时间窗口：4.0秒
- 阶段阈值：[8, 40, 80]
- 奖励系数：1.2倍

普通难度：
- 基准值

困难难度：
- 时间窗口：2.5秒
- 受击惩罚：连击清零 + 2秒debuff
- 奖励系数：1.5倍（高风险高回报）

无尽模式：
- 每波时间窗口减少0.1秒（最低1.5秒）
- 每波奖励系数增加2%（最高2.0倍）
```

#### 🎛️ 5.1.9 玩家体验设计

连击系统直接影响**战斗爽快感**和**学习曲线**：

1. **即时反馈系统**：
   - **视觉反馈**：连击数字放大显示、颜色变化、屏幕震动
   - **听觉反馈**：连击音效、阶段升级音效、中断警告音
   - **触觉反馈**：手柄震动强度随连击数增加

2. **学习曲线设计**：
   - **教程阶段**：只介绍基础连击概念
   - **早期游戏**：重点练习10连击阶段
   - **中期游戏**：掌握50连击的节奏控制
   - **后期游戏**：挑战100连击并管理风险

3. **技能表达空间**：
   - **连击风格**：快速低伤害 vs 慢速高伤害
   - **风险偏好**：激进保持连击 vs 保守避免中断
   - **Build专精**：连击特化 vs 均衡发展

#### 🔧 5.1.10 技术实现架构

连击系统需要高效且灵活的技术实现：

1. **状态机设计**：
   ```
   [空闲] → [连击进行中] → [阶段升级] → [最大连击]
         ↓                    ↓
   [连击中断] ← [受击检测] ← [时间检测]
   ```

2. **事件驱动架构**：
   - **命中事件**：增加连击数，重置计时器
   - **受击事件**：检查是否硬直打击
   - **时间事件**：每帧检查时间窗口
   - **阶段事件**：达到阈值时触发奖励

3. **性能优化策略**：
   - **按需计算**：只在状态改变时重新计算
   - **缓存结果**：连击奖励效果缓存到下次改变
   - **批次处理**：多个敌人的连击计算合并处理

---

### 🛠️ 5.2 实践举例：评分配置表与计算模板

#### 📋 5.2.1 JSON配置表设计

连击系统的所有参数都通过JSON配置表驱动，支持热更新和平衡调整：

```json
// Config/ComboConfig.json
{
  "version": "1.0",
  "description": "连击系统核心参数配置",

  "globalParameters": {
    "timeWindow": 3.0,
    "decayType": "linear", // linear, exponential, quadratic
    "maxCombo": 100,
    "updateInterval": 0.1
  },

  "stages": [
    {
      "threshold": 10,
      "name": "入门连击",
      "rewards": {
        "moveSpeed": {
          "type": "additive",
          "value": 0.05,
          "description": "移动速度 +5%"
        }
      },
      "visualEffects": {
        "textColor": "#4CAF50", // 绿色
        "particleEffect": "VFX_Combo_Stage1",
        "soundEffect": "SFX_Combo_Stage1"
      }
    },
    {
      "threshold": 50,
      "name": "熟练连击",
      "rewards": {
        "attackSpeed": {
          "type": "additive",
          "value": 0.10,
          "description": "攻击速度 +10%"
        },
        "resourceGain": {
          "type": "multiplicative",
          "value": 0.10,
          "description": "资源获取率 +10%"
        }
      },
      "visualEffects": {
        "textColor": "#2196F3", // 蓝色
        "particleEffect": "VFX_Combo_Stage2",
        "soundEffect": "SFX_Combo_Stage2"
      }
    },
    {
      "threshold": 100,
      "name": "专家连击",
      "rewards": {
        "allDamage": {
          "type": "multiplicative",
          "value": 0.20,
          "description": "全伤害 +20%"
        },
        "arcEffect": {
          "type": "special",
          "radius": 5.0,
          "damagePerTick": 0.5, // 50%武器伤害
          "tickInterval": 0.5,
          "shockChance": 0.1, // 10%感电概率
          "description": "周围产生电弧，每0.5秒造成50%武器伤害"
        }
      },
      "visualEffects": {
        "textColor": "#FF9800", // 橙色
        "particleEffect": "VFX_Combo_Stage3",
        "soundEffect": "SFX_Combo_Stage3",
        "screenShake": {
          "intensity": 0.3,
          "duration": 0.5
        }
      }
    }
  ],

  "damageTypeWeights": {
    "melee": 1.0,
    "ranged": 0.8,
    "area": 0.5,
    "dot": 0.3,
    "environmental": 0.0
  },

  "interruptConditions": {
    "timeout": {
      "enabled": true,
      "duration": 3.0,
      "resetType": "clear" // clear, halve, keep_current
    },
    "staggerHit": {
      "enabled": true,
      "resetType": "clear",
      "debuffDuration": 0.0, // 0表示无debuff
      "debuffEffect": "none"
    },
    "death": {
      "enabled": true,
      "resetType": "clear"
    }
  },

  "difficultySettings": {
    "easy": {
      "timeWindow": 4.0,
      "stageThresholds": [8, 40, 80],
      "rewardMultiplier": 1.2,
      "interruptDebuffDuration": 0.0
    },
    "normal": {
      "timeWindow": 3.0,
      "stageThresholds": [10, 50, 100],
      "rewardMultiplier": 1.0,
      "interruptDebuffDuration": 0.0
    },
    "hard": {
      "timeWindow": 2.5,
      "stageThresholds": [12, 60, 120],
      "rewardMultiplier": 1.5,
      "interruptDebuffDuration": 2.0,
      "interruptDebuffEffect": "Combo_Reset_Debuff"
    },
    "endless": {
      "timeWindowReductionPerWave": 0.1,
      "minTimeWindow": 1.5,
      "rewardIncreasePerWave": 0.02,
      "maxRewardMultiplier": 2.0
    }
  },

  "visualFeedback": {
    "comboCounter": {
      "fontSizeBase": 24,
      "fontSizeMax": 48,
      "colorGradient": ["#FFFFFF", "#4CAF50", "#2196F3", "#FF9800"],
      "pulseOnHit": true,
      "pulseIntensity": 1.2
    },
    "timeIndicator": {
      "enabled": true,
      "type": "radial", // radial, bar, numeric
      "colorFull": "#4CAF50",
      "colorEmpty": "#F44336",
      "warningThreshold": 0.3 // 剩余30%时间时变色
    },
    "stageIndicators": {
      "enabled": true,
      "position": "top_right",
      "showNextStage": true
    }
  },

  "audioFeedback": {
    "hitSounds": {
      "basePitch": 1.0,
      "pitchIncreasePerCombo": 0.01,
      "maxPitch": 1.5,
      "volumeBase": 0.5,
      "volumeMax": 0.8
    },
    "stageSounds": {
      "stage1": "SFX_Combo_Stage1",
      "stage2": "SFX_Combo_Stage2",
      "stage3": "SFX_Combo_Stage3",
      "volume": 1.0
    },
    "resetSound": {
      "sound": "SFX_Combo_Reset",
      "volume": 0.7
    },
    "warningSound": {
      "enabled": true,
      "sound": "SFX_Combo_Warning",
      "triggerTime": 1.0, // 剩余1秒时播放
      "volume": 0.5
    }
  }
}
```

#### 📊 5.2.2 Excel计算模板

使用Excel进行连击系统的手动计算和平衡测试：

**连击计算表 (`Combo_Calculator.xlsx`)**：

| 参数 | 值 | 说明 |
|------|-----|------|
| **时间窗口** | 3.0秒 | 连击保持时间 |
| **衰减类型** | 线性 | 时间衰减方式 |
| **最大连击** | 100 | 连击上限 |
| **阶段阈值** | 10,50,100 | 奖励触发点 |

**伤害权重表**：

| 伤害类型 | 权重 | 说明 |
|----------|------|------|
| 近战伤害 | 1.0 | 标准权重 |
| 远程伤害 | 0.8 | 降低20%权重 |
| 区域伤害 | 0.5 | 降低50%权重，防止刷连击 |
| DoT伤害 | 0.3 | 每跳单独计算，权重较低 |

**连击时间衰减计算**：

| 时间差(秒) | 线性衰减 | 指数衰减(λ=0.5) | 二次衰减 |
|------------|----------|-----------------|----------|
| 0.0 | 1.000 | 1.000 | 1.000 |
| 1.0 | 0.667 | 0.607 | 0.444 |
| 2.0 | 0.333 | 0.368 | 0.111 |
| 3.0 | 0.000 | 0.223 | 0.000 |

**计算公式**：
```
线性衰减：剩余时间比例 = 1 - (时间差 / 时间窗口)
指数衰减：衰减因子 = exp(-λ × 时间差)
二次衰减：剩余时间比例 = (1 - 时间差/时间窗口)²
```

**连击奖励计算**：

| 连击数 | 当前阶段 | 移速加成 | 攻速加成 | 资源加成 | 伤害加成 | 电弧伤害 |
|--------|----------|----------|----------|----------|----------|----------|
| 5 | 无 | 0% | 0% | 0% | 0% | 无 |
| 15 | 阶段1 | 5% | 0% | 0% | 0% | 无 |
| 60 | 阶段2 | 5% | 10% | 10% | 0% | 无 |
| 105 | 阶段3 | 5% | 10% | 10% | 20% | 50%武器伤害 |

**总奖励计算**：
```
总移速加成 = 装备移速 + 连击移速（独立）
总攻速加成 = 装备攻速 + 连击攻速（加法）
总资源获取 = 基础资源 × (1 + 连击资源)（乘法）
总伤害加成 = (1 + 其他增伤) × (1 + 连击伤害)（独立乘区）
```

#### 💻 5.2.3 Unity C#实现代码

**核心连击管理器**：

```csharp
// Scripts/Combat/ComboManager.cs
using System.Collections.Generic;
using UnityEngine;

[System.Serializable]
public struct ComboStage
{
    public int threshold;
    public string name;
    public ComboReward[] rewards;
    public VisualEffectConfig visualEffects;
}

[System.Serializable]
public struct ComboReward
{
    public string type; // moveSpeed, attackSpeed, resourceGain, allDamage
    public float value;
    public string description;
}

public class ComboManager : MonoBehaviour
{
    [Header("配置引用")]
    [SerializeField] private ComboConfig config;

    [Header("运行时数据")]
    private int currentCombo = 0;
    private float lastHitTime = 0f;
    private int currentStageIndex = -1;
    private Dictionary<string, float> activeRewards = new();
    private bool isArcActive = false;
    private float arcTickTimer = 0f;

    // 事件委托
    public delegate void ComboChangedHandler(int newCombo, int oldCombo);
    public event ComboChangedHandler OnComboChanged;

    public delegate void StageChangedHandler(int newStage, string stageName);
    public event StageChangedHandler OnStageChanged;

    public delegate void ComboResetHandler(int lostCombo, ResetReason reason);
    public event ComboResetHandler OnComboReset;

    void Update()
    {
        // 检查时间中断
        CheckTimeout();

        // 更新电弧特效
        if (isArcActive)
        {
            UpdateArcEffect();
        }
    }

    public void RegisterHit(DamageType damageType, float damageAmount)
    {
        // 1. 计算权重连击数
        float weight = config.damageTypeWeights.GetValueOrDefault(damageType, 1.0f);
        int comboIncrement = Mathf.CeilToInt(weight); // 至少1连击

        // 2. 更新连击数
        int oldCombo = currentCombo;
        currentCombo = Mathf.Min(currentCombo + comboIncrement, config.globalParameters.maxCombo);
        lastHitTime = Time.time;

        // 3. 触发连击变化事件
        if (currentCombo != oldCombo)
        {
            OnComboChanged?.Invoke(currentCombo, oldCombo);
            PlayHitFeedback(currentCombo);
        }

        // 4. 检查阶段升级
        CheckStageUpgrade();

        // 5. 更新UI
        UpdateComboUI();
    }

    private void CheckTimeout()
    {
        if (currentCombo == 0) return;

        float timeSinceLastHit = Time.time - lastHitTime;
        float timeWindow = GetCurrentTimeWindow();

        if (timeSinceLastHit >= timeWindow)
        {
            ResetCombo(ResetReason.Timeout);
        }
        else if (timeSinceLastHit >= timeWindow * 0.7f)
        {
            // 剩余30%时间时警告
            PlayWarningFeedback(timeWindow - timeSinceLastHit);
        }
    }

    public void RegisterStaggerHit()
    {
        if (currentCombo == 0) return;

        if (config.interruptConditions.staggerHit.enabled)
        {
            ResetCombo(ResetReason.StaggerHit);

            // 应用debuff
            if (config.interruptConditions.staggerHit.debuffDuration > 0)
            {
                ApplyComboResetDebuff();
            }
        }
    }

    private void ResetCombo(ResetReason reason)
    {
        int lostCombo = currentCombo;
        currentCombo = 0;
        currentStageIndex = -1;
        ClearAllRewards();
        isArcActive = false;

        // 触发事件
        OnComboReset?.Invoke(lostCombo, reason);
        OnComboChanged?.Invoke(0, lostCombo);

        // 播放重置音效
        PlayResetFeedback(reason);
    }

    private void CheckStageUpgrade()
    {
        for (int i = config.stages.Length - 1; i >= 0; i--)
        {
            if (currentCombo >= config.stages[i].threshold && i > currentStageIndex)
            {
                // 升级到新阶段
                UpgradeToStage(i);
                break;
            }
        }
    }

    private void UpgradeToStage(int stageIndex)
    {
        int oldStage = currentStageIndex;
        currentStageIndex = stageIndex;

        var stage = config.stages[stageIndex];

        // 应用阶段奖励
        ApplyStageRewards(stage);

        // 触发事件
        OnStageChanged?.Invoke(stageIndex, stage.name);

        // 播放阶段升级特效
        PlayStageUpgradeFeedback(stageIndex);

        // 更新UI
        UpdateStageUI(stageIndex);
    }

    private void ApplyStageRewards(ComboStage stage)
    {
        foreach (var reward in stage.rewards)
        {
            switch (reward.type)
            {
                case "moveSpeed":
                    activeRewards["moveSpeed"] = reward.value;
                    break;

                case "attackSpeed":
                    activeRewards["attackSpeed"] = reward.value;
                    break;

                case "resourceGain":
                    activeRewards["resourceGain"] = reward.value;
                    break;

                case "allDamage":
                    activeRewards["allDamage"] = reward.value;
                    break;

                case "arcEffect":
                    isArcActive = true;
                    arcTickTimer = 0f;
                    break;
            }
        }
    }

    private void ClearAllRewards()
    {
        activeRewards.Clear();
        isArcActive = false;
    }

    private void UpdateArcEffect()
    {
        arcTickTimer += Time.deltaTime;

        if (arcTickTimer >= config.stages[2].rewards.arcEffect.tickInterval)
        {
            arcTickTimer = 0f;

            // 对周围敌人造成伤害
            DamageNearbyEnemies();

            // 播放电弧特效
            PlayArcEffect();
        }
    }

    private void DamageNearbyEnemies()
    {
        float radius = config.stages[2].rewards.arcEffect.radius;
        float damageMultiplier = config.stages[2].rewards.arcEffect.damagePerTick;
        float shockChance = config.stages[2].rewards.arcEffect.shockChance;

        Collider[] hitColliders = Physics.OverlapSphere(transform.position, radius);
        foreach (var collider in hitColliders)
        {
            var enemy = collider.GetComponent<Enemy>();
            if (enemy != null)
            {
                // 计算伤害
                float baseDamage = GetPlayerWeaponDamage();
                float arcDamage = baseDamage * damageMultiplier;
                enemy.TakeDamage(arcDamage, DamageType.Lightning);

                // 概率触发感电
                if (Random.value < shockChance)
                {
                    enemy.ApplyStatus(StatusType.Shock, 2.0f);
                }
            }
        }
    }

    // 获取当前连击奖励
    public float GetRewardValue(string rewardType)
    {
        if (activeRewards.ContainsKey(rewardType))
        {
            float baseValue = activeRewards[rewardType];
            float difficultyMultiplier = GetDifficultyMultiplier();
            return baseValue * difficultyMultiplier;
        }
        return 0f;
    }

    public bool IsArcActive() => isArcActive;
    public int GetCurrentCombo() => currentCombo;
    public int GetCurrentStage() => currentStageIndex;

    private float GetCurrentTimeWindow()
    {
        float baseTime = config.globalParameters.timeWindow;
        float difficultyMultiplier = GetDifficultyTimeMultiplier();

        // 无尽模式时间缩减
        if (GameManager.Instance.IsEndlessMode)
        {
            float reduction = config.difficultySettings.endless.timeWindowReductionPerWave
                * GameManager.Instance.CurrentWave;
            reduction = Mathf.Min(reduction,
                baseTime - config.difficultySettings.endless.minTimeWindow);
            return (baseTime - reduction) * difficultyMultiplier;
        }

        return baseTime * difficultyMultiplier;
    }

    private float GetDifficultyMultiplier()
    {
        var difficulty = GameManager.Instance.Difficulty;
        return config.difficultySettings.GetValueOrDefault(difficulty)?.rewardMultiplier ?? 1.0f;
    }

    private float GetDifficultyTimeMultiplier()
    {
        var difficulty = GameManager.Instance.Difficulty;
        switch (difficulty)
        {
            case Difficulty.Easy: return 4.0f / 3.0f; // +33%
            case Difficulty.Normal: return 1.0f;
            case Difficulty.Hard: return 2.5f / 3.0f; // -17%
            default: return 1.0f;
        }
    }

    // 反馈系统
    private void PlayHitFeedback(int combo)
    {
        // 音效：音调随连击数增加
        float pitch = config.audioFeedback.hitSounds.basePitch
            + config.audioFeedback.hitSounds.pitchIncreasePerCombo * combo;
        pitch = Mathf.Min(pitch, config.audioFeedback.hitSounds.maxPitch);

        float volume = Mathf.Lerp(
            config.audioFeedback.hitSounds.volumeBase,
            config.audioFeedback.hitSounds.volumeMax,
            combo / (float)config.globalParameters.maxCombo
        );

        AudioManager.Instance.PlaySound("SFX_Combo_Hit", volume, pitch);

        // 视觉：连击数字脉冲
        if (config.visualFeedback.comboCounter.pulseOnHit)
        {
            UIManager.Instance.PulseComboCounter(config.visualFeedback.comboCounter.pulseIntensity);
        }
    }

    private void PlayStageUpgradeFeedback(int stageIndex)
    {
        var stage = config.stages[stageIndex];

        // 音效
        AudioManager.Instance.PlaySound(stage.visualEffects.soundEffect,
            config.audioFeedback.stageSounds.volume);

        // 特效
        ParticleManager.Instance.PlayEffect(stage.visualEffects.particleEffect,
            transform.position);

        // 屏幕震动
        if (stage.visualEffects.screenShake.intensity > 0)
        {
            CameraManager.Instance.ShakeCamera(
                stage.visualEffects.screenShake.intensity,
                stage.visualEffects.screenShake.duration
            );
        }
    }

    private void PlayWarningFeedback(float timeLeft)
    {
        if (config.audioFeedback.warningSound.enabled &&
            timeLeft <= config.audioFeedback.warningSound.triggerTime)
        {
            AudioManager.Instance.PlaySound(
                config.audioFeedback.warningSound.sound,
                config.audioFeedback.warningSound.volume
            );

            // 视觉警告
            UIManager.Instance.FlashWarningColor();
        }
    }

    private void PlayResetFeedback(ResetReason reason)
    {
        AudioManager.Instance.PlaySound(
            config.audioFeedback.resetSound.sound,
            config.audioFeedback.resetSound.volume
        );

        // 根据重置原因播放不同特效
        switch (reason)
        {
            case ResetReason.Timeout:
                ParticleManager.Instance.PlayEffect("VFX_Combo_Timeout", transform.position);
                break;
            case ResetReason.StaggerHit:
                ParticleManager.Instance.PlayEffect("VFX_Combo_StaggerReset", transform.position);
                break;
        }
    }

    private void PlayArcEffect()
    {
        ParticleManager.Instance.PlayEffect("VFX_Combo_Arc", transform.position);
        AudioManager.Instance.PlaySound("SFX_Combo_Arc", 0.7f);
    }

    private void UpdateComboUI()
    {
        UIManager.Instance.UpdateComboCounter(
            currentCombo,
            GetCurrentTimeWindow() - (Time.time - lastHitTime)
        );
    }

    private void UpdateStageUI(int stageIndex)
    {
        var stage = config.stages[stageIndex];
        UIManager.Instance.UpdateStageIndicator(
            stageIndex,
            stage.name,
            stage.visualEffects.textColor
        );
    }

    private void ApplyComboResetDebuff()
    {
        var debuffConfig = config.interruptConditions.staggerHit;
        StatusManager.Instance.ApplyStatus(
            StatusType.ComboResetDebuff,
            debuffConfig.debuffDuration,
            debuffConfig.debuffEffect
        );
    }
}

public enum ResetReason
{
    Timeout,
    StaggerHit,
    Death,
    Manual
}

public enum DamageType
{
    Melee,
    Ranged,
    Area,
    Dot,
    Environmental
}
```

**单元测试代码**：

```csharp
// Tests/EditMode/ComboManagerTests.cs
using NUnit.Framework;
using UnityEngine;

public class ComboManagerTests
{
    private ComboManager comboManager;
    private TestComboConfig config;

    [SetUp]
    public void SetUp()
    {
        // 创建测试配置
        config = ScriptableObject.CreateInstance<TestComboConfig>();
        config.globalParameters = new GlobalParameters {
            timeWindow = 3f,
            maxCombo = 100
        };

        config.stages = new ComboStage[] {
            new ComboStage {
                threshold = 10,
                rewards = new ComboReward[] {
                    new ComboReward { type = "moveSpeed", value = 0.05f }
                }
            },
            new ComboStage {
                threshold = 50,
                rewards = new ComboReward[] {
                    new ComboReward { type = "attackSpeed", value = 0.10f },
                    new ComboReward { type = "resourceGain", value = 0.10f }
                }
            }
        };

        // 创建管理器
        var go = new GameObject("ComboManager");
        comboManager = go.AddComponent<ComboManager>();
        comboManager.SetConfigForTesting(config);
    }

    [Test]
    public void TestComboIncrement()
    {
        // 第一次命中
        comboManager.RegisterHit(DamageType.Melee, 100f);
        Assert.AreEqual(1, comboManager.GetCurrentCombo());

        // 第二次命中
        comboManager.RegisterHit(DamageType.Melee, 100f);
        Assert.AreEqual(2, comboManager.GetCurrentCombo());

        // 远程伤害权重0.8，应该只增加1连击
        comboManager.RegisterHit(DamageType.Ranged, 100f);
        Assert.AreEqual(3, comboManager.GetCurrentCombo());
    }

    [Test]
    public void TestStageUpgrade()
    {
        // 达到10连击应该升级到阶段1
        for (int i = 0; i < 10; i++)
        {
            comboManager.RegisterHit(DamageType.Melee, 100f);
        }

        Assert.AreEqual(1, comboManager.GetCurrentStage());
        Assert.AreEqual(0.05f, comboManager.GetRewardValue("moveSpeed"), 0.001f);

        // 达到50连击应该升级到阶段2
        for (int i = 0; i < 40; i++) // 已经是10连击，再加40
        {
            comboManager.RegisterHit(DamageType.Melee, 100f);
        }

        Assert.AreEqual(2, comboManager.GetCurrentStage());
        Assert.AreEqual(0.10f, comboManager.GetRewardValue("attackSpeed"), 0.001f);
        Assert.AreEqual(0.10f, comboManager.GetRewardValue("resourceGain"), 0.001f);
    }

    [Test]
    public void TestTimeoutReset()
    {
        // 建立一些连击
        comboManager.RegisterHit(DamageType.Melee, 100f);
        comboManager.RegisterHit(DamageType.Melee, 100f);
        Assert.AreEqual(2, comboManager.GetCurrentCombo());

        // 模拟时间流逝（3.1秒后）
        comboManager.SimulateTimePassing(3.1f);

        // 应该被重置
        Assert.AreEqual(0, comboManager.GetCurrentCombo());
        Assert.AreEqual(-1, comboManager.GetCurrentStage());
    }

    [Test]
    public void TestStaggerReset()
    {
        // 建立一些连击
        for (int i = 0; i < 5; i++)
        {
            comboManager.RegisterHit(DamageType.Melee, 100f);
        }
        Assert.AreEqual(5, comboManager.GetCurrentCombo());

        // 受到硬直打击
        comboManager.RegisterStaggerHit();

        // 应该被重置
        Assert.AreEqual(0, comboManager.GetCurrentCombo());
    }

    [Test]
    public void TestDamageTypeWeights()
    {
        // 重置连击
        comboManager.ResetComboForTesting();

        // 近战伤害：权重1.0
        comboManager.RegisterHit(DamageType.Melee, 100f);
        Assert.AreEqual(1, comboManager.GetCurrentCombo());

        // 远程伤害：权重0.8，应该只增加1连击
        comboManager.RegisterHit(DamageType.Ranged, 100f);
        Assert.AreEqual(2, comboManager.GetCurrentCombo());

        // 区域伤害：权重0.5，应该只增加1连击
        comboManager.RegisterHit(DamageType.Area, 100f);
        Assert.AreEqual(3, comboManager.GetCurrentCombo());

        // DoT伤害：权重0.3，应该只增加1连击
        comboManager.RegisterHit(DamageType.Dot, 100f);
        Assert.AreEqual(4, comboManager.GetCurrentCombo());
    }

    [Test]
    public void TestMaxComboLimit()
    {
        // 尝试超过最大连击数
        for (int i = 0; i < 150; i++)
        {
            comboManager.RegisterHit(DamageType.Melee, 100f);
        }

        // 应该被限制在100
        Assert.AreEqual(100, comboManager.GetCurrentCombo());
    }

    [TearDown]
    public void TearDown()
    {
        Object.DestroyImmediate(comboManager.gameObject);
    }
}
```

**可视化调试工具**：

```csharp
// Editor/ComboDebugWindow.cs
using UnityEditor;
using UnityEngine;

public class ComboDebugWindow : EditorWindow
{
    [MenuItem("Tools/Vampirefall/连击系统调试")]
    public static void ShowWindow()
    {
        GetWindow<ComboDebugWindow>("连击调试");
    }

    private ComboManager comboManager;
    private Vector2 scrollPos;
    private bool simulateTime = false;
    private float simulatedTimeScale = 1.0f;
    private float lastSimulatedTime = 0f;

    void OnGUI()
    {
        if (comboManager == null)
            comboManager = FindObjectOfType<ComboManager>();

        if (comboManager == null)
        {
            EditorGUILayout.HelpBox("场景中未找到ComboManager", MessageType.Warning);
            return;
        }

        // 控制面板
        EditorGUILayout.BeginHorizontal("Box");

        if (GUILayout.Button("+1 近战连击"))
            comboManager.RegisterHit(DamageType.Melee, 100f);

        if (GUILayout.Button("+1 远程连击"))
            comboManager.RegisterHit(DamageType.Ranged, 100f);

        if (GUILayout.Button("硬直中断"))
            comboManager.RegisterStaggerHit();

        if (GUILayout.Button("重置连击"))
            comboManager.ResetComboForTesting();

        EditorGUILayout.EndHorizontal();

        // 时间模拟
        EditorGUILayout.BeginHorizontal("Box");
        simulateTime = EditorGUILayout.Toggle("模拟时间", simulateTime);
        if (simulateTime)
        {
            simulatedTimeScale = EditorGUILayout.Slider("时间倍率", simulatedTimeScale, 0.1f, 10f);
            if (GUILayout.Button("前进1秒"))
                comboManager.SimulateTimePassing(1f);
        }
        EditorGUILayout.EndHorizontal();

        scrollPos = EditorGUILayout.BeginScrollView(scrollPos);

        // 当前状态
        EditorGUILayout.Space();
        EditorGUILayout.LabelField("当前状态", EditorStyles.boldLabel);

        EditorGUILayout.BeginVertical("Box");
        EditorGUILayout.LabelField($"连击数: {comboManager.GetCurrentCombo()}");
        EditorGUILayout.LabelField($"当前阶段: {comboManager.GetCurrentStage()}");
        EditorGUILayout.LabelField($"上次命中时间: {comboManager.GetLastHitTime():F2}");
        EditorGUILayout.LabelField($"剩余时间: {comboManager.GetRemainingTime():F2}s");
        EditorGUILayout.LabelField($"电弧激活: {comboManager.IsArcActive()}");
        EditorGUILayout.EndVertical();

        // 当前奖励
        EditorGUILayout.Space();
        EditorGUILayout.LabelField("当前奖励", EditorStyles.boldLabel);

        EditorGUILayout.BeginVertical("Box");
        EditorGUILayout.LabelField($"移速加成: {comboManager.GetRewardValue("moveSpeed"):P0}");
        EditorGUILayout.LabelField($"攻速加成: {comboManager.GetRewardValue("attackSpeed"):P0}");
        EditorGUILayout.LabelField($"资源加成: {comboManager.GetRewardValue("resourceGain"):P0}");
        EditorGUILayout.LabelField($"伤害加成: {comboManager.GetRewardValue("allDamage"):P0}");
        EditorGUILayout.EndVertical();

        // 配置信息
        EditorGUILayout.Space();
        EditorGUILayout.LabelField("配置信息", EditorStyles.boldLabel);

        var config = comboManager.GetConfigForTesting();
        if (config != null)
        {
            EditorGUILayout.BeginVertical("Box");
            EditorGUILayout.LabelField($"时间窗口: {config.globalParameters.timeWindow:F1}s");
            EditorGUILayout.LabelField($"最大连击: {config.globalParameters.maxCombo}");
            EditorGUILayout.LabelField($"阶段数量: {config.stages.Length}");

            EditorGUILayout.Space();
            EditorGUILayout.LabelField("阶段阈值:", EditorStyles.miniBoldLabel);
            foreach (var stage in config.stages)
            {
                EditorGUILayout.LabelField($"  {stage.name}: {stage.threshold}连击");
            }
            EditorGUILayout.EndVertical();
        }

        // 伤害权重
        EditorGUILayout.Space();
        EditorGUILayout.LabelField("伤害权重", EditorStyles.boldLabel);

        EditorGUILayout.BeginVertical("Box");
        if (config != null && config.damageTypeWeights != null)
        {
            foreach (var kvp in config.damageTypeWeights)
            {
                EditorGUILayout.LabelField($"{kvp.Key}: {kvp.Value:F1}");
            }
        }
        EditorGUILayout.EndVertical();

        // 历史记录
        EditorGUILayout.Space();
        EditorGUILayout.LabelField("连击历史", EditorStyles.boldLabel);

        var history = comboManager.GetComboHistoryForTesting();
        if (history.Count > 0)
        {
            EditorGUILayout.BeginVertical("Box");
            foreach (var record in history)
            {
                EditorGUILayout.LabelField(
                    $"+{record.timestamp:F1}s: {record.combo}连击 ({record.damageType})"
                );
            }
            EditorGUILayout.EndVertical();
        }

        EditorGUILayout.EndScrollView();
    }

    void Update()
    {
        if (simulateTime)
        {
            float deltaTime = Time.realtimeSinceStartup - lastSimulatedTime;
            if (deltaTime >= 0.1f) // 每0.1秒更新一次
            {
                comboManager.SimulateTimePassing(deltaTime * simulatedTimeScale);
                lastSimulatedTime = Time.realtimeSinceStartup;
                Repaint();
            }
        }
    }
}
```

---

### 🌍 5.3 业界案例分析：鬼泣评分系统

为了防止“站撸”，限制回复手段。

*   **生命偷取 (Life Leech):** 不是瞬间回复。
    *   造成伤害的 x% 进入“吸血池”。
    *   吸血池以 `MaxHP * 20% / sec` 的速度回充到生命值。
    *   满血时吸血池清空。
*   **击杀回复 (Life on Kill):** 瞬间回复固定数值。适合割草。
*   **药瓶 (Flask):** 类似 PoE，充能制。杀怪充能，而非冷却制。

---

## 7. 技术实现备注

*   **Tag System:** 使用 `GameplayTag` (如 UE) 或类似的 `Enum Flags` (Unity) 来标记伤害类型 (e.g., `Damage.Fire`, `Damage.Melee`)。
*   **Snapshotting:** DoT 伤害应在施加瞬间计算数值（快照机制），而非随玩家实时面板变化，以减少计算量。
