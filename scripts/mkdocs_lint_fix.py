#!/usr/bin/env python3
"""
MkDocs Markdown Linter and Fixer
================================
Automatically checks and fixes common Markdown syntax issues for MkDocs compatibility.

Usage:
    python scripts/mkdocs_lint_fix.py <file.md>           # Fix a single file
    python scripts/mkdocs_lint_fix.py --all               # Fix all .md files in docs/
    python scripts/mkdocs_lint_fix.py --all --dry-run     # Preview changes without saving
"""

import argparse
import re
import sys
from pathlib import Path
from typing import List, Tuple

# --- Configuration ---

# HLSL/Shader functions to wrap in \text{} inside math blocks
MATH_FUNCTIONS = [
    'saturate', 'lerp', 'step', 'smoothstep', 'frac', 'floor', 'ceil',
    'tex2D', 'tex2DLod', 'dot', 'cross', 'normalize', 'length', 'distance',
    'clamp', 'abs', 'pow', 'exp', 'log', 'sqrt', 'min', 'max', 'round',
    'atan2', 'if', 'discard'
]

# Problematic Unicode icons and their safe replacements
# Note: Only replace truly problematic characters that break MkDocs rendering
# Keep visually distinct icons that render correctly
ICON_REPLACEMENTS = {
    # Removed: These characters render fine in modern MkDocs
    # '\u21dd': '~',      # Elastic arrow (↝) - renders OK
    # '\u256d': '[arc]',  # Circle curve (╭) - too ugly as text
    # '\u1d55': '~',      # Back curve (ᵕ) - renders OK
}

# --- Core Fix Functions ---

def fix_math_blocks(content: str) -> Tuple[str, List[str]]:
    """
    Fix math rendering issues:
    1. Fix list item + $$ block issue (MUST be first!)
    2. Unindent $$ blocks
    3. Fix escaped subscripts (UV\\_{new} -> UV_{new})
    4. Fix malformed subscripts (A*{up} -> A_{up})
    5. Wrap functions in \\text{}
    6. Add blank lines between consecutive $$ blocks
    """
    changes = []
    
    # 1. Fix list item + $$ block issue (MUST be before unindent!)
    # Pattern: "- **label:**\n  $$...$$" -> "**label:**\n\n$$...$$"
    # This ensures $$ blocks render as block-level elements, not inline
    lines = content.split('\n')
    result_lines = []
    i = 0
    fix_count = 0
    while i < len(lines):
        line = lines[i]
        stripped = line.strip()
        # Check if this is a list item with bold label ending with :** or :**)
        if re.match(r'^-\s+\*\*[^*]+\*\*:?\)?$', stripped):
            # Check if next line is indented $$ block
            if i + 1 < len(lines) and re.match(r'^\s+\$\$', lines[i + 1]):
                # Extract label from list item (use stripped version)
                label_match = re.match(r'^-\s+(\*\*[^*]+\*\*:?\)?)\s*$', stripped)
                if label_match:
                    label = label_match.group(1)
                    # Get the $$ block (remove indentation)
                    formula_line = lines[i + 1].strip()
                    # Output: label on its own line, blank line, then formula
                    result_lines.append(label)
                    result_lines.append('')
                    result_lines.append(formula_line)
                    fix_count += 1
                    i += 2
                    continue
        result_lines.append(line)
        i += 1
    
    if fix_count > 0:
        content = '\n'.join(result_lines)
        changes.append(f"Fixed {fix_count} list-item + $$ block patterns")
    
    # 2. Unindent $$ blocks (remove leading whitespace)
    pattern = r'^(\s+)(\$\$.+?\$\$)$'
    def unindent_match(m):
        changes.append(f"Unindented math block: {m.group(2)[:50]}...")
        return m.group(2)
    content = re.sub(pattern, unindent_match, content, flags=re.MULTILINE)
    
    # 3. Fix escaped subscripts: \\_{xxx} -> _{xxx}
    # But NOT variable names like \\_Cutoff (these should stay escaped)
    pattern = r'([A-Za-z]+)\\_{([a-z]+)}'  # e.g., UV\_{new}
    def fix_subscript(m):
        changes.append(f"Fixed subscript: {m.group(0)} -> {m.group(1)}_{{{m.group(2)}}}")
        return f"{m.group(1)}_{{{m.group(2)}}}"
    content = re.sub(pattern, fix_subscript, content)
    
    # 4. Fix malformed subscripts: A*{xxx} -> A_{xxx}
    pattern = r'([A-Za-z]+)\*{([a-z]+)}'  # e.g., A*{up}
    def fix_star_subscript(m):
        changes.append(f"Fixed star subscript: {m.group(0)} -> {m.group(1)}_{{{m.group(2)}}}")
        return f"{m.group(1)}_{{{m.group(2)}}}"
    content = re.sub(pattern, fix_star_subscript, content)
    
    # 5. Wrap functions in \text{} inside $$ blocks
    def wrap_functions_in_block(match):
        block = match.group(0)
        for func in MATH_FUNCTIONS:
            # Only wrap if not already wrapped
            # Match function name followed by ( but not preceded by \text{
            pattern = rf'(?<!\\text{{)(?<![a-zA-Z])({func})(\s*\()'
            replacement = rf'\\text{{\1}}\2'
            block = re.sub(pattern, replacement, block)
        return block
    
    # Apply to $$ blocks
    content = re.sub(r'\$\$[^$]+\$\$', wrap_functions_in_block, content)
    # Apply to inline $ blocks (more careful)
    content = re.sub(r'\$[^$\n]+\$', wrap_functions_in_block, content)
    
    # 6. Add blank lines between consecutive $$ blocks
    # Pattern: $$...$$\n$$...$$  -> $$...$$\n\n$$...$$
    # Use while loop to handle multiple consecutive blocks
    pattern = r'(\$\$[^$]+\$\$)\n(\$\$)'
    total_count = 0
    while True:
        count = len(re.findall(pattern, content))
        if count == 0:
            break
        content = re.sub(pattern, r'\1\n\n\2', content)
        total_count += count
    if total_count > 0:
        changes.append(f"Added blank lines between {total_count} consecutive $$ blocks")
    
    return content, changes


def fix_tables(content: str) -> Tuple[str, List[str]]:
    """
    Fix table rendering issues:
    1. Ensure blank line before table
    2. Fix inconsistent column counts
    3. Escape pipe characters in cell content
    """
    changes = []
    lines = content.split('\n')
    result = []
    i = 0
    
    while i < len(lines):
        line = lines[i]
        
        # Detect table start (line starting with |)
        if line.strip().startswith('|') and line.strip().endswith('|'):
            # Check if previous line is not empty and not a table row
            if result and result[-1].strip() and not result[-1].strip().startswith('|'):
                changes.append(f"Added blank line before table at line {i+1}")
                result.append('')
            
            # Collect all table rows
            table_start = i
            table_rows = []
            while i < len(lines) and lines[i].strip().startswith('|'):
                table_rows.append(lines[i])
                i += 1
            
            # Analyze table structure
            if len(table_rows) >= 2:
                # Get header column count (first row)
                header = table_rows[0]
                header_cols = len([c for c in header.split('|') if c.strip() != '']) 
                
                # Fix each row to match header column count
                fixed_rows = []
                for row_idx, row in enumerate(table_rows):
                    cells = row.split('|')
                    # Remove empty first/last from split
                    if cells and cells[0].strip() == '':
                        cells = cells[1:]
                    if cells and cells[-1].strip() == '':
                        cells = cells[:-1]
                    
                    current_cols = len(cells)
                    
                    if current_cols > header_cols:
                        # Too many columns - trim
                        cells = cells[:header_cols]
                        changes.append(f"Trimmed extra columns in table row {table_start + row_idx + 1}")
                    elif current_cols < header_cols and row_idx > 1:  # Skip header and separator
                        # Too few columns - pad
                        cells.extend([''] * (header_cols - current_cols))
                        changes.append(f"Padded missing columns in table row {table_start + row_idx + 1}")
                    
                    fixed_rows.append('| ' + ' | '.join(cells) + ' |')
                
                result.extend(fixed_rows)
            else:
                result.extend(table_rows)
            
            continue
        
        result.append(line)
        i += 1
    
    return '\n'.join(result), changes


def fix_icons(content: str) -> Tuple[str, List[str]]:
    """
    Replace problematic Unicode icons with MkDocs-safe alternatives.
    """
    changes = []
    
    for icon, replacement in ICON_REPLACEMENTS.items():
        if icon in content:
            count = content.count(icon)
            content = content.replace(icon, replacement)
            changes.append(f"Replaced icon '{icon}' with '{replacement}' ({count} occurrences)")
    
    return content, changes


def fix_inline_math_spacing(content: str) -> Tuple[str, List[str]]:
    """
    Fix inline math spacing issues:
    1. REMOVE spaces inside inline math: $ expr $ -> $expr$
    2. Fix parentheses spacing: ($V$ ) -> ($V$), ( $N$) -> ($N$)
    MkDocs arithmatex requires tight $...$ format for proper rendering.
    """
    changes = []
    
    # Process line by line to avoid cross-line matches and skip table/code lines
    lines = content.split('\n')
    result_lines = []
    in_code_block = False
    
    for line in lines:
        # Track code block boundaries
        if line.strip().startswith('```'):
            in_code_block = not in_code_block
            result_lines.append(line)
            continue
        
        # Skip if inside code block or if line is a table row
        if in_code_block or line.strip().startswith('|'):
            result_lines.append(line)
            continue
        
        # Pattern 1: $ <space>...<space> $ - remove internal spaces (single line only)
        pattern = r'\$ ([^$\n]+) \$'
        def remove_spaces(m):
            inner = m.group(1).strip()
            # Skip if inner content looks like it's not math:
            # - contains pipes (table)
            # - too long
            # - no LaTeX-like content (no backslash, underscore, caret, etc.)
            if '|' in inner or len(inner) > 100:
                return m.group(0)
            # Only process if it looks like LaTeX (contains math operators/syntax)
            if not any(c in inner for c in ['\\', '_', '^', '{', '}', '+', '-', '=', '/', '*', '(', ')']):
                return m.group(0)
            changes.append(f"Removed spacing from inline math: ${inner}$")
            return f'${inner}$'
        line = re.sub(pattern, remove_spaces, line)
        
        # Pattern 2: ($..$ ) - space after math before closing paren
        pattern = r'\(\$([^$\n]+)\$\s+\)'
        def fix_trailing_paren(m):
            inner = m.group(1)
            changes.append(f"Fixed trailing space in paren: (${inner}$)")
            return f'(${inner}$)'
        line = re.sub(pattern, fix_trailing_paren, line)
        
        # Pattern 3: ( $..$) - space before math after opening paren
        pattern = r'\(\s+\$([^$\n]+)\$\)'
        def fix_leading_paren(m):
            inner = m.group(1)
            changes.append(f"Fixed leading space in paren: (${inner}$)")
            return f'(${inner}$)'
        line = re.sub(pattern, fix_leading_paren, line)
        
        result_lines.append(line)
    
    return '\n'.join(result_lines), changes


# --- Main Processing ---

def process_file(filepath: Path, dry_run: bool = False) -> List[str]:
    """
    Process a single Markdown file.
    Returns list of changes made.
    """
    try:
        content = filepath.read_text(encoding='utf-8')
    except UnicodeDecodeError:
        # Try with default encoding
        content = filepath.read_text(encoding='gbk')
    
    original = content
    all_changes = []
    
    # Apply fixes in order
    content, changes = fix_math_blocks(content)
    all_changes.extend(changes)
    
    content, changes = fix_tables(content)
    all_changes.extend(changes)
    
    content, changes = fix_icons(content)
    all_changes.extend(changes)
    
    content, changes = fix_inline_math_spacing(content)
    all_changes.extend(changes)
    
    # Save if changed
    if content != original and not dry_run:
        filepath.write_text(content, encoding='utf-8')
    
    return all_changes


def main():
    parser = argparse.ArgumentParser(
        description='MkDocs Markdown Linter and Fixer',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument('file', nargs='?', help='Markdown file to process')
    parser.add_argument('--all', action='store_true', help='Process all .md files in docs/')
    parser.add_argument('--dry-run', action='store_true', help='Preview changes without saving')
    parser.add_argument('--docs-dir', default='docs', help='Documentation directory (default: docs)')
    
    args = parser.parse_args()
    
    if not args.file and not args.all:
        parser.print_help()
        sys.exit(1)
    
    files_to_process = []
    
    if args.all:
        docs_dir = Path(args.docs_dir)
        if not docs_dir.exists():
            print(f"Error: Directory '{docs_dir}' not found.")
            sys.exit(1)
        files_to_process = list(docs_dir.rglob('*.md'))
    else:
        filepath = Path(args.file)
        if not filepath.exists():
            print(f"Error: File '{filepath}' not found.")
            sys.exit(1)
        files_to_process = [filepath]
    
    total_changes = 0
    files_changed = 0
    
    for filepath in files_to_process:
        changes = process_file(filepath, dry_run=args.dry_run)
        if changes:
            files_changed += 1
            total_changes += len(changes)
            print(f"\n{'[DRY-RUN] ' if args.dry_run else ''}[EDIT] {filepath}")
            for change in changes:
                # Handle non-ASCII characters in output
                safe_change = change.encode('ascii', errors='replace').decode('ascii')
                print(f"  [OK] {safe_change}")
    
    # Summary
    mode = "previewed" if args.dry_run else "applied"
    print(f"\n[DONE] {total_changes} changes {mode} across {files_changed}/{len(files_to_process)} files.")
    
    if args.dry_run and total_changes > 0:
        print("Run without --dry-run to apply changes.")


if __name__ == '__main__':
    main()
