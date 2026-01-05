# 💻 核心代码定义 (Core Code Definitions)

本文档定义了通用决策系统的关键 C# 接口与类结构，包括核心引擎和一组标准评分器。

---

## 0. 基础数据接口 (Core Data Interfaces)

为了让评分器能够通用，候选对象 `T` 需要实现这些接口，以暴露必要的数据。

### `IPositionable`
```csharp
using UnityEngine;

namespace Vampirefall.DecisionSystem
{
    /// <summary>
    /// 可定位的物体，用于 DistanceScorer
    /// </summary>
    public interface IPositionable
    {
        Vector3 Position { get; }
    }
}
```

### `IHealth`
```csharp
namespace Vampirefall.DecisionSystem
{
    /// <summary>
    /// 具有生命值的物体，用于 HealthScorer
    /// </summary>
    public interface IHealth
    {
        float CurrentHealth { get; }
        float MaxHealth { get; }
        bool IsAlive { get; }
    }
}
```

### `IHasTags`
```csharp
using System.Collections.Generic;

namespace Vampirefall.DecisionSystem
{
    /// <summary>
    /// 具有标签列表的物体，用于 TagSynergyScorer
    /// </summary>
    public interface IHasTags
    {
        List<string> Tags { get; }
    }
}
```

### `IHasEntityType`
```csharp
using System.Collections.Generic;

namespace Vampirefall.DecisionSystem
{
    // 假设 EntityType 是一个全局定义的枚举，例如：
    public enum EntityType { Player, TankTower, StandardTower, Minion, Nexus, Obstacle, Boss, Elite }

    /// <summary>
    /// 具有实体类型的物体，用于 PriorityScorer
    /// </summary>
    public interface IHasEntityType
    {
        EntityType EntityType { get; }
    }
}
```

---

## 1. 基础接口 (Interfaces)

### `DecisionContext` (上下文)
用于在评分过程中传递环境数据。使用 `Dictionary` 实现灵活的黑板模式，同时也提供常用属性的快捷访问。

```csharp
using UnityEngine;
using System.Collections.Generic;

namespace Vampirefall.DecisionSystem
{
    /// <summary>
    /// 决策上下文：包含决策所需的所有环境信息
    /// </summary>
    public class DecisionContext
    {
        // --- 常用属性 (热数据，避免查字典) ---
        public Vector3 Origin { get; set; }         // 决策发起者的位置
        public GameObject Source { get; set; }      // 决策发起者实例
        
        // --- 扩展数据 (黑板) ---
        private Dictionary<string, object> _blackboard = new Dictionary<string, object>();

        public void Set<T>(string key, T value)
        {
            _blackboard[key] = value;
        }

        public T Get<T>(string key, T defaultValue = default)
        {
            if (_blackboard.TryGetValue(key, out object val))
            {
                return (T)val;
            }
            return defaultValue;
        }
        
        // 复用池接口 (可选)
        public void Reset() {
            _blackboard.Clear();
            Origin = Vector3.zero;
            Source = null;
        }
    }
}
```

### `IScorer<T>` (评分器)
核心逻辑单元。

```csharp
namespace Vampirefall.DecisionSystem
{
    /// <summary>
    /// 评分器接口：对单个候选人进行评分
    /// </summary>
    /// <typeparam name="T">候选人类型 (Enemy, PerkData, etc.)</typeparam>
    public interface IScorer<T>
    {
        /// <summary>
        /// 计算分数。
        /// </summary>
        /// <param name="candidate">待评估的目标</param>
        /// <param name="ctx">当前上下文</param>
        /// <returns>分数 (可以是负数)</returns>
        float Evaluate(T candidate, DecisionContext ctx);
    }
}
```

### `IFilter<T>` (过滤器)
用于在评分前剔除无效目标（硬性门槛）。

```csharp
namespace Vampirefall.DecisionSystem
{
    public interface IFilter<T>
    {
        /// <summary>
        /// 是否保留该候选人？
        /// </summary>
        bool IsValid(T candidate, DecisionContext ctx);
    }
}
```

---

## 2. 核心引擎 (Core Engine)

### `DecisionEngine<T>`
负责组装评分器并执行选择逻辑。

```csharp
using System.Collections.Generic;
using UnityEngine;
using System.Linq; // for OrderByDescending

namespace Vampirefall.DecisionSystem
{
    public class DecisionEngine<T>
    {
        private readonly List<IScorer<T>> _scorers = new List<IScorer<T>>();
        private readonly List<IFilter<T>> _filters = new List<IFilter<T>>();

        // --- 配置方法 ---
        public DecisionEngine<T> AddScorer(IScorer<T> scorer)
        {
            _scorers.Add(scorer);
            return this; // 链式调用
        }

        public DecisionEngine<T> AddFilter(IFilter<T> filter)
        {
            _filters.Add(filter);
            return this;
        }

        // --- 核心逻辑 A: 选出最优解 (Best Choice) ---
        // 适用于：AI索敌、自动拾取
        public T SelectBest(IEnumerable<T> candidates, DecisionContext ctx)
        {
            T bestCandidate = default;
            float maxScore = float.MinValue;
            bool foundAny = false;

            foreach (var candidate in candidates)
            {
                // 1. 过滤 (Hard Filter)
                if (!PassesFilters(candidate, ctx)) continue;

                // 2. 评分 (Scoring)
                float currentScore = 0f;
                for (int i = 0; i < _scorers.Count; i++)
                {
                    currentScore += _scorers[i].Evaluate(candidate, ctx);
                }

                // 3. 比较 (Comparison)
                if (currentScore > maxScore)
                {
                    maxScore = currentScore;
                    bestCandidate = candidate;
                    foundAny = true;
                }
            }

            return foundAny ? bestCandidate : default;
        }

        // --- 核心逻辑 B: 加权随机 (Weighted Random) ---
        // 适用于：掉落、抽卡
        public T SelectRandom(IEnumerable<T> candidates, DecisionContext ctx)
        {
            // 临时列表用于存储通过过滤的候选项及其权重
            // 注意：生产环境应使用 ListPool 避免 GC
            List<T> validCandidates = new List<T>();
            List<float> weights = new List<float>();
            float totalWeight = 0f;

            foreach (var candidate in candidates)
            {
                if (!PassesFilters(candidate, ctx)) continue;

                float weight = 0f;
                for (int i = 0; i < _scorers.Count; i++)
                {
                    weight += _scorers[i].Evaluate(candidate, ctx);
                }

                // 权重必须非负
                if (weight <= 0) continue;

                validCandidates.Add(candidate);
                weights.Add(weight);
                totalWeight += weight;
            }

            if (validCandidates.Count == 0) return default;

            // 轮盘赌算法 (Roulette Wheel Selection)
            float randomValue = Random.Range(0f, totalWeight);
            float runningTotal = 0f;

            for (int i = 0; i < weights.Count; i++)
            {
                runningTotal += weights[i];
                if (randomValue <= runningTotal)
                {
                    return validCandidates[i];
                }
            }
            // Fallback for floating point inaccuracies or if randomValue is exactly totalWeight
            return validCandidates.LastOrDefault(); 
        }

        private bool PassesFilters(T candidate, DecisionContext ctx)
        {
            for (int i = 0; i < _filters.Count; i++)
            {
                if (!_filters[i].IsValid(candidate, ctx)) return false;
            }
            return true;
        }
    }
}
```

---

## 3. 标准评分器实现 (Standard Scorer Implementations)

### `DistanceScorer` (距离评分)
通用性极强，用于 AI 和 塔防。

```csharp
using UnityEngine;
using System; // For Func

namespace Vampirefall.DecisionSystem
{
    public class DistanceScorer<T> : IScorer<T> // where T : IPositionable // No direct interface constraint here for flexibility
    {
        private float _weight;
        private float _maxDistance; // 超过此距离分数为0，或按最大距离计算
        private bool _inverse;      // true: 越远分越高; false: 越近分越高
        private Func<T, Vector3> _getPositionFunc; // 动态获取T的位置

        /// <summary>
        /// 构造函数
        /// </summary>
        /// <param name="weight">评分权重</param>
        /// <param name="getPositionFunc">一个委托，用于从候选对象T获取其Vector3位置</param>
        /// <param name="maxDistance">最大考量距离，超出按此距离计算，或直接返回0</param>
        /// <param name="inverse">是否反向：true为越远分越高，false为越近分越高</param>
        public DistanceScorer(float weight, Func<T, Vector3> getPositionFunc, float maxDistance = 20f, bool inverse = false)
        {
            _weight = weight;
            _getPositionFunc = getPositionFunc ?? throw new ArgumentNullException(nameof(getPositionFunc));
            _maxDistance = maxDistance;
            _inverse = inverse;
        }

        public float Evaluate(T candidate, DecisionContext ctx)
        {
            Vector3 candidatePos = _getPositionFunc(candidate);
            float dist = Vector3.Distance(candidatePos, ctx.Origin);
            
            // 超出最大距离则直接不给分 (或者按最远距离计算)
            if (dist > _maxDistance) return 0f; // 也可以 return (_inverse ? _maxDistance : 0f) * _weight;

            // 归一化距离 (0~1)
            float normalizedDist = dist / _maxDistance;
            
            float score;
            if (_inverse)
            {
                score = normalizedDist; // 越远分越高
            }
            else
            {
                score = 1f - normalizedDist; // 越近分越高
            }

            return score * _weight;
        }
    }
}
```

### `HealthScorer` (生命值评分)
根据生命值高低进行评分。

```csharp
using System; // For Func

namespace Vampirefall.DecisionSystem
{
    public enum HealthScoreMode { Lowest, Highest, PercentageRemaining }

    public class HealthScorer<T> : IScorer<T> // where T : IHealth
    {
        private float _weight;
        private HealthScoreMode _mode;
        private Func<T, IHealth> _getHealthFunc; // 动态获取T的IHealth接口

        /// <summary>
        /// 构造函数
        /// </summary>
        /// <param name="weight">评分权重</param>
        /// <param name="getHealthFunc">一个委托，用于从候选对象T获取其IHealth接口</param>
        /// <param name="mode">评分模式：最低血量优先，最高血量优先，或剩余百分比</param>
        public HealthScorer(float weight, Func<T, IHealth> getHealthFunc, HealthScoreMode mode = HealthScoreMode.Lowest)
        {
            _weight = weight;
            _getHealthFunc = getHealthFunc ?? throw new ArgumentNullException(nameof(getHealthFunc));
            _mode = mode;
        }

        public float Evaluate(T candidate, DecisionContext ctx)
        {
            IHealth health = _getHealthFunc(candidate);
            if (health == null || !health.IsAlive) return 0f; // 已死亡或无生命值属性则不给分

            float score = 0f;
            float healthRatio = health.CurrentHealth / health.MaxHealth; // 0-1之间

            switch (_mode)
            {
                case HealthScoreMode.Lowest:
                    score = 1f - healthRatio; // 血量越低，比值越小，1-比值越大
                    break;
                case HealthScoreMode.Highest:
                    score = healthRatio; // 血量越高，比值越大
                    break;
                case HealthScoreMode.PercentageRemaining:
                    score = healthRatio; // 直接按百分比
                    break;
            }
            return score * _weight;
        }
    }
}
```

### `TagSynergyScorer` (标签协同评分)
用于 Perk 系统，根据标签匹配度评分。

```csharp
using System.Collections.Generic;
using System.Linq; // For .Contains() and .Intersect()
using System; // For Func

namespace Vampirefall.DecisionSystem
{
    public class TagSynergyScorer<T> : IScorer<T> // where T : IHasTags
    {
        private float _weight;
        private Func<T, IHasTags> _getTagsFunc; // 动态获取T的IHasTags接口
        private List<string> _synergyTags; // 用于匹配的标签，可从Context或构造函数传入

        /// <summary>
        /// 构造函数
        /// </summary>
        /// <param name="weight">评分权重</param>
        /// <param name="getTagsFunc">一个委托，用于从候选对象T获取其IHasTags接口</param>
        /// <param name="synergyTags">期望匹配的协同标签列表</param>
        public TagSynergyScorer(float weight, Func<T, IHasTags> getTagsFunc, List<string> synergyTags = null)
        {
            _weight = weight;
            _getTagsFunc = getTagsFunc ?? throw new ArgumentNullException(nameof(getTagsFunc));
            _synergyTags = synergyTags; // 可以通过Context覆盖
        }

        public float Evaluate(T candidate, DecisionContext ctx)
        {
            IHasTags candidateTags = _getTagsFunc(candidate);
            if (candidateTags == null || candidateTags.Tags == null || candidateTags.Tags.Count == 0) return 0f;

            // 优先从 Context 获取协同标签，如果 Context 没有，则使用构造函数传入的
            List<string> currentSynergyTags = ctx.Get<List<string>>("PlayerSynergyTags", _synergyTags);
            if (currentSynergyTags == null || currentSynergyTags.Count == 0) return 0f;

            int matchCount = candidateTags.Tags.Intersect(currentSynergyTags).Count();
            
            // 简单地按匹配数量给分
            return matchCount * _weight;
        }
    }
}
```

### `PriorityScorer` (优先级评分)
根据实体类型给定固定分数。

```csharp
using System.Collections.Generic;
using System; // For Func

namespace Vampirefall.DecisionSystem
{
    // EntityType 枚举已在 IHasEntityType 定义处提供
    
    public class PriorityScorer<T> : IScorer<T> // where T : IHasEntityType
    {
        private float _weight;
        private Func<T, IHasEntityType> _getEntityTypeFunc; // 动态获取T的IHasEntityType接口
        private Dictionary<EntityType, float> _priorityMap;

        /// <summary>
        /// 构造函数
        /// </summary>
        /// <param name="weight">基础评分权重</param>
        /// <param name="getEntityTypeFunc">一个委托，用于从候选对象T获取其IHasEntityType接口</param>
        /// <param name="priorityMap">EntityType 到分数的映射</param>
        public PriorityScorer(float weight, Func<T, IHasEntityType> getEntityTypeFunc, Dictionary<EntityType, float> priorityMap)
        {
            _weight = weight;
            _getEntityTypeFunc = getEntityTypeFunc ?? throw new ArgumentNullException(nameof(getEntityTypeFunc));
            _priorityMap = priorityMap ?? throw new ArgumentNullException(nameof(priorityMap));
        }

        public float Evaluate(T candidate, DecisionContext ctx)
        {
            IHasEntityType entityType = _getEntityTypeFunc(candidate);
            if (entityType == null) return 0f;

            if (_priorityMap.TryGetValue(entityType.EntityType, out float basePriority))
            {
                return basePriority * _weight;
            }
            return 0f; // 未知实体类型不给分
        }
    }
}
```