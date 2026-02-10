#!/usr/bin/env python3
"""
dedupe_scan.py

Low-token duplicate scan for docs markdown files.

Usage:
    python scripts/dedupe_scan.py --docs docs --out reports/dedupe_candidates.json --min-score 0.35
    python scripts/dedupe_scan.py --docs docs --out reports/dedupe_candidates.json --incremental --cache reports/dedupe_cache.json
    python scripts/dedupe_scan.py --docs docs --out reports/dedupe_candidates.json --incremental --update-plan scripts/doc_reorganize_plan.json
"""

import argparse
import hashlib
import json
import re
import subprocess
from difflib import SequenceMatcher
from pathlib import Path
from typing import Dict, List, Set


IGNORED_DIRS = {".vitepress", "assets", "stylesheets", "javascripts"}


def estimate_tokens(text: str) -> int:
    return int(len(text) / 1.6)


def normalize_text(text: str) -> str:
    text = text.lower()
    text = re.sub(r"```.*?```", " ", text, flags=re.S)
    text = re.sub(r"`[^`]*`", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def heading_set(text: str) -> Set[str]:
    values = re.findall(r"^#{1,3}\s+(.+)$", text, flags=re.M)
    return {v.strip().lower() for v in values if v.strip()}


def filename_family(path: Path) -> str:
    stem = path.stem.lower()
    stem = re.sub(
        r"(?:_complete|_guide|_deepdive|_analysis|_system|_design|_theory|_standards|_best_practices)$",
        "",
        stem,
    )
    stem = re.sub(r"[^a-z0-9]+", "_", stem).strip("_")
    return stem


def pick_target(paths: List[Path]) -> Path:
    priority = ["_complete", "_guide", "_deepdive", "_analysis"]
    sorted_paths = sorted(paths, key=lambda p: len(p.as_posix()))
    for suffix in priority:
        for path in sorted_paths:
            if path.stem.lower().endswith(suffix):
                return path
    return sorted_paths[0]


def file_sha1(path: Path) -> str:
    return hashlib.sha1(path.read_bytes()).hexdigest()


def should_skip(path: Path) -> bool:
    return any(part in IGNORED_DIRS for part in path.parts)


def load_cache(cache_path: Path) -> Dict:
    if not cache_path.exists():
        return {"files": {}}
    try:
        return json.loads(cache_path.read_text(encoding="utf-8"))
    except Exception:
        return {"files": {}}


def save_cache(cache_path: Path, cache_obj: Dict) -> None:
    cache_path.parent.mkdir(parents=True, exist_ok=True)
    cache_path.write_text(json.dumps(cache_obj, ensure_ascii=False, indent=2), encoding="utf-8")


def get_changed_docs_git(docs_dir: Path) -> Set[Path]:
    changed = set()
    cmds = [
        ["git", "diff", "--name-only", "HEAD"],
        ["git", "ls-files", "--others", "--exclude-standard"],
    ]
    for cmd in cmds:
        try:
            out = subprocess.check_output(cmd, text=True, stderr=subprocess.DEVNULL)
        except Exception:
            continue
        for line in out.splitlines():
            p = Path(line.strip())
            if not p:
                continue
            if p.suffix.lower() != ".md":
                continue
            resolved = p.resolve()
            if docs_dir in resolved.parents or resolved == docs_dir:
                if not should_skip(resolved):
                    changed.add(resolved)
    return changed


def build_index(docs_dir: Path, cache_obj: Dict, use_incremental: bool) -> Dict[str, Dict]:
    files = [p.resolve() for p in docs_dir.rglob("*.md") if not should_skip(p)]
    changed = get_changed_docs_git(docs_dir) if use_incremental else set(files)

    index: Dict[str, Dict] = {}
    cache_files = cache_obj.setdefault("files", {})
    parsed_count = 0
    cache_hit = 0

    for md in files:
        key = md.as_posix()
        sig = f"{md.stat().st_mtime_ns}:{md.stat().st_size}"
        cached = cache_files.get(key)

        if cached and cached.get("sig") == sig:
            data = cached["data"]
            cache_hit += 1
        else:
            text = md.read_text(encoding="utf-8", errors="ignore")
            norm = normalize_text(text)
            data = {
                "path": key,
                "family": filename_family(md),
                "dir": md.parent.as_posix(),
                "tokens": estimate_tokens(text),
                "heads": sorted(heading_set(text)),
                "norm": norm[:120000],
                "sha1": file_sha1(md),
            }
            cache_files[key] = {"sig": sig, "data": data}
            parsed_count += 1
        index[key] = data

    if use_incremental and changed:
        changed_keys = {p.as_posix() for p in changed}
    else:
        changed_keys = set(index.keys())

    return {
        "index": index,
        "changed_keys": changed_keys,
        "stats": {"total_files": len(index), "parsed_files": parsed_count, "cache_hits": cache_hit},
    }


def select_candidate_pairs(index: Dict[str, Dict], changed_keys: Set[str]) -> List[List[str]]:
    by_family: Dict[str, List[str]] = {}
    by_dir: Dict[str, List[str]] = {}
    for key, row in index.items():
        by_family.setdefault(row["family"], []).append(key)
        by_dir.setdefault(row["dir"], []).append(key)

    pairs = set()
    for changed_key in changed_keys:
        row = index.get(changed_key)
        if not row:
            continue
        pool = set(by_family.get(row["family"], [])) | set(by_dir.get(row["dir"], []))
        pool.discard(changed_key)
        for other in pool:
            a, b = sorted([changed_key, other])
            pairs.add((a, b))
    return [[a, b] for a, b in sorted(pairs)]


def score_pairs(index: Dict[str, Dict], pairs: List[List[str]], min_score: float) -> List[Dict]:
    candidates = []
    for a, b in pairs:
        left = index[a]
        right = index[b]

        seq = SequenceMatcher(None, left["norm"], right["norm"]).ratio()
        heads_l = set(left["heads"])
        heads_r = set(right["heads"])
        union = heads_l | heads_r
        inter = heads_l & heads_r
        heading_overlap = len(inter) / len(union) if union else 0.0
        score = 0.7 * seq + 0.3 * heading_overlap
        if score < min_score:
            continue

        target = pick_target([Path(a), Path(b)])
        source = Path(b) if target.as_posix() == a else Path(a)
        token_saving = index[source.as_posix()]["tokens"]

        candidates.append(
            {
                "family": left["family"] if left["family"] == right["family"] else "cross_scope",
                "target": target.as_posix(),
                "source": source.as_posix(),
                "seq_ratio": round(seq, 4),
                "heading_overlap": round(heading_overlap, 4),
                "similarity_score": round(score, 4),
                "token_saving_est": int(token_saving),
                "reason": "incremental_pool_similarity_threshold",
            }
        )

    candidates.sort(key=lambda c: c["similarity_score"], reverse=True)
    return candidates


def update_plan(plan_path: Path, docs_dir: Path, candidates: List[Dict]) -> int:
    if not plan_path.exists():
        return 0

    plan = json.loads(plan_path.read_text(encoding="utf-8"))
    merges = plan.get("merges", [])
    existing_targets = {m.get("target") for m in merges}
    existing_sources = set()
    for merge in merges:
        for src in merge.get("sources", []):
            existing_sources.add(src)

    added = 0
    for cand in candidates:
        rel_target = str(Path(cand["target"]).relative_to(docs_dir)).replace("\\", "/")
        rel_source = str(Path(cand["source"]).relative_to(docs_dir)).replace("\\", "/")
        if rel_target in existing_targets or rel_source in existing_sources:
            continue

        merges.append(
            {
                "name": f"自动合并_{Path(rel_target).stem}",
                "target": rel_target,
                "sources": [rel_target, rel_source],
                "description": "由 dedupe_scan 增量扫描建议",
                "merge_strategy": "delete_sources",
                "similarity_score": cand["similarity_score"],
                "token_saving_est": cand["token_saving_est"],
                "reason": cand["reason"],
            }
        )
        existing_targets.add(rel_target)
        existing_sources.add(rel_source)
        added += 1

    plan["merges"] = merges
    plan_path.write_text(json.dumps(plan, ensure_ascii=False, indent=2), encoding="utf-8")
    return added


def main() -> None:
    parser = argparse.ArgumentParser(description="Scan docs similarity and suggest merge candidates.")
    parser.add_argument("--docs", default="docs", help="Docs directory path.")
    parser.add_argument("--out", required=True, help="Output candidate report json.")
    parser.add_argument("--min-score", type=float, default=0.35, help="Similarity threshold.")
    parser.add_argument("--incremental", action="store_true", help="Only score pairs related to git-changed docs.")
    parser.add_argument(
        "--changed-list",
        help="Optional text file with one docs-relative .md path per line. Overrides git-changed set in incremental mode.",
    )
    parser.add_argument("--cache", default="reports/dedupe_cache.json", help="Cache file for parsed docs.")
    parser.add_argument("--update-plan", help="Optional reorganize plan path to append auto merge groups.")
    args = parser.parse_args()

    docs_dir = Path(args.docs).resolve()
    cache_path = Path(args.cache)
    cache_obj = load_cache(cache_path)
    payload_index = build_index(docs_dir, cache_obj, args.incremental)
    index = payload_index["index"]
    changed_keys = payload_index["changed_keys"]
    stats = payload_index["stats"]

    if args.incremental and args.changed_list:
        changed_file = Path(args.changed_list)
        if changed_file.exists():
            selected = set()
            for line in changed_file.read_text(encoding="utf-8", errors="ignore").splitlines():
                v = line.strip().replace("\\", "/")
                if not v or v.startswith("#"):
                    continue
                abs_path = (Path.cwd() / v).resolve()
                key = abs_path.as_posix()
                if key in index:
                    selected.add(key)
            if selected:
                changed_keys = selected

    pairs = select_candidate_pairs(index, changed_keys)
    candidates = score_pairs(index, pairs, args.min_score)

    payload = {
        "docs_dir": docs_dir.as_posix(),
        "min_score": args.min_score,
        "incremental": args.incremental,
        "cache": cache_path.as_posix(),
        "scan_stats": {
            **stats,
            "changed_files": len(changed_keys),
            "candidate_pairs": len(pairs),
        },
        "candidate_count": len(candidates),
        "candidates": candidates,
    }

    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    save_cache(cache_path, cache_obj)

    print(f"Saved candidates to: {out_path.as_posix()}")
    print(
        f"Candidates: {len(candidates)} | parsed: {stats['parsed_files']} | cache_hits: {stats['cache_hits']} | pairs: {len(pairs)}"
    )

    if args.update_plan:
        added = update_plan(Path(args.update_plan), docs_dir, candidates)
        print(f"Plan updated: {added} auto merge groups added")


if __name__ == "__main__":
    main()
