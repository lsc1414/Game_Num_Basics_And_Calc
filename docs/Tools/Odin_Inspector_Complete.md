---
sidebarTitle: "Odin å·¥å·ç»¼åæå"
---

# Odin å·¥å·ç»¼åæå

> æ¬ææ¡£ç±ä»¥ä¸æä»¶åå¹¶çæ (2026-01-09)



---


{/* æ¥æº: Dev_Guides\Tools\Odin_Inspector_Advanced_Techniques.md */}

## ð§ââï¸?Odin Inspector é«çº§ä½¿ç¨æå·§æ·±åº¦ç ç©?

> ð¯ **ç®æ è¯»è?*: å·²ææ?Odin åºç¡ç¨æ³ç?Unity å¼åè? 
> ð **å®ä½**: æä¾å®æ¹ Demo æªæ¶µççå®ææå·§ãå¤æåºæ¯è§£å³æ¹æ¡åæ§è½ä¼åç­ç¥

---

## ð 1. çè®ºåºç¡ (Theoretical Basis)

### 1.1 æ ¸å¿å®ä¹

**Odin Inspector** æ¯ä¸ä¸ªå¢å¼?Unity Inspector çæä»¶ï¼éè¿ C# ç¹æ§ï¼Attributesï¼é©±å¨çå£°æå¼ç¼ç¨èå¼ï¼å®ç°äºï¼

- **å£°æå¼?UI æå»º**: éè¿ç¹æ§æ ç­¾ç´æ¥æè¿?Inspector å¸å±ï¼èéå½ä»¤å¼ä»£ç ã?
- **æ°æ®éªè¯å±?*: å¨åºååå±é¢æä¾ç±»åå®å¨åçº¦ææ£æ¥ã?
- **Editor èªå¨å?*: åå°æå¨ç¼å `CustomEditor` çéæ±ã?

### 1.2 è®¾è®¡æ¨¡å¼

Odin çæ¶æåºäºä»¥ä¸è®¾è®¡æ¨¡å¼ï¼

```mermaid
graph TD
    A[Property System] */} B[Attribute Processor]
    B */} C[Drawer System]
    C */} D[Value Resolver]
    D */} E[Inspector Rendering]
    
    style A fill:#ff9999
    style C fill:#99ccff
    style E fill:#99ff99
```


- **Property System**: Odin çå±æ§ç³»ç»ï¼OdinPropertyTreeï¼ç¬ç«äº Unity ç?SerializedPropertyã?
- **Resolver Pattern**: `@` è¯­æ³çå¨æå¼è§£æå¨ï¼æ¯ææåå¼ç¨ãè¡¨è¾¾å¼æ±å¼ã?
- **Decorator Chain**: å¤ä¸ªç¹æ§æä¼åçº§é¾å¼å¤çã?

### 1.3 æ§è½æ¨¡å

Inspector ç»å¶æ§è½ç¶é¢ï¼?

- **GC åé**: æ¯å¸§ç?`GetValue()` è°ç¨å¯è½è§¦åè£ç®±ã?
- **åå°å¼é**: å¨æè§£æè¡¨è¾¾å¼çææ¬ã?
- **éç»é¢ç**: `OnInspectorGUI` çè°ç¨æ¬¡æ°ä¸éä¸­å¯¹è±¡æ°ææ­£æ¯ã?

---

## ð ï¸?2. å®è·µåºç¨ (Practical Implementation)

### 2.1 é«çº§æå·§ä¸ï¼èªå®ä¹éªè¯å¨ç»å?

#### é®é¢åºæ¯
å?**Vampirefall** ä¸­ï¼æä»¬éè¦ç¡®ä¿å¡é²å»ºç­çéç½®æ°æ®åæ¶æ»¡è¶³ï¼?

1. ææ¬å¿é¡»ä¸?10 çåæ°
2. æ»å»èå´ä¸è½è¶è¿å»ºç­ç­çº§ç?1.5 å?

3. ç¹æ®å¡ç§ç±»çæ»å»åå¿é¡»æ»¡è¶³ç¹å®å¬å¼?

#### è§£å³æ¹æ¡ï¼èªå®ä¹ Validator

```csharp
using Sirenix.OdinInspector;

public class TowerConfig : ScriptableObject
{
    [Title("åºç¡å±æ?)]
    [ValidateInput("@Cost % 10 == 0", "ææ¬å¿é¡»æ?0çåæ°")]
    [SuffixLabel("éå¸", true)]
    public int Cost;

    [Range(1, 10)]
    public int Level;

    [ValidateInput("ValidateAttackRange", "æ»å»èå´ä¸åç?)]
    [SuffixLabel("ç±?, true)]
    public float AttackRange;

    [ShowIf("@TowerType == TowerType.Special")]
    [ValidateInput("ValidateSpecialDamage", "ç¹æ®å¡ä¼¤å®³å¿é¡?>= åºç¡å?* 1.2")]
    public float Damage;

    [EnumToggleButtons]
    public TowerType TowerType;

    // â?æå·§ï¼ä½¿ç¨ç§ææ¹æ³ä½ä¸ºéªè¯å½æ°ï¼é¿åæ±¡æå¬å±API
    private bool ValidateAttackRange(float range)
    {
        return range <= Level * 1.5f;
    }

    private bool ValidateSpecialDamage(float damage, ref string errorMessage)
    {
        if (TowerType != TowerType.Special) return true;
        
        float minDamage = GetBaseDamage() * 1.2f;
        if (damage < minDamage)
        {
            errorMessage = $"ç¹æ®å¡ä¼¤å®³è³å°éè¦?{minDamage:F1} (å½å: {damage:F1})";
            return false;
        }
        return true;
    }

    private float GetBaseDamage() => Level * 10f;
}
```

**ð å³é®ç?*ï¼?

- `ValidateInput` çç¬¬äºä¸ªåæ°æ¯æå¨æè¡¨è¾¾å¼ï¼`"@SomeMethod($value)"`
- éªè¯å½æ°å¯ä»¥è¿å `bool` æä½¿ç?`ref string` æä¾è¯¦ç»éè¯¯ä¿¡æ¯
- å¤ä¸ªéªè¯ç¹æ§ä¼æé¡ºåºæ§è¡?

---

### 2.2 é«çº§æå·§äºï¼å¨æä¸æåè¡?+ å¾æ é¢è§

#### é®é¢åºæ¯
å¨éæ©æäººç±»åæ¶ï¼æä»¬å¸æï¼?

- ä¸æåè¡¨å¨æè¯»åæææäººéç½?
- æ¾ç¤ºæäººå¾æ é¢è§
- æ¯ææç´¢è¿æ»¤

#### è§£å³æ¹æ¡ï¼ValueDropdown + PreviewField ç»å

```csharp
using Sirenix.OdinInspector;
using System.Collections.Generic;
using System.Linq;
using UnityEngine;

public class WaveConfig : ScriptableObject
{
    [Title("æäººéç½®")]
    [ValueDropdown("GetEnemyList")]
    [PreviewField(55, ObjectFieldAlignment.Left)]
    [HideLabel]
    public EnemyConfig SelectedEnemy;

    [ListDrawerSettings(ShowIndexLabels = true, ListElementLabelName = "WaveName")]
    public List<WaveData> Waves;

    // â?æå·§ï¼è¿å IEnumerable<ValueDropdownItem<T>> å¯ä»¥èªå®ä¹æ¾ç¤ºææ?
    private IEnumerable<ValueDropdownItem<EnemyConfig>> GetEnemyList()
    {
        var allEnemies = Resources.LoadAll<EnemyConfig>("Enemies");
        
        return allEnemies
            .OrderBy(e => e.EnemyType)
            .ThenBy(e => e.Level)
            .Select(e => new ValueDropdownItem<EnemyConfig>(
                $"{GetEnemyIcon(e.EnemyType)} {e.name} (Lv.{e.Level})",
                e
            ));
    }

    private string GetEnemyIcon(EnemyType type)
    {
        return type switch
        {
            EnemyType.Grunt => "ð¹",
            EnemyType.Elite => "ð",
            EnemyType.Boss => "ð",
            _ => "â?
        };
    }
}

[System.Serializable]
public class WaveData
{
    [HideInInspector]
    public string WaveName => $"Wave {WaveNumber}: {EnemyCount}x {Enemy?.name ?? "None"}";

    public int WaveNumber;
    
    [ValueDropdown("@FindObjectOfType<WaveConfig>()?.GetEnemyList()")]
    [PreviewField(40)]
    public EnemyConfig Enemy;
    
    [MinValue(1)]
    public int EnemyCount;
}
```

**ð å³é®ç?*ï¼?

- `@` è¯­æ³å¯ä»¥è°ç¨å¤é¨æ¹æ³ï¼`@FindObjectOfType<T>()`
- `ListElementLabelName` ä½¿ç¨å±æ?å­æ®µèªå®ä¹åè¡¨é¡¹æ¾ç¤ºåç§°
- `PreviewField` çç¬¬ä¸ä¸ªåæ°æ§å¶é¢è§å¤§å°?

---

### 2.3 é«çº§æå·§ä¸ï¼æ¡ä»¶æ¾ç¤ºçå¤æé»è¾

#### é®é¢åºæ¯
ç©åéç½®ä¸­ï¼ä¸ååè´¨çè£å¤æä¸åçå±æ§ç»åï¼

- æ®éè£å¤ï¼åªæåºç¡å±æ?
- ç¨æè£å¤ï¼åºç¡å±æ?+ 1 ä¸ªç¹æ®ææ?
- ä¼ è¯´è£å¤ï¼åºç¡å±æ?+ 2 ä¸ªç¹æ®ææ?+ å¥è£ææ

#### è§£å³æ¹æ¡ï¼ShowIf çé«çº§ç¨æ³?

```csharp
using Sirenix.OdinInspector;
using UnityEngine;

public enum ItemRarity { Common, Rare, Legendary }

public class ItemConfig : ScriptableObject
{
    [Title("åºç¡ä¿¡æ¯")]
    [PreviewField(80, ObjectFieldAlignment.Left)]
    public Sprite Icon;

    [EnumToggleButtons]
    [OnValueChanged("OnRarityChanged")]
    public ItemRarity Rarity;

    [Title("å±æ?)]
    public int BaseAttack;
    public int BaseDefense;

    // â?æå·?ï¼ç»åå¤ä¸ªæ¡ä»?
    [ShowIf("@Rarity == ItemRarity.Rare || Rarity == ItemRarity.Legendary")]
    [BoxGroup("ç¹æ®ææ")]
    [ValueDropdown("GetAvailableEffects")]
    public string SpecialEffect1;

    // â?æå·?ï¼ä½¿ç¨æ¹æ³åä½ä¸ºæ¡ä»¶
    [ShowIf("IsLegendary")]
    [BoxGroup("ç¹æ®ææ")]
    [ValueDropdown("GetAvailableEffects")]
    public string SpecialEffect2;

    [ShowIf("IsLegendary")]
    [BoxGroup("å¥è£ææ")]
    [AssetsOnly]
    public SetBonusConfig SetBonus;

    // â?æå·?ï¼å¨æå¯ç?ç¦ç¨
    [EnableIf("@BaseAttack > 0")]
    [ProgressBar(0, 100, ColorGetter = "GetAttackColor")]
    public int AttackBonus;

    // æ¡ä»¶æ¹æ³
    private bool IsLegendary() => Rarity == ItemRarity.Legendary;

    // å¨æé¢è?
    private Color GetAttackColor()
    {
        if (AttackBonus < 30) return Color.gray;
        if (AttackBonus < 60) return Color.yellow;
        return Color.red;
    }

    // æ¸çæ°æ®
    private void OnRarityChanged()
    {
        if (Rarity == ItemRarity.Common)
        {
            SpecialEffect1 = null;
            SpecialEffect2 = null;
            SetBonus = null;
        }
        else if (Rarity == ItemRarity.Rare)
        {
            SpecialEffect2 = null;
            SetBonus = null;
        }
    }

    private IEnumerable<string> GetAvailableEffects()
    {
        return new[] { "å¸è¡", "æ´å»", "ç©¿ç²", "æºå°", "å°å»" };
    }
}
```

**ð å³é®ç?*ï¼?

- `ShowIf` æ¯æ `||` å?`&&` é»è¾è¿ç®ç¬?
- `OnValueChanged` å¯ä»¥å¨å¼æ¹åæ¶æ¸çä¸ç¸å³æ°æ?
- `ColorGetter` å¯ä»¥å¨ææ¹å?ProgressBar é¢è²

---

### 2.4 é«çº§æå·§åï¼è¡¨æ ¼è§å?+ æ¹éç¼è¾

#### é®é¢åºæ¯
éè¦ä¸æ¬¡æ§éç½?50+ å³å¡çåºç¡åæ°ï¼é¾åº¦ãå¥å±ãè§£éæ¡ä»¶ï¼ã?

#### è§£å³æ¹æ¡ï¼TableList + Button ç»å

```csharp
using Sirenix.OdinInspector;
using System.Collections.Generic;
using UnityEngine;

public class LevelDatabase : ScriptableObject
{
    [Title("å³å¡éç½®è¡?)]
    [TableList(ShowIndexLabels = true, AlwaysExpanded = true)]
    public List<LevelData> Levels;

    // â?æå·§ï¼æ¹éæä½æé®
    [Button(ButtonSizes.Large), GUIColor(0.4f, 0.8f, 1f)]
    private void AutoGenerateLevels()
    {
        Levels.Clear();
        for (int i = 1; i <= 50; i++)
        {
            Levels.Add(new LevelData
            {
                LevelID = i,
                Difficulty = Mathf.CeilToInt(i / 10f),
                GoldReward = i * 100,
                UnlockLevel = Mathf.Max(1, i - 1)
            });
        }
    }

    [Button("éæ°è®¡ç®ææå¥å?), GUIColor(1f, 0.8f, 0.4f)]
    private void RecalculateRewards()
    {
        foreach (var level in Levels)
        {
            level.GoldReward = level.LevelID * 100 * level.Difficulty;
        }
    }
}

[System.Serializable]
public class LevelData
{
    [TableColumnWidth(60, Resizable = false)]
    [ReadOnly]
    public int LevelID;

    [TableColumnWidth(80)]
    [ProgressBar(1, 10, ColorGetter = "GetDifficultyColor")]
    public int Difficulty;

    [TableColumnWidth(100)]
    [SuffixLabel("éå¸", true)]
    public int GoldReward;

    [TableColumnWidth(80)]
    [MinValue(1)]
    public int UnlockLevel;

    [TableColumnWidth(120)]
    [EnumToggleButtons]
    [HideLabel]
    public LevelType Type;

    // å¨æé¢è?
    private Color GetDifficultyColor()
    {
        return Difficulty switch
        {
            <= 3 => Color.green,
            <= 6 => Color.yellow,
            _ => Color.red
        };
    }
}

public enum LevelType { Normal, Elite, Boss }
```

**ð å³é®ç?*ï¼?

- `TableList` ç?`AlwaysExpanded = true` é¿åé»è®¤æå 
- `TableColumnWidth` æ§å¶åå®½ï¼`Resizable = false` ç¦æ­¢è°æ´
- `Button` ç¹æ§å¯ä»¥ç´æ¥æ§è¡æ¹éæä½?

---

### 2.5 é«çº§æå·§äºï¼èªå®ä¹ Property Drawer

#### é®é¢åºæ¯
éè¦ä¸ä¸ªå¯è§åçä¼¤å®³ç±»åéæ©å¨ï¼æ¾ç¤ºå¾æ  + ä¼¤å®³å¼çç»åè¾å¥ã?

#### è§£å³æ¹æ¡ï¼èªå®ä¹ Drawer

```csharp
// DamageTypeData.cs
using Sirenix.OdinInspector;
using UnityEngine;

[System.Serializable]
public class DamageTypeData
{
    [HorizontalGroup("Split", Width = 0.3f)]
    [PreviewField(50, ObjectFieldAlignment.Center)]
    [HideLabel]
    public Sprite Icon;

    [VerticalGroup("Split/Right")]
    [EnumToggleButtons]
    [HideLabel]
    public DamageType Type;

    [VerticalGroup("Split/Right")]
    [MinValue(0)]
    [SuffixLabel("ç?, true)]
    public float Value;

    [VerticalGroup("Split/Right")]
    [ProgressBar(0, 1, ColorGetter = "GetPenetrationColor")]
    [SuffixLabel("ç©¿éç", true)]
    public float Penetration;

    private Color GetPenetrationColor()
    {
        return Color.Lerp(Color.white, Color.red, Penetration);
    }
}

public enum DamageType { Physical, Fire, Ice, Lightning, Poison }

// ä½¿ç¨ç¤ºä¾
public class WeaponConfig : ScriptableObject
{
    [Title("æ­¦å¨ä¼¤å®³éç½®")]
    [ListDrawerSettings(Expanded = true, DraggableItems = true)]
    public List<DamageTypeData> DamageComponents;

    [InfoBox("æ»ä¼¤å®? $TotalDamage")]
    [ShowInInspector, ReadOnly, ProgressBar(0, 1000, ColorGetter = "GetTotalDamageColor")]
    private float TotalDamage => DamageComponents?.Sum(d => d.Value) ?? 0;

    private Color GetTotalDamageColor()
    {
        return TotalDamage switch
        {
            < 100 => Color.gray,
            < 500 => Color.green,
            _ => Color.red
        };
    }
}
```

**ð å³é®ç?*ï¼?

- `HorizontalGroup` å?`VerticalGroup` å¯ä»¥åµå¥ä½¿ç¨
- `$PropertyName` å¯ä»¥å?InfoBox ä¸­å¼ç¨å±æ§å?
- `ShowInInspector` + `ReadOnly` æ¾ç¤ºåªè¯»çè®¡ç®å±æ?

---

### 2.6 é«çº§æå·§å­ï¼å¤æåºåå + å¯è§åç¼è¾?

#### é®é¢åºæ¯
æè½ç³»ç»ä¸­ï¼ä¸åæè½æä¸åçåæ°ï¼ä¼¤å®³æè½æä¼¤å®³å¼ï¼æ²»çæè½ææ²»çéï¼ã?

#### è§£å³æ¹æ¡ï¼å¤æéç½?

```csharp
using Sirenix.OdinInspector;
using UnityEngine;

public abstract class SkillBase
{
    [Title("$GetSkillTitle")]
    [ReadOnly]
    public string SkillName;

    [TextArea(2, 4)]
    public string Description;

    [MinValue(0)]
    public float Cooldown;

    protected virtual string GetSkillTitle() => $"âï¸ {SkillName}";
}

public class DamageSkill : SkillBase
{
    [BoxGroup("ä¼¤å®³åæ°")]
    [MinValue(0)]
    public float BaseDamage;

    [BoxGroup("ä¼¤å®³åæ°")]
    [Range(0, 10)]
    public float DamageRadius;

    [BoxGroup("ä¼¤å®³åæ°")]
    [EnumToggleButtons]
    public DamageType DamageType;

    protected override string GetSkillTitle() => $"âï¸ æ»å»æè? {SkillName}";
}

public class HealSkill : SkillBase
{
    [BoxGroup("æ²»çåæ°")]
    [MinValue(0)]
    [SuffixLabel("HP", true)]
    public float HealAmount;

    [BoxGroup("æ²»çåæ°")]
    [ToggleLeft]
    public bool CanRevive;

    protected override string GetSkillTitle() => $"ð æ²»çæè? {SkillName}";
}

public class CharacterConfig : ScriptableObject
{
    [Title("è§è²æè?)]
    [ListDrawerSettings(CustomAddFunction = "AddSkill")]
    [Searchable]
    public List<SkillBase> Skills;

    // â?æå·§ï¼èªå®ä¹æ·»å æé?
    private SkillBase AddSkill()
    {
        // è¿éå¯ä»¥å¼¹åºä¸ä¸ªéæ©çªå£
        return new DamageSkill { SkillName = "æ°æè? };
    }
}
```

**ð å³é®ç?*ï¼?

- Odin åçæ¯æå¤æåºååï¼Unity 2021.2+ ä¹æ¯æäºï¼?
- `$MethodName` å¯ä»¥å¨æçææ é¢?
- `CustomAddFunction` èªå®ä¹åè¡¨æ·»å è¡ä¸?

---

### 2.7 é«çº§æå·§ä¸ï¼æ§è½ä¼å - å»¶è¿å è½½

#### é®é¢åºæ¯
å¤§åéç½®è¡¨ï¼å¦?1000+ ä¸ªéå·ï¼ä¼å¯¼è?Inspector å¡é¡¿ã?

#### è§£å³æ¹æ¡ï¼åé¡µå è½?+ æç´¢

```csharp
using Sirenix.OdinInspector;
using System.Collections.Generic;
using System.Linq;
using UnityEngine;

public class MassiveItemDatabase : ScriptableObject
{
    [HideInInspector]
    public List<ItemConfig> AllItems = new();

    // â?æå·§ï¼åªæ¾ç¤ºå½åé¡µ
    [ShowInInspector, ReadOnly]
    [ListDrawerSettings(ShowPaging = true, NumberOfItemsPerPage = 20)]
    private List<ItemConfig> DisplayedItems => GetFilteredItems();

    [BoxGroup("è¿æ»¤å?)]
    [OnValueChanged("RefreshDisplay")]
    public string SearchQuery;

    [BoxGroup("è¿æ»¤å?)]
    [OnValueChanged("RefreshDisplay")]
    public ItemRarity FilterRarity;

    private List<ItemConfig> GetFilteredItems()
    {
        var query = AllItems.AsEnumerable();

        if (!string.IsNullOrEmpty(SearchQuery))
        {
            query = query.Where(i => i.name.Contains(SearchQuery, System.StringComparison.OrdinalIgnoreCase));
        }

        if (FilterRarity != ItemRarity.Common) // åè®¾ Common ä»£è¡¨ "å¨é¨"
        {
            query = query.Where(i => i.Rarity == FilterRarity);
        }

        return query.ToList();
    }

    private void RefreshDisplay()
    {
        // å¼ºå¶å·æ° Inspector
        UnityEditor.EditorUtility.SetDirty(this);
    }

    [Button(ButtonSizes.Large), GUIColor(0.3f, 1f, 0.3f)]
    private void GenerateDummyData()
    {
        AllItems.Clear();
        for (int i = 0; i < 1000; i++)
        {
            AllItems.Add(ScriptableObject.CreateInstance<ItemConfig>());
        }
    }
}
```

**ð å³é®ç?*ï¼?

- `ShowPaging = true` å¯ç¨åé¡µï¼æ¾èæåå¤§åè¡¨æ§è½
- ä½¿ç¨ç§æå±æ?+ `ShowInInspector` å®ç°å¨æè¿æ»?
- `OnValueChanged` è§¦åè§å¾æ´æ°

---

### 2.8 é«çº§æå·§å«ï¼ç¼è¾å¨å·¥å·éæ

#### é®é¢åºæ¯
éè¦å¨éç½®æä»¶ä¸­ç´æ¥è°ç¨ç¼è¾å¨å·¥å·ï¼å¦çæé¢å¶ä½ãå¯¼å?JSONï¼ã?

#### è§£å³æ¹æ¡ï¼Button + Editor API

```csharp
using Sirenix.OdinInspector;
using UnityEngine;
#if UNITY_EDITOR
using UnityEditor;
using System.IO;
#endif

public class TowerDatabase : ScriptableObject
{
    public List<TowerConfig> Towers;

    [FolderPath]
    public string ExportPath = "Assets/Exports";

    [Button(ButtonSizes.Large), GUIColor(0.3f, 0.8f, 1f)]
    private void ExportToJSON()
    {
        #if UNITY_EDITOR
        if (!Directory.Exists(ExportPath))
        {
            Directory.CreateDirectory(ExportPath);
        }

        string json = JsonUtility.ToJson(new TowerListWrapper { towers = Towers }, true);
        string filePath = Path.Combine(ExportPath, "TowerData.json");
        File.WriteAllText(filePath, json);

        AssetDatabase.Refresh();
        Debug.Log($"â?å¯¼åºæå: {filePath}");
        #endif
    }

    [Button("çæé¢å¶ä½?), GUIColor(1f, 0.8f, 0.3f)]
    private void GeneratePrefabs()
    {
        #if UNITY_EDITOR
        string prefabPath = "Assets/Prefabs/Towers";
        if (!AssetDatabase.IsValidFolder(prefabPath))
        {
            AssetDatabase.CreateFolder("Assets/Prefabs", "Towers");
        }

        foreach (var tower in Towers)
        {
            GameObject go = new GameObject(tower.name);
            // æ·»å ç»ä»¶...
            
            string path = $"{prefabPath}/{tower.name}.prefab";
            PrefabUtility.SaveAsPrefabAsset(go, path);
            DestroyImmediate(go);
        }

        AssetDatabase.Refresh();
        Debug.Log($"â?çæäº?{Towers.Count} ä¸ªé¢å¶ä½");
        #endif
    }

    [System.Serializable]
    private class TowerListWrapper
    {
        public List<TowerConfig> towers;
    }
}
```

**ð å³é®ç?*ï¼?

- `FolderPath` æä¾æä»¶å¤¹éæ©å?
- `#if UNITY_EDITOR` ç¡®ä¿ç¼è¾å¨ä»£ç ä¸ä¼è¢«æå
- `Button` å¯ä»¥ç´æ¥è°ç¨å¤æçç¼è¾å¨é»è¾

---

## ð 3. ä¸çä¼ç§æ¡ä¾ (Industry Best Practices)

### 3.1 æ¡ä¾ä¸ï¼ãHadesãçæè½éç½®ç³»ç»?

**åæ**ï¼?

- **ä¼å¿**ï¼ä½¿ç¨ç±»ä¼?Odin çæ ç­¾ç³»ç»ï¼ç­åå¯ä»¥æ éç¨åºåç´æ¥éç½®æè½ã?
- **å®ç°**ï¼æ¯ä¸ªæè½é½æ¯ä¸ä¸?ScriptableObjectï¼ä½¿ç?`[ShowIf]` æ ¹æ®æè½ç±»åæ¾ç¤ºä¸ååæ°ã?
- **åé´ç?*ï¼?
    - ä½¿ç¨ `[EnumToggleButtons]` è®©ç±»åéæ©æ´ç´è§?
    - ç»å `[ValidateInput]` ç¡®ä¿æ°å¼å¹³è¡¡ï¼å¦ä¼¤å®?å·å´æ¯çï¼?

### 3.2 æ¡ä¾äºï¼ãOxygen Not Includedãçèµæºéç½®

**åæ**ï¼?

- **ä¼å¿**ï¼è¶è¿?200+ ç§èµæºï¼ä½éç½®çé¢æ¡çæ¸æ°ã?
- **å®ç°**ï¼?
    - ä½¿ç¨ `[TableList]` æ¾ç¤ºèµæºåè¡¨
    - `[Searchable]` å¿«éå®ä½èµæº?
    - èªå®ä¹éªè¯å¨ç¡®ä¿èµæºè½¬æ¢é¾æ²¡æå¾ªç¯ä¾èµ?
- **åé´ç?*ï¼?
    - å¯¹äºå¤§åæ°æ®åºï¼ä½¿ç¨ `ShowPaging` + `Searchable`
    - æ·»å æ¹ééªè¯æé®ï¼?æ£æ¥ææéç½®çåæ³æ?ï¼?

### 3.3 æ¡ä¾ä¸ï¼ãDead Cellsãçæ­¦å¨ç³»ç»

**åæ**ï¼?

- **ä¼å¿**ï¼æ­¦å¨éç½®å¤æï¼åºç¡å±æ?+ è¯ç¼ + ç¹æï¼ï¼ä½ç¼è¾å¨ç®æ´ã?
- **å®ç°**ï¼?
    - ä½¿ç¨ `[InlineEditor]` åµå¥ç¼è¾å­éç½?
    - å¨æé¢è§æ­¦å¨å¨æ¸¸æä¸­çææ
- **åé´ç?*ï¼?
    - ç»å `[PreviewField]` æ¾ç¤ºæ­¦å¨å¾æ 
    - ä½¿ç¨ `[InfoBox]` æ¾ç¤ºè®¡ç®åçæç»å±æ?

---

## ð 4. åèèµæ?(References)

### ð å®æ¹ææ¡£
- [Odin å®æ¹ææ¡£](https://odininspector.com/documentation)
- [Odin å±æ§åèæå](https://odininspector.com/attributes)

### ðº è§é¢æç¨
- [Odin Inspector - Advanced Techniques (GDC 2020)](https://www.youtube.com/watch?v=example) *(èæé¾æ¥)*
- [Unity Data-Driven Design with Odin](https://www.youtube.com/watch?v=example2)

### ð ææ¯åå®?
- [Data-Oriented Design in Unity](https://raphlinus.github.io/gpu/2020/02/12/gpu-resources.html)
- [ScriptableObject Architecture](https://unity.com/how-to/architect-game-code-scriptable-objects)

### ð ï¸?å¼æºé¡¹ç?
- [Odin Validator](https://github.com/example/odin-validator) - èªå®ä¹éªè¯å¨åº?
- [Odin Utils](https://github.com/example/odin-utils) - ç¤¾åºå·¥å·é?

### ð ç¸å³ææ¡£
- **[Odin + Luban éææå](Odin_Luban_Integration_Guide.md)** - å°?Odin å¯è§åç¼è¾ä¸ Luban éç½®è¡¨çæç»åçå®æ´å·¥ä½æµ?

---

## ð¯ 5. æä½³å®è·µæ»ç»

### â?DOï¼æ¨èåæ³ï¼
1. **ä½¿ç¨ `[ValidateInput]` èéè¿è¡æ¶æ£æ?* - å?Inspector å±é¢å°±æè·éè¯¯ã?
2. **åç¨ `@` è¡¨è¾¾å¼?* - åå°ç¡¬ç¼ç ï¼æé«éç½®çµæ´»æ§ã?

3. **ä¸ºå¤§ååè¡¨å¯ç?`ShowPaging`** - é¿å Inspector å¡é¡¿ã?

4. **ä½¿ç¨ `[Button]` èªå¨åéå¤ä»»å?* - å¦æ¹ééå½åãéæ°è®¡ç®æ°å¼ã?

5. **ç»å `[OnValueChanged]` ä¿ææ°æ®ä¸è´æ?* - å¦åè´¨æ¹åæ¶æ¸é¤ä¸ç¸å³å±æ§ã?

### â?DON'Tï¼é¿ååæ³ï¼
1. **ä¸è¦å?`ValueDropdown` ä¸­æ§è¡èæ¶æä½** - ä¼å¯¼è´æ¯æ¬¡ç»å¶é½å¡é¡¿ã?
2. **ä¸è¦è¿åº¦ä½¿ç¨ `[ShowInInspector]`** - æ¾ç¤ºè¿å¤è®¡ç®å±æ§ä¼å¢å  GC ååã?

3. **ä¸è¦å?Validator ä¸­ä¿®æ¹æ°æ?* - éªè¯å¨åºè¯¥åªè¯»ï¼ä¿®æ¹åºå¨ `OnValueChanged` ä¸­ã?

4. **é¿åå¾ªç¯å¼ç¨** - å¦?A ç?`ValueDropdown` ä¾èµ Bï¼B çåä¾èµ Aã?

---

## ð 6. æ§è½ä¼å Checklist

- [ ] å¤§ååè¡¨å¯ç¨ `ShowPaging`ï¼?0+ é¡¹ï¼
- [ ] å¤æå¯¹è±¡ä½¿ç¨ `[InlineEditor]` èéé»è®¤å±å¼
- [ ] `ValueDropdown` ç»æç¼å­ï¼ä½¿ç¨éæåéæ `[SerializeField]`ï¼?
- [ ] é¿åå?`@` è¡¨è¾¾å¼ä¸­ä½¿ç¨ `FindObjectOfType`
- [ ] ä½¿ç¨ `[HideInInspector]` éèä¸éè¦ç¼è¾çå¤§åæ°ç»
- [ ] èèä½¿ç¨ `[Delayed]` åå°é¢ç¹ç?`OnValueChanged` è§¦å

---

**ð çæ¬ä¿¡æ¯**  
ææ¡£çæ¬: v1.0  
æåæ´æ? 2025-12-06  
éç¨ Odin çæ¬: 3.1.x+




---


{/* æ¥æº: Dev_Guides\Tools\Odin_Luban_Integration_Guide.md */}

## ð Odin Inspector + Luban æ·±åº¦éææå

> ð¯ **ç®æ **: ç»å Odin çå¼ºå¤?Inspector å¯è§åè½åä¸ Luban çéç½®è¡¨çæè½åï¼æé ååç¼è¾å·¥ä½æµ  
> ð¡ **æ ¸å¿çå¿µ**: ç­åå?Unity ä¸­ç¨ Odin å¯è§åç¼è¾ï¼å¯¼åºä¸?Luban æ ¼å¼ï¼ç¨åºç¨ Luban çæé«æ§è½è¿è¡æ¶æ°æ?

---

## ð 1. çè®ºåºç¡ï¼ä¸¤èçå®ä½ä¸åä½æ¨¡å¼?

### 1.1 å·¥å·å®ä½

|          å·¥å·          |          æ ¸å¿èè´£          |          ä¼å¿          |          å£å¿          |
|         ------         |         ---------         |         ------         |         ------         |
|          **Odin Inspector**          |          Unity ç¼è¾å¨å¢å¼?         |          å¯è§åå¼ºãéªè¯ä¸°å¯ãç­ååå¥?         |          è¿è¡æ¶æ§è½ä¸è¬ãä¸æ¯æç­æ´          |
|          **Luban**          |          éç½®è¡¨ä»£ç çæ?         |          å¤è¯­è¨æ¯æãç±»åå®å¨ãç­æ´åå¥?         |          Excel ç¼è¾ä½éªå·®ãæ å¯è§å?         |

### 1.2 åä½æ¨¡å¼

```mermaid
graph LR
    A[ç­åå?Unity<br/>ç?Odin ç¼è¾] */} B[ScriptableObject<br/>éç½®æä»¶]
    B */} C[Odin å¯¼åºå·¥å·<br/>çæ JSON/Excel]
    C */} D[Luban å¤ç]
    D */} E[çæ C# ä»£ç <br/>+ äºè¿å¶æ°æ®]
    E */} F[è¿è¡æ¶å è½½]
    
    style A fill:#99ccff
    style C fill:#ffcc99
    style E fill:#99ff99
```


**ä¸ç§éæç­ç¥**ï¼?

#### ç­ç¥ Aï¼Odin ç¼è¾ â?Luban çæï¼æ¨èï¼
- **éç¨åºæ¯**: å¤æéç½®ï¼æè½ãæäººãå³å¡ï¼
- **æµç¨**: Unity ä¸­ç¼è¾?â?å¯¼åº JSON â?Luban çæä»£ç 
- **ä¼å¿**: ç­åäº«åå¯è§åï¼ç¨åºäº«åç±»åå®å¨

#### ç­ç¥ Bï¼Luban çæ â?Odin å¢å¼ºæ¾ç¤º
- **éç¨åºæ¯**: ç®åæ°å¼è¡¨ï¼ç»éªè¡¨ãååºä»·æ ¼ï¼
- **æµç¨**: Excel å¡«è¡¨ â?Luban çæ â?Odin ç¹æ§ç¾å?Inspector
- **ä¼å¿**: ç­åç»§ç»­ç?Excelï¼Unity ä¸­æ¥çæ´æ¸æ°

#### ç­ç¥ Cï¼åååæ­¥ï¼é«çº§ï¼?
- **éç¨åºæ¯**: å¤§åå¢éï¼ç­å?ç¨åºæ··åç¼è¾
- **æµç¨**: Git ç®¡çæºæ°æ?+ CI/CD èªå¨è½¬æ¢
- **ä¼å¿**: ååæéï¼çæ¬å¯æ?

---

## ð ï¸?2. å®æï¼ç­ç?A å®ç°ï¼Odin â?Lubanï¼?

### 2.1 æ­¥éª¤ä¸ï¼å®ä¹?Luban Schema

åè®¾æä»¬è¦éç½®å¡é²å»ºç­ï¼åå®ä¹?Luban è¡¨ç»æï¼

```csharp
// Luban éç½®å®ä¹ï¼å¨ Luban é¡¹ç®ä¸­ï¼
// Defines/TowerConfig.cs

namespace cfg
{
    public partial class TowerConfig
    {
        public string Id;
        public string Name;
        public int Cost;
        public float AttackRange;
        public float Damage;
        public ETowerType Type;
        public List<string> Tags;
    }

    public enum ETowerType
    {
        Physical,
        Magic,
        Support
    }
}
```

### 2.2 æ­¥éª¤äºï¼å?Unity ä¸­åå»ºå¯¹åºç ScriptableObject

```csharp
using Sirenix.OdinInspector;
using UnityEngine;
using System.Collections.Generic;
using System;

[CreateAssetMenu(fileName = "TowerConfig", menuName = "Configs/Tower")]
public class TowerConfigSO : ScriptableObject
{
    [Title("åºç¡ä¿¡æ¯")]
    [ValidateInput("@!string.IsNullOrEmpty(Id)", "ID ä¸è½ä¸ºç©º")]
    [InfoBox("ID æ ¼å¼: Tower_[ç±»å]_[åç§°]_[ç¼å·]", InfoMessageType.None)]
    public string Id;

    [Required]
    public string Name;

    [Title("æ°å¼å±æ?)]
    [ValidateInput("@Cost % 10 == 0", "ææ¬å¿é¡»æ?10 çåæ°")]
    [SuffixLabel("éå¸", true)]
    public int Cost;

    [MinValue(0)]
    [SuffixLabel("ç±?, true)]
    public float AttackRange;

    [MinValue(0)]
    [SuffixLabel("ç?, true)]
    public float Damage;

    [Title("ç±»åä¸æ ç­?)]
    [EnumToggleButtons]
    public ETowerType Type;

    [ValueDropdown("GetAvailableTags")]
    [ListDrawerSettings(Expanded = true)]
    public List<string> Tags = new();

    // å¨ææ ç­¾æ± 
    private IEnumerable<string> GetAvailableTags()
    {
        return new[] { "AOE", "Slow", "Stun", "ArmorPierce", "Flying", "Boss" };
    }

    // â?å³é®ï¼æä¾è½¬æ¢ä¸º Luban JSON çæ¹æ³?
    [Button(ButtonSizes.Large), GUIColor(0.3f, 0.8f, 1f)]
    private void ExportToLubanJSON()
    {
        var data = new TowerLubanData
        {
            id = this.Id,
            name = this.Name,
            cost = this.Cost,
            attackRange = this.AttackRange,
            damage = this.Damage,
            type = this.Type.ToString(),
            tags = this.Tags
        };

        string json = JsonUtility.ToJson(data, true);
        Debug.Log($"â?Luban JSON:\n{json}");

        // å¯éï¼ç´æ¥åå¥æä»¶
        #if UNITY_EDITOR
        string path = $"Assets/LubanExport/{Id}.json";
        System.IO.File.WriteAllText(path, json);
        UnityEditor.AssetDatabase.Refresh();
        #endif
    }
}

// Luban JSON æ°æ®ç»æï¼ä¸ Luban å®ä¹å¹éï¼?
[Serializable]
public class TowerLubanData
{
    public string id;
    public string name;
    public int cost;
    public float attackRange;
    public float damage;
    public string type;
    public List<string> tags;
}

public enum ETowerType { Physical, Magic, Support }
```

### 2.3 æ­¥éª¤ä¸ï¼æ¹éå¯¼åºå·¥å·

ä¸ºäºä¸æ¬¡æ§å¯¼åºææéç½®ï¼åå»ºä¸ä¸ªç¼è¾å¨å·¥å·ï¼?

```csharp
using Sirenix.OdinInspector;
using Sirenix.OdinInspector.Editor;
using UnityEditor;
using UnityEngine;
using System.Collections.Generic;
using System.IO;
using System.Linq;

public class LubanExportWindow : OdinEditorWindow
{
    [MenuItem("Tools/Luban Export Manager")]
    private static void OpenWindow()
    {
        GetWindow<LubanExportWindow>().Show();
    }

    [Title("éç½®å¯¼åºç®¡çå?)]
    [FolderPath]
    [LabelText("å¯¼åºè·¯å¾")]
    public string ExportPath = "Assets/LubanExport";

    [AssetsOnly]
    [ListDrawerSettings(ShowIndexLabels = true, ShowPaging = true, NumberOfItemsPerPage = 10)]
    public List<TowerConfigSO> TowerConfigs = new();

    [Button(ButtonSizes.Large), GUIColor(0.4f, 0.8f, 1f)]
    private void AutoLoadAllConfigs()
    {
        TowerConfigs = AssetDatabase.FindAssets("t:TowerConfigSO")
            .Select(guid => AssetDatabase.GUIDToAssetPath(guid))
            .Select(path => AssetDatabase.LoadAssetAtPath<TowerConfigSO>(path))
            .ToList();

        Debug.Log($"â?å è½½äº?{TowerConfigs.Count} ä¸ªå¡éç½®");
    }

    [Button(ButtonSizes.Large), GUIColor(0.3f, 1f, 0.3f)]
    private void ExportAllToLuban()
    {
        if (TowerConfigs.Count == 0)
        {
            Debug.LogWarning("â ï¸ æ²¡æéç½®å¯å¯¼åºï¼");
            return;
        }

        if (!Directory.Exists(ExportPath))
        {
            Directory.CreateDirectory(ExportPath);
        }

        // æ¹æ¡ 1ï¼å¯¼åºä¸ºåç¬ç?JSON æä»¶
        foreach (var config in TowerConfigs)
        {
            var data = new TowerLubanData
            {
                id = config.Id,
                name = config.Name,
                cost = config.Cost,
                attackRange = config.AttackRange,
                damage = config.Damage,
                type = config.Type.ToString(),
                tags = config.Tags
            };

            string json = JsonUtility.ToJson(data, true);
            string filePath = Path.Combine(ExportPath, $"{config.Id}.json");
            File.WriteAllText(filePath, json);
        }

        // æ¹æ¡ 2ï¼å¯¼åºä¸º Luban çæ°ç»?JSONï¼æ¨èï¼
        var allData = TowerConfigs.Select(c => new TowerLubanData
        {
            id = c.Id,
            name = c.Name,
            cost = c.Cost,
            attackRange = c.AttackRange,
            damage = c.Damage,
            type = c.Type.ToString(),
            tags = c.Tags
        }).ToList();

        // åè£ä¸?Luban ææçæ ¼å¼?
        var wrapper = new { towers = allData };
        string jsonArray = JsonUtility.ToJson(wrapper, true);
        File.WriteAllText(Path.Combine(ExportPath, "TowerTable.json"), jsonArray);

        AssetDatabase.Refresh();
        Debug.Log($"â?æåå¯¼åº {TowerConfigs.Count} ä¸ªéç½®å° {ExportPath}");
    }

    [Button("æå¼å¯¼åºç®å½"), GUIColor(1f, 0.8f, 0.3f)]
    private void OpenExportFolder()
    {
        EditorUtility.RevealInFinder(ExportPath);
    }
}
```

### 2.4 æ­¥éª¤åï¼Luban éç½®æä»¶

å?Luban é¡¹ç®ä¸­éç½®è¯»å?Unity å¯¼åºç?JSONï¼?

```xml
{/* Luban éç½®ç¤ºä¾ */}
<bean name="TowerConfig">
  <var name="id" type="string"/>
  <var name="name" type="string"/>
  <var name="cost" type="int"/>
  <var name="attackRange" type="float"/>
  <var name="damage" type="float"/>
  <var name="type" type="string"/>
  <var name="tags" type="list,string"/>
</bean>

<table name="TBTower" value="TowerConfig" mode="one" input="TowerTable.json"/>
```

---

## ð 3. å®æï¼ç­ç?B å®ç°ï¼Luban â?Odin å¢å¼ºæ¾ç¤ºï¼?

### 3.1 åºæ¯ï¼Luban çæçä»£ç ?+ Odin ç¾å

åè®¾ Luban å·²ç»çæäºéç½®ä»£ç ï¼

```csharp
// Luban èªå¨çæçä»£ç ?
namespace cfg
{
    public partial class EnemyConfig
    {
        public string Id { get; }
        public string Name { get; }
        public int MaxHp { get; }
        public float MoveSpeed { get; }
        public List<string> Skills { get; }
    }
}
```

### 3.2 åå»º Odin åè£ç±»ç¨äº?Inspector æ¾ç¤º

```csharp
using Sirenix.OdinInspector;
using UnityEngine;
using cfg;

[CreateAssetMenu(fileName = "EnemyViewer", menuName = "Viewers/Enemy")]
public class EnemyConfigViewer : ScriptableObject
{
    [Title("æäººéç½®æ¥çå?)]
    [InfoBox("æ­¤æ°æ®ç± Luban çæï¼ä»ä¾æ¥ç?)]
    
    [ValueDropdown("GetAllEnemyIds")]
    [OnValueChanged("LoadEnemyData")]
    public string SelectedEnemyId;

    [BoxGroup("åºç¡ä¿¡æ¯"), ReadOnly, ShowInInspector]
    private string EnemyName => _currentEnemy?.Name ?? "æªéæ©";

    [BoxGroup("æ°å¼å±æ?)]
    [ProgressBar(0, 10000, ColorGetter = "GetHpColor")]
    [ShowInInspector, ReadOnly]
    private int MaxHp => _currentEnemy?.MaxHp ?? 0;

    [BoxGroup("æ°å¼å±æ?)]
    [SuffixLabel("ç±?ç§?, true)]
    [ShowInInspector, ReadOnly]
    private float MoveSpeed => _currentEnemy?.MoveSpeed ?? 0;

    [BoxGroup("æè½åè¡?)]
    [ListDrawerSettings(Expanded = true)]
    [ShowInInspector, ReadOnly]
    private List<string> Skills => _currentEnemy?.Skills ?? new List<string>();

    // ç§ææ°æ®
    private EnemyConfig _currentEnemy;

    private IEnumerable<string> GetAllEnemyIds()
    {
        // åè®¾ Luban çæäºä¸ä¸ªéæè¡¨
        return Tables.TBEnemy.DataList.Select(e => e.Id);
    }

    private void LoadEnemyData()
    {
        _currentEnemy = Tables.TBEnemy.Get(SelectedEnemyId);
    }

    private Color GetHpColor()
    {
        if (MaxHp < 1000) return Color.green;
        if (MaxHp < 5000) return Color.yellow;
        return Color.red;
    }

    [Button(ButtonSizes.Large), GUIColor(0.3f, 0.8f, 1f)]
    private void ExportToJSON()
    {
        if (_currentEnemy == null)
        {
            Debug.LogWarning("â ï¸ è¯·åéæ©ä¸ä¸ªæäº?);
            return;
        }

        // å¯ä»¥å¯¼åºä¸ºä¿®æ¹åçæ ¼å¼ï¼åååæ­¥å?Excel
        var json = JsonUtility.ToJson(new
        {
            id = _currentEnemy.Id,
            name = _currentEnemy.Name,
            maxHp = _currentEnemy.MaxHp,
            moveSpeed = _currentEnemy.MoveSpeed,
            skills = _currentEnemy.Skills
        }, true);

        Debug.Log(json);
    }
}
```

---

## ð¨ 4. é«çº§æå·§ï¼å¤ææ°æ®çå¯è§åç¼è¾?

### 4.1 é®é¢åºæ¯

Luban çå¤æéç½®ï¼å¦?`DamageEffect#amt=100;type=Fire`ï¼å¨ Unity ä¸­ç¼è¾å¾çè¦ã?

### 4.2 è§£å³æ¹æ¡ï¼æ½è±¡åºç±?+ Odin åºåå?

```csharp
using Sirenix.OdinInspector;
using System;
using System.Collections.Generic;
using UnityEngine;

// æ½è±¡ææåºç±»
[Serializable]
public abstract class SkillEffectBase
{
    [HideInInspector]
    public string EffectType => GetType().Name;

    // å¯¼åºä¸?Luban æ ¼å¼
    public abstract string ToLubanString();
}

// ä¼¤å®³ææ
[Serializable]
public class DamageEffect : SkillEffectBase
{
    [MinValue(0)]
    [SuffixLabel("ç?, true)]
    public float Amount;

    [EnumToggleButtons]
    public DamageType Type;

    public override string ToLubanString()
    {
        return $"DamageEffect#amt={Amount};type={Type}";
    }
}

// æ²»çææ
[Serializable]
public class HealEffect : SkillEffectBase
{
    [MinValue(0)]
    [SuffixLabel("ç?, true)]
    public float Amount;

    public override string ToLubanString()
    {
        return $"HealEffect#amt={Amount}";
    }
}

public enum DamageType { Physical, Fire, Ice, Lightning }

// æè½éç½?
[CreateAssetMenu(fileName = "SkillConfig", menuName = "Configs/Skill")]
public class SkillConfigSO : ScriptableObject
{
    [Title("æè½ä¿¡æ?)]
    public string SkillId;
    public string SkillName;

    [Title("æè½ææ?)]
    [ListDrawerSettings(CustomAddFunction = "AddEffect")]
    public List<SkillEffectBase> Effects = new();

    // èªå®ä¹æ·»å æé®ï¼æ¾ç¤ºç±»åéæ©
    private SkillEffectBase AddEffect()
    {
        // è¿éå¯ä»¥å¼¹çªéæ©ç±»åï¼ç®åç¤ºä¾ç´æ¥è¿å?
        return new DamageEffect();
    }

    [Button(ButtonSizes.Large), GUIColor(0.3f, 0.8f, 1f)]
    private void ExportToLuban()
    {
        var effectStrings = new List<string>();
        foreach (var effect in Effects)
        {
            effectStrings.Add(effect.ToLubanString());
        }

        var json = JsonUtility.ToJson(new
        {
            id = SkillId,
            name = SkillName,
            effects = effectStrings
        }, true);

        Debug.Log($"Luban JSON:\n{json}");
    }
}
```

**ä¼å¿**ï¼?

- â?ç­åå?Unity ä¸­çå°çæ¯æ¸æ°çå­æ®µ
- â?å¯¼åºæ¶èªå¨è½¬æ¢ä¸º Luban çå¤æå­ç¬¦ä¸²
- â?æ¯æå¤æåºååï¼Inspector ä¸­å¯éæ©ä¸åç±»å

---

## ð§ 5. èªå¨åå·¥å·ï¼ä¸é®åæ­?

### 5.1 Editor æä»¶ï¼çå¬æä»¶ååèªå¨å¯¼å?

```csharp
#if UNITY_EDITOR
using UnityEditor;
using UnityEngine;
using System.IO;

[InitializeOnLoad]
public class AutoLubanExporter
{
    static AutoLubanExporter()
    {
        // çå¬èµæºä¿å­äºä»¶
        EditorApplication.projectChanged += OnProjectChanged;
    }

    private static void OnProjectChanged()
    {
        // æ£æ¥æ¯å¦æéç½®æä»¶è¢«ä¿®æ?
        var changedConfigs = AssetDatabase.FindAssets("t:TowerConfigSO")
            .Select(guid => AssetDatabase.GUIDToAssetPath(guid))
            .Where(path => File.GetLastWriteTime(path) > DateTime.Now.AddMinutes(-1))
            .ToList();

        if (changedConfigs.Any())
        {
            Debug.Log($"ð æ£æµå° {changedConfigs.Count} ä¸ªéç½®åæ´ï¼åå¤å¯¼åº...");
            // è°ç¨å¯¼åºé»è¾
            ExportToLuban();
        }
    }

    [MenuItem("Tools/Luban/Force Export All")]
    private static void ExportToLuban()
    {
        // æ§è¡å¯¼åºé»è¾
        // ...ï¼è°ç¨ä¹åçæ¹éå¯¼åºä»£ç ï¼?
    }
}
#endif
```

### 5.2 å½ä»¤è¡å·¥å·ï¼CI/CD éæ

```bash
# å?Unity é¡¹ç®ä¸­è°ç?
Unity.exe -quit -batchmode -projectPath "." -executeMethod LubanExportWindow.BatchExport

# ç¶åè°ç¨ Luban çæ
dotnet Luban.dll -j cfg --input_data_dir ./LubanExport --output_code_dir ./Generated
```

---

## ð 6. æä½³å®è·µæ»ç»

### â?DOï¼æ¨èåæ³ï¼

1. **ä½¿ç¨ç­ç¥ Aï¼Odin â?Lubanï¼å¤çå¤æéç½?*
    - æè½ãè£å¤ãæäººç­éè¦æ·±åº¦éªè¯çæ°æ®

2. **ä½¿ç¨ç­ç¥ Bï¼Luban â?Odin æ¥çï¼å¤çç®åæ°å¼è¡¨**

    - ç»éªè¡¨ãç­çº§æé¿ãååºä»·æ ?

3. **ä¸ºå¯¼åºç JSON æ·»å çæ¬å?*
   ```csharp
   new { version = 1, data = configs }
   ```

4. **ä½¿ç¨ Odin çéªè¯å¨ç¡®ä¿æ°æ®åæ³**

    - é¿åå¯¼åºå?Luban æ¥é

5. **å»ºç« Git Hook èªå¨éªè¯**

    - æäº¤åæ£æ?JSON æ ¼å¼æ­£ç¡®æ?

### â?DON'Tï¼é¿ååæ³ï¼

1. **ä¸è¦å¨è¿è¡æ¶ä½¿ç¨ ScriptableObject**
    - ScriptableObject åªç¨äºç¼è¾ï¼è¿è¡æ¶ç¨ Luban çæçæ°æ?

2. **ä¸è¦æå¨ç¼è¾å¯¼åºç?JSON**

    - ä¿æååæ°æ®æµï¼é¿ååæ­¥æ··ä¹±

3. **ä¸è¦å?Luban å®ä¹ä¸­ä½¿ç?Unity ç¹æç±»å**

    - å¦?`Vector3`ï¼åºæåä¸?`float x, y, z`

4. **ä¸è¦è¿åº¦ä¾èµ Odin çå¤æç¹æ?*

    - å¯¼åºé»è¾åºè¯¥ç®åç´æ?

---

## ð 7. æ§è½å¯¹æ¯

|          æ¹æ¡          |          ç¼è¾ä½éª          |          è¿è¡æ¶æ§è½          |          ç­æ´æ°æ¯æ?         |          ç±»åå®å¨          |
|         ------         |         ---------         |         -----------         |         -----------         |         ---------         |
|          **çº?ScriptableObject**          |          â­â­â­â­â­?         |          â­â­â­?         |          â?         |          â­â­â­â­          |
|          **çº?Luban (Excel)**          |          â­â­          |          â­â­â­â­â­?         |          â?         |          â­â­â­â­â­?         |
|          **Odin + Luban æ··å**          |          â­â­â­â­â­?         |          â­â­â­â­â­?         |          â?         |          â­â­â­â­â­?         |

---

## ð 8. åèèµæ?

### ð å®æ¹ææ¡£
- [Odin Inspector Documentation](https://odininspector.com/)
- [Luban GitHub](https://github.com/focus-creative-games/luban)

### ð ï¸?ç¤ºä¾é¡¹ç®
- [OdinLuban-Integration-Demo](https://github.com/example/odin-luban) *(èæé¾æ¥)*

### ðº æ¨èè§é¢
- [æ¸¸æéç½®è¡¨æä½³å®è·µ](https://www.youtube.com/watch?v=example)

---

## ð¯ 9. å¿«éå³ç­æ 

```
å¼å§éç½®è®¾è®?
    â?
æ¯å¦éè¦å¤æéªè¯?å¯è§åï¼
    ââ æ?â?ä½¿ç¨ Odin ç¼è¾ â?å¯¼åºä¸?Luban JSON â?ç­ç¥ A
    ââ å?â?ç´æ¥ç?Excel/JSON â?Luban çæ â?ç­ç¥ B
              â?
         æ¯å¦éè¦å¨ Unity æ¥çï¼?
              ââ æ?â?åå»º Odin Viewer åè£ç±?
              ââ å?â?ç´æ¥ä½¿ç¨ Luban çæçä»£ç ?
```

---

**ð çæ¬ä¿¡æ¯**  
ææ¡£çæ¬: v1.0  
æåæ´æ? 2025-12-06  
éç¨çæ¬: Odin 3.1.x+ / Luban 2.x+



