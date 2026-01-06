#!/usr/bin/env python3
"""
MkDocs Markdown Linter and Fixer (Strict & Sane Edition)
=======================================================
Enforces best practices for MkDocs (Material) rendering:
1. Lists: 4-space indentation, no blank lines between parent and first child.
2. Math: Blank lines around block math ($$), syntax fixing.
3. Tables: Blank lines before.
4. Inline Math: Space trimming.
"""

import argparse
import re
from pathlib import Path
from typing import List, Tuple, Optional
import dataclasses

# --- Configuration ---
MATH_FUNCTIONS = [
    'saturate', 'lerp', 'step', 'smoothstep', 'frac', 'floor', 'ceil',
    'tex2D', 'tex2DLod', 'dot', 'cross', 'normalize', 'length', 'distance',
    'clamp', 'abs', 'pow', 'exp', 'log', 'sqrt', 'min', 'max', 'round',
    'atan2', 'if', 'discard'
]

@dataclasses.dataclass
class LineContext:
    content: str
    indent: int
    is_blank: bool
    list_marker: Optional[str] = None # '-', '*', '1.'
    is_math_block_start: bool = False
    is_math_block_end: bool = False
    is_code_boundary: bool = False

class MarkdownLinter:
    def __init__(self, content: str):
        self.lines = content.split('\n')
        self.changes = []
        self.output_lines = []
    
    def get_line_context(self, line: str) -> LineContext:
        stripped_left = line.lstrip()
        stripped = line.strip()
        indent = len(line) - len(stripped_left)
        is_blank = not stripped
        
        list_match = re.match(r'^([-*+]|\d+\.)\s+', stripped_left)
        list_marker = list_match.group(1) if list_match else None
        
        is_math_start = stripped.startswith('$$')
        is_math_end = stripped.endswith('$$') and len(stripped) > 2
        if stripped == '$$':
            is_math_start = True
            is_math_end = True
            
        is_code = stripped.startswith('```') or stripped.startswith('~~~')
        
        return LineContext(
            content=line,
            indent=indent,
            is_blank=is_blank,
            list_marker=list_marker,
            is_math_block_start=is_math_start,
            is_math_block_end=is_math_end,
            is_code_boundary=is_code
        )

    def fix_math_syntax(self, text: str) -> str:
        text = re.sub(r'([A-Za-z0-9])\\_\{([a-zA-Z0-9]+)\}', r'\1_{\2}', text)
        text = re.sub(r'([A-Za-z0-9])\*\{([a-zA-Z0-9]+)\}', r'\1_{\2}', text)
        for func in MATH_FUNCTIONS:
             pattern = rf'(?<!\\text\{{)(?<!\\)(?<![a-zA-Z])({func})(\s*\()'
             text = re.sub(pattern, rf'\\text{{\1}}\2', text)
        return text

    def run(self) -> Tuple[str, List[str]]:
        i = 0
        n = len(self.lines)
        in_code_block = False
        in_math_block = False
        
        # Track original indentation to mapped target indentation (4-space steps)
        # item: (orig_indent, target_indent)
        indent_map = [] 

        while i < n:
            ctx = self.get_line_context(self.lines[i])
            
            # --- Code Block Bypass ---
            if ctx.is_code_boundary:
                in_code_block = not in_code_block
                self.output_lines.append(ctx.content)
                i += 1
                continue
            if in_code_block:
                self.output_lines.append(ctx.content)
                i += 1
                continue

            # --- Math Block Logic ---
            if ctx.is_math_block_start and not in_math_block:
                stripped = ctx.content.strip()
                if '$$' in stripped and not stripped.startswith('$$'):
                    label, _, body = ctx.content.partition('$$')
                    self.output_lines.append(label.rstrip())
                    # NO blank line here if it's a "Label: $$" pattern, usually
                    # But for Arithmatex standard, YES blank line.
                    self.output_lines.append('')
                    cur_indent = len(label) - len(label.lstrip())
                    self.lines[i] = ' ' * cur_indent + '$$' + body
                    self.changes.append(f"Line {i+1}: Split hybrid math line")
                    continue

                if self.output_lines and self.output_lines[-1].strip():
                    self.output_lines.append('')
                    self.changes.append(f"Line {i+1}: Added blank line before math block")
                
                in_math_block = True
                fixed = self.fix_math_syntax(ctx.content)
                if fixed != ctx.content: self.changes.append(f"Line {i+1}: Fixed math syntax")
                self.output_lines.append(fixed)
                
                if ctx.is_math_block_end and stripped != '$$':
                    in_math_block = False
                    if i + 1 < n and self.lines[i+1].strip():
                         self.output_lines.append('')
                         self.changes.append(f"Line {i+1}: Added blank line after math block")
                i += 1
                continue

            if in_math_block:
                fixed = self.fix_math_syntax(ctx.content)
                if fixed != ctx.content: self.changes.append(f"Line {i+1}: Fixed math syntax")
                self.output_lines.append(fixed)
                if ctx.is_math_block_end or ctx.content.strip() == '$$':
                    in_math_block = False
                    if i + 1 < n and self.lines[i+1].strip():
                         self.output_lines.append('')
                         self.changes.append(f"Line {i+1}: Added blank line after math block")
                i += 1
                continue

            # --- List Logic ---
            if ctx.list_marker:
                # 1. Update Indent Map
                if not indent_map or ctx.indent > indent_map[-1][0]:
                    target = 4 * len(indent_map)
                    indent_map.append((ctx.indent, target))
                elif ctx.indent < indent_map[-1][0]:
                    while indent_map and ctx.indent <= indent_map[-1][0] - 2:
                        indent_map.pop()
                
                target_indent = indent_map[-1][1] if indent_map else 0
                
                # 2. Fix Indentation
                if ctx.indent != target_indent:
                    ctx.content = ' ' * target_indent + ctx.content.lstrip()
                    self.changes.append(f"Line {i+1}: Normalized list indentation to {target_indent}")
                
                # 3. Handle Blank Line before/after
                if self.output_lines:
                    prev = self.output_lines[-1]
                    # If this is a sub-item (target_indent > 0), REMOVE blank line before it if previous was its parent
                    if target_indent > 0 and not prev.strip():
                         # Check if prev-1 was a list item or heading
                         if len(self.output_lines) > 1:
                              prev_prev = self.output_lines[-2]
                              if prev_prev.lstrip().startswith(('-', '*', '+', '1.')) or prev_prev.strip().startswith('#'):
                                   self.output_lines.pop()
                                   self.changes.append(f"Line {i+1}: Removed blank line between parent and child list item")
                    
                    # If this is a top-level list item (target_indent == 0) and previous was text, ensure blank line
                    elif target_indent == 0:
                         if prev.strip() and not (prev.lstrip().startswith(('-', '*', '+', '1.')) or prev.strip().startswith('#')):
                              self.output_lines.append('')
                              self.changes.append(f"Line {i+1}: Added blank line before list")
            
            elif not ctx.is_blank:
                 # Check if this text should be indented to match a parent list item
                 if indent_map:
                      # If it's a paragraph within a list item, it must match or be deeper
                      if ctx.indent >= indent_map[-1][0]:
                           target_indent = indent_map[-1][1] + 4 # Content indent
                           if ctx.indent != target_indent:
                                # Only adjust if it's close or obviously inside
                                # But let's be safe and only do this if it's already significantly indented
                                if ctx.indent >= 2:
                                     ctx.content = ' ' * target_indent + ctx.content.lstrip()
                                     self.changes.append(f"Line {i+1}: Normalized content indentation to {target_indent}")
                      elif ctx.indent <= 2:
                           # Fled the list
                           indent_map = []
            
            # --- Table logic ---
            if ctx.content.strip().startswith('|'):
                if self.output_lines and self.output_lines[-1].strip() and not self.output_lines[-1].strip().startswith('|'):
                    self.output_lines.append('')
                    self.changes.append(f"Line {i+1}: Added blank line before table")

            # --- Inline Math ---
            if '$' in ctx.content:
                fixed_line = ctx.content
                def repl_space(m):
                    inner = m.group(1).strip()
                    if len(inner) > 2 and inner.isalpha(): return m.group(0)
                    self.changes.append(f"Line {i+1}: Trimmed inline math")
                    return f"${inner}$"
                fixed_line = re.sub(r'(?<!\\)\$\s+([^$]+?)\s+\$', repl_space, fixed_line)
                parts = re.split(r'(\$[^$]+\$)', fixed_line)
                for idx, part in enumerate(parts):
                    if part.startswith('$') and part.endswith('$'):
                        parts[idx] = f"${self.fix_math_syntax(part[1:-1])}$"
                ctx.content = ''.join(parts)

            self.output_lines.append(ctx.content)
            i += 1
            
        return '\n'.join(self.output_lines), self.changes

def process_file(filepath: Path, dry_run: bool = False):
    content = filepath.read_text(encoding='utf-8')
    linter = MarkdownLinter(content)
    new_content, changes = linter.run()
    if changes:
        print(f"\nProcessing {filepath}:")
        for c in changes:
            print(f"  [FIX] {c}")
        if not dry_run:
            filepath.write_text(new_content, encoding='utf-8')
            print("  -> Fixed.")
    else:
        print(f"No issues in {filepath}")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('file', nargs='?')
    parser.add_argument('--all', action='store_true')
    parser.add_argument('--dry-run', action='store_true')
    args = parser.parse_args()
    if args.all:
        for f in Path('docs').rglob('*.md'):
            process_file(f, args.dry_run)
    elif args.file:
        process_file(Path(args.file), args.dry_run)
    else:
        parser.print_help()

if __name__ == '__main__':
    main()
