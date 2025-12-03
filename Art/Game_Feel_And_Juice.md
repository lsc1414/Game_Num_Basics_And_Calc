# 游戏手感与 "Juice" (Game Feel & Juice)

> [!TIP]
> **定义**: "Juice" 是指那些不改变游戏核心机制，但能极大提升玩家交互反馈和满足感的视听元素。
> *It's the difference between a spreadsheet and a game.*

对于 **Vampirefall** (Roguelike + Looter) 这种高频战斗游戏，优秀的手感是留存的关键。

---

## 1. 核心支柱 (The Core Pillars)

### 1.1 屏幕震动 (Screen Shake)
最直接的力量传达方式。
*   **关键点**: 不要只是随机移动摄像机位置 (Position)，要结合旋转 (Rotation) 和视场角 (FOV) 的微小变化。
*   **算法**: 使用 **Perlin Noise** 替代 `Random.insideUnitCircle`，以获得更平滑、更有“重量感”的震动。

### 1.2 顿帧 (Hit Stop / Freeze Frames)
当强力攻击命中时，让时间暂停几毫秒。
*   **原理**: 模仿动作电影中的慢镜头或漫画中的打击定格，强调“冲击力”。
*   **数值**: 
    *   轻攻击: 0ms (无顿帧)
    *   中攻击: 0.05s - 0.1s
    *   暴击/终结技: 0.15s - 0.3s

### 1.3 视觉闪烁 (Flash & Blink)
*   **敌人受击**: 材质瞬间变白 (Shader Emission)。
*   **屏幕闪光**: 暴击时屏幕边缘瞬间泛红或泛白。

### 1.4 动态色差 (Chromatic Aberration)
在受击或爆炸瞬间，短暂拉高后处理中的色差值，模拟摄像机镜头的“损坏”或“过载”感。

---

## 2. 架构设计：Trauma 系统 (The Trauma System)

为了避免震动过于混乱或被截断，推荐使用 GDC 演讲中提到的 **Trauma (创伤)** 系统。

### 2.1 概念
*   **Trauma (0-1)**: 一个表示当前“混乱程度”的浮点数。
*   **Decay (衰减)**: Trauma 每帧线性减少 (例如每秒 -1.0)。
*   **Shake (输出)**: 震动强度是 Trauma 的**平方**或**立方** ($Shake = Trauma^2$)。
    *   这使得高 Trauma 时震动剧烈，而低 Trauma 时震动非常微弱且细腻。

### 2.2 代码实现 (Unity)

```csharp
public class GameFeelManager : MonoBehaviour {
    public static GameFeelManager Instance;
    
    [Header("Settings")]
    public float maxAngle = 10f; // 最大旋转角度
    public float maxOffset = 0.5f; // 最大位移距离
    public float traumaDecay = 1.0f; // 每秒衰减速度

    private float _trauma;
    private float _seed; // Perlin Noise 种子

    public void AddTrauma(float amount) {
        _trauma = Mathf.Clamp01(_trauma + amount);
    }

    void Update() {
        if (_trauma > 0) {
            // 衰减
            _trauma -= Time.deltaTime * traumaDecay;
            _trauma = Mathf.Clamp01(_trauma);

            // 计算震动强度 (平方曲线)
            float shake = _trauma * _trauma;

            // 使用 Perlin Noise 计算偏移
            _seed += Time.deltaTime * 10f; // 震动频率
            float x = (Mathf.PerlinNoise(_seed, 0) - 0.5f) * 2f * maxOffset * shake;
            float y = (Mathf.PerlinNoise(0, _seed) - 0.5f) * 2f * maxOffset * shake;
            float rot = (Mathf.PerlinNoise(_seed, _seed) - 0.5f) * 2f * maxAngle * shake;

            // 应用到摄像机 (假设是局部坐标)
            Camera.main.transform.localPosition = new Vector3(x, y, -10);
            Camera.main.transform.localRotation = Quaternion.Euler(0, 0, rot);
        } else {
            // 复位逻辑...
        }
    }
}
```

---

## 3. 动画原则的应用 (Animation Principles)

### 3.1 挤压与拉伸 (Squash & Stretch)
*   **应用**: 子弹发射时拉长，击中时压扁。掉落物落地时有弹性的形变。
*   **实现**: 通过代码动态修改 `transform.localScale`。

### 3.2 预备动作 (Anticipation)
*   **应用**: 怪物攻击前的闪光、后撤或蓄力特效。
*   **目的**: 给玩家反应时间 (Telegraphing)，让攻击看起来更公平且有力。

---

## 4. 音频反馈 (Audio Feedback)

声音占据了手感的 50%。

### 4.1 音高随机化 (Pitch Variation)
永远不要让同一个音效听起来完全一样。
*   每次播放时，随机改变 Pitch (例如 0.9 ~ 1.1)。
*   这能有效防止听觉疲劳 (Machine Gun Effect)。

### 4.2 分层设计 (Layering)
一个好的打击音效通常由三层组成：
1.  **Impact (低频)**: 拳头打在肉上的闷响 (Thud)。
2.  **Body (中频)**: 材质的声音 (金属撞击、骨折声)。
3.  **Top (高频)**: 细节 (风声、刀剑划破空气的尖啸)。

---

## 5. 辅助功能与输入 (Accessibility & Input)

### 5.1 土狼时间 (Coyote Time)
允许玩家在离开平台后的几帧内仍然能起跳。虽然 Vampirefall 可能是俯视角，但在冲刺/闪避判定中同样适用。

### 5.2 输入缓冲 (Input Buffering)
如果玩家在攻击动画结束前按下了“再次攻击”，系统应该记录并在动画结束后立即执行，而不是忽略。这能让连招极其流畅。

---

## 6. 经典案例 (Case Studies)

### Vlambeer (Nuclear Throne)
*   **名言**: "Screen shake is the MSG of game design." (屏幕震动是游戏设计的味精)。
*   **技巧**: 即使是开枪射击空地，也会有巨大的后坐力反馈、弹壳飞出、烟雾残留。

### Hollow Knight (空洞骑士)
*   **下劈 (Pogo)**: 当玩家向下攻击钉刺或敌人时，角色会获得一个向上的反作用力，同时伴随顿帧和特效。这不仅是攻击，更是位移手段。

### Celeste (蔚蓝)
*   **屏幕震动**: 极其克制但精准。
*   **辅助功能**: 允许玩家关闭震动（这一点很重要，部分玩家会晕3D）。
