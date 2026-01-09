#!/usr/bin/env python3
"""
Batch fix script to restore \\text{if} and similar incorrectly escaped
code keywords back to their original form inside code blocks.

这个脚本用于修复因 mintlify_helper.py lint bug 导致的代码块内
\\text{if} 等错误转换。
"""

import re
import sys
from pathlib import Path

# 被错误转换的函数列表
FUNCTIONS_TO_RESTORE = [
    'saturate', 'lerp', 'step', 'smoothstep', 'frac', 'floor', 'ceil',
    'tex2D', 'tex2DLod', 'dot', 'cross', 'normalize', 'length', 'distance',
    'clamp', 'abs', 'pow', 'exp', 'log', 'sqrt', 'min', 'max', 'round',
    'atan2', 'if', 'discard'
]

def restore_code_blocks(content: str) -> str:
    """
    在代码块 (```...```) 中恢复被错误转换的 \\text{func} 为 func
    """
    # 匹配代码块
    code_block_pattern = re.compile(r'(```[\w]*\n)(.*?)(```)', re.DOTALL)
    
    def fix_code_block(match):
        prefix = match.group(1)  # ```language\n
        code = match.group(2)     # actual code
        suffix = match.group(3)   # ```
        
        # 恢复所有被错误转换的函数名
        for func in FUNCTIONS_TO_RESTORE:
            # \text{if} -> if
            code = code.replace(f'\\text{{{func}}}', func)
        
        return prefix + code + suffix
    
    return code_block_pattern.sub(fix_code_block, content)


def restore_inline_code(content: str) -> str:
    """
    在行内代码 (`...`) 中恢复被错误转换的 \\text{func} 为 func
    """
    # 匹配行内代码 (不跨行)
    inline_code_pattern = re.compile(r'`([^`\n]+)`')
    
    def fix_inline(match):
        code = match.group(1)
        for func in FUNCTIONS_TO_RESTORE:
            code = code.replace(f'\\text{{{func}}}', func)
        return f'`{code}`'
    
    return inline_code_pattern.sub(fix_inline, content)


def process_file(file_path: Path, dry_run: bool = False) -> bool:
    """处理单个文件，返回是否有修改"""
    # 尝试多种编码
    encodings = ['utf-8-sig', 'utf-8', 'gbk', 'latin-1']
    content = None
    
    for encoding in encodings:
        try:
            content = file_path.read_text(encoding=encoding)
            break
        except (UnicodeDecodeError, LookupError):
            continue
    
    if content is None:
        print(f"Warning: Could not decode {file_path}, skipping")
        return False
    
    original = content
    
    # 修复代码块和行内代码
    content = restore_code_blocks(content)
    content = restore_inline_code(content)
    
    if content != original:
        if not dry_run:
            file_path.write_text(content, encoding='utf-8')
        return True
    return False


def main():
    docs_dir = Path('docs')
    if not docs_dir.exists():
        print("Error: docs/ directory not found")
        sys.exit(1)
    
    dry_run = '--dry-run' in sys.argv
    
    if dry_run:
        print("=== DRY RUN MODE ===\n")
    
    fixed_files = []
    
    for md_file in docs_dir.rglob('*.md'):
        if process_file(md_file, dry_run):
            fixed_files.append(md_file)
            print(f"{'Would fix' if dry_run else 'Fixed'}: {md_file}")
    
    print(f"\n{'Would fix' if dry_run else 'Fixed'} {len(fixed_files)} file(s)")
    
    if dry_run and fixed_files:
        print("\nRun without --dry-run to apply fixes.")


if __name__ == "__main__":
    main()
