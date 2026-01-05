import os
import re

DOCS_DIR = 'docs'
FULL_INDEX_PATH = os.path.join(DOCS_DIR, 'Full_Index.md')
MKDOCS_PATH = 'mkdocs.yml'

def get_clean_title(filepath):
    """
    Extracts the title from the first H1 header in the file.
    New Rule: Use the full title as is (after removing #), including emojis and English.
    """
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line.startswith('# '):
                    # Found title: remove leading '# ' and simple whitespace
                    clean_title = line.lstrip('#').strip()
                    return clean_title
    except Exception as e:
        print(f"Error reading {filepath}: {e}")
        return None
    return None

def main():
    # 1. Map paths to titles
    title_map = {}
    print("Scanning files...")
    for root, dirs, files in os.walk(DOCS_DIR):
        for file in files:
            if file.endswith('.md'):
                abs_path = os.path.join(root, file)
                rel_path = os.path.relpath(abs_path, DOCS_DIR).replace('\\', '/')
                
                title = get_clean_title(abs_path)
                if title:
                    title_map[rel_path] = title
                    # print(f"Mapped {rel_path} -> {title}")

    # 2. Update Full_Index.md
    if os.path.exists(FULL_INDEX_PATH):
        print(f"Updating {FULL_INDEX_PATH}...")
        with open(FULL_INDEX_PATH, 'r', encoding='utf-8') as f:
            content = f.read()

        def index_replacer(match):
            original_text = match.group(1)
            path = match.group(2)
            # Handle potential relative path differences? 
            # Current Full_Index uses paths relative to docs/ e.g. "Art/Art_Direction_Guide.md"
            # Our key is "Art/Art_Direction_Guide.md". Match should be exact.
            
            # Check if path in map
            clean = title_map.get(path)
            if clean:
                return f"- [{clean}]({path})"
            else:
                return match.group(0)

        # Regex: - [Text](Path)
        new_content = re.sub(r'-\s\[(.*?)\]\((.*?)\)', index_replacer, content)
        
        with open(FULL_INDEX_PATH, 'w', encoding='utf-8') as f:
            f.write(new_content)

    # 3. Update mkdocs.yml
    if os.path.exists(MKDOCS_PATH):
        print(f"Updating {MKDOCS_PATH}...")
        with open(MKDOCS_PATH, 'r', encoding='utf-8') as f:
            content = f.read()
            
        def yaml_replacer(match):
            indent = match.group(1)
            original_key = match.group(2)
            path = match.group(3)
            
            clean = title_map.get(path)
            if clean:
                return f"{indent}- {clean}: {path}"
            else:
                return match.group(0)
        
        # Regex: (Spaces)- Key: Path
        # Note: Path usually ends with .md
        # Using strict multiline regex now. [ \t]+ ensures we don't match newlines.
        new_content = re.sub(r'^(\s*)-\s+(.+?):[ \t]+(.+?\.md)\s*$', yaml_replacer, content, flags=re.MULTILINE)
        
        with open(MKDOCS_PATH, 'w', encoding='utf-8') as f:
            f.write(new_content)

    print("Done!")

if __name__ == '__main__':
    # Force UTF-8 for stdout to prevent UnicodeEncodeError on Windows consoles
    import sys
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    main()
