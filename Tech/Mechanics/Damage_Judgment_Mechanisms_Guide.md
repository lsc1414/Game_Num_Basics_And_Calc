# 🥊 伤害判定机制详解：Hitbox vs. Distance vs. Raycast

本文档详细解析游戏中伤害判定的三种核心流派：**基于数值的距离判定 (Distance Check)**、**基于模型的物理判定 (Hitbox/Collider)** 以及 **射线检测 (Raycast/Hitscan)**。

我们将探讨它们的原理、优缺点、适用场景，并结合 **FPS游戏**、**Monster Hunter**、**Elden Ring** 和 **Vampire Survivors** 等业界案例进行分析。

---

## 1. 理论基础 (Theoretical Foundation)

伤害判定的本质是回答一个问题：**“在攻击生效的瞬间，受害者是否处于攻击范围内？”**

### 1.1 距离判定 (Distance/Logic Check)
*   **原理:** 纯数学计算。不关心模型长什么样，只关心两个坐标点的距离和角度。
*   **公式:** `Distance(Attacker, Victim) <= Range + RadiiSum` AND `Angle(Forward, DirToVictim) <= ConeAngle/2`。
*   **特征:**
    *   **确定性 (Deterministic):** 只要在圈里，必中。
    *   **性能极高:** 简单的向量运算。
    *   **视觉偏差:** 可能出现“刀还没碰到怪，怪就掉血了”的情况（Phantom Range）。

### 1.2 物理判定 (Hitbox/Physics Check)
*   **原理:** 利用物理引擎的碰撞检测。
*   **实现:** 在武器模型上挂一个 `Collider` (Trigger)，在攻击动画挥动期间激活它。当它与敌人的 `Hurtbox` 重叠时触发事件。
*   **特征:**
    *   **精确性 (Pixel Perfect):** 只有刀刃划过身体才算中。
    *   **性能开销:** 物理引擎 (PhysX) 的开销比数学计算大得多。
    *   **不稳定性:** 容易发生穿模 (Tunneling)，高速挥动时可能检测不到。

### 1.3 射线判定 (Raycast/Hitscan Check)
*   **原理:** 从发射点向目标方向发射一条无限细的“光线”，检测第一个碰到的物体。
*   **实现:** `Physics.Raycast(origin, direction, out hitInfo, maxDistance)`。
*   **特征:**
    *   **瞬时性 (Instant):** 没有飞行时间，按下开火键即命中。
    *   **点对点:** 只要两点之间有障碍物，就会被挡住（极其精准的视线遮挡）。
    *   **体积忽略:** 射线没有厚度，极难命中细小的移动目标，通常需要配合“辅助瞄准”或“粗射线 (SphereCast)”。

---

## 2. 什么时候用什么？ (Decision Matrix)

| 场景 | 推荐方案 | 原因 |
| :--- | :--- | :--- |
| **FPS / TPS (CS:GO, Overwatch)** | **射线判定 (Hitscan)** | 枪械射击要求瞬时反馈，所见即所得。 |
| **Moba / RTS (LoL, Starcraft)** | **距离判定** | 强调竞技公平性。A出去就必须中，不能因为模型动作没碰到就Miss。 |
| **MMORPG (WoW, FF14)** | **距离判定** | 网络延迟存在，物理判定会导致严重的“我明明躲开了”的同步问题。 |
| **动作游戏 (DMC, Elden Ring)** | **混合模式** | 玩家攻击通常用物理判定（追求打击感）；怪物攻击常用距离判定（追求可靠性）。 |
| **割草游戏 (Vampire Survivors)** | **距离判定** | 同屏 500 个怪，用物理判定 CPU 会直接爆炸。 |
| **格斗游戏 (Street Fighter)** | **Hitbox (2D)** | 定义极其严格的矩形框，这是玩法的核心。 |

---

## 3. 深度实践指南 (Implementation Guide)

### 方案 A: 纯距离判定 (Distance Check) —— *塔防/ARPG小怪首选*
*同上，此处省略重复内容...*

### 方案 B: 物理判定 (Weapon Collider) —— *大型Boss/精确闪避首选*
*同上，此处省略重复内容...*

### 方案 C: 射线判定 (Raycast/SphereCast) —— *远程武器/狙击塔首选*

适合高速飞行的子弹、激光或瞬发的魔法攻击。

1.  **基础射线 (Raycast):**
    ```csharp
    if (Physics.Raycast(muzzlePos, direction, out RaycastHit hit, range, enemyLayer)) {
        ApplyDamage(hit.collider.gameObject);
    }
    ```
    *   *缺点:* 射线太细，容易穿过怪物的咯吱窝或两腿之间，导致“描边枪法”。

2.  **粗射线 (SphereCast / BoxCast):**
    *   想象发射一根粗壮的“圆柱体”而不是细线。
    *   `Physics.SphereCast(origin, radius, direction, out hit, maxDist)`。
    *   **优点:** 极大地提高了命中率，手感更好，允许稍微打偏一点也能中。

3.  **多段射线 (Multi-Raycast) - *霰弹枪*:**
    *   在一个圆锥体内随机发射 10 条射线。
    *   每条射线单独判定伤害。
    *   **效果:** 距离越近，命中的射线越多，伤害越高（贴脸暴击）。

---

## 4. 业界优秀案例 (Industry Case Studies)

### 🔫 Overwatch (守望先锋) —— *Hitscan 与 Projectile 的平衡*
*   **黑百合 (狙击):** 纯 Hitscan。鼠标点哪打哪，考验极致定位。
*   **半藏 (弓箭):** Projectile (有飞行时间的投射物)。实际上是一个带 Collider 的小球在飞。
*   **判定膨胀:** 为了照顾主机手柄玩家，角色的 Hitbox 比模型实际要大一圈（头部判定框像个大西瓜）。

### 🏆 Monster Hunter (怪物猎人) —— *精准 Hitbox 的极致*
*   **机制:** 极其严格的 Hitbox。龙的尾巴扫过，如果玩家正好在尾巴弯曲的空隙里，就不会受伤。

### 💍 Elden Ring (艾尔登法环) —— *混合的艺术*
*   **投技 (Grab):** 极其诡异的混合判定。看起来手还没碰到，但判定框已经到了，导致“空气抓取”。

### 🧛 Vampire Survivors (吸血鬼幸存者) —— *性能的妥协*
*   **机制:** 只有距离判定。

---

## 5. Project Vampirefall 建议 (Recommendation)

针对我们的 **塔防 + Roguelike** 混合类型：

1.  **普通怪物 & 防御塔 (近战):** 全面使用 **方案 A (距离判定)**。
2.  **玩家近战:** 使用 **方案 A (距离判定)** 但配合 **扇形检测 (Cone)**。
3.  **狙击塔 / 激光塔 / 枪械:** 使用 **方案 C (SphereCast)**。
    *   使用 `SphereCast` 而不是 `Raycast`，给射线 0.2m 的半径，防止因为怪物动画导致的判定丢失。
    *   **必须做遮挡检测:** 确保射线没有穿过墙壁。
4.  **Boss 关键技能:** 使用 **方案 B (物理判定)** 或 **延迟指示器 (Telegraphing)**。

---