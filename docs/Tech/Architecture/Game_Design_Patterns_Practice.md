# 🏗️ 游戏设计模式：理论与 Unity 实战

设计模式 (Design Patterns) 是解决常见架构问题的通用方案。但在游戏开发中，性能敏感性和迭代速度要求我们对经典模式进行“魔改”。

本文档总结了在 **Project Vampirefall** 及业界 3A/独立游戏中最高频使用的模式。

---

## 1. 核心模式 (The Essentials)

### 1.1 单例模式 (Singleton) & 服务定位器 (Service Locator)
*   **理论:** 保证一个类只有一个实例，并提供全局访问点。
*   **Unity 痛点:** 传统的 `Instance` 静态变量会导致紧耦合，且难以测试。
*   **最佳实践:** **服务定位器 (Service Locator)** 或 **依赖注入 (DI)**。
    *   不要直接调用 `AudioManager.Instance.Play()`。
    *   而是让系统在启动时注册: `ServiceLocator.Register<IAudioService>(new AudioManager())`。
    *   业务逻辑只依赖接口: `ServiceLocator.Get<IAudioService>().Play()`。
*   **Vampirefall 应用:** `GameManager`, `SaveSystem`, `LootManager`。

### 1.2 对象池模式 (Object Pool)
*   **理论:** 预先实例化一组对象，用完回收而非销毁，避免 GC (垃圾回收) 造成的卡顿。
*   **Unity 实战:**
    *   使用 Unity 2021+ 内置的 `UnityEngine.Pool` API。
    *   **脏数据清理 (Dirty State):** 核心难点在于 `OnGet` 和 `OnRelease`。取出对象时，必须重置其状态（血量、Buff、位置），否则会出现“刚出生的怪带着半血”的 Bug。
*   **Vampirefall 应用:** 子弹、伤害数字、怪物模型。

### 1.3 状态机模式 (State Machine / FSM)
*   **理论:** 对象处于有限的几种状态之一 (Idle, Walk, Attack)，且根据条件在状态间切换。
*   **实战:**
    *   **分层状态机 (HFSM):** 状态套状态。`Alive` 状态下包含 `Move`, `Skill`；`Dead` 状态下包含 `Ragdoll`, `Dissolve`。
    *   **代码即数据:** 不要用巨大的 `switch-case`。每个状态应该是一个独立的类 (`IState`)。
*   **Vampirefall 应用:** 怪物 AI、UI 窗口流转、防御塔行为。

---

## 2. 进阶架构模式 (Advanced Architecture)

### 2.1 观察者模式 (Observer / Event Bus)
*   **理论:** 定义一对多的依赖关系，当一个对象改变状态时，所有依赖者都会收到通知。
*   **实战:** **事件总线 (Event Bus)**。
    *   `GlobalEvents.OnEnemyKilled?.Invoke(enemyInfo)`。
    *   成就系统订阅它：“杀敌数+1”。
    *   任务系统订阅它：“任务进度更新”。
    *   UI 系统订阅它：“飘字显示”。
*   **优点:** 彻底解耦。杀怪逻辑不需要知道成就系统的存在。

### 2.2 命令模式 (Command)
*   **理论:** 将“请求”封装成对象。
*   **实战:** RTS 和 回合制游戏的核心。
    *   不要直接 `unit.MoveTo(pos)`。
    *   而是创建 `new MoveCommand(unit, pos)` 并压入队列。
*   **Vampirefall 应用:** 
    *   **输入缓冲 (Input Buffer):** 在攻击动作未结束时按下闪避，指令被存入 Command Queue，动作结束后立即执行。
    *   **录像回放:** 记录一局内所有的 Command，即可完美重播整局游戏。

### 2.3 装饰器模式 (Decorator) - *Deep Dive*
*   **核心价值:** 动态地、透明地、无限叠加地改变对象的行为，而无需修改原始类。

#### A. 为什么“继承”是死胡同？
假设你需要实现：A(火焰)、B(冰冻)、C(吸血)。
如果用继承：`FireAttack`, `IceAttack`, `FireAndIceAttack`...
**组合爆炸 (Combinatorial Explosion):** 10 种效果需要 $2^{10} = 1024$ 个类。

#### B. 像俄罗斯套娃一样 (The "Russian Doll" Model)
装饰器模式创建的是“包装纸”。

1.  **Component (接口)**: `IAttack`
2.  **Concrete (本体)**: `SwordAttack` (最里面的娃娃)
3.  **Decorator (包装)**: `FireDecorator` (包在外面)

**调用链:** `Game -> LifeSteal -> Fire -> Sword`

*   外层只管调 `Execute()`，不知道里面包了多少层。

#### C. Vampirefall 实战代码 (C#)
```csharp
// 1. 接口
public interface IAttack {
    void Execute(Enemy target, DamageInfo info);
}

// 2. 本体
public class SwordAttack : IAttack {
    public void Execute(Enemy target, DamageInfo info) {
        target.TakeDamage(info.BaseDamage); // 核心逻辑
    }
}

// 3. 装饰器基类
public abstract class AttackDecorator : IAttack {
    protected IAttack _inner;
    public AttackDecorator(IAttack inner) { _inner = inner; }
    public virtual void Execute(Enemy target, DamageInfo info) {
        _inner.Execute(target, info); // 转发
    }
}

// 4. 具体装饰器：拦截与修改
public class CritDecorator : AttackDecorator {
    public CritDecorator(IAttack inner) : base(inner) {}
    public override void Execute(Enemy target, DamageInfo info) {
        // 拦截输入：在攻击发生前修改参数
        if (Random.value < 0.2f) info.BaseDamage *= 2.0f; 
        base.Execute(target, info);
    }
}
```

#### D. 装饰器 vs 事件 (Event)
*   **事件 (Event):** 通常发生在动作**之后** (`OnHit`)。适合做 UI 显示、成就统计。
*   **装饰器:** 可以介入动作**之前**，修改参数甚至阻止执行。适合做暴击计算、格挡判定。

#### E. 工业级痛点与进化：管道模式 (Pipeline)
标准的 GoF 装饰器在面对复杂 RPG 系统时有三大缺陷：

1.  **移除困难:** 想要移除中间的一层包装（如 Buff 过期），需要解构整个链条。
2.  **顺序混乱:** 先加后乘 `(10+5)*1.5` vs 先乘后加 `(10*1.5)+5`，结果截然不同。
3.  **互斥管理:** 如何实现“武器附魔只能有一个”？

**解决方案：Modifier Pipeline (中间件模式)**
不再使用层层包裹，而是维护一个**有序列表**。

```csharp
public enum ModifierPriority {
    BaseStats = 100,   // 基础数值 (+10)
    Multiplier = 200,  // 乘法修正 (+50%)
    Conversion = 300,  // 属性转化 (物理转火)
    OnHit = 400        // 击中特效
}

public class AttackPipeline {
    private List<IAttackModifier> _modifiers = new List<IAttackModifier>();

    public void AddModifier(IAttackModifier mod) {
        // 1. 处理互斥 (Conflict Policy)
        var existing = _modifiers.Find(m => m.GroupID == mod.GroupID);
        if (existing != null && mod.Policy == ConflictPolicy.Override) {
            _modifiers.Remove(existing);
        }
        
        // 2. 添加并排序
        _modifiers.Add(mod);
        _modifiers.Sort((a, b) => a.Priority.CompareTo(b.Priority));
    }

    public void Execute(AttackContext ctx) {
        foreach (var mod in _modifiers) {
            mod.OnAttack(ctx);
            if (ctx.IsConsumed) break; // 支持中断 (如被格挡)
        }
    }
}
```

---

## 3. 性能特化模式 (Performance Oriented)

### 3.1 数据局部性 (Data Locality / ECS)
*   **理论:** CPU 缓存行 (Cache Line) 极其敏感。处理连续内存的数据比处理随机指针快几十倍。
*   **实战:** **Unity DOTS (Data-Oriented Technology Stack)**。
    *   **Struct vs Class:** 核心战斗数据全部用 `struct` 存储。
    *   **Array vs List:** 使用定长数组或 NativeArray。
*   **Vampirefall 应用:** 500+ 同屏怪物的移动与碰撞计算。

### 3.2 享元模式 (Flyweight)
*   **理论:** 运用共享技术有效地支持大量细粒度的对象。
*   **实战:** **ScriptableObject**。
    *   1000 个哥布林，不需要存 1000 份“攻击力=5，名字=Goblin”。
    *   它们共享同一个 `MonsterData.asset` (ScriptableObject)。
    *   每个实例只存变化的数据（当前血量、位置）。

---

## 4. 设计模式陷阱 (Anti-Patterns)

1.  **过度单例 (Singleton Abuse):** 导致代码变成一团乱麻，哪里都能改数据，无法追踪 Bug 来源。
2.  **上帝类 (God Class):** 一个 `PlayerController` 写了 3000 行代码，包含输入、移动、动画、音效。**解法:** 使用组件模式 (Component)，拆分为 `PlayerInput`, `PlayerMover`, `PlayerAnimator`。
3.  **过度设计 (Over-Engineering):** 为还没出现的需求写复杂的接口。**YAGNI (You Aren't Gonna Need It)** 原则是王道。

---

## 📚 扩展阅读与代码圣经 (References)

### 🏛️ 设计模式基础
*   **[Game Programming Patterns](https://gameprogrammingpatterns.com/)** (Bob Nystrom)
    *   **必读圣经**。免费在线阅读。重点推荐 *Type Object* (对应 ScriptableObject) 和 *Data Locality* (对应 DOTS) 章节。
*   **[Refactoring.Guru](https://refactoring.guru/design-patterns)**
    *   图文并茂地讲解了 GoF 23 种经典模式。如果你忘了“装饰器模式”怎么写，来这查。

### 🏎️ 性能与架构
*   **[Unity ECS (Entity Component System) Documentation](https://docs.unity3d.com/Packages/com.unity.entities@latest)**
    *   官方 DOTS 文档。理解数据导向编程 (Data-Oriented Design) 的权威来源。
*   **[Dependency Injection in Unity](https://www.youtube.com/watch?v=NkQ_nQw5eNo)** (Infallible Code)
    *   讲解为什么你应该使用 DI (依赖注入) 来替代 Singleton，从而写出更干净、可测试的代码。

### 🔧 实战案例
*   **[Command Pattern in Strategy Games](https://www.gamasutra.com/view/feature/131265/implementing_a_command_system_for_.php)**
    *   详解如何利用命令模式实现 RTS 游戏中的“输入缓冲”和“回放系统”。
