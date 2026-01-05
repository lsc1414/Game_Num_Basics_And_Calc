# 🕵️‍♂️ 福尔摩斯调试法：像侦探一样修 Bug (Sherlock Holmes Debugging)

> **"排除了一切不可能的，剩下的不管多难以置信，那都是真相。" —— 夏洛克·福尔摩斯**
>
> 调试不是瞎猜 (Guessing)，而是推理 (Reasoning)。

---

## 1. 🔍 核心法则：二分查找 (Divide and Conquer)

当你面对一个庞大的系统 Bug 时，不要试图一行行看代码。

### 🔪 代码二分法
1.  **现象：** 游戏启动就崩，不知道是哪个系统的问题。
2.  **操作：** 
    - 把 `GameBootstrapper` 里一半的 Manager 注释掉。
    - 跑一下。还崩吗？
    - **崩：** 问题在剩下的一半里。继续二分。
    - **不崩：** 问题在被注释掉的那一半里。把那一半恢复，再注释掉其中一半。
3.  **效率：** 1000 个模块只需要 10 次就能定位到也是 O(logN)。

### 🕰️ 时间二分法 (Git Bisect)
1.  **现象：** 昨天是好的，今天坏了。但我今天提交了 20 个 Commit。
2.  **操作：** 使用 `git bisect`。
    - `git bisect start`
    - `git bisect bad` (当前版本)
    - `git bisect good <commit-hash>` (昨天的版本)
    - Git 会自动跳到中间的一个 Commit。你测一下，告诉 Git 是 `good` 还是 `bad`。
    - 几次之后，Git 会告诉你：**"就是这行代码搞崩了全场"**。

---

## 2. 🧠 内存侦查 (Memory Leak Hunting)

内存泄漏通常是隐形的杀手。

### 📸 内存快照对比 (Snapshot Diffing)
1.  打开 Unity Memory Profiler。
2.  进入主菜单，点击 **Capture (Snapshot A)**。
3.  进入战斗，打一架，退回主菜单。
4.  点击 **Capture (Snapshot B)**。
5.  **核心操作：** 查看 Diff (B - A)。
    - 理论上，回到主菜单后，内存应该大致回到 A 的水平。
    - 如果你发现多了 100 个 `Texture2D` 或 500 个 `EnemyInstance`，那就是没卸载干净（比如被静态 Action 引用了）。

---

## 3. 🎨 渲染诊断 (RenderDoc)

当画面出现紫块、黑块，或者 DrawCall 莫名其妙爆炸时。

### 🎞️ 逐帧分析
1.  在 Game 窗口点击右键 -> Load RenderDoc。
2.  点击 Capture Frame。
3.  在 RenderDoc 里打开这一帧。
4.  **Event Browser:** 你可以看到这一帧 GPU 做的每一件事。
    - DrawSkybox
    - DrawOpaque
    - DrawTransparent
5.  **查案：**
    - 为什么这个模型没有被合批 (Batching)？看它的 State，是不是材质不一样？是不是 Lightmap Index 不一样？
    - 为什么这个像素是黑的？点击 Pixel History，看是哪个 Shader 计算出了 (0,0,0)。

---

## 4. 📝 崩溃分析 (Crash Dump Analysis)

不要只说“游戏崩了”。看日志。

### 📜 读懂 Stack Trace
*   **NullReferenceException:** 90% 是因为你没判读 `if (obj != null)` 或者初始化顺序错了。
*   **MissingReferenceException:** 你试图访问一个已经被 `Destroy` 的物体。
*   **IndexOutOfRangeException:** 数组越界。

### 📱 移动端真机调试
*   **Android:** 使用 Android Logcat (Unity 2019+ Package)。过滤 `Unity` 标签，可以看到真机的红色报错。
*   **iOS:** 打开 Xcode -> Window -> Devices and Simulators -> View Device Logs。看崩溃报告 (Crash Report)。

---

## 5. 🌡️ 性能分析 (Profiling First)

**不要先优化，先分析！**

- 不要觉得 "我觉得这里卡" 就去改代码。
- 打开 **Unity Profiler** (Deep Profile 慎用，卡爆)。
- 看 **CPU Usage** 下的 **Timeline**。
- 找到那个耗时最长的函数长条。
- **那才是凶手。** 优化其他地方都是浪费时间。
