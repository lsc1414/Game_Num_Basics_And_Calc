from __future__ import annotations

import argparse
import re
from pathlib import Path


SUMMARY_RE = re.compile(r"^>\s*\*\*摘要\*\*")
BOLD_QUOTE_RE = re.compile(r'^>\s*\*\*\s*["“].+["”]\s*\*\*.*$')
H2_RE = re.compile(r"^##\s+")


def find_header_intro_violations(text: str, max_lines: int = 30) -> list[tuple[int, str]]:
    lines = text.splitlines()
    head = lines[:max_lines]

    summary_index = -1
    for i, line in enumerate(head):
        if SUMMARY_RE.search(line):
            summary_index = i
            break
    if summary_index < 0:
        return []

    first_h2_index = len(head)
    for i in range(summary_index + 1, len(head)):
        if H2_RE.search(head[i]):
            first_h2_index = i
            break

    violations: list[tuple[int, str]] = []
    for i in range(summary_index + 1, first_h2_index):
        if BOLD_QUOTE_RE.search(head[i]):
            violations.append((i + 1, head[i]))
            break
    return violations


def find_header_separator_violations(text: str, max_lines: int = 30) -> list[tuple[int, str]]:
    lines = text.splitlines()
    head = lines[:max_lines]

    frontmatter_end = -1
    if head and head[0].strip() == "---":
        for i in range(1, len(head)):
            if head[i].strip() == "---":
                frontmatter_end = i
                break

    first_h2_index = len(head)
    for i, line in enumerate(head):
        if H2_RE.search(line):
            first_h2_index = i
            break

    violations: list[tuple[int, str]] = []
    for i in range(frontmatter_end + 1, first_h2_index):
        if head[i].strip() == "---":
            violations.append((i + 1, head[i]))
    return violations


def scan_docs(root: Path, max_lines: int = 30) -> list[tuple[Path, int, str]]:
    results: list[tuple[Path, int, str]] = []
    for md in root.rglob("*.md"):
        text = md.read_text(encoding="utf-8")
        for line_no, line in find_header_intro_violations(text, max_lines=max_lines):
            results.append((md, line_no, line))
    return results


def scan_header_separators(root: Path, max_lines: int = 30) -> list[tuple[Path, int, str]]:
    results: list[tuple[Path, int, str]] = []
    for md in root.rglob("*.md"):
        text = md.read_text(encoding="utf-8")
        for line_no, line in find_header_separator_violations(text, max_lines=max_lines):
            results.append((md, line_no, line))
    return results


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Check docs for style issue: summary followed by bold-quote intro title."
    )
    parser.add_argument("--root", default="docs", help="Docs root directory (default: docs)")
    parser.add_argument(
        "--max-lines",
        type=int,
        default=30,
        help="Only scan first N lines of each markdown file (default: 30)",
    )
    args = parser.parse_args()

    root = Path(args.root)
    if not root.exists():
        print(f"ERROR: root not found: {root}")
        return 2

    intro_violations = scan_docs(root, max_lines=args.max_lines)
    sep_violations = scan_header_separators(root, max_lines=args.max_lines)

    if not intro_violations and not sep_violations:
        print("OK: no intro-style violations found.")
        return 0

    total = len(intro_violations) + len(sep_violations)
    print(f"FOUND: {total} violation(s)")
    for path, line_no, line in intro_violations:
        print(f"{path}:{line_no}: {line}")
    for path, line_no, line in sep_violations:
        print(f"{path}:{line_no}: {line}")
    print('Hint1: replace `> **"..."**` with `> 引言：「...」` after a summary block.')
    print("Hint2: remove `---` between frontmatter and first `##` heading.")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
