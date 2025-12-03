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
*   **核心逻辑:** `Vector3.Distance(a, b) < (r1 + r2)`。
*   **优化技巧:**
    *   **平方距离比较:** 使用 `(a-b).sqrMagnitude < (r1+r2)^2`，避免开方运算 `Math.sqrt`，性能提升显著。
    *   **空间划分:** 使用 Quadtree 或 Grid 将 500 个怪物的 $O(N^2)$ 检测降低到 $O(N)$。
    *   **扇形检测:** 先做距离检测，再做 `Vector3.Dot` 点积检测角度。
*   **适用:** 塔防中的范围攻击（AoE）、Roguelike 中的割草技能。

### 方案 B: 物理判定 (Weapon Collider) —— *大型Boss/精确闪避首选*
*   **核心逻辑:** `OnTriggerEnter(Collider other)`。
*   **配置要点:**
    *   **Rigidbody:** 武器通常不需要刚体，或者设为 Kinematic。
    *   **LayerMatrix:** 严格设置碰撞矩阵，武器层只能撞击 `Hurtbox` 层，避免与墙壁或队友发生无意义的物理计算。
    *   **插值 (Interpolation):** 开启刚体插值，确保在低帧率下判定框平滑移动。
*   **适用:** 魂类游戏的翻滚闪避、Boss 的挥砍动作（玩家需要根据动作方向躲避）。

### 方案 C: 射线判定 (Raycast/SphereCast) —— *远程武器/狙击塔首选*

适合高速飞行的子弹、激光或瞬发的魔法攻击。

1.  **基础射线 (Raycast):**
    *   **原理:** `Physics.Raycast(origin, direction, out RaycastHit hit, range, enemyLayer)`。
    *   **代码示例:**
        ```csharp
        if (Physics.Raycast(muzzlePos, direction, out RaycastHit hit, range, enemyLayer)) {
            ApplyDamage(hit.collider.gameObject);
        }
        ```
    *   **缺点:** 射线太细，容易穿过怪物的咯吱窝或两腿之间，导致“描边枪法”。

2.  **粗射线 (SphereCast / BoxCast):**
    *   想象发射一根粗壮的“圆柱体”而不是细线。
    *   `Physics.SphereCast(origin, radius, direction, out hit, maxDist)`。
    *   **优点:** 极大地提高了命中率，手感更好，允许稍微打偏一点也能中。这是现代 FPS 的主流做法。

3.  **多段射线 (Multi-Raycast) - *霰弹枪*:**
    *   在一个圆锥体内随机发射 10 条射线。
    *   每条射线单独判定伤害。
    *   **效果:** 距离越近，命中的射线越多，伤害越高（贴脸暴击）。

### 3.4 复杂动作判定 (Advanced Animation Sync)
*不仅仅是旋转攻击，任何非瞬发动作都需要让“判定形状”匹配“动画轨迹”。*

#### A. 旋转攻击 (Spin / Whirlwind)
**问题:** 纯圆形判定会导致“刀未到，伤先至”。
**解法:** **多段扇形检测 (Multi-Stage Sector Check)**。
*   T+0.0s: 前方 90° -> T+0.1s: 右侧 90° -> ...
*   *Vampirefall 策略:* 高攻速下退化为全圆检测以节省性能。

#### B. 突刺 (Thrust / Stab)
**问题:** 动画是细长的直线，如果用圆形判定，会打到身侧的空气。
**解法:** **延迟矩形检测 (Delayed Box Check)**。
*   在刺击达到最远端的帧，检测前方一个长条形区域（如 长5m x 宽1m）。
*   或者使用 **粗射线 (SphereCast)**。

#### C. 下劈 (Overhead Smash)
**问题:** 动作有明显的前摇（举剑），如果按下键立刻伤害，毫无打击感。
**解法:** **关键帧触发 (Impact Frame)**。
*   必须严格在武器接触地面的那一帧触发判定。
*   判定区域通常是一个以落点为圆心的小圆（震波），加上前方的一小段矩形（剑身）。

**核心原则:** **判定形状 (Hit Shape) 必须拟合 动画轨迹 (Animation Trail)。**

---

## 4. 业界优秀案例 (Industry Case Studies)

### 🔫 Overwatch (守望先锋) —— *Hitscan 与 Projectile 的平衡*
*   **黑百合 (狙击):** 纯 Hitscan。鼠标点哪打哪，考验极致定位。
*   **半藏 (弓箭):** Projectile (有飞行时间的投射物)。实际上是一个带 Collider 的小球在飞。
*   **判定膨胀:** 为了照顾主机手柄玩家，角色的 Hitbox 比模型实际要大一圈（头部判定框像个大西瓜）。

### 🏆 Monster Hunter (怪物猎人) —— *精准 Hitbox 的极致*
*   **机制:** 极其严格的 Hitbox。龙的尾巴扫过，如果玩家正好在尾巴弯曲的空隙里，就不会受伤。这种精确性是硬核动作体验的基石。

### 💍 Elden Ring (艾尔登法环) —— *混合的艺术*
*   **投技 (Grab):** 极其诡异的混合判定。看起来手还没碰到，但判定框已经到了，导致“空气抓取”。这是为了平衡PVP延迟而做的妥协。

### 🧛 Vampire Survivors (吸血鬼幸存者) —— *性能的妥协*
*   **机制:** 只有距离判定。
*   **理由:** 当同屏有 1000 个怪时，物理碰撞是不可能的。所有的“武器”实际上都是以玩家为中心的数学公式（圆环、扇形、随机点）。

---

## 5. Project Vampirefall 选型指导 (Strategic Guide)

针对 **塔防 + Roguelike** 这一独特混合品类，我们需要在“海量单位性能”与“动作打击感”之间走钢丝。

### 5.1 核心原则：分级判定策略
不要试图用一种方案解决所有问题。按单位数量级分层：

| 单位类型 | 数量级 | 推荐方案 | 理由 |
| :--- | :--- | :--- | :--- |
| **海量杂兵 (Swarm)** | 100+ | **距离判定 (Distance)** | CPU 预算极为有限，必须使用最廉价的数学计算。配合 GPU Instancing 渲染。 |
| **精英怪 (Elite)** | 10-20 | **距离 + 扇形 (Sector)** | 需要一定的方向感，不能让怪屁股对着玩家也能打出伤害。 |
| **Boss** | 1 | **混合判定 (Hybrid)** | 普攻用距离，大招用物理 Hitbox 或复杂的射线组合，提供“可闪避”的交互空间。 |
| **防御塔 (Tower)** | 20-50 | **距离 (AoE) / 射线 (单体)** | 塔是静止的，不需要复杂的动作判定。 |

### 5.2 投射物选型：Hitscan vs. Projectile
*   **狙击塔/激光塔:** 必须用 **Hitscan (射线)**。
    *   *理由:* 避免“弹道飞行过程中怪死了”导致的伤害丢失（Overkill），保证高频塔的有效 DPS。
*   **火炮/法师塔:** 必须用 **Projectile (投射物)**。
    *   *理由:* 爆炸延迟和飞行轨迹是塔防的视觉核心。且慢速投射物允许玩家预判和操作（如用技能聚怪）。

### 5.3 混乱环境下的预警机制 (Telegraphing)
在肉鸽后期，屏幕上全是特效。
*   **Boss 技能:** 严禁使用“无前摇”的 Hitbox 判定。
*   **解决方案:** 必须先在地面绘制 **预警贴花 (Decal)**（红色矩形/扇形），延迟 0.5秒 后再进行伤害判定。
*   **判定逻辑:** 实际上是检测“谁站在了预警贴花里”，而不是检测“谁被 Boss 模型碰到了”。这在视觉混乱时最公平。

### 5.4 网络同步考量 (Multiplayer Considerations)
如果未来支持联机 Co-op：
*   **防守方有利 (Defender's Advantage):** 伤害判定应在**客户端**先行预演（显示扣血数字），服务器做最终校验。
    *   **位置宽容:** 由于网络延迟，怪物的实际位置可能与客户端不同。服务器在校验距离时，应给予额外 **0.5米 ~ 1.0米** 的宽容度 (Buffer)，防止“明明打到了却没伤”的挫败感。

### 5.5 英雄多武器判定架构 (Hero Weapon Architecture)
针对 Vampirefall 英雄拥有多种武器（太刀、大剑、弓、弩）且具备招式连段（Combo）的特点，建议采用 **组件化判定框架**。

#### A. 架构设计
将“攻击逻辑”从代码中剥离，封装为可插拔的模组 (`ScriptableObject`):
*   `MeleeSlashModule`: 负责扇形/矩形检测。
*   `PhysicsHitboxModule`: 负责激活武器上的 Collider。
*   `ProjectileModule`: 负责生成子弹实体。
*   `HitscanModule`: 负责发射射线。

#### B. 武器特定实现
1.  **太刀 (Katana) - *快节奏/多段判定***
    *   **普攻 (Slash):** 使用 **延迟矩形检测**。速度快，不需要精确 Hitbox，保证命中率优先。
    *   **旋风斩 (Spin):** 使用 **多段扇形检测** (如前文 3.4 所述)，确保 360° 无死角且时序正确。
    *   **居合 (Iaijutsu):** 使用 **超长距离 Hitscan** 或 **超大矩形**，强调“瞬杀”感。

2.  **大剑 (Greatsword) - *慢节奏/重打击***
    *   **横扫 (Wide Swing):** 建议开启 **Physics Hitbox**。因为动作慢，玩家会盯着剑刃看，穿模会很明显。且物理判定能天然支持“打到墙壁弹刀”的硬核机制。
    *   **下劈 (Slam):** 严格的 **Impact Frame** 触发震波 (AoE 圆形)。

3.  **长弓 (Bow) - *物理手感***
    *   使用 **Projectile (实体箭矢)**。
    *   **抛物线:** 加上重力，让玩家体验“吊射”的乐趣。
    *   **蓄力:** 蓄力时间决定箭矢的初速度和穿透力。

4.  **轻弩 (Crossbow) - *机械精准***
    *   使用 **Hitscan (射线)** 或 **极高速 Projectile**。
    *   强调指哪打哪，适合快速清理高威胁目标（如自爆怪）。

#### C. 数据驱动配置
每个武器的每一招（Combo 1, 2, 3）都应配置一个 `WeaponMoveSet`：
```csharp
class WeaponMove {
    public float DamageMult;
    public float ImpactTime; // 判定生效时间点
    public HitType Type; // Melee, Projectile...
    public Vector3 HitboxSize; // 仅近战有效
}
```
---