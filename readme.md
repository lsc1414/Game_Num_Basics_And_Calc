# 🏰 Project Vampirefall - Server & Numerical Core

[English Version](README.md) | [中文版本](README_CN.md)

Welcome to the core design and calculation repository for **Project Vampirefall**.
This project is a hybrid game combining **Tower Defense**, **Roguelike**, and **Looter** mechanics, inspired by titles like *Path of Exile*, *Vampire Survivors*, and *GemCraft*.

This directory serves as the "Brain" of the project, containing the mathematical models, design philosophies, and technical standards that drive the game's balance and architecture.

---

## 📚 Documentation Map

### 1. 🧠 Design & Mathematics (The "Why" & "How")
*   **[Numerical Design Manual](Numerical_Design_Manual.md)** (Renamed from old readme)
    *   **What is it?** The "Bible" of the game's math.
    *   **Contents:** Damage formulas, PRD algorithms, Armor vs. Dodge curves, Loot bucket logic.
    *   **Target Audience:** Systems Designers, Gameplay Programmers.

*   **[Game Design Philosophy](GameDesign_Philosophy_And_Systems.md)**
    *   **What is it?** The theory of "Fun".
    *   **Contents:** Core Loops, Synergy (1+1>2), Pacing Control, Player Psychographics.
    *   **Target Audience:** All Designers.

*   **[Industry Case Studies](IndustryCaseStudies.md)**
    *   **What is it?** A library of mechanics from top-tier games (Diablo, Genshin, Warframe).
    *   **Contents:** Analysis of why specific mechanics work and how to adapt them.

### 2. 🛠️ Technical Implementation (The "Code")
*   **[Unity Practical Dev Tips](Unity_Practical_Dev_Tips.md)**
    *   **Contents:** Performance optimization (Pooling, Batching), Architecture (EventBus, SO), and Debugging tricks.
    *   **Target:** Client Programmers.

*   **[Unity Asset Management](Unity_Asset_Management_Tips.md)**
    *   **Contents:** Import settings, Addressables vs. Resources, and Git LFS handling.
    *   **Target:** Tech Artists, Programmers.

*   **[Asset Naming Standards](AssetNaming_Standards.md)**
    *   **Contents:** Strict naming conventions (`T_`, `M_`, `P_`) to keep the project organized.
    *   **Tool:** Includes a link to the `AssetNamingValidator.cs` script.

*   **[Folder Structure Standards](Unity_Folder_Structure_Standards.md)**
    *   **Contents:** The "Hybrid" folder structure (`Features/` vs `Art/`) for modular development.

### 3. ☠️ Production Survival Guide
*   **[Game Dev Post-Mortem Lessons](GameDev_Production_Lessons.md)**
    *   **Contents:** A collection of painful lessons on Scope Creep, Localization, UI/UX, and Marketing. Read this to avoid cancelling the project.

---

## 🚀 Quick Start

### 📊 Visualizing the Math
We have provided an interactive HTML dashboard to simulate and verify the numerical models without writing code.
1.  Locate **`index.html`** in this directory.
2.  Open it in any modern web browser (Chrome/Edge).
3.  Use it to calculate:
    *   **DPS Expectations:** See how `Inc` vs `More` affects output.
    *   **Defense Curves:** Visualize Linear Armor vs. Exponential Dodge.
    *   **PRD Stability:** Compare True Random vs. Pseudo-Random variance.

### 👮 Enforcing Standards
To ensure the project stays clean:
1.  Copy `AssetNamingValidator.cs` to your Unity project's `Assets/Editor` folder.
2.  It will automatically flag any asset that violates the naming conventions defined in `AssetNaming_Standards.md`.

---

## 🤖 AI Context
*   **[GEMINI.md](GEMINI.md)**: This file is generated for the AI agent to understand the project context quickly. It summarizes the directory structure and key file contents.

---

*Project maintained by the Vampirefall Team.*