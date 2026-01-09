#!/usr/bin/env python3
"""
analyze_docs_structure.py

分析 docs 文件夹结构，识别冗余和需要重组的文件。
输出分析报告和建议的文件移动/合并操作。

Usage:
    python scripts/analyze_docs_structure.py

Outputs:
    - 控制台输出结构分析
    - 生成 scripts/doc_reorganize_plan.json (移动和合并计划)
"""

import json
import sys
import io
import re
from pathlib import Path
from collections import defaultdict
from typing import Dict, List, Tuple

# Windows 控制台 UTF-8 支持
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')


# ========================================
# 新目录结构映射
# ========================================

# 需要移动的知识图谱文件 → 新位置
KNOWLEDGE_MAP_MOVES = {
    # Roguelike 游戏
    "Design/Dead_Cells_Knowledge_Map.md": "Case_Studies/Roguelike/Dead_Cells.md",
    "Design/Risk_of_Rain_2_Knowledge_Map.md": "Case_Studies/Roguelike/Risk_of_Rain_2.md",
    "Design/Enter_the_Gungeon_Knowledge_Map.md": "Case_Studies/Roguelike/Enter_the_Gungeon.md",
    "Design/Binding_of_Isaac_Knowledge_Map.md": "Case_Studies/Roguelike/Binding_of_Isaac.md",
    "Design/Noita_Knowledge_Map.md": "Case_Studies/Roguelike/Noita.md",
    "Design/Darkest_Dungeon_Knowledge_Map.md": "Case_Studies/Roguelike/Darkest_Dungeon.md",
    "Design/Roguelike_Deckbuilder_Knowledge_Map.md": "Case_Studies/Roguelike/Slay_the_Spire.md",
    
    # 塔防游戏
    "Design/They_Are_Billions_Knowledge_Map.md": "Case_Studies/Tower_Defense/They_Are_Billions.md",
    
    # 混合类型
    "Design/Dome_Keeper_Knowledge_Map.md": "Case_Studies/Hybrid/Dome_Keeper.md",
    "Design/Minimalist_Strategy_Design_Knowledge.md": "Case_Studies/Hybrid/Thronefall.md",
    
    # 魔法/合作游戏
    "Design/Magicka_Knowledge_Map.md": "Case_Studies/Magic_System/Magicka.md",
    "Design/Magicraft_Knowledge_Map.md": "Case_Studies/Magic_System/Magicraft.md",
    "Design/Deep_Rock_Galactic_Knowledge_Map.md": "Case_Studies/Coop/Deep_Rock_Galactic.md",
}

# Dev_Guides/Industry_Cases 也需要移动
INDUSTRY_CASE_MOVES = {
    "Dev_Guides/Industry_Cases/Hades_Build_Diversity.md": "Case_Studies/Roguelike/Hades.md",
    "Dev_Guides/Industry_Cases/Brotato_Numerical_Analysis.md": "Case_Studies/Roguelike/Brotato.md",
    "Dev_Guides/Industry_Cases/Vampire_Survivors_Performance.md": "Case_Studies/Survivors/Vampire_Survivors.md",
    "Dev_Guides/Industry_Cases/Bloons_TD6_Damage_Matrix.md": "Case_Studies/Tower_Defense/Bloons_TD6.md",
    "Dev_Guides/Industry_Cases/Kingdom_Rush_Numerical_Model.md": "Case_Studies/Tower_Defense/Kingdom_Rush.md",
    "Dev_Guides/Industry_Cases/Thronefall_Minimalist_Hybrid.md": "Case_Studies/Hybrid/Thronefall_Analysis.md",
    "Dev_Guides/Industry_Cases/Loop_Hero_Loop_Mechanics.md": "Case_Studies/Hybrid/Loop_Hero.md",
    "Dev_Guides/Industry_Cases/Factorio_Optimization_Study.md": "Case_Studies/Sandbox/Factorio.md",
    "Dev_Guides/Industry_Cases/Palworld_Production_Model.md": "Case_Studies/Sandbox/Palworld.md",
    
    # 失败案例
    "Dev_Guides/Industry_Cases/Failure_Analysis/Anthem_Failure_Analysis.md": "Case_Studies/Failure/Anthem.md",
    "Dev_Guides/Industry_Cases/Failure_Analysis/Battleborn_Failure_Analysis.md": "Case_Studies/Failure/Battleborn.md",
    "Dev_Guides/Industry_Cases/Failure_Analysis/Concord_Failure_Analysis.md": "Case_Studies/Failure/Concord.md",
    "Dev_Guides/Industry_Cases/Failure_Analysis/Paragon_Complexity_Trap.md": "Case_Studies/Failure/Paragon.md",
    "Dev_Guides/Industry_Cases/Failure_Analysis/The_Day_Before_Failure_Analysis.md": "Case_Studies/Failure/The_Day_Before.md",
}

# 需要合并的文件组
MERGE_GROUPS = [
    {
        "name": "决策系统合并",
        "target": "Tech/Architecture/Decision_System.md",
        "sources": [
            "Tech/Architecture/Unified_Decision_System.md",
            "Tech/Architecture/Decision_System_Diagrams.md",
            "Tech/Code_Snippets/DecisionSystem_Core_Classes.md",
            "Tech/Code_Snippets/DecisionSystem_Performance_Demo.md",
        ],
        "description": "合并决策系统相关的 4 个文件为一个完整文档"
    },
    {
        "name": "索敌系统合并",
        "target": "Tech/Mechanics/Targeting_System_Complete.md",
        "sources": [
            "Tech/Mechanics/Targeting_System_DeepDive.md",
            "Tech/Mechanics/Targeting_Pipeline_DeepDive.md",
        ],
        "description": "合并索敌系统的两个文档"
    },
    {
        "name": "Git 指南合并",
        "target": "Guides/Collaboration/Git_Complete_Guide.md", 
        "sources": [
            "Dev_Guides/Collaboration/Git_Advanced_Guide_For_Programmers.md",
            "Dev_Guides/Collaboration/Git_Commit_Standards.md",
            "Dev_Guides/Collaboration/GitHub_PR_Workflow.md",
            "Dev_Guides/Collaboration/SVN_vs_Git_Migration_Guide.md",
        ],
        "description": "合并 Git 相关的 4 个文档"
    },
    {
        "name": "Steam 发行合并",
        "target": "Guides/Publishing/Steam_Complete_Guide.md",
        "sources": [
            "Dev_Guides/Publishing/Steam_Strategy.md",
            "Dev_Guides/Publishing/Steam_Unity_Indie_Game_Guide.md",
            "Dev_Guides/Publishing/Steam_Unity_Quality_Standards.md",
            "Dev_Guides/Publishing/Steam_Unity_Steamworks_Checklist.md",
        ],
        "description": "合并 Steam 发行相关的 4 个文档"
    },
    {
        "name": "Odin 工具合并",
        "target": "Tools/Odin_Inspector_Complete.md",
        "sources": [
            "Dev_Guides/Tools/Odin_Inspector_Advanced_Techniques.md",
            "Dev_Guides/Tools/Odin_Luban_Integration_Guide.md",
        ],
        "description": "合并 Odin Inspector 相关的 2 个文档"
    },
    {
        "name": "移动优化合并",
        "target": "Tech/Performance/Mobile_Optimization_Complete.md",
        "sources": [
            "Tech/Mobile_Optimization_Guide.md",
            "Tech/Mobile_Optimization/Device_Grading_And_Scalability.md",
        ],
        "description": "合并移动优化相关的 2 个文档"
    },
    {
        "name": "ECS 合并",
        "target": "Tech/Architecture/ECS_Complete_Guide.md",
        "sources": [
            "Tech/Architecture/ECS_Theory_And_Practice.md",
            "Dev_Guides/Technical_Implementation/ECS_Performance_Optimization.md",
        ],
        "description": "合并 ECS 理论与实践文档"
    },
    {
        "name": "PCG 算法合并",
        "target": "Tech/Algorithms/Procedural_Generation_Complete.md",
        "sources": [
            "Tech/Algorithms/Procedural_Generation_Guide.md",
            "Dev_Guides/Technical_Implementation/Procedural_Generation_WFC.md",
        ],
        "description": "合并程序生成相关文档"
    },
]


def scan_docs_folder(docs_path: Path) -> Dict[str, List[Path]]:
    """扫描 docs 文件夹，按目录分组"""
    files_by_dir = defaultdict(list)
    
    for md_file in docs_path.rglob("*.md"):
        rel_path = md_file.relative_to(docs_path)
        parent = str(rel_path.parent)
        files_by_dir[parent].append(rel_path)
    
    return dict(files_by_dir)


def analyze_file_sizes(docs_path: Path) -> List[Tuple[Path, int]]:
    """分析文件大小，找出过小的文件（可能需要合并）"""
    small_files = []
    
    for md_file in docs_path.rglob("*.md"):
        size = md_file.stat().st_size
        if size < 2000:  # 小于 2KB
            rel_path = md_file.relative_to(docs_path)
            small_files.append((rel_path, size))
    
    return sorted(small_files, key=lambda x: x[1])


def check_file_exists(docs_path: Path, moves: Dict[str, str]) -> Dict[str, str]:
    """检查源文件是否存在"""
    valid_moves = {}
    missing_files = []
    
    for src, dst in moves.items():
        src_path = docs_path / src
        if src_path.exists():
            valid_moves[src] = dst
        else:
            missing_files.append(src)
    
    if missing_files:
        print(f"  ⚠️ 以下文件不存在，将跳过:")
        for f in missing_files[:5]:  # 只显示前5个
            print(f"     - {f}")
        if len(missing_files) > 5:
            print(f"     ... 还有 {len(missing_files) - 5} 个")
    
    return valid_moves


def generate_reorganize_plan(docs_path: Path) -> dict:
    """生成重组计划 JSON"""
    plan = {
        "moves": [],
        "merges": [],
        "new_directories": set(),
    }
    
    # 1. 知识图谱移动
    print("\n📁 检查知识图谱文件...")
    valid_km_moves = check_file_exists(docs_path, KNOWLEDGE_MAP_MOVES)
    for src, dst in valid_km_moves.items():
        plan["moves"].append({"source": src, "destination": dst})
        plan["new_directories"].add(str(Path(dst).parent))
    
    # 2. 行业案例移动
    print("\n📁 检查行业案例文件...")
    valid_ic_moves = check_file_exists(docs_path, INDUSTRY_CASE_MOVES)
    for src, dst in valid_ic_moves.items():
        plan["moves"].append({"source": src, "destination": dst})
        plan["new_directories"].add(str(Path(dst).parent))
    
    # 3. 合并计划
    print("\n📁 检查需要合并的文件...")
    for merge_group in MERGE_GROUPS:
        existing_sources = []
        for src in merge_group["sources"]:
            if (docs_path / src).exists():
                existing_sources.append(src)
        
        if len(existing_sources) >= 2:
            plan["merges"].append({
                "name": merge_group["name"],
                "target": merge_group["target"],
                "sources": existing_sources,
                "description": merge_group["description"],
            })
            plan["new_directories"].add(str(Path(merge_group["target"]).parent))
            print(f"  ✓ {merge_group['name']}: {len(existing_sources)} 个文件")
        else:
            print(f"  ⚠️ {merge_group['name']}: 源文件不足，跳过")
    
    # 转换 set 为 list
    plan["new_directories"] = sorted(list(plan["new_directories"]))
    
    return plan


def main():
    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    docs_path = project_root / "docs"
    
    if not docs_path.exists():
        print(f"❌ 找不到 docs 目录: {docs_path}")
        sys.exit(1)
    
    print("=" * 60)
    print("📊 文档结构分析报告")
    print("=" * 60)
    
    # 1. 扫描目录结构
    print("\n📂 目录结构概览:\n")
    files_by_dir = scan_docs_folder(docs_path)
    
    dir_stats = []
    for dir_name, files in files_by_dir.items():
        dir_stats.append((dir_name, len(files)))
    
    dir_stats.sort(key=lambda x: -x[1])
    
    for dir_name, count in dir_stats[:15]:
        print(f"  {dir_name}: {count} 个文件")
    
    if len(dir_stats) > 15:
        print(f"  ... 还有 {len(dir_stats) - 15} 个目录")
    
    total_files = sum(len(files) for files in files_by_dir.values())
    print(f"\n  📊 总计: {len(dir_stats)} 个目录, {total_files} 个 Markdown 文件")
    
    # 2. 分析小文件
    print("\n📏 小文件分析 (< 2KB):\n")
    small_files = analyze_file_sizes(docs_path)
    for path, size in small_files[:10]:
        print(f"  {size:>5} bytes - {path}")
    if len(small_files) > 10:
        print(f"  ... 还有 {len(small_files) - 10} 个小文件")
    
    # 3. 生成重组计划
    print("\n" + "=" * 60)
    print("📋 生成重组计划")
    print("=" * 60)
    
    plan = generate_reorganize_plan(docs_path)
    
    # 4. 输出统计
    print("\n" + "=" * 60)
    print("📊 重组计划统计")
    print("=" * 60)
    print(f"\n  📁 需要创建的新目录: {len(plan['new_directories'])} 个")
    print(f"  📄 需要移动的文件: {len(plan['moves'])} 个")
    print(f"  🔄 需要合并的文件组: {len(plan['merges'])} 个")
    
    # 5. 保存计划
    output_path = script_dir / "doc_reorganize_plan.json"
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(plan, f, ensure_ascii=False, indent=2)
    
    print(f"\n✅ 重组计划已保存到: {output_path}")
    print("\n💡 下一步: 运行 python scripts/reorganize_docs.py --dry-run 预览更改")


if __name__ == "__main__":
    main()
