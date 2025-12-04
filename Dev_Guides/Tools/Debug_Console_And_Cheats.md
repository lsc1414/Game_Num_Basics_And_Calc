# 🛠️ 调试指令与GM工具 (Debug Console & Cheats)

> **重要性**: Roguelike 游戏的随机性是测试的噩梦。如果没有一套强大的上帝工具，QA 根本无法验证“第 50 层刷出的神器是否会导致闪退”。

## 1. 核心指令集 (Command List)

建议接入开源库（如 **SRDebugger** 或 **IngameDebugConsole**），实现以下指令：

### 1.1 资源控制
*   `/add_gold [amount]`: 加金币。
*   `/add_exp [amount]`: 加主角经验。
*   `/level_up`: 直接升级并触发 Perk 选择界面。

### 1.2 流程控制
*   `/skip_wave`: 直接跳过当前波次（杀死所有怪）。
*   `/spawn_mob [id] [count]`: 在鼠标位置生成指定怪物。
*   `/spawn_boss`: 直接召唤当前关卡的 BOSS。
*   `/time_scale [float]`: 游戏变速。0=暂停，10=十倍速（测试数值平衡神器）。

### 1.3 装备与掉落
*   `/give_item [id]`:以此 ID 获取装备。
*   `/force_drop [rarity]`: 下一次击杀必掉指定稀有度的物品。
*   `/clear_bag`: 清空背包。

### 1.4 无敌与状态
*   `/god_mode`: 主角无敌 + 秒杀敌人。
*   `/no_cd`: 技能无冷却。
*   `/show_fps`: 显示帧率和内存占用。

## 2. 自动化测试脚本 (Auto-Play Bots)

为了测试服务器压力或数值崩坏，需要简单的 AI 脚本：

*   **AFK Bot**: 主角站在原地不动，自动普攻最近敌人。用于测试“挂机一晚上会不会内存溢出”。
*   **Random Bot**: 随机移动，有技能就放。用于测试“乱按会不会报错”。

## 3. 安全与权限 (Security)

*   **开发宏 (`#if UNITY_EDITOR`)**: 确保这些作弊代码**绝对不会**打包进 Release 版本。
*   **后门锁**: 如果必须在 Release 版保留（为了线上救火），必须加 **密码锁** 或 **设备 ID 白名单**。
    *   *案例*: 连续点击屏幕左上角 10 次，输入密码 `vampire2025` 才能打开控制台。

## 4. 推荐插件
*   **Quantum Console**: 极其强大的 C# 控制台，支持自动补全。
*   **SRDebugger**: 也就是 "SROptions"，手机端非常好用的调试面板，支持各种 Tweak 选项。

