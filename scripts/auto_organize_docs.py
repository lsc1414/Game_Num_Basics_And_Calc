import os
import re
import sys
import io

# Fix unicode printing on Windows
if sys.stdout.encoding != 'utf-8':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Configuration
DOCS_DIR = 'docs'
MKDOCS_FILE = 'mkdocs.yml'
INDEX_FILE = 'docs/Full_Index.md'

# Files/Folders to exclude from the automatic index/nav
EXCLUDE_DIRS = {
    'assets', 'stylesheets', 'javascripts', 'theme', 'overrides', '.obsidian', '.git', '__pycache__', 'Research'
}
EXCLUDE_FILES = {
    'index.md', 'START_HERE.md', 'Full_Index.md', '.DS_Store'
}

# Root level files order (optional, forces specific files to be at top of nav)
ROOT_FILES_ORDER = [
    'index.md',
    'START_HERE.md',
    'Full_Index.md'
]

def has_chinese(text):
    """Check if text contains any Chinese characters."""
    return any('\u4e00' <= char <= '\u9fff' for char in text)

def clean_title(text):
    """
    Removes English phrases in parentheses from the title.
    Rules:
    1. Scans matched pattern: (Content)
    2. If Content has NO Chinese characters AND contains at least one space, remove it.
       - This preserves acronyms like (OOP), (GAS), (DOD) which usually have no spaces.
       - This removes translation phrases like (Aim Assist System) which have spaces.
    3. Cleans up extra spaces resulting from removal.
    4. Handles optional surrounding quotes.
    """
    quote_char = ''
    content_to_clean = text.strip()
    if len(content_to_clean) > 1 and ((content_to_clean.startswith('"') and content_to_clean.endswith('"')) or (content_to_clean.startswith("'") and content_to_clean.endswith("'"))):
        quote_char = content_to_clean[0]
        content_to_clean = content_to_clean[1:-1]

    def replacement_check(match):
        full_match = match.group(0)
        content = match.group(2) # The text inside parens
        
        # Condition to remove: No Chinese AND Has Space
        if not has_chinese(content) and ' ' in content:
            return '' # Remove entirely
        
        return full_match # Keep original

    new_content = re.sub(r'(\s?)\(([^)]+)\)', replacement_check, content_to_clean)
    new_content = re.sub(r'\s+', ' ', new_content).strip()
    
    return f"{quote_char}{new_content}{quote_char}"

def get_file_title(filepath):
    """Extracts title from the first H1 header in the file, or falls back to basename."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                match = re.match(r'^#\s+(.+)$', line)
                if match:
                    return clean_title(match.group(1).strip())
    except Exception as e:
        print(f"Warning: Could not read {filepath}: {e}")
    
    # Fallback to filename without extension
    name = os.path.splitext(os.path.basename(filepath))[0]
    return clean_title(name.replace('_', ' '))

def get_dir_title(dirpath):
    """
    Derive a display title for a directory.
    If the directory matches a known category in MkDocs (e.g. from previous manual config), 
    we could use that, but for now we just pretty print the directory name.
    """
    dirname = os.path.basename(dirpath)
    # Simple heuristic: Replace underscores with spaces, maybe capitalize?
    # But let's keep it simple and consistent.
    # If the directory name ends with parentheses mapping (e.g. "Design (策划)"), we might want to keep it?
    # But usually directories on disk are just "Design".
    # Let's try to find an index.md inside? Some setups do that.
    # For now, just return the name.
    return dirname

def build_tree(current_path, rel_path=''):
    """
    Recursively scans directory to build a tree structure.
    Returns a list of items.
    Item format: {'name': 'Title', 'path': 'path/to/file.md'} (Leaf)
              or {'name': 'Folder Name', 'children': [...]} (Node)
    """
    items = []
    
    try:
        entries = sorted(os.listdir(current_path))
    except OSError:
        return []

    # Separate files and directories for sorting/grouping preference
    files_list = []
    dirs_list = []

    for entry in entries:
        full_path = os.path.join(current_path, entry)
        entry_rel_path = os.path.join(rel_path, entry).replace('\\', '/')

        if os.path.isdir(full_path):
            if entry in EXCLUDE_DIRS:
                continue
            
            children = build_tree(full_path, entry_rel_path)
            if children: # Only add directory if it has content
                title = get_dir_title(full_path)
                dirs_list.append({
                    'name': title,
                    'children': children,
                    'is_dir': True
                })
        
        elif os.path.isfile(full_path):
            if entry in EXCLUDE_FILES or not entry.endswith('.md'):
                continue
            
            title = get_file_title(full_path)
            files_list.append({
                'name': title,
                'path': entry_rel_path,
                'is_dir': False
            })

    # Sort logic: You might want directories first, or mixed. 
    # Standard MkDocs typically mixes or puts folders at top.
    # Let's simple sort by name
    return sorted(files_list + dirs_list, key=lambda x: x['name'])


def generate_yaml_nav(tree, indent=0):
    lines = []
    prefix = "  " * indent
    for item in tree:
        if item.get('is_dir'):
            lines.append(f"{prefix}- {item['name']}:")
            lines.extend(generate_yaml_nav(item['children'], indent + 1))
        else:
            lines.append(f"{prefix}- {item['name']}: {item['path']}")
    return lines

def generate_markdown_index(tree, level=2):
    lines = []
    heading = "#" * level
    for item in tree:
        if item.get('is_dir'):
            # Directory - Make a header
            lines.append(f"\n{heading} {item['name']}\n")
            lines.extend(generate_markdown_index(item['children'], level + 1))
        else:
            # File - Make a link
            lines.append(f"- [{item['name']}]({item['path']})")
    return lines

def update_mkdocs_yml(nav_lines):
    # Read original file
    with open(MKDOCS_FILE, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Split content to preserve everything before 'nav:'
    # We look for the "nav:" key at the start of a line
    parts = re.split(r'(^nav:\s*\n)', content, maxsplit=1, flags=re.MULTILINE)
    
    if len(parts) >= 2:
        pre_nav = parts[0] + parts[1]
        # We ignore whatever was after nav:
    else:
        # If nav not found, append it
        pre_nav = content + "\nnav:\n"

    # Construct the new nav block
    # We need to manually add the ROOT_FILES_ORDER items first
    final_nav_lines = []
    
    # Check manual entries in original nav? No, we rebuild from scratch.
    # But we want specific root files to have nice names.
    
    # Special handling for root items to match current specific naming if desired
    # e.g. "游戏开发 101 🎮: index.md"
    # For now, let's just add them as is from ROOT_FILES_ORDER
    
    root_map = {
        'index.md': '游戏开发 101 🎮',
        'START_HERE.md': '🚀 新人上路指南',
        'Full_Index.md': '📚 全站索引'
    }

    for fname in ROOT_FILES_ORDER:
         if os.path.exists(os.path.join(DOCS_DIR, fname)):
             name = root_map.get(fname, fname)
             final_nav_lines.append(f"  - {name}: {fname}")

    # Add the generated tree
    # Note: nav_lines passed here are already indented for level 1 items? 
    # check generate_yaml_nav: it starts with indent=0 which means "- Name".
    # Under "nav:", we need indentation.
    
    for line in nav_lines:
        final_nav_lines.append(f"  {line}")

    new_content = pre_nav + "\n".join(final_nav_lines) + "\n"
    
    with open(MKDOCS_FILE, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print(f"Updated {MKDOCS_FILE}")

def main():
    if not os.path.exists(DOCS_DIR):
        print(f"Error: {DOCS_DIR} not found.")
        return

    print("Scanning docs directory...")
    # Get the tree. Note we pass rel_path='' because we want paths relative to docs/
    # But wait, standard build_tree recursive call joins rel_path.
    # For root call, we want to scan entries in DOCS_DIR
    
    # Actually, let's adjust build_tree to take just directory path and return relative paths
    tree = build_tree(DOCS_DIR)

    print("Generating navigation...")
    nav_lines = generate_yaml_nav(tree)
    
    print("Updating mkdocs.yml...")
    update_mkdocs_yml(nav_lines)

    print("Generating Full Index...")
    index_lines = generate_markdown_index(tree)
    
    header = [
        "# 📚 全站索引",
        "",
        "这里列出了 `docs/` 目录下所有的文档，按照文件夹结构自动整理。",
        ""
    ]
    
    with open(INDEX_FILE, 'w', encoding='utf-8') as f:
        f.write("\n".join(header + index_lines))
    print(f"Updated {INDEX_FILE}")

if __name__ == "__main__":
    main()
