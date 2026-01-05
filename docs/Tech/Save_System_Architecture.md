# 💾 存档与数据持久化架构 (Save System Architecture)

本文档定义了游戏数据的存储结构、序列化方式及云存档策略。

---

## 1. 数据结构分类

我们将数据分为两类，分开存储：

### 1.1 用户账户数据 (User Profile) - *Meta Progression*
*   **内容:** 天赋树解锁状态、全局货币 (Soul Shards)、解锁的图鉴、设置选项。
*   **特点:** 必须高安全性，防止修改。
*   **存储:** 
    *   本地: 加密二进制文件 (`user.dat`).
    *   云端: Steam Cloud / PlayFab.

### 1.2 游戏存档数据 (Game Session) - *Run State*
*   **内容:** 当前关卡进度、背包物品、塔的布局、当前血量。
*   **特点:** 频繁读写（用于中断恢复），Roguelike 模式下死亡即删除。
*   **存储:** JSON 或 Binary (`slot_0.save`).

## 2. 序列化方案 (Serialization)

不使用 Unity 自带的 `PlayerPrefs` 或 `JsonUtility` (性能差且不支持复杂结构)。

*   **推荐库:** `Newtonsoft.Json` (开发期方便调试) 或 `MessagePack` / `Protobuf` (发布期高性能)。
*   **接口设计:** 所有需存档的类实现 `ISaveable` 接口。

```csharp
public interface ISaveable {
    object CaptureState();
    void RestoreState(object state);
}
```

## 3. 存档文件结构 (Schema)

```json
{
  "version": "1.0.2",
  "timestamp": 1701234567,
  "player": {
    "stats": {"hp": 100, "gold": 500},
    "inventory": [...]
  },
  "world": {
    "wave_index": 5,
    "towers": [
      {"id": "T01", "pos": {"x":10, "y":5}, "tier": 2}
    ]
  }
}
```

## 4. 反作弊与校验 (Anti-Cheat Basics)

虽然是单机为主，但为了维护排行榜公正性：

1.  **哈希校验 (Hash Check):** 存档文件末尾附加内容的 SHA256 签名。加载时比对，防止简单的文本编辑。
2.  **数据混淆 (Obfuscation):** 关键数值（如金币）在内存中不直接存 `int`, 而是存 `XorInt` 结构，防止 Cheat Engine 简单搜索。

## 5. 存档流程 (Save/Load Flow)

1.  **自动保存 (Auto-Save):**
    *   每波结束时。
    *   进入下一层关卡时。
    *   *注意:* 避免在战斗激烈时保存，防止卡顿。
2.  **版本迁移 (Migration):**
    *   存档头部包含 `version` 字段。
    *   加载时检测版本，如果旧于当前版本，运行 `MigrationService` 进行数据补全或转换。

