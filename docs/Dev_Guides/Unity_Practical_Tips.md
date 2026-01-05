# 🛠️ Unity 游戏开发实战锦囊 (Unity Practical Dev Tips)

**文档目标：** 只有干货。拒绝教科书式的废话，专注解决“为什么我的游戏卡顿”和“为什么我的代码写不下去了”这两个核心问题。
**适用范围：** 适用于中高级开发，特别是 **塔防 (TD)** 和 **肉鸽 (Roguelike)** 这类对性能和架构要求极高的品类。

---

## 1. 🏎️ 性能优化：别让 GC 杀了你的游戏

在塔防/肉鸽游戏中，屏幕上可能有 500 个敌人和 2000 发子弹。如果处理不好，帧率会跌到个位数。

### 1.1 ♻️ 对象池 (Object Pooling) —— 必修课
*   **原理：** `Instantiate` (生成) 和 `Destroy` (销毁) 是极其昂贵的操作，还会产生垃圾内存 (Garbage)，导致 GC (垃圾回收) 触发时游戏卡顿。
*   **做法：**
    *   **🟢 借出：** 想要子弹？从池子里拿一个隐藏的，重置位置和状态，设为 `SetActive(true)`。
    *   **🔴 归还：** 子弹撞墙了？别 `Destroy`。把它移出屏幕，`SetActive(false)`，放回池子。
*   **进阶技巧：** 使用 `release` 接口而非 `return`。对于复杂的池对象（如怪物），在 `OnDisable` 里重置状态，防止下次拿出来时带着上一局的 Debuff。

### 1.2 🧵 字符串的陷阱 (The String Trap)
*   **大忌：** 在 `Update()` 里写字符串拼接。
    *   `uiText.text = "Score: " + score;` // 每帧都会产生一个新的 String 对象，GC 爆炸。
*   **对策：**
    *   **缓存：** 如果分数没变，别更新 UI。
    *   **StringBuilder：** 对于复杂拼接，使用 `StringBuilder`。
    *   **ZString / C# Span:** (高级) 使用零内存分配的字符串库。

### 1.3 🧱 物理系统的 90% 性能都在这
*   **碰撞矩阵 (Collision Matrix):**
    *   打开 `Project Settings -> Physics 2D`。
    *   **✅ 取消勾选**所有不需要碰撞的组合！
    *   *例子：* “子弹”不需要撞“子弹”。“敌人”不需要撞“经验球”。这能节省大量的物理计算。
*   **别用 MeshCollider:** 除非是静态的地形。移动物体请用 `BoxCollider` 或 `SphereCollider` (或 2D 对应版)。
*   **Rigidbody 的休眠:** 确保不动的物体能进入 Sleep 状态。

### 1.4 🖼️ 批量渲染 (Batching / DrawCalls)
*   **问题：** 100 个怪，如果用了 100 个不同的材质球，就是 100 个 DrawCall。CPU 会累死。
*   **对策 (Sprite Atlas):**
    *   把所有怪物的图片打包成一张大图 (Sprite Atlas)。
    *   这样渲染 100 个怪，可能只需要 1 个 DrawCall。
*   **文本 (TMP):** TextMeshPro 也是一样的道理，尽量共用字体贴图。

### 1.5 🎯 塔防专项优化案例

#### 📍 路径寻找优化（A*算法替代方案）
```csharp
// 塔防游戏中500+敌人同时寻路的性能噩梦解决方案
public class TowerDefensePathfinding
{
    // ❌ 传统A*：每帧每个敌人都计算路径，CPU爆炸
    // ✅ 预计算路径点 + 流场寻路

    private Vector2[] waypoints; // 预计算的关键路径点
    private Dictionary<Vector2, Vector2> flowField; // 流场数据

    public void PreCalculatePath()
    {
        // 只在地图变化时计算一次流场
        // 每个格子存储最佳移动方向
        flowField = CalculateFlowField(waypoints);
    }

    // 敌人移动时只需查表，O(1)复杂度
    public Vector2 GetMovementDirection(Vector2 currentPos)
    {
        Vector2 gridPos = SnapToGrid(currentPos);
        return flowField.GetValueOrDefault(gridPos, Vector2.right);
    }
}
```

#### 🎯 弹幕碰撞检测优化（空间哈希）
```csharp
public class BulletCollisionSystem
{
    // 2000发子弹的碰撞检测优化
    private SpatialHashGrid spatialGrid;

    public void CheckCollisions()
    {
        spatialGrid.Clear();

        // 1. 将所有子弹插入空间哈希网格
        foreach (var bullet in activeBullets)
        {
            spatialGrid.Insert(bullet);
        }

        // 2. 每个敌人只检测同网格内的子弹
        foreach (var enemy in activeEnemies)
        {
            var nearbyBullets = spatialGrid.GetNearby(enemy.position);

            foreach (var bullet in nearbyBullets)
            {
                if (Vector2.Distance(enemy.position, bullet.position) < bullet.radius)
                {
                    HandleCollision(enemy, bullet);
                }
            }
        }
    }
}

// 空间哈希网格实现
public class SpatialHashGrid
{
    private Dictionary<int, List<GameObject>> cells;
    private float cellSize = 2f;

    private int GetHashKey(Vector2 position)
    {
        int x = Mathf.FloorToInt(position.x / cellSize);
        int y = Mathf.FloorToInt(position.y / cellSize);
        return x * 73856093 ^ y * 19349663; // 质数乘法减少哈希冲突
    }
}
```

#### ⚡ 技能特效GPU Instancing优化
```csharp
// 1000个火焰特效的性能优化
public class EffectManager : MonoBehaviour
{
    [SerializeField] private Material instancedMaterial;
    [SerializeField] private Mesh effectMesh;

    private Matrix4x4[] matrices; // 存储所有特效的变换矩阵
    private Vector4[] colors;     // 存储所有特效的颜色
    private MaterialPropertyBlock propertyBlock;

    void Start()
    {
        // 初始化GPU Instancing数据
        matrices = new Matrix4x4[MAX_EFFECTS];
        colors = new Vector4[MAX_EFFECTS];
        propertyBlock = new MaterialPropertyBlock();
    }

    void Update()
    {
        // 收集所有需要渲染的特效数据
        int count = CollectEffectData();

        if (count > 0)
        {
            // 一次性渲染所有特效，只需1个DrawCall
            propertyBlock.SetVectorArray("_Colors", colors);
            Graphics.DrawMeshInstanced(effectMesh, 0, instancedMaterial,
                matrices, count, propertyBlock);
        }
    }
}

// Shader中需要添加的instancing支持
Shader "Custom/InstancedEffect"
{
    Properties
    {
        _MainTex ("Texture", 2D) = "white" {}
    }

    SubShader
    {
        Tags { "RenderType"="Opaque" }
        LOD 100

        Pass
        {
            CGPROGRAM
            #pragma vertex vert
            #pragma fragment frag
            #pragma multi_compile_instancing // 启用instancing

            #include "UnityCG.cginc"

            UNITY_INSTANCING_BUFFER_START(Props)
                UNITY_DEFINE_INSTANCED_PROP(float4, _Colors)
            UNITY_INSTANCING_BUFFER_END(Props)

            // ... 其余shader代码
            ENDCG
        }
    }
}

```

---

## 2. 🏗️ 架构设计：如何写出不耦合的代码

塔防游戏最怕代码变成“意大利面条”：塔的代码引用了怪物，怪物引用了血条，血条引用了音效管理器... 删一个文件报错一百个。

### 2.1 📢 事件总线 (Event Bus) / 观察者模式
*   **场景：** 怪物死了，需要：1.加分 2.播音效 3.掉落金币 4.任务计数。
*   **错误写法：** 在 `Monster.cs` 里调用 `ScoreManager.Add()`, `AudioManager.Play()`, `LootManager.Spawn()`...
*   **正确写法 (解耦):**
    *   `Monster.cs`: `public static event Action<Monster> OnMonsterDied;`
    *   怪物死的时候：`OnMonsterDied?.Invoke(this);` 我只管喊一声“我死啦！”，谁爱管谁管。
    *   `ScoreManager.cs`: 监听 `OnMonsterDied`，听到就加分。
    *   **好处：** 你删掉音效管理器，怪物代码一行都不用改。

### 2.2 📄 ScriptableObject (SO) —— 策划的好朋友
*   **核心理念：** **数据与逻辑分离**。
*   **应用：** 别在代码里写 `public float atk = 10;`。
*   **做法：**
    1.  创建一个 `EnemyData : ScriptableObject`，里面存 HP, Atk, Speed, Prefab。
    2.  在 Project 窗口右键创建 `Goblin_Lv1.asset`, `Dragon_Lv99.asset`。
    3.  怪物逻辑 `Monster.cs` 里只有一个变量：`public EnemyData data;`。
*   **好处：**
    *   策划可以直接在编辑器里调数值，不用改代码，不用重新编译。
    *   内存里只有一份数据，1000 个哥布林共用一个 SO，省内存。

### 2.3 🧩 组合优于继承 (Composition over Inheritance)
*   **问题：** `class FireDragon : Dragon`。如果我想做一个"冰龙"，又要继承。如果我想做一个"会喷火的骷髅"怎么办？多重继承？
*   **对策 (组件化):**
    *   不再写"火龙"类。
    *   写功能组件：`Health` (血量), `Mover` (移动), `Shooter` (发射), `ElementType` (元素类型)。
    *   **🔥 火龙** = Health + Mover + Shooter(Fireball) + Element(Fire)。
    *   **💀 喷火骷髅** = Health + Mover + Shooter(Fireball) + Element(Undead)。
    *   Unity 的 `GameObject` + `Component` 本身就是这个设计哲学，请贯彻它。

### 2.4 🏛️ ECS架构实战（Entity Component System）

#### 📊 为什么传统OOP在大量实体时性能差？
```csharp
// ❌ 传统OOP：每个敌人都有Update，1000个敌人=1000次虚函数调用
public class Enemy : MonoBehaviour
{
    void Update() // 虚函数调用开销
    {
        Move();
        CheckHealth();
        UpdateAI();
    }
}

// ✅ ECS：数据和行为分离，批量处理
public struct Health : IComponentData
{
    public float current;
    public float max;
}

public struct Movement : IComponentData
{
    public float3 direction;
    public float speed;
}

// 系统一次性处理所有实体
public class MovementSystem : SystemBase
{
    protected override void OnUpdate()
    {
        float deltaTime = Time.DeltaTime;

        Entities.ForEach((ref Translation translation, in Movement movement) =>
        {
            translation.Value += movement.direction * movement.speed * deltaTime;
        }).ScheduleParallel(); // 并行处理！
    }
}
```

#### 🎯 DOTS（Data-Oriented Tech Stack）实战案例
```csharp
// 塔防游戏中的1000个敌人同屏优化
public struct Enemy : IComponentData
{
    public float speed;
    public float health;
    public int pathIndex;
}

public struct PathFollow : IComponentData
{
    public float3 targetPosition;
    public float reachedDistance;
}

[BurstCompile] // 使用Burst编译器加速
public partial struct PathFollowingSystem : ISystem
{
    [BurstCompile]
    public void OnUpdate(ref SystemState state)
    {
        float deltaTime = SystemAPI.Time.DeltaTime;

        new PathFollowJob
        {
            DeltaTime = deltaTime,
            Waypoints = SystemAPI.GetSingletonBuffer<PathWaypoint>()
        }.ScheduleParallel();
    }

    [BurstCompile]
    partial struct PathFollowJob : IJobEntity
    {
        public float DeltaTime;
        public DynamicBuffer<PathWaypoint> Waypoints;

        void Execute(ref LocalTransform transform, ref Enemy enemy, ref PathFollow pathFollow)
        {
            // 批量路径跟随逻辑
            float3 direction = math.normalize(pathFollow.targetPosition - transform.Position);
            transform.Position += direction * enemy.speed * DeltaTime;

            // 检查是否到达路径点
            if (math.distance(transform.Position, pathFollow.targetPosition) < pathFollow.reachedDistance)
            {
                enemy.pathIndex++;
                if (enemy.pathIndex < Waypoints.Length)
                {
                    pathFollow.targetPosition = Waypoints[enemy.pathIndex].Position;
                }
            }
        }
    }
}
```

### 2.5 🗃️ 状态机模式（FSM）详解

#### 🎮 塔防游戏中的复杂状态管理
```csharp
// ❌ 传统if-else地狱
public class Tower : MonoBehaviour
{
    private bool isBuilding = false;
    private bool isAttacking = false;
    private bool isUpgrading = false;

    void Update()
    {
        if (isBuilding) { /* 建造逻辑 */ }
        else if (isAttacking) { /* 攻击逻辑 */ }
        else if (isUpgrading) { /* 升级逻辑 */ }
        // 状态越来越多，代码越来越乱...
    }
}

// ✅ 状态机模式：每个状态独立处理逻辑
public abstract class TowerState
{
    protected Tower tower;
    protected TowerStateMachine stateMachine;

    public TowerState(Tower tower, TowerStateMachine stateMachine)
    {
        this.tower = tower;
        this.stateMachine = stateMachine;
    }

    public virtual void Enter() { }
    public virtual void Update() { }
    public virtual void Exit() { }
}

public class TowerBuildingState : TowerState
{
    private float buildTimer;

    public TowerBuildingState(Tower tower, TowerStateMachine stateMachine)
        : base(tower, stateMachine) { }

    public override void Enter()
    {
        buildTimer = 0f;
        tower.ShowBuildAnimation();
    }

    public override void Update()
    {
        buildTimer += Time.deltaTime;

        if (buildTimer >= tower.buildTime)
        {
            stateMachine.ChangeState(tower.IdleState);
        }
    }
}

public class TowerAttackingState : TowerState
{
    private float attackCooldown;

    public override void Update()
    {
        attackCooldown -= Time.deltaTime;

        if (attackCooldown <= 0f)
        {
            var target = tower.FindTarget();
            if (target != null)
            {
                tower.Attack(target);
                attackCooldown = tower.attackSpeed;
            }
            else
            {
                stateMachine.ChangeState(tower.IdleState);
            }
        }
    }
}

// 状态机管理器
public class TowerStateMachine
{
    private TowerState currentState;

    public void ChangeState(TowerState newState)
    {
        currentState?.Exit();
        currentState = newState;
        currentState?.Enter();
    }

    public void Update()
    {
        currentState?.Update();
    }
}


---

```

## 3. 🛠️ 开发效率：别重复造轮子

### 3.1 ⏳ 异步编程：UniTask
*   **现状：** Unity 原生 `Coroutine` (协程) 容易产生垃圾内存，且无法返回值。C# 原生 `Task` 在 WebGL 上支持不好且有线程问题。
*   **推荐：** 使用 **UniTask** (开源库)。
    *   `await UniTask.Delay(1000);`
    *   比协程更快，0 GC，像写同步代码一样写异步逻辑。

### 3.2 🎨 动画插件：DoTween
*   **场景：** 想要一个 UI 弹窗“弹”出来的效果。
*   **别自己写：** `Update` 里写 `transform.scale += Time.deltaTime...` 太累了。
*   **用 DoTween：** `transform.DOScale(1.2f, 0.5f).SetEase(Ease.OutBack);` 一行代码搞定，丝般顺滑。

### 3.3 🕵️ 编辑器扩展 (Odin Inspector)
*   **痛点：** Unity 原生的 Inspector 很难看，List 没法搜索，字典没法显示。
*   **推荐：** **Odin Inspector** (收费但值得/也有免费替代品)。
*   **低配版 (原生):**
    *   `[Header("基础属性")]`: 给变量分组。
    *   `[Tooltip("攻击力")]`: 鼠标悬停提示。
    *   `[Range(0, 100)]`: 变成滑动条。
    *   `[ContextMenu("测试击杀")]`: 在组件右键菜单里添加一个按钮来执行函数，方便测试。

---

## 4. 🐛 调试与防坑

### 4.1 🛑 空引用 (NullReferenceException)
*   **原则：** 永远不要信任 `GetComponent` 和 `Find`。
*   **🛡️ 防御式编程：**
    *   `RequireComponent(typeof(Rigidbody))`：强制挂载依赖组件。
    *   `TryGetComponent(out Rigidbody rb)`：比 `GetComponent` 安全且快。

### 4.2 📌 还能这么 Debug?
*   **Debug.Break():** 代码里调用这个，游戏会自动暂停。适合捕捉“一闪而过”的 Bug。
*   **Debug.DrawLine / Gizmos:**
    *   别光看 Log。在 `OnDrawGizmos` 里把攻击范围、索敌半径画出来。
    *   可视化调试比看 Console 快 10 倍。

### 4.3 ⏱️ Time.timeScale
*   **做暂停功能时：** 设为 0。
*   **做倍速功能时：** 设为 2.0。
*   **坑：** `Update` 里的逻辑受影响，但 `FixedUpdate` (物理) 也受影响。如果你有一些 UI 动画不想受暂停影响，请用 `UnscaledTime`。

### 4.4 🧪 单元测试与集成测试

#### 🎯 游戏逻辑测试框架
```csharp
// ❌ 传统测试：手动测试，效率低下
// ✅ 自动化测试：快速验证核心逻辑

using NUnit.Framework;
using UnityEngine.TestTools;
using System.Collections;

public class TowerDefenseTests
{
    // 塔防游戏核心逻辑测试
    [Test]
    public void Test_DamageCalculation()
    {
        // 测试伤害计算公式
        float attackPower = 100f;
        float defense = 20f;
        float expectedDamage = attackPower * (1 - defense / (defense + 3000f));

        float actualDamage = DamageCalculator.CalculateDamage(attackPower, defense);

        Assert.AreEqual(expectedDamage, actualDamage, 0.01f);
    }

    [Test]
    public void Test_TowerRange()
    {
        // 测试塔的攻击范围检测
        var tower = new GameObject().AddComponent<Tower>();
        tower.range = 5f;
        tower.transform.position = Vector3.zero;

        var enemyInRange = CreateEnemyAt(Vector3.right * 4f); // 4米内
        var enemyOutOfRange = CreateEnemyAt(Vector3.right * 6f); // 6米外

        Assert.IsTrue(tower.IsInRange(enemyInRange));
        Assert.IsFalse(tower.IsInRange(enemyOutOfRange));
    }

    [UnityTest]
    public IEnumerator Test_EnemyMovement()
    {
        // 测试敌人移动逻辑
        var enemy = CreateEnemyAt(Vector3.zero);
        enemy.speed = 2f;
        var targetPosition = Vector3.right * 10f;

        enemy.SetDestination(targetPosition);

        float startTime = Time.time;
        while (Vector3.Distance(enemy.transform.position, targetPosition) > 0.1f)
        {
            yield return null;
        }
        float travelTime = Time.time - startTime;

        float expectedTime = 10f / enemy.speed;
        Assert.AreEqual(expectedTime, travelTime, 0.1f);
    }
}

// 性能测试：确保算法复杂度正确
[TestFixture]
public class PerformanceTests
{
    [Test]
    [Timeout(1000)] // 1秒内必须完成
    public void Test_PathfindingPerformance()
    {
        var pathfinder = new Pathfinder();
        var grid = CreateLargeGrid(100, 100); // 100x100网格
        var start = new Vector2(0, 0);
        var end = new Vector2(99, 99);

        var path = pathfinder.FindPath(start, end, grid);

        Assert.IsNotNull(path);
        Assert.Greater(path.Count, 0);
    }
}
```

#### 🔍 内存泄漏检测工具
```csharp
public class MemoryLeakDetector
{
    private long initialMemory;
    private List<WeakReference> objectReferences = new List<WeakReference>();

    public void StartMonitoring()
    {
        // 强制垃圾回收
        System.GC.Collect();
        System.GC.WaitForPendingFinalizers();
        System.GC.Collect();

        initialMemory = System.GC.GetTotalMemory(false);
    }

    public void TrackObject(GameObject obj)
    {
        objectReferences.Add(new WeakReference(obj));
    }

    public MemoryReport GetReport()
    {
        System.GC.Collect();
        long currentMemory = System.GC.GetTotalMemory(false);

        int aliveObjects = 0;
        foreach (var reference in objectReferences)
        {
            if (reference.IsAlive)
                aliveObjects++;
        }

        return new MemoryReport
        {
            memoryIncrease = currentMemory - initialMemory,
            aliveObjects = aliveObjects,
            totalTracked = objectReferences.Count
        };
    }
}

// 使用示例
public class ResourceManager
{
    private MemoryLeakDetector leakDetector = new MemoryLeakDetector();

    public void LoadLevel(int levelId)
    {
        leakDetector.StartMonitoring();

        // 加载各种资源
        var enemies = LoadEnemies(levelId);
        var towers = LoadTowers(levelId);

        foreach (var enemy in enemies)
            leakDetector.TrackObject(enemy);

        foreach (var tower in towers)
            leakDetector.TrackObject(tower);
    }

    public void UnloadLevel()
    {
        // 清理资源
        DestroyAllEnemies();
        DestroyAllTowers();

        // 检查内存泄漏
        var report = leakDetector.GetReport();
        if (report.memoryIncrease > 1024 * 1024) // 1MB
        {
            Debug.LogError($"内存泄漏检测：增加了{report.memoryIncrease / 1024f:F2}KB，{report.aliveObjects}个对象未释放");
        }
    }
}
```

### 4.5 📊 Unity Profiler高级技巧

#### 🔥 性能分析最佳实践
```csharp
// 自定义性能分析标签
using Unity.Profiling;

public class TowerManager : MonoBehaviour
{
    private static readonly ProfilerMarker s_UpdateMarker =
        new ProfilerMarker("TowerManager.Update");

    private static readonly ProfilerMarker s_PathfindingMarker =
        new ProfilerMarker("TowerManager.Pathfinding");

    private static readonly ProfilerMarker s_TargetingMarker =
        new ProfilerMarker("TowerManager.Targeting");

    void Update()
    {
        using (s_UpdateMarker.Auto())
        {
            using (s_TargetingMarker.Auto())
            {
                UpdateTargetAcquisition();
            }

            using (s_PathfindingMarker.Auto())
            {
                UpdatePathfinding();
            }
        }
    }
}

// 内存分配分析
public class AllocationAnalyzer
{
    [RuntimeInitializeOnLoadMethod]
    static void Initialize()
    {
        Application.logMessageReceived += HandleLog;
    }

    static void HandleLog(string condition, string stackTrace, LogType type)
    {
        if (condition.Contains("GC.Alloc") && condition.Contains("Bytes"))
        {
            // 检测到GC分配，记录详细信息
            var match = System.Text.RegularExpressions.Regex.Match(condition, @"(\d+) Bytes");
            if (match.Success)
            {
                int bytes = int.Parse(match.Groups[1].Value);
                if (bytes > 1024) // 大于1KB的分配才关注
                {
                    Debug.LogWarning($"检测到大量GC分配: {bytes}Bytes\n{stackTrace}");
                }
            }
        }
    }
}
```

#### 🎯 真机性能分析技巧
```csharp
// 移动端性能监控
public class MobileProfiler : MonoBehaviour
{
    [Header("性能监控")]
    public bool enableFPSMonitor = true;
    public bool enableMemoryMonitor = true;
    public bool enableBatteryMonitor = true;

    private float deltaTime = 0.0f;
    private float fps;
    private long lastMemory = 0;

    void Update()
    {
        if (enableFPSMonitor)
        {
            deltaTime += (Time.unscaledDeltaTime - deltaTime) * 0.1f;
            fps = 1.0f / deltaTime;
        }

        if (enableMemoryMonitor && Time.frameCount % 60 == 0) // 每秒检查一次
        {
            long currentMemory = UnityEngine.Profiling.Profiler.GetTotalAllocatedMemoryLong();
            if (Mathf.Abs(currentMemory - lastMemory) > 1024 * 1024) // 内存变化超过1MB
            {
                Debug.Log($"内存变化: {FormatBytes(lastMemory)} -> {FormatBytes(currentMemory)}");
                lastMemory = currentMemory;
            }
        }
    }

    void OnGUI()
    {
        if (!Application.isEditor) // 只在真机显示
        {
            GUIStyle style = new GUIStyle();
            style.fontSize = 30;
            style.normal.textColor = Color.white;

            if (enableFPSMonitor)
            {
                string fpsText = $"FPS: {fps:F1}";
                Color color = fps > 50 ? Color.green : fps > 30 ? Color.yellow : Color.red;
                style.normal.textColor = color;
                GUI.Label(new Rect(10, 10, 200, 50), fpsText, style);
            }

            if (enableMemoryMonitor)
            {
                long totalMemory = UnityEngine.Profiling.Profiler.GetTotalAllocatedMemoryLong();
                string memoryText = $"Memory: {FormatBytes(totalMemory)}";
                style.normal.textColor = totalMemory > 100 * 1024 * 1024 ? Color.red : Color.white;
                GUI.Label(new Rect(10, 60, 300, 50), memoryText, style);
            }
        }
    }

    string FormatBytes(long bytes)
    {
        string[] suffixes = { "B", "KB", "MB", "GB" };
        int counter = 0;
        decimal number = bytes;
        while (Math.Round(number / 1024) >= 1)
        {
            number = number / 1024;
            counter++;
        }
        return string.Format("{0:n1} {1}", number, suffixes[counter]);
    }
}

```

---

## 5. 📂 项目结构规范 (Project Structure)

混乱的文件夹是烂尾的第一步。

```text
Assets/
├── _Project/           # 只有这里放你自己的资源，把插件和下载的资源隔离开
│   ├── Scripts/
│   │   ├── Core/       # 核心系统 (GameManager, EventBus)
│   │   ├── Gameplay/   # 玩法逻辑 (Tower, Enemy)
│   │   ├── UI/
│   │   └── Utils/
│   ├── Prefabs/
│   ├── ScriptableObjects/
│   ├── Materials/
│   └── Scenes/
├── Plugins/            # 第三方插件 (DoTween, UniTask)
└── Resources/          # ⚠️ 尽量别用！会拖慢启动速度。用 Addressables 或直接引用。
```