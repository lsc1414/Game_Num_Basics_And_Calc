# 🏷️ Unity 资产命名规范与强制检查工具

**文档目标：** 建立统一的资产“语言”，并提供自动化工具确保执行。
**核心逻辑：** `[前缀]_[模块/类别]_[名称]_[变体/后缀]`

---

## 1. 📜 命名规范详情 (The Standards)

### 1.1 基础规则
1.  **语言：** 严禁中文命名。使用英文 (PascalCase 或 snake_case)。
2.  **分隔符：** 使用下划线 `_` 分隔前缀和主体。
3.  **文件夹约束：** 特定资产必须放在特定文件夹下（如 UI 图片必须在 `Assets/Art/UI`）。

### 1.2 前缀对照表 (Prefix Table)

| 资产类型 (Asset Type) | 前缀 (Prefix) | 示例 (Example) | 备注 |
| :--- | :--- | :--- | :--- |
| **场景 (Scene/Level)** | `L_` | `L_MainMenu`, `L_Dungeon_01` | L 代表 Level |
| **预制体 (Prefab)** | `P_` | `P_GoblinWarrior`, `P_Coin` | 最常用的前缀 |
| **材质球 (Material)** | `M_` | `M_HeroSkin`, `M_Water` | |
| **纹理 (Texture/Model)** | `T_` | `T_Brick_Albedo`, `T_Brick_Normal` | 通用纹理 |
| **UI 图片 (Sprite)** | `UI_` | `UI_Button_Close`, `UI_Icon_Sword` | 区分于模型贴图 |
| **模型 (Mesh)** | `SM_` / `SK_` | `SM_Tree` (静), `SK_Hero` (动) | Static / Skinned |
| **动画片段 (Anim Clip)** | `Anim_` | `Anim_Hero_Run`, `Anim_Door_Open` | |
| **动画控制器 (Animator)** | `AC_` | `AC_Hero`, `AC_Door` | |
| **音频 (Audio)** | `SFX_` / `BGM_` | `SFX_Explosion`, `BGM_BossFight` | 区分音效与背景乐 |
| **着色器 (Shader)** | `Sh_` | `Sh_ToonWater` | |
| **物理材质 (Phys Mat)** | `PM_` | `PM_Bouncy`, `PM_Ice` | |
| **粒子系统 (Particle)** | `FX_` | `FX_FireBall`, `FX_Rain` | 通常指 Prefab |

### 1.3 后缀对照表 (Suffix Table - 纹理专用)

| 贴图类型 | 后缀 | 示例 |
| :--- | :--- | :--- |
| **基础颜色 (Albedo/Diffuse)** | `_D` 或 无 | `T_Wall_D` |
| **法线 (Normal)** | `_N` | `T_Wall_N` |
| **金属/光滑 (Metallic/Gloss)** | `_M` | `T_Wall_M` |
| **环境光遮蔽 (AO)** | `_AO` | `T_Wall_AO` |
| **自发光 (Emission)** | `_E` | `T_Wall_E` |
| **蒙版 (Mask)** | `_Mask` | `T_Wall_Mask` |

---

## 2. 👮‍♂️ 强制检查脚本 (The Enforcer Script)

将下方的脚本放入项目的 `Assets/Editor` 文件夹中。它拥有以下功能：

1.  **自动检查：** 每当你导入或移动资源时，检查前缀是否合规。
2.  **强力报警：** 如果命名错误，控制台会输出 **红色 Error**。
3.  **一键修复：** 右键点击资源 -> `Tools/Fix Naming Prefix` 自动添加前缀。

### 使用方法
1.  在 `Assets` 下创建一个名为 `Editor` 的文件夹（如果还没有）。
2.  将生成的 `AssetNamingValidator.cs` 放入其中。
3.  尝试创建一个材质球命名为 `New Material`，你会看到控制台报错。

---

## 3. ⚙️ 配置说明

脚本中的 `_prefixRules` 字典可以根据你的项目需求进行修改。

```csharp
// 示例：如果你想让材质球的前缀变成 "Mat_"
{ typeof(Material), "Mat_" },
```

---

## 4. 💡 为什么不自动重命名？ (Why No Auto-Rename?)

虽然脚本有能力在导入时自动重命名，但**强烈不建议**开启自动重命名：
1.  **引用丢失：** 如果代码中使用了 `Resources.Load("WrongName")`，自动重命名会导致代码崩溃。
2.  **Meta 文件混乱：** 频繁的自动重命名可能导致 Git 历史记录混乱。
3.  **开发者意识：** 只有通过报错让开发者手动修改（或使用右键工具），才能培养良好的命名习惯。
