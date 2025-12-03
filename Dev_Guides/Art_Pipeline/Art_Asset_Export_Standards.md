# 🎨 美术资源出图规范与速查表 (Art Asset Export Standards)

本文档旨在统一美术资源的输出格式，确保导入 Unity 后无需二次调整即可直接使用。

---

## ⚡ 速查表 (Cheat Sheet)

| 资源类型 | 命名前缀 | 格式 | 关键设置 | 备注 |
| :--- | :--- | :--- | :--- | :--- |
| **模型 (Static)** | `SM_` | `.fbx` | Scale=1, Y-Up, Z-Forward | 轴心点在底部中心 |
| **模型 (Skinned)** | `SK_` | `.fbx` | Bake Animation=On | 包含骨骼，轴心点在脚底 |
| **贴图 (Albedo)** | `T_` | `.tga` / `.png` | sRGB=On | 必须是 2 的幂次方 (POT) |
| **贴图 (Normal)** | `T_` ... `_N` | `.tga` / `.png` | sRGB=Off | 必须标记为 Normal Map |
| **贴图 (Mask)** | `T_` ... `_M` | `.tga` / `.png` | sRGB=Off | R=Metal, G=Occ, B=Smooth |
| **UI 图标** | `UI_Icon_` | `.png` | Alpha Is Transparency=On | **必须留 1px 透明边缘** |
| **UI 背景** | `UI_Bg_` | `.png` | 9-Slice 预留 | 检查压缩格式 (ASTC/ETC2) |

---

## 1. 命名规范 (Naming Conventions)

严禁使用中文、空格或特殊字符。使用 **PascalCase** (大驼峰) 或 **Snake_Case** (下划线)。

### 1.1 模型 (Meshes)
*   **静态网格**: `SM_[Name]_[Variant]` (e.g., `SM_Tree_Birch_01`)
*   **骨骼网格**: `SK_[Name]` (e.g., `SK_Hero_Vampire`)

### 1.2 贴图 (Textures)
*   **基础色**: `T_[Name]_D` (Diffuse/Albedo)
*   **法线**: `T_[Name]_N` (Normal)
*   **混合遮罩**: `T_[Name]_M` (Mask - R:Metallic, G:Occlusion, B:Smoothness)
*   **自发光**: `T_[Name]_E` (Emissive)

### 1.3 材质 (Materials)
*   `M_[Name]` (e.g., `M_Tree_Bark`)
*   如果是实例材质: `MI_[Name]` (Material Instance)

---

## 2. 模型出图规则 (Model Rules)

### 2.1 软件导出设置 (Software Export Settings)

为了避免“人为失误”，强烈建议使用脚本一键导出。

#### A. Blender (推荐使用 Python 脚本)
Blender 的坐标系坑最大 (Z-Up)，必须强制转换。

*   **手动设置**:
    *   `Apply Scalings`: **FBX All** (关键！否则 Scale 会变成 100)
    *   `Forward`: **-Z Forward**
    *   `Up`: **Y Up**
    *   `Apply Unit`: **Checked**
    *   `Bake Animation`: 仅对骨骼模型勾选

*   **自动化脚本 (Save as `export_unity_fbx.py`)**:
    ```python
    import bpy
    import os

    # 1. 准备工作：应用缩放，重置位置
    bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)

    # 2. 导出路径 (当前 .blend 同级目录)
    basedir = os.path.dirname(bpy.data.filepath)
    name = bpy.path.display_name_from_filepath(bpy.data.filepath)
    filepath = os.path.join(basedir, name + ".fbx")

    # 3. 强制参数导出
    bpy.ops.export_scene.fbx(
        filepath=filepath,
        use_selection=True,
        axis_forward='-Z',  # Unity Forward
        axis_up='Y',        # Unity Up
        apply_unit_scale=True,
        apply_scale_options='FBX_SCALE_ALL', # 修复 Scale 100 问题
        bake_space_transform=True,
        use_mesh_modifiers=True,
        add_leaf_bones=False # 避免产生多余的叶子骨骼
    )
    print(f"Successfully exported to: {filepath}")
    ```

    ```

#### C. 进阶：Blender "万能洗澡" 流程 (Universal Cleaner)
**Q: 我能随便拖一个 FBX 进 Blender，然后用上面的脚本导出就完美了吗？**
**A: 不完全是。** 脚本能保证**格式** (Scale/Axis) 正确，但无法自动修复**内容** (Pivot/Hierarchy)。

如果你的目标是清洗外部杂乱资源，请在运行导出脚本前，手动执行以下“洗澡”步骤：

1.  **清理层级 (Clear Hierarchy)**:
    *   很多外部 FBX 有多层空物体 (Empty Nodes)。
    *   *操作*: 选中模型 -> `Alt+P` -> `Clear and Keep Transformation` (解除父子关系)。
2.  **重置轴心 (Reset Pivot)**:
    *   *操作*: 选中模型 -> `Right Click` -> `Set Origin` -> `Origin to Geometry` (或者手动移到底部)。
    *   *注意*: 确保模型位于世界坐标 (0,0,0)。
3.  **检查 UV**:
    *   外部模型的 UV 往往是乱的。进入 `UV Editing` 快速看一眼。

> **💡 脚本增强**: 上面的 Python 脚本包含 `transform_apply`，这会自动修复大部分缩放和旋转问题，但**不会**修复轴心点位置。

#### D. 3ds Max
Max 的单位设置最容易乱。
*   **System Unit Setup**: 必须设为 **Meters** (1 Unit = 1.0 Meters)。不要只改 Display Unit！
*   **FBX Export**:
    *   `Up Axis`: **Y-Up**
    *   `Scale Factor`: Automatic (确保显示为 1.0)
    *   `Embed Media`: **Uncheck** (不要把贴图包进 FBX，Unity 无法复用)

*   **单位**: **1 Unit = 1 Meter**.
    *   门高: 2.5m
    *   角色高: 1.7m ~ 1.8m

### 2.2 轴心点 (Pivot)
*   **地面物体** (树、石头、建筑): **底部中心 (Bottom Center)** (0, 0, 0)。
*   **悬挂物体** (吊灯): **顶部中心 (Top Center)**。
*   **手持物体** (剑、枪): **握把中心 (Handle Center)**。

### 2.3 UV 与顶点色
*   **UV1**: 必须在 0-1 范围内。
*   **UV2**: 如果需要烘焙光照贴图，必须展开 UV2，且 UV Island 之间保留至少 2px 间隙。
*   **顶点色**:
    *   **R**: 用于混合材质 (如树干混合苔藓)。
    *   **G**: 用于风动权重 (0=静止, 1=随风摆动)。

---

## 3. 贴图出图规则 (Texture Rules)

### 3.1 尺寸 (Dimensions)
*   **必须是 POT (Power of Two)**: 256, 512, 1024, 2048, 4096.
*   **非正方形允许**: 512x1024 是合法的，但 500x500 是**非法**的。
*   **例外 (UI Sprites)**:
    *   如果 UI 图片会被打入 **Sprite Atlas** (图集)，则单张图片**不需要**是 POT。
    *   Unity 会自动将它们打包成一张大的 POT 图集。
    *   *注意*: 如果是 `UITexture` (不打图集的大图，如背景)，则**必须**是 POT。
*   **移动端建议**:
    *   角色: 1024 ~ 2048
    *   场景物件: 512 ~ 1024
    *   特效: 256 ~ 512

### 3.2 颜色空间 (Color Space)
*   **sRGB (Color Data)**: 勾选 sRGB。
    *   Albedo (Diffuse), Emissive.
*   **Linear (Math Data)**: **取消**勾选 sRGB。
    *   Normal Map, Metallic, Roughness, Ambient Occlusion.

---

## 4. UI 图标工作流：1px 边缘法则

### 4.1 为什么要留 1px 空白？
在游戏引擎中，UI 图标通常会被打包成图集 (Atlas)。当图标进行缩放或旋转时，采样器会读取相邻像素 (Bilinear Filtering)。
*   **如果没有边缘**: 采样器会读取到隔壁图标的像素，导致图标边缘出现奇怪的杂色线条 (Bleeding)。
*   **如果有 1px 透明边缘**: 采样器读取到透明像素，完美过渡。

### 4.2 Photoshop 快速导出动作 (Action)
不要手动去缩放画布！使用 PS 动作自动化：

1.  **Trim**: `Image` -> `Trim` -> `Transparent Pixels` (切掉多余空白)。
2.  **Canvas Size**: 勾选 `Relative`，Width = `2px`, Height = `2px` (上下左右各加 1px)。
3.  **Export**: `Save for Web` -> PNG-24 (带透明通道)。

> **脚本化方案**: 也可以使用 Python (Pillow 库) 批量处理文件夹下的所有 PNG。

```python
from PIL import Image, ImageOps
import os

def process_icon(path):
    img = Image.open(path)
    # 1. Trim transparent borders
    bbox = img.getbbox()
    if bbox:
        img = img.crop(bbox)
    
    # 2. Add 1px padding
    new_size = (img.width + 2, img.height + 2)
    new_img = Image.new("RGBA", new_size, (0, 0, 0, 0))
    new_img.paste(img, (1, 1))
    
    new_img.save(path)

# 遍历文件夹调用 process_icon...
```
