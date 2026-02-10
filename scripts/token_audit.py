#!/usr/bin/env python3
"""
token_audit.py

Estimate token footprint for docs markdown files and write a JSON report.

Usage:
    python scripts/token_audit.py --docs docs --out reports/token_before.json
"""

import argparse
import json
from pathlib import Path


IGNORED_DIRS = {".vitepress", "assets", "stylesheets", "javascripts"}


def estimate_tokens(text: str) -> int:
    # Fast mixed-language heuristic used for relative comparison.
    return int(len(text) / 1.6)


def should_skip(path: Path) -> bool:
    return any(part in IGNORED_DIRS for part in path.parts)


def main() -> None:
    parser = argparse.ArgumentParser(description="Audit markdown token footprint.")
    parser.add_argument("--docs", default="docs", help="Docs directory path.")
    parser.add_argument("--out", required=True, help="Output json path.")
    parser.add_argument("--top", type=int, default=30, help="Top heavy files to store.")
    args = parser.parse_args()

    docs_dir = Path(args.docs)
    out_path = Path(args.out)

    files = []
    total_tokens = 0
    total_chars = 0

    for md in docs_dir.rglob("*.md"):
        if should_skip(md):
            continue
        text = md.read_text(encoding="utf-8", errors="ignore")
        chars = len(text)
        tokens = estimate_tokens(text)
        files.append(
            {
                "path": md.as_posix(),
                "chars": chars,
                "tokens_est": tokens,
                "lines": text.count("\n") + 1,
            }
        )
        total_chars += chars
        total_tokens += tokens

    files.sort(key=lambda item: item["tokens_est"], reverse=True)

    report = {
        "docs_dir": docs_dir.as_posix(),
        "file_count": len(files),
        "total_chars": total_chars,
        "total_tokens_est": total_tokens,
        "avg_tokens_est": int(total_tokens / len(files)) if files else 0,
        "top_heavy_files": files[: args.top],
    }

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Saved token audit to: {out_path.as_posix()}")
    print(f"Files: {report['file_count']}, tokens_est: {report['total_tokens_est']}")


if __name__ == "__main__":
    main()
