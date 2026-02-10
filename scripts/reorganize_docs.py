#!/usr/bin/env python3
"""
reorganize_docs.py

Apply doc reorganization plan:
- create directories
- move files
- merge files
- update docs.json references
- optional source deletion for merged docs

Usage:
    python scripts/reorganize_docs.py --dry-run
    python scripts/reorganize_docs.py --apply
    python scripts/reorganize_docs.py --plan scripts/doc_reorganize_plan.json --apply --delete-sources
"""

import argparse
import io
import json
import re
import shutil
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Tuple

# Windows console UTF-8 support
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")


def create_directories(docs_path: Path, directories: List[str], dry_run: bool) -> int:
    created = 0
    for dir_name in directories:
        dir_path = docs_path / dir_name
        if dir_path.exists():
            continue
        if dry_run:
            print(f"  [DRY-RUN] 创建目录: {dir_name}")
        else:
            dir_path.mkdir(parents=True, exist_ok=True)
            print(f"  ✓ 创建目录: {dir_name}")
        created += 1
    return created


def move_files(docs_path: Path, moves: List[Dict], dry_run: bool, minimal_report: bool) -> Tuple[int, List[Dict]]:
    moved = 0
    applied_moves = []
    for move in moves:
        src = docs_path / move["source"]
        dst = docs_path / move["destination"]
        if not src.exists():
            if not minimal_report:
                print(f"  ⚠️ 源文件不存在: {move['source']}")
            continue
        if dst.exists():
            if not minimal_report:
                print(f"  ⚠️ 目标已存在，跳过: {move['destination']}")
            continue
        if dry_run:
            if not minimal_report:
                print(f"  [DRY-RUN] 移动: {move['source']}")
                print(f"          → {move['destination']}")
        else:
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(src), str(dst))
            if not minimal_report:
                print(f"  ✓ 移动: {move['source']}")
                print(f"       → {move['destination']}")
        moved += 1
        applied_moves.append(move)
    return moved, applied_moves


def extract_title_from_md(file_path: Path) -> str:
    try:
        content = file_path.read_text(encoding="utf-8")
        match = re.search(r"^#\s+(.+)$", content, re.MULTILINE)
        return match.group(1).strip() if match else file_path.stem
    except Exception:
        return file_path.stem


def _promote_first_h1_to_h2(content: str) -> str:
    return re.sub(r"^#\s+(.+)$", r"## \1", content, count=1, flags=re.MULTILINE)


def merge_files(
    docs_path: Path, merges: List[Dict], dry_run: bool, delete_sources: bool, minimal_report: bool
) -> Tuple[int, List[Dict], List[Dict]]:
    merged = 0
    applied_merges = []
    deleted_sources = []

    for merge in merges:
        target = docs_path / merge["target"]
        source_paths = [docs_path / src for src in merge.get("sources", [])]
        existing_sources = [src for src in source_paths if src.exists()]

        if len(existing_sources) < 2:
            if not minimal_report:
                print(f"  ⚠️ 合并组 '{merge.get('name', merge['target'])}' 源文件不足，跳过")
            continue

        if dry_run:
            if not minimal_report:
                print(f"\n  [DRY-RUN] 合并 '{merge.get('name', merge['target'])}':")
                for src in existing_sources:
                    print(f"    - {src.relative_to(docs_path)} ({extract_title_from_md(src)})")
                print(f"    → {merge['target']}")
                if delete_sources:
                    print("    [DRY-RUN] 合并后删除源文件")
            merged += 1
            applied_merges.append(merge)
            continue

        merged_content = []
        h1_title = merge.get("name", target.stem).replace("合并", "综合指南")
        merged_content.append(f"# {h1_title}\n")
        merged_content.append(f"> 本文档由以下文件合并生成 ({datetime.now().strftime('%Y-%m-%d')})\n")
        merged_content.append("")

        for src in existing_sources:
            content = src.read_text(encoding="utf-8")
            content = _promote_first_h1_to_h2(content)
            merged_content.append("\n---\n")
            merged_content.append(f"\n<!-- 来源: {src.relative_to(docs_path)} -->\n")
            merged_content.append(content)
            merged_content.append("\n")

        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text("\n".join(merged_content), encoding="utf-8")

        if not minimal_report:
            print(f"\n  ✓ 合并 '{merge.get('name', merge['target'])}':")
            for src in existing_sources:
                print(f"    - {src.relative_to(docs_path)}")
            print(f"    → {merge['target']}")

        if delete_sources:
            keep = target.resolve()
            for src in existing_sources:
                if src.resolve() == keep:
                    continue
                if src.exists():
                    src.unlink()
                    deleted_sources.append(
                        {
                            "source": str(src.relative_to(docs_path)).replace("\\", "/"),
                            "target": merge["target"],
                        }
                    )
                    if not minimal_report:
                        print(f"      删除源文件: {src.relative_to(docs_path)}")

        merged += 1
        applied_merges.append(merge)

    return merged, applied_merges, deleted_sources


def _dedupe_pages_node(node, seen_global=None):
    if seen_global is None:
        seen_global = set()
    if isinstance(node, dict):
        for key, value in list(node.items()):
            if key == "pages" and isinstance(value, list):
                deduped = []
                for item in value:
                    token = json.dumps(item, ensure_ascii=False, sort_keys=True)
                    if token in seen_global:
                        continue
                    seen_global.add(token)
                    deduped.append(item)
                node[key] = deduped
            else:
                _dedupe_pages_node(value, seen_global)
    elif isinstance(node, list):
        for item in node:
            _dedupe_pages_node(item, seen_global)


def update_docs_json(
    project_root: Path,
    applied_moves: List[Dict],
    applied_merges: List[Dict],
    dry_run: bool,
    minimal_report: bool,
) -> Dict[str, int]:
    docs_json_path = project_root / "docs.json"
    stats = {"path_rewrites": 0, "duplicate_pages_removed": 0}

    if not docs_json_path.exists():
        if not minimal_report:
            print("  ⚠️ docs.json 不存在，跳过更新")
        return stats

    obj = json.loads(docs_json_path.read_text(encoding="utf-8"))

    rewrite_map = {}
    for move in applied_moves:
        old_path = "docs/" + move["source"].replace(".md", "")
        new_path = "docs/" + move["destination"].replace(".md", "")
        rewrite_map[old_path] = new_path

    for merge in applied_merges:
        target = "docs/" + merge["target"].replace(".md", "")
        for src in merge.get("sources", []):
            src_ref = "docs/" + src.replace(".md", "")
            if src_ref != target:
                rewrite_map[src_ref] = target

    raw_before = json.dumps(obj, ensure_ascii=False)
    for old, new in rewrite_map.items():
        if old in raw_before:
            stats["path_rewrites"] += raw_before.count(f"\"{old}\"")
            raw_before = raw_before.replace(f"\"{old}\"", f"\"{new}\"")
    obj = json.loads(raw_before)

    nav = obj.get("navigation", {})
    before_nav = json.dumps(nav, ensure_ascii=False, sort_keys=True)
    _dedupe_pages_node(nav)
    after_nav = json.dumps(nav, ensure_ascii=False, sort_keys=True)
    if before_nav != after_nav:
        # Best-effort count: compare number of "docs/" page refs.
        stats["duplicate_pages_removed"] = before_nav.count('"docs/') - after_nav.count('"docs/')
    obj["navigation"] = nav

    if dry_run:
        if stats["path_rewrites"] or stats["duplicate_pages_removed"]:
            if not minimal_report:
                print(
                    f"\n  [DRY-RUN] docs.json 将更新路径 {stats['path_rewrites']} 处, 去重页面引用 {stats['duplicate_pages_removed']} 处"
                )
        return stats

    docs_json_path.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if not minimal_report:
        print(
            f"\n  ✓ docs.json 已更新: 路径 {stats['path_rewrites']} 处, 去重页面引用 {stats['duplicate_pages_removed']} 处"
        )
    return stats


def write_merge_report(
    project_root: Path,
    dry_run: bool,
    plan_path: Path,
    applied_moves: List[Dict],
    applied_merges: List[Dict],
    deleted_sources: List[Dict],
    docs_json_stats: Dict[str, int],
    minimal_report: bool,
) -> None:
    report_dir = project_root / "reports"
    report_path = report_dir / "merge_report.md"

    lines = []
    lines.append("# 文档重组报告")
    lines.append("")
    lines.append(f"- 时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append(f"- 模式: {'DRY-RUN' if dry_run else 'APPLY'}")
    lines.append(f"- 计划文件: `{plan_path.as_posix()}`")
    lines.append(f"- 移动文件: {len(applied_moves)}")
    lines.append(f"- 合并分组: {len(applied_merges)}")
    lines.append(f"- 删除源文件: {len(deleted_sources)}")
    lines.append(f"- docs.json 路径改写: {docs_json_stats.get('path_rewrites', 0)}")
    lines.append(f"- docs.json 页面去重: {docs_json_stats.get('duplicate_pages_removed', 0)}")
    lines.append("")

    if deleted_sources and not minimal_report:
        lines.append("## 删除源文件映射")
        lines.append("")
        for row in deleted_sources:
            lines.append(f"- `{row['source']}` -> `{row['target']}`")
        lines.append("")

    if not dry_run:
        report_dir.mkdir(parents=True, exist_ok=True)
        report_path.write_text("\n".join(lines), encoding="utf-8")
        if not minimal_report:
            print(f"\n  ✓ 报告已生成: {report_path.as_posix()}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Reorganize docs using JSON plan.")
    parser.add_argument("--plan", default="scripts/doc_reorganize_plan.json", help="Plan json path.")
    parser.add_argument("--dry-run", action="store_true", help="Preview changes only.")
    parser.add_argument("--apply", action="store_true", help="Apply changes.")
    parser.add_argument("--moves-only", action="store_true", help="Only apply file moves.")
    parser.add_argument("--merge-only", action="store_true", help="Only apply file merges.")
    parser.add_argument("--delete-sources", action="store_true", help="Delete merge source files.")
    parser.add_argument("--minimal-report", action="store_true", help="Print and write summary-only report.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    dry_run = args.dry_run or not args.apply

    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    docs_path = project_root / "docs"
    plan_path = (project_root / args.plan).resolve() if not Path(args.plan).is_absolute() else Path(args.plan)

    if not plan_path.exists():
        print(f"❌ 找不到重组计划: {plan_path.as_posix()}")
        sys.exit(1)

    plan = json.loads(plan_path.read_text(encoding="utf-8"))

    print("=" * 64)
    print("📋 文档重组预览 [DRY-RUN]" if dry_run else "🚀 执行文档重组")
    print("=" * 64)
    if not args.minimal_report:
        print(f"计划文件: {plan_path.as_posix()}")

    applied_moves = []
    applied_merges = []
    deleted_sources = []

    if not args.merge_only:
        if not args.minimal_report:
            print("\n📁 步骤 1: 创建新目录")
        created = create_directories(docs_path, plan.get("new_directories", []), dry_run)
        if not args.minimal_report:
            print(f"  共 {created} 个目录")

    if not args.merge_only:
        if not args.minimal_report:
            print("\n📄 步骤 2: 移动文件")
        moved, applied_moves = move_files(docs_path, plan.get("moves", []), dry_run, args.minimal_report)
        if not args.minimal_report:
            print(f"\n  共 {moved} 个文件")

    if not args.moves_only:
        if not args.minimal_report:
            print("\n🔄 步骤 3: 合并文件")
        merged, applied_merges, deleted_sources = merge_files(
            docs_path, plan.get("merges", []), dry_run, args.delete_sources, args.minimal_report
        )
        if not args.minimal_report:
            print(f"\n  共 {merged} 个合并组")

    if not args.minimal_report:
        print("\n📝 步骤 4: 更新 docs.json")
    docs_json_stats = update_docs_json(project_root, applied_moves, applied_merges, dry_run, args.minimal_report)

    write_merge_report(
        project_root=project_root,
        dry_run=dry_run,
        plan_path=plan_path,
        applied_moves=applied_moves,
        applied_merges=applied_merges,
        deleted_sources=deleted_sources,
        docs_json_stats=docs_json_stats,
        minimal_report=args.minimal_report,
    )

    if args.minimal_report:
        print(
            f"summary moves={len(applied_moves)} merges={len(applied_merges)} deleted={len(deleted_sources)} "
            f"rewrites={docs_json_stats.get('path_rewrites', 0)} dedup={docs_json_stats.get('duplicate_pages_removed', 0)}"
        )

    print("\n" + "=" * 64)
    if dry_run:
        print("✅ [DRY-RUN] 预览完成，未执行写入")
        print("💡 执行命令: python scripts/reorganize_docs.py --apply --delete-sources")
    else:
        print("✅ 文档重组完成")
    print("=" * 64)


if __name__ == "__main__":
    main()
