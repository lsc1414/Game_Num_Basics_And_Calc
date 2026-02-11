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

## 7. 第三方资产包管理规范 (Third-Party Asset Management)

❌ 错误做法：  
直接导入 Asset Store 包，任由它在 `Assets` 根目录下生成 `SuperSciFiKit`、`PolygonHorror` 等文件夹。

后果：项目目录乱成一锅粥；由于包含大量 4K 贴图和 Demo 场景，工程体积爆炸；想要修改某个脚本时，下次更新插件又被覆盖了。

✅ 工业化做法 (隔离与清洗)：

### A. 目录隔离 (The Quarantine Zone)

建立一个专门的文件夹（如 `Assets/_ThirdParty` 或 `Assets/Vendor`），所有购买的插件、素材包必须放在这里面。

- 保持原样：在这个文件夹内，尽量保持插件原本的目录结构，方便未来更新。

### B. 提取与清洗工作流 (Extract & Clean)

- 绝不直接使用第三方包里的 Prefab。
- 筛选 (Filter)：导入包时，取消勾选 `Documentation`、`Demos`、`Examples` 文件夹。这些只会拖慢你的工程。
- 提取 (Extract)：
  - 如果你看中了包里的一个“油桶”模型，不要直接引用。
  - 复制那个 `.fbx` 和对应的贴图，粘贴到你自己的 `Assets/Art/Models/Props` 文件夹中。
  - 按照本文第 1 章的规范，为这个复制出来的模型创建你自己的 Prefab。
- 理由：这样你可以随意修改材质、碰撞体，而不必担心更新资产包时被重置。

### C. 代码隔离 (Assembly Definition)

对于包含大量脚本的插件（如 `A* Pathfinding`、`Rewired`）：

- 在该插件的根目录下创建一个 Assembly Definition (`.asmdef`) 文件。
- 作用：这会把插件编译成一个独立的 DLL。当你修改自己的游戏逻辑代码时，Unity 不需要重新编译这些巨大的插件代码，编译速度能快 50% 以上。

### D. 修改原则 (Modification Rule)

- 原则：永远不要修改第三方脚本的源代码。
- 如果必须改：
  - 优先尝试继承 (Inheritance) 或扩展方法 (Extension Methods)。
  - 如果非改不可，必须在修改处加上注释 `// MODIFIED BY [YOUR NAME]`，并把修改过的脚本复制一份备份。否则下次插件更新，你的修改就全没了。

## 8. 资产引用强制隔离与自动化提取 (Enforcement & Automation)

针对“资产包文件夹混乱”和“手动复制麻烦”的痛点，我们需要两套脚本：一套负责拦截，一套负责智能搬运。

### A. 引用阻断器 (The Reference Barrier)

将此脚本放入 `Assets/Editor` 文件夹。当你保存 Prefab 时，它会自动检查依赖。

```csharp
using UnityEngine;
using UnityEditor;

public class AssetReferenceBarrier : UnityEditor.AssetModificationProcessor
{
    // 定义隔离区和安全区
    const string FORBIDDEN_FOLDER = "Assets/_ThirdParty";
    const string MY_PREFABS_FOLDER = "Assets/Prefabs";

    static string[] OnWillSaveAssets(string[] paths)
    {
        foreach (string path in paths)
        {
            // 只检查我们自己的 Prefab 文件夹
            if (path.StartsWith(MY_PREFABS_FOLDER) && path.EndsWith(".prefab"))
            {
                // 获取该 Prefab 的所有依赖（包括脚本、材质、贴图、模型）
                string[] dependencies = AssetDatabase.GetDependencies(path, true);
                
                foreach (string depPath in dependencies)
                {
                    // 如果发现依赖了隔离区的内容
                    if (depPath.StartsWith(FORBIDDEN_FOLDER))
                    {
                        string errorMsg = $"[阻断] 禁止保存！Prefab '{path}' 引用了隔离区资产: '{depPath}'。\n" +
                                          "请先使用 'Smart Extract' 工具将该资产提取到 'Assets/Art' 目录。";
                        
                        EditorUtility.DisplayDialog("违反工业化规范", errorMsg, "我错了");
                        Debug.LogError(errorMsg);
                        
                        // 返回原始路径列表，但实际上 Unity 的 Save 机制比较强硬，
                        // 这里虽然只是报错，但配合下面的工具使用效果更佳。
                        // 如果要强制禁止保存，可能需要抛出异常或重置 Asset。
                        return paths;
                    }
                }
            }
        }
        return paths;
    }
}
```

### B. 智能提取器 (Smart Asset Extractor)

这是一个“一键搬家”工具。  
用法：在 Project 窗口选中 `_ThirdParty` 里的一个 FBX 模型 -> 右键 -> `Industrial Tools -> Smart Extract to Art`。

功能：自动找到该模型用到的材质和贴图，把它们全部移动到 `Assets/Art/Imported/[模型名]` 文件夹，并保持引用不断裂。

```csharp
using UnityEngine;
using UnityEditor;
using System.IO;
using System.Collections.Generic;

public class SmartExtractor : Editor
{
    [MenuItem("Assets/Industrial Tools/Smart Extract to Art (Move)", false, 20)]
    static void ExtractAsset()
    {
        // 1. 获取选中的主资产
        Object selectedObject = Selection.activeObject;
        string mainAssetPath = AssetDatabase.GetAssetPath(selectedObject);

        if (string.IsNullOrEmpty(mainAssetPath) || !mainAssetPath.StartsWith("Assets/_ThirdParty"))
        {
            EditorUtility.DisplayDialog("Error", "请在 _ThirdParty 文件夹内选中一个主要资产 (如 FBX)", "OK");
            return;
        }

        // 2. 准备目标路径
        string assetName = Path.GetFileNameWithoutExtension(mainAssetPath);
        string targetFolder = $"Assets/Art/Imported/{assetName}"; // 自动创建同名文件夹
        
        if (!Directory.Exists(targetFolder))
        {
            Directory.CreateDirectory(targetFolder);
            AssetDatabase.Refresh();
        }

        // 3. 获取所有依赖 (递归查找)
        string[] dependencies = AssetDatabase.GetDependencies(mainAssetPath, true);
        List<string> assetsToMove = new List<string>();

        foreach (string depPath in dependencies)
        {
            // 只移动在 _ThirdParty 里的东西，且排除脚本 (脚本通常不需要移动)
            if (depPath.StartsWith("Assets/_ThirdParty") && !depPath.EndsWith(".cs"))
            {
                if (!assetsToMove.Contains(depPath))
                {
                    assetsToMove.Add(depPath);
                }
            }
        }

        // 4. 执行移动
        int moveCount = 0;
        AssetDatabase.StartAssetEditing(); // 暂停导入，加速移动
        
        try
        {
            foreach (string srcPath in assetsToMove)
            {
                string fileName = Path.GetFileName(srcPath);
                string dstPath = $"{targetFolder}/{fileName}";

                // 避免同名覆盖
                if (srcPath == dstPath) continue;

                // 使用 MoveAsset，Unity 会自动更新所有引用！这是关键！
                string error = AssetDatabase.MoveAsset(srcPath, dstPath);
                
                if (string.IsNullOrEmpty(error))
                {
                    moveCount++;
                }
                else
                {
                    Debug.LogError($"移动失败: {srcPath} -> {error}");
                }
            }
        }
        finally
        {
            AssetDatabase.StopAssetEditing();
            AssetDatabase.Refresh();
        }

        Debug.Log($"<color=green>成功提取 {moveCount} 个文件到 {targetFolder}</color>");
        
        // 5. 选中移动后的主文件
        string newMainPath = $"{targetFolder}/{Path.GetFileName(mainAssetPath)}";
        Object newObj = AssetDatabase.LoadAssetAtPath<Object>(newMainPath);
        if (newObj != null) Selection.activeObject = newObj;
    }
}
```

## 9. 提交前检查清单（Pre-Commit）

1. 无 `Missing Prefab` / 丢失引用。  
2. 场景根目录无测试垃圾对象。  
3. 灯光烘焙状态正确（或明确使用 Realtime）。  
4. 静态环境对象正确标记 `Static`（关系到 Occlusion Culling / NavMesh）。

## 10. 标准 Scrap 预制体范例

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

