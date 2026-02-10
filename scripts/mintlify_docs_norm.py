#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
from dataclasses import dataclass
from pathlib import Path


FM_LINE_RE = re.compile(r"^([A-Za-z][A-Za-z0-9_-]*)\s*:\s*(.*)$")
H1_RE = re.compile(r"^#\s+(.+?)\s*$")
MD_LINK_RE = re.compile(r"(?<!!)\[([^\]]+)\]\(([^)\s]+\.md)(#[^)]+)?\)")


@dataclass
class Stats:
    total: int = 0
    changed: int = 0
    invalid_frontmatter: int = 0
    fixed_frontmatter: int = 0
    fixed_links: int = 0


def unquote(value: str) -> str:
    v = value.strip()
    if len(v) >= 2 and ((v[0] == '"' and v[-1] == '"') or (v[0] == "'" and v[-1] == "'")):
        return v[1:-1].strip()
    return v


def quote(value: str) -> str:
    return '"' + value.replace('"', '\\"') + '"'


def has_meaningful_text(value: str) -> bool:
    if not value.strip():
        return False
    return not re.fullmatch(r"[\\\"'\s]+", value.strip())


def derive_title_from_body(body_lines: list[str], file_path: Path) -> str:
    for line in body_lines:
        m = H1_RE.match(line)
        if m:
            return m.group(1).strip()
    return file_path.stem.replace("_", " ").strip()


def derive_sidebar_from_title(title: str) -> str:
    sidebar = re.sub(r"^[^\w\u4e00-\u9fff]+", "", title).strip()
    return sidebar or title


def split_frontmatter(raw: str) -> tuple[bool, list[str], list[str]]:
    lines = raw.splitlines()
    if len(lines) >= 3 and lines[0].strip() == "---":
        for i in range(1, len(lines)):
            if lines[i].strip() == "---":
                return True, lines[1:i], lines[i + 1 :]
    return False, [], lines


def normalize_links(text: str) -> tuple[str, int]:
    count = 0

    def repl(m: re.Match[str]) -> str:
        nonlocal count
        label, link, anchor = m.group(1), m.group(2), m.group(3) or ""
        fixed = re.sub(r"\.md$", "", link, flags=re.IGNORECASE)
        if fixed != link:
            count += 1
        return f"[{label}]({fixed}{anchor})"

    return MD_LINK_RE.sub(repl, text), count


def normalize_file(path: Path, fix: bool, normalize_md_links: bool) -> tuple[bool, int, bool]:
    raw = path.read_text(encoding="utf-8")
    has_bom = raw.startswith("\ufeff")
    if has_bom:
        raw = raw.lstrip("\ufeff")

    has_frontmatter, fm_lines, body_lines = split_frontmatter(raw)
    changed = False
    fixed_links = 0
    frontmatter_invalid = False

    other_fm: list[str] = []
    title = ""
    sidebar = ""

    if has_frontmatter:
        for line in fm_lines:
            m = FM_LINE_RE.match(line)
            if not m:
                if line.strip():
                    other_fm.append(line)
                continue
            key, raw_value = m.group(1), m.group(2)
            value = unquote(raw_value)
            if key == "title":
                if has_meaningful_text(value):
                    title = value
            elif key == "sidebarTitle":
                if has_meaningful_text(value):
                    sidebar = value
            else:
                other_fm.append(f"{key}: {raw_value.strip()}")
    else:
        frontmatter_invalid = True

    derived_title = derive_title_from_body(body_lines, path)
    needs_fm_fix = (not has_frontmatter)

    if not has_meaningful_text(title):
        title = derived_title
        needs_fm_fix = True
        frontmatter_invalid = True

    if not has_meaningful_text(sidebar):
        sidebar = derive_sidebar_from_title(title)
        needs_fm_fix = True
        frontmatter_invalid = True

    new_body = body_lines[:]

    if normalize_md_links:
        body_text = "\n".join(new_body)
        body_text2, fixed_links = normalize_links(body_text)
        if body_text2 != body_text:
            changed = True
            new_body = body_text2.splitlines()

    if not needs_fm_fix and not changed:
        return False, 0, frontmatter_invalid

    if needs_fm_fix:
        fm_payload = [f"sidebarTitle: {quote(sidebar)}", f"title: {quote(title)}", *other_fm]
        changed = True
    else:
        fm_payload = fm_lines[:]

    newline = "\r\n" if "\r\n" in raw else "\n"
    new_lines = ["---", *fm_payload, "---", "", *new_body]
    new_content = newline.join(new_lines).rstrip() + newline

    if changed and fix:
        out = ("\ufeff" if has_bom else "") + new_content
        path.write_text(out, encoding="utf-8")

    return changed, fixed_links, frontmatter_invalid


def main() -> int:
    parser = argparse.ArgumentParser(description="Normalize docs/**/*.md for Mintlify.")
    parser.add_argument("--docs-dir", default="docs", help="Docs root directory (default: docs)")
    parser.add_argument("--fix", action="store_true", help="Write changes to files")
    parser.add_argument("--check", action="store_true", help="Check only and return non-zero if issues found")
    parser.add_argument(
        "--normalize-md-links",
        action="store_true",
        help="Also convert relative links like (foo.md) to (foo)",
    )
    args = parser.parse_args()

    docs_dir = Path(args.docs_dir)
    if not docs_dir.exists():
        print(f"[ERROR] docs dir not found: {docs_dir}")
        return 2

    stats = Stats()
    for file_path in sorted(docs_dir.rglob("*.md")):
        stats.total += 1
        changed, link_count, fm_invalid = normalize_file(
            file_path,
            fix=args.fix,
            normalize_md_links=args.normalize_md_links,
        )
        if changed:
            stats.changed += 1
            if link_count:
                stats.fixed_links += link_count
            if fm_invalid:
                stats.fixed_frontmatter += 1
            if args.check and not args.fix:
                rel = file_path.as_posix()
                print(f"[NEEDS_FIX] {rel}")
        if fm_invalid:
            stats.invalid_frontmatter += 1

    print(f"total={stats.total}")
    print(f"changed={stats.changed}")
    print(f"frontmatter_issues={stats.invalid_frontmatter}")
    print(f"frontmatter_fixed={stats.fixed_frontmatter}")
    if args.normalize_md_links:
        print(f"md_links_fixed={stats.fixed_links}")

    if args.check and stats.changed > 0 and not args.fix:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
