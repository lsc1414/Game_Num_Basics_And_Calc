---
description: Documentation Refactoring Workflow
---

# Documentation Refactoring Workflow

This workflow assists in restructuring large markdown files (>1000 lines) without losing content.

## Step 1: Structure Extraction

**User Action:** Open the markdown file you want to refactor (e.g., `original.md`).
**Agent Instruction:**

1.  Read the currently open file.
2.  Extract ONLY the headers (H1, H2, H3, H4) into a nested bulleted list.
3.  Create a NEW file named `_structure_plan.md` in the same directory.
4.  Write the extracted headers into `_structure_plan.md`.
5.  **Stop** and ask the user to rearrange the `_structure_plan.md` file to their desired order.

## Step 2: Content Migration (Run this after editing the plan)

**User Action:** Open the modified `_structure_plan.md` and type "Proceed".
**Agent Instruction:**

1.  Read `@_structure_plan.md` (the new structure) and `@original.md` (the source content).
2.  Create a NEW file named `_refactored_draft.md`.
3.  **CRITICAL RULE:** For each header in the plan, find the corresponding section in the source file and copy the content **verbatim**.
4.  **Do not summarize.** Keep all text, code blocks, images, and formatting exactly as they are.
5.  If a header was renamed in the plan, use the new name but copy the old content.
6.  If a header was deleted in the plan, skip that content.

## Step 3: Verification

**Agent Instruction:**

1.  Compare `@original.md` and `@_refactored_draft.md`.
2.  Report if any code blocks or large sections appear to be missing.
