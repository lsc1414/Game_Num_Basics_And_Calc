#!/usr/bin/env python3
"""
Check Mintlify markdown title/frontmatter consistency.

Rules checked:
1) frontmatter must be the first block when present
2) top frontmatter must not contain `title:`
3) each markdown file should have exactly one H1 (`# ...`)
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


FM_RE = re.compile(r"^---\r?\n(?P<fm>.*?)\r?\n---", re.S)
H1_RE = re.compile(r"(?m)^#\s+.+$")
TITLE_RE = re.compile(r"(?m)^\s*title\s*:")
SIDEBAR_RE = re.compile(r"(?m)^\s*sidebarTitle\s*:")


def list_markdown_files(docs_dir: Path) -> list[Path]:
    return [p for p in docs_dir.rglob("*.md") if ".vitepress" not in p.parts]


def check_file(path: Path) -> list[str]:
    issues: list[str] = []
    raw = path.read_text(encoding="utf-8", errors="strict")
    text = raw.lstrip("\ufeff")
    top_match = FM_RE.match(text)
    has_top_fm = bool(top_match)

    # If title/sidebar exists anywhere but file does not start with frontmatter,
    # this is likely an embedded/incorrect frontmatter block.
    has_title_anywhere = bool(TITLE_RE.search(text))
    has_sidebar_anywhere = bool(SIDEBAR_RE.search(text))
    if (has_title_anywhere or has_sidebar_anywhere) and not has_top_fm:
        issues.append("frontmatter_not_at_top")

    if top_match:
        fm = top_match.group("fm")
        if TITLE_RE.search(fm):
            issues.append("top_frontmatter_contains_title")

    h1_count = len(H1_RE.findall(text))
    if h1_count != 1:
        issues.append(f"h1_count_{h1_count}")

    return issues


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--docs-dir", default="docs", help="docs root directory")
    args = parser.parse_args()

    docs_dir = Path(args.docs_dir).resolve()
    if not docs_dir.exists():
        print(f"[ERROR] docs dir not found: {docs_dir}")
        return 2

    files = list_markdown_files(docs_dir)
    bad = 0
    for f in files:
        issues = check_file(f)
        if issues:
            bad += 1
            rel = f.relative_to(Path.cwd())
            print(f"{rel} :: {', '.join(issues)}")

    print(f"SCANNED={len(files)} BAD={bad}")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
