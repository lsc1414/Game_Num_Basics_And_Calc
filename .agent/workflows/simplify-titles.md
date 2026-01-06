---
description: Simplify Titles Workflow
---

# Simplify Titles Workflow

This workflow simplifies the titles in `mkdocs.yml` and `docs/Full_Index.md` by removing the English translation part (text within parentheses at the end of the title) to make the index cleaner.

## Prerequisites

- Python 3.x

## Usage

Run the following command in the project root:

```bash
python scripts/simplify_titles.py
```

## What it does

1.  **mkdocs.yml**: Scans the `nav` section. If a title ends with `(English Text)`, it removes the `(English Text)` part. It preserves titles like `Art (美术)` where the text in parentheses contains Chinese characters.
2.  **docs/Full_Index.md**: Scans headers and links. Applies the same title cleaning logic.
