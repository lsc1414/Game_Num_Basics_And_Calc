---
sidebarTitle: "Unity 轻量级音频框架"
---

# 🛠️ Unity 轻量级音频框架

> **概述**: 这是一个专为中小型项目（特别是 Roguelike/塔防）设计的纯代码音频管理方案。它不依赖任何第三方插件，通过**对象池**和**配置化**解决性能与听感问题。

## 1. 核心架构设计

### 1.1 功能清单
*   **对象池 (Object Pooling)**: 预先生成 32-64 个 `AudioSource`，循环使用，零 GC Alloc。
*   **自动变奏 (Auto-Variation)**: 播放时自动随机微调 Pitch 和 Volume。
*   **冷却限制 (Cooldown/Throttling)**: 针对每个音效 ID 设置最小触发间隔，杜绝“爆音”。
*   **空间化自动切换**: 支持 2D (UI) 和 3D (世界坐标) 播放模式。

## 2. 核心代码实现 (`SimpleAudioManager.cs`)

您可以直接将此脚本挂载在场景中唯一的 `AudioManager` GameObject 上。

```csharp
using UnityEngine;
using System.Collections.Generic;
using UnityEngine.Audio;

public class SimpleAudioManager : MonoBehaviour
{
    public static SimpleAudioManager Instance { get; private set; }

    [Header("Settings")]
    [Tooltip("同时存在的最大声音数量")]
    public int poolSize = 32;
    public AudioMixerGroup sfxMixerGroup;
    public AudioMixerGroup musicMixerGroup;

    [Header("Music")]
    public AudioSource musicSource;

    // 简单的音效配置类 (实际项目中建议用 ScriptableObject 管理)
    [System.Serializable]
    public class SoundProfile
    {
        public string id;           // 音效ID (如 "Attack_Sword")
        public AudioClip clip;
        [Range(0f, 1f)] public float volume = 1f;
        [Range(0.1f, 3f)] public float pitch = 1f;
        [Range(0f, 0.5f)] public float randomPitch = 0.1f; // 音调随机范围 +/-
        public float cooldown = 0.1f; // 最小播放间隔 (秒)
        public bool is3D = false;     // 是否为 3D 音效
    }

    [Header("Library")]
    public List<SoundProfile> soundLibrary; // 在 Inspector 里配置所有音效

    // 运行时数据
    private Dictionary<string, SoundProfile> _libraryLookup;
    private Dictionary<string, float> _lastPlayedTimes;
    private List<AudioSource> _sourcePool;
    private int _poolIndex = 0;

    void Awake()
    {
        // 单例初始化
        if (Instance == null) { Instance = this; DontDestroyOnLoad(gameObject); }
        else { Destroy(gameObject); return; }

        InitializeLibrary();
        InitializePool();
    }

    private void InitializeLibrary()
    {
        _libraryLookup = new Dictionary<string, SoundProfile>();
        _lastPlayedTimes = new Dictionary<string, float>();

        foreach (var s in soundLibrary)
        {
            if (!_libraryLookup.ContainsKey(s.id))
            {
                _libraryLookup.Add(s.id, s);
                _lastPlayedTimes.Add(s.id, 0f);
            }
        }
    }

    private void InitializePool()
    {
        _sourcePool = new List<AudioSource>();
        GameObject poolRoot = new GameObject("SFX_Pool");
        poolRoot.transform.SetParent(transform);

        for (int i = 0; i < poolSize; i++)
        {
            GameObject obj = new GameObject($"SFX_Source_{i}");
            obj.transform.SetParent(poolRoot.transform);
            AudioSource src = obj.AddComponent<AudioSource>();
            src.playOnAwake = false;
            src.outputAudioMixerGroup = sfxMixerGroup;
            _sourcePool.Add(src);
        }
    }

    /// <summary>
    /// 播放音效的核心方法
    /// </summary>
    /// <param name="id">音效配置ID</param>
    /// <param name="position">世界坐标 (如果是 null 则为 2D 声音)</param>
    public void PlaySFX(string id, Vector3? position = null)
    {
        if (!_libraryLookup.TryGetValue(id, out SoundProfile profile))
        {
            Debug.LogWarning($"Audio: Sound ID '{id}' not found!");
            return;
        }

        // 1. 冷却检测 (Throttling)
        if (Time.time < _lastPlayedTimes[id] + profile.cooldown) return;
        _lastPlayedTimes[id] = Time.time;

        // 2. 获取对象池中的 Source
        AudioSource source = GetNextSource();

        // 3. 应用配置
        source.clip = profile.clip;
        
        // 随机化处理
        float finalPitch = profile.pitch + Random.Range(-profile.randomPitch, profile.randomPitch);
        // 防止 Pitch 变成负数或 0
        source.pitch = Mathf.Max(0.1f, finalPitch); 
        source.volume = profile.volume;

        // 4. 空间化处理
        if (position.HasValue && profile.is3D)
        {
            source.spatialBlend = 1f; // 3D
            source.transform.position = position.Value;
            // 简单的衰减设置
            source.minDistance = 1f;
            source.maxDistance = 20f;
        }
        else
        {
            source.spatialBlend = 0f; // 2D
        }

        // 5. 播放
        source.Play();
    }

    private AudioSource GetNextSource()
    {
        // 简单的循环覆盖策略 (Round Robin)
        // 如果池子满了，会强行切断最久远的那个声音
        AudioSource src = _sourcePool[_poolIndex];
        _poolIndex = (_poolIndex + 1) % poolSize;
        return src;
    }

    // 背景音乐淡入淡出 (简单版)
    public void PlayMusic(AudioClip clip, float fadeDuration = 1f)
    {
        if (musicSource.clip == clip) return;
        // 此处省略 Coroutine 淡入淡出逻辑，实际项目中建议加上 Tween
        musicSource.clip = clip;
        musicSource.Play();
    }
}
```

## 3. 使用指南 (Usage)

### 3.1 基础调用
在任何代码中，不再需要 `GetComponent<AudioSource>`，直接调用单例：

```csharp
// 播放 UI 点击声 (2D)
SimpleAudioManager.Instance.PlaySFX("UI_Click");

// 播放怪物受击声 (3D，在怪物位置)
SimpleAudioManager.Instance.PlaySFX("Hit_Flesh", transform.position);
```

### 3.2 进阶技巧：ScriptableObject 数据分离
上面的代码把数据存在了 Manager 里。对于大型项目，建议把 `SoundProfile` 抽离成 `ScriptableObject`。

```csharp
[CreateAssetMenu(menuName = "Audio/SoundData")]
public class SoundData : ScriptableObject {
    public string id;
    public AudioClip[] clips; // 支持多个素材随机
    // ... 其他参数
}
```
然后 `AudioManager` 只需持有一个 `List<SoundData>`。

### 3.3 关于 Audio Mixer
建议在项目中创建 `MainMixer`：

*   **Master**
    *   **Music** (BGM)
    *   **SFX** (音效)
        *   **UI**
        *   **Combat**
        
将 `SimpleAudioManager` 的 `sfxMixerGroup` 变量绑定到 `SFX` 组。这样你可以一键实现“静音音效但保留音乐”。

## 4. 常见问题
*   **为什么不用 PlayOneShot?**
    *   `AudioSource.PlayOneShot` 无法打断。如果你用对象池模式 (`source.Play()`)，当池子转了一圈回到第一个 Source 时，我们可以强制停止旧声音播放新声音，这在子弹极其密集时能有效控制 CPU 负载（旧的没听完就没必要听了）。
*   **3D 声音听不见?**
    *   检查 `spatialBlend` 是否为 1。
    *   检查 `AudioListener` 是否在摄像机上。
