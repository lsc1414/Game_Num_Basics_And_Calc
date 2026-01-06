---
description: Reorganize documentation index and navigation based on directory structure.
---

# Reorganize Documentation

This workflow scans the `docs/` directory, simplifies titles by removing English translations, and automatically updates both `mkdocs.yml` navigation and `docs/Full_Index.md`.

## Steps

1. Run the auto-organization script.
   // turbo

```bash
python scripts/auto_organize_docs.py
```

2. (Optional) Review the changes.
   - Check `mkdocs.yml` to see the new navigation structure.
   - Check `docs/Full_Index.md` to see the generated index.
