---
sidebarTitle: "🚀 决策系统性能优化示例"
---

# 🚀 决策系统性能优化示例 (Decision System Performance Optimization Demo)

本文档展示了如何将时间分片 (Time-Slicing) 和空间划分 (Spatial Partitioning) 策略集成到 `DecisionEngine` 的工作流中，以确保游戏在高并发计算时依然流畅。

---

## 1. 时间分片 (Time-Slicing)

在游戏中，有数百个 AI 同时进行索敌或决策是非常常见的。如果所有单位都在同一帧内更新其 `DecisionEngine`，会导致帧率骤降。时间分片通过在多帧之间分配计算负载来解决这个问题。

### 1.1 `IDecisionRequester` 接口

定义一个接口，任何需要定期执行决策的 AI 或塔都应实现它。

```csharp
using Vampirefall.DecisionSystem; // 引入DecisionSystem命名空间

namespace Vampirefall.DecisionSystem.Performance
{
    /// <summary>
    /// 任何需要DecisionScheduler调度的决策请求者
    /// </summary>
    public interface IDecisionRequester
    {
        void PerformDecision(DecisionContext sharedContext);
        bool IsActive { get; } // 是否还需要继续调度
        int Priority { get; }  // 调度优先级 (可选)
    }
}
```

### 1.2 `DecisionScheduler` (决策调度器)

一个单例 (Singleton) 或全局服务，负责管理和调度所有 `IDecisionRequester`。

```csharp
using UnityEngine;
using System.Collections.Generic;
using System.Linq; // For OrderBy

namespace Vampirefall.DecisionSystem.Performance
{
    public class DecisionScheduler : MonoBehaviour
    {
        public static DecisionScheduler Instance { get; private set; }

        [SerializeField] private int _requestsPerFrame = 10; // 每帧处理多少个决策请求

        private List<IDecisionRequester> _requesters = new List<IDecisionRequester>();
        private int _currentIndex = 0;

        void Awake()
        {
            if (Instance != null && Instance != this)
            {
                Destroy(gameObject);
            }
            else
            {
                Instance = this;
                DontDestroyOnLoad(gameObject);
            }
        }

        void Update()
        {
            if (_requesters.Count == 0) return;

            // 用于所有决策请求的共享上下文（减少GC，并在多个请求间传递通用数据）
            // 在实际使用中，可能每个请求都会填充一些特定的上下文数据
            DecisionContext sharedContext = new DecisionContext();

            for (int i = 0; i < _requestsPerFrame; i++)
            {
                if (_requesters.Count == 0) break; // 防止列表为空

                _currentIndex = (_currentIndex + 1) % _requesters.Count;
                IDecisionRequester currentRequester = _requesters[_currentIndex];

                if (currentRequester.IsActive)
                {
                    sharedContext.Reset(); // 重置上下文，准备下一个请求
                    currentRequester.PerformDecision(sharedContext);
                }
                else
                {
                    // 如果请求者不再活跃，将其移除
                    _requesters.RemoveAt(_currentIndex);
                    _currentIndex--; // 移除后索引需要调整
                    if (_currentIndex < 0) _currentIndex = 0;
                }

                if (_requesters.Count == 0) break;
            }
        }

        public void RegisterRequester(IDecisionRequester requester)
        {
            if (!_requesters.Contains(requester))
            {
                _requesters.Add(requester);
                // 可以根据优先级进行排序：_requesters = _requesters.OrderByDescending(r => r.Priority).ToList();
            }
        }

        public void UnregisterRequester(IDecisionRequester requester)
        {
            _requesters.Remove(requester);
        }
    }
}
```

### 1.3 `AggroAgent` (或其他AI) 集成调度器

```csharp
using UnityEngine;
using System.Collections.Generic;
using Vampirefall.DecisionSystem;
using Vampirefall.DecisionSystem.Performance;
using System.Linq; // for Select

// 假设 AggroAgent 已经像之前示例一样被重构了
public partial class AggroAgent : MonoBehaviour, IDecisionRequester
{
    // ... 其他 AggroAgent 字段和方法 ...
    
    // IDecisionRequester 接口实现
    public bool IsActive => gameObject.activeInHierarchy && _currentTarget != null && _currentTarget.IsAlive; // 怪物存活且有目标

    public int Priority => (int)(Vector3.Distance(transform.position, _currentTarget.Position)); // 优先处理近距离目标

    void OnEnable() {
        // 注册到调度器
        DecisionScheduler.Instance?.RegisterRequester(this);
    }

    void OnDisable() {
        // 从调度器注销
        DecisionScheduler.Instance?.UnregisterRequester(this);
    }

    // 将原先的 FindBestTarget 逻辑放入 PerformDecision
    public void PerformDecision(DecisionContext sharedContext)
    {
        // 1. 获取所有潜在候选人 (使用空间划分，下一节讨论)
        List<IAggroTargetRefactored> allTargets = GameManager.GetAllAggroTargetsInRadius(transform.position, aggroRange);

        // 2. 准备决策上下文 (填充当前请求者的特定数据)
        sharedContext.Origin = transform.position;
        sharedContext.Source = gameObject;
        sharedContext.Set("AggroThreatTable", _threatTable); // 将自身的仇恨表放入上下文供ThreatScorer使用

        // 3. 执行决策
        IAggroTargetRefactored newTarget = _decisionEngine.SelectBest(allTargets, sharedContext);

        // 4. 切换目标逻辑
        if (newTarget != null && ShouldSwitchTarget(newTarget, _currentTarget))
        {
            _currentTarget = newTarget;
            // TODO: 通知 NavMeshAgent 新目标
        }
        else if (newTarget == null && _currentTarget != null && !_currentTarget.IsAlive)
        {
            _currentTarget = null; // 当前目标死亡
        }
    }

    // Note: 原来的 Update 方法只需要处理移动/攻击动画，不再需要 FindBestTarget()
}
```

---

## 2. 空间划分 (Spatial Partitioning)

空间划分系统是提供 `Candidates` 列表给 `DecisionEngine` 的关键优化。它将整个游戏世界划分为多个区域，从而将“遍历所有敌人”的操作变为“查询局部区域的敌人”。

### 2.1 概念：Grid 或 QuadTree

*   **Grid System (网格系统):**
    *   **原理:** 将世界地图划分为均匀的网格，每个网格单元存储其中的所有单位引用。
    *   **查询:** 塔或 AI 只需查询其射程覆盖的几个网格单元，就能获得潜在目标列表。
    *   **适用:** 地形平坦、单位分布相对均匀的 2D 或伪 3D 游戏（如标准塔防）。
*   **QuadTree (四叉树/八叉树):**
    *   **原理:** 递归地将空间划分为更小的象限，直到每个象限内的单位数量达到某个阈值。
    *   **查询:** 快速定位到包含查询区域的象限，并只检索这些象限内的单位。
    *   **适用:** 单位分布稀疏、地图广阔、有垂直高度的 3D 游戏。

### 2.2 伪代码：优化 `GetAllAggroTargetsInRadius`

这个方法现在应该由一个专门的 **空间管理服务** 提供，而不是遍历一个大列表。

```csharp
using UnityEngine;
using System.Collections.Generic;
using System.Linq;

// 假设我们有一个全局空间管理服务
public static class SpatialManager // 这是一个概念性的Manager，实际会更复杂
{
    // ... 内部管理 Grid 或 QuadTree 数据结构 ...

    public static List<IAggroTargetRefactored> GetEntitiesInRadius(Vector3 origin, float radius)
    {
        // 实际实现：
        // 1. 根据 origin 和 radius 计算出需要查询的网格单元或四叉树节点。
        // 2. 从这些单元/节点中高效地检索出所有 IAggroTargetRefactored。
        // 3. 严格地说，Physics.OverlapSphereNonAlloc 是 Unity 提供的加速结构。
        //    List<Collider> results = new List<Collider>();
        //    Physics.OverlapSphereNonAlloc(origin, radius, results, targetLayerMask);
        //    return results.Select(c => c.GetComponent<IAggroTargetRefactored>()).ToList();
        
        // 为了演示，我们继续使用简化的 GameManager.GetAllAggroTargetsInRadius
        // 但请记住，真实项目会替换它。
        return GameManager.GetAllAggroTargetsInRadius(origin, radius);
    }
}

// 之前的 GameManager 伪代码中的 GetAllAggroTargetsInRadius 会被调用
// class GameManager { ... } // 见 AggroSystem_Refactor_Demo.md
```

### 2.3 `AggroAgent` 中的应用

当 `AggroAgent.PerformDecision` 被调用时，它不再依赖一个全局的 `_allAggroTargets` 列表。

```csharp
// AggroAgent.PerformDecision 方法的一部分
public void PerformDecision(DecisionContext sharedContext)
{
    // **优化点：通过 SpatialManager 获取候选人列表**
    List<IAggroTargetRefactored> allTargets = SpatialManager.GetEntitiesInRadius(transform.position, aggroRange);

    // ... 后续逻辑不变 ...
}
```

---
