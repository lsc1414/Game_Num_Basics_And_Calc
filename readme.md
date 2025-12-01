# 🏰 Project Vampirefall - Server & Numerical Core

[English Version](README.md) | [中文版本](README_CN.md)

Welcome to the core design and calculation repository for **Project Vampirefall**.
This project is a hybrid game combining **Tower Defense**, **Roguelike**, and **Looter** mechanics.

This directory serves as the "Single Source of Truth" for all mathematical models, design philosophies, and technical standards.

---

## 📚 Documentation Map

### 1. 🧠 Game Design (The "Soul")
#### Core Mechanics
*   **[Numerical Manual](Design/Numerical_Manual.md):** The "Bible" of math (Damage formulas, Defense models).
*   **[Combat System](Design/Mechanics/Combat_System.md):** Damage types, Status ailments, Poise/Stagger.
*   **[Tower Defense](Design/Mechanics/Tower_Defense_System.md):** Tower types, Construction rules, Hero synergy.
*   **[Roguelike Perks](Design/Mechanics/Roguelike_Perks.md):** In-run progression, Drafting pools, Curses.

#### Systems & Economy
*   **[Itemization](Design/Systems/Itemization.md):** Gear slots, Affix pools, Unique item design.
*   **[Loot Rules](Design/Systems/Loot_Table_Rules.md):** Drop buckets, Smart loot, Chest types.
*   **[Meta Progression](Design/Systems/Meta_Progression.md):** Skill tree (Constellation), Base building.

#### Content & World
*   **[Bestiary & AI](Design/Content/Enemy_Bestiary.md):** Monster hierarchy, AI archetypes, Affixes.
*   **[Level Design](Design/Content/Level_Design_Guide.md):** Map generation, Wave pacing, Map events.

#### Theory
*   **[Philosophy](Design/Philosophy_And_Systems.md):** Core loops, Player psychographics.
*   **[Case Studies](Design/Industry_CaseStudies.md):** Analysis of Diablo, PoE, Vampire Survivors.

---

### 2. 🛠️ Technical Architecture (The "Brain")
*   **[Save System](Tech/Save_System_Architecture.md):** Data structure, Serialization, Anti-cheat.
*   **[Performance Budget](Tech/Performance_Budget.md):** CPU/GPU limits, LOD policy for 60FPS.
*   **[Input System](Tech/Input_System_Design.md):** Action maps, Controller support, Accessibility.

---

### 3. 🎨 Art & Audio (The "Skin")
*   **[UI/UX Guidelines](Art/UI_UX_Guidelines.md):** Visual style, Layer hierarchy, Interaction feedback.
*   **[VFX Standards](Art/VFX_Standards.md):** Visual hierarchy, Color coding, Optimization.
*   **[Audio Guide](Audio/Practical_Guide.md):** Sound hierarchy, Mixing, Implementation tips.

---

### 4. 📋 Production & Standards (The "Law")
*   **[Documentation Roadmap](Design/Documentation_Roadmap.md):** The master plan for all docs.
*   **[Folder Structure](Unity_Standards/Folder_Structure.md):** Unity project organization.
*   **[Asset Naming](Unity_Standards/Asset_Naming.md):** Strict naming conventions (`T_`, `M_`, `P_`).
*   **[Asset Management](Unity_Standards/Asset_Management.md):** Import settings & best practices.
*   **[Production Lessons](Dev_Guides/Production_Lessons.md):** Post-mortem lessons to avoid failure.
*   **[Unity Tips](Dev_Guides/Unity_Practical_Tips.md):** Coding & Debugging tricks.

---

## 🚀 Quick Start

### 📊 Visualizing the Math
We have provided an interactive HTML dashboard to simulate and verify the numerical models without writing code.
1.  Locate **`Design/Calculator/index.html`** in this directory.
2.  Open it in any modern web browser (Chrome/Edge).

### 👮 Enforcing Standards
1.  Copy `Unity_Standards/Tools/AssetNamingValidator.cs` to your Unity project's `Assets/Editor` folder.
2.  It will automatically flag any asset that violates naming conventions.

---

## 🤖 AI Context
*   **[GEMINI.md](GEMINI.md)**: Summarizes the project context for AI agents.

---

*Project maintained by the Vampirefall Team.*