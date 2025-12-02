# 🎲 肉鸽强化抽取系统重构示例 (Perk Drafting System Refactor Demo)

本文档展示了如何将 `Design/Mechanics/Roguelike_Perks.md` 中定义的肉鸽强化（Perk）抽取逻辑，通过我们设计的 `DecisionEngine` 进行重构。这使得 Perk 池的加权随机选择、流派偏好和稀有度控制变得高度可配置。

---

## 1. 模拟 `PerkData` 实现

Perk 数据需要实现 `IHasTags` 和 `IHasRarity` 接口，以便评分器对其进行评估。

```csharp
using System.Collections.Generic;
using Vampirefall.DecisionSystem; // 引入DecisionSystem命名空间

// 模拟一个强化数据对象
public class PerkData : IHasTags, IHasRarity
{
    public string ID { get; set; }
    public string Name { get; set; }
    public string Description { get; set; }
    public List<string> Tags { get; set; } = new List<string>();
    public Rarity Rarity { get; set; } = Rarity.Common;

    // 假设每个Perk还可以有冲突Perk的列表
    public List<string> ConflictingPerkIDs { get; set; } = new List<string>();

    public PerkData(string id, string name, Rarity rarity, List<string> tags = null)
    {
        ID = id;
        Name = name;
        Rarity = rarity;
        Tags = tags ?? new List<string>();
    }

    public override string ToString()
    {
        return $"[{Rarity}] {Name} (Tags: {string.Join(", ", Tags)})";
    }
}
```

## 2. `PerkBanFilter` 实现

为了避免玩家抽到已有的 Perk 或与当前 Build 冲突的 Perk，我们需要一个过滤器。

```csharp
using System.Collections.Generic;
using System.Linq;

namespace Vampirefall.DecisionSystem
{
    /// <summary>
    /// 过滤器：排除玩家已拥有或被禁止的Perk
    /// </summary>
    public class PerkBanFilter : IFilter<PerkData>
    {
        private List<string> _playerOwnedPerkIDs;
        private List<string> _blacklistedPerkIDs; // 例如，与玩家当前Build冲突的Perk

        public PerkBanFilter(List<string> playerOwnedPerkIDs, List<string> blacklistedPerkIDs = null)
        {
            _playerOwnedPerkIDs = playerOwnedPerkIDs ?? new List<string>();
            _blacklistedPerkIDs = blacklistedPerkIDs ?? new List<string>();
        }

        public bool IsValid(PerkData candidate, DecisionContext ctx)
        {
            // 排除已拥有的Perk
            if (_playerOwnedPerkIDs.Contains(candidate.ID))
            {
                return false;
            }
            // 排除黑名单Perk
            if (_blacklistedPerkIDs.Contains(candidate.ID))
            {
                return false;
            }
            // 排除与已拥有Perk冲突的Perk (从PerkData自身的冲突列表判断)
            // 需要遍历 _playerOwnedPerkIDs 才能判断，或者在Context中传入玩家的冲突Perk列表
            // 为了简化示例，这里不实现复杂的冲突逻辑，只基于ID黑名单
            return true;
        }

        /// <summary>
        /// 动态更新黑名单，例如当玩家选择一个Perk后，将其冲突Perk加入黑名单
        /// </summary>
        public void UpdateBlacklist(List<string> newBlacklist)
        {
            _blacklistedPerkIDs = newBlacklist;
        }
    }
}
```

## 3. `PerkDraftingSystem` 实现

核心系统使用 `DecisionEngine` 进行加权随机抽取。

```csharp
using UnityEngine;
using System.Collections.Generic;
using Vampirefall.DecisionSystem;
using System.Linq;

public class PerkDraftingSystem : MonoBehaviour
{
    [Header("配置")]
    public int draftOptionCount = 3; // 每次提供多少个Perk供选择
    
    private DecisionEngine<PerkData> _decisionEngine;
    private PerkBanFilter _perkBanFilter;
    private List<PerkData> _allAvailablePerks; // 所有Perk的Master List
    private List<PerkData> _playerOwnedPerks = new List<PerkData>();
    private List<string> _playerSynergyTags = new List<string> { "Fire", "Melee" }; // 模拟玩家当前Build的标签

    void Start()
    {
        InitializePerkPool();
        InitializeDecisionEngine();
    }

    void InitializePerkPool()
    {
        // 模拟加载所有Perk
        _allAvailablePerks = new List<PerkData>
        {
            new PerkData("P_FireDmg", "火焰强化", Rarity.Common, new List<string> { "Fire", "Damage" }),
            new PerkData("P_IceDmg", "冰霜强化", Rarity.Common, new List<string> { "Ice", "Damage" }),
            new PerkData("P_MeleeCrit", "近战暴击", Rarity.Rare, new List<string> { "Melee", "Crit" }),
            new PerkData("P_RangedSpeed", "远程攻速", Rarity.Rare, new List<string> { "Ranged", "AttackSpeed" }),
            new PerkData("P_BloodMagic", "血魔法", Rarity.Legendary, new List<string> { "Life", "Skill" }) { ConflictingPerkIDs = new List<string>{"P_ManaShield"} },
            new PerkData("P_ManaShield", "法力护盾", Rarity.Epic, new List<string> { "Mana", "Defense" }) { ConflictingPerkIDs = new List<string>{"P_BloodMagic"} },
            new PerkData("P_Fireball", "火球术", Rarity.Rare, new List<string> { "Fire", "Skill" }),
            new PerkData("P_HealthBoost", "生命增幅", Rarity.Common, new List<string> { "Defense" }),
            new PerkData("P_QuickFeet", "疾速步伐", Rarity.Common, new List<string> { "Movement" }),
            new PerkData("P_Phoenix", "凤凰涅槃", Rarity.Epic, new List<string> { "Fire", "Life" }),
            new PerkData("P_AuraOfMight", "力量光环", Rarity.Legendary, new List<string> { "Aura", "Damage" })
        };
    }

    void InitializeDecisionEngine()
    {
        _decisionEngine = new DecisionEngine<PerkData>();

        // 过滤器：排除已拥有或冲突的Perk
        _perkBanFilter = new PerkBanFilter(_playerOwnedPerks.Select(p => p.ID).ToList());
        _decisionEngine.AddFilter(_perkBanFilter);
        
        // 评分器：
        // 1. 稀有度评分 (权重高) - 基础权重，传说Perk得分最高
        var rarityWeights = new Dictionary<Rarity, float>()
        {
            { Rarity.Common, 1f },
            { Rarity.Rare, 2f },
            { Rarity.Epic, 4f },
            { Rarity.Legendary, 8f }
        };
        _decisionEngine.AddScorer(new RarityScorer<PerkData>(1f, p => p, rarityWeights));

        // 2. 标签协同评分 (权重中等) - 偏好与玩家现有Build标签匹配的Perk
        _decisionEngine.AddScorer(new TagSynergyScorer<PerkData>(2f, p => p)); // PlayerSynergyTags会从Context传入
        
        // TODO: 其他评分器，如：同类Perk数量过多时降低权重，或PityTimerScorer等
    }

    /// <summary>
    /// 触发一次Perk抽取，返回指定数量的Perk选项
    /// </summary>
    public List<PerkData> DraftPerks()
    {
        List<PerkData> draftedPerks = new List<PerkData>();
        HashSet<string> selectedThisDraft = new HashSet<string>(); // 避免本次抽取中重复出现
        
        DecisionContext ctx = new DecisionContext();
        ctx.Set("PlayerSynergyTags", _playerSynergyTags); // 将玩家Build标签放入Context

        // 为了避免在一次抽取中重复拿到同一个Perk，每次抽取后从池中临时移除
        List<PerkData> currentPool = new List<PerkData>(_allAvailablePerks);

        for (int i = 0; i < draftOptionCount; i++)
        {
            PerkData selectedPerk = _decisionEngine.SelectRandom(currentPool, ctx);
            if (selectedPerk != null)
            {
                draftedPerks.Add(selectedPerk);
                // 从当前抽取池中移除，避免本次Draft重复
                currentPool.Remove(selectedPerk); 
                selectedThisDraft.Add(selectedPerk.ID);
            }
        }
        
        Debug.Log($"Drafted Perks (Player Tags: {string.Join(", ", _playerSynergyTags)}):");
        foreach(var perk in draftedPerks)
        {
            Debug.Log($"- {perk}");
        }
        return draftedPerks;
    }

    /// <summary>
    /// 模拟玩家选择了一个Perk
    /// </summary>
    public void PlayerChosePerk(PerkData chosenPerk)
    {
        if (chosenPerk == null) return;

        Debug.Log($"Player chose: {chosenPerk.Name}");
        _playerOwnedPerks.Add(chosenPerk);

        // 更新过滤器黑名单，以便下次抽取时排除已选择和冲突的Perk
        List<string> newBlacklist = _playerOwnedPerks.SelectMany(p => p.ConflictingPerkIDs).ToList();
        _perkBanFilter.UpdateBlacklist(_playerOwnedPerkIDs.Select(p=>p.ID).ToList().Concat(newBlacklist).ToList());
        
        // 模拟更新玩家的协同标签 (例如，选择了火系Perk后，玩家Build标签中加入"Fire")
        if (chosenPerk.Tags.Any(tag => tag == "Fire")) {
            if (!_playerSynergyTags.Contains("Fire")) _playerSynergyTags.Add("Fire");
        }
    }

    // 简单触发器
    void Update() {
        if (Input.GetKeyDown(KeyCode.Space)) {
            Debug.Log("--- Drafting New Perks ---");
            List<PerkData> options = DraftPerks();
            if (options.Count > 0) {
                // 模拟玩家选择第一个Perk
                PlayerChosePerk(options[0]);
            }
        }
    }
}
```
