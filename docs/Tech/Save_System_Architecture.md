---
sidebarTitle: "存档与数据持久化架构"
title: "存档与数据持久化架构"
---
> **摘要**：本文档定义了游戏数据的存储结构、序列化方式及云存档策略。

## 1. 数据结构分类

我们将数据分为两类，分开存储：

### 1.1 用户账户数据 (User Profile) - _Meta Progression_

- **内容:** 天赋树解锁状态、全局货币 (Soul Shards)、解锁的图鉴、设置选项。
- **特点:** 必须高安全性，防止修改。
- **存储:**
    - 本地: 加密二进制文件 (`user.dat`).
    - 云端: Steam Cloud / PlayFab.

### 1.2 游戏存档数据 (Game Session) - _Run State_

- **内容:** 当前关卡进度、背包物品、塔的布局、当前血量。
- **特点:** 频繁读写（用于中断恢复），Roguelike 模式下死亡即删除。
- **存储:** JSON 或 Binary (`slot_0.save`).

## 2. 序列化与性能 (Serialization & Performance)

### 2.1 序列化方案

不使用 Unity 自带的 `PlayerPrefs` 或 `JsonUtility` (性能差且不支持复杂结构)。

- **推荐库:** `Newtonsoft.Json` (通用性强，Tag: `Dev`) 或 `MessagePack` (高性能，Tag: `Release`)。
- **接口设计:** 所有需存档的类实现 `ISaveable` 接口。

### 2.2 性能陷阱与优化

> [!NOTE] > **误区**: 很多开发者担心 JSON 序列化会导致手机发热。
> **事实**: 典型的 RPG 存档大小通常 < 500KB。即使每分钟全量序列化一次，CPU 开销也是微乎其微的。真正的性能杀手是 **主线程 I/O (Main Thread I/O)** 和 **GC Alloc**。

**优化策略:**

1.  **异步 I/O (Async I/O):** 序列化可以是同步的（为了保证数据一致性），但**写入磁盘必须是异步的**。
    ```csharp
    // 伪代码示例
    string json = JsonConvert.SerializeObject(data); // 几毫秒，主线程
    await File.WriteAllTextAsync(path, json);        // 几十毫秒，线程池，不卡顿 UI
    ```

2.  **脏标记 (Dirty Flags):** 只有当背包/数据发生实际变化时，才标记为 `IsDirty = true`。自动保存触发时，检测 `IsDirty`，如果为 `false` 则直接跳过。

3.  **增量存档 (Incremental Save) - _不推荐_:** 除非存档达到 MB 级别（如《缺氧》），否则**不要**尝试拆分文件存储单个道具。维护一致性（Transaction）的代价远高于全量重写的开销。

## 3. 存档安全性与原子性 (Atomicity & Safety)

> [!IMPORTANT] > **核心痛点:** 玩家在保存过程中强制关机/闪退，导致存档文件写入一半，由于 JSON 格式损坏无法读取，存档丢失。

### 3.1 原子写入模式 (Atomic Save Pattern)

必须严格遵循 **"Write-Flush-Move"** 流程：

1.  **写入临时文件:** 将数据写入 `save_slot_0.tmp`。
2.  **强制刷盘 (Flush):** 确保操作系统将缓冲区写入物理磁盘。

3.  **原子重命名:** 调用 `File.Move` 将 `save_slot_0.tmp` 替换为 `save_slot_0.dat`。

    - 如果第 1、2 步失败，原存档 `save_slot_0.dat` 依然完好。
    - 第 3 步是原子的（在大多数现代文件系统上），要么成功，要么失败，不会出现“只有一半”的情况。

### 3.2 备份策略 (Rotation)

- 保留 `slot_0.dat` 和 `slot_0.bak` (上一次成功的存档)。
- 加载失败时，自动尝试加载 `.bak` 并提示玩家。

## 4. 版本控制与迁移 (Versioning & Migration)

### 4.1 版本号设计

存档根节点必须包含 `ConfigVersion` 或 `SchemaVersion`。

```json
{
  "SchemaVersion": 5,
  "Timestamp": 1709876543,
  "Data": { ... }
}
```

### 4.2 迁移流水线 (Migration Pipeline)

随着游戏更新，数据结构必然改变（如：删除了个属性，改了个字段名）。
**禁止**在新版本代码中保留旧版本的兼容逻辑（这会导致代码变成屎山）。
**推荐**使用迁移器模式：

- **当前代码版本:** 5
- **存档版本:** 3
- **流程:**
    1.  检测 Version 3 < 5。
    2.  运行 `Migrator_3_to_4.Execute(jsonDoc)`。

    3.  运行 `Migrator_4_to_5.Execute(jsonDoc)`。

    4.  反序列化为当前对象。

> [!WARNING] > **降级保护:** 严格**禁止**旧版本客户端加载新版本存档（如 v4 客户端加载 v5 存档）。应直接报错提示“请更新游戏”。

## 5. 反作弊与校验 (Anti-Cheat Basics)

虽然是单机为主，但为了维护排行榜公正性：

1.  **哈希签名 (HMAC):** 存档文件末尾附加内容的 SHA256 签名（加盐）。加载时比对。
2.  **简单混淆:** 避免明文存储 `gold: 99999`，可存为 Base64 或 XOR 处理后的值，防止小学生用记事本修改。

3.  **注意:** 不要过度设计，本地反作弊永远防不住有心人，防君子不防小人。

## 6. 存档文件结构示例 (Schema)

```json
{
  "Meta": {
    "Version": 10,
    "PlayTime": 3600,
    "Hash": "a1b2c3d4..."
  },
  "Player": {
    "Stats": {"Hp": 100, "Gold": 500},
    "Inventory": [...]
  },
  "World": {
    "Wave": 15,
    "Seed": 123456
  }
}
```
