# ⏱️ 性能监控脚本集：Unity 实战性能守门员

**文档目标**：提供一套轻量级的运行时监控脚本，帮助开发团队在非 Profiler 模式下（如真机包、演示包）实时发现性能瓶颈。

---

## 1. 为什么需要运行时监控？

Unity Profiler 开销很大，且只能连接开发机。
我们需要在**QA 测试包**或**每日构建包**中，直观地看到：
*   是不是掉帧了？
*   是不是内存泄漏了？
*   是不是同屏怪太多了？

---

## 2. 脚本清单

将以下脚本放入 `Assets/Scripts/Debug/Performance`。

### 2.1 `FPSMonitor.cs` (帧时间直方图)
不只是显示 "60 FPS"。因为 "平均 60 FPS" 可能意味着 59 帧是 1ms，第 60 帧是 500ms（卡顿）。
*   **功能**：显示 1% Low FPS 和帧生成时间 (ms)。
*   **颜色编码**：<16ms (绿), 16-33ms (黄), >33ms (红)。

```csharp
void Update() {
    float frameTime = Time.unscaledDeltaTime * 1000f;
    _buffer.Add(frameTime);
    // 计算 99th percentile...
}
```

### 2.2 `ObjectCountTracker.cs` (实体预算监控)
防止策划或生成器配置错误导致爆内存。
*   **功能**：每秒统计场景中特定 Tag (Enemy, Bullet, VFX) 的数量。
*   **报警**：
    *   `Enemy Count > 500`: ⚠️ Warning
    *   `Bullet Count > 2000`: ❌ Critical
*   **UI**：在屏幕左上角显示红字警告。

### 2.3 `MemoryWatcher.cs` (GC 监控)
*   **功能**：监控 `GC.GetTotalMemory` 的变化率。
*   **检测泄漏**：如果在非战斗场景（如主菜单），内存依然每秒持续上涨，说明有 UI 或静态引用泄漏。

---

## 3. 集成与开关

建议使用 `SRDebugger` 或自定义的调试控制台来切换显示。

```csharp
#if DEVELOPMENT_BUILD || UNITY_EDITOR
    PerformanceHUD.Show();
#endif
```

*   **快捷键**：在 PC 包中按 `F3` 开启/关闭。
*   **手势**：在手机包中三指点击屏幕开启。

---

## 4. 验收标准

*   **战斗场景**：
    *   Enemy < 500
    *   DrawCalls < 300 (Mobile) / 1500 (PC)
    *   FrameTime < 16.6ms (保持 60fps)
    *   GC Alloc < 50KB / frame (理想是 0)

任何超出上述标准的情况，测试人员应截图并将 `FPSMonitor` 的数据附在 Bug 单中。
