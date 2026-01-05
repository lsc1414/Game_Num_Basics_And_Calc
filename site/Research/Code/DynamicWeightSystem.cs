using System;
using System.Collections.Generic;
using System.Linq;
using UnityEngine;

/// <summary>
/// 动态权重系统 - 根据玩家选择历史动态调整强化选项的出现概率
/// </summary>
public class DynamicWeightSystem
{
    private Dictionary<string, float> baseWeights;
    private Dictionary<string, int> tagSelections;
    private Dictionary<string, int> rarityMissCount;
    private int totalSelections = 0;
    
    // 系统参数
    private readonly float tagBiasFactor = 0.3f;      // 标签偏好系数
    private readonly float pityFactor = 0.8f;         // 防脸黑补偿系数
    private readonly int pityInterval = 5;           // 防脸黑间隔
    private readonly float diversityBonus = 0.1f;    // 多样性奖励
    
    public DynamicWeightSystem()
    {
        baseWeights = new Dictionary<string, float>();
        tagSelections = new Dictionary<string, int>();
        rarityMissCount = new Dictionary<string, int>();
        InitializeBaseWeights();
    }
    
    private void InitializeBaseWeights()
    {
        baseWeights["Common"] = 100f;
        baseWeights["Rare"] = 30f;
        baseWeights["Epic"] = 10f;
        baseWeights["Legendary"] = 3f;
        
        rarityMissCount["Rare"] = 0;
        rarityMissCount["Epic"] = 0;
        rarityMissCount["Legendary"] = 0;
    }
    
    public List<PerkOption> GenerateWeightedOptions(List<PerkOption> availableOptions, int count = 3)
    {
        if (availableOptions == null || availableOptions.Count == 0)
            return new List<PerkOption>();
        
        var weightedOptions = new List<(PerkOption option, float weight)>();
        
        foreach (var option in availableOptions)
        {
            float weight = CalculateDynamicWeight(option);
            weightedOptions.Add((option, weight));
        }
        
        ApplyDiversityPenalty(weightedOptions);
        return WeightedRandomSelection(weightedOptions, count);
    }
    
    private float CalculateDynamicWeight(PerkOption option)
    {
        float baseWeight = GetBaseWeight(option.Rarity);
        float weight = baseWeight;
        
        weight *= CalculateTagBias(option.Tags);
        weight *= CalculatePityBonus(option.Rarity);
        weight *= CalculateDiversityBonus(option.Tags);
        weight *= CalculateTimeDecay(option);
        
        return Mathf.Max(weight, 0.01f);
    }
    
    private float GetBaseWeight(Rarity rarity)
    {
        string key = rarity.ToString();
        return baseWeights.GetValueOrDefault(key, 10f);
    }
    
    private float CalculateTagBias(List<string> tags)
    {
        if (tags == null || tags.Count == 0)
            return 1f;
        
        float totalBias = 1f;
        
        foreach (var tag in tags)
        {
            int tagCount = tagSelections.GetValueOrDefault(tag, 0);
            float tagBias = 1f + (tagBiasFactor * tagCount);
            totalBias *= tagBias;
        }
        
        return totalBias;
    }
    
    private float CalculatePityBonus(Rarity rarity)
    {
        string rarityKey = rarity.ToString();
        
        if (rarity == Rarity.Common || !rarityMissCount.ContainsKey(rarityKey))
            return 1f;
        
        int missCount = rarityMissCount[rarityKey];
        int pityStacks = missCount / pityInterval;
        
        return 1f + (pityFactor * pityStacks);
    }
    
    private float CalculateDiversityBonus(List<string> tags)
    {
        return 1f;
    }
    
    private float CalculateTimeDecay(PerkOption option)
    {
        return 1f;
    }
    
    private void ApplyDiversityPenalty(List<(PerkOption option, float weight)> weightedOptions)
    {
        var recentTags = GetRecentSelectedTags(5);
        
        foreach (var item in weightedOptions)
        {
            if (item.option.Tags != null)
            {
                int overlapCount = item.option.Tags.Count(tag => recentTags.Contains(tag));
                if (overlapCount > 0)
                {
                    float penalty = 1f - (overlapCount * diversityBonus);
                    int index = weightedOptions.IndexOf(item);
                    weightedOptions[index] = (item.option, item.weight * penalty);
                }
            }
        }
    }
    
    private List<string> GetRecentSelectedTags(int count)
    {
        return tagSelections.OrderByDescending(kvp => kvp.Value)
                           .Take(count)
                           .Select(kvp => kvp.Key)
                           .ToList();
    }
    
    private List<PerkOption> WeightedRandomSelection(List<(PerkOption option, float weight)> items, int count)
    {
        var results = new List<PerkOption>();
        var tempItems = new List<(PerkOption option, float weight)>(items);
        
        for (int i = 0; i < count; i++)
        {
            if (tempItems.Count == 0)
                break;
            
            float totalWeight = tempItems.Sum(x => x.weight);
            float randomValue = UnityEngine.Random.Range(0f, totalWeight);
            
            float currentWeight = 0;
            foreach (var item in tempItems)
            {
                currentWeight += item.weight;
                if (randomValue <= currentWeight)
                {
                    results.Add(item.option);
                    tempItems.Remove(item);
                    break;
                }
            }
        }
        
        return results;
    }
    
    public void RecordSelection(PerkOption selectedOption)
    {
        if (selectedOption == null)
            return;
        
        totalSelections++;
        
        if (selectedOption.Tags != null)
        {
            foreach (var tag in selectedOption.Tags)
            {
                tagSelections[tag] = tagSelections.GetValueOrDefault(tag, 0) + 1;
            }
        }
        
        UpdateRarityMissCount(selectedOption.Rarity);
    }
    
    private void UpdateRarityMissCount(Rarity selectedRarity)
    {
        string selectedKey = selectedRarity.ToString();
        if (rarityMissCount.ContainsKey(selectedKey))
        {
            rarityMissCount[selectedKey] = 0;
        }
        
        foreach (var key in rarityMissCount.Keys.ToList())
        {
            if (key != selectedKey)
            {
                rarityMissCount[key]++;
            }
        }
    }
    
    public DynamicWeightStats GetStats()
    {
        return new DynamicWeightStats
        {
            totalSelections = totalSelections,
            tagSelectionCounts = new Dictionary<string, int>(tagSelections),
            rarityMissCounts = new Dictionary<string, int>(rarityMissCount),
            mostSelectedTag = GetMostSelectedTag(),
            leastSelectedTag = GetLeastSelectedTag()
        };
    }
    
    private string GetMostSelectedTag()
    {
        if (tagSelections.Count == 0)
            return "None";
        return tagSelections.OrderByDescending(kvp => kvp.Value).First().Key;
    }
    
    private string GetLeastSelectedTag()
    {
        if (tagSelections.Count == 0)
            return "None";
        return tagSelections.OrderBy(kvp => kvp.Value).First().Key;
    }
    
    public void Reset()
    {
        tagSelections.Clear();
        rarityMissCount.Clear();
        totalSelections = 0;
        
        foreach (var key in rarityMissCount.Keys.ToList())
        {
            rarityMissCount[key] = 0;
        }
    }
}
