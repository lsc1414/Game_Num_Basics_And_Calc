using System;
using System.Collections.Generic;
using UnityEngine;

/// <summary>
/// PRD（伪随机分布）算法实现
/// 用于确保事件触发更加均匀，避免极端情况
/// </summary>
public class PRDAlgorithm
{
    private Dictionary<string, int> failureCounters;
    private Dictionary<string, float> cValues;
    
    public PRDAlgorithm()
    {
        failureCounters = new Dictionary<string, int>();
        cValues = new Dictionary<string, float>();
        
        // 初始化常用C值
        InitializeCValues();
    }
    
    private void InitializeCValues()
    {
        cValues["5%"] = 0.00380f;
        cValues["10%"] = 0.01475f;
        cValues["15%"] = 0.03222f;
        cValues["20%"] = 0.05570f;
        cValues["25%"] = 0.08474f;
        cValues["30%"] = 0.11948f;
        cValues["35%"] = 0.15997f;
        cValues["40%"] = 0.20615f;
        cValues["45%"] = 0.25865f;
        cValues["50%"] = 0.30210f;
    }
    
    /// <summary>
    /// 计算给定概率的C值
    /// </summary>
    public static float CalculateCValue(float probability)
    {
        // 使用牛顿迭代法求解C值
        double c = probability; // 初始猜测
        double p = probability;
        
        for (int i = 0; i < 20; i++) // 迭代20次确保收敛
        {
            double oldC = c;
            
            // 计算函数值和导数
            double f = 1 - Math.Pow(1 - c, 1 / c) - p;
            double df = Math.Pow(1 - c, 1 / c) * (Math.Log(1 - c) / (c * c) + 1 / (c * (1 - c)));
            
            // 牛顿迭代更新
            c = c - f / df;
            
            // 检查收敛
            if (Math.Abs(c - oldC) < 1e-10)
                break;
        }
        
        return (float)c;
    }
    
    /// <summary>
    /// 尝试触发PRD事件
    /// </summary>
    public bool TryTrigger(string eventId, float probability)
    {
        string key = $"{eventId}_{probability}";
        
        if (!failureCounters.ContainsKey(key))
        {
            failureCounters[key] = 0;
        }
        
        // 获取C值（使用缓存或计算）
        string probKey = $"{probability * 100}%";
        float c = cValues.ContainsKey(probKey) ? cValues[probKey] : CalculateCValue(probability);
        
        // 计算当前触发概率
        int failures = failureCounters[key];
        float currentProbability = c * (failures + 1);
        
        // 尝试触发
        bool triggered = UnityEngine.Random.Range(0f, 1f) <= currentProbability;
        
        if (triggered)
        {
            failureCounters[key] = 0; // 重置失败计数
        }
        else
        {
            failureCounters[key] = failures + 1; // 增加失败计数
        }
        
        return triggered;
    }
    
    /// <summary>
    /// 获取当前失败次数
    /// </summary>
    public int GetFailureCount(string eventId, float probability)
    {
        string key = $"{eventId}_{probability}";
        return failureCounters.GetValueOrDefault(key, 0);
    }
    
    /// <summary>
    /// 重置特定事件的计数器
    /// </summary>
    public void ResetCounter(string eventId, float probability)
    {
        string key = $"{eventId}_{probability}";
        failureCounters[key] = 0;
    }
    
    /// <summary>
    /// 重置所有计数器
    /// </summary>
    public void ResetAllCounters()
    {
        failureCounters.Clear();
    }
}

/// <summary>
/// PRD事件参数
/// </summary>
[System.Serializable]
public struct PRDEvent
{
    public string eventId;
    public float baseProbability;
    public string description;
    
    public PRDEvent(string id, float probability, string desc)
    {
        eventId = id;
        baseProbability = probability;
        description = desc;
    }
}

/// <summary>
/// PRD触发结果
/// </summary>
public struct PRDResult
{
    public bool triggered;
    public int failureCount;
    public float actualProbability;
    
    public PRDResult(bool trig, int failures, float actualProb)
    {
        triggered = trig;
        failureCount = failures;
        actualProbability = actualProb;
    }
}
