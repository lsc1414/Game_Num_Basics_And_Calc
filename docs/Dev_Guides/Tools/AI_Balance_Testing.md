---
sidebarTitle: "AI 平衡测试工具：利用 LLM 进行自动化数值验收"
title: "AI 平衡测试工具：利用 LLM 进行自动化数值验收"
---
> **摘要**：本文围绕「AI 平衡测试工具：利用 LLM 进行自动化数值验收」提供核心内容与可落地方法。

---

**文档目标**：介绍如何利用大语言模型 (Claude 3.5 Sonnet / GPT-4o) 作为“虚拟测试员”，以极低成本进行数千轮的游戏平衡性测试。

---

## 1. 为什么不用真人测试？

在 Vertical Slice 阶段，真人测试极其昂贵且低效：

*   **时间成本**：玩一局 20 分钟，测试 100 局需要 33 小时。
*   **主观偏差**：开发者自己玩通常太强，无法模拟新手体验。
*   **数据稀疏**：很难覆盖所有 Build 组合。

**AI 方案**：让 LLM 扮演特定类型的玩家，阅读战斗日志，给出反馈。

---

## 2. 架构设计 (The Pipeline)

### 2.1 角色扮演 (Personas)
我们需要定义不同的 System Prompt：

*   **The Timmy (爽游玩家)**：喜欢大数字，讨厌复杂机制，对 TTK 敏感。
*   **The Spike (硬核玩家)**：寻找最优解，对数值平衡极其敏感。
*   **The Newbie (萌新)**：容易迷路，不懂元素克制，容易受挫。

### 2.2 输入数据 (Context)
不是把画面截图给 AI，而是发送**结构化日志 (JSON)**：
```json
{
  "turn": 15,
  "player": { "hp": 20, "build": "FireMage", "dps": 450 },
  "enemies": [
    { "name": "GoblinElite", "status": "Burning", "hp_percent": 0.1 }
  ],
  "events": [
    "Player cast Fireball, dealt 120 dmg",
    "GoblinElite hit Player, dealt 5 dmg"
  ]
}
```

### 2.3 提示词 (Prompt)
> "你是 Timmy，一个喜欢割草的休闲玩家。阅读上面的战斗日志。
> 1. 给爽快感打分 (1-10)。
> 2. 你觉得现在的难度是‘无聊’、‘适中’还是‘太难’？
> 3. 如果你要退款，会是因为什么？"

---

## 3. 实战脚本 (Python + OpenAI API)

```python
import openai

def analyze_combat_log(log_json, persona="Timmy"):
    prompts = {
        "Timmy": "You are a casual gamer...",
        "Spike": "You are a competitive gamer..."
    }
    
    response = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": prompts[persona]},
            {"role": "user", "content": f"Analyze this log: {log_json}"}
        ]
    )
    return response.choices[0].message.content

## 批量运行
for i in range(10):
    log = run_headless_game_simulation() # 运行一局游戏仿真
    feedback = analyze_combat_log(log)
    print(f"Round {i} Feedback: {feedback}")
```

---

## 4. 成本与收益分析

*   **成本**：
    *   1 局日志约 2k tokens。
    *   GPT-4o-mini 价格极低。
    *   跑 100 局测试 < $0.5 美元。
*   **收益**：
    *   **发现隐性 Bug**：AI 可能会问“为什么我满血被一刀秒了？”，指出数值边界溢出。
    *   **情感曲线验证**：检查波峰波谷是否符合设计预期（Design/Philosophy_And_Systems.md）。

---

## 5. 局限性
*   AI 无法测试“手感” (Game Feel)，如打击感、操作延迟。
*   AI 可能会产生幻觉 (Hallucination)，需要人工抽查。

**结论**：此工具用于**数值体验**的初筛，而非最终验收。
