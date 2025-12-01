# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 🎯 Project Overview

**Project Vampirefall** - A hybrid game combining Tower Defense, Roguelike, and Looter mechanics. This repository serves as the "Single Source of Truth" for all mathematical models, design philosophies, and technical standards.

## 🚀 Development Commands

### Interactive Numerical Calculator
```bash
# Open the interactive calculator for validating damage formulas and game mechanics
open Design/Calculator/index.html
# Or serve it locally
python -m http.server 8000
# Then navigate to http://localhost:8000/Design/Calculator/index.html
```

### Unity Asset Validation
```bash
# Copy the naming validator to Unity project
cp Unity_Standards/Tools/AssetNamingValidator.cs /path/to/unity/project/Assets/Editor/
```

## 📐 Core Numerical Formulas

### Damage Calculation (Golden Formula)
```
最终伤害 = 输出面板 × 防御减伤系数
输出面板 = [(面板攻击 × 技能倍率) + 技能固定伤] × (1 + 增伤总和) × (1 + 独立增伤A) × (1 + 独立增伤B)... × 暴击期望
```

### Key Formulas
- **Armor Reduction**: `物理减伤 = 护甲 / (护甲 + 3000)`
- **Elemental Resistance**: `抗性倍率 = 1 - min((目标抗性 - 攻击者穿透), 75%)`
- **Effective HP**: `EHP = 生命值 / ((1 - 减伤率) × (1 - 闪避率))`
- **Combat Power**: `战斗力 = Σ(属性值 × 权重) + 机制分`

### Numerical Standards
- **Randomness**: Use PRD (Pseudo-Random Distribution) for critical hits and evasion
- **Cooldown Cap**: 75% maximum cooldown reduction
- **Attack Speed**: Separate from cooldown system
- **Crit Rate**: Use PRD algorithm to prevent streaks

## 🏗️ Unity Project Architecture

### Directory Structure
```
Assets/
├── _Project/                   # Core development (prefixed with _ for sorting)
│   ├── Art/                    # Shared art assets
│   ├── Audio/                  # Audio resources
│   ├── Core/                   # Core frameworks (AudioSystem, EventSystem, SaveSystem, UIManager)
│   ├── Features/               # Gameplay modules (Enemies, Towers, Player, Inventory)
│   ├── Scenes/                 # Game scenes
│   └── Resources/              # Minimal usage (logos/loading only)
├── Plugins/                    # Third-party plugins
├── StreamingAssets/            # Streaming assets
└── Editor/                     # Editor tool scripts
```

### Asset Naming Conventions
Format: `[前缀]_[模块/类别]_[名称]_[变体/后缀]`

| Asset Type | Prefix | Example |
|------------|--------|---------|
| Prefab | `P_` | `P_Hero`, `P_Tower_Archer` |
| Material | `M_` | `M_HeroSkin`, `M_Water` |
| Texture (3D) | `T_` | `T_Brick_D`, `T_Brick_N` |
| UI Sprite | `UI_` | `UI_Btn_Close`, `UI_Icon_Skill` |
| Audio (SFX) | `SFX_` | `SFX_Hit`, `SFX_Coin` |
| Audio (BGM) | `BGM_` | `BGM_Boss`, `BGM_Menu` |
| Scene | `L_` | `L_MainMenu`, `L_Dungeon_01` |

### Critical Unity Rules
1. **Never move assets outside Unity** - always use Project window to maintain meta files
2. **No Resources folder** - causes startup slowdown and memory issues
3. **Use Addressables** for asset management and hot updates
4. **Git LFS required** for large binary files (PSD, FBX, WAV, MP4)
5. **Force To Mono** for audio clips
6. **Test multiple resolutions** and aspect ratios

## 🎮 Game Systems

### Combat System
- **Three damage types**: Physical (vs Armor), Elemental (Fire/Ice/Lightning vs Resistance), Chaos (ignores shields)
- **Status effects**: Ignite, Chill, Freeze, Shock, Bleed with specific durations and effects
- **Poise system**: Break poise to stagger enemies and interrupt skills
- **Combo system**: Maintain damage within 3 seconds to build combo rewards

### Tower Defense
- **Core philosophy**: "Player is the spear, towers are the shield" - player handles burst damage, towers handle sustained defense
- **Resource loop**: Tower resources from monster kills, encourages active combat
- **Tower lifecycle**: Instant build → 2s deployment → attackable → repairable → upgradeable → salvageable (50% refund)
- **Synergy systems**: Overdrive (spend mana to double tower attack speed), weapon enchantments affect nearby towers

### Roguelike Perks
- **Draft system**: Choose 1 of 3 perks with Common/Rare/Epic/Legendary rarities
- **Dynamic weights**: Adjusts probabilities based on selected tags, includes bad luck protection
- **Curse system**: Powerful buffs with permanent debuffs for high risk/reward gameplay

### Itemization
- **Rarity tiers**: Normal (White) → Magic (Blue, 1-2 affixes) → Rare (Yellow, 3-6 affixes) → Legendary (Orange, fixed effects)
- **Affix structure**: Prefixes determine base stats, suffixes determine secondary attributes
- **Item Level (iLvl)**: Higher level items can generate higher tier affixes (T1-T10)
- **Legendary design**: Focus on mechanical changes rather than pure numerical increases

## 🛠️ Development Tools

### Asset Naming Validator
Automatically validates asset naming conventions in Unity Editor:
- Checks prefixes against asset types
- Special handling for UI vs 3D textures
- Ignores Editor scripts and plugin assets
- Logs warnings for violations

### Interactive Calculator Features
- Real-time damage formula calculations
- Armor vs Evasion efficiency comparison charts
- Critical hit stability analysis
- Attack speed and cooldown calculations
- Combat power scoring system
- Endless mode numerical growth simulation

## 📊 Performance Targets

- **Frame Rate**: 60 FPS minimum
- **Unit Cap**: 200-300 units maximum on screen
- **Texture Compression**: DXT for PC, ASTC for mobile
- **Audio**: Streaming for background music
- **LOD Policy**: Defined for maintaining performance

## 🔧 Technical Standards

- **FSM State Machines**: For monster AI logic and tower cycles
- **Event-Driven Architecture**: Use event buses to reduce coupling
- **Component-Based Design**: Favor composition over inheritance
- **Data-Driven Design**: Use ScriptableObjects for game data
- **Save System**: Version from day one with anti-cheat measures
- **Input System**: Support for controllers and accessibility features

## ⚠️ Common Pitfalls to Avoid

- Adding multiplayer to single-player games mid-development
- Hard-coding strings (especially Chinese text)
- Perfectionism over completion - ship the MVP first
- Ignoring audio design until the last minute
- Assuming all players use WASD controls
- Not planning for localization from the start
- Using the Resources folder for asset loading
- Moving assets outside Unity (breaks meta files)

## 📚 Key Documentation

### Design Documents
- `Design/Numerical_Manual.md` - Core mathematical formulas
- `Design/Mechanics/Combat_System.md` - Combat mechanics
- `Design/Mechanics/Tower_Defense_System.md` - Tower defense systems
- `Design/Systems/Itemization.md` - Equipment and item systems

### Technical Documents
- `Unity_Standards/Folder_Structure.md` - Project organization
- `Unity_Standards/Asset_Naming.md` - Naming conventions
- `Tech/Performance_Budget.md` - Performance targets
- `Tech/Save_System_Architecture.md` - Save system design

### Development Guides
- `Dev_Guides/Production_Lessons.md` - Lessons learned
- `Dev_Guides/Unity_Practical_Tips.md` - Unity development tips

## 📝 交互与文档规范 (Interaction & Documentation Standards)

1.  **中文输出与思考 (Chinese Output & Thinking):**
    *   请始终使用**中文**进行思考和回复（代码术语除外）。
    *   Output and reasoning must be in **Chinese**.
    *   所有的文档都不应该只给出**怎么做**,还需要写出**为什么**,如果是可以举例的,请举出**业界优秀的例子**
    *   生成的文档添加适当的**emoji图标**