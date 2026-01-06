import re
import os
import sys
import io

# Fix unicode printing on Windows
if sys.stdout.encoding != 'utf-8':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

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
    # Check for quotes
    quote_char = ''
    content_to_clean = text
    if len(text) > 1 and ((text.startswith('"') and text.endswith('"')) or (text.startswith("'") and text.endswith("'"))):
        quote_char = text[0]
        content_to_clean = text[1:-1]

    def replacement_check(match):
        full_match = match.group(0)
        content = match.group(2) # The text inside parens
        
        # Condition to remove: No Chinese AND Has Space
        if not has_chinese(content) and ' ' in content:
            return '' # Remove entirely
        
        return full_match # Keep original

    # Regex:
    # 1. (\s*) capture leading spaces
    # 2. \( start paren
    # 3. ([^)]+) capture content
    # 4. \) end paren
    # 5. (\s*) capture trailing spaces
    # We use a simple pass first to remove the target, then clean up spaces.
    
    # Robust approach: re.sub with callback
    # We target just the paren group including potentially one leading space to avoid double spacing
    # Pattern: (space?)\(content\)
    new_content = re.sub(r'(\s?)\(([^)]+)\)', replacement_check, content_to_clean)
    
    # Post-processing to fix double spaces that might have been created if we didn't catch them
    new_content = re.sub(r'\s+', ' ', new_content).strip()
    
    return f"{quote_char}{new_content}{quote_char}"

def process_mkdocs_yml(file_path):
    print(f"Processing {file_path}...")
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    new_lines = []
    # Regex to capture nav items: indent - key : value
    # Capture groups: 1=indent+dash, 2=key, 3=colon+rest
    # We use greedy matching for group 2 to handle potential colons inside quotes if simple,
    # but simplest is non-greedy until last colon? No, first colon.
    # In "nav:", items are "- Key: Value" or "- Key:"
    # We assume valid YAML where Key doesn't contain unquoted colons.
    
    nav_started = False
    
    for line in lines:
        # Simple state machine to only touch 'nav' section if needed, 
        # but the user might have other keys? No, only nav has titles usually.
        # But let's just process any line that looks like a list item with a key.
        
        # Check if it looks like a list item: "  - Something: ..."
        match = re.match(r'^(\s*-\s+)(.+?)(:\s*.*|:)$', line)
        if match:
            prefix = match.group(1)
            title = match.group(2)
            suffix = match.group(3)
            
            # Special check: excludes known non-title keys if any?
            # In mkdocs, list items with colons are usually nav entries or plugin configs.
            # We assume most "- Text (...):" patterns are navs.
            
            new_title = clean_title(title)
            if new_title != title:
                print(f"  Changed: {title} -> {new_title}")
                new_lines.append(f"{prefix}{new_title}{suffix}\n")
            else:
                new_lines.append(line)
        else:
            new_lines.append(line)

    with open(file_path, 'w', encoding='utf-8') as f:
        f.writelines(new_lines)

def process_markdown_index(file_path):
    print(f"Processing {file_path}...")
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        
    new_lines = []
    for line in lines:
        # Process Headers: ## Title
        header_match = re.match(r'^(#+\s+)(.*)$', line)
        if header_match:
            hashes = header_match.group(1)
            text = header_match.group(2)
            new_text = clean_title(text)
            if new_text != text:
                print(f"  Header Changed: {text} -> {new_text}")
                new_lines.append(f"{hashes}{new_text}\n")
                continue

        # Process Links: - [Title](Url)
        link_match = re.match(r'^(\s*-\s*\[)([^\]]+)(\].*)$', line)
        if link_match:
            prefix = link_match.group(1)
            text = link_match.group(2)
            suffix = link_match.group(3)
            new_text = clean_title(text)
            if new_text != text:
                print(f"  Link Changed: {text} -> {new_text}")
                new_lines.append(f"{prefix}{new_text}{suffix}\n")
                continue
                
        new_lines.append(line)
        
    with open(file_path, 'w', encoding='utf-8') as f:
        f.writelines(new_lines)

if __name__ == "__main__":
    base_dir = os.getcwd()
    mkdocs_path = os.path.join(base_dir, 'mkdocs.yml')
    full_index_path = os.path.join(base_dir, 'docs', 'Full_Index.md')
    
    if os.path.exists(mkdocs_path):
        process_mkdocs_yml(mkdocs_path)
    else:
        print(f"Error: {mkdocs_path} not found.")

    if os.path.exists(full_index_path):
        process_markdown_index(full_index_path)
    else:
        print(f"Error: {full_index_path} not found.")
