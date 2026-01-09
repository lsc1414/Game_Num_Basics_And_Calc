"""
批量重构 docs 目录下所有 md 文件的 H1 标题
规则：
1. 移除括号中的英文翻译
2. 精简冗余后缀（深度研究、详解等）
"""
import os
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

docs_dir = 'docs'
dry_run = '--dry-run' in sys.argv  # 预览模式

# 需要移除的英文括号模式
ENGLISH_BRACKET_PATTERN = re.compile(r'\s*[\(（][A-Za-z0-9\s&\-\.:\'\"]+[\)）]$')

# 需要精简的冗余后缀（按优先级排序）
REDUNDANT_SUFFIXES = [
    '深度研究',
    '详解',
    # '指南',  # 保留，因为有些是真正的指南
]

def clean_h1(h1_content: str) -> str:
    """清理 H1 标题内容"""
    original = h1_content
    
    # 1. 移除末尾的英文括号翻译
    h1_content = ENGLISH_BRACKET_PATTERN.sub('', h1_content)
    
    # 2. 精简冗余后缀（仅当标题足够长时）
    for suffix in REDUNDANT_SUFFIXES:
        if h1_content.endswith(suffix) and len(h1_content) > 15:
            h1_content = h1_content[:-len(suffix)].rstrip()
    
    return h1_content

def process_file(filepath: str) -> tuple[bool, str, str]:
    """处理单个文件，返回 (是否修改, 原标题, 新标题)"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 查找 H1 标题
    match = re.search(r'^(# )(.+)$', content, re.MULTILINE)
    if not match:
        return False, '', ''
    
    original_h1 = match.group(2)
    new_h1 = clean_h1(original_h1)
    
    if original_h1 == new_h1:
        return False, original_h1, new_h1
    
    # 替换标题
    new_content = content[:match.start()] + f'# {new_h1}' + content[match.end():]
    
    if not dry_run:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
    
    return True, original_h1, new_h1

def main():
    modified_count = 0
    results = []
    
    for root, dirs, files in os.walk(docs_dir):
        for f in sorted(files):
            if f.endswith('.md'):
                filepath = os.path.join(root, f)
                rel_path = os.path.relpath(filepath, docs_dir)
                
                try:
                    modified, old_h1, new_h1 = process_file(filepath)
                    if modified:
                        modified_count += 1
                        results.append((rel_path, old_h1, new_h1))
                except Exception as e:
                    print(f"❌ 错误处理 {rel_path}: {e}")
    
    # 输出结果
    print(f"\n{'[预览模式] ' if dry_run else ''}共修改 {modified_count} 个文件:\n")
    for rel_path, old_h1, new_h1 in results:
        print(f"📝 {rel_path}")
        print(f"   旧: {old_h1}")
        print(f"   新: {new_h1}\n")

if __name__ == '__main__':
    main()
