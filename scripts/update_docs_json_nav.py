#!/usr/bin/env python3
"""
update_docs_json_nav.py

将 docs.json 中的英文导航标题替换为中文标题。
保持文件结构不变，仅修改 tab 和 group 名称。

Usage:
    python scripts/update_docs_json_nav.py [--dry-run]
    
Options:
    --dry-run   仅预览更改，不实际写入文件
"""

import json
import sys
import io
from pathlib import Path
from copy import deepcopy

# Windows 控制台 UTF-8 支持
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

# ========================================
# 中英文标题映射表
# ========================================

# Tabs (顶级标签页)
TAB_MAPPING = {
    "开始": "🚀 开始",
    "Art": "🎨 美术",
    "Audio": "🎵 音频",
    "Design": "🎮 设计",
    "Dev Guides": "📖 开发指南",
    "Tech": "🖥️ 技术",
    "Unity Standards": "📋 规范",
}

# Groups (分组)
GROUP_MAPPING = {
    # Art
    "Tech Art": "技术美术",
    "UI/UX": "界面设计",
    "VFX": "视觉特效",
    "其他": "其他",
    
    # Design
    "Case Studies": "案例研究",
    "Content": "内容设计",
    "LiveOps": "运营系统",
    "Mechanics": "游戏机制",
    "Narrative": "叙事设计",
    "Numerical": "数值体系",
    "Philosophy & Systems": "设计哲学",
    "Product Strategy": "产品策略",
    "Production": "制作流程",
    "Psychology": "心理学",
    "Systems": "游戏系统",
    "UX": "用户体验",
    "Game Knowledge Maps": "🎲 游戏案例图谱",
    
    # Dev Guides
    "Art Pipeline": "美术流水线",
    "Collaboration": "团队协作",
    "Community": "社区运营",
    "Debugging": "调试技巧",
    "Industry Cases": "行业案例",
    "Failure Analysis": "💀 失败复盘",
    "Publishing": "发行上线",
    "Technical Implementation": "技术实现",
    "Testing": "测试",
    "Tools": "工具",
    
    # Tech
    "Algorithms": "算法",
    "Architecture": "架构",
    "Code Snippets": "代码片段",
    "Graphics": "图形渲染",
    "Math": "数学",
    "Mechanics": "机制实现",  # Tech 下的 Mechanics
    "Mobile Optimization": "移动优化",
    "Optimization": "性能优化",
    "Core": "核心系统",
}


def translate_tab(tab_name: str) -> str:
    """翻译 Tab 名称"""
    return TAB_MAPPING.get(tab_name, tab_name)


def translate_group(group_name: str) -> str:
    """翻译 Group 名称"""
    return GROUP_MAPPING.get(group_name, group_name)


def process_navigation(nav: dict) -> dict:
    """处理整个导航结构"""
    new_nav = deepcopy(nav)
    
    if "tabs" not in new_nav:
        return new_nav
    
    for tab in new_nav["tabs"]:
        # 翻译 Tab 名称
        if "tab" in tab:
            old_tab = tab["tab"]
            tab["tab"] = translate_tab(old_tab)
            if old_tab != tab["tab"]:
                print(f"  Tab: '{old_tab}' → '{tab['tab']}'")
        
        # 翻译 Groups
        if "groups" in tab:
            for group in tab["groups"]:
                if "group" in group:
                    old_group = group["group"]
                    group["group"] = translate_group(old_group)
                    if old_group != group["group"]:
                        print(f"    Group: '{old_group}' → '{group['group']}'")
    
    return new_nav


def main():
    # 检查参数
    dry_run = "--dry-run" in sys.argv
    
    # 路径
    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    docs_json_path = project_root / "docs.json"
    
    if not docs_json_path.exists():
        print(f"❌ 找不到 docs.json: {docs_json_path}")
        sys.exit(1)
    
    print(f"📖 读取 docs.json: {docs_json_path}")
    
    # 读取 JSON
    with open(docs_json_path, "r", encoding="utf-8") as f:
        docs_config = json.load(f)
    
    # 处理导航
    print("\n🔄 翻译导航标题...\n")
    
    if "navigation" in docs_config:
        docs_config["navigation"] = process_navigation(docs_config["navigation"])
    else:
        print("⚠️ 未找到 navigation 字段")
        sys.exit(1)
    
    # 输出或写入
    if dry_run:
        print("\n📋 [DRY-RUN] 预览新的 docs.json:\n")
        print(json.dumps(docs_config, ensure_ascii=False, indent=4))
        print("\n✅ [DRY-RUN] 完成预览，未写入文件")
    else:
        # 写入文件
        with open(docs_json_path, "w", encoding="utf-8") as f:
            json.dump(docs_config, ensure_ascii=False, indent=4, fp=f)
        
        print(f"\n✅ 已更新 docs.json")
        print("💡 建议运行 prettier 格式化: npx prettier --write docs.json")


if __name__ == "__main__":
    main()
