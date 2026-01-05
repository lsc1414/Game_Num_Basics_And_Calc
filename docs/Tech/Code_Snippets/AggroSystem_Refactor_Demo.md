# 몬스터仇恨系统重构示例 (Monster Aggro System Refactor Demo)

本文档展示了如何将 `Design/Mechanics/Aggro_System.md` 中定义的怪物仇恨系统，通过我们设计的 `DecisionEngine` 进行重构。这使得仇恨逻辑更加模块化、可配置，并能轻松扩展新的仇恨考量因素。

---

## 1. 模拟 `IAggroTarget` 实现

为了与 `DecisionSystem` 的通用接口对接，我们需要确保所有可被仇恨的目标（玩家、防御塔、召唤物）都实现了相应的接口。

```csharp
using UnityEngine;
using System.Collections.Generic;
using Vampirefall.DecisionSystem; // 引入DecisionSystem命名空间

// 假设我们有一个全局的EntityType枚举 (已在DecisionSystem_Core_Classes.md中定义)
// public enum EntityType { Player, TankTower, StandardTower, Minion, Nexus, Obstacle, Boss, Elite }

// 扩展 IAggroTarget 接口以继承我们通用的数据接口
public interface IAggroTargetRefactored : IPositionable, IHealth, IHasEntityType, IThreatable
{
    // 可以保留原 Aggro_System.md 中的 GetThreatModifier 或 IsValid 方法，
    // 但 IsValid 最好转化为 IFilter，GetThreatModifier 的逻辑则融入 Score
    // bool IsValid(); 
}

// 模拟一个可被仇恨的目标（例如：玩家或防御塔）
public class MockTarget : MonoBehaviour, IAggroTargetRefactored
{
    public string ID { get; set; } = System.Guid.NewGuid().ToString(); // 用于ThreatScorer查找
    public Vector3 Position => transform.position;
    public float CurrentHealth { get; set; } = 100f;
    public float MaxHealth { get; set; } = 100f;
    public bool IsAlive => CurrentHealth > 0;
    public EntityType EntityType { get; set; } = EntityType.Player; // 默认玩家

    public void TakeDamage(float amount)
    {
        CurrentHealth -= amount;
        if (CurrentHealth <= 0) CurrentHealth = 0;
    }
}
```

## 2. Refactored `AggroAgent` 实现

怪物身上的 `AggroAgent` 现在不再自己维护复杂的仇恨计算逻辑，而是将其委托给 `DecisionEngine`。

```csharp
using UnityEngine;
using System.Collections.Generic;
using Vampirefall.DecisionSystem;
using System.Linq; // for Select

public class AggroAgent : MonoBehaviour
{
    [Header("配置")]
    public float aggroCheckInterval = 0.5f; // 仇恨检测间隔
    public float aggroRange = 15f;           // 仇恨范围
    public EntityType monsterEntityType = EntityType.Minion; // 怪物自身类型

    private DecisionEngine<IAggroTargetRefactored> _decisionEngine;
    private IAggroTargetRefactored _currentTarget;
    private Dictionary<string, float> _threatTable = new Dictionary<string, float>(); // 怪物自身维护的仇恨表
    private float _aggroCheckTimer;

    // --- Unity Callbacks ---
    void Start()
    {
        InitializeDecisionEngine();
        _aggroCheckTimer = Random.Range(0f, aggroCheckInterval); // 错开计时器，避免同时计算
    }

    void Update()
    {
        _aggroCheckTimer -= Time.deltaTime;
        if (_aggroCheckTimer <= 0)
        {
            _aggroCheckTimer = aggroCheckInterval;
            FindBestTarget();
        }

        // 假设怪物会朝 _currentTarget 移动或攻击
        if (_currentTarget != null && _currentTarget.IsAlive)
        {
            Debug.DrawLine(transform.position, _currentTarget.Position, Color.red);
        } else {
            // 如果目标死亡或无效，重新索敌或回基地
            _currentTarget = null;
        }
    }

    // --- Public Methods ---
    /// <summary>
    /// 当怪物受到伤害、被嘲讽等时调用，更新仇恨值
    /// </summary>
    public void AddThreat(IAggroTargetRefactored source, float amount)
    {
        if (_threatTable.ContainsKey(source.ID))
        {
            _threatTable[source.ID] += amount;
        }
        else
        {
            _threatTable[source.ID] = amount;
        }
        // 立即触发一次仇恨检查，防止反应迟钝
        FindBestTarget(); 
    }

    // --- Private Methods ---
    private void InitializeDecisionEngine()
    {
        _decisionEngine = new DecisionEngine<IAggroTargetRefactored>();

        // 过滤器：目标必须活着
        _decisionEngine.AddFilter(new AliveFilter<IAggroTargetRefactored>(t => t)); // 获取IHealth接口的委托

        // 评分器：
        // 1. 仇恨表评分 (权重高)
        _decisionEngine.AddScorer(new ThreatScorer<IAggroTargetRefactored>(10f, t => t)); // 获取IThreatable接口的委托

        // 2. 距离评分 (越近分越高，有MaxAggroRange)
        _decisionEngine.AddScorer(new DistanceScorer<IAggroTargetRefactored>(5f, t => t.Position, aggroRange));

        // 3. 实体类型优先级评分 (Nexus, TankTower优先级更高)
        var priorityMap = new Dictionary<EntityType, float>()
        {
            { EntityType.Nexus, 200f },       // 基地核心永远最高优先级
            { EntityType.TankTower, 100f },   // 嘲讽塔
            { EntityType.Player, 50f },       // 玩家
            { EntityType.StandardTower, 20f },// 普通防御塔
            { EntityType.Minion, 5f }         // 召唤物
        };
        _decisionEngine.AddScorer(new PriorityScorer<IAggroTargetRefactored>(1f, t => t, priorityMap));

        // TODO: 添加其他评分器，如：距离我出生点多远 (Leash)，是否在施法，血量最低等
    }

    private void FindBestTarget()
    {
        // 1. 获取所有潜在候选人 (优化点：只获取 aggroRange 内的敌人)
        // 假设有一个 GameManager 来管理所有 IAggroTargetRefactored
        List<IAggroTargetRefactored> allTargets = GameManager.GetAllAggroTargetsInRadius(transform.position, aggroRange);

        // 2. 准备决策上下文
        DecisionContext ctx = new DecisionContext();
        ctx.Origin = transform.position;
        ctx.Source = gameObject;
        ctx.Set("AggroThreatTable", _threatTable); // 将自身的仇恨表放入上下文供ThreatScorer使用

        // 3. 执行决策
        IAggroTargetRefactored newTarget = _decisionEngine.SelectBest(allTargets, ctx);

        // 4. 切换目标逻辑 (考虑到目标粘性)
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

    // 假设需要一个 GameManager 来获取所有 IAggroTargetRefactored
    public static class GameManager // 简化的伪代码
    {
        private static List<IAggroTargetRefactored> _allAggroTargets = new List<IAggroTargetRefactored>();

        public static void RegisterAggroTarget(IAggroTargetRefactored target) => _allAggroTargets.Add(target);
        public static void UnregisterAggroTarget(IAggroTargetRefactored target) => _allAggroTargets.Remove(target);

        public static List<IAggroTargetRefactored> GetAllAggroTargetsInRadius(Vector3 origin, float radius)
        {
            // 真实的实现会使用 Physics.OverlapSphereNonAlloc 和空间划分优化
            return _allAggroTargets.Where(t => Vector3.Distance(origin, t.Position) <= radius).ToList();
        }
    }

    /// <summary>
    /// 目标切换逻辑，考虑目标粘性（防止频繁切换）
    /// </summary>
    private bool ShouldSwitchTarget(IAggroTargetRefactored newTarget, IAggroTargetRefactored currentTarget)
    {
        if (currentTarget == null || !currentTarget.IsAlive) return true; // 没有当前目标或已死亡，直接切换

        // 计算当前目标和新目标的最终分数
        // 这里需要重新运行 DecisionEngine 的 Evaluate 方法
        DecisionContext ctx = new DecisionContext();
        ctx.Origin = transform.position;
        ctx.Source = gameObject;
        ctx.Set("AggroThreatTable", _threatTable);

        float currentTargetScore = GetTargetScore(currentTarget, ctx);
        float newTargetScore = GetTargetScore(newTarget, ctx);

        // 目标切换阈值 (例如，新目标的分数必须比当前目标高20%才切换)
        float switchThreshold = 1.2f; // 可以配置
        if (newTargetScore > currentTargetScore * switchThreshold)
        {
            return true;
        }

        return false;
    }

    /// <summary>
    /// 辅助方法：计算单个目标的总分数
    /// </summary>
    private float GetTargetScore(IAggroTargetRefactored target, DecisionContext ctx)
    {
        if (!(_decisionEngine as dynamic).PassesFilters(target, ctx)) return float.MinValue; // 过滤器判断
        
        float score = 0f;
        foreach (var scorer in (_decisionEngine as dynamic)._scorers) // 反射访问私有字段，实际应该通过公有方法
        {
            score += scorer.Evaluate(target, ctx);
        }
        return score;
    }
}
```
