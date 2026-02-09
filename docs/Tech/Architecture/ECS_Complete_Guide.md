# ECS 综合指南

> 本文档由以下文件合并生成 (2026-01-09)



---


<!-- 来源: Tech\Architecture\ECS_Theory_And_Practice.md -->

## 🧩 ECS 理论与实践：从面向对象 (OOP) 到数据导向 (DOD) 的思维跃迁

## 1. 什么是 ECS？ (What is ECS?)

**实体组件系统 (Entity Component System, ECS)** 是一种遵循 **组合优于继承 (Composition over Inheritance)** 原则的架构模式。它将游戏对象的数据与行为彻底分离。

### 1.1 三大支柱
*   **Entity (实体)**: 仅仅是一个 **ID** (通常是 `int` 或 `uint`)。它不包含任何数据，也不包含任何函数。它只是组件的容器索引。
*   **Component (组件)**: **纯数据** (Struct)。它只包含字段 (Fields)，不包含方法 (Methods)。
    *   *例子*: `Position { x, y }`, `Velocity { x, y }`, `Health { current, max }`.
*   **System (系统)**: **纯逻辑**。它负责筛选拥有特定组件集合的实体，并批量处理它们。
    *   *例子*: `MovementSystem` 筛选所有拥有 `Position` 和 `Velocity` 的实体，执行 `Pos += Vel * dt`。
## 2. 为什么要放弃 OOP？ (Why abandon OOP?)
在传统的面向对象编程 (OOP) 中，我们习惯于：
### 2.1 OOP 的原罪
1.  **继承的噩梦 (Diamond Problem)**:
    *   如果需要一个“既能飞又能游泳”的怪物，是继承 `FlyingMonster` 还是 `SwimmingMonster`？多重继承极其复杂。
2.  **缓存未命中 (Cache Miss)**:

    *   OOP 对象在堆内存中是随机分布的。CPU 在处理 `Player` 时，预取不到下一个对象的数据，导致 CPU 经常停下来等待内存（性能杀手）。
3.  **耦合过重**:
    *   `Player` 类往往包含了移动、攻击、动画、音效等所有逻辑，变成一个几千行的 "God Class"。

### 2.2 DOD 的救赎
**数据导向设计 (Data-Oriented Design)** 关注数据的内存布局。
*   **连续内存**: 同类组件（如所有 `Velocity`）在内存中紧密排列。
*   **批量处理**: CPU 可以像流水线一样处理数据，极大利用 L1/L2 缓存。
## 3. 思维跃迁：如何从 OOP 转为 ECS？
这是一个从“我是谁”到“我有什么”的转变。
### 3.1 转变一：对象 -> ID
*   **OOP**: 我手里拿着一个 `Player` 对象引用。
*   **ECS**: 我手里拿着一个 `EntityID` (整数)。
### 3.2 转变二：属性 -> 组件
不要把所有数据都塞进一个类。根据**功能**拆分数据。
|          OOP 属性          |          ECS 组件          |
|          `class Monster { bool isStunned; }`          |          `struct StunTag : IComponentData {}` (空组件，仅作标记)          |
### 3.3 转变三：方法 -> 系统
不要在类里写 `Update()`。思考“这个行为需要什么数据”。
**OOP 写法**:
**ECS 写法**:
        // 筛选: 有 Position, 有 Speed, 但没有 StunTag 的实体
## 4. 实战案例：重构“吸血鬼幸存者”逻辑
假设我们要实现：**当玩家捡起磁铁道具时，全屏所有的经验宝石飞向玩家。**

### 4.1 OOP 实现 (痛苦面具)
1.  `Player` 碰撞到 `Magnet`。
2.  `Player` 调用 `GameManager.Instance.GetAllGems()`。
3.  遍历所有 `Gem` 对象，调用 `gem.SetTarget(player)`。
4.  `Gem.Update()` 中判断如果有 Target，则向 Target 移动。
*   *缺点*: 需要维护全局列表，Gem 类逻辑变复杂，内存跳跃访问。
### 4.2 ECS 实现 (优雅高效)
1.  **组件设计**:
    *   `MagnetBuffComponent`: 标记玩家捡到了磁铁。
    *   `MoveToTargetComponent { Entity target; }`: 给宝石用的组件。
2.  **系统设计**:
        *   检测到玩家有 `MagnetBuff`。
        *   查询所有拥有 `GemTag` 的实体。
        *   **批量添加** `MoveToTargetComponent { target = player }` 给这些实体。
        *   查询所有拥有 `Position` 和 `MoveToTargetComponent` 的实体。
        *   计算方向，更新 Position。

### 4.3 优势总结
*   **解耦**: 宝石完全不知道“磁铁”的存在，它只知道“我有了一个追踪目标”。
*   **性能**: `HomingSystem` 只处理需要追踪的物体，不需要遍历所有物体来判断 `if (target != null)`。
*   **扩展性**: 如果想要“黑洞技能”吸怪，只需要给怪物添加 `MoveToTargetComponent`，逻辑完全复用。
## 5. 常见误区 (Common Pitfalls)

1.  **组件里写逻辑**: ❌ 绝对禁止。组件必须是纯数据 Struct。
2.  **系统间直接调用**: ❌ 系统应该通过**修改组件数据**来通信，而不是直接调用另一个系统的方法。

3.  **过度拆分**: ⚠️ 不要把 `x` 和 `y` 拆成两个组件。通常相关联的数据（如位置和旋转）可以放在一起，或者根据访问频率拆分。
## 6. 总结
ECS 不仅仅是性能优化工具，更是一种**架构解耦**的利器。它强迫开发者关注**数据流 (Data Flow)** 而非对象状态，这在处理复杂交互（如技能系统、Buff系统）时会带来意想不到的清晰度。
<!-- 来源: Dev_Guides\Technical_Implementation\ECS_Performance_Optimization.md -->
## 🚀 ECS 性能优化实战：从 Vampire Survivors 到 Unity DOTS
**文档目标**：解析如何在 Unity 中实现同屏 500+ 敌人的高性能逻辑，参考 *Vampire Survivors* 的优化思路，并映射到 Unity DOTS (Data-Oriented Technology Stack) 的最佳实践。同时结合本项目特有的 **GAS (Gameplay Ability System)** 进行混合架构设计。

## 1. 为什么传统 OOP (面向对象) 会卡？
在传统的 `MonoBehaviour` 方式中，每个怪物都是一个 GameObject。

### 💀 性能杀手名单：
1.  **内存碎片与缓存未命中 (Cache Miss)**：
    *   **现象**: 怪物数据 (`Enemy` 类) 散落在堆内存的各个角落。
    *   **原理**: CPU 读取内存的速度远慢于计算速度。当 CPU 处理 `EnemyA` 时，它会将附近内存块加载到 L1/L2 缓存（Prefetching）。但如果 `EnemyB` 在内存的另一头，预取失效，CPU 必须停下来等待内存读取（Cache Miss）。这是性能的头号杀手。
2.  **GC 压力 (Garbage Collection)**：
    *   大量的临时对象实例化和销毁（如子弹、掉落物）导致 GC 频繁触发，造成卡顿。
3.  **Transform 同步开销**：
    *   Unity 引擎层 (C++) 和脚本层 (C#) 之间的 `transform.position` 交互有封送（Marshalling）开销。
4.  **Update() 调用开销**：
    *   500 个 `Update()` 方法的虚函数调用本身就是巨大的 CPU 负担。

## 2. 核心解法：数据导向设计 (DOD)
**Data-Oriented Design (DOD)** 的核心思想是：**CPU 喜欢处理连续的、简单的数据块。**
### 2.1 结构体数组 (SoA) vs 数组结构体 (AoS)
*   **AoS (Array of Structs) - OOP 常用**:
    *   **问题**：如果系统只想更新位置（Position += Speed * dt），CPU 缓存行里却被迫加载了不用的 HP 数据，浪费了宝贵的缓存带宽。
*   **SoA (Struct of Arrays) - ECS 推荐**:
    *   **优势**：
        1.  **缓存命中率极高**: 当移动系统运行时，只加载 Pos 和 Speed 数组，每一字节的数据都是有用的。
        2.  **SIMD 优化**: 现代 CPU 可以用一条指令同时处理 4 个或 8 个浮点数（Vectorization）。连续的数组天然适合 SIMD。
## 3. Vampire Survivors 的优化魔法
虽然 *Vampire Survivors* 早期是基于 Phaser (JS) 开发的，但其优化逻辑通用：
### 3.1 伪物理碰撞 (Fake Physics)
不要给 500 个怪物挂 `Rigidbody` 或 `BoxCollider`。
*   **网格法 (Spatial Hashing)**：将地图划分为小格子。只检测同一格子或相邻格子内的单位。
*   **圆圆碰撞 (Circle-Circle)**：`DistanceSquared(A, B) < (R1+R2)^2`。避免开方运算。
*   **“推挤”而非“物理”**：怪物重叠时，根据重叠向量给一个排斥力，而不是物理引擎的刚体解算。
### 3.2 对象池 (Object Pooling) 2.0
*   不仅复用 GameObject，还要**复用数据结构**。
*   **Loot Reservoir (掉落蓄水池)**：经验宝石不总是实例化。如果地上超过 50 个宝石，将新掉落的经验值“合并”到最近的宝石上，或创建一个特殊的“红宝石”来吸收全屏经验。
## 4. Unity 实现方案 (从入门到进阶)

### 🟢 方案 A：简易版 (Job System + Burst)
不使用完整的 Entities 包，仅用 Job System 优化计算。
*   **适用**：项目中期优化，不想重写整个架构。
*   **收益**：移动计算移至多线程，Burst 编译器优化数学运算。
### 🟡 方案 B：GPU Instancing 渲染
逻辑再快，渲染 500 个 DrawCall 也会死。
*   使用 `Graphics.DrawMeshInstanced` 或 `DrawMeshInstancedIndirect`。
*   将所有怪物的 Position/Rotation/Color 塞入 `ComputeBuffer`，一次提交给 GPU。

### 🔴 方案 C：Pure ECS (Unity DOTS)
*   **Entities**：纯数据实体 ID。
*   **Components**：`IComponentData` (struct)，如 `MoveSpeedData`, `HealthData`。
*   **Systems**：`SystemBase` 或 `ISystem`，只负责逻辑。
## 5. 深度整合：ECS + GAS 混合架构
在 **Project Vampirefall** 中，我们结合 [Gameplay Ability System (GAS)](../../Tech/Gameplay_Ability_System_Design.md) 设计，采用混合架构。
### 5.1 架构图
*   **Hero / Boss**: `MonoBehaviour` + `AbilitySystemComponent (C# Class)`。处理复杂逻辑、动画状态机。
*   **Minions (500+)**: `ECS Entity` + `BuffBuffer (DynamicBuffer)`。处理移动、简单攻击、Buff 状态。
### 5.2 案例：特斯拉电塔 vs 虫群
**场景**: 特斯拉电塔释放“连锁闪电”，击中 50 个敌人，造成伤害并施加“感电” Debuff。
**流程**:
1.  **触发 (Mono)**: 电塔 (GameObject) 的 `GA_ChainLightning` 触发。
2.  **查询 (ECS)**: 通过 `EntityQuery` 瞬间找到范围内最近的 50 个带有 `Tag_Enemy` 的实体。

3.  **应用 (ECS Job)**:
    *   创建一个 `ApplyEffectJob`。
    *   并行写入：扣除 HP (`Health -= Damage`)。
    *   并行写入：向实体的 `BuffBuffer` 添加 `GE_Shock` (感电) 的 ID。
4.  **表现 (Hybrid)**:
    *   Job 输出被击中实体的坐标列表。
    *   主线程根据坐标生成 50 条闪电链 VFX (使用 ParticleSystem 或 LineRenderer)。

**代码片段：Buff 处理系统 (ECS)**
        // 遍历所有拥有 Buff 缓冲区的实体
                // 处理持续时间
                // 处理 Buff 逻辑 (例如：每秒伤害)
                // 移除过期 Buff
## 6. 实战检查清单 (Checklist)

1.  [ ] **去 Mono化**：核心高频逻辑（移动、碰撞）剥离 MonoBehaviour。
2.  [ ] **关闭物理**：小怪禁用 Rigidbody，使用自定义轻量级碰撞。
3.  [ ] **批量渲染**：确保怪物材质支持 GPU Instancing。

4.  [ ] **结构体代替类**：数据层尽可能使用 `struct` 以利用 SoA 优势。
5.  [ ] **混合同步**：仅在必要时（如播放死亡动画）将 ECS 数据同步回 GameObject。
## 7. 性能预算参考

|          平台          |          同屏目标 (60FPS)          |          DrawCalls 限制          |          物理计算耗时          |
|          PC (Mid)          |          2000+          |          < 1500 (Batching后)          |          < 3ms          |

---

## 6. æ»ç»
ECS ä¸ä»ä»æ¯æ§è½ä¼åå·¥å·ï¼æ´æ¯ä¸ç§?*æ¶æè§£è?*çå©å¨ãå®å¼ºè¿«å¼åèå³æ³?*æ°æ®æµ?(Data Flow)** èéå¯¹è±¡ç¶æï¼è¿å¨å¤çå¤æäº¤äºï¼å¦æè½ç³»ç»ãBuffç³»ç»ï¼æ¶ä¼å¸¦æ¥ææ³ä¸å°çæ¸æ°åº¦ã?




---


{/* æ¥æº: Dev_Guides\Technical_Implementation\ECS_Performance_Optimization.md */}

## ð ECS æ§è½ä¼åå®æï¼ä» Vampire Survivors å?Unity DOTS

**ææ¡£ç®æ **ï¼è§£æå¦ä½å¨ Unity ä¸­å®ç°åå±?500+ æäººçé«æ§è½é»è¾ï¼åè?*Vampire Survivors* çä¼åæè·¯ï¼å¹¶æ å°å?Unity DOTS (Data-Oriented Technology Stack) çæä½³å®è·µãåæ¶ç»åæ¬é¡¹ç®ç¹æç?**GAS (Gameplay Ability System)** è¿è¡æ··åæ¶æè®¾è®¡ã?

---

## 1. ä¸ºä»ä¹ä¼ ç»?OOP (é¢åå¯¹è±¡) ä¼å¡ï¼?

å¨ä¼ ç»ç `MonoBehaviour` æ¹å¼ä¸­ï¼æ¯ä¸ªæªç©é½æ¯ä¸ä¸?GameObjectã?

### ð æ§è½ææååï¼
1.  **åå­ç¢çä¸ç¼å­æªå½ä¸­ (Cache Miss)**ï¼?
    *   **ç°è±¡**: æªç©æ°æ® (`Enemy` ç±? æ£è½å¨å åå­çåä¸ªè§è½ã?
    *   **åç**: CPU è¯»ååå­çéåº¦è¿æ¢äºè®¡ç®éåº¦ãå½ CPU å¤ç `EnemyA` æ¶ï¼å®ä¼å°éè¿åå­åå è½½å?L1/L2 ç¼å­ï¼Prefetchingï¼ãä½å¦æ `EnemyB` å¨åå­çå¦ä¸å¤´ï¼é¢åå¤±æï¼CPU å¿é¡»åä¸æ¥ç­å¾åå­è¯»åï¼Cache Missï¼ãè¿æ¯æ§è½çå¤´å·ææã?
2.  **GC åå (Garbage Collection)**ï¼?

    *   å¤§éçä¸´æ¶å¯¹è±¡å®ä¾ååéæ¯ï¼å¦å­å¼¹ãæè½ç©ï¼å¯¼è?GC é¢ç¹è§¦åï¼é æå¡é¡¿ã?
3.  **Transform åæ­¥å¼é**ï¼?

    *   Unity å¼æå±?(C++) åèæ¬å± (C#) ä¹é´ç?`transform.position` äº¤äºæå°éï¼Marshallingï¼å¼éã?
4.  **Update() è°ç¨å¼é**ï¼?

    *   500 ä¸?`Update()` æ¹æ³çèå½æ°è°ç¨æ¬èº«å°±æ¯å·¨å¤§ç?CPU è´æã?

---

## 2. æ ¸å¿è§£æ³ï¼æ°æ®å¯¼åè®¾è®?(DOD)

**Data-Oriented Design (DOD)** çæ ¸å¿ææ³æ¯ï¼**CPU åæ¬¢å¤çè¿ç»­çãç®åçæ°æ®åã?*

### 2.1 ç»æä½æ°ç»?(SoA) vs æ°ç»ç»æä½?(AoS)

*   **AoS (Array of Structs) - OOP å¸¸ç¨**:
    *   `[ {HP, Pos, Speed}, {HP, Pos, Speed}, ... ]`
    *   **é®é¢**ï¼å¦æç³»ç»åªæ³æ´æ°ä½ç½®ï¼Position += Speed * dtï¼ï¼CPU ç¼å­è¡éå´è¢«è¿«å è½½äºä¸ç¨ç?HP æ°æ®ï¼æµªè´¹äºå®è´µçç¼å­å¸¦å®½ã?

*   **SoA (Struct of Arrays) - ECS æ¨è**:
    *   `Pos: [P1, P2, P3...]`
    *   `Speed: [S1, S2, S3...]`
    *   `HP: [H1, H2, H3...]`
    *   **ä¼å¿**ï¼?
        1.  **ç¼å­å½ä¸­çæé«?*: å½ç§»å¨ç³»ç»è¿è¡æ¶ï¼åªå è½½ Pos å?Speed æ°ç»ï¼æ¯ä¸å­èçæ°æ®é½æ¯æç¨çã?
        2.  **SIMD ä¼å**: ç°ä»£ CPU å¯ä»¥ç¨ä¸æ¡æä»¤åæ¶å¤ç?4 ä¸ªæ 8 ä¸ªæµ®ç¹æ°ï¼Vectorizationï¼ãè¿ç»­çæ°ç»å¤©ç¶éå SIMDã?

---

## 3. Vampire Survivors çä¼åé­æ³?

è½ç¶ *Vampire Survivors* æ©ææ¯åºäº?Phaser (JS) å¼åçï¼ä½å¶ä¼åé»è¾éç¨ï¼?

### 3.1 ä¼ªç©çç¢°æ?(Fake Physics)
ä¸è¦ç»?500 ä¸ªæªç©æ?`Rigidbody` æ?`BoxCollider`ã?

*   **ç½æ ¼æ³?(Spatial Hashing)**ï¼å°å°å¾ååä¸ºå°æ ¼å­ãåªæ£æµåä¸æ ¼å­æç¸é»æ ¼å­åçåä½ã?
*   **ååç¢°æ (Circle-Circle)**ï¼`DistanceSquared(A, B) < (R1+R2)^2`ãé¿åå¼æ¹è¿ç®ã?
*   **âæ¨æ¤âèéâç©çâ?*ï¼æªç©éå æ¶ï¼æ ¹æ®éå åéç»ä¸ä¸ªææ¥åï¼èä¸æ¯ç©çå¼æçåä½è§£ç®ã?

### 3.2 å¯¹è±¡æ±?(Object Pooling) 2.0
*   ä¸ä»å¤ç¨ GameObjectï¼è¿è¦?*å¤ç¨æ°æ®ç»æ**ã?
*   **Loot Reservoir (æè½èæ°´æ±?**ï¼ç»éªå®ç³ä¸æ»æ¯å®ä¾åãå¦æå°ä¸è¶è¿?50 ä¸ªå®ç³ï¼å°æ°æè½çç»éªå¼âåå¹¶âå°æè¿çå®ç³ä¸ï¼æåå»ºä¸ä¸ªç¹æ®çâçº¢å®ç³âæ¥å¸æ¶å¨å±ç»éªã?

---

## 4. Unity å®ç°æ¹æ¡ (ä»å¥é¨å°è¿é¶)

### ð¢ æ¹æ¡ Aï¼ç®æç (Job System + Burst)
ä¸ä½¿ç¨å®æ´ç Entities åï¼ä»ç¨ Job System ä¼åè®¡ç®ã?

*   **éç¨**ï¼é¡¹ç®ä¸­æä¼åï¼ä¸æ³éåæ´ä¸ªæ¶æã?
*   **æ¶ç**ï¼ç§»å¨è®¡ç®ç§»è³å¤çº¿ç¨ï¼Burst ç¼è¯å¨ä¼åæ°å­¦è¿ç®ã?

### ð¡ æ¹æ¡ Bï¼GPU Instancing æ¸²æ
é»è¾åå¿«ï¼æ¸²æ?500 ä¸?DrawCall ä¹ä¼æ­»ã?

*   ä½¿ç¨ `Graphics.DrawMeshInstanced` æ?`DrawMeshInstancedIndirect`ã?
*   å°æææªç©ç?Position/Rotation/Color å¡å¥ `ComputeBuffer`ï¼ä¸æ¬¡æäº¤ç» GPUã?

### ð´ æ¹æ¡ Cï¼Pure ECS (Unity DOTS)
*   **Entities**ï¼çº¯æ°æ®å®ä½ IDã?
*   **Components**ï¼`IComponentData` (struct)ï¼å¦ `MoveSpeedData`, `HealthData`ã?
*   **Systems**ï¼`SystemBase` æ?`ISystem`ï¼åªè´è´£é»è¾ã?

---

## 5. æ·±åº¦æ´åï¼ECS + GAS æ··åæ¶æ

å?**Project Vampirefall** ä¸­ï¼æä»¬ç»å [Gameplay Ability System (GAS)](../../Tech/Gameplay_Ability_System_Design.md) è®¾è®¡ï¼éç¨æ··åæ¶æã?

### 5.1 æ¶æå?
*   **Hero / Boss**: `MonoBehaviour` + `AbilitySystemComponent (C# Class)`ãå¤çå¤æé»è¾ãå¨ç»ç¶ææºã?
*   **Minions (500+)**: `ECS Entity` + `BuffBuffer (DynamicBuffer)`ãå¤çç§»å¨ãç®åæ»å»ãBuff ç¶æã?

### 5.2 æ¡ä¾ï¼ç¹æ¯æçµå¡ vs è«ç¾¤

**åºæ¯**: ç¹æ¯æçµå¡éæ¾âè¿ééªçµâï¼å»ä¸­ 50 ä¸ªæäººï¼é æä¼¤å®³å¹¶æ½å âæçµâ?Debuffã?

**æµç¨**:

1.  **è§¦å (Mono)**: çµå¡ (GameObject) ç?`GA_ChainLightning` è§¦åã?
2.  **æ¥è¯¢ (ECS)**: éè¿ `EntityQuery` ç¬é´æ¾å°èå´åæè¿ç 50 ä¸ªå¸¦æ?`Tag_Enemy` çå®ä½ã?

3.  **åºç¨ (ECS Job)**:

    *   åå»ºä¸ä¸?`ApplyEffectJob`ã?
    *   å¹¶è¡åå¥ï¼æ£é?HP (`Health -= Damage`)ã?
    *   å¹¶è¡åå¥ï¼åå®ä½ç?`BuffBuffer` æ·»å  `GE_Shock` (æçµ) ç?IDã?
4.  **è¡¨ç° (Hybrid)**:

    *   Job è¾åºè¢«å»ä¸­å®ä½çåæ åè¡¨ã?
    *   ä¸»çº¿ç¨æ ¹æ®åæ çæ?50 æ¡éªçµé¾ VFX (ä½¿ç¨ ParticleSystem æ?LineRenderer)ã?

**ä»£ç çæ®µï¼Buff å¤çç³»ç» (ECS)**
```csharp
[BurstCompile]
public partial struct BuffProcessingSystem : ISystem
{
    public void OnUpdate(ref SystemState state)
    {
        float dt = SystemAPI.Time.DeltaTime;
        
        // éåæææ¥æ?Buff ç¼å²åºçå®ä½
        foreach (var buffBuffer in SystemAPI.Query<DynamicBuffer<ActiveBuff>>())
        {
            for (int i = 0; i < buffBuffer.Length; i++)
            {
                // å¤çæç»­æ¶é´
                var buff = buffBuffer[i];
                buff.RemainingTime -= dt;
                
                // å¤ç Buff é»è¾ (ä¾å¦ï¼æ¯ç§ä¼¤å®?
                if (buff.TypeId == BuffIDs.Poison) {
                    // ... Apply Damage Logic ...
                }

                // ç§»é¤è¿æ Buff
                if (buff.RemainingTime <= 0) {
                    buffBuffer.RemoveAt(i);
                    i--;
                }
            }
        }
    }
}
```

---

## 6. å®ææ£æ¥æ¸å?(Checklist)

1.  [ ] **å?Monoå?*ï¼æ ¸å¿é«é¢é»è¾ï¼ç§»å¨ãç¢°æï¼å¥ç¦» MonoBehaviourã?
2.  [ ] **å³é­ç©ç**ï¼å°æªç¦ç?Rigidbodyï¼ä½¿ç¨èªå®ä¹è½»éçº§ç¢°æã?

3.  [ ] **æ¹éæ¸²æ**ï¼ç¡®ä¿æªç©æè´¨æ¯æ GPU Instancingã?

4.  [ ] **ç»æä½ä»£æ¿ç±»**ï¼æ°æ®å±å°½å¯è½ä½¿ç?`struct` ä»¥å©ç?SoA ä¼å¿ã?

5.  [ ] **æ··ååæ­¥**ï¼ä»å¨å¿è¦æ¶ï¼å¦æ­æ¾æ­»äº¡å¨ç»ï¼å° ECS æ°æ®åæ­¥å?GameObjectã?

## 7. æ§è½é¢ç®åè?

|          å¹³å°          |          åå±ç®æ  (60FPS)          |          DrawCalls éå¶          |          ç©çè®¡ç®èæ¶          |
|          :---          |          :---          |          :---          |          :---          |
|          PC (Mid)          |          2000+          |          < 1500 (Batchingå?          |          < 3ms          |
|          Mobile (High)          |          500+          |          < 300          |          < 4ms          |
|          Mobile (Low)          |          100+          |          < 100          |          < 5ms          |



