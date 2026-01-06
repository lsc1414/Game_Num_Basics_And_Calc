# 📂 Unity 项目文件夹结构规范 (Folder Structure Standards)

**文档目标：** 终结“按类型放”还是“按模块放”的争论。
**核心结论：** 采用 **“混合式架构” (Hybrid Approach)**。底层通用资源按类型，上层业务逻辑按模块。

---

## 1. ⚖️ 核心哲学：为什么纯“按类型”是错误的？

### ❌ 传统做法 (按类型 / Type-Based)
*   `Assets/Scripts/Player/PlayerController.cs`
*   `Assets/Prefabs/Player/Player.prefab`
*   `Assets/Textures/Player/Skin.png`
*   **痛点：** 当你想删除“玩家”功能，或者想把“玩家”功能迁移到另一个项目时，你需要跨越 5 个大文件夹去寻找相关文件。**高耦合，低内聚。**

### ✅ 现代做法 (按特性 / Feature-Based)
*   `Assets/Features/Player/`
    *   `Scripts/`
    *   `Prefabs/`
    *   `Art/`
*   **优势：** 删掉 `Player` 文件夹，整个功能就删干净了。

---

## 2. 🌳 黄金目录树 (The Golden Tree)

这是适用于中大型（塔防/RPG）项目的标准结构。

```text
Assets/
├── _Project/                   # 🔒 核心开发区 (加下划线置顶)
│   ├── Art/                    # 🎨 通用美术资源 (被多个模块复用的)
│   │   ├── Animations/
│   │   ├── Materials/          # 通用材质 (如全屏后处理)
│   │   ├── Models/             # 环境、建筑等静态模型
│   │   ├── Shaders/
│   │   ├── Textures/           # 地面、天空盒
│   │   └── UI/                 # 通用 UI (按钮、窗口底板、通用图标)
│   │   
│   ├── Audio/                  # 🔊 音频资源
│   │   ├── BGM/
│   │   └── SFX/                # 通用音效 (UI点击、升级成功)
│   │   
│   ├── Core/                   # 🧠 核心框架 (不依赖具体玩法)
│   │   ├── AudioSystem/
│   │   ├── EventSystem/
│   │   ├── SaveSystem/
│   │   └── UIManager/
│   │   
│   ├── Features/               # 🧩 玩法模块 (按功能切分 - 最重要!)
│   │   ├── Enemies/            # 敌人模块
│   │   │   ├── Bosses/
│   │   │   ├── Minions/
│   │   │   └── EnemySpawner.cs
│   │   ├── Towers/             # 塔模块
│   │   │   ├── ArcherTower/    # 包含该塔的 Prefab, Script, 独有贴图
│   │   │   └── MagicTower/
│   │   ├── Player/             # 玩家模块
│   │   └── Inventory/          # 背包系统
│   │   
│   ├── Scenes/                 # 🎬 场景文件
│   │   ├── Boot.unity          # 启动场景
│   │   ├── Menu.unity
│   │   └── Levels/
│   │   
│   └── Resources/              # 🚫 慎用！仅放 Logo 或 Loading 预制体
│
├── Plugins/                    # 🔌 第三方插件 (DoTween, Odin, Sirenix)
├── StreamingAssets/            # 🌊 流式资源 (视频、热更包)
└── Editor/                     # 🛠️ 存放编辑器工具脚本 (AssetNamingValidator.cs)
```

---

## 3. 📂 关键文件夹详解

### 3.1 `_Project` (根目录隔离)
**为什么要这一层？**
当你从 Asset Store 下载插件时，它们通常会直接安装在 `Assets` 根目录下。如果你把自己的代码也放在 `Assets` 根目录下，很快你的文件就会和插件文件混在一起。

*   **规则：** 所有的**原创**内容，必须放在 `_Project`（或 `_Game`）里。`Assets` 根目录只留给插件和系统文件夹。

### 3.2 `Features` (特性/模块目录)
这是“按模块放”哲学的核心。

*   **原则：** 如果一个资源（图片/音效）**只被**某个特定模块使用（例如：只有火法师塔用的火焰特效贴图），那么它就应该放在 `Features/Towers/FireTower/` 里面，而**不是** `Art/Textures` 里面。
*   **判定标准：**
    *   **独享资源** -> 放 `Features/[ModuleName]/`
    *   **共享资源** -> 放 `_Project/Art/` 或 `_Project/Audio/`

### 3.3 `Art` vs `Features`
很多美术同学习惯按 `Art/Characters`, `Art/Weapons` 提交资源。

*   **开发建议：**
    *   `Art` 文件夹作为“仓库”。美术提交的原始模型、贴图放在这里。
    *   `Features` 文件夹作为“组装车间”。程序在这里制作 Prefab。
    *   Prefab 引用 `Art` 里的模型。
    *   *如果项目较小，可以直接把美术资源也拖进 Features 里，不再保留 Art 文件夹，实现完全的模块化。*

### 3.4 `StreamingAssets`
*   **用途：** 这里的文不会被 Unity 压缩或打包成二进制，保持原始格式。
*   **场景：**
    *   PC 版游戏读取外部配置 (`.json`, `.xml`)。
    *   手机版播放视频 (`.mp4`)。
    *   WebGL 甚至不支持多线程读取这里。

---

## 4. 🚫 常见错误 (Bad Practices)

1.  **根目录混乱：**
    *   ❌ `Assets/Player.cs`
    *   ❌ `Assets/MyGameScript.cs`
    *   *后果：* 看起来像个 Demo，不像正经项目。

2.  **滥用 Resources：**

    *   ❌ `Assets/Resources/Textures/All_Game_Textures...`
    *   *后果：* 见《资产管理实战指南》，这是性能杀手。

3.  **拼写不一致：**

    *   ❌ `Assets/Script` (单数)
    *   ❌ `Assets/Prefabs` (复数)
    *   *规范：* 建议统用**复数** (Scripts, Prefabs, Models, Textures)。

4.  **空文件夹：**

    *   Git 默认不上传空文件夹。如果一定要保留结构，在里面放一个 `.keep` 文件。

---

## 5. 🤖 自动化建议

你可以写一个简单的 Editor 脚本，在项目初始化时自动创建这些文件夹，保证所有团队成员的结构一致。

```csharp
// 放在 Assets/Editor/ProjectSetup.cs
[MenuItem("Tools/Setup Project Folders")]
public static void CreateFolders() {
    string root = "Assets/_Project";
    Directory.CreateDirectory($"{root}/Art");
    Directory.CreateDirectory($"{root}/Audio");
    Directory.CreateDirectory($"{root}/Code");
    Directory.CreateDirectory($"{root}/Features");
    Directory.CreateDirectory($"{root}/Scenes");
    AssetDatabase.Refresh();
}
```