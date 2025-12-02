# 📝 游戏文本配置方案：富文本、动态参数与多语言架构

在现代游戏中，技能描述（Tooltip）不仅仅是一段文字，它是**逻辑的视觉化呈现**。不仅需要处理数值的动态变化，还要应对复杂的富文本样式（颜色、图标、超链接）以及多语言本地化（L10n）的挑战。

本文档详细阐述了业界通用的文本配置标准和技术实现方案。

---

## 1. 核心痛点与设计目标

| 痛点 | 描述 | 解决方案 |
| :--- | :--- | :--- |
| **数据脱节** | 技能伤害从 10 改为 20，描述文本忘了更新，仍显示 "造成 10 点伤害"。 | **动态参数注入**：文本只作为模版，数值实时读取。 |
| **样式硬编码** | 使用 `<color=#FF0000>` 硬编码颜色，后期美术调整风格时需修改上万条文本。 | **语义化标签**：使用 `<c=dmg_phys>`，通过全局样式表解析。 |
| **交互缺失** | 描述中提到“点燃”状态，玩家不知道“点燃”具体效果。 | **超链接系统**：`<l=buff_burn>`，点击/悬停弹出详细 Tooltip。 |
| **语言差异** | 俄语/阿拉伯语的复数规则复杂，语序与英语完全不同。 | **ICU MessageFormat**：支持性数变化的标准语法。 |

---

## 2. 架构设计：三层解耦模型

我们将文本系统分为三层：**配置层 (Template)**、**解析层 (Parser)**、**渲染层 (Renderer)**。

### 2.1 配置层 (Excel / Localization Table)

不要在代码中硬编码文本。所有文本应在 Excel 或 Google Sheets 中管理，并导出为 CSV/JSON。

**配置示例：**

| Key | Context | English | Chinese_Simplified |
| :--- | :--- | :--- | :--- |
| `Skill_Fireball_Name` | 技能名 | Fireball | 火球术 |
| `Skill_Fireball_Desc` | 技能描述 | Hurls a bolt dealing <c=dmg>{0}</c> damage and applying <l=buff_burn>Burn</l>. | 发射火球，造成 <c=dmg>{0}</c> 点伤害并施加 <l=buff_burn>燃烧</l>。 |

*   `{0}`: 占位符，将在运行时被实际伤害值替换。
*   `<c=dmg>`: 语义化颜色标签。
*   `<l=buff_burn>`: 链接标签，指向 ID 为 `buff_burn` 的数据。

### 2.2 解析层 (C# Text Parser)

这是系统的核心，负责将“模版”转换为“最终富文本”。

#### A. 动态参数注入 (Dynamic Injection)

```csharp
public class SkillDescriptionBuilder {
    public string GetDescription(SkillData skill) {
        // 1. 获取本地化模版
        string template = LocalizationManager.Get(skill.DescriptionKey); 
        // template = "造成 <c=dmg>{0}</c> 点伤害"

        // 2. 获取实时数值 (关键步骤)
        // 技能实例必须能提供上下文数据
        float currentDamage = skill.Attributes.Get(StatType.Damage).Value; 
        
        // 3. 格式化
        // 注意：建议封装 string.Format 以处理异常
        return string.Format(template, currentDamage);
    }
}
```

#### B. 参数格式化 (Parameter Formatting)

直接注入浮点数会导致 "造成 10.533333 点伤害" 这种丑陋的显示。C# 的 `string.Format` 原生支持格式说明符，必须充分利用。

**常用格式语法：**

| 语法 | 说明 | 示例输入 | 输出结果 |
| :--- | :--- | :--- | :--- |
| `{0:0}` | 整数（四舍五入） | `10.6` | `11` |
| `{0:0.0}` | 保留一位小数 | `10.0` -> `10.0` | `10.0` |
| `{0:0.#}` | 最多保留一位小数（去掉末尾0） | `10.0` -> `10` | `10` |
| `{0:0%}` | 百分比格式 | `0.15` | `15%` |
| `{0:+0;-0;0}` | 强制正负号 | `5` | `+5` |

**配置示例（优化后）：**

| Key | Template | 实际数值 | 最终文本 |
| :--- | :--- | :--- | :--- |
| `Skill_Heal` | 恢复 {0:0} 点生命 | `50.6` | 恢复 51 点生命 |
| `Buff_Crit` | 暴击率提高 {0:+0%} | `0.123` | 暴击率提高 +12% |

#### C. 语义标签替换 (Semantic Tag Replacement)

不要让策划直接写 Hex 颜色码。建立一个全局样式表（ScriptableObject）。

```csharp
// 样式表配置
public Dictionary<string, string> styleMap = new Dictionary<string, string>() {
    { "dmg", "#FF4500" },       // 物理伤害橙红色
    { "heal", "#00FF7F" },      // 治疗翠绿色
    { "warn", "#FFD700" }       // 警告金黄色
};

// 解析逻辑 (Regex 或 字符串替换)
public string ParseTags(string input) {
    // 将 <c=dmg> 替换为 <color=#FF4500>
    // 将 <l=buff_id> 替换为 <link="buff_id"> (TextMeshPro 格式)
    // 将 <s=icon_fire> 替换为 <sprite name="icon_fire">
    return processedString;
}
```

### 2.3 渲染层 (Unity TextMeshPro)

使用 Unity 的 `TextMeshPro (TMP)` 组件进行渲染。

*   **超链接交互**：
    TMP 组件支持 `OnLinkPointerClick` 事件。
    ```csharp
    public void OnPointerClick(PointerEventData eventData) {
        int linkIndex = TMP_TextUtilities.FindIntersectingLink(tmpText, Input.mousePosition, ...);
        if (linkIndex != -1) {
            TMP_LinkInfo linkInfo = tmpText.textInfo.linkInfo[linkIndex];
            string linkID = linkInfo.GetLinkID(); // 获取 "buff_burn"
            TooltipSystem.Show(linkID); // 弹出对应 ID 的详情页
        }
    }
    ```

---

## 3. 进阶功能：智能文本 (Smart Text)

对于复杂逻辑，简单的 `{0}` 可能不够。可以引入简单的表达式解析。

### 条件文本 (Conditional Text)
语法：`"Deal {dmg} damage. {if isNight}Stun target.{/if}"`
*   **场景**：某些效果仅在特定条件（如夜晚、满血）下生效。
*   **实现**：解析器检测到 `{if}` 块时，计算布尔条件。若为 `false`，剔除块内文本，避免显示无意义的描述。

### 动态运算 (Math Operations)
语法：`"Next level: {dmg * 1.2} damage."`
*   **场景**：显示升级后的预览数值。
*   **实现**：解析器支持基础数学运算，直接根据当前变量算出预览值。

### ICU 复数支持 (Plurals)
语法：`"Summon {count, plural, one {1 Skeleton} other {# Skeletons}}."`
*   **场景**：处理 "1 Skeleton" vs "5 Skeletons" 的语言差异。
*   **工具**：Unity 插件如 **I2 Localization** 或 **Smart String** 已内置此功能。

---

## 4. Vampirefall 落地建议

### 推荐技术栈
*   **存储**: Excel / Google Sheets (利用 Luban 导出)。
*   **运行时**: I2 Localization (处理多语言加载) + TextMeshPro (渲染)。
*   **逻辑层**: 自定义 `TextFormatter` 类。

### 开发工具 (Editor Tool)
**必做工具**：**技能描述预览器**。
*   **界面**：左侧选择技能，右侧显示 TMP 渲染出的富文本。
*   **功能**：
    *   提供“等级”滑块：拖动滑块，实时看到描述里的数字变化（验证公式绑定是否正确）。
    *   样式切换：一键切换“亮色模式/暗色模式”，检查颜色标签在不同底板下的可读性。

### 命名规范
*   **颜色标签**：使用功能命名，而非颜色命名。
    *   ✅ `<c=buff>` (Buff颜色)
    *   ❌ `<c=green>` (绿色)
*   **图标标签**：与图集 Sprite 名字保持一致。
    *   `<s=stat_atk>` -> 对应图集里的 `stat_atk.png`。

---

## 5. 总结

技能文本系统本质上是一个**微型 UI 程序**。
*   **Input**: 技能数据 (SkillData) + 本地化模版 (Template)。
*   **Process**: 注入参数 -> 替换标签 -> 处理逻辑。
*   **Output**: 带有交互功能的富文本 (Rich Text)。

通过这套架构，我们可以确保描述永远准确（数据驱动）、样式易于统一调整（语义标签），并提供顶级的用户体验（超链接交互）。
