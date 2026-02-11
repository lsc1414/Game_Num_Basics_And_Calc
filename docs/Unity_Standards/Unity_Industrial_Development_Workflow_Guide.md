---
sidebarTitle: "Unity 工业化标准流程指南"
title: "Unity 游戏开发工业化标准流程指南"
---
> **摘要**：本文聚焦 Unity 工业化开发流程，覆盖资产导入、Prefab 结构、场景组织、物理层矩阵、碰撞体、材质规范、版本协作与提交流程。

**适用范围**：中大型独立游戏、长期维护项目、多人协作项目。  
**核心哲学**：一切皆预制体（Everything is a Prefab）；数据与逻辑分离。

## 1. 资产导入与 Prefab 规范

这是工业化流程的基石。在大型项目中，美术和程序并行工作，错误导入习惯会导致合并冲突与逻辑丢失。

### 1.1 错误做法（新手常见）

直接把 `.fbx` 拖入场景后，在该实例上挂脚本、改材质、加碰撞体，或在 FBX Import Settings 中直接勾选 `Generate Colliders`。

常见后果：
- 逻辑丢失：美术覆盖 FBX 后，层级或组件引用可能被重置，脚本配置丢失。
- 重复劳动：同一物体跨多个场景重复手动配置，后续修改成本极高。
- 版本冲突：多人同时改同一个 Scene 文件，难以合并。

### 1.2 工业化做法：容器模式与逻辑解耦

核心原则：**FBX 是原材料，Prefab 是成品**。

#### A. 模型导入标准（Import Settings）

1. `Scale Factor`：导入后缩放必须正确，不允许依赖 Transform 手调 100/0.01。  
2. `Materials`：使用 `Do Not Import Materials` 或统一提取材质，不使用 FBX 内嵌材质。  
3. `Rig`：静态物体用 `None`，道具用 `Generic`，角色用 `Humanoid`。

#### B. 容器模式结构（Container Pattern）

推荐结构如下：

```text
▼ Chair_Prefab (Root)
      Component: NetworkObject (联机ID)
      Component: Rigidbody
      Component: Collider
      Component: InteractionScript (交互逻辑)

      ▼ Visual (Layer: Default)
            Component: MeshFilter (Chair_Model / FBX)
            Component: MeshRenderer

      ▼ VFX_SpawnPoint (空物体 - 特效生成点)
```

优势：替换模型时只动 `Visual` 子节点，根节点逻辑与物理不受影响。

#### C. 变体与嵌套（Variants & Nested Prefabs）

- 基类预制体：`Scrap_Base`（包含通用逻辑组件）。
- 变体预制体：`Scrap_Engine`、`Scrap_Bottle`（只替换模型与局部参数）。
- 价值：修复基类逻辑后，全部变体自动继承。

## 2. 场景结构管理

标准关卡层级示例：

```text
▼ Level_01 (Scene)
  ▼ _Management (不销毁的管理器)
    ▶ NetworkManager
    ▶ GameManager
    ▶ InputManager
  ▼ _Environment (静态环境，标记为 Static)
    ▼ Geometry (墙、地)
    ▼ Props (不可互动的装饰)
    ▼ Lights
  ▼ _Gameplay (动态物体)
    ▶ SpawnPoints
    ▶ Interactables (你的废料、开关)
    ▶ AI_Agents
  ▼ _Debug (开发工具，打包时自动剔除)
```

关键规范：
- 系统级物体使用 `_` 前缀，便于置顶排序。
- 纯组织用父节点坐标保持 `(0,0,0)`。

## 3. 物理层与碰撞矩阵

不要把所有对象都放在 `Default`。

### 3.1 Layer 规划建议

| Layer ID | Name | 用途 |
| --- | --- | --- |
| 6 | Terrain/Ground | 地面与落脚点检测 |
| 7 | Wall | 墙体遮挡、阻挡 |
| 8 | Interactable | 交互对象射线检测 |
| 9 | Player | 玩家本体 |
| 10 | PlayerHand | 手持物体 |
| 11 | Enemy | 敌人 |
| 12 | Debris | 视觉碎片 |
| 13 | Trigger | 触发器 |

### 3.2 Collision Matrix 建议

在 `Edit > Project Settings > Physics > Layer Collision Matrix` 中精简碰撞关系：
- 关闭 `Player vs Player`（无互推需求时）。
- 关闭 `Debris vs Debris`。
- 关闭 `Debris vs Player`。
- 视玩法关闭 `Interactable vs Player`。

## 4. 碰撞体制作流程

### 4.1 静态场景

- 视觉网格与碰撞网格分离：
  - `Visual_Mesh`：高模，仅渲染。
  - `Collision_Mesh`：低模，仅碰撞。
- 避免高面数 MeshCollider 直接用于整场景。

### 4.2 动态道具

- 优先使用 Primitive Collider（Box/Sphere/Capsule）。
- 复杂形体使用复合碰撞体（Compound Colliders），避免单个 MeshCollider。

## 5. 材质与贴图规范

- 优先复用 Shader，不因颜色差异复制 Shader。  
- 使用材质变体或 `MaterialPropertyBlock` 控制个体差异。  
- 贴图建议采用打包图（如 MOS：`Metallic=R, Occlusion=G, Smoothness=B/A`）减少采样与内存。

## 6. 版本控制协作规范

场景文件（`.unity`）难以合并，必须避免多人同时修改同一 Scene。

推荐多场景工作流：
- `Level_Layout.unity`（美术）
- `Level_Logic.unity`（程序）
- `Level_Audio.unity`（音频）

通过多场景同时加载并行开发，降低冲突。

## 7. 提交前检查清单（Pre-Commit）

1. 无 `Missing Prefab` / 丢失引用。  
2. 场景根目录无测试垃圾对象。  
3. 灯光烘焙状态正确（或明确使用 Realtime）。  
4. 静态环境对象正确标记 `Static`（关系到 Occlusion Culling / NavMesh）。

## 8. 标准 Scrap 预制体范例

```text
▼ Scrap_Engine (Layer: Interactable, Tag: Scrap)
      Component: NetworkObject (联机ID)
      Component: Rigidbody (Mass: 20, Drag: 1)
      Component: NetworkTransform (同步位置)
      Component: ScrapItem (你的逻辑脚本：价格=100, 重量=20)
      Component: AudioSource (碰撞音效)

      ▼ Visual (Layer: Default)
            Component: MeshRenderer (引擎高模)
            Component: MeshFilter

      ▼ Colliders (Layer: Interactable)
          ▼ MainBox (BoxCollider - 主体)
          ▼ Handle (CapsuleCollider - 提手)

      ▼ ScanPoint (空物体 - 扫描仪瞄准点)
      ▼ GrabPoint (空物体 - 手拿的位置/IK目标)
```

该结构确保了：
- 逻辑与视觉可独立迭代。
- 批量变体继承统一行为。
- 跨团队协作时引用与合并风险最小化。
