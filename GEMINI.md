# 🤖 Project 游戏开发 101 - AI Context Summary (GEMINI.md)

## 📌 Project Overview

**Project Vampirefall** is a hybrid game combining **Tower Defense**, **Roguelike**, and **Looter** mechanics.
This repository (`Server/Game_Num_Basics_And_Calc`) serves as the **Single Source of Truth** for all numerical models, design philosophies, and technical standards.

## 🗺️ Directory Structure & Key Documentation

### 1. Design (`/Design`) - The "Soul"

- **Numerical & Combat**:
  - `Numerical_Manual.md`: **CRITICAL**. The mathematical "bible" (Damage formulas, Defense models).
  - `Mechanics/Combat_System.md`: Damage types, status effects, resilience.
- **Systems**:
  - `Mechanics/Tower_Defense_System.md`: Tower types, building rules.
  - `Mechanics/Roguelike_Perks.md`: In-game growth, perks, curses.
  - `Systems/Itemization.md`: Equipment, affixes, loot generation.
  - `Systems/Loot_Table_Rules.md`: Drop logic, reservoirs.
- **Content**:
  - `Content/Enemy_Bestiary.md`: Enemy types, AI behaviors.
  - `Content/Level_Design_Guide.md`: Map generation, wave control.

### 2. Tech (`/Tech`) - The "Brain"

- **AI & Decision Making**:
  - `AI_Utility_System.md`: Utility-based AI decision making (Scoring curves).
  - `FSM_Design_Patterns.md`: State machine patterns for AI/Towers.
  - `Architecture/Unified_Decision_System.md`: Modular decision logic.
- **Core Systems**:
  - `Mobile_Optimization_Guide.md`: TBDR, Overdraw, Half-precision.
  - `Mechanics/Unity_Transform_Math_Guide.md`: Vector math, Matrices, RectTransform.

### 3. Standards (`/Unity_Standards`)

- **Code & Assets**:
  - `Tools/AssetNamingValidator.cs`: Editor tool for enforcing naming conventions.

## 🧠 Key Concepts for AI Agents

1.  **Data-Driven Design**: Most logic should be configurable via tables/ScriptableObjects.
2.  **Hybrid Gameplay**: Always consider how a change affects both the Tower Defense aspect and the Action/RPG aspect.
3.  **Performance First**: Mobile optimization is a priority. Avoid heavy per-frame allocations.

## 👮 AI Rules (Must Follow)

1.  **Language**: All output must be in **Chinese** (except for code).
2.  **Documentation**: When adding a new document, you **MUST** update `readme.md` to include a link to it.
3.  **MkDocs Compatibility**:

    - **Mermaid**: Use standard fenced code blocks with language `mermaid`. MkDocs Material handles rendering automatically.
    - **Math**: Use LaTeX syntax (`$..$` or `$$..$$`).
    - **Tables**: Ensure there is an empty line before the start of any Markdown table.

4.  **Navigation Maintenance**: When adding a new document, you **MUST**:

    - **Update `mkdocs.yml`**: Add the file path to the `nav` section under the appropriate category.
    - **Icons**: 📐Math / ⚔️Combat / 🏗️Arch / 🤖AI / 🎮Design / 📖Graph / 💀Fail / 🎨Art / 🎵Audio / 🛠️Tool / 🚀Live / 📋Std.

## 🔗 Quick Links

- [Main Readme](readme.md)
- [Numerical Manual](Design/Numerical_Manual.md)
