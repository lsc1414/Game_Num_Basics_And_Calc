# 🛠️ Luban 配表实战与 ID 命名规范 (Config Practices)

本文档旨在确立 Project Vampirefall 的配表标准。我们使用 **Luban** 作为核心数据工具。

---

## 1. ID 设计辩论：字符串 vs 数字 (String Key vs Int Key)

*(...此处保持原有的 ID 对比内容，为节省篇幅省略，实际写入时会保留...)*
这是一个没有标准答案的选择，取决于团队更看重**程序维护性**还是**策划填表效率**。

### 🔴 纯数字 ID (Int Key)
*   **格式:** `1001`, `200201`
*   **优点:** Excel 友好，存储小。
*   **缺点:** 代码可读性差，易冲突，分段维护累。

### 🔵 字符串语义 ID (String Semantic Key) - *推荐方案*
*   **格式:** `Item_Sword_Fire_01`
*   **优点:** 代码自解释，调试方便。
*   **缺点:** 手输易错，Excel 无法递增。
*   **对策:** 详见下文 Excel 技巧章节。

---

## 2. 字符串 ID 命名范例 (Naming Examples)

*(...此处保持原有的命名范例内容...)*

---

## 3. Excel 填表实战技巧 (Excel Best Practices)

*(...此处保持原有的公式生成 ID、下拉菜单内容...)*

---

## 4. 多态填写的救赎：如何让策划不骂人 (Handling Polymorphism)

Luban 的多态功能（`Bean#Field=Val`）虽然程序用爽了，但如果直接让策划手填字符串，**出错率是 100%**。

### ❌ 错误做法：让策划手写
*   策划在单元格填：`DamageEffect#value=100;type=Fire`
*   **后果:** 策划拼错单词 `valeu`，或者漏了分号，或者大小写错了。程序解析报错，排查半天。

### ✅ 解决方案 A：Excel 辅助列 + 公式自动拼接 (推荐)

利用 Excel 的隐藏列，策划只填“人看得懂的列”，Excel 帮我们拼“Luban 看得懂的字”。

**场景:** 技能效果 (SkillEffect)，可能是造成伤害 (Damage)，也可能是加血 (Heal)。

**Excel 表头设置:**

| 列号 | A | B | C | D | E (导出给Luban) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **注释** | **效果类型** | **参数1(数值)** | **参数2(类型/其他)** | **参数3** | **(隐藏)实际效果字段** |
| **填写示例** | `Damage` | 100 | Fire | | `DamageEffect#amt=100;element=Fire` |
| **填写示例** | `Heal` | 500 | | | `HealEffect#amt=500` |

**E 列公式 (核心魔法):**
使用 `IFS` 或 `CHOOSE` 函数根据 A 列的类型，拼接不同的字符串模板。

```excel
=IFS(
  A2="Damage", "DamageEffect#amt=" & B2 & ";element=" & C2,
  A2="Heal",   "HealEffect#amt=" & B2,
  A2="Summon", "SummonEffect#unit=" & C2 & ";duration=" & B2,
  TRUE, ""
)
```

*   **优势:**
    1.  策划只需要在 B、C 列填数字或选类型。
    2.  字段名 (`amt`, `element`) 此时硬编码在公式里，策划**永远**不会拼错。
    3.  如果某个类型参数太多，列不够用，见方案 B。

### ✅ 解决方案 B：拆表引用法 (针对复杂结构)

如果一个多态 Bean 里面有 10 个参数，Excel 这一行就没法看了。此时应果断**拆表**。

**结构:**
1.  **主表 (SkillTable):** 不存具体效果，只存一个 `EffectID` (String)。
2.  **子表 (SkillEffectTable):** 专门的一张表，用来定义效果。

**SkillEffectTable 设计:**
这张表可以做得非常宽，或者利用 Luban 的 **Excel 多行记录 (Multi-Row Record)** 特性。

或者，更简单地，按类型拆分 Sheet：
*   `Sheet_Damage`: 专门填伤害类，列定义固定 (Amt, Element)。
*   `Sheet_Heal`: 专门填治疗类，列定义固定 (Amt)。
*   `Sheet_Summon`: 专门填召唤类。

然后 Luban 配置所有这些 Sheet 都导出到同一个 `cfg.SkillEffect` 列表中。

### 🎯 总结：推荐工作流

1.  **简单多态 (2-3个参数):** 使用 **方案 A (公式拼接)**。
    *   例子: 物品的使用效果（加血、回蓝）。
2.  **复杂多态 (>5个参数):** 使用 **方案 B (引用独立表)**。
    *   例子: AI 行为树节点配置、复杂的关卡逻辑。

---

## 5. 必须遵守的“防呆”军规

为了保护策划的理智，请程序遵守以下军规：

1.  **Demo 必须有:** 在 Excel 的首行（数据开始前的注释行），**必须**给每一个多态类型留一个正确的 Demo 字符串。
2.  **字段名统一:** 所有子类的同义字段必须同名。
    *   ❌ `DamageBean` 用 `Amount`, `HealBean` 用 `Value`。
    *   ✅ 全部统一叫 `Value`。这样 Excel 公式好写，策划也好记。
3.  **默认值:** Bean 定义时尽量给字段默认值。这样策划不填那一列时，生成的字符串可以少写几个参数。
