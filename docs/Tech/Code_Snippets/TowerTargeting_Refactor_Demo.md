---
sidebarTitle: "防御塔索敌系统重构示例"
title: "防御塔索敌系统重构示例"
---
> **摘要**：本文档展示了如何将 `Design/Mechanics/Tower_Defense_System.md` 中定义的防御塔索敌逻辑，通过我们设计的 `DecisionEngine` 进行重构。这使得不同的防御塔可以灵活配置其索敌策略，而无需编写重复的逻辑。

## 1. 模拟 `Enemy` 实现

为了与 `DecisionSystem` 的通用接口对接，敌人必须实现相应的接口。

```csharp
using UnityEngine;
using System.Collections.Generic;
using Vampirefall.DecisionSystem; // 引入DecisionSystem命名空间

// 模拟一个敌人，实现所有必要的接口
public class MockEnemy : MonoBehaviour, IPositionable, IHealth, IHasEntityType, IHasTags
{
    public string ID { get; set; } = System.Guid.NewGuid().ToString(); // 假设有ID
    public Vector3 Position => transform.position;
    public float CurrentHealth { get; set; } = 100f;
    public float MaxHealth { get; set; } = 100f;
    public bool IsAlive => CurrentHealth > 0;
    public EntityType EntityType { get; set; } = EntityType.Minion; // 默认小兵
    public List<string> Tags { get; set; } = new List<string>(); // 例如 "Armored", "Wet", "Flying"

    public void TakeDamage(float amount)
    {
        CurrentHealth -= amount;
        if (CurrentHealth <= 0) CurrentHealth = 0;
    }

    public void SetTags(params string[] newTags) {
        Tags.Clear();
        Tags.AddRange(newTags);
    }
}
```

## 2. Refactored `TowerController` 实现

防御塔不再需要编写复杂的 `if/else` 链来判断目标，而是通过配置 `DecisionEngine` 来定义行为。

```csharp
using UnityEngine;
using System.Collections.Generic;
using Vampirefall.DecisionSystem;
using System.Linq;

public class TowerController : MonoBehaviour
{
    public enum TowerType { BasicBallista, SniperTurret, TeslaCoil }

    [Header("塔配置")]
    public TowerType towerType;
    public float attackRange = 10f;
    public float attackRate = 1f; // 攻击间隔
    public float damage = 20f;

    private DecisionEngine<MockEnemy> _decisionEngine;
    private MockEnemy _currentTarget;
    private float _attackTimer;

    // --- Unity Callbacks ---
    void Start()
    {
        InitializeDecisionEngine();
        _attackTimer = 1f / attackRate;
    }

    void Update()
    {
        // 如果没有目标或者目标无效，则重新索敌
        if (_currentTarget == null || !_currentTarget.IsAlive || Vector3.Distance(transform.position, _currentTarget.Position) > attackRange)
        {
            FindNewTarget();
        }

        // 如果有目标，进行攻击
        if (_currentTarget != null && _currentTarget.IsAlive)
        {
            _attackTimer -= Time.deltaTime;
            if (_attackTimer <= 0)
            {
                AttackTarget(_currentTarget);
                _attackTimer = 1f / attackRate;
            }
            // 绘制连线以示索敌
            Debug.DrawLine(transform.position, _currentTarget.Position, Color.green);
        }
    }

    // --- Private Methods ---
    private void InitializeDecisionEngine()
    {
        _decisionEngine = new DecisionEngine<MockEnemy>();

        // 基础过滤器：在射程内且目标必须活着
        _decisionEngine.AddFilter(new RangeFilter<MockEnemy>(transform.position, attackRange, (e) => e.Position));
        _decisionEngine.AddFilter(new AliveFilter<MockEnemy>((e) => e)); // 获取IHealth接口的委托

        // 根据塔类型配置索敌逻辑
        switch (towerType)
        {
            case TowerType.BasicBallista:
                // 基础箭塔：优先最近，次优先残血小兵
                _decisionEngine.AddScorer(new DistanceScorer<MockEnemy>(3f, (e) => e.Position));
                _decisionEngine.AddScorer(new HealthScorer<MockEnemy>(1f, (e) => e, HealthScoreMode.Lowest));
                _decisionEngine.AddScorer(new PriorityScorer<MockEnemy>(0.5f, (e) => e, new Dictionary<EntityType, float>
                {
                    { EntityType.Boss, 100f },
                    { EntityType.Elite, 50f },
                    { EntityType.Minion, 10f }
                }));
                break;

            case TowerType.SniperTurret:
                // 狙击塔：过滤掉低血量目标 (防止伤害溢出)，优先 Boss/精英，优先高血量
                _decisionEngine.AddFilter(new MinHealthFilter<MockEnemy>(damage * 0.8f, (e) => e)); // 过滤掉生命值低于80%伤害的目标
                _decisionEngine.AddScorer(new PriorityScorer<MockEnemy>(5f, (e) => e, new Dictionary<EntityType, float>
                {
                    { EntityType.Boss, 1000f },
                    { EntityType.Elite, 500f }
                }));
                _decisionEngine.AddScorer(new HealthScorer<MockEnemy>(2f, (e) => e, HealthScoreMode.Highest));
                _decisionEngine.AddScorer(new DistanceScorer<MockEnemy>(0.5f, (e) => e.Position, attackRange, true)); // 稍微偏远
                break;

            case TowerType.TeslaCoil:
                // 特斯拉塔：优先带特定标签的（如“湿润”），其次是集群目标（TODO: ClusterScorer）
                _decisionEngine.AddScorer(new TagSynergyScorer<MockEnemy>(4f, (e) => e, new List<string> { "Wet", "Conductive" }));
                _decisionEngine.AddScorer(new DistanceScorer<MockEnemy>(2f, (e) => e.Position)); // 偏近
                // _decisionEngine.AddScorer(new ClusterScorer<MockEnemy>(3f, (e) => e.Position)); // 假设有此评分器
                break;
        }
    }

    private void FindNewTarget()
    {
        // 1. 获取所有潜在候选人 (优化点：只获取 attackRange 内的敌人)
        List<MockEnemy> allEnemies = EnemySpawnManager.GetAllActiveEnemiesInRadius(transform.position, attackRange);

        // 2. 准备决策上下文
        DecisionContext ctx = new DecisionContext();
        ctx.Origin = transform.position;
        ctx.Source = gameObject;
        // 可以将塔自身的攻击类型、状态等放入Context供Scorer使用

        // 3. 执行决策
        _currentTarget = _decisionEngine.SelectBest(allEnemies, ctx);
    }

    private void AttackTarget(MockEnemy enemy)
    {
        Debug.Log($"{name} attacking {enemy.name} at {enemy.Position} for {damage} damage.");
        enemy.TakeDamage(damage);
        if (!enemy.IsAlive)
        {
            Debug.Log($"{enemy.name} defeated!");
            _currentTarget = null; // 目标死亡
        }
    }
}

// 假设存在一个管理所有敌人的单例
public static class EnemySpawnManager // 简化的伪代码
{
    private static List<MockEnemy> _allActiveEnemies = new List<MockEnemy>();

    public static void RegisterEnemy(MockEnemy enemy) => _allActiveEnemies.Add(enemy);
    public static void UnregisterEnemy(MockEnemy enemy) => _allActiveEnemies.Remove(enemy);

    public static List<MockEnemy> GetAllActiveEnemiesInRadius(Vector3 origin, float radius)
    {
        // 真实的实现会使用 Physics.OverlapSphereNonAlloc 和空间划分优化
        return _allActiveEnemies.Where(e => Vector3.Distance(origin, e.Position) <= radius).ToList();
    }
}
```

## 3. 标准过滤器实现 (Standard Filter Implementations)

在 `Tech/Code_Snippets/DecisionSystem_Core_Classes.md` 中只定义了 `IFilter<T>` 接口，这里提供一些常用的过滤器实现。

### `AliveFilter` (存活过滤器)
```csharp
using System;

namespace Vampirefall.DecisionSystem
{
    /// <summary>
    /// 过滤器：只保留活着的候选人
    /// </summary>
    public class AliveFilter<T> : IFilter<T> // where T : IHealth
    {
        private Func<T, IHealth> _getHealthFunc;

        public AliveFilter(Func<T, IHealth> getHealthFunc)
        {
            _getHealthFunc = getHealthFunc ?? throw new ArgumentNullException(nameof(getHealthFunc));
        }

        public bool IsValid(T candidate, DecisionContext ctx)
        {
            IHealth health = _getHealthFunc(candidate);
            return health != null && health.IsAlive;
        }
    }
}
```

### `RangeFilter` (射程过滤器)
```csharp
using UnityEngine;
using System; // For Func

namespace Vampirefall.DecisionSystem
{
    /// <summary>
    /// 过滤器：只保留在指定射程内的候选人
    /// </summary>
    public class RangeFilter<T> : IFilter<T> // where T : IPositionable
    {
        private Vector3 _origin;
        private float _range;
        private Func<T, Vector3> _getPositionFunc;

        public RangeFilter(Vector3 origin, float range, Func<T, Vector3> getPositionFunc)
        {
            _origin = origin;
            _range = range;
            _getPositionFunc = getPositionFunc ?? throw new ArgumentNullException(nameof(getPositionFunc));
        }

        public bool IsValid(T candidate, DecisionContext ctx)
        {
            Vector3 candidatePos = _getPositionFunc(candidate);
            return Vector3.Distance(_origin, candidatePos) <= _range;
        }
    }
}
```

### `MinHealthFilter` (最低血量过滤器)
用于狙击塔，防止伤害溢出。

```csharp
using System;

namespace Vampirefall.DecisionSystem
{
    /// <summary>
    /// 过滤器：只保留生命值高于指定阈值的候选人 (例如，防止伤害溢出)
    /// </summary>
    public class MinHealthFilter<T> : IFilter<T> // where T : IHealth
    {
        private float _minHealthThreshold;
        private Func<T, IHealth> _getHealthFunc;

        public MinHealthFilter(float minHealthThreshold, Func<T, IHealth> getHealthFunc)
        {
            _minHealthThreshold = minHealthThreshold;
            _getHealthFunc = getHealthFunc ?? throw new ArgumentNullException(nameof(getHealthFunc));
        }

        public bool IsValid(T candidate, DecisionContext ctx)
        {
            IHealth health = _getHealthFunc(candidate);
            return health != null && health.IsAlive && health.CurrentHealth >= _minHealthThreshold;
        }
    }
}
```
