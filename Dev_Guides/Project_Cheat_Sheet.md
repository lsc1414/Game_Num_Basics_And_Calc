# 📜 全员速查表 (The Blood Oath)

> **Status**: **LAW (宪法)**
> **执行力**: 违反本表红线导致的 Bug 或 性能事故，将被视为**严重失职**。请所有成员将对应部分背诵并在 Code Review / 资源提交时严格对照。

---

## 1. 💻 程序员 (Code: The Foundation)

**核心痛点**: 同屏 500+ 单位的性能压力 & 复杂的 Roguelike 状态叠加。

### 🔴 绝对红线 (Must Not)
1.  **禁止在主线程处理战斗逻辑**: 伤害计算、索敌、Buff 结算必须走 **Job System / Burst**。主线程只负责发令。
2.  **禁止每帧分配内存 (No GC in Update)**:
    *   ❌ `string text = "HP: " + hp;`
    *   ❌ `new List<Enemy>()`
    *   ❌ `foreach (var x in list)` (在老版本编译器会有 GC，养成习惯用 `for`)。
3.  **禁止直接 Destroy/Instantiate**: 任何高频对象（子弹、特效、怪物、伤害数字）**必须**走 `ObjectPoolManager`。
4.  **禁止硬编码文本**: UI 上不允许出现任何中文/英文字符串，必须使用 `Localization.Get("KEY")`。
5.  **禁止在 Release 包开启 Log**: Log 必须封装在 `DebugUtil` 中，并确保 `[Conditional("DEBUG")]`。字符串拼接的 Log 是手机发热的元凶。

### 🟢 核心原则 (Must)
1.  **防御式编程 (Null Checks)**: `GetComponent` 必须缓存。外部传来的数据默认是脏的。
2.  **数据驱动 (Data Driven)**: 技能效果不写死在代码里，而是由 `EffectID` + `Params` 驱动。
    *   *正确*: `ApplyEffect(EffectType.Damage, 100)`
    *   *错误*: `target.hp -= 100;`
3.  **断线重连优先**: 网络层设计必须假设**随时会断网**。所有请求必须有 `Retry` 和 `Timeout`，且在重连后能自动恢复状态。

---

## 2. 🎨 美术 (Art: The Face)

**核心痛点**: 混乱的战场视觉 & 移动端 GPU 压力。

### 🔴 绝对红线 (Must Not)
1.  **禁止无限制的 Overdraw**: 特效粒子数严格限制（见 [VFX标准](../Art/VFX_Standards.md)）。一个火球爆炸不能覆盖全屏 3 层像素。
2.  **禁止使用 Standard Shader**: 所有材质必须使用项目定制的 `Toon/Mobile` Shader。Standard Shader 是性能杀手。
3.  **禁止半透明物体乱序**: 透明材质（UI、特效）必须手动指定 `RenderQueue`，防止显示层级错乱。
4.  **禁止非压缩贴图**: Android 必须是 ASTC，iOS 必须是 ASTC/PVRTC。禁止 RGBA32 (UI 除外)。
5.  **禁止 Model 轴心不在脚底**: 怪物和塔的 Pivot 必须在 `(0,0,0)` 且位于底部中心，否则寻路和放置会对不齐。

### 🟢 核心原则 (Must)
1.  **视觉层级 (Hierarchy)**: 玩家技能 > 怪物技能 > 死亡特效。做特效前先看 [视觉层级指南](../Art/Visual_Hierarchy_In_Chaos.md)。
2.  **合批优先 (Batching)**: 场景物件必须共用材质球。能用一张 2048 图集解决的，绝不拆成 4 张 1024。
3.  **LOD (Levels of Detail)**: 超过 500面的单位必须有 LOD1 (减面 50%)。

---

## 3. 🧠 策划 (Design: The Soul)

**核心痛点**: 数值崩坏 & 引导劝退。

### 🔴 绝对红线 (Must Not)
1.  **禁止“乘法堆叠”无上限**: 伤害公式中，独立乘区 (More Damage) 不能超过 3 个。必须引入**边际收益递减**。
2.  **禁止修改已上线 ID**: 任何配置表里的 `ID` 一旦推上线，**永不修改**，只能废弃 (`Deprecated`) 并新增。否则玩家存档会坏。
3.  **禁止无提示的机制杀**: 玩家死了一定要让他知道“怎么死的”。不能有“看不见的秒杀光环”。
4.  **禁止空投新机制**: 任何新机制（如：带护盾的怪）必须先在简单的关卡单独出现一次（教学），然后再混入怪群。

### 🟢 核心原则 (Must)
1.  **Excel 注释**: 每一个配表字段，必须写清楚单位（秒、毫秒、百分比）。`Speed: 100` 是 100米/秒 还是 100%？
2.  **保底机制 (Pity)**: 任何随机掉落（Roguelike 选卡、装备掉落）必须有伪随机保底。不能让非酋连续 10 次选不到核心卡。
3.  **预期管理**: 技能描述里的数值必须是**最终值**（绿色高亮），而不是基础值。

---

## 4. 🎵 音频 (Audio: The Vibe)

**核心痛点**: 听觉疲劳 & 爆音。

### 🔴 绝对红线 (Must Not)
1.  **禁止无限制叠加音效**: 同一帧播放同一个音效超过 3 次，必须被 `AudioManager` 拦截。
2.  **禁止 BGM 不循环**: 背景音乐必须完美 Loop，不能有明显的“断点”。
3.  **禁止 2D/3D 混用**: 只有 UI 音效是 2D 的。战场音效必须是 3D 的（或经过虚拟耳朵处理），否则玩家听声辨位会乱。

### 🟢 核心原则 (Must)
1.  **侧链压缩 (Ducking)**: 关键音效（大招、升级）播放时，必须自动压低背景音乐和杂音。
2.  **随机化**: 高频音效（普攻、脚步）必须有 Pitch/Volume 的微小随机扰动，防止机关枪效应。

---

## 5. 📦 版本与流程 (Pipeline)

### 🔴 绝对红线 (Must Not)
1.  **禁止提交“红名”代码**: 提交前必须本地编译通过，且无 Error Log。
2.  **禁止周五下午发版**: 除非你想毁了全组人的周末。
3.  **禁止私自升级 Unity 版本**: 引擎升级是全组的大事，必须由主程评估。

### 🟢 核心原则 (Must)
1.  **Commit Message**: 必须清晰。`Fix bug` 是垃圾提交。`Fix: 修复了箭塔在 30 级时攻速溢出的 Bug` 是好提交。
2.  **美术资源命名**: 严格遵守 `T_Icon_Sword_01` (Type_Category_Name_Variant) 的命名规范。

---

## 📚 扩展阅读与技术标准 (References)

### 🚀 性能优化
*   **[Unity Performance Best Practices](https://unity.com/how-to/unity-performance-best-practices)** (Official Unity)
    *   官方白皮书。必读章节：*Memory Management* 和 *Asset Auditing*。
*   **[10000 Update() calls vs 10000 Array iterations](https://blogs.unity3d.com/2015/12/23/1k-update-calls/)** (Unity Blog)
    *   用数据证明了为什么 **Update** 是性能杀手，以及为什么你应该用 Manager 统一轮询。

### 🎨 美术规范
*   **[The Technical Art of Sea of Thieves](https://www.youtube.com/watch?v=C2h6W52y474)** (GDC 2018)
    *   *盗贼之海* 的技术美术分享。展示了如何用最少的 DrawCall 实现最绚丽的风格化海洋。
*   **[Optimizing Graphics in Unity](https://learn.unity.com/tutorial/fixing-performance-problems)**
    *   Unity Learn 上的官方课程，详细讲解了 DrawCall Batching 和 GPU Instancing 的触发条件。

### 💻 代码架构
*   **[Level Up Your Code with Game Programming Patterns](https://gameprogrammingpatterns.com/)** (Bob Nystrom)
    *   *必读*: **Object Pool** 和 **Data Locality** 章节。这是高性能游戏编程的基石。