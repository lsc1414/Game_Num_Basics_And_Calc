#!/usr/bin/env python3
"""
run_low_token_pipeline.py

One-command low-token docs pipeline:
1) incremental dedupe scan (with cache)
2) optional plan update
3) reorganize docs (dry-run by default)
4) optional nav/index refresh
5) optional token audit snapshot

Usage:
  python scripts/run_low_token_pipeline.py
  python scripts/run_low_token_pipeline.py --apply --delete-sources
  python scripts/run_low_token_pipeline.py --changed-list reports/changed_docs.txt
"""

import argparse
import subprocess
import sys
from pathlib import Path


def run(cmd):
    print("$ " + " ".join(cmd))
    subprocess.check_call(cmd)


def main() -> None:
    parser = argparse.ArgumentParser(description="Run low-token docs maintenance pipeline.")
    parser.add_argument("--docs", default="docs", help="Docs directory path.")
    parser.add_argument("--plan", default="scripts/doc_reorganize_plan.json", help="Reorganize plan json.")
    parser.add_argument("--out", default="reports/dedupe_candidates_incremental.json", help="Dedupe output json.")
    parser.add_argument("--cache", default="reports/dedupe_cache.json", help="Dedupe cache json.")
    parser.add_argument("--min-score", type=float, default=0.35, help="Similarity threshold.")
    parser.add_argument("--changed-list", help="Optional changed file list.")
    parser.add_argument("--update-plan", action="store_true", help="Append candidates into plan merges.")
    parser.add_argument("--apply", action="store_true", help="Apply mutations. Default is dry-run.")
    parser.add_argument("--delete-sources", action="store_true", help="Delete merged source docs.")
    parser.add_argument("--refresh-nav", action="store_true", help="Run nav/index refresh scripts.")
    parser.add_argument("--token-audit", action="store_true", help="Write token audit snapshot after pipeline.")
    args = parser.parse_args()

    py = sys.executable

    scan_cmd = [
        py,
        "scripts/dedupe_scan.py",
        "--docs",
        args.docs,
        "--out",
        args.out,
        "--min-score",
        str(args.min_score),
        "--incremental",
        "--cache",
        args.cache,
    ]
    if args.changed_list:
        scan_cmd.extend(["--changed-list", args.changed_list])
    if args.update_plan:
        scan_cmd.extend(["--update-plan", args.plan])
    run(scan_cmd)

    reorg_cmd = [py, "scripts/reorganize_docs.py", "--plan", args.plan, "--minimal-report"]
    if args.apply:
        reorg_cmd.append("--apply")
    else:
        reorg_cmd.append("--dry-run")
    if args.delete_sources:
        reorg_cmd.append("--delete-sources")
    run(reorg_cmd)

    if args.refresh_nav and args.apply:
        run([py, "scripts/auto_organize_docs.py"])
        run([py, "scripts/generate_full_index.py"])

    if args.token_audit:
        run([py, "scripts/token_audit.py", "--docs", args.docs, "--out", "reports/token_snapshot.json", "--top", "20"])

    print("pipeline_done")


if __name__ == "__main__":
    main()
