"""
修复被 vitepress_html_fix.py 脚本意外破坏的反引号格式
模式：`text.`Generic<T>` -> `text.Generic<T>`
"""

import os
import re
from pathlib import Path

DOCS_DIR = Path(r"i:\MTSVN_NEW\002_Vampirefall\Server\Game_Num_Basics_And_Calc\docs")

def fix_broken_backticks(filepath):
    """修复被破坏的反引号格式"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"无法读取 {filepath}: {e}")
        return False, 0
    
    original = content
    
    # 模式1: `xxx.`Generic<T>`(yyy)` -> `xxx.Generic<T>(yyy)`
    # 匹配: 反引号开始 + 文本 + 反引号 + 泛型 + 反引号 + 可选括号内容 + 反引号
    pattern1 = r'`([^`]+\.)`([A-Za-z_]\w*<[^>]+>)`(\([^)]*\))?`'
    content = re.sub(pattern1, r'`\1\2\3`', content)
    
    # 模式2: `prefix `Type<T>`` -> `prefix Type<T>`  
    # 匹配: 反引号 + 可选空格 + 反引号 + 泛型 + 反引号 + 反引号
    pattern2 = r'`([^`]+) `([A-Za-z_]\w*<[^>]+>)``'
    content = re.sub(pattern2, r'`\1 \2`', content)
    
    # 模式3: `new `List<T>`()` -> `new List<T>()`
    pattern3 = r'`(new )`([A-Za-z_]\w*<[^>]+>)`(\([^)]*\))`'
    content = re.sub(pattern3, r'`\1\2\3`', content)
    
    # 模式4: `@`FindObjectOfType<T>`()` -> `@FindObjectOfType<T>()`
    pattern4 = r'`(@)`([A-Za-z_]\w*<[^>]+>)`(\([^)]*\))`'
    content = re.sub(pattern4, r'`\1\2\3`', content)
    
    # 模式5: Dictionary<int, `List<Entity>`> -> `Dictionary<int, List<Entity>>`
    pattern5 = r'`([A-Za-z_]\w*<[^,>]+, )`([A-Za-z_]\w*<[^>]+>)`>'
    content = re.sub(pattern5, r'`\1\2>`', content)
    
    # 模式6: `static event `Action<T>` -> `static event Action<T>`
    pattern6 = r'`([^`]+ )`([A-Za-z_]\w*<[^>]+>)`'
    content = re.sub(pattern6, r'`\1\2`', content)
    
    if content != original:
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            return True, content.count('`') - original.count('`')
        except Exception as e:
            print(f"无法写入 {filepath}: {e}")
            return False, 0
    
    return False, 0

def main():
    print("修复被破坏的反引号格式...")
    print("=" * 60)
    
    total_files = 0
    
    for md_file in DOCS_DIR.rglob("*.md"):
        if ".vitepress" in str(md_file):
            continue
        
        modified, _ = fix_broken_backticks(md_file)
        if modified:
            rel_path = md_file.relative_to(DOCS_DIR)
            print(f"[FIXED] {rel_path}")
            total_files += 1
    
    print(f"\n完成! 修复了 {total_files} 个文件")

if __name__ == "__main__":
    main()
