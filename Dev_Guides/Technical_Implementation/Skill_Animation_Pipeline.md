# 🎬 技能动画管线：从 Animator Event 到可视化时间轴

在动作游戏与 RPG 开发中，技能释放不仅仅是播放一个 Animation Clip。它涉及到复杂的**时序同步**：第 0.1秒 播放音效，第 0.3秒 生成特效，第 0.4秒 开启伤害判定框，第 0.8秒 允许输入打断。

如何优雅地维护这些时序逻辑？本文档对比了传统方案与工业化方案，并提供最佳实践。

---

## 1. 传统方案：Animation Events

Unity 原生支持在 Animation Clip 的特定帧插入 Event，调用挂在同一个 GameObject 上的函数。

### 1.1 工作流
1.  打开 Animation 窗口。
2.  在第 20 帧右键 -> `Add Animation Event`。
3.  填写函数名 `OnHit` 和参数 `1.0`。
4.  代码中实现 `void OnHit(float damageMultiplier) { ... }`。

### 1.2 致命缺陷 (The "Traps")
*   **弱引用地狱**: Event 依赖字符串匹配函数名。如果你重构代码改了函数名，所有动画里的 Event 都会默默失效，编译器不会报错。
*   **逻辑丢失**: 当动画处于 **Transition (过渡)** 阶段，或者被 `CrossFade` 强行打断时，被跳过的帧上的 Event **不会触发**。这会导致严重 Bug（例如：玩家动作被打断，但“无敌状态”没被清除，导致永久无敌）。
*   **复用困难**: 多个角色复用同一个动画文件（Humanoid Retargeting），但他们的脚本逻辑不同，会导致 MissingMethodException。
*   **数据分散**: 技能逻辑散落在几十个 `.anim` 文件里，策划无法在一个地方概览所有配置。

**结论**: 仅适用于简单的原型或纯视觉反馈（如脚步声）。**严禁用于核心战斗逻辑（伤害、状态切换）。**

---

## 2. 进阶方案：State Machine Behaviours (SMB)

利用 Unity Animator 的 `StateMachineBehaviour` 脚本，绑定在 Animator Controller 的 **State** 上，而非 Clip 内。

### 2.1 工作流
1.  在 Animator 窗口选中 "Attack_Slash" 状态。
2.  点击 `Add Behaviour` -> 新建脚本 `SkillState`.
3.  利用 `OnStateEnter`, `OnStateUpdate`, `OnStateExit` 钩子。

### 2.2 优缺点
*   ✅ **生命周期明确**: 保证 Enter/Exit 一定会成对调用（除非 Animator 被禁用），适合处理 Buff 开关、无敌帧开关。
*   ✅ **逻辑解耦**: 脚本在 Asset 层面，不依赖具体场景物体。
*   ❌ **时序精度低**: `OnStateUpdate` 每一帧都跑，如果要精确在“动作播放到 35%”时触发伤害，需要写繁琐的 `normalizedTime` 检查逻辑，且难以可视化编辑。

---

## 3. 工业级方案：可视化时间轴编辑器 (Visual Timeline Editor)

这是目前 3A 及大型独立游戏（如 *Hades*, *God of War*）的主流做法。核心思想是将技能看作一个**序列 (Sequence)**，而非单纯的动画。

### 3.1 架构核心
技能不再是一个函数，而是一个 **ScriptableObject**（我们称之为 `SkillSequence`）。它包含多条轨道（Track）：
*   **Animation Track**: 播放哪个动作。
*   **Audio Track**: 播放什么音效。
*   **VFX Track**: 在哪个骨骼点生成特效。
*   **Logic Track**: 伤害判定框 (Hitbox) 的开启与关闭时间窗口。
*   **Interrupt Track**: 哪个时间段允许被移动打断，哪个时间段允许被大招打断。

### 3.2 实现路径
#### A. 使用 Unity Playable API + Timeline
Unity 内置的 Timeline 功能强大，但原生主要用于过场动画 (Cutscene)。
*   **魔改 Timeline**: 自定义 Track 和 Clip。
*   **优势**: 编辑器体验极其丝滑，支持预览。
*   **劣势**: 运行时性能开销略大（Playable Graph），且数据结构较重。

#### B. 自研轻量级编辑器 (推荐)
基于 `EditorWindow` 开发一个类似 Timeline 的 GUI。
*   **数据结构**:
    ```csharp
    public class SkillData : ScriptableObject {
        public float duration;
        public List<SkillEvent> events; // 按时间排序
    }
    
    [Serializable]
    public class SkillEvent {
        public float time;
        public EventType type; // Damage, VFX, Sound
        public string parameter;
    }
    ```
*   **运行时驱动**:
    在 `Update` 中计时：
    ```csharp
    void Update() {
        timer += Time.deltaTime;
        while (nextEventIndex < events.Count && timer >= events[nextEventIndex].time) {
            Execute(events[nextEventIndex]);
            nextEventIndex++;
        }
    }
    ```

### 3.3 为什么它更优雅？
1.  **确定性 (Determinism)**: 逻辑完全由时间驱动，不依赖动画系统的混合状态。即使模型丢失、动画卡住，伤害判定依然会准时触发。
2.  **可视化 (Visualization)**: 策划可以直观地看到：伤害是在刀光特效出现的 0.1秒 后触发的。
3.  **热重载**: 可以在 Play Mode 下拖动时间轴上的滑块，实时调整手感（例如修改前摇时间），无需重编译。
4.  **健壮性**: 所有的配置都是强引用的 Asset，不会因为改了函数名而崩坏。

---

## 4. Vampirefall 落地建议

鉴于项目类型（塔防+肉鸽），技能系统主要用于**防御塔**和**怪物**。

### 推荐方案：轻量级帧事件系统
不需要做完整的 Timeline 编辑器，性价比最高的是 **"Animation Curve + ScriptableObject"**。

1.  **配置**: 在技能 SO 中定义关键帧时间点。
    *   `FireTime: 0.5s` (发射投射物时间)
    *   `BackswingTime: 0.8s` (后摇结束，可进行下一次攻击时间)
    *   `TotalDuration: 1.2s` (动作总时长)
2.  **预览**: 写一个简单的 Editor 脚本，在 Scene View 中根据当前选中的帧，画出怪物的 Hitbox 范围，方便对齐。
3.  **执行**: 使用 Coroutine 或 Timer 在代码中严格执行上述时间点，**动画仅作为视觉表现配合逻辑播放**，而不是逻辑驱动动画。

**黄金法则**: **Logic Drives Animation, Never the Other Way Around.** (逻辑驱动表现，永远不要反过来。)
