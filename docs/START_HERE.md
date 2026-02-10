---
sidebarTitle: "新人上路指南"
title: "新人上路指南"
---
> **摘要**：本文聚焦「新人上路指南」，梳理核心概念、关键方法与落地实践。

欢迎加入游戏开发 101！本指南帮助你快速熟悉文档结构和核心知识。

## 📖 文档结构

```
docs/
├── 🎨 Art/          # 美术相关 (技术美术、UI、VFX)
├── 🎵 Audio/        # 音频设计
├── 🎮 Design/       # 游戏设计 (数值、机制、系统)
├── 📖 Case_Studies/ # 游戏案例分析
├── 📖 Dev_Guides/   # 开发实战指南
├── 🖥️ Tech/         # 技术实现
└── 📋 Unity_Standards/ # 规范标准
```

## 🎯 推荐阅读顺序

### 1. 理解项目定位 (30 分钟)

- [设计哲学与系统架构](Design/Philosophy_And_Systems)
- [混合类型游戏分析](Design/Philosophy_And_Systems/Hybrid_Genre_Analysis)

### 2. 掌握核心数值 (2 小时)

- [核心数值手册](Design/Numerical_Manual) ⭐ 必读
- [数值框架方法论](Design/Numerical/Numerical_Framework_Methodology)

### 3. 学习核心机制 (2 小时)

- [战斗系统详解](Design/Mechanics/Combat_System)
- [Roguelike Perk 系统](Design/Mechanics/Roguelike_Perks)
- [塔防建筑机制](Design/Mechanics/Tower_Defense_System)

### 4. 参考成功案例 (1 小时)

- [Hades 构建多样性](Case_Studies/Roguelike/Hades)
- [Dead Cells 知识图谱](Case_Studies/Roguelike/Dead_Cells)
- [Vampire Survivors 性能奇迹](Case_Studies/Survivors/Vampire_Survivors)

## 🧭 先选阅读路线（建议）

如果你是带着具体工作目标来的，先看 [阅读导航中心](NAVIGATION.md)：

- 按职责：程序 / 美术 / 策划 / 发行 / 运营 / 制作管理
- 按阶段：立项 -> 预制作 -> 制作 -> 上线与长线
- 按目标：战斗手感、数值框架、性能稳定、上线运营

## 🛠️ 工具与规范

- [Unity 资产命名规范](Unity_Standards/Asset_Naming)
- [项目文件夹结构](Unity_Standards/Folder_Structure)
- [全员速查表](Dev_Guides/Project_Cheat_Sheet)

## 💡 常见问题

**Q: 文档太多，从哪里开始？**

A: 先看 [核心数值手册](Design/Numerical_Manual)，这是整个项目的数学基础。

**Q: 如何贡献文档？**

A: 使用 GitHub PR，遵循 [Git 提交规范](Dev_Guides/Collaboration/Git_Commit_Standards)。
