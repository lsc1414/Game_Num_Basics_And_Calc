
import re

def check_file(path, pattern, description):
    print(f"--- Scanning {path} for {description} ---")
    try:
        with open(path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        for i, line in enumerate(lines):
            # Check for patterns that are NOT inside backticks
            # Simple heuristic: remove backticked content first?
            # Or just check if the pattern exists.
            
            # Remove content inside `...`
            clean_line = re.sub(r'`[^`]*`', '', line)
            
            # Remove content inside ``` ... ``` (rudimentary check)
            # This is hard line-by-line, but let's assume single line checks for now.
            
            if re.search(pattern, clean_line):
                # Print the match
                match = re.search(pattern, clean_line)
                print(f"Line {i+1}: {line.strip()}")
                print(f"  Match: {match.group(0)}")
                
    except Exception as e:
        print(f"Error reading {path}: {e}")

if __name__ == '__main__':
    # 1. Numerical Manual: Look for < followed by something with = (JSX attribute error)
    # The error was "Unexpected character = before name".
    # This might be <Tag= or <Tag attr=.
    # Regex: <[^>]*=
    check_file('docs/Design/Numerical_Manual.md', r'<[^>]*=', "Potential improper tags with =")
    
    # 2. Skill Text: Look for { or <c= or <l=
    check_file('docs/Dev_Guides/Technical_Implementation/Skill_Text_Localization_System.md', r'(<[a-zA-Z]+=[^>]+>|\{[0-9]+\})', "Unescaped tags or braces")
