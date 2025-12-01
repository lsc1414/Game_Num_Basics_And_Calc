# 🎨 GPU Instancing 渲染优化：15,000 个单位 1 个 DrawCall

**文档目标**：详解如何在 Unity 中实现海量同屏单位的高效渲染，从 `MaterialPropertyBlock` 到 `DrawMeshInstancedIndirect` 的完整技术路线。

---

## 1. 渲染瓶颈在哪里？

当屏幕上有 1000 个相同的史莱姆时，传统的渲染流程是：
1.  CPU 告诉 GPU：“准备好，我要画史莱姆 A 了，它在 (1,0,1)。”
2.  GPU 绘制 A。
3.  CPU 告诉 GPU：“准备好，我要画史莱姆 B 了，它在 (2,0,1)。”
4.  GPU 绘制 B。

**问题**：CPU 和 GPU 之间的通讯（Draw Call）太慢了。GPU 可以在 1 毫秒内画完 1000 个史莱姆，但 CPU 发送 1000 条指令需要 10 毫秒。
**解法**：CPU 打包数据：“这里有一堆位置列表，都是史莱姆，一次画完！”（GPU Instancing）。

---

## 2. Level 1: 基础 Instancing (MaterialPropertyBlock)

最简单的优化，不需要改 Shader（如果是 Standard Shader）或仅需少量改动。

### ✅ 适用场景
*   单位数量 < 1023 (受限于 Constant Buffer 大小)。
*   每个单位颜色、透明度不同，但网格相同。

### 💻 代码实现
```csharp
// ❌ 错误做法：renderer.material.color = Color.red; (会创建材质副本，破坏合批)
// ✅ 正确做法：使用 MaterialPropertyBlock

private MaterialPropertyBlock _propBlock;
private Renderer _renderer;

void Start() {
    _propBlock = new MaterialPropertyBlock();
    _renderer = GetComponent<Renderer>();
}

void UpdateColor(Color newColor) {
    _renderer.GetPropertyBlock(_propBlock);
    _propBlock.SetColor("_Color", newColor);
    _renderer.SetPropertyBlock(_propBlock);
}
```
**Shader 设置**：确保材质勾选了 `Enable GPU Instancing`。

---

## 3. Level 2: 进阶 Instancing (DrawMeshInstanced)

当不需要 GameObject，只需要纯粹的渲染时（例如弹幕、掉落物）。

### ✅ 适用场景
*   单位数量 > 1000。
*   不需要物理碰撞，或者物理逻辑在 JobSystem 中处理。

### 💻 代码实现
```csharp
public class BulletRenderer : MonoBehaviour
{
    public Mesh bulletMesh;
    public Material bulletMat;
    
    // 每次最多画 1023 个，所以需要切分数组
    private List<Matrix4x4[]> _batches = new List<Matrix4x4[]>();

    void Update() {
        // 假设 _batches 已经填满了位置数据
        foreach (var batch in _batches) {
            Graphics.DrawMeshInstanced(bulletMesh, 0, bulletMat, batch);
        }
    }
}
```
**限制**：仍然需要在每一帧由 CPU 整理 `Matrix4x4` 数组并上传，带宽压力依然存在。

---

## 4. Level 3: 终极优化 (DrawMeshInstancedIndirect)

**Indirect** 的意思是：CPU 甚至不知道要画多少个，数量由 GPU (Compute Shader) 决定，或者参数直接存在 GPU 显存里（ComputeBuffer）。

### ✅ 适用场景
*   **Vampire Survivors 规模**：10,000+ 单位。
*   逻辑完全在 Compute Shader 或 Job System 中运行。
*   **剔除 (Culling)**：在 GPU 中做视锥体剔除，看不见的不画。

### 💻 核心架构

1.  **ComputeBuffer**: 存储所有怪物数据的结构体（位置、旋转、缩放、颜色）。
2.  **ArgsBuffer**: 存储绘制参数（Mesh 顶点数、实例数量、起始索引等）。
3.  **Shader**: 修改顶点着色器，直接从 Buffer 读取数据。

### 💻 Shader 示例 (HLSL)
```hlsl
// 声明缓冲区
StructuredBuffer<float4x4> _LocalToWorldBuffer;
StructuredBuffer<float4> _ColorBuffer;

void vert(inout appdata_full v, uint instanceID : SV_InstanceID) {
    // 直接从显存读取矩阵
    float4x4 mat = _LocalToWorldBuffer[instanceID];
    v.vertex = mul(mat, v.vertex);
    v.normal = mul((float3x3)mat, v.normal);
}
```

### 💻 C# 驱动脚本
```csharp
void Update() {
    // 将计数重置，或由 Compute Shader 计算可见数量
    argsBuffer.SetData(args); 
    
    // 绑定数据
    instanceMaterial.SetBuffer("_LocalToWorldBuffer", positionBuffer);
    instanceMaterial.SetBuffer("_ColorBuffer", colorBuffer);
    
    // 一次调用，画 15,000 个
    Graphics.DrawMeshInstancedIndirect(mesh, 0, instanceMaterial, bounds, argsBuffer);
}
```

---

## 5. 性能对比 (同屏 10,000 个方块)

| 方法 | Draw Calls | FPS (PC) | CPU 开销 |
| :--- | :--- | :--- | :--- |
| **GameObjects** | ~10,000 | 4 fps | 100% (Main Thread) |
| **Static Batching** | ~50 | 15 fps | High (Memory Overhead) |
| **GPU Instancing** | ~10 | 45 fps | Medium (Matrix Upload) |
| **Indirect** | **1** | **120+ fps** | **Zero** |

---

## 6. 常见坑点 (Troubleshooting)

1.  **阴影 (Shadows)**：自定义 Shader 需要手动添加 `SHADOW_CASTER` pass 并支持 Instancing 宏，否则阴影会消失或不跟随。
2.  **LOD**：Indirect 模式下做 LOD 比较麻烦，需要把不同 LOD 的单位分到不同的 Buffer 绘制，或者在 Shader 中通过距离丢弃顶点（退化为点）。
3.  **设备兼容性**：Compute Shader 在古老的手机（OpenGLES 3.0 以下）上不支持。需要回退方案。

## 7. 结论
对于 *Vampirefall*：
*   **精英怪/Boss**：使用 Level 1 (MaterialPropertyBlock)。
*   **普通怪群 (500+)**：使用 Level 2 (DrawMeshInstanced) 配合 Job System。
*   **经验宝石/弹幕 (5000+)**：必须使用 Level 3 (Indirect)。
