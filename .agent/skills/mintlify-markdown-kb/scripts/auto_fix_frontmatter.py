#!/usr/bin/env python3
"""
Auto-fix mechanical frontmatter issues for Mintlify markdown files.

What this script does:
1) Find metadata frontmatter blocks anywhere in file body
2) Build a single canonical top frontmatter block
3) Remove duplicate embedded metadata frontmatter blocks
4) Drop `title:` from frontmatter (repo rule: H1 is the page title)

What this script does NOT do:
- Rewrite content structure
- Reduce multiple H1 sections
- Edit semantic text
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path


FM_BLOCK_RE = re.compile(r"(?ms)^---\r?\n(?P<fm>.*?)\r?\n---\s*")
KEY_RE = re.compile(r"(?m)^\s*(sidebarTitle|description|icon|title)\s*:")
LINE_RE = re.compile(r"(?m)^\s*([A-Za-z_][A-Za-z0-9_]*)\s*:\s*(.*)$")
TOP_FM_RE = re.compile(r"^---\r?\n(?P<fm>.*?)\r?\n---\s*", re.S)

KEEP_KEYS = ("sidebarTitle", "description", "icon")


def markdown_files(docs_dir: Path) -> list[Path]:
    return [p for p in docs_dir.rglob("*.md") if ".vitepress" not in p.parts]


def split_lines(text: str) -> tuple[str, list[str]]:
    nl = "\r\n" if "\r\n" in text else "\n"
    return nl, text.splitlines()


def parse_kv(fm_text: str) -> dict[str, str]:
    out: dict[str, str] = {}
    for m in LINE_RE.finditer(fm_text):
        k, v = m.group(1), m.group(2).strip()
        if k in KEEP_KEYS:
            out[k] = v
    return out


def build_fm(nl: str, kv: dict[str, str]) -> str:
    lines: list[str] = []
    for k in KEEP_KEYS:
        if k in kv and kv[k] != "":
            lines.append(f"{k}: {kv[k]}")
    if not lines:
        return ""
    return f"---{nl}" + nl.join(lines) + f"{nl}---{nl}{nl}"


def read_text_with_bom(path: Path) -> tuple[str, bool]:
    data = path.read_bytes()
    has_bom = data.startswith(b"\xef\xbb\xbf")
    text = data.decode("utf-8", errors="strict")
    return text, has_bom


def write_text_with_bom(path: Path, text: str, has_bom: bool) -> None:
    encoded = text.encode("utf-8-sig" if has_bom else "utf-8")
    path.write_bytes(encoded)


def fix_one(path: Path) -> bool:
    original, has_bom = read_text_with_bom(path)
    original = original.lstrip("\ufeff")
    nl, _ = split_lines(original)

    text = original
    top_m = TOP_FM_RE.match(text)

    top_kv: dict[str, str] = {}
    body = text
    if top_m:
        top_fm = top_m.group("fm")
        top_kv = parse_kv(top_fm)
        body = text[top_m.end() :]

    # collect metadata-like frontmatter blocks from body
    body_blocks = list(FM_BLOCK_RE.finditer(body))
    embedded_meta_blocks = [m for m in body_blocks if KEY_RE.search(m.group("fm"))]

    merged = dict(top_kv)
    if not merged and embedded_meta_blocks:
        merged.update(parse_kv(embedded_meta_blocks[0].group("fm")))

    # remove all embedded metadata frontmatter blocks
    if embedded_meta_blocks:
        parts: list[str] = []
        last = 0
        for m in embedded_meta_blocks:
            parts.append(body[last : m.start()])
            last = m.end()
        parts.append(body[last:])
        body = "".join(parts)

    new_top = build_fm(nl, merged)
    new_text = new_top + body.lstrip("\r\n")

    if new_text != original:
        write_text_with_bom(path, new_text, has_bom)
        return True
    return False


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--docs-dir", default="docs")
    args = parser.parse_args()

    docs_dir = Path(args.docs_dir).resolve()
    files = markdown_files(docs_dir)

    changed = 0
    for f in files:
        if fix_one(f):
            changed += 1
            print(f"FIXED {f}")

    print(f"SCANNED={len(files)} CHANGED={changed}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
