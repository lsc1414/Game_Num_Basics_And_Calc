# 项目结构与组织

## 仓库类型

这是一个**文档仓库**，而非游戏源代码仓库。包含 Project Vampirefall 的设计文档、技术规范和知识库资料。

## 顶层组织结构

```
/
├── Art/                    # 视觉设计指南和标准
├── Audio/                  # 音频系统设计和实现指南
├── Design/                 # 游戏设计文档（核心支柱）
├── Dev_Guides/            # 生产、协作和工作流程指南
├── Research/              # 实验性代码示例和分析报告
├── Tech/                  # 技术架构和实现
├── Unity_Standards/       # Unity 特定的约定和工具
├── .agent/                # AI 代理工作流定义
├── .kiro/                 # Kiro steering 规则（本文件夹）
└── readme.md              # 主入口和导航
```

## 关键目录详解

### `/Design` - 项目灵魂
主要设计文档，按以下方式组织：
- **Mechanics/**: 核心玩法系统（战斗、塔防、肉鸽词条、元素反应）
- **Systems/**: 元系统（装备、经济、掉落表、成长）
- **Content/**: 关卡设计、敌人图鉴、Boss 设计
- **Numerical/**: 数学框架和平衡模型
- **LiveOps/**: 通行证、活动和运营设计
- **UX/**: 无障碍和 FTUE（首次用户体验）
- **CaseStudies/**: 行业分析和竞品研究
- **Knowledge Maps（知识图谱）**: 参考游戏深度分析（Binding of Isaac、Dead Cells、Risk of Rain 2 等）

### `/Tech` - 技术实现
- **Architecture/**: 核心模式（ECS、统一决策系统、设计模式）
- **Algorithms/**: 程序化生成、RNG 系统、常用游戏算法
- **Mechanics/**: 玩法技术实现（弹道、瞄准、寻路）
- **Code_Snippets/**: 重构示例和性能演示
- **Graphics/**: Shader 数学、Compute Shaders
- **Math/**: 游戏曲线和数学基础

### `/Dev_Guides` - 生产与工作流
- **Art_Pipeline/**: 资源导出标准、灰盒工作流、UI 制作
- **Collaboration/**: Git 工作流、PR 标准、敏捷实践
- **Publishing/**: Steam 和 TapTap 发行策略
- **Tools/**: 调试控制台、数值计算器、自动化测试
- **Industry_Cases/**: 成功游戏分析（Vampire Survivors、Hades、Kingdom Rush）
- **Failure_Cases/**: 失败项目复盘（Anthem、Concord、Paragon）

### `/Unity_Standards` - Unity 约定
- **Asset_Naming.md**: 完整的命名规则与前缀/后缀表
- **Folder_Structure.md**: 混合式特性组织
- **Asset_Management.md**: 资源工作流和优化
- **Tools/**: 验证用编辑器脚本（AssetNamingValidator.cs）

### `/Research` - 实验性工作
- **Code/**: 示例实现（PerkSystemFramework、PRDAlgorithm、DynamicWeightSystem）
- **GUI/**: UI 原型（CurseSystemUI、DraftSystemUI）
- **Assets/**: 测试数据（PerkData.json）
- 中文分析报告

### `/Art` & `/Audio` - 创意标准
- 美术方向、视觉质量指南、VFX 标准
- 相机设置、游戏手感、UI/UX 指南
- 音频系统设计、自适应音乐、Wwise 集成

## 文件命名约定

### 文档文件
- 使用描述性英文名称，用下划线分隔：`Tower_Defense_System.md`
- 知识图谱：`[GameName]_Knowledge_Map.md`
- 深度分析：`[Topic]_DeepDive.md`
- 案例研究：`[GameName]_[Type]_Analysis.md`

### 代码文件
- C# 脚本：PascalCase 匹配类名（`PlayerController.cs`）
- JSON 数据：camelCase 或 PascalCase（`PerkData.json`）

### 特殊文件
- `CLAUDE.md` / `GEMINI.md`: AI 助手上下文文件
- `readme.md`: 主导航（小写符合 GitHub 约定）
- `Research_TODO.md` / `TODO.md`: 任务跟踪

## 导航模式

`readme.md` 作为**中心枢纽**，包含：
- 不同角色的快速入门指南（策划、程序、美术）
- 按领域组织的可展开章节
- 关键文档的直接链接
- 展示三大核心支柱的可视化表格

**重要**: 添加新文档时，务必更新 `readme.md`，在相应章节中添加链接。

## 文档标准

### 结构要求
1. **Emoji 标题**: 使用相关 emoji 建立视觉层级（🎯、🧠、⚔️ 等）
2. **为什么 + 怎么做 + 示例**: 不仅要说明怎么做，还要解释为什么，并提供业界示例
3. **中文内容**: 所有说明性文字使用简体中文
4. **英文术语**: 技术术语、代码和文件名使用英文
5. **GitHub Pages 兼容**: 图表使用正确的 Mermaid 脚本标签

### 交叉引用
- 使用相对路径：`[链接文字](../Design/Systems/Itemization.md)`
- 引用业界示例："参考: Kingdom Rush"、"ref: Path of Exile"
- 在文件末尾链接到相关文档

## 文件夹组织哲学

**混合式方法**: 
- **底层**（共享资源）: 按类型组织（Art、Audio、Tech）
- **顶层**（特定功能）: 按领域组织（Design、Dev_Guides）
- **原则**: 文件夹内高内聚，文件夹间低耦合

这样做的好处：
- 易于删除整个功能集
- 清晰的所有权边界
- 最小化交叉依赖
- 随项目增长可扩展的结构

## 使用本仓库

### 策划人员
从 `/Design` 开始，参考 `/Dev_Guides/Industry_Cases` 获取灵感

### 程序人员  
从 `/Tech/Architecture` 开始，参考 `/Unity_Standards` 了解约定

### 美术人员
从 `/Art` 开始，参考 `/Dev_Guides/Art_Pipeline` 了解工作流

### 制作人
从 `/Dev_Guides/Production_Lessons` 和 `/Dev_Guides/Publishing` 开始

### AI 助手
- 阅读 `CLAUDE.md` 或 `GEMINI.md` 了解上下文
- 遵循 `.kiro/steering/` 中的 steering 规则
- 除代码外始终使用中文输出
- 添加新文档时更新 `readme.md`
