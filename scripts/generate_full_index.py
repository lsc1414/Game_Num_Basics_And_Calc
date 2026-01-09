#!/usr/bin/env python3
"""
generate_full_index.py

扫描 docs 目录并生成 Full_Index.md 文件。
按目录结构组织，提取每个文件的 H1 标题。

Usage:
    python scripts/generate_full_index.py
"""

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

# 忽略的目录
IGNORED_DIRS = {'.vitepress', 'assets', 'javascripts', 'stylesheets', 'Research'}

# 忽略的文件
IGNORED_FILES = {'index.md', 'START_HERE.md', 'Full_Index.md'}

# 目录中文名映射
DIR_CN_NAMES = {
    'Art': '🎨 美术',
    'Audio': '🎵 音频',
    'Design': '🎮 设计',
    'Dev_Guides': '📖 开发指南',
    'Tech': '🖥️ 技术',
    'Unity_Standards': '📋 规范',
    'Case_Studies': '📖 案例研究',
    'Guides': '📚 指南',
    'Tools': '🛠️ 工具',
    
    # 二级目录
    'Tech_Art': '技术美术',
    'UI_UX': '界面设计',
    'VFX': '视觉特效',
    'Content': '内容设计',
    'LiveOps': '运营系统',
    'Mechanics': '机制',
    'Narrative': '叙事设计',
    'Numerical': '数值体系',
    'Philosophy_And_Systems': '设计哲学',
    'Product_Strategy': '产品策略',
    'Production': '制作流程',
    'Psychology': '心理学',
    'Systems': '游戏系统',
    'UX': '用户体验',
    'CaseStudies': '案例分析',
    'Art_Pipeline': '美术流水线',
    'Collaboration': '团队协作',
    'Community': '社区运营',
    'Debugging': '调试技巧',
    'Industry_Cases': '行业案例',
    'Failure_Analysis': '失败复盘',
    'Publishing': '发行上线',
    'Technical_Implementation': '技术实现',
    'Testing': '测试',
    'Algorithms': '算法',
    'Architecture': '架构',
    'Code_Snippets': '代码片段',
    'Graphics': '图形渲染',
    'Math': '数学',
    'Mobile_Optimization': '移动优化',
    'Optimization': '性能优化',
    'Performance': '性能',
    
    # Case_Studies 子目录
    'Roguelike': '🎲 Roguelike',
    'Tower_Defense': '🏰 塔防',
    'Hybrid': '⚔️ 混合类型',
    'Failure': '💀 失败复盘',
    'Sandbox': '🏭 沙盒建造',
    'Magic_System': '🔮 魔法系统',
    'Coop': '👥 合作游戏',
    'Survivors': '🧛 幸存者类',
}


def get_h1_title(file_path: Path) -> str:
    """提取 Markdown 文件的 H1 标题"""
    try:
        content = file_path.read_text(encoding='utf-8')
        match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
        if match:
            return match.group(1).strip()
    except:
        pass
    return file_path.stem.replace('_', ' ')


def scan_docs(docs_path: Path) -> Dict[str, List[Tuple[Path, str]]]:
    """扫描 docs 目录，返回按目录分组的文件列表"""
    files_by_dir = defaultdict(list)
    
    for md_file in sorted(docs_path.rglob('*.md')):
        # 跳过忽略的文件
        if md_file.name in IGNORED_FILES:
            continue
        
        # 跳过忽略的目录
        rel_path = md_file.relative_to(docs_path)
        parts = rel_path.parts
        if any(p in IGNORED_DIRS for p in parts):
            continue
        
        # 获取目录路径 (不含文件名)
        if len(parts) > 1:
            dir_key = '/'.join(parts[:-1])
        else:
            dir_key = '.'
        
        title = get_h1_title(md_file)
        files_by_dir[dir_key].append((rel_path, title))
    
    return dict(files_by_dir)


def get_dir_display_name(dir_path: str) -> str:
    """获取目录的显示名称"""
    parts = dir_path.split('/')
    names = []
    for p in parts:
        cn_name = DIR_CN_NAMES.get(p, p.replace('_', ' '))
        names.append(cn_name)
    return ' / '.join(names)


def generate_index(files_by_dir: Dict[str, List[Tuple[Path, str]]]) -> str:
    """生成 Full_Index.md 内容"""
    lines = [
        '# 📚 全站索引',
        '',
        '> 本索引根据 `docs/` 目录结构自动生成。',
        '',
    ]
    
    # 按目录路径排序
    sorted_dirs = sorted(files_by_dir.keys())
    
    current_top_level = None
    
    for dir_path in sorted_dirs:
        files = files_by_dir[dir_path]
        
        if dir_path == '.':
            # 根目录文件
            lines.append('## 📄 根目录')
            lines.append('')
            for rel_path, title in sorted(files, key=lambda x: x[1]):
                link = str(rel_path).replace('\\', '/')
                lines.append(f'- [{title}]({link})')
            lines.append('')
        else:
            parts = dir_path.split('/')
            top_level = parts[0]
            
            # 顶级目录标题
            if top_level != current_top_level:
                current_top_level = top_level
                cn_name = DIR_CN_NAMES.get(top_level, top_level)
                lines.append(f'## {cn_name}')
                lines.append('')
            
            # 子目录标题
            if len(parts) > 1:
                sub_name = get_dir_display_name('/'.join(parts[1:]))
                lines.append(f'### {sub_name}')
                lines.append('')
            
            # 文件列表
            for rel_path, title in sorted(files, key=lambda x: x[1]):
                link = str(rel_path).replace('\\', '/')
                lines.append(f'- [{title}]({link})')
            lines.append('')
    
    return '\n'.join(lines)


def main():
    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    docs_path = project_root / 'docs'
    output_path = docs_path / 'Full_Index.md'
    
    if not docs_path.exists():
        print('❌ docs 目录不存在')
        sys.exit(1)
    
    print('📂 扫描 docs 目录...')
    files_by_dir = scan_docs(docs_path)
    
    total_files = sum(len(files) for files in files_by_dir.values())
    print(f'  发现 {len(files_by_dir)} 个目录, {total_files} 个文件')
    
    print('\n📝 生成 Full_Index.md...')
    content = generate_index(files_by_dir)
    
    output_path.write_text(content, encoding='utf-8')
    print(f'✅ 已保存到 {output_path}')


if __name__ == '__main__':
    main()
