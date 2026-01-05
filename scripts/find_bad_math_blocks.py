
import os
import sys

# Force utf-8 output for Windows console
sys.stdout.reconfigure(encoding='utf-8')

def check_file(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    except Exception as e:
        print(f"Error reading {filepath}: {e}")
        return

    in_block = False
    
    for i, line in enumerate(lines):
        stripped = line.strip()
        
        # Check for $$ markers
        if stripped.startswith('$$'):
            # Determine if this is a Start or End of a block
            # If it contains $$ at start and end and length > 2, it might be a one-liner block
            # e.g. $$ E=mc^2 $$
            is_one_liner = (len(stripped) > 2 and stripped.endswith('$$'))
            
            if is_one_liner:
                # Treating one-liner as a block start event
                if not in_block:
                    # Check prev
                    if i > 0:
                        prev = lines[i-1].strip()
                        if prev and not prev.endswith('$$'): # If prev is not empty AND not another math block end
                             print(f"{filepath}:{i+1}")
                             print(f"  Type: One-liner")
                             print(f"  Prev: {prev}")
                             print(f"  Curr: {stripped}\n")
                # No state change effectively, or open then close immediately
                continue

            # Multi-line block marker
            if not in_block:
                # This is a START marker
                in_block = True
                if i > 0:
                    prev = lines[i-1].strip()
                    # We flag if previous line is NOT empty
                    # AND previous line is NOT the end of another block (e.g. adjacent blocks)
                    if prev and not prev.endswith('$$'): 
                        print(f"{filepath}:{i+1}")
                        print(f"  Type: Start Block")
                        print(f"  Prev: {prev}")
                        print(f"  Curr: {stripped}\n")
            else:
                # This is an END marker
                in_block = False

def scan_docs(root_dir):
    for root, dirs, files in os.walk(root_dir):
        for file in files:
            if file.endswith(".md"):
                check_file(os.path.join(root, file))

if __name__ == "__main__":
    scan_docs("i:/MTSVN_NEW/002_Vampirefall/Server/Game_Num_Basics_And_Calc/docs")
