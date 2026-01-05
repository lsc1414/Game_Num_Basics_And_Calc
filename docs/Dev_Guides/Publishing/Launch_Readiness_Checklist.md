# 🚀 发射前夜：上线前的生死清单 (Launch Readiness Checklist)

> **"起飞前漏掉任何一颗螺丝，都可能导致坠机。"**
>
> 别相信记忆，只相信清单。请在提交审核（Submission）前逐项勾选。

---

## 1. 👶 第一印象 (FTUE - First Time User Experience)

这是最容易被老开发者忽视的环节，因为我们的本地环境总是“脏”的。

- [ ] **白纸测试 (Clean Install Test):**
    - 彻底删除本地所有数据（卸载游戏 + 清除 PlayerPrefs + 删除 PersistentDataPath 下所有文件）。
    - 重新安装游戏。
    - **检查点:** 
        - [ ] 是否在请求权限（如通知、广告跟踪）前给了用户解释？
        - [ ] 教程流程是否因断网而卡死？
        - [ ] 默认音量是否合适（不要一上来就炸麦）？
        - [ ] 默认语言是否正确识别了系统语言？

- [ ] **弱网/断网测试:**
    - 开启飞行模式进入游戏。
    - **检查点:**
        - [ ] 游戏应该提示“网络连接失败”并允许重试，而不是卡在 Loading 条或直接崩溃。
        - [ ] 只有广告/IAP按钮应该被禁用，单机内容应正常游玩。

---

## 2. 🏗️ 构建与性能 (Build & Verification)

- [ ] **Release 模式检查:**
    - [ ] 确保 Build Setting 里是 `Release` 不是 `Debug`。
    - [ ] 确保 `Development Build`, `Autoconnect Profiler` **未勾选**。
    - [ ] 检查 `Scripting Backend` 是否为 **IL2CPP** (Android/iOS 必须)。
    - [ ] 检查 `Target Architectures` 是否包含 **ARM64**。

- [ ] **日志剥离 (Log Stripping):**
    - [ ] 发布包中是否屏蔽了 `Debug.Log`？
    - *技巧: 使用 `Conditional("ENABLE_LOG")` 或自定义 Logger 在 Release 版中移除日志。大量日志拼接字符串会消耗性能。*

- [ ] **安装包体积 (Health Check):**
    - [ ] 查看 Editor Log 里的打包含量报告。
    - [ ] 检查是否有未压缩的 `.wav` 音频（应设为 Vorbis/MP3）。
    - [ ] 检查是否有未压缩的 `.psd/.tif` 纹理被错误打包。

---

## 3. ⚖️ 法务与合规 (Compliance)

- [ ] **隐私政策 (Privacy Policy):**
    - [ ] 游戏内（通常在设置页）必须有点击跳转隐私政策的链接。
    - [ ] 链接必须有效且可访问。

- [ ] **恢复购买 (Restore Purchase):**
    - [ ] (iOS 必须) 必须有显眼的“恢复购买”按钮。
    - [ ] 点击后应该能正确恢复非消耗品（去除广告、皮肤）。

- [ ] **UI 安全区 (Safe Area):**
    - [ ] **刘海/灵动岛:** 关键 UI（金币、返回按钮）是否被刘海挡住？
    - [ ] **底部横条:** 底部交互按钮是否被 iPhone 的 Home Indicator 遮挡？

---

## 4. 🛍️ 商店页面 (Store Presence)

- [ ] **元数据检查:**
    - [ ] 版本号 (Version Code) 是否已递增？(如果不仅增，谷歌/苹果后台会拒绝上传)。
    - [ ] 应用图标 (Icon) 是否是最新的高辨识度版本？
    - [ ] 截图 (Screenshots) 是否包含真实 gameplay？（很多平台反感纯 CG 截图）。

- [ ] **关键词:**
    - [ ] 标题和副标题没有拼写错误。

---

## 5. 🩹 最后的防线

- [ ] **Crash 收集:**
    - [ ] 确保已接入 Crashlytics / Bugly 等崩溃上报 SDK。
    - [ ] 测试一次人为制造的崩溃，确保后台能收到报告。

> **祝你好运！Good Luck!**
