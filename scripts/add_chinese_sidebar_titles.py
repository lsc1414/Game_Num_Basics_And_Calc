#!/usr/bin/env python3
"""
add_chinese_sidebar_titles.py

为所有 Markdown 文件添加中文 sidebarTitle frontmatter。
Mintlify 使用 sidebarTitle 控制侧边栏显示的标题。

Usage:
    python scripts/add_chinese_sidebar_titles.py [--dry-run]
"""

import sys
import io
import re
from pathlib import Path
from typing import Optional, Tuple

# Windows 控制台 UTF-8 支持
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

# 忽略的文件
IGNORED_FILES = {'index.md', 'portal.html'}

# 忽略的目录
IGNORED_DIRS = {'.vitepress', 'assets', 'javascripts', 'stylesheets', 'Research'}


def extract_title(content: str) -> Optional[str]:
    """从内容中提取 H1 标题"""
    match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
    if match:
        return match.group(1).strip()
    return None


def extract_chinese_title(title: str) -> str:
    """从标题中提取中文部分，或返回原标题"""
    if not title:
        return title
    
    # 如果标题已经全是中文，直接返回
    if re.match(r'^[\u4e00-\u9fff\s\d\(\)（）：:、，。！？]+$', title):
        return title
    
    # 尝试匹配 "中文标题 (English Title)" 格式
    match = re.match(r'^(.+?)\s*[\(（].*[\)）]\s*$', title)
    if match:
        chinese_part = match.group(1).strip()
        # 如果包含中文字符，使用中文部分
        if re.search(r'[\u4e00-\u9fff]', chinese_part):
            return chinese_part
    
    # 尝试匹配 "Emoji 中文标题" 格式 (移除 emoji 后的部分)
    match = re.match(r'^[\U0001F300-\U0001F9FF\s🧙‍♂️👶⚔️⛏️🌧️🌲🏰👥💰📈📧🗺️🛡️🪄]+\s*(.+)$', title)
    if match:
        remaining = match.group(1).strip()
        # 提取中文部分
        cn_match = re.match(r'^(.+?)\s*[\(（]', remaining)
        if cn_match:
            return cn_match.group(1).strip()
        return remaining
    
    return title


def has_frontmatter(content: str) -> bool:
    """检查内容是否已有 frontmatter"""
    return content.strip().startswith('---')


def get_existing_frontmatter(content: str) -> Tuple[str, str]:
    """提取现有的 frontmatter 和正文内容"""
    if not has_frontmatter(content):
        return "", content
    
    # 匹配 frontmatter 块
    match = re.match(r'^---\s*\n(.*?)\n---\s*\n(.*)$', content, re.DOTALL)
    if match:
        return match.group(1), match.group(2)
    return "", content


def add_sidebar_title(content: str, sidebar_title: str) -> str:
    """添加 sidebarTitle 到 frontmatter"""
    existing_fm, body = get_existing_frontmatter(content)
    
    # 检查是否已有 sidebarTitle
    if 'sidebarTitle' in existing_fm:
        return content
    
    # 构建新的 frontmatter
    if existing_fm:
        new_fm = existing_fm.rstrip() + f'\nsidebarTitle: "{sidebar_title}"'
    else:
        new_fm = f'sidebarTitle: "{sidebar_title}"'
    
    return f'---\n{new_fm}\n---\n\n{body.lstrip()}'


def process_file(file_path: Path, dry_run: bool) -> bool:
    """处理单个文件，返回是否有更改"""
    try:
        content = file_path.read_text(encoding='utf-8')
    except:
        return False
    
    # 检查是否已有 sidebarTitle
    if 'sidebarTitle' in content[:500]:
        return False
    
    # 提取标题
    title = extract_title(content)
    if not title:
        return False
    
    # 获取中文标题
    chinese_title = extract_chinese_title(title)
    
    # 如果中文标题和原标题相同且没有中文，跳过
    if chinese_title == title and not re.search(r'[\u4e00-\u9fff]', title):
        # 对于纯英文标题，尝试使用文件名生成
        basename = file_path.stem.replace('_', ' ')
        chinese_title = basename
    
    # 添加 sidebarTitle
    new_content = add_sidebar_title(content, chinese_title)
    
    if new_content == content:
        return False
    
    if dry_run:
        print(f"  [+] {file_path.name}")
        print(f"      sidebarTitle: \"{chinese_title}\"")
    else:
        file_path.write_text(new_content, encoding='utf-8')
        print(f"  ✓ {file_path.name} → \"{chinese_title}\"")
    
    return True


def main():
    dry_run = "--dry-run" in sys.argv
    
    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    docs_path = project_root / "docs"
    
    print("=" * 60)
    if dry_run:
        print("📝 添加中文侧边栏标题 [DRY-RUN]")
    else:
        print("📝 添加中文侧边栏标题")
    print("=" * 60)
    
    updated = 0
    total = 0
    
    for md_file in sorted(docs_path.rglob("*.md")):
        # 跳过忽略的文件
        if md_file.name in IGNORED_FILES:
            continue
        
        # 跳过忽略的目录
        rel_path = md_file.relative_to(docs_path)
        if any(p in IGNORED_DIRS for p in rel_path.parts):
            continue
        
        total += 1
        if process_file(md_file, dry_run):
            updated += 1
    
    print(f"\n共处理 {total} 个文件，更新 {updated} 个")
    
    if dry_run:
        print("\n✅ [DRY-RUN] 预览完成")
    else:
        print("\n✅ 完成! 建议运行 prettier 格式化后提交")


if __name__ == "__main__":
    main()
