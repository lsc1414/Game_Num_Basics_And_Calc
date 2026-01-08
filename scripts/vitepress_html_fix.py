"""
VitePress HTML 语法自动修复脚本
在代码块外的泛型语法添加反引号转义
"""

import os
import re
from pathlib import Path

DOCS_DIR = Path(r"i:\MTSVN_NEW\002_Vampirefall\Server\Game_Num_Basics_And_Calc\docs")

def is_in_code_block(lines, line_idx):
    """检查该行是否在代码块内"""
    in_code = False
    for i in range(line_idx):
        if lines[i].strip().startswith('```'):
            in_code = not in_code
    return in_code

def fix_file(filepath):
    """修复单个文件中的泛型语法"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    except Exception as e:
        print(f"无法读取 {filepath}: {e}")
        return False, 0
    
    modified = False
    fix_count = 0
    
    for i, line in enumerate(lines):
        # 跳过代码块内的行
        if is_in_code_block(lines, i):
            continue
        
        # 跳过以 ``` 开头的行
        if line.strip().startswith('```'):
            continue
        
        original = line
        
        # 修复泛型语法: List<String> -> `List<String>`
        # 但不修复已经在反引号中的
        # 匹配模式: 非反引号 + 泛型 + 非反引号
        patterns = [
            # 完整泛型: List<String>, Dictionary<K, V>
            (r'(?<![`\w])([A-Za-z_]\w*<[A-Za-z_]\w*(?:,\s*[A-Za-z_]\w*)*>)(?![`\w])', r'`\1`'),
            # <字符串> 形式
            (r'(?<![`\w])(<[A-Za-z_]\w+>)(?![`\w])', r'`\1`'),
        ]
        
        for pattern, replacement in patterns:
            line = re.sub(pattern, replacement, line)
        
        if line != original:
            lines[i] = line
            modified = True
            fix_count += 1
    
    if modified:
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.writelines(lines)
            return True, fix_count
        except Exception as e:
            print(f"无法写入 {filepath}: {e}")
            return False, 0
    
    return False, 0

def main():
    print("自动修复 VitePress HTML 语法问题...")
    print("=" * 60)
    
    total_files = 0
    total_fixes = 0
    
    for md_file in DOCS_DIR.rglob("*.md"):
        # 跳过 .vitepress 目录
        if ".vitepress" in str(md_file):
            continue
        
        modified, fixes = fix_file(md_file)
        if modified:
            rel_path = md_file.relative_to(DOCS_DIR)
            print(f"[FIXED] {rel_path} ({fixes} fixes)")
            total_files += 1
            total_fixes += fixes
    
    print(f"\n完成! 修复了 {total_files} 个文件中的 {total_fixes} 处问题")

if __name__ == "__main__":
    main()
