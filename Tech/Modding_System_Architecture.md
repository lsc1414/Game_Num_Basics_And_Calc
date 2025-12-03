# 🛠️ Mod 系统架构指南 (Modding System Architecture)

> **核心哲学**: 游戏本体应该只是一个 **"引擎" (Engine)**，而所有的官方内容（塔、怪、装备）都应该被视为 **"官方 Mod" (Core Mod)**。
> 当你把官方内容也当成 Mod 来加载时，Mod 支持就自然完成了。

## 1. Mod 的三个层级 (The Three Tiers)

### Tier 1: 数值与配置 Mod (Data Mod)
*   **难度**: 低。
*   **功能**: 修改塔的攻击力、修改掉率、修改怪物血量。
*   **实现**: 使用 **JSON / XML / CSV** 存储数据，而不是写死在 C# 里或 ScriptableObject 里。
    *   *例子*: 玩家把 `Tower_Fire.json` 里的 `"damage": 10` 改成 `"damage": 9999`。

### Tier 2: 资源替换 Mod (Asset Mod)
*   **难度**: 中。
*   **功能**: 替换塔的贴图 (Skin)、修改音效、汉化/多语言。
*   **实现**: 运行时动态加载 `.png` / `.wav` / `.txt`。
    *   *例子*: 玩家画了一个皮卡丘，把 `Tower_Fire.png` 替换掉，游戏里火塔就变成了皮卡丘。

### Tier 3: 逻辑脚本 Mod (Script Mod)
*   **难度**: 高。
*   **功能**: 创造全新的机制（比如“吃怪物的塔”）。
*   **实现**: 嵌入 **Lua (XLua/ToLua)** 或 **C# (Harmony/BepInEx)**。

---

## 2. 架构设计方案 (Architecture Design)

### 2.1 目录结构 (Folder Structure)
在 `Application.streamingAssetsPath` 下建立 `Mods` 文件夹。

```text
Vampirefall_Data/
└── StreamingAssets/
    └── Mods/
        ├── Core/ (官方内容)
        │   ├── mod_info.json
        │   ├── Towers/
        │   │   ├── FireTower.json
        │   │   └── FireTower.png
        │   └── Localization/
        │       └── en.json
        └── MyCrazyMod/ (玩家Mod)
            ├── mod_info.json (定义依赖、版本)
            ├── Towers/
            │   └── SuperTower.json
            └── Scripts/
                └── main.lua
```

### 2.2 数据加载流程 (The Loading Pipeline)

**原则**: **后加载覆盖先加载 (Last Write Wins)**。

1.  **初始化**: 扫描 `Mods` 目录下所有文件夹。
2.  **排序**: 根据 `mod_info.json` 里的 `order` 或 `dependencies` 排序。
    *   Core (Order: 0)
    *   Community_Patch (Order: 10)
    *   CrazyMod (Order: 100)
3.  **合并**:
    *   加载 Core 的 `FireTower.json`。
    *   加载 CrazyMod 的 `FireTower.json`（如果存在）。
    *   如果 CrazyMod 里只写了 `{"damage": 999}`，则只修改 damage 字段，保留其他字段不变 (**Deep Merge**)。

### 2.3 核心代码实现 (C# Demo)

这是一个简单的 JSON Mod 加载器伪代码。

```csharp
[System.Serializable]
public class TowerDefinition {
    public string id;
    public float damage;
    public string spritePath;
}

public class ModManager : MonoBehaviour {
    // 存储所有塔的定义
    public Dictionary<string, TowerDefinition> towerDatabase = new Dictionary<string, TowerDefinition>();

    public void LoadAllMods() {
        string modsRoot = Path.Combine(Application.streamingAssetsPath, "Mods");
        var directories = Directory.GetDirectories(modsRoot);
        
        // 1. 遍历每个 Mod 文件夹
        foreach (var dir in directories) {
            // 2. 加载 Towers 目录下的 JSON
            var towerFiles = Directory.GetFiles(Path.Combine(dir, "Towers"), "*.json");
            foreach (var file in towerFiles) {
                string json = File.ReadAllText(file);
                
                // 3. 解析
                TowerDefinition def = JsonUtility.FromJson<TowerDefinition>(json);
                
                // 4. 注册/覆盖
                if (towerDatabase.ContainsKey(def.id)) {
                    // 简单覆盖 (实际项目建议做 Deep Merge)
                    towerDatabase[def.id] = def; 
                    Debug.Log($"[Mod] Overwrote tower: {def.id}");
                } else {
                    towerDatabase.Add(def.id, def);
                    Debug.Log($"[Mod] Added tower: {def.id}");
                }
            }
        }
    }
    
    // 运行时获取图片
    public Sprite LoadSprite(string partialPath) {
        // 逻辑：去所有 Mod 文件夹里找这个图，返回优先级最高的那张
        // ... 使用 Texture2D.LoadImage() ...
    }
}
```

## 3. 脚本 Mod 支持详解：Harmony 方案

Harmony 是一个 C# 库，用于在 **运行时 (Runtime)** 替换或修改现有的 .NET 方法。即使你没有源码，只要你有 DLL，你就能修改它。

### 3.1 核心原理 (How it works)
Harmony 不修改磁盘上的 DLL 文件，而是在内存中修改机器码。
它利用反射找到目标方法 `TargetMethod`，然后插入三种“补丁”：
1.  **Prefix (前置补丁)**: 在原方法执行**前**运行。
    *   *用途*: 修改输入参数，或者拦截执行（直接 `return false` 跳过原方法）。
2.  **Postfix (后置补丁)**: 在原方法执行**后**运行。
    *   *用途*: 修改返回值，或者读取原方法的计算结果。
3.  **Transpiler (转译补丁)**: 修改原方法的 IL 指令。
    *   *用途*: 高级黑魔法，修改方法中间的某一行逻辑。

### 3.2 如何在官方项目中集成 Harmony？
如果你决定官方支持 C# Mod (像 *RimWorld* 那样)，你可以内置 Harmony。

1.  **引入库**: 将 `0Harmony.dll` 放进 Plugins。
2.  **Mod Loader**: 编写一个加载器，扫描 Mods 文件夹下的 `.dll`。
3.  **执行加载**:
    ```csharp
    // 在游戏启动时执行
    void LoadScriptMods() {
        var modDlls = Directory.GetFiles(modPath, "*.dll");
        foreach(var dll in modDlls) {
            var assembly = Assembly.LoadFile(dll);
            // Harmony 会自动扫描该 DLL 中带有 [HarmonyPatch] 标签的类并应用
            var harmony = new Harmony("com.vampirefall.mod." + assembly.GetName().Name);
            harmony.PatchAll(assembly);
        }
    }
    ```

### 3.3 Modder 如何写代码？(示例)
假设官方代码里有一个计算伤害的方法：
```csharp
// 官方代码
public class DamageCalculator {
    public int Calculate(int baseDmg) {
        return baseDmg * 2;
    }
}
```

Modder 想把伤害改成 10倍，他只需要写一个 DLL：
```csharp
// Modder 代码
[HarmonyPatch(typeof(DamageCalculator), "Calculate")]
public class DamagePatch {
    // Postfix: 在原方法返回后，修改结果
    static void Postfix(ref int __result) {
        __result *= 10; // 把结果乘以 10
    }
}
```

### 3.4 Harmony 的优缺点
| 维度 | 优点 | 缺点 |
| :--- | :--- | :--- |
| **能力** | **无限**。可以修改游戏里任何一行私有代码。 | **不安全**。Mod 可以轻易崩溃游戏，甚至写病毒。 |
| **性能** | 极高。修改的是 JIT 后的机器码，几乎无损耗。 | 如果 100 个 Mod 同时 Patch 一个方法，调用栈会很深。 |
| **维护** | 社区生态成熟 (*RimWorld*, *Cities: Skylines* 都用它)。 | 如果官方更新改了方法名，Mod 直接失效 (红字报错)。 |

### 3.5 建议
对于 *Vampirefall*：
*   **初期**: 暂时不需要官方集成 Harmony。因为 **BepInEx** (第三方 Mod 加载器) 已经完美支持 Unity 游戏了。硬核玩家自己会装 BepInEx。
*   **官方态度**: **默许但不提供支持**。不要使用 IL2CPP 打包（这会让 Harmony 失效），尽量使用 Mono 后端，方便社区逆向。

## 4. BepInEx：Unity Modding 的事实标准

如果 Harmony 是手术刀，**BepInEx (Bepis Injector Extensible)** 就是全套的手术台。

### 4.1 BepInEx 是什么？
它是一个开源的 **Unity / .NET 游戏插件框架**。
*   **功能**: 它负责把 Modder 写的 DLL 注入到游戏进程中，并提供生命周期管理 (Start, Update)、配置管理 (Config)、日志 (Logging) 等基础设施。
*   **地位**: 它是目前 Unity 游戏 Mod 社区（Thunderstore, NexusMods）的绝对基石。

### 4.2 它是怎么工作的？(原理)
1.  **Doorstop**: BepInEx 利用了一个名为 `winhttp.dll` 或 `version.dll` 的劫持技术。当 Windows 启动游戏 exe 时，会优先加载游戏目录下的这个“假 DLL”。
2.  **注入**: 这个假 DLL 启动后，会拉起 BepInEx 的核心逻辑，然后再启动 Mono 虚拟机。
3.  **加载**: BepInEx 扫描 `BepInEx/plugins` 目录下的所有用户 DLL，并自动执行它们。

### 4.3 官方需要做什么？(Action Items)
其实，**官方什么都不用做**，BepInEx 就能工作。但为了让社区更舒服，建议做以下几点：

1.  **不要使用 IL2CPP**: IL2CPP 会把 C# 代码编译成 C++ 机器码，导致 metadata 丢失，BepInEx 极其难用（需要复杂的 Cpp2IL 转换）。**请务必使用 Mono 后端打包** (PC端)。
2.  **不要混淆代码**: 除非你有极高的商业机密，否则不要开代码混淆。混淆后 `DamageCalculator` 变成了 `A` 类，`Calculate` 变成了 `b` 方法，Modder 会疯掉。
3.  **保持 API 稳定**: 核心类（如 `Tower`, `Enemy`）的方法签名尽量不要频繁改动。如果改了，社区 Mod 会全部报错。

### 4.4 官方集成策略
如果你想更进一步，可以直接把 BepInEx 的功能“吸纳”进来：
*   **Steam 启动项**: 允许玩家添加 `-enable-mods` 参数，官方代码里检测到参数就加载 StreamingAssets 里的 DLL。
*   **提供 SDK**: 官方发布一个 `Vampirefall.Modding.dll`，里面全是接口 (`ITowerMod`, `IEnemyMod`)。Modder 引用这个 DLL 写代码，比用 Harmony 瞎猜要安全得多。

---

## 5. 避坑与安全

1.  **ID 管理**: 必须使用字符串 ID (`"tower_fire"`) 而不是枚举 (`Enum.TowerFire`)。枚举是编译死的，字符串是灵活的。
2.  **路径大小写**: Windows 不区分大小写，Linux/Android 区分。Mod 加载代码最好统一转小写处理路径。
3.  **沙盒**: 不要允许 Mod 访问 `System.IO` 里的删除/写入 API（除了 Mod 自己的临时文件夹），防止恶意 Mod 格式化玩家硬盘。

## 6. Steam Workshop 集成

如果你打算上 Steam，集成 Workshop 是最方便的。
*   使用 [Steamworks.NET](https://github.com/rlabrecque/Steamworks.NET)。
*   API: `SteamUGC.SubscribeItem()` 下载 Mod 到本地，然后你的 `ModManager` 去 Steam 的下载目录加载即可。

## 7. 总结

对于 *Vampirefall*:
1.  **第一步**: 确保你的 Config (Luban) 可以导出为 **JSON** 并在运行时读取。
2.  **第二步**: 编写一个 `ResourceManager`，支持从 StreamingAssets 加载 `.png` 覆盖默认 Sprite。
3.  **第三步 (进阶)**: 使用 **Mono** 编译构建，不要用 IL2CPP，为 Harmony/BepInEx 社区留一扇门。
