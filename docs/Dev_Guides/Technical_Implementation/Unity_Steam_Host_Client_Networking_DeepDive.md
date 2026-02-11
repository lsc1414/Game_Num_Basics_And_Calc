---
sidebarTitle: "Unity Steam Host+Client 深度研究"
title: "Unity Steam Host+Client 联网游戏深度研究"
---
> **摘要**：本文专门写给两类人：1）第一次做联网游戏的 Unity 开发者；2）已经有单机项目，准备无损升级到 Steam 联机的团队。核心目标是三件事：框架选型不踩雷、单机到联网思维切换、联网代码可插拔可回退。

## 1. 先定义问题：Steam Host+Client 到底是什么

Host+Client（Listen Server）指的是：一名玩家机器既跑客户端又跑权威主机逻辑，其他玩家作为客户端接入。

典型 Steam 结构：

1. 用 **Steam Lobby** 负责建房、搜房、邀请、准备状态同步。
2. 用 **Steam Networking Sockets / SDR** 负责实际实时数据传输。
3. 房主同时承担“主机 + 玩家”双角色。

这套模型的优点是部署成本低，适合 2-8 人 Coop；缺点是对房主机器质量和稳定性高度敏感。

---

## 2. 联网框架选型：不要先选“最强”，先选“最稳”

## 2.1 2026 常见技术栈对比（Unity + Steam 场景）

| 方案 | 学习成本 | 生态成熟度 | Steam 接入成本 | 适合规模 | 结论 |
| :-- | :-- | :-- | :-- | :-- | :-- |
| NGO (Netcode for GameObjects) + UTP | 低~中 | 高（Unity 官方） | 中（需接 Steam 传输层方案） | 小中型 Coop | **新团队首选** |
| FishNet | 中 | 高（社区活跃） | 中（有社区 Steam 方案） | 中型实时联机 | 对性能与控制要求更高可选 |
| Mirror | 中 | 高（老牌） | 低~中（FizzySteamworks 等） | 小中型 | 迭代快，工程化要自管 |
| Photon Fusion | 中 | 高（商用成熟） | 低（官方云服务路线） | 中大型 | 更偏“买成熟方案” |
| Netcode for Entities | 高 | 上升中 | 高 | 大规模高并发 | 不建议作为首个联网项目起步 |

## 2.2 给“没做过联网”的推荐顺序

1. 第一款联网项目：`NGO + UTP + Steam Lobby/Invite`。
2. 团队掌握同步与预测后：再评估 FishNet / Fusion。
3. 明确需要超大规模并发：再考虑 Netcode for Entities。

你要的不是“理论最强”，而是“团队 3 个月内能稳定上线”。

---

## 3. 单机 vs 联网：开发思维的硬切换（新手必读）

## 3.1 六个根本差异

| 维度 | 单机 | 联网 |
| :-- | :-- | :-- |
| 真实来源 | 本地就是事实 | 服务器/主机才是事实 |
| 输入处理 | 本地立即生效 | 本地预测 + 远端确认 |
| 时间系统 | `deltaTime` 就够 | 必须有网络 Tick 与时钟同步 |
| 随机数 | 想怎么用都行 | 必须可复现或由主机下发 |
| 错误恢复 | 读档即可 | 要有断线重连与状态修复 |
| 安全模型 | 允许自娱自乐修改 | 客户端默认不可信 |

## 3.2 初次联网最容易犯的错

1. 把本地 `Update` 逻辑直接当联网逻辑同步。
2. 用 `Random.Range` 直接参与战斗关键判定。
3. 用 RPC 到处发“结果”，而不是发“输入/请求”。
4. 没有主机迁移设计，房主退出就全房解散。

## 3.3 单机/联机 Cheatsheet 对照表（速查版）

### A. 研发设计对照

| 主题 | 单机做法 | 联机做法 | 迁移建议 |
| :-- | :-- | :-- | :-- |
| 核心逻辑入口 | 直接读 `Input` + 本地执行 | 输入命令化后上报主机/服务器 | 先定义 `PlayerCommand` 再改系统 |
| 胜负/伤害判定 | 客户端直接算 | 权威端计算，客户端只表现 | “输入上报，结果下发” |
| 随机数 | `Random.Range` 随便用 | 固定种子或权威下发 | 抽象 `IRandomProvider` |
| 时间步 | `deltaTime` 驱动 | 固定 Tick + 插值渲染 | 先把战斗逻辑改 fixed tick |
| 状态来源 | 本地内存是事实 | 主机/服务器状态是事实 | 建立状态版本号与快照 |
| 资源经济 | 本地扣费/加钱 | 服务器扣费并回包 | 客户端只做预览与 UI |
| Save/Load | 本地文件全量写 | 本地缓存 + 联网同步策略 | 增加 schemaVersion 与迁移器 |

### B. 程序实现对照

| 模块 | 单机代码习惯 | 联机代码习惯 | 坑点提示 |
| :-- | :-- | :-- | :-- |
| 移动 | `transform.position += ...` | 输入同步 + 状态校正 + 插值 | 不要每帧全量同步 Transform |
| 技能释放 | 直接调用 `Cast()` | 客户端请求 -> 权威校验 -> 广播事件 | 客户端本地先播前摇可减感知延迟 |
| 对象生成 | 本地 `Instantiate` | 由权威端决定 spawn 并同步 | “双生怪”通常是本地也 spawn 了 |
| RPC 使用 | 用 RPC 传所有数据 | RPC 传事件，状态走快照/变量 | RPC 滥用会难排障难回放 |
| 版本兼容 | 不关注协议版本 | 消息版本号 + build hash 校验 | 先拦截不兼容玩家入房 |
| 断线处理 | 弹窗返回主菜单 | 超时检测、重连、状态恢复 | 无重连就是线上大事故 |
| 日志 | 调试日志即可 | 带 `sessionId/tick/peerId` 结构化日志 | 不打结构化日志几乎无法追 bug |

### C. QA 测试对照

| 测试项 | 单机通过标准 | 联机通过标准 |
| :-- | :-- | :-- |
| 功能回归 | 单人流程可闭环 | 双开/多开均闭环，房主/房客都稳定 |
| 性能 | 本机 FPS 稳定 | Host 与 Client 同时运行时仍稳定 |
| 稳定性 | 崩溃可重启 | 断线重连成功率、重连耗时达标 |
| 弱网测试 | 可选 | 必做（高延迟/丢包/抖动） |
| 兼容测试 | 分辨率/设备 | NAT/地区/网络类型/版本兼容 |

### D. 发布运维对照

| 主题 | 单机发布 | 联机发布 |
| :-- | :-- | :-- |
| 发布策略 | 全量发布即可 | 分支灰度（candidate/canary/default） |
| 事故处理 | 回滚客户端版本 | 回滚客户端 + 协议兼容 + 房间善后 |
| 监控指标 | 崩溃率/FPS | 连通率、掉线率、重连成功率、RTT 分布 |
| 用户反馈 | 单机 BUG 修复 | 需附 sessionId/房间号/时间戳定位 |

> 快速记忆：  
> **单机关注“本地正确”**，**联机关注“全局一致 + 可恢复”**。

---

## 4. 无损插拔联网代码：核心架构范式

目标：让单机与联网共享同一套核心战斗逻辑，避免分叉维护。

## 4.1 三层拆分（必须做）

1. **Domain（纯游戏规则）**：不依赖 Unity Network API，不依赖 Steam API。
2. **Application（用例编排）**：输入命令、状态推进、回放与保存。
3. **Infrastructure（网络/平台）**：NGO/FishNet/Mirror/Steam 适配层。

## 4.2 关键接口（端口）示例

```csharp
public interface IGameSessionRuntime
{
    bool IsOnline { get; }
    bool IsHost { get; }
    ulong LocalPlayerId { get; }
    void SendCommand(in PlayerCommand cmd);
    event Action<PlayerCommand> OnCommandReceived;
}

public interface IDeterministicClock
{
    int Tick { get; }
    float TickDelta { get; }
}
```

实现两套运行时：

- `LocalSessionRuntime`：单机直连自身，零网络依赖。
- `SteamHostClientRuntime`：通过网络传命令，同样喂给 Domain 层。

这样单机/联网切换只是替换 runtime 绑定，不改核心规则代码。

## 4.3 组合根（Composition Root）示例

```csharp
public static class GameBootstrap
{
    public static void Build(bool online, bool isHost)
    {
        IGameSessionRuntime session = online
            ? new SteamHostClientRuntime(isHost)
            : new LocalSessionRuntime();

        IDeterministicClock clock = new FixedTickClock(60);
        var gameLoop = new BattleGameLoop(session, clock);
        gameLoop.Start();
    }
}
```

---

## 5. Steam Host+Client 推荐技术切片

## 5.1 最小闭环（MVP）

1. Steam 登录与 AppID 初始化
2. Lobby 建房/入房/邀请
3. 房主启动 Host，其他玩家启动 Client
4. 同步最小对象：玩家位置 + 一种攻击命令
5. 断线提示 + 重新入房按钮

## 5.2 再上生产

1. 主机权威判定（伤害、掉落、资源）
2. 客户端预测 + 回滚校正
3. Host Migration（或至少断房善后）
4. Steam Relay 路径稳定性验证
5. 版本校验与分支隔离（防止协议不兼容）

---

## 6. Host Migration：房主掉线时怎么“不炸房”

如果你做 Listen Server，不设计主机迁移，线上一定出现“房主一退全员白给”。

## 6.1 最小可行迁移方案

1. 常驻候选主机列表（按 RTT、硬件、稳定性排序）。
2. 主机每 `N` Tick 广播状态快照（压缩后）。
3. 房主断开时，候选主机接管并广播新 `HostToken`。
4. 客户端按 `Lobby + SessionToken` 重连新主机。

## 6.2 状态快照建议内容

- 当前 Tick
- 实体关键状态（HP、位置、Buff、CD）
- 随机种子状态
- 波次/房间规则状态

注意：快照不是每帧全量状态；要做增量或周期性关键帧，避免带宽爆炸。

---

## 7. “单机改联网”分阶段迁移路线（无损改造）

## Stage 1：清理单机隐形耦合

- 去掉直接读 `Input` 的战斗代码，改成 `PlayerCommand` 输入流。
- 把战斗随机统一到 `IRandomProvider`。
- 固定逻辑 Tick（例如 30/60Hz）。

## Stage 2：先做“假联网”

- 用 `LocalSessionRuntime` 模拟网络延迟与丢包。
- 命令先本地排队再消费，验证架构稳定性。

## Stage 3：接入真实网络

- 替换 runtime 到 `SteamHostClientRuntime`。
- Domain 层零改动，只改基础设施层。

## Stage 4：上线上防护

- 协议版本号 + 不兼容阻断
- 主机迁移或房间善后策略
- 崩溃恢复 + 重连逻辑

---

## 8. 专项坑点清单（高频事故）

## 8.1 同步与性能

| 坑点 | 现象 | 处理 |
| :-- | :-- | :-- |
| NetworkVariable 滥用 | 带宽上涨、抖动 | 高频对象改“命令 + 快照”混合 |
| Transform 全量同步 | 延迟高时拖影严重 | 关键状态同步 + 本地插值 |
| RPC 当状态机 | 难回放、难纠错 | RPC 只做事件，状态走快照 |
| `FixedUpdate` 与网络 Tick 脱节 | 命中不一致 | 明确单一权威 Tick |

## 8.2 Steam 实战

| 坑点 | 现象 | 处理 |
| :-- | :-- | :-- |
| 只测局域网不测 Relay | 上线后跨网连不上 | 必测不同 NAT/地区 |
| 房主退房无迁移 | 全员掉线 | 预设 host migration 或快速重建 |
| 版本不一致仍能入房 | 进房后异常 | 入房前做 build hash 校验 |
| 邀请只做 UI 不做状态 | 点邀请后卡死 | Lobby 状态机与超时回退 |

## 8.3 给新手的“反作弊最小集”

1. 经济与掉落只由主机/服务器决定。
2. 移动速度、技能 CD、伤害都做上限校验。
3. 客户端上报的是“输入”，不是“结果”。

---

## 9. 最佳实践：上线前 12 条硬性标准

- [ ] 单机与联网共用一套 Domain 规则代码
- [ ] 输入命令流可记录、可回放
- [ ] 全量网络消息有版本号与兼容策略
- [ ] 关键状态可快照恢复
- [ ] Host 退出有迁移或善后
- [ ] 跨 NAT / 跨区 / 高延迟完成回归测试
- [ ] 200ms 延迟 + 2% 丢包可玩
- [ ] 崩溃后可恢复到 Lobby 而非黑屏
- [ ] 关键经济逻辑权威端计算
- [ ] 有联机专项日志（sessionId / tick / peerId）
- [ ] 灰度分支可快速回滚
- [ ] QA 有“双开 + 弱网 + 断线重连”固定用例

---

## 10. 给 Vampirefall 的落地建议（Host+Client 版）

1. 首版本把联机目标压到 2-4 人 Coop，不要一开始追 8 人大房间。
2. 战斗核心先做“命令同步 + 主机权威结算”，再做复杂预测。
3. 把“局外成长/经济”与“局内战斗”拆协议，避免相互污染。
4. 优先做稳定性指标：连通率、掉线恢复率、重连耗时，再追求极限延迟。

---

## 11. 参考资料（官方/主文档）

- Unity Netcode for GameObjects：[https://docs.unity3d.com/Packages/com.unity.netcode.gameobjects@latest](https://docs.unity3d.com/Packages/com.unity.netcode.gameobjects@latest)
- Unity Netcode for Entities：[https://docs.unity3d.com/Packages/com.unity.netcode@latest](https://docs.unity3d.com/Packages/com.unity.netcode@latest)
- Unity Transport：[https://docs.unity3d.com/Packages/com.unity.transport@latest](https://docs.unity3d.com/Packages/com.unity.transport@latest)
- Unity Multiplayer Center：[https://docs.unity3d.com/Manual/com.unity.services.multiplayer.html](https://docs.unity3d.com/Manual/com.unity.services.multiplayer.html)
- Unity Relay 概念文档：[https://docs.unity.com/ugs/en-us/manual/relay/manual/introduction](https://docs.unity.com/ugs/en-us/manual/relay/manual/introduction)
- Steam Matchmaking & Lobbies：[https://partner.steamgames.com/doc/features/multiplayer/matchmaking](https://partner.steamgames.com/doc/features/multiplayer/matchmaking)
- SteamNetworkingSockets API：[https://partner.steamgames.com/doc/api/ISteamNetworkingSockets](https://partner.steamgames.com/doc/api/ISteamNetworkingSockets)
- Steam Datagram Relay：[https://partner.steamgames.com/doc/features/multiplayer/steamdatagramrelay](https://partner.steamgames.com/doc/features/multiplayer/steamdatagramrelay)
- Steamworks.NET：[https://steamworks.github.io/](https://steamworks.github.io/)
- Mirror 文档入口：[https://mirror-networking.gitbook.io/docs](https://mirror-networking.gitbook.io/docs)
- FishNet 文档入口：[https://fish-networking.gitbook.io/docs](https://fish-networking.gitbook.io/docs)
- Photon Fusion 文档入口：[https://doc.photonengine.com/fusion/current/getting-started/overview](https://doc.photonengine.com/fusion/current/getting-started/overview)
