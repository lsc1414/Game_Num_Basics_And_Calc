# 🧙‍♂️ Steam Unity 游戏开发标准：下限与上限深度研究

## 📚 1. 理论基础 (Theoretical Basis)

### 1.1 核心定义：下限与上限

在 Steam 平台，“下限”与手游截然不同。Steam 玩家群体（尤其是“PC Master Race”）对基础功能的缺失容忍度极低。

- **🛡️ 下限 (The Floor)**：**功能性完备 (Functional Completeness)**。即游戏“像一个正经的 PC 软件”一样运行。如果做不到，会招致“差评轰炸”、“退款”和“翻新货（Asset Flip）”的指控。
- **🚀 上限 (The Ceiling)**：**体验性卓越 (Experience Excellence)**。即游戏充分利用 Steam 生态和 PC 硬件优势，提供超出预期的细节打磨，建立“精品”口碑。

### 1.2 PC 玩家心理模型 (The PC Gamer Mentality)

- **“我的电脑我做主”**：玩家痛恨被教条地锁定 60 帧、无法修改按键、无法静音后台声音。
- **“硬件军备竞赛”**：从 720p 笔记本到 4K 144Hz 带鱼屏，游戏必须适配千奇百怪的硬件环境。
- **“生态依赖”**：习惯 Shift+Tab 聊天，习惯 F12 截图，习惯云存档漫游。

## 🛠️ 2. 实践应用 (Practical Implementation)

### 🛡️ 保证下限：绝对必做 (The Must-Dos)

如果这些没做到，你的游戏在 Steam 评论区会被 **狠狠羞辱**。

#### A. 分辨率与窗口管理 (Resolution & Window)

- **🚫 错误做法**：只提供 1920x1080 选项，或者强制全屏无法切出。
- **✅ 正确做法**：
  - **支持任意比例**：动态读取 `Screen.resolutions`，不要硬编码。
  - **支持超宽屏 (21:9)**：UI 锚点（Anchors）必须设置正确，核心玩法画面不能被拉伸或裁剪（使用 Camera Viewport 适配）。
  - **窗口模式三剑客**：全屏 (Exclusive Fullscreen)、无边框窗口 (Borderless Window)、窗口化 (Windowed)。
  - _Unity 提示_：使用 `Screen.SetResolution(w, h, mode)`。

#### B. 音频控制 (Audio Control)

- **✅ 独立滑块**：必须分离 **主音量 (Master)**、**音乐 (BGM)**、**音效 (SFX)**。
- **✅ 后台静音**：提供“后台运行时静音”的 Toggle 选项（Many players watch YouTube while playing）。
- _代码结构建议_：
  ```csharp
  [Serializable]
  public class AudioSettings {
      public float MasterVolume = 1.0f;
      public float MusicVolume = 0.8f;
      public float SfxVolume = 1.0f;
      public bool MuteInBackground = true;
  }
  ```

#### C. 输入与控制 (Input & Controls)

- **✅ 键鼠纹理**：检测到键盘输入时，UI 提示显示“E”；检测到手柄时，动态切换为“Xbox A”或“PS Cross”。
- **✅ 鼠标锁定**：全屏游玩时如果不锁定鼠标在窗口内，多屏玩家会由衷地痛恨你。
- **✅ 退出游戏**：主菜单必须有“退出”按钮。千万不要让玩家必须 Alt+F4 才能退。

#### D. 基础 Steamworks 集成

- **✅ 启动检查**：必须调用 `SteamAPI.RestartAppIfNecessary(AppId)`。防止玩家直接点击 exe 绕过 Steam 启动（导致成就无法触发、时长不统计）。
- **✅ 暂停游戏**：当玩家呼出 Steam Overlay (Shift+Tab) 时，单机游戏**必须自动暂停**。

### 🚀 提升上限：加分项 (The Nice-to-Haves)

做好了这些，玩家会称赞“开发者很用心”。

#### A. 极致的 Steam 生态整合

- **🌟 Steam Cloud (云存档)**：
  - **自动同步**：对 Roguelike 至关重要。
  - **双存档架构**：本地 `SaveData.json` + `Meta.json`（全局解锁）。Unity 中配合 Steamworks.NET 的 `SteamRemoteStorage`。
- **🌟 Rich Presence (富豪状态)**：
  - 好友列表不仅显示“游戏中”，还要显示“正在攻打第 3 层 BOSS [困难]”。
  - _实现_：`SteamFriends.SetRichPresence("status", "Level 3 - Hard Mode")`。
- **🌟 动态按键绑定 (Key Rebinding)**：
  - 允许玩家重定义所有按键。使用新版 Input System (Input Action Assets) 实现 Rebinding UI 相对容易。

#### B. 硬件潜力挖掘

- **🌟 高刷新率支持**：
  - 不要锁死 60fps。提供 30/60/120/144/Inifite 选项。
  - 物理更新（FixedUpdate）与渲染帧率解耦（插值）。
- **🌟 Steam Deck 完美适配 (Verified)**：
  - **字体大小**：最小字体在 720p 屏幕上依然清晰可读。
  - **虚拟键盘**：输入文本框被点击时，自动呼出 Deck 键盘 (`SteamUtils.ShowGamepadTextInput`)。

#### C. 数据与反馈

- **🌟 崩溃报告 (Crash Reporting)**：
  - 接入 Sentry 或 Unity Cloud Diagnostics。Steam 玩家遇到闪退如果不报错，会直接差评；如果弹窗“已发送错误报告”，他们通常会宽容很多。
- **🌟 详细的统计数据 (Stats)**：
  - 不只是成就，还要统计“总杀敌数”、“总死亡数”、“造成总伤害”。这些数据可以在 Steam 社区展示，增加粘性。

## 🌟 3. 业界优秀案例 (Industry Best Practices)

### 3.1 🏆 《Hades》 (Supergiant Games)

- **下限稳固**：完美适配各种分辨率，从未出现 UI 拉伸。
- **上限突破**：
  - **God Mode (神力模式)**：动态难度调节，死亡增加减伤。照顾了手残玩家，又不影响硬核玩家体验。
  - **Vulkan/DX11 切换**：启动项提供图形 API 选择，最大限度兼容老旧显卡。

### 3.2 🏆 《Vampire Survivors》 (Poncle)

- **从下限到上限的进化**：
  - 它是反面教材转正的典型。早期版本是 WebGL 暴力转制，全屏适配极差，性能卡顿。
  - **后期优化**：重写了引擎（从 Phaser 到 Unity/Custom），完美适配 Steam Deck，增加了详细的成就系统（结合游戏内解锁表）。这告诉我们，**核心玩法好可以掩盖技术缺陷，但要长卖必须补齐短板**。

### 3.3 借鉴点 (Takeaways for Vampirefall)

- **必须模仿**：Hades 的 **Rich Presence**。让玩家的朋友看到“他正在第 50 波苦战”，这是最好的免费广告。
- **必须规避**：早期吸血鬼幸存者的 **FPS 也就是伤害**。数值计算逻辑必须与帧率完全剥离（使用 `Time.deltaTime` 或固定时间步长）。

## 🔗 4. 参考资料 (References)

- **官方文档**: [Steamworks Documentation - Best Practices](https://partner.steamgames.com/doc/gettingstarted/bestpractices)
- **技术指南**: [PCGamingWiki - Game Engine: Unity](https://www.pcgamingwiki.com/wiki/Engine:Unity) (查看常见 Bugs 和修复方案)
- **GDC 演讲**: ["You suck at updating your game"](https://www.youtube.com/watch?v=...) - 讲述版本兼容性。
- **Unity 插件**: [Steamworks.NET](https://github.com/rlabrecque/Steamworks.NET) (必用库)
