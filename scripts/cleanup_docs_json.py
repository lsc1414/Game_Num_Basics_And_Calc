#!/usr/bin/env python3
"""
cleanup_docs_json.py

清理 docs.json 中的无效引用和重复条目。
- 移除指向不存在文件的引用
- 合并重复的案例研究条目
- 清理空的 groups

Usage:
    python scripts/cleanup_docs_json.py [--dry-run]
"""

import json
import sys
import io
from pathlib import Path
from typing import List, Dict, Any

# Windows 控制台 UTF-8 支持
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')


def check_page_exists(project_root: Path, page_path: str) -> bool:
    """检查页面文件是否存在"""
    # 添加 .md 扩展名
    file_path = project_root / (page_path + ".md")
    return file_path.exists()


def clean_pages_list(project_root: Path, pages: List[str]) -> tuple[List[str], int]:
    """清理无效的页面引用"""
    valid_pages = []
    removed = 0
    
    for page in pages:
        if check_page_exists(project_root, page):
            valid_pages.append(page)
        else:
            removed += 1
            print(f"    ❌ 移除无效引用: {page}")
    
    return valid_pages, removed


def clean_groups(project_root: Path, groups: List[Dict]) -> tuple[List[Dict], int]:
    """清理 groups 中的无效引用"""
    cleaned_groups = []
    total_removed = 0
    
    for group in groups:
        if "pages" in group:
            group["pages"], removed = clean_pages_list(project_root, group["pages"])
            total_removed += removed
            
            # 只保留非空的 groups
            if group["pages"]:
                cleaned_groups.append(group)
            else:
                print(f"    ⚠️ 移除空 Group: {group.get('group', 'unknown')}")
    
    return cleaned_groups, total_removed


def clean_tabs(project_root: Path, tabs: List[Dict]) -> tuple[List[Dict], int]:
    """清理所有 tabs"""
    total_removed = 0
    
    for tab in tabs:
        tab_name = tab.get("tab", "unknown")
        print(f"\n  检查 Tab: {tab_name}")
        
        if "pages" in tab:
            tab["pages"], removed = clean_pages_list(project_root, tab["pages"])
            total_removed += removed
        
        if "groups" in tab:
            tab["groups"], removed = clean_groups(project_root, tab["groups"])
            total_removed += removed
    
    return tabs, total_removed


def remove_duplicate_case_studies(tabs: List[Dict]) -> List[Dict]:
    """移除 Design Tab 中的重复案例引用"""
    # 收集所有 Case_Studies 路径
    case_study_paths = set()
    for tab in tabs:
        if "案例研究" in tab.get("tab", ""):
            for group in tab.get("groups", []):
                for page in group.get("pages", []):
                    case_study_paths.add(page)
    
    # 从 Design Tab 的 "游戏案例图谱" group 中移除已在 Case_Studies Tab 中的条目
    for tab in tabs:
        if "设计" in tab.get("tab", ""):
            for group in tab.get("groups", []):
                if "游戏案例" in group.get("group", "") or "Game Knowledge" in group.get("group", ""):
                    original_count = len(group.get("pages", []))
                    group["pages"] = [
                        p for p in group.get("pages", [])
                        if p not in case_study_paths and "Case_Studies" not in p
                    ]
                    removed = original_count - len(group["pages"])
                    if removed > 0:
                        print(f"\n  ✓ 从 '{group['group']}' 移除 {removed} 个已迁移的案例引用")
    
    # 移除空的 groups
    for tab in tabs:
        if "groups" in tab:
            tab["groups"] = [g for g in tab["groups"] if g.get("pages")]
    
    return tabs


def main():
    dry_run = "--dry-run" in sys.argv
    
    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    docs_json_path = project_root / "docs.json"
    
    if not docs_json_path.exists():
        print("❌ docs.json 不存在")
        sys.exit(1)
    
    print("=" * 60)
    if dry_run:
        print("🧹 清理 docs.json [DRY-RUN]")
    else:
        print("🧹 清理 docs.json")
    print("=" * 60)
    
    # 读取配置
    with open(docs_json_path, "r", encoding="utf-8") as f:
        config = json.load(f)
    
    tabs = config.get("navigation", {}).get("tabs", [])
    
    # 1. 清理无效引用
    print("\n📋 步骤 1: 清理无效引用")
    tabs, removed = clean_tabs(project_root, tabs)
    print(f"\n  共移除 {removed} 个无效引用")
    
    # 2. 移除重复的案例研究
    print("\n📋 步骤 2: 移除重复的案例研究条目")
    tabs = remove_duplicate_case_studies(tabs)
    
    # 保存
    config["navigation"]["tabs"] = tabs
    
    if dry_run:
        print("\n" + "=" * 60)
        print("✅ [DRY-RUN] 预览完成")
    else:
        with open(docs_json_path, "w", encoding="utf-8") as f:
            json.dump(config, f, ensure_ascii=False, indent=2)
        print("\n" + "=" * 60)
        print("✅ docs.json 已清理")
        print("💡 建议运行: cmd /c \"npx prettier --write docs.json\"")


if __name__ == "__main__":
    main()
