"""
VitePress HTML 语法检查和修复脚本
扫描所有 Markdown 文件，查找可能导致 VitePress 构建失败的 HTML 语法问题
"""

import os
import re
from pathlib import Path

DOCS_DIR = Path(r"i:\MTSVN_NEW\002_Vampirefall\Server\Game_Num_Basics_And_Calc\docs")

# 需要转义的模式
PATTERNS_TO_FIX = [
    # 泛型语法: List<String>, Dictionary<K,V> 等
    (r'(?<!`)(?<!``)(?<!```)(\w+)<(\w+(?:,\s*\w+)*)>(?!`)', r'`\1<\2>`'),
    # 自定义标签在代码块外: <c=xxx>, <l=xxx>, <s=xxx>
    (r'(?<!`)(?<!``)(?<!```)(<[cls]=\w+>)', r'`\1`'),
    (r'(?<!`)(?<!``)(?<!```)(<\/[cls]>)', r'`\1`'),
]

def is_in_code_block(content, pos):
    """检查位置是否在代码块内"""
    # 简单检查：统计之前的 ``` 数量
    before = content[:pos]
    triple_backticks = before.count('```')
    return triple_backticks % 2 == 1

def scan_file(filepath):
    """扫描单个文件，返回发现的问题"""
    issues = []
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            lines = content.split('\n')
    except Exception as e:
        return [f"无法读取文件: {e}"]
    
    for i, line in enumerate(lines, 1):
        # 跳过代码块内的行
        pos = content.find(line)
        if is_in_code_block(content, pos):
            continue
        
        # 检查泛型语法
        generics = re.findall(r'(?<!`)(\w+<\w+(?:,\s*\w+)*>)(?!`)', line)
        for g in generics:
            issues.append(f"  行 {i}: 泛型语法未转义: {g}")
        
        # 检查自定义标签
        custom_tags = re.findall(r'(?<!`)(<[cls]=\w+>|<\/[cls]>)(?!`)', line)
        for t in custom_tags:
            issues.append(f"  行 {i}: 自定义标签未转义: {t}")
        
        # 检查不完整的 HTML 标签
        unclosed = re.findall(r'<(\w+)[^>]*>(?!.*<\/\1>)', line)
        for u in unclosed:
            if u.lower() not in ['br', 'hr', 'img', 'input', 'link', 'meta']:
                # 排除自闭合标签
                if not re.search(rf'<{u}[^>]*/>', line):
                    issues.append(f"  行 {i}: 可能未闭合的标签: <{u}>")
    
    return issues

def main():
    print("扫描 VitePress HTML 语法问题...")
    print("=" * 60)
    
    all_issues = {}
    
    for md_file in DOCS_DIR.rglob("*.md"):
        # 跳过 .vitepress 目录
        if ".vitepress" in str(md_file):
            continue
        
        issues = scan_file(md_file)
        if issues:
            rel_path = md_file.relative_to(DOCS_DIR)
            all_issues[str(rel_path)] = issues
    
    if all_issues:
        print(f"\n发现 {len(all_issues)} 个文件有潜在问题:\n")
        for filepath, issues in sorted(all_issues.items()):
            print(f"[FILE] {filepath}")
            for issue in issues[:5]:  # 每个文件最多显示5个问题
                print(issue)
            if len(issues) > 5:
                print(f"  ... 还有 {len(issues) - 5} 个问题")
            print()
    else:
        print("✅ 未发现明显问题")

if __name__ == "__main__":
    main()
