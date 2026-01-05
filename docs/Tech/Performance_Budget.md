# ⚡ 性能预算与优化标准 (Performance Budget)

为了确保游戏在目标平台（PC中低配 / Steam Deck / 潜在的主机）上稳定运行 60FPS，必须严格执行此预算。

---

## 1. 目标平台规格 (Target Specs)

*   **基准平台:** GTX 1060 / Steam Deck.
*   **目标帧率:** 60 FPS (16.6ms per frame).
*   **分辨率:** 1080p.

## 2. CPU 预算 (CPU Budget)

Roguelike + 塔防意味着海量实体，CPU 是最大瓶颈。

*   **同屏单位数:** 最大 500 (怪物 + 塔 + 投射物)。
*   **AI 更新频率:**
    *   近处怪物 (<20m): 每帧更新。
    *   远处怪物 (>20m): 每 3-5 帧更新一次逻辑 (Time Slicing)。
    *   不可见怪物: 仅更新位置，暂停动画和物理。
*   **物理 (Physics):**
    *   使用 `Physics.Simulate` 或 DOTS Physics。
    *   **禁止**使用 MeshCollider 对动态物体。全部使用 Sphere/Capsule/Box。
*   **垃圾回收 (GC):**
    *   战斗中 **禁止** `new` 操作。
    *   所有投射物、特效、伤害飘字必须使用 **Object Pool**。

## 3. GPU 预算 (GPU Budget)

*   **Draw Calls (Batches):** < 2000。
    *   必须启用 GPU Instancing (大量同屏怪物)。
    *   UI 图集必须合并，减少 Draw Call。
*   **Triangle Count:** < 1.5M (全场景)。
    *   主角: 15k - 20k。
    *   杂兵: 1.5k - 3k (使用 LOD)。
    *   Boss: 10k - 15k。
*   **Overdraw:**
    *   特效粒子限制透明层数。
    *   避免全屏后处理叠加过多。

## 4. 内存预算 (Memory Budget)

*   **总内存:** < 4GB (System RAM).
*   **显存 (VRAM):** < 2GB.
*   **纹理:**
    *   角色: 2048x2048 (Atlas).
    *   环境: 1024x1024 (Tiling).
    *   杂兵: 512x512 或 1024 合集。
    *   *压缩:* PC使用 DXT5/BC7, 移动端使用 ASTC。

## 5. 优化技术栈 (Tech Stack)

1.  **DOTS (Data-Oriented Technology Stack):**
    *   对于海量怪物的移动和简单逻辑，考虑使用 ECS (Entities) + Burst Compiler。这是解决千人同屏的终极方案。
2.  **GPU Skinning:**
    *   将骨骼动画计算从 CPU 转移到 GPU Shader，解放 CPU 算力。
3.  **Addressables:**
    *   资源按需加载，避免启动时加载所有资源导致内存溢出。

---

## 6. 性能分级策略 (LOD Policy)

| 设置 | 阴影 | 抗锯齿 | 怪物数量 | 粒子密度 |
| :--- | :--- | :--- | :--- | :--- |
| **Low** | 仅主角 | FXAA | 200 (超过不再生成) | 50% |
| **Med** | 实时硬阴影 | SMAA | 350 | 75% |
| **High**| 软阴影 (Cascade) | TAA | 500 | 100% |
