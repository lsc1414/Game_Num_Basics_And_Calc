# 🎲 Roguelike 随机算法剖析：从纯随机到智能加权

> **核心问题**: 为什么在 *Hades* 中我觉得是我构建了 Build，而在有些国产肉鸽中我觉得纯粹是运气好？
> **答案**: 优秀的 RNG (随机数生成) 不是掷骰子，而是 **"有偏见的上帝" (Biased God)**。

## 1. 三大流派解析

### 1.1 吸血鬼幸存者 (Vampire Survivors) - "纯随机 + 进化树"
*   **算法**: **Bag Random w/ Evolution Check**
*   **机制**:
    *   **武器池**: 纯随机抽取。
    *   **被动池**: 纯随机抽取。
    *   **进化 (关键)**: 一旦你持有 `鞭子` + `黑心`，下次宝箱 **100%** 掉落进化后的 `血鞭`。
*   **体验**: 它的爽感来自于 **"公式背诵"**。玩家觉得自己是天才，因为他背住了进化公式，而不是因为他运气好。
*   **Vampirefall 适用性**: ⭐⭐⭐ (适合作为底层保底)。

### 1.2 土豆兄弟 (Brotato) - "标签加权 (Tag Weighting)"
*   **算法**: **Dynamic Tag Bias**
*   **机制**:
    *   每个道具都有标签：`[近战]`, `[远程]`, `[元素]`, `[速度]`。
    *   **滚雪球**: 当你拿了第一把 `[近战]` 武器后，下一轮商店刷新出 `[近战]` 标签物品的概率 **提升 5-10%**。
    *   **商店锁定**: 允许玩家“锁”住一个道具下回合买。
*   **体验**: 玩家觉得系统“懂我”。我想玩近战，系统就给我推近战。
*   **Vampirefall 适用性**: ⭐⭐⭐⭐⭐ (极度推荐)。因为塔防需要高度特化的 Build（全火塔或全物理塔），如果纯随机，很容易随出一堆不沾边的塔导致崩盘。

### 1.3 哈迪斯 (Hades) - "伪随机树 (Pseudo-RNG Tree)"
*   **算法**: **God Pool + Pity Timer**
*   **机制**:
    *   **神明池**: 一局游戏通常只会出现 4 位神明。一旦你选了 宙斯、雅典娜、阿瑞斯、波塞冬，第 5 位神明出现的概率会降到极低。
    *   **双重祝福 (Duo Boons)**: 只要你通过前置条件（如拥有宙斯的普攻 + 雅典娜的特技），下次遇到这两位神，出现双重祝福的概率大幅提升。
    *   **防脸黑 (Pity)**: 如果连续 10 个房间没有遇到神明房间，第 11 个房间必出。
*   **体验**: **"构建感"** 最强。系统强迫你专注由 4 位神明组成的体系，而不是给你一堆杂乱的祝福。

## 2. 让玩家感觉像天才的算法：智能加权 (Smart Weighting)

对于 *Vampirefall*，建议采用 **Brotato 的标签加权** + **Hades 的双重祝福**。

### 2.1 核心算法逻辑

```csharp
// 伪代码：计算物品出现权重
float CalculateWeight(Item item, PlayerState player) {
    float weight = item.baseWeight;

    // 1. 标签协同 (Synergy)
    foreach (var tag in item.tags) {
        if (player.HasTag(tag)) {
            weight *= 1.5f; // 玩家已有同类物品，权重提升
        }
    }

    // 2. 互斥剔除 (Exclusion)
    if (player.HasIncompatibleTag(item.tags)) {
        weight *= 0.1f; // 玩家玩的是物理流，元素物品权重降低
    }

    // 3. 套装保底 (Set Completion)
    if (player.HasItem(item.requiredParent)) {
        weight *= 10.0f; // 玩家有前置塔，进阶塔权重暴增
    }

    return weight;
}
```

### 2.2 具体的“天才时刻”设计

1.  **预测需求**:
    *   玩家造了 5 个 **火塔**。
    *   下一轮选卡，系统故意刷出 **"所有火塔攻击附带油浸效果"** 的紫卡。
    *   *玩家反应*: "卧槽！这正是我要的！这 Build 无敌了！" (其实是系统喂到嘴边的)。

2.  **关键 Key 牌**:
    *   设计一些只有在特定极端条件下才会出现的卡。
    *   比如玩家 **只有 1 滴血** 时，大幅提高 **"背水一战 (血越少攻越高)"** 的权重。

3.  **重随机制 (Reroll)**:
    *   给玩家有限的刷新机会，但每次刷新都会**轻微增加**玩家当前流派相关卡的权重。
    *   第一次刷不到，第二次刷到的概率变大。让玩家觉得是自己“坚持不懈”刷出来的。

## 3. 必须避免的坑

1.  **完全纯随机**: 这是最懒的设计。塔防游戏如果随不到关键塔是没法玩的。必须有**保底机制**（如每 3 次选卡必出塔卡）。
2.  **过度智能**: 如果每次都给玩家最完美的卡，游戏会变得无聊。必须保留 20% 的“垃圾卡”或者“干扰项”，让玩家有**甄别**的快感。
3.  **隐藏机制不透明**: *Brotato* 的标签是写在明面上的。玩家知道“买近战会出更多近战”。如果这个机制是隐性的，玩家就无法主动利用它，也就无法产生“我是天才”的感觉。

## 4. 结论

要在 *Vampirefall* 中实现“天才感”：
1.  **显性标签**: 所有的塔和装备都要有 `[火]`, `[速]`, `[暴]` 这样的标签。
2.  **动态权重**: 玩家拿了 `[火]`，后续出 `[火]` 的概率 +20%。
3.  **双重质变**: 设计类似 *Hades* 的双重祝福（如 火+油），并在玩家凑齐前置时，**疯狂暗示**甚至**硬塞**给他。

让玩家觉得运气好，是 Roguelike 的入门；让玩家觉得是自己的选择导致了无敌，才是 Roguelike 的大师。

---

## 📚 扩展阅读与数学原理 (References)

### 🎲 随机性理论
*   **[Randomness in Game Design](https://www.youtube.com/watch?v=dwI5b-wRLic)** (Game Maker's Toolkit)
    *   Mark Brown 深入浅出地解释了 **"Input Randomness" (输入随机)** vs **"Output Randomness" (输出随机)** 的区别。
*   **[Controlling Chaos: The Art of RNG](https://www.gdcvault.com/play/1024927/Controlling-Chaos-The-Art-of)** (GDC 2018)
    *   *Slay the Spire* 的开发者演讲（如果找不到原视频，可参考相关设计文章），讲述如何平衡卡牌游戏的随机性。

### 💻 算法实现
*   **[Shuffle Bag Algorithm](https://tetrisconcept.net/wiki/Random_Generator)** (Tetris Wiki)
    *   俄罗斯方块的随机生成器（7-Bag 机制）。这是实现“防脸黑”保底机制的最简单算法。
*   **[Weighted Random Selection](https://blog.bruce-hill.com/a-faster-weighted-random-choice)**
    *   技术博客，详细比较了多种加权随机算法的性能（O(n) vs O(log n)）。在 *Vampirefall* 中，如果掉落池很大，需要高效算法。

### 🎮 案例研究
*   **[Hades' "God Mode" and Pity Timers](https://www.supergiantgames.com/blog/hades-updates/)** (Supergiant Blog)
    *   研究 Hades 如何通过隐性的数值调整来控制玩家的心流体验。
*   **[Unity Random Class Documentation](https://docs.unity3d.com/ScriptReference/Random.html)**
    *   官方文档。注意 `Random.Range` 的边界问题（整数是包左不包右，浮点数是全包）。
