#!/usr/bin/env python3
"""
reorganize_docs.py

根据 doc_reorganize_plan.json 执行文档重组。
包括：创建目录、移动文件、合并文件、更新 docs.json。

Usage:
    python scripts/reorganize_docs.py --dry-run     # 预览更改
    python scripts/reorganize_docs.py               # 执行更改
    python scripts/reorganize_docs.py --moves-only  # 仅执行移动
    python scripts/reorganize_docs.py --merge-only  # 仅执行合并
"""

import json
import sys
import io
import shutil
import re
from pathlib import Path
from datetime import datetime
from typing import List, Dict

# Windows 控制台 UTF-8 支持
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')


def create_directories(docs_path: Path, directories: List[str], dry_run: bool) -> int:
    """创建新目录"""
    created = 0
    for dir_name in directories:
        dir_path = docs_path / dir_name
        if not dir_path.exists():
            if dry_run:
                print(f"  [DRY-RUN] 创建目录: {dir_name}")
            else:
                dir_path.mkdir(parents=True, exist_ok=True)
                print(f"  ✓ 创建目录: {dir_name}")
            created += 1
    return created


def move_files(docs_path: Path, moves: List[Dict], dry_run: bool) -> int:
    """移动文件"""
    moved = 0
    for move in moves:
        src = docs_path / move["source"]
        dst = docs_path / move["destination"]
        
        if not src.exists():
            print(f"  ⚠️ 源文件不存在: {move['source']}")
            continue
        
        if dst.exists():
            print(f"  ⚠️ 目标已存在，跳过: {move['destination']}")
            continue
        
        if dry_run:
            print(f"  [DRY-RUN] 移动: {move['source']}")
            print(f"          → {move['destination']}")
        else:
            # 确保目标目录存在
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(src), str(dst))
            print(f"  ✓ 移动: {move['source']}")
            print(f"       → {move['destination']}")
        
        moved += 1
    
    return moved


def extract_title_from_md(file_path: Path) -> str:
    """从 Markdown 文件提取标题"""
    try:
        content = file_path.read_text(encoding="utf-8")
        # 查找第一个 H1 标题
        match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
        if match:
            return match.group(1).strip()
        return file_path.stem
    except:
        return file_path.stem


def merge_files(docs_path: Path, merges: List[Dict], dry_run: bool) -> int:
    """合并文件"""
    merged = 0
    
    for merge in merges:
        target = docs_path / merge["target"]
        sources = [docs_path / src for src in merge["sources"]]
        
        # 检查源文件
        existing_sources = [src for src in sources if src.exists()]
        if len(existing_sources) < 2:
            print(f"  ⚠️ 合并组 '{merge['name']}' 源文件不足，跳过")
            continue
        
        if dry_run:
            print(f"\n  [DRY-RUN] 合并 '{merge['name']}':")
            for src in existing_sources:
                title = extract_title_from_md(src)
                print(f"    - {src.relative_to(docs_path)} ({title})")
            print(f"    → {merge['target']}")
        else:
            # 创建合并内容
            merged_content = []
            merged_content.append(f"# {merge['name'].replace('合并', '综合指南')}\n")
            merged_content.append(f"> 本文档由以下文件合并生成 ({datetime.now().strftime('%Y-%m-%d')})\n")
            merged_content.append("")
            
            for i, src in enumerate(existing_sources):
                title = extract_title_from_md(src)
                content = src.read_text(encoding="utf-8")
                
                # 移除原有的 H1 标题，转为 H2
                content = re.sub(r'^#\s+(.+)$', r'## \1', content, count=1, flags=re.MULTILINE)
                
                merged_content.append(f"\n---\n")
                merged_content.append(f"\n<!-- 来源: {src.relative_to(docs_path)} -->\n")
                merged_content.append(content)
                merged_content.append("\n")
            
            # 确保目标目录存在
            target.parent.mkdir(parents=True, exist_ok=True)
            
            # 写入合并文件
            target.write_text("\n".join(merged_content), encoding="utf-8")
            print(f"\n  ✓ 合并 '{merge['name']}':")
            for src in existing_sources:
                print(f"    - {src.relative_to(docs_path)}")
            print(f"    → {merge['target']}")
        
        merged += 1
    
    return merged


def update_docs_json(project_root: Path, moves: List[Dict], merges: List[Dict], dry_run: bool):
    """更新 docs.json 中的路径引用"""
    docs_json_path = project_root / "docs.json"
    
    if not docs_json_path.exists():
        print("  ⚠️ docs.json 不存在，跳过更新")
        return
    
    # 读取 docs.json
    with open(docs_json_path, "r", encoding="utf-8") as f:
        content = f.read()
    
    original_content = content
    changes = 0
    
    # 替换移动的文件路径
    for move in moves:
        old_path = "docs/" + move["source"].replace(".md", "")
        new_path = "docs/" + move["destination"].replace(".md", "")
        
        if old_path in content:
            content = content.replace(f'"{old_path}"', f'"{new_path}"')
            changes += 1
    
    if dry_run:
        if changes > 0:
            print(f"\n  [DRY-RUN] docs.json 将更新 {changes} 处路径引用")
    else:
        if changes > 0:
            with open(docs_json_path, "w", encoding="utf-8") as f:
                f.write(content)
            print(f"\n  ✓ docs.json 已更新 {changes} 处路径引用")
        else:
            print("\n  ℹ️ docs.json 无需更新")


def main():
    # 解析参数
    dry_run = "--dry-run" in sys.argv
    moves_only = "--moves-only" in sys.argv
    merge_only = "--merge-only" in sys.argv
    
    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    docs_path = project_root / "docs"
    plan_path = script_dir / "doc_reorganize_plan.json"
    
    if not plan_path.exists():
        print("❌ 找不到重组计划，请先运行: python scripts/analyze_docs_structure.py")
        sys.exit(1)
    
    # 读取计划
    with open(plan_path, "r", encoding="utf-8") as f:
        plan = json.load(f)
    
    print("=" * 60)
    if dry_run:
        print("📋 文档重组预览 [DRY-RUN 模式]")
    else:
        print("🚀 执行文档重组")
    print("=" * 60)
    
    # 1. 创建目录
    if not merge_only:
        print("\n📁 步骤 1: 创建新目录")
        created = create_directories(docs_path, plan.get("new_directories", []), dry_run)
        print(f"  共 {created} 个目录")
    
    # 2. 移动文件
    if not merge_only:
        print("\n📄 步骤 2: 移动文件")
        moved = move_files(docs_path, plan.get("moves", []), dry_run)
        print(f"\n  共 {moved} 个文件")
    
    # 3. 合并文件
    if not moves_only:
        print("\n🔄 步骤 3: 合并文件")
        merged = merge_files(docs_path, plan.get("merges", []), dry_run)
        print(f"\n  共 {merged} 个合并组")
    
    # 4. 更新 docs.json
    if not merge_only and not moves_only:
        print("\n📝 步骤 4: 更新 docs.json")
        update_docs_json(project_root, plan.get("moves", []), plan.get("merges", []), dry_run)
    
    # 完成
    print("\n" + "=" * 60)
    if dry_run:
        print("✅ [DRY-RUN] 预览完成，未做任何更改")
        print("💡 确认无误后，运行: python scripts/reorganize_docs.py")
    else:
        print("✅ 文档重组完成!")
        print("💡 建议:")
        print("   1. 检查 git status 确认更改")
        print("   2. 运行 mintlify dev 验证文档")
        print("   3. 手动更新 docs.json 导航结构")
    print("=" * 60)


if __name__ == "__main__":
    main()
