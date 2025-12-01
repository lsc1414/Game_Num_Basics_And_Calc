# 📈 全局埋点实战指南：用数据上帝视角“看”游戏

**文档目标**：定义 *Vampirefall* 的全套数据埋点方案。通过构建完整的数据闭环，让开发团队能回答：“玩家在干什么？玩家在哪流失？玩家为什么不付费？”

---

## 1. 埋点设计哲学 (Philosophy)

不要收集垃圾数据。每一个埋点必须对应一个**分析目的**。

*   **❌ 错误做法**：`Button_Clicked` (无参数)。不知道点的哪个按钮，点了有什么用。
*   **✅ 正确做法**：`UI_Interaction` { `element_id`: "StartGame", `screen`: "MainMenu", `time_spent`: 5.2s }。

### 1.1 通用参数 (Common Parameters)
所有事件必须携带的“元数据”，用于切片分析：
*   `user_id`: 唯一标识。
*   `device_model`: 机型 (如 iPhone 15 Pro)。
*   `app_version`: 版本号 (如 0.8.1)。
*   `os_version`: 操作系统。
*   `network_type`: WIFI / 5G / Offline。
*   `player_level`: 玩家当前账号等级。

---

## 2. 核心生命周期埋点 (User Journey)

把握玩家从“下载”到“卸载”的全过程。

### 2.1 启动与系统 (System)
| Event Name | 参数 (Params) | 触发时机 | 分析目的 |
| :--- | :--- | :--- | :--- |
| `sys_app_launch` | `is_cold_start` (冷/热启动) | 游戏进程开始 | 计算 DAU (日活)。 |
| `sys_device_info` | `cpu`, `ram`, `gpu`, `screen_res` | 首次启动/每日首次 | 了解机型分布，制定性能预算。 |
| `sys_performance` | `avg_fps`, `min_fps`, `memory_peak` | 关卡结束/每5分钟 | 监控性能退化，定位卡顿机型。 |
| `sys_error` | `error_msg`, `stack_trace`, `scene` | 发生 Exception | 线上 Bug 监控 (CrashRate)。 |

### 2.2 新手引导 (Tutorial)
**流失率最高的阶段**，必须埋得最细，精确到每一步。

| Event Name | 参数 | 触发时机 | 分析目的 |
| :--- | :--- | :--- | :--- |
| `guide_step` | `step_id` (101, 102...), `duration` | 完成某一步引导 | **漏斗分析**：看玩家在哪一步卡住/退出了。 |
| `guide_finish` | `total_time` | 引导全部完成 | 计算新手转化率。 |
| `guide_skip` | `step_id` | 点击“跳过” | 验证引导是否太罗嗦。 |

---

## 3. 战斗与关卡埋点 (Core Gameplay)

把握核心玩法的平衡性与难度曲线。

### 3.1 关卡流程
| Event Name | 参数 | 触发时机 | 分析目的 |
| :--- | :--- | :--- | :--- |
| `level_start` | `level_id`, `difficulty`, `hero_id`, `hero_power` | 点击开始战斗 | 关卡热度统计。 |
| `level_finish` | `level_id`, `result` (Win/Lose/Quit), `duration`, `hp_percent` | 战斗结束 | **通过率分析**：如果某关通过率 < 20%，说明数值崩了。 |
| `player_die` | `level_id`, `killer_id`, `killer_type`, `pos_x`, `pos_y` | 玩家死亡 | **死亡热力图**：看玩家经常死在哪里，死在谁手里。 |

### 3.2 战斗细节 (Combat)
*注意：高频事件（如“造成伤害”）不要直接上报，而是在关卡结束时上报汇总数据。*

| Event Name | 参数 | 触发时机 | 分析目的 |
| :--- | :--- | :--- | :--- |
| `combat_summary` | `total_dmg_dealt`, `total_dmg_taken`, `max_combo`, `mvp_skill_id` | 关卡结束 (Win/Lose) | 验证 Build 强度，发现超模技能。 |
| `skill_select` | `skill_id`, `reroll_count` | 肉鸽三选一环节 | 统计技能选取率 (Pick Rate)，平衡技能强弱。 |
| `buff_acquired` | `buff_id`, `source` (Drop/Shop) | 获得强力 Buff | 关联分析：拿到这个 Buff 的玩家胜率提高了多少？ |

---

## 4. 经济与成长埋点 (Economy & Meta)

监控通货膨胀，抓捕作弊者。

### 4.1 资源产出与消耗 (Source & Sink)
这是经济系统的总账。

| Event Name | 参数 | 触发时机 | 分析目的 |
| :--- | :--- | :--- | :--- |
| `eco_resource_change` | `currency_type` (Gold/Gem), `amount` (+/-), `balance` (变动后余额), `reason` | 货币变动 | **通胀监控**：如果 `balance` 曲线指数级上升，说明产出失控。 |

**Reason 枚举 (示例)**:
*   `Source`: `LevelWin`, `QuestReward`, `ShopPurchase`, `MailGift`
*   `Sink`: `UpgradeHero`, `BuyItem`, `Revive`, `RerollSkill`

### 4.2 养成 (Progression)
| Event Name | 参数 | 触发时机 | 分析目的 |
| :--- | :--- | :--- | :--- |
| `meta_upgrade` | `talent_id`, `new_level`, `cost` | 升级局外天赋 | 了解玩家的加点偏好。 |
| `item_equip` | `item_id`, `slot_index` | 穿戴装备 | 统计装备使用率。 |

---

## 5. 商业化埋点 (Monetization)

对于独立/商业游戏，这是吃饭的家伙。

| Event Name | 参数 | 触发时机 | 分析目的 |
| :--- | :--- | :--- | :--- |
| `iap_store_open` | `entry_point` (MainMenu/Pause/Die) | 打开商店界面 | 曝光率 (Impression)。 |
| `iap_product_click` | `product_id`, `price` | 点击某个商品 | 点击率 (CTR)。 |
| `iap_checkout` | `product_id`, `order_id` | 点击购买按钮（唤起支付） | **支付中断率**：点了买但没付钱，可能是支付渠道挂了。 |
| `iap_purchase_verify` | `product_id`, `order_id`, `status` (Success/Fail) | 支付回调 | 实际收入 (Revenue)。 |
| `ad_show` | `ad_type` (Reward/Interstitial), `placement` (Revive/DoubleGold) | 广告开始播放 | 广告变现效率。 |
| `ad_complete` | `ad_type`, `reward_claimed` | 广告播放完成 | 完播率。 |

---

## 6. 数据分析实战案例 (Case Studies)

数据本身没有价值，**洞察 (Insight)** 才有价值。以下是经典的分析模型。

### 🔍 案例 A：精准定位流失 (Churn Analysis)
*   **现象**：次日留存率 (Day 1 Retention) 只有 15%，远低于业界标准的 35%。
*   **分析步骤**：
    1.  **漏斗图 (Funnel)**：绘制 `sys_app_launch` -> `level_start(1)` -> `level_finish(1)` -> `level_start(2)`。
    2.  **发现断点**：发现 40% 的玩家在 `level_finish(1)` 后没有进入第 2 关。
    3.  **下钻数据**：查看第 1 关的 `guide_finish` 事件。发现 60% 的流失玩家没有完成新手引导的“穿装备”步骤。
*   **结论**：引导 UI 卡住了，或者装备按钮太不明显。
*   **行动**：给“穿装备”按钮增加强光呼吸特效。

### ⚔️ 案例 B：数值平衡与 Build 强度 (Balance)
*   **现象**：论坛有人抱怨 "火法太弱了"。
*   **分析步骤**：
    1.  **胜率矩阵**：拉取 `level_finish` 数据，按 `hero_class` 分组。
    2.  **发现**：火法的平均胜率是 45%，而冰法的胜率是 70%。
    3.  **伤害构成**：查看 `combat_summary`，发现火法的 `total_dmg_dealt` 并不低，但 `hp_percent` (剩余血量) 普遍很低。
*   **结论**：火法输出够，但身板太脆，容错率低。
*   **行动**：增加火法技能的吸血词缀或基础生命值，而不是加伤害。

### 🛒 案例 C：商品滞销之谜 (Merchandise Optimization)
*   **现象**：新上架的 "$4.99 新手礼包" 销量惨淡。
*   **分析步骤**：
    1.  **电商漏斗**：`iap_store_open` (曝光) -> `iap_product_click` (详情) -> `iap_purchase_verify` (成交)。
    2.  **数据**：曝光量巨大（主页弹窗），但详情页点击率 (CTR) 只有 2%。
    3.  **对比**：另一个 "$0.99 每日特惠" 的 CTR 是 20%。
*   **结论**：玩家对 $4.99 的价格敏感，或者礼包内容（图片）看起来不值这个价。
*   **行动**：拆分礼包，改为 "$1.99" 的低价版进行 A/B 测试。

### 🚪 案例 D：商店打开率有什么用？ (Store Traffic)
*   **问题**：为什么我的 ARPU (平均用户收入) 这么低？
*   **分析步骤**：
    1.  **统计渗透率**：计算 (打开过商店的人数 / DAU)。如果低于 10%，说明大部分人根本没见过你的商品。
    2.  **入口分析**：统计 `iap_store_open` 的 `entry_point` 参数。
        *   MainMenu: 60%
        *   PauseMenu: 5%
        *   **ReviveScreen (复活界面): 35%**
*   **洞察**：玩家在死亡时付费意愿最强（冲动消费）。
*   **行动**：在复活倒计时界面增加“复活 + 满血 + 10秒无敌”的特惠推送，直接提升商店流量。

### 🕵️ 案例 E：抓捕作弊者 (Anti-Cheat)
*   **逻辑**：基于统计学的异常检测。
*   **规则**：
    1.  **资源异常**：单场掉落 `Gold > 5000` (理论上限 500)。
    2.  **伤害异常**：1级角色 `dps > 1000`。
    3.  **通关时间异常**：第 10 关 `duration < 30s`。
*   **行动**：不要立即封号（防止误判），而是打上 `cheater_flag` 标签，将其移出排行榜，或匹配到“神仙服”让他们互殴。

### 📺 案例 F：广告变现效率 (Ad Monetization)
*   **问题**：玩家很反感看广告吗？
*   **分析步骤**：
    1.  **相关性分析**：横轴是“日均观看广告次数”，纵轴是“次日留存率”。
    2.  **发现**：
        *   看 0 次广告的留存率：30%
        *   看 1-3 次广告的留存率：35% (反而高了？因为看了广告拿了资源，玩得更爽)
        *   看 >8 次广告的留存率：15% (断崖式下跌)
*   **结论**：适度的激励视频是正反馈，但过度的插屏广告是劝退。
*   **行动**：设置每日广告上限为 5 次，或者在第 5 次后不再弹出主动广告。

---

## 7. 实时分析系统 (Real-time Analytics)

### 7.1 实时监控面板 (Live Dashboard)
**为什么需要实时数据？**
- 新功能上线后，需要立即发现问题
- 活动期间需要实时调整策略
- 崩溃或支付异常需要秒级响应

| 指标类型 | 监控项 | 报警阈值 | 处理方案 |
| :--- | :--- | :--- | :--- |
| 📈 收入监控 | 小时收入同比下降 | > 30% | 立即检查支付渠道 |
| 👥 用户活跃 | 实时在线人数异常 | < 历史均值 50% | 检查服务器状态 |
| 🐛 稳定性 | 崩溃率 | > 2% | 回滚版本或热修复 |
| ⚡ 性能 | 服务器响应时间 | > 1000ms | 扩容或优化查询 |

### 7.2 实时活动追踪 (Event Tracking)
```csharp
// 实时活动效果监控
public class RealTimeEventTracker
{
    public static void TrackEvent(string eventType, Dictionary<string, object> data)
    {
        // 发送到实时数据流 (Kafka/WebSocket)
        RealTimeStream.Send(eventType, data);

        // 同时记录到离线分析系统
        AnalyticsMgr.LogEvent(eventType, data);
    }

    // 活动转化漏斗实时监控
    public static void MonitorFunnel(string funnelId, string step, string userId)
    {
        TrackEvent("funnel_step", new Dictionary<string, object>{
            {"funnel_id", funnelId},
            {"step", step},
            {"user_id", userId},
            {"timestamp", DateTime.UtcNow}
        });
    }
}
```

## 8. A/B测试框架 (A/B Testing Framework)

### 8.1 实验设计原则
**🎯 业界最佳实践**：
- **Netflix** 每天运行 250+ 个A/B测试
- **Facebook** 通过A/B测试发现蓝色主题提升15%互动率
- **Airbnb** 用A/B测试优化搜索算法，提升20%预订率

| 实验类型 | 适用场景 | 最小样本量 | 运行时长 |
| :--- | :--- | :--- | :--- |
| 🎨 UI变化 | 按钮颜色、文案 | 1000用户/组 | 1-2周 |
| 🎮 玩法调整 | 难度曲线、奖励 | 5000用户/组 | 2-4周 |
| 💰 商业化 | 价格、礼包内容 | 10000用户/组 | 4-6周 |

### 8.2 分流算法 (User Bucketing)
```csharp
public class ABTestManager
{
    // 基于用户ID的一致性哈希分流
    public static string GetExperimentGroup(string experimentName, string userId)
    {
        // 确保用户始终在同一实验组
        int hash = (experimentName + userId).GetHashCode();
        int bucket = Math.Abs(hash) % 100;

        // 50%对照组，50%实验组
        return bucket < 50 ? "control" : "treatment";
    }

    // 多变量测试 (MVT)
    public static string GetMVTGroup(string experimentName, string userId,
        Dictionary<string, float> variantWeights)
    {
        int hash = (experimentName + userId).GetHashCode();
        int bucket = Math.Abs(hash) % 100;

        float cumulative = 0;
        foreach (var variant in variantWeights)
        {
            cumulative += variant.Value;
            if (bucket < cumulative * 100)
                return variant.Key;
        }
        return "control";
    }
}
```

### 8.3 统计显著性检验
```csharp
public class StatisticalAnalyzer
{
    // 计算置信区间 (95%)
    public static (double lower, double upper) CalculateConfidenceInterval(
        double conversionRate, int sampleSize)
    {
        double standardError = Math.Sqrt(conversionRate * (1 - conversionRate) / sampleSize);
        double margin = 1.96 * standardError; // 95%置信度
        return (conversionRate - margin, conversionRate + margin);
    }

    // A/B测试效果评估
    public static bool IsSignificant(ExperimentResult control, ExperimentResult treatment)
    {
        // 使用Z检验计算p值
        double pooledP = (control.Conversions + treatment.Conversions) /
                        (control.Users + treatment.Users);
        double se = Math.Sqrt(pooledP * (1 - pooledP) *
                    (1.0/control.Users + 1.0/treatment.Users));
        double zScore = (treatment.ConversionRate - control.ConversionRate) / se;

        return Math.Abs(zScore) > 1.96; // p < 0.05
    }
}
```

## 9. 数据可视化与报告 (Data Visualization)

### 9.1 核心仪表板设计
**📊 业界标杆**：
- **Supercell** 的实时仪表板显示全球玩家分布
- **King** 用热力图分析关卡难度曲线
- **Riot Games** 通过玩家行为预测流失

```csharp
public class DashboardGenerator
{
    // 留存率热力图
    public static void GenerateRetentionHeatmap()
    {
        var retentionData = GetRetentionData();
        // 使用颜色深浅表示留存率高低
        // 红色: 低留存 (< 20%)
        // 黄色: 中等留存 (20-40%)
        // 绿色: 高留存 (> 40%)
    }

    // 收入预测曲线
    public static void GenerateRevenueForecast()
    {
        var historicalData = GetHistoricalRevenue();
        var forecast = TimeSeriesForecast(historicalData, days: 30);
        // 显示置信区间
        ShowForecastWithConfidence(forecast);
    }
}
```

### 9.2 自动化报告系统
| 报告类型 | 频率 | 关键指标 | 发送对象 |
| :--- | :--- | :--- | :--- |
| 📱 每日简报 | 早上9点 | DAU、收入、崩溃率 | 全团队 |
| 📈 周度深度 | 周一 | 留存、关卡数据、商业化 | 产品经理 |
| 🎯 月度复盘 | 月初 | 版本对比、竞品分析 | 高层管理 |

## 10. 数据质量与监控 (Data Quality)

### 10.1 数据质量检查
**🚨 常见问题**：
- 数据丢失（网络问题导致事件未上报）
- 数据重复（客户端重试机制）
- 数据异常（作弊、测试账号污染）

```csharp
public class DataQualityMonitor
{
    // 数据完整性检查
    public static void ValidateDataCompleteness()
    {
        var expectedEvents = GetExpectedEvents();
        var actualEvents = GetActualEvents();

        double completeness = (double)actualEvents / expectedEvents;
        if (completeness < 0.95) // 95%完整性阈值
        {
            AlertManager.SendAlert("Data completeness below threshold");
        }
    }

    // 异常值检测（使用3σ原则）
    public static List<DataPoint> DetectOutliers(List<DataPoint> data)
    {
        double mean = data.Average(d => d.Value);
        double stdDev = CalculateStandardDeviation(data);

        return data.Where(d => Math.Abs(d.Value - mean) > 3 * stdDev).ToList();
    }
}
```

### 10.2 反作弊数据监控
| 监控维度 | 异常阈值 | 检测算法 | 处理策略 |
| :--- | :--- | :--- | :--- |
| 💰 资源获取速度 | > 正常值5倍 | 统计分布 | 标记观察 |
| ⚔️ 战斗数据 | 伤害超出理论上限 | 规则引擎 | 自动封禁 |
| 🏃 移动速度 | > 最大移动速度 | 物理引擎验证 | 踢出游戏 |
| ⏱️ 游戏时间 | > 24小时连续在线 | 行为模式 | 人工审核 |

---

## 11. 代码实现接口 (C# Interface)

```csharp
public static class AnalyticsMgr
{
    public static void LogEvent(string eventName, Dictionary<string, object> params)
    {
        // 1. 添加通用参数 (User ID, Device, etc.)
        params["user_id"] = UserProfile.ID;
        params["ts"] = DateTime.UtcNow.ToUnixTimeSeconds();

        // 2. 发送给第三方 SDK (Unity Analytics, Firebase, ThinkingData)
        // SDK.Track(eventName, params);

        // 3. 开发模式下打印日志
        if (Debug.isDebugBuild)
        {
            Debug.Log($"[Analytics] {eventName}: {JsonConvert.SerializeObject(params)}");
        }
    }

    // 封装常用方法，防止拼写错误
    public static void LogLevelStart(int levelId, string difficulty) { ... }
    public static void LogResourceChange(string type, int amount, string reason) { ... }
}
```
