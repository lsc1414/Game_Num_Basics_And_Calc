# 🧛 Vampire Survivors 性能奇迹：如何渲染与逻辑解耦

**文档目标**：深入分析 *Vampire Survivors* (VS) 如何处理 300,000+ 累计杀怪量的极端压力，并提炼对 Unity 开发的启示。

---

## 1. 现象级的数据压力

在 VS 后期（30分钟），屏幕上可能同时存在：
*   500+ 敌人精灵。
*   1000+ 经验宝石 (Gems)。
*   200+ 伤害数字。
*   数十个全屏特效。

原版 VS 使用 **Phaser (HTML5 游戏引擎)** 开发，它是如何跑在浏览器里的？

---

## 2. 核心优化技术

### 2.1 经验宝石合并算法 (Gem Merging)
这是 VS 最天才的设计之一。
*   **问题**：如果地上有 1000 个 1点经验的蓝宝石，由于渲染上限，屏幕会卡死。
*   **方案**：
    *   当屏幕上的宝石数量 > 400 时。
    *   新掉落的经验值不再生成新宝石。
    *   而是**累加**到离玩家最近的一颗“红宝石”上。
    *   甚至把屏幕外的所有散落宝石删除，将其经验值总和全部灌注到这颗红宝石里。
*   **结果**：玩家捡起这一颗红宝石，瞬间升 5 级。既解决了性能问题，又创造了极爽的反馈。

### 2.2 对象池与视口剔除 (Pooling & Culling)
*   **视口外不渲染**：虽然逻辑上怪物还在向你移动，但只要出了屏幕 100px，就不再执行 `Draw` 调用。
*   **逻辑降频**：屏幕外的怪物，每 10 帧才计算一次移动逻辑。

### 2.3 碰撞检测的极简主义
*   没有 Quadtree，没有复杂的物理。
*   **距离检测**：只检测“怪 vs 玩家”和“怪 vs 武器”。
*   **怪 vs 怪**：通过简单的“位置抖动”或“斥力向量”来模拟挤压，而不是真正的刚体碰撞。允许怪物重叠，但这在 2D 像素风下是可以接受的。

---

## 3. 引擎迁移：从 Phaser 到 Unity (New Engine)

VS 后来移植到了 Unity (New Engine update)。

### 3.1 为什么换引擎？
*   Web 技术的单线程限制了 CPU 密集型计算。
*   Unity 的 IL2CPP 和 Burst Compiler 可以榨干硬件性能。

### 3.2 Unity 中的等效实现
在 *Vampirefall* 中，我们应采用以下 Unity 技术复现 VS 的性能：

1.  **ECS / DOTS**：处理海量怪物的移动逻辑（参考 `ECS_Performance_Optimization.md`）。
2.  **GPU Instancing**：处理同屏精灵的渲染（参考 `GPU_Instancing_Guide.md`）。
3.  **Texture Array**：将不同怪物的帧动画打包到一个 Texture Array 中，避免切换材质。

---

## 4. 关键代码模式 (C#)

### 4.1 经验值合并逻辑
```csharp
public class GemManager : MonoBehaviour
{
    public int MaxGems = 400;
    private List<Gem> _activeGems = new List<Gem>();
    private Gem _superGem; // 红宝石

    public void OnDropExp(Vector3 pos, int amount)
    {
        if (_activeGems.Count < MaxGems)
        {
            SpawnGem(pos, amount);
        }
        else
        {
            // 场上宝石已满，寻找或创建超级宝石
            if (_superGem == null || !_superGem.gameObject.activeSelf)
            {
                // 选取离玩家最近的一个变为超级宝石，或者就在屏幕边缘生成一个
                _superGem = FindNearestGem(PlayerPos);
                _superGem.SetVisualToRed();
            }
            _superGem.AddExp(amount);
        }
    }
}
```

---

## 5. 总结：设计服务于性能

VS 告诉我们，**性能优化不仅仅是程序的事，更是策划的事**。
*   策划设计了“红宝石机制”，程序才能省下 90% 的 DrawCall。
*   策划接受了“怪物重叠”，程序才能移除昂贵的刚体物理。

**Vampirefall 准则**：
当策划提出“我要满屏掉落物”时，程序应立刻提出“那我们需要一个合并/吸附机制”，而不是硬着头皮去优化几千个对象的渲染。
