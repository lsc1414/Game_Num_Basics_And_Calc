import os
import re
import json

docs_path = r'i:\MTSVN_NEW\002_Vampirefall\Server\Game_Num_Basics_And_Calc\docs'
portal_file = os.path.join(docs_path, 'portal.html')

# Category mapping
CAT_MAP = {
    'Design/Numerical': 'math',
    'Design/Mechanics': 'combat',
    'Design/Systems': 'combat',
    'Design/Content': 'design',
    'Design/Philosophy': 'design',
    'Design/Narrative': 'design',
    'Design/Psychology': 'design',
    'Design/UX': 'design',
    'Design/LiveOps': 'publish',
    'Design/Product_Strategy': 'publish',
    'Design/Production': 'tools',
    'Design/CaseStudies': 'knowledge',
    'Design/Calculator': 'tools',
    'Dev_Guides/Publishing': 'publish',
    'Dev_Guides/Tools': 'tools',
    'Dev_Guides/Debugging': 'tools',
    'Dev_Guides/Technical_Implementation': 'arch',
    'Dev_Guides/Collaboration': 'standard',
    'Dev_Guides/Art_Pipeline': 'art',
    'Dev_Guides/Industry_Cases': 'knowledge',
    'Dev_Guides/Failure_Cases': 'postmortem',
    'Tech/Architecture': 'arch',
    'Tech/AI': 'ai',
    'Tech/Algorithms': 'ai',
    'Tech/Optimization': 'arch',
    'Tech/Graphics': 'art',
    'Tech/Mechanics': 'combat',
    'Tech/Math': 'math',
    'Art': 'art',
    'Audio': 'audio',
    'Unity_Standards': 'standard',
}

def get_cat(rel_path):
    rel_path = rel_path.replace('\\', '/')
    if 'Knowledge_Map' in rel_path:
        return 'knowledge'
    for prefix, cat in CAT_MAP.items():
        if rel_path.startswith(prefix):
            return cat
    if rel_path.startswith('Design/'):
        return 'design'
    if rel_path.startswith('Tech/'):
        return 'arch'
    if rel_path.startswith('Dev_Guides/'):
        return 'tools'
    return 'knowledge'

def get_title(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                if line.strip().startswith('# '):
                    title = line.strip()[2:].strip()
                    return title
    except:
        pass
    return os.path.basename(file_path).replace('.md', '').replace('_', ' ')

# 1. Read existing portal docs to preserve metadata
with open(portal_file, 'r', encoding='utf-8') as f:
    portal_content = f.read()

existing_docs = {}
# Regex to match doc objects - updated to be more robust
doc_pattern = re.compile(r'\{\s*title:\s*"((?:\\.|[^"])*)",\s*path:\s*"([^"]+)",\s*cat:\s*"([^"]*)",\s*desc:\s*"((?:\\.|[^"])*)",\s*role:\s*(\[[^\]]*\]),?\s*\}', re.DOTALL)
for match in doc_pattern.finditer(portal_content):
    title, path, cat, desc, role = match.groups()
    # Normalize path to .md style for matching
    # Handle both .html and directory style /
    norm_path = path
    if norm_path.endswith('.html'):
        norm_path = norm_path.replace('.html', '.md')
    elif norm_path.endswith('/'):
        norm_path = norm_path[:-1] + '.md'
    else:
        norm_path = norm_path + '.md'
    
    existing_docs[norm_path] = {'title': title, 'cat': cat, 'desc': desc, 'role': role}

# 2. Scan all .md files (and Design/Calculator/index.html)
all_files = []
for root, dirs, files in os.walk(docs_path):
    for file in files:
        if file.endswith('.md') and file not in ['index.md', 'START_HERE.md', 'GEMINI.md', 'readme.md']:
            full_path = os.path.join(root, file)
            rel_path = os.path.relpath(full_path, docs_path).replace('\\', '/')
            all_files.append((rel_path, full_path, 'md'))
        elif file == 'index.html' and 'Calculator' in root:
            full_path = os.path.join(root, file)
            rel_path = os.path.relpath(full_path, docs_path).replace('\\', '/')
            all_files.append((rel_path, full_path, 'html'))

# 3. Build new docs list
new_docs = []
for rel_path, full_path, ftype in all_files:
    if rel_path in existing_docs:
        doc = existing_docs[rel_path].copy()
        if ftype == 'md':
            doc['path'] = rel_path.replace('.md', '/')
        else:
            doc['path'] = rel_path
        new_docs.append(doc)
    else:
        # New file
        if ftype == 'md':
            title = get_title(full_path)
            path = rel_path.replace('.md', '/')
        else:
            title = "数值计算器"
            path = rel_path
        
        cat = get_cat(rel_path)
        new_docs.append({
            'title': title,
            'path': path,
            'cat': cat,
            'desc': f"来自 {os.path.dirname(rel_path)} 的相关文档。",
            'role': '["all"]'
        })

# Sort by category and title
new_docs.sort(key=lambda x: (x['cat'], x['title']))

# 4. Generate the JS code
def escape_js_string(s):
    return s.replace('"', '\\"')

js_docs = "const docs = [\n"
curr_cat = None
for doc in new_docs:
    if doc['cat'] != curr_cat:
        curr_cat = doc['cat']
        js_docs += f"        // {curr_cat}\n"
    
    js_docs += "        {\n"
    js_docs += f'          title: "{escape_js_string(doc["title"])}",\n'
    js_docs += f'          path: "{doc["path"]}",\n'
    js_docs += f'          cat: "{doc["cat"]}",\n'
    js_docs += f'          desc: "{escape_js_string(doc["desc"])}",\n'
    js_docs += f'          role: {doc["role"]},\n'
    js_docs += "        },\n"
js_docs += "      ];"

# 5. Replace the old docs list in portal.html
final_content = re.sub(r'const docs = \[.*?\];', js_docs, portal_content, flags=re.DOTALL)

with open(portal_file, 'w', encoding='utf-8') as f:
    f.write(final_content)

print(f"Updated portal.html with {len(new_docs)} documents.")
