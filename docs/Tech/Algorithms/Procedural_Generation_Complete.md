---
sidebarTitle: "PCG 绠楁硶缁煎悎鎸囧崡"
---

# PCG 绠楁硶缁煎悎鎸囧崡

> 鏈枃妗ｇ敱浠ヤ笅鏂囦欢鍚堝苟鐢熸垚 (2026-01-09)



---


{/* 鏉ユ簮: Tech\Algorithms\Procedural_Generation_Guide.md */}

## 馃鈥嶁檪锔?鍏冲崱鐢熸垚绠楁硶(PCG)娣卞害鐮旂┒

## 馃摎 1. 鐞嗚鍩虹 (Theoretical Basis)

### 馃幆 鏍稿績瀹氫箟

**绋嬪簭鍖栧唴瀹圭敓鎴?(Procedural Content Generation, PCG)** 鏄€氳繃绠楁硶鑷姩鍒涘缓娓告垙鍐呭鐨勬妧鏈€傚浜嶳oguelike娓告垙锛孭CG鏄牳蹇冩敮鏌便€?

**PCG鐨勪紭鍔?*:

1. **鏃犻檺鍐呭** - 閬垮厤閲嶅鎰?
2. **闄嶄綆鎴愭湰** - 鍑忓皯鎵嬪伐璁捐宸ヤ綔閲?

3. **澧炲姞瀵垮懡** - 姣忔娓哥帺閮戒笉鍚?

**PCG鐨勬寫鎴?*:

1. **璐ㄩ噺鎺у埗** - 鐢熸垚缁撴灉鍙兘涓嶅彲鐜?
2. **鎬ц兘寮€閿€** - 鐢熸垚绠楁硶鍙兘寰堟參

3. **骞宠　鎬?* - 闅惧害/濂栧姳鍙兘澶辫　

### 馃搻 鏍稿績绠楁硶鍒嗙被

#### 1. WFC (Wave Function Collapse) - 娉㈠嚱鏁板潔缂?

**鍘熺悊**: 鍩轰簬绾︽潫浼犳挱鐨勭摝鐗囨嫾鎺ョ畻娉曘€?

```
鍩烘湰娴佺▼:
1. 瀹氫箟鐡︾墖闆嗗悎鍙婂叾鐩搁偦瑙勫垯
2. 闅忔満閫夋嫨涓€涓綅缃紝鍧嶇缉涓虹‘瀹氱姸鎬?
3. 浼犳挱绾︽潫鍒伴偦灞?
4. 閲嶅鐩村埌鎵€鏈変綅缃‘瀹?

绀轰緥 - 绠€鍗曞湴鐗?
鐡︾墖绫诲瀷: 澧欍€佸湴鏉裤€侀棬
瑙勫垯:
- 澧欏彧鑳介偦鎺ュ鎴栭棬
- 鍦版澘鍙兘閭绘帴鍦版澘鎴栭棬
- 闂ㄥ繀椤昏繛鎺ュ鍜屽湴鏉?
```

**浼樼偣**:

- 鉁?鐢熸垚缁撴灉濮嬬粓绗﹀悎瑙勫垯
- 鉁?閫傚悎澶嶆潅绾︽潫
- 鉁?鍙互鐢熸垚鏈夋満鎰熺殑鍏冲崱

**缂虹偣**:

- 鉂?鍙兘闄峰叆鏃犺В鐘舵€侊紙闇€瑕佸洖婧級
- 鉂?鎬ц兘杈冩參
- 鉂?瑙勫垯瀹氫箟澶嶆潅

#### 2. BSP (Binary Space Partitioning) - 浜屽弶绌洪棿鍒嗗壊

**鍘熺悊**: 閫掑綊鍒嗗壊绌洪棿锛屽垱寤烘埧闂村拰璧板粖銆?

```
鍩烘湰娴佺▼:
1. 浠庢暣涓尯鍩熷紑濮?
2. 闅忔満閫夋嫨姘村钩鎴栧瀭鐩村垎鍓?
3. 閫掑綊鍒嗗壊瀛愬尯鍩?
4. 鍦ㄥ彾鑺傜偣鍒涘缓鎴块棿
5. 杩炴帴鐩搁偦鎴块棿

绀轰緥:
鈹屸攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?
鈹?    鎴块棿A       鈹?鈫?鍙惰妭鐐?
鈹溾攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?
鈹?鎴块棿B  鈹?鎴块棿C  鈹?鈫?鍙惰妭鐐?銆?
鈹斺攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹粹攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?
   鈫?璧板粖杩炴帴
```

**浼樼偣**:

- 鉁?绠€鍗曟槗瀹炵幇
- 鉁?鐢熸垚閫熷害蹇?
- 鉁?鎴块棿鍒嗗竷鍧囧寑

**缂虹偣**:

- 鉂?鐢熸垚缁撴灉杈冭鏁达紙缂轰箯鏈夋満鎰燂級
- 鉂?璧板粖鍙兘鍐楅暱
- 鉂?涓嶅闅忔満

#### 3. Cellular Automata - 鍏冭優鑷姩鏈?

**鍘熺悊**: 鍩轰簬绠€鍗曡鍒欑殑杩唬婕斿寲銆?

```
缁忓吀瑙勫垯 (4-5瑙勫垯):
- 濡傛灉閭诲眳澧?>= 5: 鍙樻垚澧?
- 濡傛灉閭诲眳澧?<= 4: 鍙樻垚鍦版澘

杩唬杩囩▼:
鍒濆: 闅忔満鍣０ (50% 澧?
  鈻犫枴鈻犫枲鈻?
  鈻♀枲鈻♀枴鈻?
  鈻犫枲鈻犫枴鈻?

杩唬1: 搴旂敤瑙勫垯
  鈻犫枲鈻犫枲鈻?
  鈻犫枲鈻犫枴鈻?
  鈻犫枲鈻犫枲鈻?

杩唬5: 鏀舵暃
  鈻犫枲鈻犫枲鈻?
  鈻犫枴鈻♀枴鈻?
  鈻犫枲鈻犫枲鈻?
  鈫?鐢熸垚娲炵┐鐘剁粨鏋?
```

**浼樼偣**:

- 鉁?鐢熸垚鑷劧鐨勬礊绌?鏈夋満褰㈢姸
- 鉁?瀹炵幇绠€鍗?
- 鉁?鍙傛暟鏄撹皟

**缂虹偣**:

- 鉂?涓嶄繚璇佽繛閫氭€?
- 鉂?闅句互鎺у埗鍏蜂綋褰㈢姸
- 鉂?闇€瑕佸悗澶勭悊锛堣繛閫氭€ф娴嬶級

---

## 馃洜锔?2. 瀹炶返搴旂敤 (Practical Implementation)

### 馃幃 Vampirefall 鍦板浘鐢熸垚妗嗘灦

#### 娣峰悎鐢熸垚绛栫暐

Vampirefall鐨勫闃?鑲夐附鐗规€ч渶瑕?*鎵嬪伐璁捐 + 绋嬪簭鐢熸垚**娣峰悎锛?

```
鈹屸攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?
鈹?绗?灞傦細鎵嬪伐妯℃澘锛堝闃插竷灞€锛?         鈹?
鈹?- 棰勮璺緞鑺傜偣                      鈹?
鈹?- 鍏抽敭濉斾綅鏍囪                      鈹?
鈹溾攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?
鈹?绗?灞傦細绋嬪簭鍙樺寲锛堣倝楦介殢鏈烘€э級        鈹?
鈹?- 鏁屼汉鍒锋柊鐐归殢鏈?                   鈹?
鈹?- 璧勬簮鐐瑰垎甯?                       鈹?
鈹?- 鍦板舰闅滅鐗?                       鈹?
鈹溾攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?
鈹?绗?灞傦細璇嶆潯淇グ锛堣倝楦藉寮猴級          鈹?
鈹?- "杩烽浘鎴樺満"锛堥檷浣庤閲庯級            鈹?
鈹?- "鐙獎閫氶亾"锛堣矾寰勫彉绐勶級            鈹?
鈹斺攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?
```

### 馃梻锔?鏁版嵁缁撴瀯

#### MapTemplate.cs

```csharp
[CreateAssetMenu(fileName = "MapTemplate", menuName = "PCG/Map Template")]
public class MapTemplate : ScriptableObject
{
    [Header("妯℃澘淇℃伅")]
    public string templateName = "妫灄鍦板浘";
    public Vector2Int size = new Vector2Int(50, 50);
    
    [Header("璺緞瀹氫箟")]
    public PathNode[] pathNodes;  // 鏁屼汉琛岃蛋璺緞
    
    [Header("濉斾綅瀹氫箟")]
    public TowerSlot[] towerSlots;  // 鍙缓濉斾綅缃?
    
    [Header("鐢熸垚瑙勫垯")]
    public GenerationRule[] rules;
}

[System.Serializable]
public class PathNode
{
    public Vector2Int position;
    public PathNode[] nextNodes;  // 鏀寔鍒嗘敮璺緞
}

[System.Serializable]
public class TowerSlot
{
    public Vector2Int position;
    public TowerSlotType type;  // Normal, Strategic(鎴樼暐鐐逛綅)
}

[System.Serializable]
public class GenerationRule
{
    public RuleType type;
    public float probability;  // 瑙﹀彂姒傜巼
    public string parameters;  // JSON鍙傛暟
}

public enum RuleType
{
    SpawnObstacle,    // 鐢熸垚闅滅鐗?
    SpawnResource,    // 鐢熸垚璧勬簮鐐?
    ModifyPath,       // 淇敼璺緞
    AddEnemySpawn     // 娣诲姞鍒锋€偣
}
```

#### ProceduralMapGenerator.cs

```csharp
public class ProceduralMapGenerator : MonoBehaviour
{
    public MapTemplate template;
    private int seed;
    
    public GeneratedMap Generate(int seed)
    {
        this.seed = seed;
        Random.InitState(seed);
        
        var map = new GeneratedMap
        {
            size = template.size,
            tiles = new TileType[template.size.x, template.size.y]
        };
        
        // 1. 鍒濆鍖栧熀纭€鍦板舰
        InitializeBaseTerrain(map);
        
        // 2. 鏀剧疆璺緞
        PlacePaths(map, template.pathNodes);
        
        // 3. 鏀剧疆濉斾綅
        PlaceTowerSlots(map, template.towerSlots);
        
        // 4. 搴旂敤鐢熸垚瑙勫垯
        ApplyGenerationRules(map, template.rules);
        
        // 5. 楠岃瘉鍙帺鎬?
        if (!ValidateMap(map))
        {
            Debug.LogWarning($"[PCG] 鍦板浘鐢熸垚澶辫触(绉嶅瓙:{seed})锛岄噸鏂扮敓鎴?);
            return Generate(seed + 1);  // 鎹竴涓瀛?
        }
        
        return map;
    }
    
    private void InitializeBaseTerrain(GeneratedMap map)
    {
        for (int x = 0; x < map.size.x; x++)
        {
            for (int y = 0; y < map.size.y; y++)
            {
                map.tiles[x, y] = TileType.Ground;
            }
        }
    }
    
    private void PlacePaths(GeneratedMap map, PathNode[] nodes)
    {
        foreach (var node in nodes)
        {
            // 浠庤妭鐐瑰埌涓嬩竴涓妭鐐圭粯鍒惰矾寰?
            foreach (var next in node.nextNodes)
            {
                DrawPath(map, node.position, next.position);
            }
        }
    }
    
    private void DrawPath(GeneratedMap map, Vector2Int from, Vector2Int to)
    {
        // A* 鎴?Bresenham 绠楁硶缁樺埗璺緞
        var points = CalculatePathPoints(from, to);
        
        foreach (var point in points)
        {
            if (IsInBounds(map, point))
            {
                map.tiles[point.x, point.y] = TileType.Path;
                
                // 鍔犱竴鐐归殢鏈哄搴?
                if (Random.value < 0.3f)
                {
                    var offset = new Vector2Int(Random.Range(-1, 2), Random.Range(-1, 2));
                    var widePoint = point + offset;
                    if (IsInBounds(map, widePoint))
                    {
                        map.tiles[widePoint.x, widePoint.y] = TileType.Path;
                    }
                }
            }
        }
    }
    
    private bool ValidateMap(GeneratedMap map)
    {
        // 1. 妫€鏌ヨ矾寰勮繛閫氭€?
        if (!IsPathConnected(map))
            return false;
        
        // 2. 妫€鏌ュ浣嶅彲杈炬€?
        if (!AreTowerSlotsValid(map))
            return false;
        
        // 3. 妫€鏌ユ晫浜烘棤娉曞埌杈惧浣?
        if (!IsTowerSafety(map))
            return false;
        
        return true;
    }
    
    private bool IsPathConnected(GeneratedMap map)
    {
        // BFS/DFS 妫€鏌ヤ粠璧风偣鍒扮粓鐐规槸鍚﹁繛閫?
        var start = FindStartPoint(map);
        var end = FindEndPoint(map);
        
        return BFS(map, start, end);
    }
}

public class GeneratedMap
{
    public Vector2Int size;
    public TileType[,] tiles;
    public List<Vector2Int> towerSlots;
    public List<Vector2Int> enemySpawns;
    public int seed;
}

public enum TileType
{
    Ground,
    Path,
    Obstacle,
    TowerSlot,
    Resource
}
```

### 馃帹 璺緞淇濊瘉绠楁硶

**闂**: 绋嬪簭鐢熸垚鍙兘浜х敓涓嶅彲閫氳鐨勮矾寰勩€?

**瑙ｅ喅鏂规**: 璺緞浼樺厛鐢熸垚 + 楠岃瘉 + 淇銆?

```csharp
public class PathGuarantee
{
    public static bool EnsurePathExists(GeneratedMap map, Vector2Int start, Vector2Int end)
    {
        // 1. A* 瀵绘壘璺緞
        var path = AStar.FindPath(map, start, end);
        
        if (path != null)
            return true;  // 璺緞宸插瓨鍦?
        
        // 2. 寮哄埗鎵撻€氳矾寰?
        path = ForceCreatePath(map, start, end);
        
        // 3. 搴旂敤鍒板湴鍥?
        foreach (var point in path)
        {
            map.tiles[point.x, point.y] = TileType.Path;
        }
        
        return true;
    }
    
    private static List<Vector2Int> ForceCreatePath(GeneratedMap map, Vector2Int start, Vector2Int end)
    {
        var path = new List<Vector2Int>();
        var current = start;
        
        while (current != end)
        {
            path.Add(current);
            
            // 绠€鍗曠瓥鐣ワ細姣忔绉诲姩鍒版洿鎺ヨ繎缁堢偣鐨勬柟鍚?
            var toEnd = end - current;
            
            if (Mathf.Abs(toEnd.x) > Mathf.Abs(toEnd.y))
            {
                current += new Vector2Int(toEnd.x > 0 ? 1 : -1, 0);
            }
            else
            {
                current += new Vector2Int(0, toEnd.y > 0 ? 1 : -1);
            }
            
            // 闃叉鏃犻檺寰幆
            if (path.Count > map.size.x * map.size.y)
                break;
        }
        
        path.Add(end);
        return path;
    }
}
```

---

## 馃専 3. 涓氱晫浼樼妗堜緥 (Industry Best Practices)

### 馃幃 妗堜緥 1: **Spelunky - 妯℃澘鎷兼帴澶у笀**

#### 鏍稿績鏈哄埗

Spelunky浣跨敤**棰勫埗鎴块棿妯℃澘 + 鏅鸿兘鎷兼帴**鐢熸垚鍏冲崱銆?

**鐢熸垚娴佺▼**:

```
1. 鐢熸垚4x4鎴块棿缃戞牸
   [A][B][C][D]
   [E][F][G][H]
   [I][J][K][L]
   [M][N][O][P]
2. 鏍囪鍏抽敭鎴块棿
   鍏ュ彛: A
   鍑哄彛: P
   鍟嗗簵: 闅忔満1涓?
   鏆楀: 闅忔満1-2涓?
3. 纭繚杩為€氭€?
   A 鈫?... 鈫?P 蹇呴』鍙揪
   浣跨敤BFS鐢熸垚涓昏矾寰?
4. 濉厖鎴块棿妯℃澘
   浠庢ā鏉垮簱涓殢鏈洪€夋嫨绗﹀悎瑙勫垯鐨勬埧闂?
5. 娣诲姞缁嗚妭

   - 闄烽槺鏀剧疆
   - 鏁屼汉鍒锋柊
   - 瀹濈鍒嗗竷
```

**妯℃澘搴撹璁?*:

```
鎴块棿鏍囩:
- 鍏ュ彛鎴?(ENT)
- 鍑哄彛鎴?(EXIT)
- 鏅€氭埧 (NORMAL)
- 闄烽槺鎴?(TRAP)
- 瀹濊棌鎴?(TREASURE)

杩炴帴瑙勫垯:
- 姣忎釜鎴块棿4涓棬锛堜笂涓嬪乏鍙筹級
- 闂ㄥ繀椤诲榻?
- 姣忎釜闂ㄦ湁"蹇呴』"鎴?鍙€?灞炴€?
```

**Vampirefall 鍊熼壌**:

- 棰勫埗濉旈槻妯℃澘锛堜笉鍚屽湴褰級
- 妯℃澘搴撳垎绫伙紙绠€鍗?鍥伴毦/Boss锛?
- 涓昏矾寰勪繚璇佺畻娉?

---

### 馃幃 妗堜緥 2: **The Binding of Isaac - 鎴块棿搴撶郴缁?*

#### 鏍稿績鏈哄埗

Isaac浣跨敤**澶ч噺鎵嬪伐璁捐鎴块棿 + 闅忔満缁勫悎**銆?

**鎴块棿搴撹妯?*:

```
鏅€氭埧: 500+ 涓?
Boss鎴? 50+ 涓?
鍟嗗簵: 20+ 涓?
瀹濊棌鎴? 30+ 涓?
绉樺瘑鎴? 20+ 涓?

鎬昏: 600+ 涓墜宸ユ埧闂?
```

**鎴块棿閫夋嫨绠楁硶**:

```csharp
Room SelectRoom(RoomType type, int difficulty, HashSet<int> usedRooms)
{
    // 1. 绛涢€夊€欓€夋埧闂?
    var candidates = roomDatabase
        .Where(r => r.type == type)
        .Where(r => r.difficulty <= difficulty)
        .Where(r => !usedRooms.Contains(r.id))
        .ToList();
    
    // 2. 鏉冮噸闅忔満閫夋嫨
    var weights = candidates.Select(r => r.weight).ToArray();
    var selected = WeightedRandom.Select(candidates, weights);
    
    // 3. 鏍囪宸蹭娇鐢紙閬垮厤閲嶅锛?
    usedRooms.Add(selected.id);
    
    return selected;
}
```

**璁捐鍝插**:
> "绋嬪簭鐢熸垚涓嶆槸涓轰簡鍑忓皯宸ヤ綔閲忥紝鑰屾槸涓轰簡澧炲姞閲嶇帺浠峰€笺€?

**Vampirefall 鍊熼壌**:

- 寤虹珛濉旈槻鍦烘櫙搴擄紙100+锛?
- 鍩轰簬闅惧害鍒嗙骇
- 閬垮厤鍚屼竴灞€閲嶅

---

### 馃幃 妗堜緥 3: **Enter the Gungeon - 绋嬪簭鍖栧湴鐗?*

#### 鏍稿績鏈哄埗

Gungeon缁撳悎浜?*BSP鍒嗗壊 + 鎵嬪伐鎴块棿 + 鐗规畩瑙勫垯**銆?

**鐢熸垚绠楁硶**:

```
1. BSP鐢熸垚鎴块棿甯冨眬
   鈹?鍒嗗壊娆℃暟: 5-7娆?
   鈹?鎴块棿鏁伴噺: 15-25涓?
   鈹?鎴块棿澶у皬: 10x10 鍒?30x30
2. 鍒嗛厤鎴块棿绫诲瀷
   鈹?1涓狟oss鎴匡紙蹇呴』鍦ㄨ竟缂橈級
   鈹?1涓晢搴?
   鈹?1-2涓疂钘忔埧
   鈹?2-3涓寫鎴樻埧
   鈹?鍏朵綑涓烘櫘閫氭垬鏂楁埧
3. 鐢熸垚璧板粖
   鈹?鏈€鐭矾寰勮繛鎺?
   鈹?娣诲姞鐜矾锛?0%姒傜巼锛?
   鈹?绉樺瘑鎴块棿杩炴帴锛堥渶瑕佺偢澧欙級
4. 濉厖鍐呭
   鈹?鎴块棿浠庢ā鏉垮簱閫夋嫨
   鈹?鏁屼汉鏍规嵁闅惧害鏇茬嚎鐢熸垚
   鈹?鐗╁搧鏍规嵁鎺夎惤琛ㄦ斁缃?
```

**鐗规畩瑙勫垯**:

```
- Boss鎴垮繀椤讳粠鍏ュ彛璧版渶杩滆矾寰?
- 鍟嗗簵蹇呴』鍦ㄤ富璺緞涓?
- 瀹濊棌鎴垮彲鑳藉湪鍒嗘敮
- 绉樺瘑鎴块偦鎺ヨ嚦灏?涓埧闂?
```

**Vampirefall 鍊熼壌**:

- BSP鐢ㄤ簬澶у尯鍩熷垝鍒?
- 鍏抽敭鎴块棿锛圔oss/鍟嗗簵锛変綅缃鍒?
- 绉樺瘑鍖哄煙璁捐

---

## 馃敆 4. 鍙傝€冭祫鏂?(References)

### 馃搫 鐞嗚

1. **Procedural Content Generation in Games**  
    浣滆€? Noor Shaker, Julian Togelius, Mark J. Nelson  
    [涔︾睄閾炬帴](http://pcgbook.com/)

2. **Wave Function Collapse Algorithm**  
    *Maxim Gumin*  
    [GitHub](https://github.com/mxgmn/WaveFunctionCollapse)

### 馃摵 GDC

1. **[GDC 2017] Spelunky Level Generation**  
    婕旇鑰? Derek Yu  
    [YouTube](https://www.youtube.com/watch?v=Uqk5Zf0tw3o)

2. **[GDC 2015] Diablo's Dungeon Generation**  
    婕旇鑰? Mike Barlow (Blizzard)  
    [GDC Vault](https://www.gdcvault.com/play/diablo_dungeon)

### 馃寪 鍗氬

1. **The Binding of Isaac Room Design**  
    [Edmund McMillen Blog](https://edmundm.com/post/isaac-room-design)

2. **Procedural Map Generation Techniques**  
    [RogueBasin Wiki](http://www.roguebasin.com/index.php?title=Articles)

---

## 馃幆 闄勫綍锛歏ampirefall PCG瀹炴柦妫€鏌ユ竻鍗?

### 鉁?闃舵1: 妯℃澘绯荤粺锛堝繀椤伙級
- [ ] 鍒涘缓10+濉旈槻鍦板浘妯℃澘
- [ ] 瀹氫箟璺緞鑺傜偣鍜屽浣?
- [ ] 寤虹珛妯℃澘搴撶鐞嗗櫒

### 鉁?闃舵2: 鐢熸垚绠楁硶锛堝繀椤伙級
- [ ] 瀹炵幇BSP鎴栨埧闂存嫾鎺?
- [ ] 璺緞淇濊瘉绠楁硶
- [ ] 杩為€氭€ч獙璇?

### 鉁?闃舵3: 闅忔満鎬э紙鎺ㄨ崘锛?
- [ ] 闅滅鐗╅殢鏈烘斁缃?
- [ ] 璧勬簮鐐瑰垎甯?
- [ ] 鏁屼汉鍒锋柊鐐瑰彉鍖?

### 鉁?闃舵4: 楠岃瘉绯荤粺锛堝繀椤伙級
- [ ] 鍙帺鎬ф娴?
- [ ] 闅惧害璇勪及
- [ ] 绉嶅瓙璁板綍锛堢敤浜巄ug澶嶇幇锛?

### 鉁?闃舵5: 璋冭瘯宸ュ叿锛堟帹鑽愶級
- [ ] 鍙鍖栫敓鎴愯繃绋?
- [ ] 绉嶅瓙杈撳叆鍔熻兘
- [ ] 鎬ц兘鐩戞帶

---

**鏈€鍚庢洿鏂?*: 2025-12-04  
**缁存姢鑰?*: Vampirefall 璁捐鍥㈤槦




---


{/* 鏉ユ簮: Dev_Guides\Technical_Implementation\Procedural_Generation_WFC.md */}

## 娉㈠嚱鏁板潔缂?(WFC) 鐢熸垚 (Wave Function Collapse)

> [!NOTE]
> **鏍稿績鎬濇兂**: WFC 鏄竴绉嶅熀浜?*绾︽潫 (Constraint)** 鐨勭敓鎴愮畻娉曘€傚畠涓嶆槸鍛婅瘔璁＄畻鏈衡€滄€庝箞鐢烩€濓紝鑰屾槸鍛婅瘔瀹冣€滀粈涔堜笉鑳界敾鈥濄€?

鍦?Roguelike 鍦扮墷鐢熸垚涓紝WFC 鑳芥瘮浼犵粺鐨勨€滄埧闂?璧板粖鈥濈畻娉曠敓鎴愭洿鑷劧銆佹洿鏈夋満鐨勭粨鏋勩€?

---

## 1. 鏍稿績姒傚康 (Core Concepts)

### 1.1 鍙犲姞鎬?(Superposition)
鍦ㄧ畻娉曞紑濮嬫椂锛屽湴鍥句笂鐨勬瘡涓€涓牸瀛愰兘鍚屾椂澶勪簬鈥滄墍鏈夊彲鑳界姸鎬佲€濈殑鍙犲姞涓€?

*   渚嬪锛氫竴涓牸瀛愭棦鍙兘鏄€滆崏鍦扳€濓紝涔熷彲鑳芥槸鈥滃澹佲€濓紝涔熷彲鑳芥槸鈥滄按鈥濄€?

### 1.2 鐔?(Entropy)
鐔垫槸琛￠噺涓嶇‘瀹氭€х殑鎸囨爣銆?

*   **楂樼喌**: 璇ユ牸瀛愭湁寰堝绉嶅彲鑳芥€?(渚嬪锛氳崏鍦?澧?姘?璺?銆?
*   **浣庣喌**: 璇ユ牸瀛愬彧鏈夊緢灏戠殑鍙兘鎬?(渚嬪锛氬彧鑳芥槸澧?銆?
*   **鐔典负0**: 璇ユ牸瀛愮姸鎬佸凡纭畾 (鍧嶇缉)銆?

### 1.3 鍧嶇缉 (Collapse)
瑙傛祴瀵艰嚧鍧嶇缉銆傛垜浠汉涓哄湴锛堟垨闅忔満鍦帮級閫夋嫨涓€涓牸瀛愶紝灏嗗叾鐘舵€佸浐瀹氫笅鏉ャ€?

### 1.4 绾︽潫浼犳挱 (Constraint Propagation)
涓€鏃︿竴涓牸瀛愮‘瀹氫簡锛堜緥濡傚彉鎴愪簡鈥滄按鈥濓級锛屽畠鐨勯偦灞呭氨涓嶅彲鑳芥槸鈥滃博娴嗏€濓紙鍋囪姘寸伀涓嶅锛夈€傝繖绉嶇害鏉熶細鍍忔尝绾逛竴鏍峰悜鍥涘懆浼犳挱锛屽噺灏戦偦灞呯殑鐔点€?

---

## 2. 绠楁硶娴佺▼ (Algorithm Flow)

1.  **鍒濆鍖?*: 灏嗙綉鏍间腑鎵€鏈夊崟鍏冩牸璁句负鍙犲姞鎬?(鍖呭惈鎵€鏈夊彲鑳界殑 Tile)銆?
2.  **瀵绘壘鏈€灏忕喌**: 鎵惧埌褰撳墠缃戞牸涓喌鏈€灏忥紙鍙兘鎬ф渶灏戯級浣嗗皻鏈潔缂╃殑鍗曞厓鏍笺€?

    *   濡傛灉鏈夊涓渶灏忕喌锛岄殢鏈洪€変竴涓€?
3.  **瑙傛祴/鍧嶇缉**: 鏍规嵁鏉冮噸闅忔満閫夋嫨璇ュ崟鍏冩牸鐨勪竴涓姸鎬侊紝灏嗗叾鍥哄畾銆?

4.  **浼犳挱**: 

    *   鏇存柊璇ュ崟鍏冩牸鐨勬墍鏈夐偦灞呫€?
    *   濡傛灉閭诲眳鐨勫彲鑳芥€у噺灏戜簡锛岀户缁洿鏂伴偦灞呯殑閭诲眳 (閫掑綊鎴栧爢鏍?銆?
    *   濡傛灉鍦ㄤ紶鎾繃绋嬩腑鏌愪釜鍗曞厓鏍肩殑鍙兘鎬у彉涓?0 (鏃犺В)锛屽垯鐢熸垚澶辫触锛岄渶瑕佸洖婧垨閲嶈瘯銆?
5.  **寰幆**: 閲嶅姝ラ 2-4锛岀洿鍒版墍鏈夊崟鍏冩牸閮藉潔缂╁畬鎴愩€?

---

## 3. 瀹炵幇鎸囧崡 (Implementation Guide)

### 3.1 瀹氫箟 Tile 涓?Socket (鎺ュ彛)
涓轰簡鍒ゆ柇涓や釜 Tile 鏄惁鑳界浉閭伙紝鎴戜滑闇€瑕佸畾涔夊畠浠殑杈圭紭鎺ュ彛 (Socket)銆?

鍋囪鎴戜滑鏈?4 涓柟鍚戯細涓娿€佷笅銆佸乏銆佸彸銆?

*   **鑽夊湴 Tile**: `[Grass, Grass, Grass, Grass]`
*   **娴峰哺 Tile**: `[Water, Grass, Coast, Coast]` (鍋囪)

**瑙勫垯**: Tile A 鐨勨€滃彸鈥濇帴鍙ｅ繀椤讳笌 Tile B 鐨勨€滃乏鈥濇帴鍙ｅ尮閰?(鍙互鏄浉鍚?ID锛屼篃鍙互鏄畾涔夌殑瀵圭О ID)銆?

### 3.2 鏃嬭浆涓庨暅鍍?
涓轰簡鑺傜渷缇庢湳璧勬簮锛屾垜浠彲浠ヨ嚜鍔ㄧ敓鎴愭棆杞彉浣撱€?

*   涓€涓笉瀵圭О鐨?Tile 鍙互鐢熸垚 4 涓棆杞増鏈€?
*   鎺ュ彛鏁版嵁涔熼渶瑕侀殢涔嬫棆杞€?

### 3.3 鍥炴函涓庨噸璇?(Backtracking)
WFC 鍙兘浼氶亣鍒扳€滄鑳″悓鈥?(Contradiction)銆?

*   **绠€鍗曠瓥鐣?*: 閬囧埌鍐茬獊鐩存帴娓呯┖鏁翠釜鍦板浘閲嶆潵 (瀵逛簬灏忓湴鍥鹃潪甯稿揩)銆?
*   **楂樼骇绛栫暐**: 璁板綍姣忎竴姝ョ殑鐘舵€侊紝閬囧埌鍐茬獊鍥為€€鍒颁笂涓€姝ワ紝骞舵爣璁板鑷村啿绐佺殑鍒嗘敮涓轰笉鍙銆?

### 3.4 鎬ц兘浼樺寲
*   **鏈€灏忓爢 (Min-Heap)**: 鐢ㄦ渶灏忓爢缁存姢鎵€鏈夋牸瀛愮殑鐔碉紝浠ヤ究 O(1) 鍙栧嚭鏈€灏忕喌鏍煎瓙銆?
*   **鑴忔爣璁?(Dirty Flags)**: 浼犳挱鏃跺彧澶勭悊鍙楀奖鍝嶇殑鍖哄煙銆?

---

## 4. Unity 浠ｇ爜鐗囨 (浼唬鐮?

```csharp
public class WFCGenerator : MonoBehaviour {
    struct Cell {
        public bool Collapsed;
        public List<Tile> PossibleTiles;
        public int Entropy => PossibleTiles.Count;
    }

    void RunWFC() {
        // 1. Init
        InitializeGrid();

        while (IsAnyCellUncollapsed()) {
            // 2. Find Min Entropy
            Vector2Int coords = GetMinEntropyCell();
            
            // 3. Collapse
            CollapseCell(coords);
            
            // 4. Propagate
            PropagateConstraints(coords);
        }
        
        DrawMap();
    }
    
    void PropagateConstraints(Vector2Int startNode) {
        Stack<Vector2Int> stack = new Stack<Vector2Int>();
        stack.Push(startNode);
        
        while (stack.Count > 0) {
            var current = stack.Pop();
            foreach (var neighbor in GetNeighbors(current)) {
                if (Constrain(current, neighbor)) {
                    stack.Push(neighbor); // 濡傛灉閭诲眳琚慨鏀逛簡锛岀户缁紶鎾?
                }
            }
        }
    }
}
```

---

## 5. 涓氱晫妗堜緥 (Industry Cases)

### Townscaper
*   **鐗圭偣**: 鏋佸叾娴佺晠鐨勫疄鏃?WFC銆?
*   **鏈哄埗**: 鐜╁鐐瑰嚮鍙槸鈥滆娴嬧€濅簡涓€涓牸瀛愶紝绠楁硶鑷姩璁＄畻鍛ㄥ洿鏍煎瓙鐨勬渶浼樿В锛堝眿椤躲€佸湴鍩恒€佹ゼ姊級銆?

### Bad North (鍖楁柟缁濆)
*   **鐗圭偣**: 寰瀷宀涘笨鐢熸垚銆?
*   **搴旂敤**: 淇濊瘉宀涘笨杈圭紭鎬绘槸骞虫粦鐨勬捣宀哥嚎锛屼笖楂樹綆宸湁姊瓙杩炴帴銆?

### Caves of Qud
*   **鐗圭偣**: 鏋佸叾澶嶆潅鐨勬枃鏈弿杩扮敓鎴愩€?
*   **搴旂敤**: 鍒╃敤 WFC 鐢熸垚鍘嗗彶浼犺鍜屽湴璨屾弿杩般€?

---

## 6. 鎵╁睍闃呰
*   [Maxim Gumin's Original WFC Repo](https://github.com/mxgmn/WaveFunctionCollapse)
*   [Oskar St氓lberg (Townscaper) Talks](https://www.youtube.com/watch?v=0bcZb-SsnrA)




