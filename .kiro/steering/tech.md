# 技术栈与构建系统

## 主要技术

**Unity Engine** - 这是一个基于 Unity 的游戏项目，使用 C# 作为主要编程语言。

## 关键技术与框架

### 核心系统
- **ECS (Entity Component System)**: 面向数据的设计，用于性能关键系统
- **Luban**: 配置表管理和数据导出工作流
- **Odin Inspector**: 增强的 Unity 检视器和编辑器工具
- **ScriptableObjects**: 数据驱动的游戏配置设计

### 架构模式
- **Unified Decision System（统一决策系统）**: AI、塔和弹道共享的模块化决策逻辑
- **Utility AI System（效用 AI 系统）**: 基于评分的敌人行为决策
- **FSM (Finite State Machine)**: 角色和游戏流程的状态管理
- **GAS (Gameplay Ability System)**: 技能和能力框架

### 图形与渲染
- **HDR Rendering**: 高动态范围渲染与色调映射
- **Compute Shaders**: GPU 加速计算（移动端优化）
- **GPU Instancing**: 批量渲染优化
- **Particle Systems**: VFX 优化与 Overdraw 管理

### 音频
- **Wwise**（可选）: 复杂项目的音频中间件
- **Lightweight Audio Framework（轻量级音频框架）**: 基于代码的音频管理方案
- **Adaptive Music System（自适应音乐系统）**: 垂直分层和水平切换的动态音乐

### 工具与实用程序
- **NavMesh**: 寻路和动态避障
- **PRD Algorithm（伪随机分布算法）**: 用于掉落和战利品
- **WFC (Wave Function Collapse)**: 程序化生成
- **Monte Carlo Simulation（蒙特卡洛模拟）**: 平衡测试和概率验证

## 代码规范

### 命名约定
- **类/方法**: PascalCase（`PlayerController`、`Attack()`）
- **公共变量**: PascalCase（`public float Health;`）
- **私有变量**: _camelCase（`private int _currentHealth;`）
- **局部变量/参数**: camelCase（`float damage`）
- **常量**: SCREAMING_SNAKE_CASE（`const int MAX_HP = 100;`）

### 文件命名
- **脚本**: 与类名完全匹配（`PlayerController.cs`）
- **预制体**: `P_` 前缀（`P_GoblinWarrior`）
- **材质**: `M_` 前缀（`M_HeroSkin`）
- **纹理**: `T_` 前缀（`T_Brick_D`）
- **UI 精灵**: `UI_` 前缀（`UI_Btn_Close`）
- **场景**: `L_` 前缀（`L_MainMenu`）

### 需要避免的反模式
- 单例滥用（参见 `Tech/Architecture/Unity_Anti_Patterns.md`）
- 过度使用协程
- 在性能关键路径使用 LINQ
- 滥用 Resources 文件夹
- 在热路径中进行逐帧内存分配

## 常用命令

### Git 工作流
```bash
# 标准提交格式
git commit -m "feat: add tower targeting system"
git commit -m "fix: resolve enemy spawn timing issue"
git commit -m "docs: update numerical manual"

# 分支策略
git checkout -b feature/tower-system
git checkout -b fix/enemy-ai-bug
```

### Unity 编辑器工具
- **菜单: Tools/Setup Project Folders** - 初始化标准文件夹结构
- **菜单: Tools/Validate Asset Naming** - 检查命名规范合规性
- **菜单: Tools/Combat Simulation** - 运行平衡测试
- **菜单: Tools/Generate Wiki** - 从数据自动生成文档

### 测试与验证
- 使用 **Debug Console** 和 GM 命令进行快速测试
- **Roguelike Rapid Testing System（肉鸽快速测试系统）**: 词条组合热重载
- **AI Balance Testing（AI 平衡测试）**: 自动化模拟运行
- **Monte Carlo Simulation（蒙特卡洛模拟）**: 概率验证工具

## 性能目标

### 移动端优化
- **Draw Calls（绘制调用）**: 每帧 < 100
- **Batches（批次）**: 通过 GPU Instancing 最大化
- **Overdraw（过度绘制）**: 平均 < 2x（使用 VFX 优化指南）
- **Memory（内存）**: 纹理压缩（移动端使用 ASTC）
- **Frame Budget（帧预算）**: 16.6ms (60 FPS) 或 33.3ms (30 FPS)

### 资源标准
- **纹理**: 3D 使用 POT（2 的幂次方），UI 允许 NPOT
- **模型**: 复杂网格使用 LOD 系统
- **音频**: 压缩格式，BGM 使用流式加载
- **粒子**: 限制同时存在的系统数量，使用对象池

## 文档参考

详细技术实现参考：
- 架构模式：`Tech/Architecture/`
- 性能优化：`Tech/Mobile_Optimization_Guide.md`
- 代码片段：`Tech/Code_Snippets/`
- Unity 最佳实践：`Dev_Guides/Technical_Implementation/Game_Dev_Best_Practices.md`
