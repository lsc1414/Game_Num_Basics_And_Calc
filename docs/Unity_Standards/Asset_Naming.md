---
sidebarTitle: "Unity 资产命名规范与强制检查工具"
title: "Unity 资产命名规范与强制检查工具"
---
> **摘要**：本文围绕「Unity 资产命名规范与强制检查工具」提供核心内容与可落地方法。

---

**文档目标：** 建立统一的资产“语言”，解决项目后期“找不到资源”的噩梦。
**核心逻辑：** `[前缀]_[模块/类别]_[名称]_[变体/后缀]`

---

## 1. 🕵️ 真实开发场景演示 (Real-World Workflows)

规范只是枯燥的列表，我们来看看在实际开发中，**一整套**资源是如何命名的。

### 场景 A：制作一个敌人 "Goblin Warrior" (哥布林战士)

目标：在 Project 窗口搜索 "Goblin"，所有相关文件整齐排列，不混杂其他东西。

|          资源类型                   |          推荐命名                         |          解释                                                     |
|          :----------------          |          :----------------------          |          :----------------------------------------------          |
|          **源模型 (FBX)**           |          `SK_GoblinWarrior`               |          **注意：** Warrior 紧跟 Goblin，不用下划线。             |
|          **基础纹理**               |          `T_GoblinWarrior_D`              |          `_D` = Diffuse/Albedo (颜色)。                           |
|          **法线纹理**               |          `T_GoblinWarrior_N`              |          `_N` = Normal Map。                                      |
|          **材质球**                 |          `M_GoblinWarrior`                |          材质球通常与模型同名，去掉前缀。                         |
|          **材质球 (变体)**          |          `M_GoblinWarrior_Elite`          |          红色皮肤的精英版变体。                                   |
|          **动画控制器**             |          `AC_Goblin`                      |          所有哥布林共用一套逻辑，所以不加 `_Warrior`。            |
|          **预制体 (最终)**          |          `P_GoblinWarrior`                |          **这是程序和策划唯一关心的文件**。                       |
|          **预制体 (变体)**          |          `P_GoblinWarrior_Elite`          |          引用了 `M_GoblinWarrior_Elite` 的精英怪预制体。          |

### 场景 B：搭建一个 "Dungeon" (地牢) 场景

目标：模块化拼装。区分“地砖”、“墙壁”和“装饰物”。

|          资源类型                     |          推荐命名                         |          解释                                                                |
|          :------------------          |          :----------------------          |          :---------------------------------------------------------          |
|          **静态模型 (墙)**            |          `SM_DungeonWall_01`              |          `SM` = Static Mesh。使用数字编号区分样式。                          |
|          **静态模型 (转角)**          |          `SM_DungeonWall_Corner`          |          功能性后缀。                                                        |
|          **静态模型 (地板)**          |          `SM_DungeonFloor_01`             |                                                                              |
|          **贴图 (可复用)**            |          `T_StoneGrey_D`                  |          这是一个通用贴图，可能被墙和地共用，所以不叫 `T_Dungeon`。          |
|          **预制体 (带碰撞)**          |          `P_DungeonWall_01`               |          加上了 BoxCollider 的成品墙。                                       |
|          **场景文件**                 |          `L_DungeonLevel_01`              |          `L` = Level。                                                       |

### 场景 C：UI 按钮状态 (图片资源)

目标：区分图片的用途，防止把 3D 贴图用到 UI 上。

|          资源类型                 |          推荐命名                       |          解释                            |
|          :--------------          |          :--------------------          |          :---------------------          |
|          **图标**                 |          `UI_Icon_SwordIron`            |          图标类。                        |
|          **按钮 (底图)**          |          `UI_Btn_Common_Norm`           |          通用按钮 - 正常状态。           |
|          **按钮 (悬停)**          |          `UI_Btn_Common_Hover`          |          通用按钮 - 鼠标悬停。           |
|          **按钮 (按下)**          |          `UI_Btn_Common_Press`          |          通用按钮 - 按下状态。           |
|          **按钮 (禁用)**          |          `UI_Btn_Common_Dis`            |          通用按钮 - 禁用/灰态。          |

### 场景 D：预制体深度命名 (Prefab Specifics)

目标：让成百上千个 Prefab 在文件夹里自动归类，而不是乱成一团。

#### **1. UI 预制体 (P*UI*)**

- **规则:** `P_UI_[Layer]_[Feature]_[Sub]`
- `P_UI_Panel_Settings` (设置面板 - 全屏)
- `P_UI_Popup_Confirm` (确认弹窗 - 模态)
- `P_UI_HUD_PlayerInfo` (战斗界面 - 玩家信息)
- `P_UI_Item_InventorySlot` (列表项 - 背包格子，会被大量克隆的小组件)

#### **2. 技能/子弹预制体 (P*Skill* / P*Bullet*)**

- **规则:** `P_Skill_[Owner]_[Element]_[Name]`
- `P_Skill_Hero_Fire_Fireball` (主角火球)
- `P_Skill_Hero_Ice_FrostNova` (主角冰环)
- `P_Bullet_Arrow_Wood` (普通木箭)
- `P_Bullet_Magic_Missile` (魔法飞弹)
- `FX_Hit_Fire_Small` (命中特效 - 属于 P*FX* 类别)

#### **3. 角色预制体 (P*Char*)**

- `P_Hero_Archer` (主角 - 弓箭手)
- `P_Enemy_Slime_Green` (敌人 - 绿史莱姆)
- `P_Boss_Dragon_Red` (Boss - 红龙)
- `P_NPC_Merchant` (NPC - 商人)

---

## 2. ➖ 下划线的艺术：何时连接，何时切断？

下划线 `_` 在计算机世界里通常代表 **"层级 (Hierarchy)"** 或 **"分割 (Split)"**。乱用下划线会导致名字支离破碎。

### 2.1 黄金法则：Snake_Pascal (蛇形大驼峰)

我们推荐一种混合命名法：**用下划线分割层级，用大驼峰连接单词。**

- **✅ 正确:** `T_DarkKnight_D`
    - 解析: [T] 是前缀，[DarkKnight] 是主体，[D] 是后缀。结构清晰 (A_B_C)。
- **❌ 错误:** `T_Dark_Knight_D`
    - 解析: 到底是 `Dark_Knight` 是主体？还是 `Dark` 是主体，`Knight` 是变体？
    - 后果: 当你写脚本解析文件名时，`string.Split('_')` 会得到 4 段，逻辑变复杂。

### 2.2 必须用下划线的场景 (Must Use)

1.  **前缀之后:** `P_`, `T_`, `M_`。这是为了让排序时，所有同类资源聚在一起。
2.  **后缀之前:** `_D`, `_N`, `_01`, `_Hover`。这是为了标记变体。

3.  **核心分类与名称之间:** `UI_Btn_Close`。这里 `Btn` 是分类，`Close` 是名称。

### 2.3 禁止用下划线的场景 (Must Avoid)

1.  **复合名词内部:**
    - ❌ `Fire_Ball`
    - ✅ `FireBall`
    - _理由:_ 它们是一个整体概念，不要切断。
2.  **形容词与名词之间:**

    - ❌ `Big_Boss`
    - ✅ `BigBoss`
3.  **系列编号之前 (除非是后缀):**

    - ❌ `Level_01_Boss`
    - ✅ `Level01_Boss` (如果 Level01 是一个整体概念)

### 2.4 为什么这么较真？ (Tooling Impact)

很多工具依赖下划线来工作：

- **Texture Packer (UI 打包):** 默认使用下划线识别动画序列。`Run_01`, `Run_02` 会被打包成 `Run` 动画。如果你写成 `Hero_Run_01`，它可能认为这是 `Hero` 组下的 `Run` 动画。如果你写成 `Hero_Fast_Run_01`，它就晕了。
- **Substance Painter:** 导出贴图时，通常自动加 `_BaseColor`。保持主体部分干净 (`DarkKnight`) 可以确保导出文件名整洁。

---

## 3. 🔠 大小写的语义学：为什么要这么写？

大小写规则不仅仅是好不好看，它是**代码的表情符号**。理解了语义，你就不需要死记硬背。

### 3.1 PascalCase (大驼峰) —— 🎩 尊贵的类型

- **规则:** 每个单词首字母大写。 `PlayerController`, `GetDamage`
- **语义:** 代表**公开的、重要的、定义性质的**东西。
- **应用:**
    - `class` (类名): `Enemy`
    - `function` (方法名): `Attack()`
    - `public` 变量: `public float Health;`
    - **资产文件名:** `P_GoblinWarrior` (除了前缀，主体部分用 PascalCase)

### 3.2 camelCase (小驼峰) —— 🐁 内部的数据

- **规则:** 首字母小写，后续单词首字母大写。 `moveSpeed`, `enemyTarget`
- **语义:** 代表**私有的、内部的、实例性质的**数据。感觉比较“轻”。
- **应用:**
    - 局部变量: `float distance = ...`
    - 参数: `void Attack(float damageAmount)`

### 3.3 \_camelCase (下划线小驼峰) —— 🔒 私有的字段

- **规则:** 下划线开头 + 小驼峰。 `_currentHealth`, `_playerTransform`
- **语义:** **"私人财产，请勿触碰"**。
- **应用:**
    - `private` 成员变量: `private float _timer;`
    - _好处:_ 在代码里看到 `_` 开头的变量，你就知道它是全局的私有变量，而不是函数里的临时变量。

### 3.4 SCREAMING_SNAKE_CASE (尖叫蛇) —— ⚠️ 警告/常量

- **规则:** 全大写，下划线分隔。 `MAX_HP`, `DEFAULT_SPEED`
- **语义:** **"我在尖叫！我是常量！不要试图修改我！"**
- **应用:**
    - `const` 常量: `const int MAX_ENEMIES = 100;`
    - `static readonly` 静态只读配置。

### 3.5 总结对照表

|          场景                       |          推荐写法               |          示例                                |          心理暗示                        |
|          :----------------          |          :------------          |          :-------------------------          |          :---------------------          |
|          **文件名/资产名**          |          **Pascal**             |          `Player.cs`, `T_Icon.png`           |          "我是个正经文件"                |
|          **类名/函数名**            |          **Pascal**             |          `class Boss`, `void Die()`          |          "我是个重要概念"                |
|          **Public 变量**            |          **Pascal**             |          `public int Score;`                 |          "大家都可以来访问我"            |
|          **Private 变量**           |          **\_camel**            |          `private int _hp;`                  |          "我是内部隐私，别乱动"          |
|          **参数/局部变量**          |          **camel**              |          `int damage`                        |          "我只是个临时工"                |
|          **常量**                   |          **SCREAMING**          |          `PI`, `MAX_COUNT`                   |          "我是宇宙真理"                  |

---

## 4. 🆘 非母语者的命名生存指南 (Survival Guide for Non-Native Speakers)

对于中文团队，强制英文命名最大的障碍是词汇量和拼写错误。为了避免 `T_GongJi_Tx` (拼音缩写) 这种可怕的东西出现，请遵守以下“生存法则”。

### 4.1 📚 受控词表 (Controlled Vocabulary)

**不要去翻牛津词典！** 游戏开发中用到的高频词只有这 100 个。请全员打印并贴在显示器旁边，**强制只用这些词**。

#### **🅰️ 通用动作 (Actions)**

|          中文               |          英文 (推荐)                |          备选/特定                              |          错误示例 (勿用)           |
|          :--------          |          :----------------          |          :----------------------------          |          :---------------          |
|          **待机**           |          `Idle`                     |                                                 |          `Wait`, `Stand`           |
|          **跑/走**          |          `Run` / `Walk`             |          `Sprint` (冲刺)                        |          `Go`, `Move`              |
|          **攻击**           |          `Atk` / `Attack`           |          `Shoot` (射击), `Cast` (施法)          |          `Hit` (这是受击)          |
|          **受击**           |          `Hit`                      |          `Damage`, `Hurt`                       |          `BeAtk`                   |
|          **死亡**           |          `Die` / `Death`            |          `Dead`                                 |          `Over`                    |
|          **出生**           |          `Spawn`                    |          `Born`                                 |          `Start`                   |
|          **眩晕**           |          `Stun`                     |          `Dizzy`                                |          `Yun`                     |
|          **拾取**           |          `Pick` / `Pickup`          |          `Loot`                                 |          `Get`                     |
|          **使用**           |          `Use`                      |          `Consume`                              |                                    |

#### **🧱 物体与材质 (Materials)**

|          中文                 |          英文 (推荐)          |          备选/特定                                |          错误示例 (勿用)          |
|          :----------          |          :----------          |          :------------------------------          |          :--------------          |
|          **木**               |          `Wood`               |                                                   |          `Tree`                   |
|          **石**               |          `Stone`              |          `Rock` (自然岩石), `Brick` (砖)          |                                   |
|          **金/铁**            |          `Metal`              |          `Iron`, `Gold`                           |          `Tie`                    |
|          **肉/生物**          |          `Flesh`              |          `Organic`                                |          `Meat`                   |
|          **水**               |          `Water`              |          `Liquid`                                 |          `Shui`                   |
|          **火**               |          `Fire`               |          `Flame`                                  |                                   |
|          **光**               |          `Light`              |          `Glow`                                   |                                   |
|          **地面**             |          `Ground`             |          `Terrain`, `Floor` (室内)                |          `Land`                   |
|          **墙**               |          `Wall`               |                                                   |                                   |

#### **🧛 角色与职业 (Roles)**

|          中文              |          英文 (推荐)          |          备选/特定                        |          错误示例 (勿用)          |
|          :-------          |          :----------          |          :----------------------          |          :--------------          |
|          **主角**          |          `Hero`               |          `Player`, `Char`                 |          `Main`                   |
|          **敌人**          |          `Enemy`              |          `Mob` (小怪), `Monster`          |          `BadGuy`                 |
|          **Boss**          |          `Boss`               |                                           |          `Big`                    |
|          **精英**          |          `Elite`              |                                           |          `JingYing`               |
|          **小兵**          |          `Minion`             |          `Creep`                          |          `Small`                  |
|          **近战**          |          `Melee`              |                                           |          `Close`                  |
|          **远程**          |          `Ranged`             |                                           |          `Far`                    |
|          **NPC**           |          `NPC`                |                                           |                                   |

#### **📊 RPG 核心属性 (Stats & Attributes)**

_参考来源: Path of Exile, Dota 2, Genshin Impact_

|          中文                  |          英文 (全称)                      |          缩写 (推荐)                  |          备注/易错点                                       |
|          :-----------          |          :----------------------          |          :------------------          |          :---------------------------------------          |
|          **力量**              |          `Strength`                       |          `Str`                        |          别拼成 Strong                                     |
|          **敏捷**              |          `Dexterity`                      |          `Dex`                        |          别拼成 Agility (虽然也对，但 Dex 更常用)          |
|          **智力**              |          `Intelligence`                   |          `Int`                        |                                                            |
|          **攻击力**            |          `Attack`                         |          `Atk`                        |          物理/普攻基础值                                   |
|          **防御力**            |          `Defense`                        |          `Def`                        |          综合防御值                                        |
|          **生命值**            |          `Health Point`                   |          `HP`                         |          MaxHP / CurHP                                     |
|          **魔法值**            |          `Mana Point`                     |          `MP`                         |                                                            |
|          **护甲**              |          `Armor`                          |          `Armor`                      |          专指物理减伤                                      |
|          **魔抗**              |          `Magic Resistance`               |          `MR` / `Res`                 |                                                            |
|          **攻击速度**          |          `Attack Speed`                   |          `Aspd` / `AtkSpd`            |          别用 Speed (那是移速)                             |
|          **移动速度**          |          `Move Speed`                     |          `Mspd` / `MovSpd`            |                                                            |
|          **暴击率**            |          `Critical Rate`                  |          `Crit` / `CritRate`          |          Rate 是几率                                       |
|          **暴击伤害**          |          `Critical Damage`                |          `CritDmg`                    |                                                            |
|          **闪避**              |          `Dodge` / `Evasion`              |          `Eva`                        |          Dodge 通常指完全规避                              |
|          **命中**              |          `Accuracy` / `Hit Rate`          |          `Acc`                        |                                                            |
|          **穿透**              |          `Penetration`                    |          `Pen`                        |          ArmorPen / MagicPen                               |
|          **冷却时间**          |          `Cooldown`                       |          `CD`                         |                                                            |
|          **冷却缩减**          |          `Cooldown Reduction`             |          `CDR`                        |                                                            |
|          **范围**              |          `Range` / `Radius`               |          `Range`                      |          Radius 指半径                                     |
|          **持续时间**          |          `Duration`                       |          `Dur`                        |                                                            |

#### **🔮 特殊机制与状态 (Mechanics)**

|          中文              |          英文 (推荐)                     |          解释                                            |
|          :-------          |          :---------------------          |          :-------------------------------------          |
|          **吸血**          |          `Leech` / `Lifesteal`           |          Leech 通常指缓慢回血，Lifesteal 指瞬间          |
|          **回复**          |          `Regen` (Regeneration)          |          每秒回血/回蓝                                   |
|          **护盾**          |          `Shield` / `Barrier`            |          覆盖在血量上的额外层                            |
|          **无敌**          |          `Invincible`                    |          不受伤害                                        |
|          **霸体**          |          `Unstoppable`                   |          受伤害但不被控制                                |
|          **嘲讽**          |          `Taunt`                         |          强制目标攻击自己                                |
|          **沉默**          |          `Silence`                       |          无法施法                                        |
|          **禁锢**          |          `Root` / `Bind`                 |          无法移动                                        |
|          **流血**          |          `Bleed`                         |          物理持续伤害                                    |
|          **点燃**          |          `Ignite` / `Burn`               |          火焰持续伤害                                    |
|          **中毒**          |          `Poison`                        |          毒素持续伤害                                    |
|          **AOE**           |          `AOE`                           |          Area of Effect (范围伤害)                       |
|          **DOT**           |          `DOT`                           |          Damage over Time (持续伤害)                     |
|          **DPS**           |          `DPS`                           |          Damage per Second (秒伤)                        |

#### **🖥️ UI 与界面 (Interface)**

|          中文                     |          英文 (推荐)                  |          备选/特定                      |          错误示例 (勿用)          |
|          :--------------          |          :------------------          |          :--------------------          |          :--------------          |
|          **面板 (全屏)**          |          `Panel`                      |          `View`, `Page`                 |          `Big`                    |
|          **弹窗 (小)**            |          `Popup`                      |          `Dialog`, `Window`             |          `Tip`                    |
|          **组件 (子项)**          |          `Item`                       |          `Slot` (格子), `Cell`          |          `Small`                  |
|          **抬头显示**             |          `HUD`                        |          `Overlay`                      |          `UI_Fight`               |
|          **按钮**                 |          `Btn` / `Button`             |                                         |          `AnNiu`                  |
|          **图标**                 |          `Icon`                       |                                         |          `Image`, `Logo`          |
|          **背景**                 |          `Bg` / `Background`          |                                         |          `Back`                   |
|          **边框**                 |          `Frame`                      |          `Border`                       |          `Kuang`                  |
|          **进度条**               |          `Bar`                        |          `Slider`                       |          `Process`                |
|          **文本**                 |          `Txt` / `Text`               |          `Label`                        |          `Font`                   |
|          **选中**                 |          `Select`                     |          `Focus`                        |          `Choose`                 |
|          **禁用**                 |          `Disable`                    |          `Lock`                         |          `No`                     |

### 4.2 🛠️ 拼写检查工具

1.  **PowerToys Run (Windows):** 按 `Alt + Space` 呼出搜索框，输入中文直接查英文。
2.  **编辑器插件:** 使用 VS Code 或 Rider 的拼写检查插件 (SpellChecker)。如果代码里的变量名下面有波浪线，说明你拼错了，赶紧改，不要带到资源名里。

### 4.3 🇨🇳 拼音特赦区 (The Pinyin Exception)

什么时候可以用拼音？
只有当**这个概念在英文中完全没有对应词**，或者**翻译过去会丢失核心神韵**时。

- **✅ 允许:** `Wuxia` (武侠), `Jianghu` (江湖), `Qigong` (气功), `GuanYu` (关羽 - 专有名词)。
- **❌ 禁止:** `Shouqiang` (Pistol), `Daguai` (Farming), `Boss_1_Sihou` (Roar)。

### 4.4 📏 缩写规范

为了避免 `Pos` 是 Position 还是 Possess 的歧义，只允许使用**通用缩写**：

- `Pos` = Position
- `Rot` = Rotation
- `Dir` = Direction
- `Tex` = Texture
- `Mat` = Material
- `Mgr` = Manager
- `Ctrl` = Controller
- `Cfg` = Config

---

## 5. 📜 基础规范详情 (The Standards)

### 5.1 基础规则

1.  **语言：** 严禁中文命名。使用英文 (PascalCase 或 snake_case)。
2.  **分隔符：** 使用下划线 `_` 分隔前缀和主体。

3.  **文件夹约束：** 特定资产必须放在特定文件夹下（如 UI 图片必须在 `Assets/Art/UI`）。

### 5.2 🔤 前缀对照表 (Prefix Table)

|          资产类型 (Asset Type)                 |          前缀 (Prefix)            |          示例 (Example)                           |          备注                                  |
|          :---------------------------          |          :--------------          |          :------------------------------          |          :---------------------------          |
|          **🎬 场景 (Scene/Level)**             |          `L_`                     |          `L_MainMenu`, `L_Dungeon_01`             |          Level, 方便搜索 `t:scene L_`          |
|          **📦 预制体 (Prefab)**                |          `P_`                     |          `P_Coin`, `P_Hero`                       |          **最核心资产**                        |
|          **🎨 材质球 (Material)**              |          `M_`                     |          `M_HeroSkin`, `M_Water`                  |                                                |
|          **🖼️ 纹理 (Texture)**                 |          `T_`                     |          `T_Brick_D`, `T_Brick_N`                 |          3D 模型用的贴图                       |
|          **🖱️ UI 图片 (Sprite)**               |          `UI_`                    |          `UI_Btn_Close`, `UI_Icon_Skill`          |          **2D/UI 专用**，区别于 T\_            |
|          **🗿 模型 (Mesh)**                    |          `SM_` / `SK_`            |          `SM_Tree` (静), `SK_Hero` (动)           |          Static / Skinned                      |
|          **💃 动画片段 (Anim Clip)**           |          `Anim_`                  |          `Anim_Run`, `Anim_Attack_01`             |                                                |
|          **🎮 动画控制器 (Animator)**          |          `AC_`                    |          `AC_Hero`, `AC_Door`                     |                                                |
|          **🔊 音频 (Audio)**                   |          `SFX_` / `BGM_`          |          `SFX_Hit`, `BGM_Boss`                    |                                                |
|          **🌈 着色器 (Shader)**                |          `Sh_`                    |          `Sh_ToonWater`                           |                                                |
|          **✨ 粒子系统 (Particle)**            |          `FX_`                    |          `FX_Explosion`                           |          指 Prefab 形式的特效                  |

### 5.3 🔡 后缀对照表 (Suffix Table - 纹理专用)

|          贴图类型                       |          后缀           |          说明                                          |
|          :--------------------          |          :----          |          :-----------------------------------          |
|          **基础颜色 (Albedo)**          |          `_D`           |          Diffuse / BaseColor                           |
|          **法线 (Normal)**              |          `_N`           |          Normal Map                                    |
|          **金属/粗糙 (Mask)**           |          `_M`           |          Metallic (R) + Smoothness (A) 复合图          |
|          **环境光遮蔽 (AO)**            |          `_AO`          |                                                        |
|          **自发光 (Emission)**          |          `_E`           |                                                        |

---

## 6. 💡 常见困惑解答 (FAQ)

### Q1: 为什么要区分 `T_` (Texture) 和 `UI_` (Sprite)?

- **A:** 它们的导入设置完全不同！
    - `T_` 通常是 POT (2 的次幂)，开启 Mipmaps，使用 DXT/ASTC 压缩。
    - `UI_` 通常是 NPOT (任意尺寸)，**关闭** Mipmaps，开启 Sprite Packer，关闭压缩或用高质量压缩。
    - 命名区分后，可以写脚本自动根据前缀设置 Import Settings，省去人工检查的麻烦。

### Q2: 什么时候用 `_01`, `_02`，什么时候用 `_A`, `_B`?

- **数字 (`_01`):** 用于**同类枚举**。
    - _例子:_ `SM_Rock_01`, `SM_Rock_02`, `SM_Rock_03` (都是石头，随便用哪个都行)。
- **字母 (`_A`):** 用于**风格/状态变体**。
    - _例子:_ `UI_Icon_Skill_A` (方形版), `UI_Icon_Skill_B` (圆形版)。

### Q3: 脚本 (Script) 需要前缀吗？

- **A:** **不需要** `S_` 或 `Cs_` 前缀。
- 脚本类名直接作为文件名：`PlayerController.cs`, `GameManager.cs`。
- _原因:_ 脚本在代码中被引用时，前缀会破坏代码的可读性 (`S_Player.Move()` 很难看)。

---

## 7. 👮‍♂️ 强制检查脚本 (The Enforcer Script)

将下方的脚本放入项目的 `Assets/Editor` 文件夹中。

```csharp
using UnityEditor;
using UnityEngine;
using System.Collections.Generic;
using System.IO;

public class AssetNamingValidator : AssetPostprocessor
{
    // 核心配置：什么类型 -> 对应什么前缀
    private static readonly Dictionary<System.Type, string> _prefixRules = new Dictionary<System.Type, string>()
    {
        { typeof(Material), "M_" },
        { typeof(GameObject), "P_" }, // 预制体
        { typeof(Texture2D), "T_" },  // 基础纹理
        { typeof(Sprite), "UI_" },    // 精灵/UI (需要额外判断)
        { typeof(AudioClip), "SFX_" }, // 默认音效 (BGM_ 需手动例外)
        { typeof(Shader), "Sh_" },
    };

    static void OnPostprocessAllAssets(string[] importedAssets, string[] deletedAssets, string[] movedAssets, string[] movedFromAssetPaths)
    {
        foreach (string path in importedAssets) CheckAsset(path);
        foreach (string path in movedAssets) CheckAsset(path);
    }

    static void CheckAsset(string path)
    {
        // 1. 忽略非 Assets 目录或系统包
        if (!path.StartsWith("Assets/") || path.Contains("Packages/") || path.Contains("/Plugins/")) return;

        // 2. 忽略 Editor 脚本和 Meta 文件
        if (path.Contains("/Editor/") || path.EndsWith(".cs") || path.EndsWith(".meta")) return;

        string fileName = Path.GetFileNameWithoutExtension(path);
        Object asset = AssetDatabase.LoadAssetAtPath<Object>(path);
        if (asset == null) return;

        System.Type type = asset.GetType();

        // 3. 特殊处理：Prefab vs Model
        if (asset is GameObject)
        {
            // 如果是 FBX 模型，前缀应为 SK_ 或 SM_，这里简化检查
            // 真实项目中可通过 AssetImporter 判断是 Model 还是 Prefab
            return;
        }

        // 4. 检查前缀
        if (_prefixRules.TryGetValue(type, out string expectedPrefix))
        {
            // 特殊处理：UI 图片
            if (type == typeof(Texture2D))
            {
                TextureImporter importer = AssetImporter.GetAtPath(path) as TextureImporter;
                if (importer != null && importer.textureType == TextureImporterType.Sprite)
                {
                    expectedPrefix = "UI_";
                }
            }

            if (!fileName.StartsWith(expectedPrefix))
            {
                Debug.LogWarning($"⚠️ [Naming Violation] Asset '{fileName}' should start with '{expectedPrefix}'\nPath: {path}");
            }
        }
    }
}
```
