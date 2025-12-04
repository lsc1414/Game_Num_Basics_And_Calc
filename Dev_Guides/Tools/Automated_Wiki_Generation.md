# 🛠️ 自动化 WIKI 生成指南：从零散项目资源到结构化文档

> **背景**: 在开发过程中，设计文档往往滞后于代码，或者数据分散在各种 `ScriptableObject`、`Prefab`、`C# 常量` 和 `JSON` 表中。
> **目标**: 建立一套 **"代码即真理" (Code as Truth)** 的自动化管线，直接从工程源文件提取数据生成 Wiki，确保游戏内数值与 Wiki 100% 同步。

## 1. 核心策略：逆向工程 (Reverse Engineering Approach)

既然没有统一的 Excel 表，我们需要把 Unity 工程本身视为一个巨大的数据库。

### 1.1 数据源扫描 (Data Source Mapping)
| 数据类型 | 常见存储位置 | 提取方式 | 推荐方案 |
| :--- | :--- | :--- | :--- |
| **基础数值** (伤害公式、常量) | `C# static const` / `Enums` | 源码解析 (Roslyn) 或 反射 | **C# 反射** (最简单) |
| **配置数据** (英雄、装备、怪物) | `ScriptableObject` (.asset) | `AssetDatabase` 加载 | **Unity Editor 脚本** |
| **实体数据** (塔、单位属性) | `Prefab` (MonoBehaviour 字段) | `PrefabUtility` 加载 | **Unity Editor 脚本** |
| **文本描述** (名称、技能说明) | `Localization` (.csv/.json) | 文本解析 | **CSV/JSON 库读取** |

## 2. 🏗️ 架构设计：Wiki 导出器 (The Wiki Exporter)

我们将创建一个 Unity Editor 工具，它在构建时运行，扫描指定目录，提取数据，并输出 Markdown 或 JSON。

### 2.1 "标记" 系统 (The Attribute System)
为了告诉导出器哪些字段需要显示在 Wiki 上，我们需要自定义 C# Attribute。这比维护一份复杂的配置文件要灵活得多。

```csharp
// 1. 定义 Attribute
[AttributeUsage(AttributeTargets.Field | AttributeTargets.Class)]
public class WikiExportAttribute : Attribute {
    public string Section; // 归属板块 (如 "基础属性")
    public string Desc;    // 字段解释 (如 "攻击速度，单位：次/秒")
    
    public WikiExportAttribute(string section = "General", string desc = "") { ... }
}

// 2. 在业务代码中使用
public class TowerData : ScriptableObject {
    [WikiExport("Stats", "塔的基础攻击力")]
    public float BaseDamage;

    [WikiExport("Stats", "攻击间隔")]
    public float AttackRate;
    
    // 不需要导出的内部字段不加标签
    public string internalId; 
}
```

### 2.2 核心导出逻辑 (Editor Script)

创建一个 `WikiGenerator.cs` 放在 `Editor` 文件夹下：

1.  **收集类型**: 扫描所有包含 `[WikiExport]` 的类。
2.  **加载资产**: 使用 `AssetDatabase.FindAssets("t:TowerData")` 找到所有实例。
3.  **反射读取**: 遍历实例字段，读取值和 Attribute 描述。
4.  **格式化输出**: 使用 `StringBuilder` 拼接 Markdown 表格。

```csharp
// 伪代码示例
public static void GenerateWiki() {
    var sb = new StringBuilder();
    sb.AppendLine("# 🏰 防御塔图鉴");
    sb.AppendLine("| 名称 | 攻击力 | 攻速 | 说明 |");
    sb.AppendLine("| :--- | :--- | :--- | :--- |");

    var guids = AssetDatabase.FindAssets("t:TowerData");
    foreach (var guid in guids) {
        var path = AssetDatabase.GUIDToAssetPath(guid);
        var tower = AssetDatabase.LoadAssetAtPath<TowerData>(path);
        
        sb.Append($"| {tower.displayName} ");
        sb.Append($"| {tower.BaseDamage} ");
        sb.Append($"| {tower.AttackRate} ");
        sb.Append($"| {tower.description} |
");
    }
    
    File.WriteAllText("Docs/Wiki/Towers.md", sb.ToString());
}
```

## 3. 🔄 自动化管线 (The Pipeline)

### 3.1 本地开发流
1.  程序员/策划修改 `ScriptableObject` 数值。
2.  点击菜单栏 `Tools > Vampirefall > Generate Wiki`。
3.  脚本在 `Docs/` 目录下生成最新的 `.md` 文件。
4.  提交 Git。

### 3.2 CI/CD 集成 (进阶)
1.  Jenkins/GitHub Actions 触发构建。
2.  调用 Unity 命令行模式:
    `-batchmode -executeMethod WikiGenerator.GenerateWiki -quit`
3.  脚本将生成的 Markdown 推送到 Wiki 仓库 (如 GitHub Wiki 或 Hugo 站点)。

## 4. 📄 内容模板 (Templates)

单纯的数据表格很难看。建议采用 **模板注入** 的方式。

1.  **模板文件 (`Tower_Template.md`)**:
    ```markdown
    # {DisplayName}
    
    ## 基础信息
    - 类型: {Type}
    - 稀有度: {Rarity}
    
    ## 属性表
    {StatsTable}
    
    ## 技能描述
    > {SkillDescription}
    ```
2.  **生成器逻辑**: 读取模板 -> 替换占位符 -> 输出文件。

## 5. 🚀 实施步骤 (Action Plan)

1.  **第一周**: 定义 `[WikiExport]` Attribute，并给核心类 (`EnemyData`, `TowerData`, `ItemData`) 加上标签。
2.  **第二周**: 编写最简单的 Editor 脚本，仅导出 "怪物列表.md" (包含名称、HP、攻击力)，验证流程。
3.  **第三周**: 接入本地化文件，确保 Wiki 显示的是中文名称而不是 `ENEMY_001`。
4.  **第四周**: 优化排版，支持图片导出 (自动将 Icon 转换并引用)。

## 6. 💡 常见问题解决方案

*   **问题**: 数据在 Prefab 上，不在 ScriptableObject 里怎么办？
    *   **解**: `AssetDatabase.FindAssets("t:Prefab")` -> `LoadAsset` -> `GetComponent<MyScript>()` -> 读取字段。
*   **问题**: 伤害公式是代码逻辑，怎么导出？
    *   **解**: 这种通常无法自动导出。建议在代码注释里写好 Markdown，利用工具 (如 DocFX) 提取注释，或者手动维护这部分“机制文档”，只自动生成“数值图鉴”。
*   **问题**: 图片怎么处理？
    *   **解**: 导出脚本可以顺便把引用的 `Sprite` 复制到 Wiki 的 `images/` 目录，并按 UUID 重命名，确保链接不失效。
