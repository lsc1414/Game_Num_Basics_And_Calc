# 🎵 游戏音效设计：从音阶算法到听觉心理学 (Audio System Design & Tricks)

> **核心理念**: 好的音效不是“听到什么”，而是让大脑“确认什么”。
> 音效在游戏中承担了三个角色：**反馈 (Feedback)**、**情绪 (Mood)** 和 **空间 (Space)**。

## 1. 🎹 核心技巧：音阶变化 (Dynamic Pitch Shifting)

您提到的“吃经验 Do-Re-Mi”效果，学名叫做 **动态音高调整**。它是解决重复音效枯燥感的神器，同时能提供强烈的连续正反馈。

### 1.1 为什么要变调？
*   **听觉疲劳**: 连续听 100 次完全一样的“叮”声，玩家会烦躁甚至关掉声音。
*   **奖励升级感**: 音调越来越高，代表奖励越来越好，或者连击数越来越高。多巴胺分泌随音高上升。

### 1.2 算法实现 (Unity C#)
在 Unity 中，我们通过修改 `AudioSource.pitch` 来实现。

**基础乐理公式**:
十二平均律中，半音的频率比是 $2^{(1/12)} \approx 1.05946$。
想要提高 `n` 个半音，公式为：
`targetPitch = originalPitch * Mathf.Pow(1.05946f, n);`

**代码实现逻辑 (ComboSystem)**:
```csharp
public class AudioPitchShifter : MonoBehaviour {
    private AudioSource _source;
    private int _comboIndex = 0;
    private float _resetTimer = 0f;
    
    // 12个半音的音阶 (大调音阶示例: Do Re Mi Fa Sol La Si Do)
    // 0=C, 2=D, 4=E, 5=F, 7=G, 9=A, 11=B, 12=High C
    private int[] _majorScale = { 0, 2, 4, 5, 7, 9, 11, 12 }; 

    public void PlayComboSound() {
        // 1. 计算当前音高
        int noteIndex = Mathf.Clamp(_comboIndex, 0, _majorScale.Length - 1);
        int semitones = _majorScale[noteIndex];
        
        // 2. 应用公式
        _source.pitch = Mathf.Pow(1.05946f, semitones);
        
        // 3. 播放
        _source.PlayOneShot(_clip);
        
        // 4. 增加连击，重置计时器
        _comboIndex++;
        _resetTimer = 1.0f; // 1秒不吃东西，音阶重置
    }

    void Update() {
        if (_resetTimer > 0) {
            _resetTimer -= Time.deltaTime;
            if (_resetTimer <= 0) {
                _comboIndex = 0; // 超时重置
            }
        }
    }
}
```

## 2. 🛠️ 业界常用音效“特效” (Standard Audio FX)

除了变调，以下几种效果是现代游戏标配：

### 2.1 随机化 (Randomization) - "防机关枪效应"
当攻速达到 5.0 时，如果没有随机化，听起来像机关枪卡壳。
*   **做法**: 每次播放时，给音高和音量加微小的随机扰动。
    *   `source.pitch = 1.0f + Random.Range(-0.1f, 0.1f);`
    *   `source.volume = 1.0f + Random.Range(-0.05f, 0.05f);`

### 2.2 闪避/侧链 (Ducking / Sidechaining) - "让路"
当**重要音效**（如：升级、BOSS出场、大招）播放时，自动压低**次要音效**（背景音乐、环境音、普通攻击）的音量。
*   **实现**: 使用 Unity 的 Audio Mixer。
    *   在 "SFX_Import" 组加一个 `Send` 效果。
    *   在 "BGM" 组加一个 `Duck Volume` 效果。
    *   当 SFX_Import 有声音时，BGM 自动降低 -10dB。

### 2.3 低通滤波 (Low Pass Filter / LPF) - "濒死/菜单"
当玩家血量低于 20%，或者打开暂停菜单时，声音变得“闷闷的”，好像在水下。
*   **原理**: 切掉高频声音，只保留低频。
*   **作用**: 制造紧张感，或者区分 UI 层级（菜单时让战斗音效退居幕后）。

### 2.4 空间限制 (Voice Limiting) - "防爆音"
在 Vampirefall 这种塔防+割草游戏，可能同时有 500 只怪在被打。如果同时播放 500 个受击音效，扬声器会爆，玩家耳朵会聋。
*   **规则**:
    *   同一种音效（如 `Hit_Flesh.wav`），同一帧最多播放 3 次。
    *   设置全剧最大发声数 (Max Voices)，通常移动端限制 32-64 个。
    *   **优先级**: 玩家的攻击声 > 塔的攻击声 > 怪物的叫声。

## 3. 🎧 Vampirefall 音效清单建议

| 类别 | 音效名 | 特性 | 备注 |
| :--- | :--- | :--- | :--- |
| **Feedback** | `Hit_Normal` | **随机化 Pitch** | 高频触发，必须随机化防止刺耳。 |
| **Reward** | `Exp_Pickup` | **动态音阶 (Do-Re-Mi)** | 连续吸入经验球时，音调递增。 |
| **Ui** | `Level_Up` | **Ducking (压低BGM)** | 升级是荣耀时刻，必须清晰。 |
| **Combat** | `Critical_Hit` | **高频提升** | 暴击音效通常含有更多高频（金属音），穿透力强。 |

## 4. 💡 心理学小贴士
*   **打击感**: 视觉上的顿帧 + 听觉上的低音冲击 (Kick/Bass) = 拳拳到肉。
*   **危险预警**: 高频、尖锐的声音（如指甲划黑板）本能地让人不适/警觉，适合用于 BOSS 大招蓄力。
