# 🛠️ Unity 游戏开发实战锦囊 (Unity Practical Dev Tips)

**文档目标：** 只有干货。拒绝教科书式的废话，专注解决“为什么我的游戏卡顿”和“为什么我的代码写不下去了”这两个核心问题。
**适用范围：** 适用于中高级开发，特别是 **塔防 (TD)** 和 **肉鸽 (Roguelike)** 这类对性能和架构要求极高的品类。

---

## 1. 🏎️ 性能优化：别让 GC 杀了你的游戏

在塔防/肉鸽游戏中，屏幕上可能有 500 个敌人和 2000 发子弹。如果处理不好，帧率会跌到个位数。

### 1.1 ♻️ 对象池 (Object Pooling) —— 必修课
*   **原理：** `Instantiate` (生成) 和 `Destroy` (销毁) 是极其昂贵的操作，还会产生垃圾内存 (Garbage)，导致 GC (垃圾回收) 触发时游戏卡顿。
*   **做法：**
    *   **借出：** 想要子弹？从池子里拿一个隐藏的，重置位置和状态，设为 `SetActive(true)`。
    *   **归还：** 子弹撞墙了？别 `Destroy`。把它移出屏幕，`SetActive(false)`，放回池子。
*   **进阶技巧：** 使用 `release` 接口而非 `return`。对于复杂的池对象（如怪物），在 `OnDisable` 里重置状态，防止下次拿出来时带着上一局的 Debuff。

### 1.2 🧵 字符串的陷阱 (The String Trap)
*   **大忌：** 在 `Update()` 里写字符串拼接。
    *   `uiText.text = "Score: " + score;` // 每帧都会产生一个新的 String 对象，GC 爆炸。
*   **对策：**
    *   **缓存：** 如果分数没变，别更新 UI。
    *   **StringBuilder：** 对于复杂拼接，使用 `StringBuilder`。
    *   **ZString / C# Span:** (高级) 使用零内存分配的字符串库。

### 1.3 🧱 物理系统的 90% 性能都在这
*   **碰撞矩阵 (Collision Matrix):**
    *   打开 `Project Settings -> Physics 2D`。
    *   **取消勾选**所有不需要碰撞的组合！
    *   *例子：* “子弹”不需要撞“子弹”。“敌人”不需要撞“经验球”。这能节省大量的物理计算。
*   **别用 MeshCollider:** 除非是静态的地形。移动物体请用 `BoxCollider` 或 `SphereCollider` (或 2D 对应版)。
*   **Rigidbody 的休眠:** 确保不动的物体能进入 Sleep 状态。

### 1.4 🖼️ 批量渲染 (Batching / DrawCalls)
*   **问题：** 100 个怪，如果用了 100 个不同的材质球，就是 100 个 DrawCall。CPU 会累死。
*   **对策 (Sprite Atlas):**
    *   把所有怪物的图片打包成一张大图 (Sprite Atlas)。
    *   这样渲染 100 个怪，可能只需要 1 个 DrawCall。
*   **文本 (TMP):** TextMeshPro 也是一样的道理，尽量共用字体贴图。

---

## 2. 🏗️ 架构设计：如何写出不耦合的代码

塔防游戏最怕代码变成“意大利面条”：塔的代码引用了怪物，怪物引用了血条，血条引用了音效管理器... 删一个文件报错一百个。

### 2.1 📢 事件总线 (Event Bus) / 观察者模式
*   **场景：** 怪物死了，需要：1.加分 2.播音效 3.掉落金币 4.任务计数。
*   **错误写法：** 在 `Monster.cs` 里调用 `ScoreManager.Add()`, `AudioManager.Play()`, `LootManager.Spawn()`...
*   **正确写法 (解耦):**
    *   `Monster.cs`: `public static event Action<Monster> OnMonsterDied;`
    *   怪物死的时候：`OnMonsterDied?.Invoke(this);` 我只管喊一声“我死啦！”，谁爱管谁管。
    *   `ScoreManager.cs`: 监听 `OnMonsterDied`，听到就加分。
    *   **好处：** 你删掉音效管理器，怪物代码一行都不用改。

### 2.2 📄 ScriptableObject (SO) —— 策划的好朋友
*   **核心理念：** **数据与逻辑分离**。
*   **应用：** 别在代码里写 `public float atk = 10;`。
*   **做法：**
    1.  创建一个 `EnemyData : ScriptableObject`，里面存 HP, Atk, Speed, Prefab。
    2.  在 Project 窗口右键创建 `Goblin_Lv1.asset`, `Dragon_Lv99.asset`。
    3.  怪物逻辑 `Monster.cs` 里只有一个变量：`public EnemyData data;`。
*   **好处：**
    *   策划可以直接在编辑器里调数值，不用改代码，不用重新编译。
    *   内存里只有一份数据，1000 个哥布林共用一个 SO，省内存。

### 2.3 🧩 组合优于继承 (Composition over Inheritance)
*   **问题：** `class FireDragon : Dragon`。如果我想做一个“冰龙”，又要继承。如果我想做一个“会喷火的骷髅”怎么办？多重继承？
*   **对策 (组件化):**
    *   不再写“火龙”类。
    *   写功能组件：`Health` (血量), `Mover` (移动), `Shooter` (发射), `ElementType` (元素类型)。
    *   **火龙** = Health + Mover + Shooter(Fireball) + Element(Fire)。
    *   **喷火骷髅** = Health + Mover + Shooter(Fireball) + Element(Undead)。
    *   Unity 的 `GameObject` + `Component` 本身就是这个设计哲学，请贯彻它。

---

## 3. 🛠️ 开发效率：别重复造轮子

### 3.1 ⏳ 异步编程：UniTask
*   **现状：** Unity 原生 `Coroutine` (协程) 容易产生垃圾内存，且无法返回值。C# 原生 `Task` 在 WebGL 上支持不好且有线程问题。
*   **推荐：** 使用 **UniTask** (开源库)。
    *   `await UniTask.Delay(1000);`
    *   比协程更快，0 GC，像写同步代码一样写异步逻辑。

### 3.2 🎨 动画插件：DoTween
*   **场景：** 想要一个 UI 弹窗“弹”出来的效果。
*   **别自己写：** `Update` 里写 `transform.scale += Time.deltaTime...` 太累了。
*   **用 DoTween：** `transform.DOScale(1.2f, 0.5f).SetEase(Ease.OutBack);` 一行代码搞定，丝般顺滑。

### 3.3 🕵️ 编辑器扩展 (Odin Inspector)
*   **痛点：** Unity 原生的 Inspector 很难看，List 没法搜索，字典没法显示。
*   **推荐：** **Odin Inspector** (收费但值得/也有免费替代品)。
*   **低配版 (原生):**
    *   `[Header("基础属性")]`: 给变量分组。
    *   `[Tooltip("攻击力")]`: 鼠标悬停提示。
    *   `[Range(0, 100)]`: 变成滑动条。
    *   `[ContextMenu("测试击杀")]`: 在组件右键菜单里添加一个按钮来执行函数，方便测试。

---

## 4. 🐛 调试与防坑

### 4.1 🛑 空引用 (NullReferenceException)
*   **原则：** 永远不要信任 `GetComponent` 和 `Find`。
*   **防御式编程：**
    *   `RequireComponent(typeof(Rigidbody))`：强制挂载依赖组件。
    *   `TryGetComponent(out Rigidbody rb)`：比 `GetComponent` 安全且快。

### 4.2 📌 还能这么 Debug?
*   **Debug.Break():** 代码里调用这个，游戏会自动暂停。适合捕捉“一闪而过”的 Bug。
*   **Debug.DrawLine / Gizmos:**
    *   别光看 Log。在 `OnDrawGizmos` 里把攻击范围、索敌半径画出来。
    *   可视化调试比看 Console 快 10 倍。

### 4.3 ⏱️ Time.timeScale
*   **做暂停功能时：** 设为 0。
*   **做倍速功能时：** 设为 2.0。
*   **坑：** `Update` 里的逻辑受影响，但 `FixedUpdate` (物理) 也受影响。如果你有一些 UI 动画不想受暂停影响，请用 `UnscaledTime`。

---

## 5. 📂 项目结构规范 (Project Structure)

混乱的文件夹是烂尾的第一步。

```text
Assets/
├── _Project/           # 只有这里放你自己的资源，把插件和下载的资源隔离开
│   ├── Scripts/
│   │   ├── Core/       # 核心系统 (GameManager, EventBus)
│   │   ├── Gameplay/   # 玩法逻辑 (Tower, Enemy)
│   │   ├── UI/
│   │   └── Utils/
│   ├── Prefabs/
│   ├── ScriptableObjects/
│   ├── Materials/
│   └── Scenes/
├── Plugins/            # 第三方插件 (DoTween, UniTask)
└── Resources/          # ⚠️ 尽量别用！会拖慢启动速度。用 Addressables 或直接引用。
```
