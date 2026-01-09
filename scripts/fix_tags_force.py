
import os

def fix_skill_text():
    path = 'docs/Dev_Guides/Technical_Implementation/Skill_Text_Localization_System.md'
    if not os.path.exists(path):
        print(f"File not found: {path}")
        return

    with open(path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    modified = False

    # 修复 Line 37 (Index 36)
    # | `Skill_Fireball_Desc` | ... | Hurls a bolt dealing <c=dmg>{0}</c> damage and applying <l=buff_burn>Burn</l>. | ...
    idx = 36
    if idx < len(lines):
        line = lines[idx]
        if '<c=dmg>' in line and '`<c=dmg>' not in line:
            print(f"Fixing Line 37 (English tags)...")
            line = line.replace('<c=dmg>{0}</c>', '`<c=dmg>{0}</c>`')
            line = line.replace('<l=buff_burn>Burn</l>', '`<l=buff_burn>Burn</l>`')
            # Chinese part
            line = line.replace('<c=dmg>{0}</c>', '`<c=dmg>{0}</c>`') # Replace again for 2nd occurrence
            line = line.replace('<l=buff_burn>燃烧</l>', '`<l=buff_burn>燃烧</l>`')
            lines[idx] = line
            modified = True

    if modified:
        with open(path, 'w', encoding='utf-8') as f:
            f.writelines(lines)
        print(f"Updated {path}")
    else:
        print(f"No changes for {path} (Line 37 might be clean or index wrong)")

def fix_numerical_manual():
    path = 'docs/Design/Numerical_Manual.md'
    if not os.path.exists(path):
        print(f"File not found: {path}")
        return

    with open(path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    modified = False

    # Helper to safe replace
    def safe_replace(line_idx, old, new):
        nonlocal modified
        if line_idx < len(lines):
            if old in lines[line_idx] and new not in lines[line_idx]:
                 lines[line_idx] = lines[line_idx].replace(old, new)
                 print(f"Fixed Line {line_idx+1}: {old} -> {new}")
                 modified = True
            elif new in lines[line_idx]:
                 print(f"Line {line_idx+1} already fixed.")
            else:
                 print(f"Line {line_idx+1} match failed. Content: {lines[line_idx].strip()[:50]}...")

    # Line 206: Speed <= 0
    safe_replace(205, 'Speed <= 0', '`Speed <= 0`')

    # Line 457: Random.value < CurrentChance
    safe_replace(456, 'Random.value < CurrentChance', '`Random.value < CurrentChance`')

    # Line 666: Random < BlockChance
    safe_replace(665, 'Random < BlockChance', '`Random < BlockChance`')
    
    # Line 697: TargetHP < MaxHP
    safe_replace(696, 'TargetHP < MaxHP', '`TargetHP < MaxHP`')

    if modified:
        with open(path, 'w', encoding='utf-8') as f:
            f.writelines(lines)
        print(f"Updated {path}")
    else:
        print(f"No changes for {path}")

if __name__ == '__main__':
    try:
        fix_skill_text()
        fix_numerical_manual()
        print("Done.")
    except Exception as e:
        print(f"Error: {e}")
