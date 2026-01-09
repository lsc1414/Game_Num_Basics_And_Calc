#!/usr/bin/env python3
"""
Mintlify Helper Script
======================
Automates tasks for Mintlify documentation:
1.  Updates `docs.json` navigation.
2.  Lints and formats Markdown files for Mintlify/MDX compatibility:
    -   Converts `!!! type` admonitions to `> [!TYPE]`.
    -   Fixes math syntax.
    -   Ensures frontmatter exists.
"""

import argparse
import json
import re
import sys
import io
from pathlib import Path
from typing import List, Dict, Any, Tuple, Optional

# 修复 Windows 控制台编码问题,支持 emoji 输出
if sys.platform == 'win32':
    try:
        # 设置控制台编码为 UTF-8
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
        sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')
    except Exception:
        pass  # 如果设置失败,继续使用默认编码

# --- Configuration ---
DOCS_JSON_PATH = Path('docs.json')
MATH_FUNCTIONS = [
    'saturate', 'lerp', 'step', 'smoothstep', 'frac', 'floor', 'ceil',
    'tex2D', 'tex2DLod', 'dot', 'cross', 'normalize', 'length', 'distance',
    'clamp', 'abs', 'pow', 'exp', 'log', 'sqrt', 'min', 'max', 'round',
    'atan2', 'if', 'discard'
]

def load_docs_json() -> Dict[str, Any]:
    if not DOCS_JSON_PATH.exists():
        print(f"Error: {DOCS_JSON_PATH} not found.")
        sys.exit(1)
    try:
        with open(DOCS_JSON_PATH, 'r', encoding='utf-8-sig') as f:
            return json.load(f)
    except json.JSONDecodeError as e:
        print(f"Error decoding {DOCS_JSON_PATH}: {e}")
        sys.exit(1)

def save_docs_json(data: Dict[str, Any]):
    with open(DOCS_JSON_PATH, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"Updated {DOCS_JSON_PATH}")

def find_group_in_nav(nav: List[Any], group_name: str) -> Optional[Dict[str, Any]]:
    """Recursively finds a group (by 'group' key) in the navigation structure."""
    for item in nav:
        if isinstance(item, dict):
            if item.get('group') == group_name:
                return item
            
            # recursive search in 'groups' or other nested lists if structure allows
            # Mintlify docs.json usually has tabs -> groups -> pages
            if 'groups' in item:
                found = find_group_in_nav(item['groups'], group_name)
                if found: return found
            # Sometimes tabs have 'pages' directly
    return None

def find_tab_in_nav(nav: List[Any], tab_name: str) -> Optional[Dict[str, Any]]:
    for item in nav:
        if isinstance(item, dict) and item.get('tab') == tab_name:
            return item
    return None

def add_to_docs_json(file_path: str, tab_name:str, group_name: str):
    """
    Adds a file path to docs.json.
    Structure: navigation -> [tabs] -> (tab matches) -> groups -> (group matches) -> pages
    """
    data = load_docs_json()
    nav = data.get('navigation', {}).get('tabs', [])
    
    # Clean path: remove extension, make relative to root (if it starts with docs/)
    # Mintlify expects paths without .md extension, usually relative to root or within docs/ 
    # based on existing pattern in docs.json.
    # The current docs.json shows paths like "docs/Design/..."
    
    p = Path(file_path)
    # Ensure forward slashes
    rel_path = p.as_posix()
    if rel_path.endswith('.md'):
        rel_path = rel_path[:-3]
    
    # 1. Find Tab
    tab_node = find_tab_in_nav(nav, tab_name)
    if not tab_node:
        print(f"Tab '{tab_name}' not found. Creating it.")
        tab_node = {"tab": tab_name, "groups": []}
        nav.append(tab_node)
    
    # 2. Find Group within Tab
    # Note: A tab can have 'pages' directly or 'groups'. 
    # If user provides a group_name, we look for it in 'groups'.
    
    if group_name:
        if 'groups' not in tab_node:
            tab_node['groups'] = []
        
        group_node = None
        for g in tab_node['groups']:
            if g.get('group') == group_name:
                group_node = g
                break
        
        if not group_node:
            print(f"Group '{group_name}' not found in tab '{tab_name}'. Creating it.")
            group_node = {"group": group_name, "pages": []}
            tab_node['groups'].append(group_node)
        
        # Check if page already exists
        if rel_path not in group_node['pages']:
            group_node['pages'].append(rel_path)
            print(f"Added '{rel_path}' to group '{group_name}' in tab '{tab_name}'.")
        else:
            print(f"'{rel_path}' already exists in docs.json.")
            
    else:
        # No group, add directly to tab's 'pages'
        if 'pages' not in tab_node:
            tab_node['pages'] = []
            
        if rel_path not in tab_node['pages']:
            tab_node['pages'].append(rel_path)
            print(f"Added '{rel_path}' directly to tab '{tab_name}'.")
        else:
            print(f"'{rel_path}' already exists in docs.json.")

    data['navigation']['tabs'] = nav # Ensure assignment back if nav was new list (though list is ref)
    save_docs_json(data)

def fix_math_syntax(text: str) -> str:
    """Fixes common math syntax issues for MathJax/KaTeX compatibility."""
    # Similar logic to mkdocs_lint_fix.py but simplified or adapted if needed
    text = re.sub(r'([A-Za-z0-9])\\_\{([a-zA-Z0-9]+)\}', r'\1_{\2}', text)
    text = re.sub(r'([A-Za-z0-9])\*\{([a-zA-Z0-9]+)\}', r'\1_{\2}', text)
    for func in MATH_FUNCTIONS:
            pattern = rf'(?<!\\text\{{)(?<!\\)(?<![a-zA-Z])({func})(\s*\()'
            text = re.sub(pattern, rf'\\text{{\1}}\2', text)
    return text

def convert_admonitions(text: str) -> str:
    """Converts MkDocs !!! type to GitHub > [!TYPE]"""
    # Mintlify supports standard GitHub alerts really well.
    # Pattern: !!! type "Title" -> > [!TYPE] Title
    # or       !!! type -> > [!TYPE]
    
    lines = text.split('\n')
    new_lines = []
    
    # State tracking
    in_admonition = False
    admonition_indent = 0
    
    # Map mkdocs types to github types
    type_map = {
        'note': 'NOTE',
        'info': 'NOTE',
        'tip': 'TIP',
        'warning': 'WARNING',
        'danger': 'CAUTION',
        'failure': 'CAUTION',
        'bug': 'CAUTION',
        'quote': 'NOTE',
        'example': 'TIP',
        'question': 'NOTE',
        'todo': 'NOTE'
    }

    i = 0
    while i < len(lines):
        line = lines[i]
        stripped = line.strip()
        indent = len(line) - len(line.lstrip())
        
        match = re.match(r'^!!!\s+(\w+)(?:\s+"(.*?)")?', stripped)
        if match:
            mk_type = match.group(1).lower()
            title = match.group(2)
            gh_type = type_map.get(mk_type, 'NOTE')
            
            # Construct GitHub Alert Header
            new_lines.append(f"> [!{gh_type}]")
            if title:
                new_lines.append(f"> **{title}**") # Mintlify renders bold text well in alerts
            
            # We are now in an admonition block. 
            # The *content* lines next are usually indented by 4 spaces in MkDocs.
            # We need to output them prefixed by '>' and dedented (relative to the !!!)
            # But wait, Markdown allows lazy blockquotes? Better to be explicit: > content
            
            # Simple state machine isn't enough because indentation varies.
            # We need to process subsequent lines that are indented relative to this one.
            # Look ahead
            j = i + 1
            while j < len(lines):
                next_line = lines[j]
                if not next_line.strip():
                    new_lines.append(">") # Empty line in blockquote
                    j += 1
                    continue
                
                next_indent = len(next_line) - len(next_line.lstrip())
                if next_indent < indent + 4: # Break if indentation drops back
                    break
                
                # It's content. Remove 4 spaces of indentation and prefix with >
                content = next_line[indent+4:] # naive dedent
                new_lines.append(f"> {content}")
                j += 1
            
            i = j # skip processed lines
            continue
            
        new_lines.append(line)
        i += 1
        
    return '\n'.join(new_lines)

def lint_file(file_path: Path, fix: bool = False):
    if not file_path.exists():
        print(f"File {file_path} not found.")
        return

    try:
        content = file_path.read_text(encoding='utf-8-sig')
    except UnicodeDecodeError:
        content = file_path.read_text(encoding='utf-16')
    original_content = content
    
    # 1. Frontmatter Check
    if not content.startswith('---'):
        print(f"Warning: {file_path} missing frontmatter.")
        # We could auto-add it, but title is context-dependent.
    
    # 2. Fix Math
    content = fix_math_syntax(content)
    
    # 3. Convert Admonitions
    content = convert_admonitions(content)
    
    # 4. Fix Common Mintlify/MDX Issues
    
    # 4.1 Unclosed <br> tags -> <br />
    content = re.sub(r'<br>(?![\s\S]*?>)', r'<br />', content)
    # Also handle table specific <br> which are common source of errors
    content = content.replace('| <br> |', '| <br /> |')
    content = re.sub(r'(?<=\|)(.*?)<br>(?=.*?\|)', r'\1<br />', content)

    # 4.2 Unescaped < followed by numbers (e.g., <10, < 20%)
    # This regex looks for < followed by a digit, and NOT followed by a valid HTML tag start
    content = re.sub(r'<(\d)', r'\\<\1', content)
    
    # 4.3 Unescaped < followed by common non-tag text in typical contexts (like "A < B")
    # This is trickier, usage of space helps identify comparisons
    content = re.sub(r' (\s*)<(\s*) ', r' \1\\<\2 ', content)

    # 4.4 Remove Liquid tags (Jekyll legacy)
    content = re.sub(r'\{%\s*raw\s*%\}', '', content)
    content = re.sub(r'\{%\s*endraw\s*%\}', '', content)

    # 4.5 Convert HTML comments to MDX comments
    # standard <!-- comment --> to {/* comment */}
    # Note: simple replacement, might need robustness for multi-line
    content = re.sub(r'<!--(.*?)-->', r'{/*\1*/}', content, flags=re.DOTALL)

    if content != original_content:
        if fix:
            file_path.write_text(content, encoding='utf-8')
            print(f"Fixed formatting in {file_path}")
        else:
            print(f"Issues found in {file_path}. Run with --fix.")
    else:
        print(f"{file_path} passed checks.")

def list_categories():
    data = load_docs_json()
    tabs = data.get('navigation', {}).get('tabs', [])
    print("Available Categories (Tabs -> Groups):")
    for tab in tabs:
        t_name = tab.get('tab', 'Unknown')
        print(f"\n[{t_name}]")
        groups = tab.get('groups', [])
        for g in groups:
             print(f"  - {g.get('group')}")
        pages = tab.get('pages', [])
        if pages:
            print(f"  - (Direct Pages: {len(pages)})")

def main():
    parser = argparse.ArgumentParser(description="Mintlify Helper Script")
    subparsers = parser.add_subparsers(dest='command')
    
    # Add to Nav
    add_parser = subparsers.add_parser('add', help='Add file to docs.json navigation')
    add_parser.add_argument('file', help='Path to markdown file (relative to root)')
    add_parser.add_argument('--tab', required=True, help='Tab name (e.g., "🎮 设计")')
    add_parser.add_argument('--group', help='Group name (e.g., "核心系统")')
    
    # Lint/Fix
    lint_parser = subparsers.add_parser('lint', help='Lint and fix markdown file')
    lint_parser.add_argument('file', help='Path to markdown file')
    lint_parser.add_argument('--fix', action='store_true', help='Apply fixes')

    # List Categories
    subparsers.add_parser('list-cats', help='List available tabs and groups')

    args = parser.parse_args()
    
    if args.command == 'add':
        add_to_docs_json(args.file, args.tab, args.group)
    elif args.command == 'lint':
        lint_file(Path(args.file), args.fix)
    elif args.command == 'list-cats':
        list_categories()
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
