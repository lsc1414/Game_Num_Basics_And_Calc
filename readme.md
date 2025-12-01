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
*   **[Luban Config](Tech/Luban_Config_Guide.md):** Excel-to-Data workflow, ID conventions.
*   **[FSM Patterns](Tech/FSM_Design_Patterns.md):** State machines for AI and Towers.

---

### 3. 🎨 Art & Audio (The "Skin")
*   **[UI/UX Guidelines](Art/UI_UX_Guidelines.md):** Visual style, Layer hierarchy, Interaction feedback.
*   **[VFX Standards](Art/VFX_Standards.md):** Visual hierarchy, Color coding, Optimization.
*   **[Audio Guide](Audio/Practical_Guide.md):** Sound hierarchy, Mixing, Implementation tips.
*   **[Visual Quality](Art/Visual_Quality_Guide.md):** URP settings, Lighting, Post-processing.
*   **[Camera Guide](Art/Camera_DeepDive_And_Settings.md):** FOV, Cinemachine, Camera shake.

---

### 4. 🔧 Deep Dive & Implementation (The "Muscle")
#### Technical Implementation
*   **[ECS Optimization](Dev_Guides/Technical_Implementation/ECS_Performance_Optimization.md):** Handling 500+ units via DOTS/JobSystem.
*   **[GPU Instancing](Dev_Guides/Technical_Implementation/GPU_Instancing_Guide.md):** Rendering 10k+ sprites with 1 DrawCall.
*   **[Loot Reservoir](Dev_Guides/Technical_Implementation/Loot_Reservoir_Algorithm.md):** 0GC drop system with constant DPM.
*   **[Game Analytics](Dev_Guides/Technical_Implementation/Game_Analytics_Guide.md):** Telemetry, Funnels, Anti-cheat monitoring.

#### Industry Case Studies
*   **[Kingdom Rush](Dev_Guides/Industry_Cases/Kingdom_Rush_Numerical_Model.md):** The 4-Axis numerical balance model.
*   **[Hades](Dev_Guides/Industry_Cases/Hades_Build_Diversity.md):** Dual-layer Tag system & Duo Boons.
*   **[Vampire Survivors](Dev_Guides/Industry_Cases/Vampire_Survivors_Performance.md):** Optimization secrets (Gem merging).
*   **[Bloons TD6](Dev_Guides/Industry_Cases/Bloons_TD6_Damage_Matrix.md):** Damage types vs Defense types matrix.

#### Failure Analysis
*   **[Battleborn](Dev_Guides/Failure_Cases/Battleborn_Failure_Analysis.md):** Visual clutter & TTK identity crisis.
*   **[Paragon](Dev_Guides/Failure_Cases/Paragon_Complexity_Trap.md):** The "Z-Axis" trap in strategic games.

---

### 5. 🤝 Collaboration & Production (The "Workflow")
*   **[Agile for Indie](Dev_Guides/Collaboration/Agile_For_Indie_Teams.md):** Lightweight Scrum for small teams.
*   **[Remote Work](Dev_Guides/Collaboration/Remote_Collaboration.md):** Async workflow & Golden Hours.
*   **[Milestones](Dev_Guides/Collaboration/Milestone_Planning.md):** Vertical Slice -> Alpha -> Gold roadmap.
*   **[Beta Testing](Dev_Guides/Collaboration/Beta_Testing_Guide.md):** Steam Playtest & Feedback triage.

---

### 6. 🛠️ Tools & Standards (The "Law")
*   **[Documentation Roadmap](Design/Documentation_Roadmap.md):** The master plan for all docs.
*   **[Folder Structure](Unity_Standards/Folder_Structure.md):** Unity project organization.
*   **[Asset Naming](Unity_Standards/Asset_Naming.md):** Strict naming conventions (`T_`, `M_`, `P_`).
*   **[Asset Management](Unity_Standards/Asset_Management.md):** Import settings & best practices.
*   **[Unity PRD Plugin](Dev_Guides/Tools/Unity_PRD_Plugin.md):** C# implementation of Pseudo-Random Distribution.
*   **[AI Balance Tool](Dev_Guides/Tools/AI_Balance_Testing.md):** Automated testing via LLM.
*   **[Combat Sim](Dev_Guides/Tools/Combat_Simulation_System.md):** Python headless battle simulator.
*   **[Perf Monitor](Dev_Guides/Tools/Performance_Monitoring_Scripts.md):** Runtime FPS/Memory HUD.
*   **[Calculators](Dev_Guides/Tools/Numerical_Calculator_Suite.md):** TTK, EHP, and Economy tools.

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