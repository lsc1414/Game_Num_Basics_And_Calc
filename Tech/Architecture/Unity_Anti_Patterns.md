# ☠️ Unity 代码毒药：那些毁灭项目的反模式 (Unity Anti-Patterns)

> **"能跑就行" 是通往重构地狱的特快列车。**
> 
> 本文档记录了那些在 Demo 阶段省事，但在生产阶段会导致项目崩盘的代码习惯。

---

## 1. 单例滥用 (The Singleton Hell)

单例模式是 Unity 开发者最爱用的模式，也是最容易导致架构腐烂的毒药。

### ❌ 典型毒药
```csharp
// 每一个 Manager 都是单例
public class GameManager : MonoBehaviour { public static GameManager Instance; ... }
public class UIManager : MonoBehaviour { public static UIManager Instance; ... }
public class AudioManager : MonoBehaviour { public static AudioManager Instance; ... }
public class PoolManager : MonoBehaviour { public static PoolManager Instance; ... }

// 这种代码随处可见
void Start() {
    // 依赖地狱：初始化顺序是谁决定的？
    // 如果 UIManager Awake 比 GameManager 晚，这里就空指针了。
    GameManager.Instance.Init(); 
    UIManager.Instance.ShowPanel("Main");
}
```
*   **后果：** 
    1.  **竞态条件 (Race Conditions):** `Awake` 和 `Start` 的执行顺序在不同对象间是不确定的（除非手动设置 Script Execution Order，但那是另一个坑）。
    2.  **紧耦合:** 所有系统都如果不引用 `Instance` 就无法工作，导致无法单独测试某个模块。
    3.  **场景切换崩溃:** 忘记处理 `DontDestroyOnLoad` 导致的重复实例，或者引用了已销毁的单例。

### ✅ 解药：依赖注入 (Dependency Injection) 或 服务定位器 (Service Locator)
*   **轻量级解药:** 使用一个总入口（Bootstrapper）。
    ```csharp
    public class GameBootstrapper : MonoBehaviour {
        [SerializeField] private UIManager _uiManager;
        [SerializeField] private AudioManager _audioManager;
        
        void Awake() {
            // 显式控制初始化顺序
            _audioManager.Init(); // 音频先好
            _uiManager.Init(_audioManager); // UI 依赖音频
        }
    }
    ```
*   **工业级解药:** 使用 Zenject / VContainer 等 DI 框架。

---

## 2. 帧率杀手：Update 中的查找 (The "Find" Trap)

### ❌ 典型毒药
```csharp
void Update() {
    // 每秒执行 60 次字符串匹配和全场景遍历
    var target = GameObject.Find("Player"); 
    // 或者
    var text = GetComponent<Text>(); 
    text.text = "Score: " + score; // 还有字符串拼接产生的 GC
}
```
*   **后果：** 手机发烫，掉帧严重。`GameObject.Find` 是非常昂贵的操作。

### ✅ 解药：缓存引用 (Cache References)
```csharp
private GameObject _player;
private Text _text;

void Start() {
    _player = GameObject.Find("Player"); // 只在初始化做一次
    _text = GetComponent<Text>();
}

void Update() {
    // 如果 score 没变，没必要每一帧都设一遍 text
    if (_lastScore != score) {
        _text.text = _scoreStringCache[score]; // 甚至可以用查找表避免 ToString() 的 GC
        _lastScore = score;
    }
}
```

---

## 3. 意大利面条事件 (Spaghetti Event Systems)

### ❌ 典型毒药
*   **C# Action 满天飞:** A 注册了 B，B 注册了 C，C 又注册了 A。
*   **无法追踪:** 按下攻击键，主角没动。你想 Debug，发现这个事件被 50 个地方监听了，不知道是哪个监听器把怪打死了或者拦截了输入。

### ✅ 解药：强类型事件总线 (Strongly Typed Event Bus)
*   不要传递 `object` 或 `string` 参数。
*   使用结构体定义事件 payload。
    ```csharp
    // 定义明确的事件结构
    public struct PlayerDiedEvent {
        public int KillerID;
        public Vector3 DeathLocation;
    }

    // 订阅
    EventBus.Subscribe<PlayerDiedEvent>(OnPlayerDied);
    ```
*   **工具推荐:** 使用 UniRx 或由我们自己维护的轻量级 EventBus，且必须带有 **Logger** 功能，能打印出“谁在什么时候发出了什么事件”。

---

## 4. 协程幽灵 (The Coroutine Ghost)

### ❌ 典型毒药
```csharp
void OnEnable() {
    StartCoroutine(DoSomething());
}

IEnumerator DoSomething() {
    while(true) {
        // ... 无限循环逻辑
        yield return null;
    }
}

// 开发者忘记写停止逻辑
void OnDisable() {
    // 协程还在跑！如果 GameObject 只是被 Disable 而不是 Destroy，
    // 下次 Enable 会再次启动一个新协程。
    // 结果：有两个协程在跑！
}
```

### ✅ 解药：严防死守
```csharp
private Coroutine _myCoroutine;

void OnEnable() {
    if (_myCoroutine != null) StopCoroutine(_myCoroutine);
    _myCoroutine = StartCoroutine(DoSomething());
}

void OnDisable() {
    if (_myCoroutine != null) {
        StopCoroutine(_myCoroutine);
        _myCoroutine = null;
    }
}
```
*   **进阶:** 使用 `UniTask` 代替协程，支持 `.ToCancellationToken(this.GetCancellationTokenOnDestroy())` 自动管理生命周期。

---

## 5. 垃圾制造者：Update 中的 LINQ (LINQ in Hot Paths)

### ❌ 典型毒药
```csharp
void Update() {
    var nearestEnemy = enemies.OrderBy(e => Vector3.Distance(transform.position, e.position)).FirstOrDefault();
}
```
*   **后果：** `OrderBy` 会产生大量的临时对象（委托、闭包、迭代器），导致 Garbage Collector (GC) 频繁触发（Stop-The-World），游戏卡顿。

### ✅ 解药：原生循环
在 `Update` 等热路径（Hot Path）中，老老实实写 `for` 循环。
```csharp
// 虽然代码长了点，但是 0 GC
Enemy nearest = null;
float minDist = float.MaxValue;
for (int i = 0; i < enemies.Count; i++) {
    float d = (enemies[i].position - transform.position).sqrMagnitude; // 用平方距离避免开根号
    if (d < minDist) {
        minDist = d;
        nearest = enemies[i];
    }
}
```

---

## 6. 上帝类 (The God Class)

### ❌ 典型毒药
*   `PlayerController.cs` 有 3000 行代码。
*   它负责移动、攻击、播放动画、扣血、UI更新、甚至播放音效。
*   **后果：** 改一行代码，整个主角崩了。多人协作时，这个文件永远在冲突。

### ✅ 解药：组合优于继承 (Composition over Inheritance)
拆分！
*   `PlayerMovement.cs`
*   `PlayerCombat.cs`
*   `PlayerAnimation.cs`
*   `PlayerStats.cs`
使用一个 `Player` 脚本作为外观（Facade）来协调这些组件，或者使用 ECS / 状态机。

---

## 7. 滥用 Public 变量

### ❌ 典型毒药
```csharp
public int Health; // 为了在 Inspector 里能填数值，设为 public
```
*   **后果：** 任何脚本都能修改 `Health`。当你发现血量莫名其妙变成 0 时，你根本不知道是哪个脚本改的。

### ✅ 解药：SerializeField + 属性
```csharp
[SerializeField] private int _health; // 只有 Inspector 能改，且保留私有性

public int Health {
    get => _health;
    private set => _health = value; // 外部只能读，不能写
}
```

---
