"""
同步 mkdocs.yml 导航标题
使用正则表达式直接处理，避免 yaml python tag 问题
"""
import os
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

docs_dir = 'docs'
mkdocs_file = 'mkdocs.yml'

def get_h1_title(md_path: str) -> str | None:
    """获取 md 文件的 H1 标题"""
    full_path = os.path.join(docs_dir, md_path)
    if not os.path.exists(full_path):
        return None
    
    with open(full_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    match = re.search(r'^# (.+)$', content, re.MULTILINE)
    return match.group(1) if match else None

def main():
    with open(mkdocs_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 匹配 nav 中的 "标题: 路径.md" 模式
    # 格式: - 标题: 路径.md 或 - 标题: 路径.md (带缩进)
    pattern = re.compile(r'^(\s*-\s*)(.+?):\s*([\w/\\]+\.md)\s*$', re.MULTILINE)
    
    modified = []
    
    def replacer(match):
        indent = match.group(1)
        old_title = match.group(2).strip()
        md_path = match.group(3).strip()
        
        h1 = get_h1_title(md_path)
        if h1 and h1 != old_title:
            modified.append((md_path, old_title, h1))
            return f'{indent}{h1}: {md_path}'
        return match.group(0)
    
    new_content = pattern.sub(replacer, content)
    
    if modified:
        print(f"将同步 {len(modified)} 个导航标题:\n")
        for path, old, new in modified[:30]:
            print(f"  📝 {path}")
            print(f"     旧: {old}")
            print(f"     新: {new}\n")
        
        if len(modified) > 30:
            print(f"  ... 还有 {len(modified) - 30} 个")
        
        with open(mkdocs_file, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"\n✅ 已更新 {mkdocs_file}")
    else:
        print("导航标题已是最新，无需修改")

if __name__ == '__main__':
    main()
