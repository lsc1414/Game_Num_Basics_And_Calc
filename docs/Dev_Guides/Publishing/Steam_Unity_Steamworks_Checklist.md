---
sidebarTitle: "Unity Steamworks 核心功能开发清单 深度研究"
---

# 🧙‍♂️ Unity Steamworks 核心功能开发清单

## 📚 1. 理论基础 (Theoretical Basis)

### 核心定义

**Steamworks** 是 Valve 提供的一套服务和 API，允许开发者将游戏与 Steam 平台深度集成。对于 Unity 开发者，常用的封装库是 **Steamworks.NET** (更底层，功能全) 或 **Facepunch.Steamworks** (C# 风格，易用)。

### 核心架构

- **AppID**: 游戏的唯一标识符。所有 API 调用都需要在正确的 AppID 环境下运行。
- **Callback System (回调系统)**: Steam 的大多数操作（如解锁成就、上传云存档）是异步的。Steamworks 使用回调机制通知游戏操作结果。
- **Steam Overlay**: Steam 的覆盖界面，许多功能（如支付、邀请好友）依赖于此。

### 设计心理学

- **成就 (Achievements)**: 提供**外在动机 (Extrinsic Motivation)**，引导玩家尝试不同的玩法（如“只用一种塔通关”）。
- **排行榜 (Leaderboards)**: 满足**社会比较 (Social Comparison)** 需求，特别是对于无尽模式或高分挑战。
- **云存档 (Cloud Save)**: 提供**安全感**，确保玩家的投入（时间/金钱）不会因设备更换而丢失。

## 🛠️ 2. 实践应用 (Practical Implementation)

### Vampirefall 适配

结合塔防+肉鸽+Looter 的特性，我们需要关注以下模块：

1.  **成就系统**: 绑定 Rogue 的特殊挑战（如“由于运气不好连续获得 3 个诅咒”）。
2.  **统计数据**: 记录杀敌数、总伤害，用于解锁元游戏内容（Perks）。

3.  **排行榜**: 针对“无尽模式”的波数排名。

4.  **云存档**: 必须同步 `GameSave.json`。

### 数据结构建议 (C#)

建议封装一个 `SteamManager` 单例，管理所有 Steam 交互。

```json
// 成就配置示例 (JSON)
{
  "achievements": [
    {
      "apiName": "ACH_FIRST_BLOOD",
      "displayName": "第一滴血",
      "description": "在无尽模式中击败第一个Boss"
    },
    {
      "apiName": "ACH_FULL_BUILD",
      "displayName": "神装",
      "description": "装备全套传说级词条装备"
    }
  ]
}
```

```csharp
// C# 管理类伪代码
public class SteamAchvManager : Singleton<SteamAchvManager>
{
    // 定义成就常量，避免魔法字符串
    public const string ACH_FIRST_BLOOD = "ACH_FIRST_BLOOD";

    public void UnlockAchievement(string id)
    {
        if (!SteamManager.Initialized) return;

        bool achievementUnlocked;
        SteamUserStats.GetAchievement(id, out achievementUnlocked);

        if (!achievementUnlocked)
        {
            SteamUserStats.SetAchievement(id);
            // 必须调用 StoreStats 才能上传服务器
            SteamUserStats.StoreStats();
            Debug.Log($"解锁成就: {id}");
        }
    }
}
```

### 关键逻辑与伪代码

#### 1. 初始化 (Initialization)

必须在游戏启动的最早阶段（`Awake`）检查 Steam 客户端是否运行。

```csharp
private void Awake() {
    try {
        if (SteamAPI.RestartAppIfNecessary((AppId_t)480)) { // 480 是测试 AppID
            Application.Quit();
            return;
        }
    } catch (System.DllNotFoundException e) {
        Debug.LogError("Steamworks.dll missing.");
        Application.Quit();
    }
}
```

#### 2. 云存档同步 (Cloud Save Sync)

Vampirefall 的存档是单文件 `GameSave.json`，适合使用 **Steam Remote Storage**。

- **读取**: 游戏启动时，对比本地和云端文件的时间戳/大小。通常以云端为准（需询问玩家冲突解决策略）。
- **写入**: 每次 `SaveGame()` 时，同时调用 `SteamRemoteStorage.FileWrite`。

```csharp
public void SaveToCloud(string fileName, byte[] data) {
    if (SteamRemoteStorage.FileWrite(fileName, data, data.Length)) {
        Debug.Log("云存档上传成功");
    }
}
```

#### 3. 排行榜上传 (Leaderboard Upload)

在无尽模式结算时触发。

```csharp
// 查找排行榜 -> 上传分数
SteamUserStats.FindLeaderboard("EndlessWaveRank");
// 在回调 OnLeaderboardFindResult 中:
SteamUserStats.UploadLeaderboardScore(leaderboardHandle, k_ELeaderboardUploadScoreMethodKeepBest, currentWave);
```

### Unity 实现注意事项

- **Update 循环**: 必须在 `Update()` 中每帧调用 `SteamAPI.RunCallbacks()`，否则回调不会触发。
- **Thread Safety**: Steamworks API 必须在主线程调用。
- **Debug**: 本地调试时，确保 Steam 客户端已登录，并且根目录有 `steam_appid.txt` 文件。

## 🌟 3. 业界优秀案例 (Industry Best Practices)

### 案例 1: 《Slay the Spire》 (杀戮尖塔)

- **机制**: 详细的“历史记录”界面，不仅有分数，还有该局的卡组、遗物和路线。
- **优点**: 极大地增强了社区分享和复盘的价值。
- **借鉴**: Vampirefall 可以在排行榜详情中，包含玩家通关时的“核心词条”或“防御塔组合”。

### 案例 2: 《Hades》

- **机制**: 动态的“丰富存在 (Rich Presence)”。好友可以看到玩家当前在哪一层、拿着什么武器。
- **优点**: 增加社交互动感 ("哇，你已经打到第三层了？")。
- **借鉴**: 设置 Rich Presence 显示 "正在无尽模式 第 50 波 | 装备等级 15"。

### 案例 3: 《Vampire Survivors》

- **机制**: 成就直接解锁游戏内物品（武器/被动）。
- **优点**: 强绑定。成就不只是图标，由于其实际奖励。
- **借鉴**: 达成 "击杀 1000 个僵尸" 成就，解锁相关的 "不死族杀手" 词条库。

## 🔗 4. 参考资料 (References)

- 📄 **官方文档**: [Steamworks Documentation](https://partner.steamgames.com/doc/home)
- 🛠️ **插件库**: [Steamworks.NET GitHub](https://github.com/rlabrecque/Steamworks.NET)
- 📺 **教程**: [Unity Steamworks Integration (YouTube)](https://www.youtube.com/results?search_query=unity+steamworks+tutorial)
- 🌐 **指南**: [Valve's Guide to Achievements](https://partner.steamgames.com/doc/features/achievements)
