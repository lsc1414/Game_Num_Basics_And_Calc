#!/usr/bin/env python3
"""
update_docs_json_structure.py

重组后更新 docs.json 导航结构。
根据新的 Case_Studies 目录结构重建导航。

Usage:
    python scripts/update_docs_json_structure.py [--dry-run]
"""

import json
import sys
import io
from pathlib import Path
from typing import List, Dict

# Windows 控制台 UTF-8 支持
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')


def scan_case_studies(docs_path: Path) -> Dict[str, List[str]]:
    """扫描 Case_Studies 目录结构"""
    case_studies_path = docs_path / "Case_Studies"
    
    if not case_studies_path.exists():
        return {}
    
    result = {}
    for subdir in sorted(case_studies_path.iterdir()):
        if subdir.is_dir():
            files = []
            for md_file in sorted(subdir.glob("*.md")):
                rel_path = md_file.relative_to(docs_path)
                # 移除 .md 扩展名，加上 docs/ 前缀
                files.append("docs/" + str(rel_path).replace("\\", "/").replace(".md", ""))
            if files:
                result[subdir.name] = files
    
    return result


# 案例类别中文名映射
CASE_CATEGORY_NAMES = {
    "Roguelike": "🎲 Roguelike",
    "Tower_Defense": "🏰 塔防",
    "Hybrid": "⚔️ 混合类型",
    "Survivors": "🧛 幸存者类",
    "Sandbox": "🏭 沙盒建造",
    "Magic_System": "🔮 魔法系统",
    "Coop": "👥 合作游戏",
    "Failure": "💀 失败复盘",
}


def build_case_studies_tab(case_categories: Dict[str, List[str]]) -> dict:
    """构建案例研究 Tab"""
    groups = []
    
    for category, files in case_categories.items():
        group_name = CASE_CATEGORY_NAMES.get(category, category)
        groups.append({
            "group": group_name,
            "pages": files
        })
    
    return {
        "tab": "📖 案例研究",
        "groups": groups
    }


def update_docs_json(project_root: Path, dry_run: bool):
    """更新 docs.json"""
    docs_path = project_root / "docs"
    docs_json_path = project_root / "docs.json"
    
    if not docs_json_path.exists():
        print("❌ docs.json 不存在")
        return
    
    # 读取现有配置
    with open(docs_json_path, "r", encoding="utf-8") as f:
        config = json.load(f)
    
    # 扫描新的 Case_Studies 目录
    case_categories = scan_case_studies(docs_path)
    
    if not case_categories:
        print("ℹ️ Case_Studies 目录不存在或为空，跳过")
        return
    
    print("\n📁 发现案例分类:")
    for category, files in case_categories.items():
        print(f"  {category}: {len(files)} 个文件")
    
    # 构建新的 Case Studies Tab
    case_studies_tab = build_case_studies_tab(case_categories)
    
    # 找到并更新/添加 Tab
    tabs = config.get("navigation", {}).get("tabs", [])
    
    # 查找现有的相关 Tab 并移除
    tabs_to_remove = []
    for i, tab in enumerate(tabs):
        tab_name = tab.get("tab", "")
        # 移除旧的 Design 中的 Game Knowledge Maps (会单独放入案例研究)
        # 保留其他 Tab
        pass  # 暂时不自动移除，让用户手动确认
    
    # 检查是否已有 "案例研究" Tab
    existing_case_tab_idx = None
    for i, tab in enumerate(tabs):
        if "案例" in tab.get("tab", "") or "Case" in tab.get("tab", ""):
            existing_case_tab_idx = i
            break
    
    if existing_case_tab_idx is not None:
        if dry_run:
            print(f"\n[DRY-RUN] 将更新现有 Tab: {tabs[existing_case_tab_idx].get('tab')}")
        else:
            tabs[existing_case_tab_idx] = case_studies_tab
            print(f"\n✓ 已更新现有 Tab")
    else:
        if dry_run:
            print(f"\n[DRY-RUN] 将添加新 Tab: {case_studies_tab['tab']}")
        else:
            # 在 Design 后面插入
            design_idx = None
            for i, tab in enumerate(tabs):
                if "设计" in tab.get("tab", "") or "Design" in tab.get("tab", ""):
                    design_idx = i
                    break
            
            if design_idx is not None:
                tabs.insert(design_idx + 1, case_studies_tab)
            else:
                tabs.append(case_studies_tab)
            print(f"\n✓ 已添加新 Tab: {case_studies_tab['tab']}")
    
    # 保存
    if not dry_run:
        config["navigation"]["tabs"] = tabs
        with open(docs_json_path, "w", encoding="utf-8") as f:
            json.dump(config, f, ensure_ascii=False, indent=2)
        print(f"\n✅ docs.json 已更新")
        print("💡 建议运行 prettier 格式化: cmd /c \"npx prettier --write docs.json\"")
    else:
        print(f"\n✅ [DRY-RUN] 预览完成")


def main():
    dry_run = "--dry-run" in sys.argv
    
    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    
    print("=" * 60)
    if dry_run:
        print("📋 更新 docs.json 导航结构 [DRY-RUN]")
    else:
        print("🚀 更新 docs.json 导航结构")
    print("=" * 60)
    
    update_docs_json(project_root, dry_run)


if __name__ == "__main__":
    main()
