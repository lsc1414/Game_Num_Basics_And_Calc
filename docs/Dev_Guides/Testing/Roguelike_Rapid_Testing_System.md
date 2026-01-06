# 🧙‍♂️ 肉鸽组合快速测试系统深度研究

## 📚 1. 理论基础 (Theoretical Basis)

### 1.1 核心定义：组合爆炸与确定性验证
在 Roguelike (+ Tower Defense + Looter) 游戏中，核心乐趣来源于**"构建 (Build)"**。然而，随着词条（Affixes）、天赋（Perks）、装备（Items）的增加，可能的组合数量呈指数级增长。

*   **组合爆炸 (Combinatorial Explosion)**: 假设有 100 种天赋，玩家能选 10 种，组合数是天文数字。手动测试每一种组合的化学反应是不现实的。
*   **确定性验证 (Deterministic Verification)**: 开发者的目标不是测试所有组合，而是**快速构建特定场景**，验证机制的预期行为（例如：“当玩家拥有[多重投射]且装备[爆炸火花]时，是否会引发性能卡顿？”）。

### 1.2 为什么需要“快速”？ (Why Speed Matters)
*   **心流阻断**: 如果策划想要测试一个新词条，需要跑图 10 分钟才能随机刷到，测试效率极低。
*   **边缘情况 (Edge Cases)**: 很多 Bug 只有在极端数值或特定罕见组合下才会触发。
*   **回归测试**: 每次修改伤害公式，都需要快速验证旧的 Build 是否崩坏。

---

## 🛠️ 2. 实践应用 (Practical Implementation)

### 2.1 快速构建系统 (Instant Build System)

在 Vampirefall 中，我们通过以下三层架构实现快速构建：

#### A. 调试控制台 (Debug Console)
最基础的层级，通过命令直接修改当前状态。

```csharp
// 示例：Vampirefall 调试指令集
/add_perk [perk_id] [level]      // 添加特定天赋
/remove_perk [perk_id]           // 移除天赋
/set_stat [stat_name] [value]    // 强制修改属性(如暴击率)
/spawn_enemy [enemy_id] [count]  // 生成特定敌人
/god_mode [bool]                 // 无敌模式(测试受击触发用)
```

#### B. Build 代码化 (Build Strings)
借鉴卡牌游戏的卡组代码，将一个完整的 Build 序列化为字符串。

*   **用途**: 策划 A 发现一个强力组合，复制字符串发给程序 B，B 粘贴即可瞬间复现该状态。
*   **数据结构**:
    ```json
    {
      "version": "1.0",
      "hero_id": "vampire_lord_01",
      "level": 20,
      "perks": ["multishot:3", "chain_lightning:1", "blood_pact:1"],
      "inventory": ["sword_legendary_01", "armor_epic_02"]
    }
    ```
    *压缩后*: `VF1.0|VD01|L20|P:MS3,CL1,BP1|I:SL01,AE02`

#### C. 预设存档槽 (Preset Save Slots)
在开发版本的主菜单提供 "Load Preset" 功能，预设多种典型环境：

*   **Glass Cannon**: 极高攻，极低防（测试秒杀逻辑）。
*   **Tank**: 极高防，高回血（测试受击回能、反伤）。
*   **Proc Machine**: 高频触发（测试特效性能、显卡压力）。

### 2.2 终极木头人系统 (The Ultimate Target Dummy)

木头人不能只是一个血量无限的沙袋，它必须是**可配置的测试环境**。

#### A. 木头人配置面板 (Dummy Configuration)
在训练场（Hub World）中，玩家/开发者可以与控制台交互，设定木头人的属性：

*   **防御属性 (Defense)**:
    *   `0 甲` vs `高甲` (测试穿透/破甲)。
    *   `0 抗` vs `火抗 75%` (测试元素穿透)。
*   **行为逻辑 (Behavior)**:
    *   **Idle**: 纯挨打，测试 DPS。
    *   **Attack (0 Damage)**: 以固定频率攻击玩家，但造成 0 伤害。**关键功能**，用于测试 "闪避后触发"、"受击触发"、"格挡触发" 的词条。
    *   **Move**: 移动靶，测试弹道追踪性能。
*   **数量 (Crowd)**:
    *   生成 1 个 vs 生成 50 个 (测试 AoE 效率和性能)。

#### B. 实时 DPS 统计 (Real-time DPS Meter)
在木头人上方或屏幕侧边显示详细战斗数据：

> **Combat Log**
> *   **DPS**: 15,400 (Peak: 22,000)
> *   **Last Hit**: 1,200 (Critical!)
> *   **Damage Breakdown**:
>     *   Physical: 40%
>     *   Fire: 30% (Ignite: 10%)
>     *   Proc (Lightning): 20%

#### C. 快速重置 (Instant Reset)
一键清除所有 DoT (Damage over Time) 状态，回满血，重置 DPS 统计。由于 DoT 伤害计算复杂，测试爆发伤害时必须能快速清空环境。

### 2.3 快速修改配置 (Hot-Reload Configs)

利用 Luban 和 Odin Inspector 实现运行时配置热重载。

*   **流程**:
    1.  策划在 Excel/JSON 中修改装备数值。
    2.  运行 `gen_data.bat`。
    3.  Unity 监听到文件变动，自动重载内存中的表格数据（无需重启游戏）。
    4.  通过 EventBus 通知 UI 和 实体 刷新数值。

```csharp
// 伪代码：配置热重载监听
public class ConfigReloader : MonoBehaviour {
    void OnEnable() {
        FileWatcher.Watch("StreamingAssets/Data", OnDataChanged);
    }

    void OnDataChanged() {
        GameTables.Reload(); // 重新加载 Luban 表
        EventManager.Trigger(new OnConfigReloadedEvent());
        Debug.Log("♻️ Configs Hot-Reloaded!");
    }
}
```

---

## 🌟 3. 业界优秀案例 (Industry Best Practices)

### 3.1 Hades (黑帝斯)
*   **Skelly (骷髅沙袋)**:
    *   **优点**: 永远在那，打死后快速复活，不废话。它是一个“角色”，有性格，通过对话解锁功能，沉浸感极强。
    *   **借鉴点**: 不要把测试工具做得太像调试软件，尽量包装进游戏世界观。
*   **Mirror of Night (夜之镜)**:
    *   允许玩家随时重洗天赋，方便尝试不同 Build。

### 3.2 Warframe (星际战甲) - Simulacrum (幻影装置)
*   **机制**: 玩家可以生成任何已扫描过的敌人。
*   **神级功能**:
    *   **Pause AI**: 让敌人不动，方便爆头测试。
    *   **Invincibility**: 玩家无敌，测试玻璃大炮 Build 而不死。
    *   **Enemy Level**: 只有在这里能测试 9999 级敌人的护甲减伤曲线。
*   **借鉴点**: 对于长线运营游戏（Looter），必须提供一个能模拟后期高难环境的场所。

### 3.3 The Binding of Isaac (以撒的结合)
*   **Modding Console**:
    *   极其强大的控制台，`/g item_name` 直接获得物品。
    *   社区依托此功能挖掘了大量深层机制。
*   **缺点**: 需要开启 Debug 模式，且开启后无法获得成就（防作弊）。

---


## 🧩 4. 深度技术实现 (Deep Tech Implementation)

### 4.1 Build Code 序列化算法 (Build Code Serialization)

要实现类似《炉石传说》或《流放之路》的卡组/Build 代码，核心是**将复杂对象映射为紧凑字符串**。

#### A. 算法步骤
1.  **映射 (Mapping)**: 建立一个全局静态字典，将长 ID 映射为短整型或 Base64 字符。
    *   `"Perk_Thunder_Strike_Level_Max"` (30 chars) -> `1042` (Integer) -> `A2` (Base64)
2.  **分割 (Delimiting)**: 使用特定字符分割不同模块。
    *   `|` 分割大模块 (英雄、天赋、装备)。
    *   `;` 分割列表项。
    *   `:` 分割键值对 (ID:等级)。
3.  **压缩 (Compression)**:
    *   **Varint**: 对于数字存储，使用 Varint 编码（小数字占用更少字节）。
    *   **RLE (Run-Length Encoding)**: 虽不常用，但如果有重复物品 `[A, A, A, A, B]` -> `4A1B`。
4.  **校验 (Checksum)**: 在末尾添加 CRC32 或简单的 Hash，防止玩家输错代码导致崩端。

#### B. C# 代码参考
```csharp
public static class BuildSerializer {
    // 示例输出: "VF1$H:1,L:20$P:3,4,12$I:40:2$C:9A"
    // VF1=版本, H=Hero, P=Perks, I=Items(ID:Count), C=Checksum
    
    public static string Serialize(PlayerData data) {
        StringBuilder sb = new StringBuilder();
        sb.Append("VF1$"); // Version Header
        
        // 1. Hero
        sb.Append($"H:{GlobalIDMap.ToInt(data.HeroId)}");
        sb.Append($",L:{data.Level}$");
        
        // 2. Perks (只存 ID)
        sb.Append("P:");
        var perkCodes = data.Perks.Select(p => GlobalIDMap.ToInt(p.Id).ToString());
        sb.Append(string.Join(",", perkCodes));
        sb.Append("$");

        // 3. Checksum
        string raw = sb.ToString();
        sb.Append($"C:{ComputeHash(raw)}");
        
        return Convert.ToBase64String(Encoding.UTF8.GetBytes(sb.ToString()));
    }
}
```

---

### 4.2 全状态快照系统 (Snapshot Dump & Restore)

用户报 Bug 时一键 Dump 并在编辑器还原，是顶级开发体验。这个系统的开发难度取决于你的**还原精度**。

#### 📊 难度分级 (Complexity Tiers)

|       级别       |       还原精度       |       适用场景       |       开发难度       |       描述       |
|       :---       |       :---       |       :---       |       :---       |       :---       |
|       **L1**       |       **静态数据 (Static)**       |       配装/面板 Bug       |       ⭐ (简单)       |       仅保存玩家身上的装备、天赋、属性。本质上就是“存档”。       |
|       **L2**       |       **战斗开局 (Session)**       |       进场报错/初始掉落       |       ⭐⭐ (中等)       |       保存 L1 + **关卡 Seed** + 当前波次索引。能还原出一模一样的怪和地图，但**不还原**你刚才打了一半的战况。       |
|       **L3**       |       **完美现场 (Exact State)**       |       AI 寻路/物理卡死       |       ⭐⭐⭐⭐⭐ (地狱)       |       需要还原所有怪物的坐标、血量、Buff、飞在空中的子弹位置。除非是 ECS 架构或确定性帧同步，否则极难实现。       |

#### 🛠️ L2 级别的实现方案 (推荐)
对于大多数 Roguelike，还原到**“进入该房间的那一刻”**通常就足够复现 Bug 了。

**1. 数据结构 (DumpData)**
```json
{
    "meta": { "timestamp": 12345678, "game_version": "0.5.2" },
    "player": { ... }, // 完整的玩家存档数据
    "level_state": {
        "chapter_id": "chapter_2_swamp",
        "current_wave": 5,
        "rng_sseed": 998244353, // 关键：随机数种子
        "difficulty_factor": 1.5
    }
}
```

**2. 只有“一键 Dump”是不够的，关键是“一键 Restore”**
你需要给编辑器写一个工具，跳过主菜单流程，直接根据 Dump 启动战斗场景。

**编辑器工作流**:

1.  右键 `bug_report.dump` -> "Play in Editor"。
2.  Unity 启动，进入 `Bootstrap` 场景。
3.  `Bootstrap` 检测到启动参数或静态变量中持有 Dump 数据。
4.  跳过主菜单，直接初始化 `GameManager`。
5.  `MapGenerator` 使用 Dump 中的 `rng_seed` 重新生成地图（保证地形一致）。
6.  `EnemyManager` 模拟快进到第 5 波（或者直接设置波次索引）。

**代码片段：编辑器入口**
```csharp
#if UNITY_EDITOR
[UnityEditor.MenuItem("Debug/Load Dump From Clipboard")]
public static void LoadDump() {
    string json = GUIUtility.systemCopyBuffer;
    var dump = JsonUtility.FromJson<DumpData>(json);
    
    // 设置一个全局标记，告诉游戏启动时不要走正常流程
    DebugContext.CurrentDump = dump;
    EditorApplication.isPlaying = true;
}
#endif

// 游戏初始化逻辑
void Start() {
    if (DebugContext.CurrentDump != null) {
        RestoreFromDump(DebugContext.CurrentDump);
    } else {
        StartNormalGame();
    }
}
```

#### 💡 开发建议
*   **不要过度追求 L3**: 还原每一颗子弹的位置通常是不划算的。只要能还原出 **Player Build + Map Seed + Enemy Wave**，95% 的数值和机制 Bug 都能复现。
*   **JSON 甚至可以加密**: 让玩家在 Discord 上发给你一串加密乱码，你丢进编辑器就能跑，非常酷且能保护存档结构不被轻易修改。

### 4.3 L2 级别快照系统实战指南 (L2 Snapshot Implementation Guide)

L2 级别的目标是**“只要提供由于同一个 Seed 生成的关卡，以及完全一致的玩家属性，就能复现 99% 的战斗逻辑问题”**。

#### A. 核心数据结构 (The Data Model)
我们需要定义一个能完全描述“战前状态”的类。

```csharp
[System.Serializable]
public class GameSnapshot {
    // 1. 元数据
    public string Version = "1.0";
    public long Timestamp;
    
    // 2. 玩家状态 (极其重要：不仅是静态属性，还有动态状态)
    public PlayerDump Player;
    
    // 3. 关卡环境 (复现现场的核心)
    public EnvironmentDump Env;
}

[System.Serializable]
public class PlayerDump {
    // 基础
    public string HeroId; 
    public int Level;
    
    // 构建 (Build)
    public List<string> InventoryItemIds; // 装备
    public List<string> ActivePerkIds;    // 词条
    
    // 运行时状态 (进房时的状态)
    public float CurrentHp;          // 也许进房时就只有 10% 血
    public float CurrentEnergy;
    public List<string> ActiveBuffs; // 只有进房时带入的 Buff 才算 (如药水效果)
}

[System.Serializable]
public class EnvironmentDump {
    public string ChapterId;      // 比如 "Level_1_3"
    public int WaveIndex;         // 当前是第几波
    public int RngSeed;           // 【核心】地图和刷怪的随机种子
    public float DifficultyScale; // 难度系数
    
    // 进阶：如果有关卡特效
    public List<string> MapAffixes; // 例如 "地面打滑", "敌人死亡爆炸"
}
```

#### B. 劫持初始化流程 (Hijacking Initialization)

普通游戏的启动流程漫长且繁琐（Splash -> MainMenu -> LoadSave -> Battle）。我们需要**“短路”**这个过程。

**Step 1: 创建调试上下文 (DebugContext)**
这是一个既能在 Editor 运行，也能在 Runtime 访问的静态桥梁。

```csharp
// DebugContext.cs
public static class DebugContext {
    // 这里存储待恢复的快照
    // 如果为 null，说明是正常启动；如果不为 null，说明是 Debug 启动
    public static GameSnapshot SnapshotToLoad; 
}
```

**Step 2: 编辑器入口 (The Editor Tool)**
策划/程序复制了一段 JSON，点击菜单，直接拉起游戏。

```csharp
// SnapshotLoader.cs (放在 Editor 文件夹)
using UnityEditor;
using UnityEngine;

public static class SnapshotLoader {
    [MenuItem("Tools/🐛 Debug/Run From Clipboard Snapshot")]
    public static void RunSnapshot() {
        // 1. 获取剪贴板内容
        string json = GUIUtility.systemCopyBuffer;
        if (string.IsNullOrEmpty(json)) {
            Debug.LogError("Clipboard is empty!");
            return;
        }

        try {
            // 2. 解析数据
            var snapshot = JsonUtility.FromJson<GameSnapshot>(json);
            
            // 3. 注入上下文
            DebugContext.SnapshotToLoad = snapshot;
            
            // 4. 打开并运行战斗场景
            // 注意：不要加载 MainMenu，直接加载 BattleScene
            UnityEditor.SceneManagement.EditorSceneManager.OpenScene("Assets/Scenes/BattleScene.unity");
            EditorApplication.isPlaying = true;
            
            Debug.Log($"🚀 Launching snapshot from Seed: {snapshot.Env.RngSeed}");
        } catch (System.Exception e) {
            Debug.LogError($"Failed to parse snapshot: {e.Message}");
        }
    }
}
```

**Step 3: 游戏管理器适配 (GameManager Adaptation)**
在战斗场景的入口脚本（如 `GameManager` 或 `BattleBootstrap`）中处理劫持逻辑。

```csharp
// GameManager.cs
void Awake() {
    if (DebugContext.SnapshotToLoad != null) {
        // A. 走调试流程
        InitializeFromSnapshot(DebugContext.SnapshotToLoad);
        
        // 重要：用完后清空，防止下次正常停止播放后，再次启动时还残留数据
        DebugContext.SnapshotToLoad = null; 
    } else {
        // B. 走正常流程 (读取本地存档、生成新关卡...)
        InitializeNormalGame();
    }
}

void InitializeFromSnapshot(GameSnapshot snap) {
    Debug.LogWarning("⚠️ Game Initialized from Debug Snapshot!");

    // 1. 还原随机数生成器 (最关键的一步)
    // 所有的怪物生成、掉落、地图构造都必须依赖这个种子
    RandomService.Init(snap.Env.RngSeed); 

    // 2. 还原玩家
    var player = PlayerFactory.Create(snap.Player.HeroId);
    player.SetStats(snap.Player.Level, snap.Player.InventoryItemIds);
    player.SetHp(snap.Player.CurrentHp); // 还原残血状态
    
    // 3. 还原环境
    LevelManager.LoadLevel(snap.Env.ChapterId);
    WaveManager.JumpToWave(snap.Env.WaveIndex); // 跳过前几波
    
    // 4. 应用特殊词条
    AffixManager.ApplyMapAffixes(snap.Env.MapAffixes);
}
```

#### C. 如何获取 Seed？ (The Seed Strategy)
要让 L2 方案生效，你的游戏中必须显式管理所有的随机性。

*   **❌ 错误做法**: 到处写 `UnityEngine.Random.Range(0, 100)`。这样无法通过一个种子还原所有行为。
*   **✅ 正确做法**: 封装一个 `RandomService`。
    ```csharp
    public static class RandomService {
        private static System.Random _rng;
        
        public static void Init(int seed) {
            _rng = new System.Random(seed);
            UnityEngine.Random.InitState(seed); // 同时重置 Unity 的随机状态
        }
        
        // 所有的业务逻辑都调用这个
        public static int Range(int min, int max) {
            return _rng.Next(min, max);
        }
    }
    ```

只要 Seed 一致，地图生成的障碍物位置、第一波刷出的怪物类型、怪物掉落的物品，就应该和报 Bug 时**完全一致**。

## 🔗 4. 参考资料 (References)

*   **GDC**: [Building the Tools for a Roguelike (Hades)](https://www.youtube.com/watch?v=FacowkSn7C4)
*   **Blog**: [Deterministic Testing in Procedural Games](https://www.gamasutra.com/blogs/...)
*   **Tools**: [Odin Inspector](https://odininspector.com/) (用于创建游戏内调试面板)

