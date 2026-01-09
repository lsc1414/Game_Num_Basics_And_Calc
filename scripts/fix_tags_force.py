
import os

def fix_skill_text():
    path = 'docs/Dev_Guides/Technical_Implementation/Skill_Text_Localization_System.md'
    with open(path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # 修复 Line 18 (Index 17)
    # 原始: | **样式硬编码** | 使用 <color=#FF0000> 硬编码颜色，后期美术调整风格时需修改上万条文本。 | **语义化标签**：使用 <c=dmg_phys>，通过全局样式表解析。    |
    # 目标: 加上反引号
    if '<color=#FF0000>' in lines[17]:
        lines[17] = lines[17].replace('<color=#FF0000>', '`<color=#FF0000>`').replace('<c=dmg_phys>', '`<c=dmg_phys>`')
        print(f"Fixed Line 18 in {path}")
    
    # 修复 Line 19 (Index 18)
    if '<l=buff_burn>' in lines[18]:
        lines[18] = lines[18].replace('<l=buff_burn>', '`<l=buff_burn>`')
        print(f"Fixed Line 19 in {path}")

    # 修复 Line 40 (Index 39) if needed
    if '<c=dmg>' in lines[39] and '`<c=dmg>`' not in lines[39]:
        lines[39] = lines[39].replace('<c=dmg>', '`<c=dmg>`')
        print(f"Fixed Line 40 in {path}")
        
    with open(path, 'w', encoding='utf-8') as f:
        f.writelines(lines)

def fix_numerical_manual():
    path = 'docs/Design/Numerical_Manual.md'
    with open(path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    # 检查 Line 457 (Index 456)
    target_457 = 'Random.value < CurrentChance'
    if target_457 in lines[456] and '`' + target_457 not in lines[456]:
        lines[456] = lines[456].replace(target_457, f'`{target_457}`')
        print(f"Fixed Line 457 in {path}")

    # 检查 Line 666 (Index 665)
    target_666 = 'Random < BlockChance'
    if target_666 in lines[665] and '`' + target_666 not in lines[665]:
        lines[665] = lines[665].replace(target_666, f'`{target_666}`')
        print(f"Fixed Line 666 in {path}")

    # 检查 Line 697 (Index 696)
    target_697 = 'TargetHP < MaxHP * CullThreshold'
    if target_697 in lines[696] and '`' + target_697 not in lines[696]:
        lines[696] = lines[696].replace(target_697, f'`{target_697}`')
        print(f"Fixed Line 697 in {path}")

    with open(path, 'w', encoding='utf-8') as f:
        f.writelines(lines)

if __name__ == '__main__':
    try:
        fix_skill_text()
        fix_numerical_manual()
        print("Done.")
    except Exception as e:
        print(f"Error: {e}")
