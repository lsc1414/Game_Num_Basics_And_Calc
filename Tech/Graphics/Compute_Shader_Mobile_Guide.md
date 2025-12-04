# ⚡ Compute Shader 移动端深度指南

## 📚 1. 理论基础 (Theoretical Basis)

### 1.1 核心定义
*   **GPGPU (General-Purpose computing on Graphics Processing Units)**: 利用 GPU 强大的并行计算能力处理非图形渲染任务。
*   **Compute Shader**: 一种独立于渲染管线（不经过顶点/片元着色器）的 Shader 程序，用于通用计算。
*   **线程模型**:
    *   **Thread**: 最小执行单元。
    *   **Group**: 线程组，包含多个线程（如 8x8x1）。组内线程共享 Thread Group Shared Memory (TGSM)。
    *   **Dispatch**: CPU 发起的调度指令，指定执行多少个 Group。

### 1.2 移动端支持现状 (Mobile Support)
*   **API 要求**:
    *   **OpenGL ES 3.1+**: Android 5.0+ 基本都支持。
    *   **Metal**: iOS (A7芯片以上) 完全支持。
    *   **Vulkan**: Android 7.0+ 支持。
*   **兼容性陷阱**:
    *   **Mali GPU (部分旧型号)**: 对浮点精度支持不佳，可能导致计算结果与 PC 不一致。
    *   **最大线程组限制**: 移动端通常限制每个 Group 最大线程数为 256 或 512，而 PC 通常是 1024。**安全做法是使用 64 (8x8) 或 128**。
    *   **读写限制**: 旧设备可能不支持对同一纹理的随机读写 (UAV)，需使用 Ping-Pong Buffer 技术。

---

## 🛠️ 2. 实践应用 (Practical Implementation)

### 2.1 Vampirefall 适配场景
1.  **海量弹幕计算 (Bullet Hell)**:
    *   CPU 无法处理 5000+ 弹幕的位移和碰撞。
    *   **方案**: Compute Shader 计算位置 -> `AppendStructuredBuffer` 存储结果 -> `DrawMeshInstancedIndirect` 渲染。
2.  **流场生成 (Flow Field)**:
    *   地图格子 100x100，每帧更新。
    *   **方案**: 一个 Kernel 计算所有格子的向量，性能比 C# Job System 快 10-50 倍。

### 2.2 核心代码结构 (Unity HLSL & C#)

#### HLSL (MyCompute.compute)
```hlsl
#pragma kernel CSMain

// 定义数据结构，必须与 C# struct 内存对齐
struct BulletData {
    float3 position;
    float3 velocity;
    float lifeTime;
};

// 读写缓冲区
RWStructuredBuffer<BulletData> bulletBuffer;
float deltaTime;

[numthreads(64, 1, 1)] // 推荐 64，兼容所有移动设备
void CSMain (uint3 id : SV_DispatchThreadID)
{
    // 防止越界
    uint index = id.x;
    if (index >= bulletBuffer.Length) return;

    // 逻辑处理
    BulletData b = bulletBuffer[index];
    b.position += b.velocity * deltaTime;
    b.lifeTime -= deltaTime;
    
    // 写回
    bulletBuffer[index] = b;
}
```

#### C# (ComputeController.cs)
```csharp
public class BulletSystem : MonoBehaviour
{
    public ComputeShader computeShader;
    private ComputeBuffer buffer;
    
    struct BulletData { ... } // 必须是 blittable 类型

    void Update()
    {
        int kernelHandle = computeShader.FindKernel("CSMain");
        
        // 设置参数
        computeShader.SetFloat("deltaTime", Time.deltaTime);
        computeShader.SetBuffer(kernelHandle, "bulletBuffer", buffer);
        
        // 调度: 总数 / 线程组大小，向上取整
        int groups = Mathf.CeilToInt(bulletCount / 64f);
        computeShader.Dispatch(kernelHandle, groups, 1, 1);
    }
}
```

### 2.3 性能注意事项 (Performance Tips)
*   **数据传输瓶颈**: **最忌讳** 每帧在 CPU 和 GPU 之间来回拷贝数据 (`GetData` / `SetData`)。
    *   **正确做法**: 数据常驻 GPU，渲染时直接用 `Graphics.DrawMeshInstancedIndirect` 读取 Buffer。
*   **异步回读 (AsyncGPUReadback)**: 如果必须把结果拿回 CPU（例如判断怪物是否死亡以播放音效），必须使用 `AsyncGPUReadback.Request`，否则会卡死主线程等待 GPU 完成。

---

## 🌟 3. 业界优秀案例 (Industry Best Practices)

### 3.1 Dyson Sphere Program (戴森球计划)
*   **机制**: 戴森球壳面上数万个节点的旋转和能量传输。
*   **实现**: 纯 GPU 模拟。只有在玩家点击查看详情时，才异步回读少量数据到 CPU。
*   **借鉴**: 视觉表现层（弹幕、特效粒子）应完全脱离 CPU 逻辑。

### 3.2 Genshin Impact (原神) - 移动端体积云
*   **机制**: 动态天气和体积云。
*   **实现**: 使用 Compute Shader 进行 3D 噪声采样和光照计算。
*   **优化**: 采用了半分辨率渲染 (Half-Resolution) 和时域重投影 (Temporal Reprojection) 来降低移动端负载。

---

## 🔗 4. 参考资料 (References)

*   📄 **Unity Manual**: [Compute Shaders](https://docs.unity3d.com/Manual/class-ComputeShader.html)
*   📄 **Catlike Coding**: [Compute Shaders Tutorial](https://catlikecoding.com/unity/tutorials/basics/compute-shaders/) - *入门必读*
*   📺 **GDC 2019**: [Mobile Compute Shaders in Fortnite](https://www.youtube.com/watch?v=2y2XF-a5_wU)
*   🌐 **Mobile GPU Compatibility**: [Android Developer Guide](https://developer.android.com/games/optimize/compute-shaders)

<script type="module">
  import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.esm.min.mjs';
  mermaid.initialize({ startOnLoad: false });
  await mermaid.run({
    querySelector: '.language-mermaid',
  });
</script>
