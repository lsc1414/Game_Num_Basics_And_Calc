"""分析所有 docs 目录下 md 文件的 H1 标题"""
import os
import re
import sys

# 设置输出编码
sys.stdout.reconfigure(encoding='utf-8')

docs_dir = 'docs'
results = []

for root, dirs, files in os.walk(docs_dir):
    for f in sorted(files):
        if f.endswith('.md'):
            filepath = os.path.join(root, f)
            rel_path = os.path.relpath(filepath, docs_dir)
            try:
                with open(filepath, 'r', encoding='utf-8') as file:
                    content = file.read()
                    match = re.search(r'^# (.+)$', content, re.MULTILINE)
                    h1 = match.group(1) if match else "**NO H1 FOUND**"
                    results.append(f"{rel_path}|{h1}")
            except Exception as e:
                results.append(f"{rel_path}|ERROR: {e}")

# 打印结果
for r in results:
    print(r)
