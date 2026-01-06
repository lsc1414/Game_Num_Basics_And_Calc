---
description: Run the MkDocs Markdown linter to check and fix syntax issues
---

# MkDocs Markdown Lint and Fix

This workflow uses the `mkdocs_lint_fix.py` script to automatically check and fix Markdown syntax issues for MkDocs compatibility.

## Steps

// turbo

1. **Preview changes (dry-run):**

   ```bash
   python scripts/mkdocs_lint_fix.py --all --dry-run
   ```

   Review the output to see what changes will be made.

2. **Apply fixes to all files:**

   ```bash
   python scripts/mkdocs_lint_fix.py --all
   ```

3. **(Optional) Fix a specific file:**
   ```bash
   python scripts/mkdocs_lint_fix.py <path/to/file.md>
   ```

## What Gets Fixed

| Category        | Issues                                                                                                       |
| --------------- | ------------------------------------------------------------------------------------------------------------ |
| **Math**        | Indented `$$` blocks, escaped subscripts (`UV\_{new}`), malformed subscripts (`A*{up}`), function formatting |
| **Tables**      | Inconsistent column counts, missing blank lines before tables                                                |
| **Icons**       | Problematic Unicode symbols (↝, ╭, ᵕ) replaced with safe alternatives                                        |
| **Inline Math** | Missing spaces in `$...$`                                                                                    |

## After Running

Verify changes with:

```bash
mkdocs serve
```
