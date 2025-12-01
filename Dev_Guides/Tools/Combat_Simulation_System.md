# ⚔️ 战斗仿真系统 (Combat Simulation System)：Python 极速模拟

**文档目标**：在不启动 Unity 的情况下，通过纯数据模拟进行数万次战斗迭代，验证 PRD、暴击率、闪避率及数值成长的数学期望。

---

## 1. 为什么需要仿真？

在 Unity 中按下 "Play" -> 等待编译 -> 加载场景 -> 刷怪 -> 战斗，整个流程至少需要 30 秒。
如果我们要验证“15% 闪避率在 10,000 次攻击下的实际减伤期望”，在 Unity 里跑要几个小时。

**Python Headless 仿真**：
*   无渲染，纯逻辑。
*   1 秒钟跑 10,000 局。
*   直接生成 Excel/CSV 报表。

---

## 2. 系统架构

### 2.1 实体类 (Entity)
```python
class Entity:
    def __init__(self, hp, atk, defense, dodge_rate):
        self.max_hp = hp
        self.hp = hp
        self.atk = atk
        self.defense = defense
        self.dodge_rate = dodge_rate
        self.prd_counter = 1 # PRD 计数器

    def take_damage(self, amount):
        actual_dmg = amount * (1 - self.defense / (self.defense + 100))
        self.hp -= actual_dmg
        return self.hp <= 0
```

### 2.2 战斗循环 (Battle Loop)
```python
def simulate_battle(hero, monster_list):
    log = []
    ticks = 0
    while hero.hp > 0 and len(monster_list) > 0:
        ticks += 1
        # 简单的回合制或时间片逻辑
        target = monster_list[0]
        
        # Hero Attack
        if ticks % hero.atk_speed == 0:
            target.take_damage(hero.atk)
            if target.hp <= 0:
                monster_list.pop(0)
                
        # Monster Attack
        for m in monster_list:
            if ticks % m.atk_speed == 0:
                # PRD 闪避判定
                if not check_dodge_prd(hero): 
                    hero.take_damage(m.atk)
                    
    return ticks, hero.hp # 返回战斗时长和剩余血量
```

---

## 3. 使用场景与输出

### 3.1 场景 A：PRD 算法验证
*   **输入**：设置闪避率为 20%，运行 100,000 次受击判定。
*   **验证**：统计实际闪避次数。如果是 True Random，方差会很大；如果是 PRD，应该非常接近 20,000 次。
*   **图表**：绘制“连续未闪避次数”的分布直方图。

### 3.2 场景 B：Build 强度对比
*   **Build A**: 高攻低频 (Attack = 100, Speed = 1.0)
*   **Build B**: 低攻高频 (Attack = 10, Speed = 0.1) + 每次攻击附带 5 点真实伤害。
*   **模拟**：对抗高甲单位 (Def = 80) 和 低甲单位 (Def = 0)。
*   **结果**：直接输出胜率矩阵。

---

## 4. 集成到工作流

1.  策划在 CSV 中配置数值。
2.  运行 `python run_sim.py`。
3.  脚本自动读取 CSV，跑 1000 局模拟。
4.  输出 `report.html` (使用 Matplotlib 绘图)。
5.  如果平衡性通过，再让程序在 Unity 中实装数值。

**核心价值**：**Fail Fast**。在写一行 C# 代码之前，先确无数值模型是成立的。
