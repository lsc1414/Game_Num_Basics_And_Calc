# 📜 Project Vampirefall 全员速查表 (The Holy Cheat Sheet)

本文档汇总了项目各领域的**绝对红线 (Must Not)**、**核心原则 (Must)** 和 **可选方案 (Option)**。
请所有成员将对应角色的部分打印并贴在显示器旁。

---

## 1. 💻 程序员 (Programmer)

### 🔴 Must Not (绝对禁止)
*   **禁止在 Update 中分配内存**: `new List<>`, `Instantiate` (必须用对象池)。
*   **禁止在战斗核心循环用 LINQ**: GC 杀手。
*   **禁止硬编码数值**: 伤害、掉率、CD 必须读表 (ConfigSystem)。
*   **禁止私自修改 Art 资产**: 尤其是 Shader 参数，必须遵循 [TCP2 协议](../Art_Pipeline/Indie_Team_Art_Strategy.md#11--程序员专用tcp2-调参协议-the-tcp2-tuning-protocol)。
*   **禁止多光源**: 场景中 `Light.Count` 永远 `<= 1` (Directional)。

### 🟢 Must (必须执行)
*   **必须使用 ECS/DOTS 处理海量单位**: 怪物数量 > 100 时必须走 Job System。
*   **必须使用 YooAsset 加载资源**: 禁止 `Resources.Load`。
*   **必须做防作弊校验**: 关键数值 (金币、伤害) 必须使用 `ObscuredType` 或服务端校验。
*   **必须处理断线重连**: 任何网络请求都要有 Retry 机制。

### 🔵 Option (可选/建议)
*   **建议使用 UniTask**: 替代 Coroutine 以减少内存开销。
*   **建议使用 Odin Inspector**: 优化策划的配置体验。

---

## 2. 🎨 美术 (Artist)

### 🔴 Must Not (绝对禁止)
*   **禁止软阴影 (Soft Shadows)**: 风格化必须是硬边 (Hard Edge)。
*   **禁止手动调阴影颜色**: 除非是 UI/FX，否则禁止修改材质球的 `ShadowColor` (应由环境光控制)。
*   **禁止非 POT 纹理**: 独立纹理必须是 512, 1024, 2048。
*   **禁止 UI 图标无出血**: 所有 UI Sprite 必须有 **1px 透明边缘** (防止线性过滤黑边)。
*   **禁止模型轴心乱飞**: 角色 Pivot 必须在脚底 (0,0,0)。

### 🟢 Must (必须执行)
*   **必须使用 Ramp Texture**: 控制光照衰减，实现风格化。
*   **必须合并 Mesh**: 静态场景物体必须使用 Static Batching 或 GPU Instancing。
*   **必须分离透明度**: 半透明物体 (Glass) 和不透明物体 (Stone) 材质球必须分开。
*   **必须检查 Mobile Shader**: 确保使用的是 Mobile 版本的 Shader (无高光、无复杂反射)。

### 🔵 Option (可选/建议)
*   **建议使用 MatCap**: 替代高光 (Specular) 来模拟金属质感。
*   **建议使用 Vertex Color**: 对于简单道具，用顶点色代替贴图以节省内存。

---

## 3. 🧠 策划 (Designer)

### 🔴 Must Not (绝对禁止)
*   **禁止无限指数膨胀**: 必须有软上限 (Soft Cap) 或递减收益 (Diminishing Returns)。
*   **禁止 Pay-to-Win (PVP)**: 氪金只能买皮肤或加速，不能买数值碾压。
*   **禁止无预警的难度跳变**: 难度曲线必须平滑，Boss 战前要有铺垫。
*   **禁止修改已上线资产的 GUID**: 会导致玩家存档损坏。

### 🟢 Must (必须执行)
*   **必须配置兜底机制**: 抽卡必须有保底 (Pity System)，闪避必须有上限 (e.g., 75%)。
*   **必须维护经济循环**: 产出 (Source) 必须小于等于 消耗 (Sink) + 留存预期。
*   **必须遵循 40 天赛季周期**: Battle Pass 设计要以此为基准。
*   **必须写注释**: Excel 表头必须有详细注释，说明字段用途。

### 🔵 Option (可选/建议)
*   **建议设计“高光时刻”**: 每局游戏至少让玩家爽一次 (如全屏清怪)。
*   **建议使用随机池 (Loot Table)**: 而不是固定掉落，增加重玩性。

---

## 4. 📅 项目经理 (Project Manager)

### 🔴 Must Not (绝对禁止)
*   **禁止无测试发版本**: 必须跑通 Automated Test 和冒烟测试。
*   **禁止忽视“差评预警”**: 玩家反馈的“肝度太高”或“逼氪”必须在 24 小时内响应。
*   **禁止在周五下午发布更新**: 除非你想周末加班修 Bug。
*   **禁止使用 AI 生成的宣传图**: Steam 玩家极其反感，会招致差评轰炸。

### 🟢 Must (必须执行)
*   **必须监控愿望单 (Wishlists)**: 确保发售前达到 7,000 (最低) / 10,000 (安全)。
*   **必须执行灰度发布**: 先在小地区 (如菲律宾、加拿大) 测试留存，再推全球。
*   **必须储备 2 个版本的存货**: 永远不要追着 Deadline 跑，要有缓冲。
*   **必须本地化定价**: 重点关注中国、巴西、俄罗斯区。

### 🔵 Option (可选/建议)
*   **建议参加 Steam Next Fest**: 这是最大的免费流量来源。
*   **建议建立 Discord 社区**: 让核心玩家参与测试和反馈。
