import os
import re

docs_path = r'i:\MTSVN_NEW\002_Vampirefall\Server\Game_Num_Basics_And_Calc\docs'
portal_file = os.path.join(docs_path, 'portal.html')

with open(portal_file, 'r', encoding='utf-8') as f:
    content = f.read()

# Extract paths from the docs array
# Example: path: "Design/Numerical_Manual.html",
matches = re.findall(r'path:\s*"([^"]+)"', content)

missing = []
for p in matches:
    # Convert .html to .md or keep as is if it's already .html/index.html
    check_p = p
    if p.endswith('.html') and not p.endswith('index.html'):
        check_p = p[:-5] + '.md'
    
    full_path = os.path.join(docs_path, check_p.replace('/', os.sep))
    if not os.path.exists(full_path):
        missing.append((p, check_p))

if missing:
    print("Missing files:")
    for m, cp in missing:
        print(f"  - {m} (checked as {cp})")
else:
    print("All files found!")
