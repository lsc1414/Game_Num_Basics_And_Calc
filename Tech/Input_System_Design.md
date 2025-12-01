# 🎮 输入与交互系统设计 (Input & Interaction Framework)

本文档定义了游戏的输入映射、跨平台适配策略以及 UI 导航逻辑。建议使用 Unity 的新版 Input System 包。

---

## 1. 输入动作映射 (Action Maps)

我们将输入逻辑分为三个独立的 Action Map，根据游戏状态动态切换。

### 1.1 Gameplay (战斗状态)
| 动作 | 键鼠 (PC) | 手柄 (Xbox) | 说明 |
| :--- | :--- | :--- | :--- |
| **Move** | WASD | 左摇杆 | 角色移动 |
| **Aim** | 鼠标位置 | 右摇杆 | 瞄准方向 |
| **Primary Fire** | 左键 | RT / R2 | 普通攻击 |
| **Secondary Fire** | 右键 | LT / L2 | 特殊攻击/格挡 |
| **Skill 1** | Q | LB / L1 | 技能槽位 1 |
| **Skill 2** | E | RB / R1 | 技能槽位 2 |
| **Dash** | Space | A / Cross | 闪避/冲刺 |
| **Interact** | F | X / Square | 与塔、NPC、掉落物交互 |
| **Build Mode** | B / Tab | Y / Triangle | 切换到建造模式 |

### 1.2 BuildMode (建造模式)
进入此模式后，时间流速减慢 (Time Scale = 0.1)，方便从容布局。

| 动作 | 键鼠 (PC) | 手柄 (Xbox) | 说明 |
| :--- | :--- | :--- | :--- |
| **Select Tower** | 1-4 / 滚轮 | D-Pad 左右 | 切换待建造的塔类型 |
| **Rotate** | R | RB / LB | 旋转塔朝向 |
| **Place** | 左键 | A / Cross | 确认建造 |
| **Cancel** | 右键 / Esc | B / Circle | 退出建造模式 |

### 1.3 UI (界面导航)
当打开暂停菜单或全屏界面时激活。

*   **手柄支持:** 必须支持“虚拟光标”或“UI 焦点吸附” (Navigation)，不能让手柄玩家无法操作菜单。

## 2. 辅助功能 (Accessibility)

*   **按键重映射 (Remapping):** 必须允许玩家在设置中更改所有键位。
*   **连点辅助 (Hold to Spam):** 对于普攻，允许“按住”代替“狂点”，保护玩家手指。
*   **手柄震动 (Haptics):** 
    *   *轻震:* 造成暴击。
    *   *重震:* 受到伤害、Boss登场。

## 3. 交互系统逻辑 (Interaction Logic)

### 3.1 软锁定 (Soft Lock)
*   **键鼠:** 精确指向鼠标位置。
*   **手柄:** 
    *   **近战:** 自动吸附面向方向 45度 扇形内最近的敌人。
    *   **远程:** 带有轻微的磁吸 (Magnetism)，当准星掠过敌人时减慢灵敏度。

### 3.2 智能交互 (Contextual Interaction)
*   当按下 `Interact` 键时，根据优先级判定：
    1.  **复活队友** (如果是多人模式)。
    2.  **维修/升级塔** (如果准星对准塔)。
    3.  **开启宝箱**。
    4.  **拾取关键道具**。

## 4. UI 提示 (Glyphs)
*   根据检测到的输入设备，动态切换 UI 上的按键图标。
*   *检测:* 如果检测到手柄输入，显示 "Press [A]"; 如果检测到鼠标移动，显示 "Press [Space]".

