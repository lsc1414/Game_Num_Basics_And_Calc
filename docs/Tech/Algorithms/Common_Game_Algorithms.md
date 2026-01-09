---
title: "娓告垙甯哥敤绠楁硶娣卞害鐮旂┒"
sidebarTitle: "馃鈥嶁檪锔?甯哥敤绠楁硶涓庡疄璺?
description: "Vampirefall 椤圭洰涓娇鐢ㄧ殑鏍稿績绠楁硶鐞嗚涓?Unity 宸ョ▼瀹炶返鎸囧崡锛屾兜鐩栧璺€佺┖闂寸鐞嗐€侀殢鏈虹郴缁熷強鎬ц兘浼樺寲銆?
icon: "function"
---

# 馃鈥嶁檪锔?娓告垙甯哥敤绠楁硶娣卞害鐮旂┒ (Common Game Algorithms)

鏈枃妗ｆ棬鍦ㄤ綔涓?**Vampirefall** 椤圭洰鐨勬妧鏈畻娉曟墜鍐屻€傛垜浠笉鍙綏鍒楃悊璁猴紝鏇存敞閲?*鐞嗚涓庡伐绋嬪疄璺电殑缁撳悎**锛岀壒鍒槸閽堝 Unity DOTS/Jobs System 鐨勪紭鍖栧疄鐜般€?

---

## 馃椇锔?1. 瀵昏矾涓庡鑸?(Pathfinding & Navigation)

瀵昏矾鏄闃?TD)鍜?Roguelike 娓告垙鐨勬牳蹇冦€傛垜浠渶瑕佸鐞嗘垚鍗冧笂涓囦釜鍗曚綅鐨勭Щ鍔紝鍚屾椂淇濊瘉鎬ц兘銆?

### 1.1 鐞嗚鍩虹锛欰\* 涓?Dijkstra

> [!NOTE] > **A\* (A-Star)** 鏄湪闈欐€佸湴鍥句腑瀵绘壘鍗曚綋鏈€浼樿矾寰勭殑鏍囧噯瑙ｆ硶銆?

- **鍏紡**: $f(n) = g(n) + h(n)$
  - $g(n)$: 浠庤捣鐐瑰埌褰撳墠鑺傜偣鐨勫疄闄呬唬浠枫€?
  - $h(n)$: 鍚彂鍑芥暟(Heuristic)锛岄浼颁粠褰撳墠鑺傜偣鍒扮粓鐐圭殑浠ｄ环锛堥€氬父鐢ㄦ浖鍝堥】璺濈鎴栨鍑犻噷寰楄窛绂伙級銆?
- **閫傜敤鍦烘櫙**: 鐜╁瀵昏矾銆佺簿鑻辨€璺紙鏁伴噺灏戯紝绮惧害瑕佹眰楂橈級銆?

### 1.2 瀹炶返锛氭祦鍦哄璺?(Flow Field)

鍦?Vampirefall 涓紝鎴戜滑闇€瑕佸鐞嗘捣閲忔€墿锛圫warm锛夋秾鍚戝悓涓€涓洰鏍囷紙鍩哄湴锛夈€傚 500 涓€墿杩愯 500 娆?A\* 鏄瀬鍏舵氮璐圭殑銆?

**鏍稿績鎬濇兂**:
涓嶈绠?鎬墿鍒扮粓鐐?鐨勮矾寰勶紝鑰屾槸璁＄畻"鍦板浘涓婃瘡涓偣鍒扮粓鐐?鐨勬柟鍚戙€傛墍鏈夋€墿鍏变韩鍚屼竴寮犳祦鍦哄浘銆?

**瀹炵幇姝ラ**:

1.  **鐢熸垚鐑姏鍥?(Integration Field)**: 浣跨敤 Dijkstra 绠楁硶锛屼粠缁堢偣鎵╂暎锛岃绠楀叏鍥炬瘡涓牸瀛愬埌缁堢偣鐨勬鏁帮紙浠ｄ环锛夈€?
    - 缁堢偣 = 0
    - 闅滅鐗?= $\infty$
    - 鐩搁偦鏍?= +1 (鎴栧湴褰㈡潈閲?
2.  **鐢熸垚娴佸満 (Vector Field)**: 閬嶅巻姣忎釜鏍煎瓙锛屾寚鍚戝叾閭诲眳涓暟鍊兼渶灏忕殑閭ｄ釜鏍煎瓙銆?

**Unity 瀹炶返 (Job System)**:

```csharp
[BurstCompile]
public struct CalculateFlowFieldJob : IJob
{
    public int2 TargetPos;
    public int2 GridSize;
    [ReadOnly] public NativeArray<bool> Obstacles;
    public NativeArray<float2> FlowMap; // 杈撳嚭缁撴灉

    public void Execute()
    {
        // 1. Dijkstra 骞垮害浼樺厛鎼滅储璁＄畻璺濈鍦?
        // ... (鐪佺暐闃熷垪瀹炵幇缁嗚妭)

        // 2. 鏍规嵁璺濈鍦鸿绠楀悜閲?
        for (int x = 0; x < GridSize.x; x++)
        {
            for (int y = 0; y < GridSize.y; y++)
            {
                int index = x + y * GridSize.x;
                if (Obstacles[index])
                {
                    FlowMap[index] = float2.zero;
                    continue;
                }

                // 瀵绘壘璺濈鏈€灏忕殑閭诲眳
                FlowMap[index] = CalculateGradient(x, y);
            }
        }
    }
}
```

### 1.3 閬块殰涓庣兢鑱?(Steering Behaviors)

瀵昏矾瑙ｅ喅浜?鎬庝箞鍘?鐨勯棶棰橈紝**Steering Behaviors** 瑙ｅ喅"鎬庝箞鍔?鐨勯棶棰橈紝閬垮厤鎬墿閲嶅彔銆?

- **Separation (鍒嗙)**: 绂诲お杩戠殑閭诲眳杩滀竴鐐广€?
- **Alignment (瀵归綈)**: 鍜岄偦灞呬繚鎸佺浉鍚屾柟鍚戯紙鍙€夛級銆?
- **Cohesion (鍑濊仛)**: 寰€閭诲眳鐨勪腑蹇冮潬锛堝彲閫夛級銆?

> [!TIP]
> 鍦ㄥ惛琛€楝煎垢瀛樿€呯被娓告垙涓紝鍙渶瑕佸疄鐜?*寮虹‖鐨勫垎绂?(Hard Separation)**銆傚鏋滀袱涓€墿纰版挒锛岀洿鎺ユ帹寮€锛屾€ц兘鏈€楂樹笖瑙嗚鏁堟灉瓒冲銆?

---

## 馃摝 2. 绌洪棿绠＄悊 (Spatial Partitioning)

褰撳睆骞曚笂鏈?1000 涓瓙寮瑰拰 500 涓€墿鏃讹紝鏆村姏妫€娴嬬鎾?($O(N^2)$) 浼氬鑷村崱姝汇€傛垜浠渶瑕佺┖闂村垝鍒嗙畻娉曞皢澶嶆潅搴﹂檷鑷?$O(N)$ 鎴?$O(N \log N)$銆?

### 2.1 鐞嗚锛氱┖闂村搱甯?(Spatial Hashing)

灏?2D 绌洪棿鍒掑垎涓哄浐瀹氱殑缃戞牸锛圙rid锛夛紝姣忎釜缃戞牸瀛樺偍鍏朵腑鐨勭墿浣撳垪琛ㄣ€?

- **浼樼偣**: 鎻掑叆鍜屾煡璇㈡帴杩?$O(1)$锛屽疄鐜版瀬鍏剁畝鍗曘€?
- **缂虹偣**: 缃戞牸澶у皬閫夊彇鏁忔劅锛岃法缃戞牸鐗╀綋澶勭悊绋嶇箒鐞愩€?
- **閫傜敤**: 鍧囧寑鍒嗗竷鐨勫ぇ閲忓姩鎬佺墿浣擄紙濡傚脊骞曘€佹€墿缇わ級銆?

### 2.2 鐞嗚锛氬洓鍙夋爲 (Quadtree)

閫掑綊鍦板皢绌洪棿鍒掑垎涓哄洓涓薄闄愶紝鐩村埌鍖哄煙鍐呯墿浣撴暟閲忓皯浜庨槇鍊笺€?

- **浼樼偣**: 閫傚簲闈炲潎鍖€鍒嗗竷锛堢┖鏃峰尯鍩熶笉鍗犵敤鍐呭瓨锛夈€?
- **缂虹偣**: 鍔ㄦ€佺墿浣撻绻佺Щ鍔ㄥ鑷存爲缁撴瀯閲嶅缓寮€閿€澶с€?
- **閫傜敤**: 闈欐€佺墿浣撶鐞嗭紙寤虹瓚鐗┿€佸湴褰級锛屾垨鐗╀綋绉诲姩涓嶉绻佺殑鍦烘櫙銆?

### 2.3 Vampirefall 瀹炶返锛欶lat Grid 浼樺寲

瀵逛簬楂橀鍙樺姩鐨?ECS 鏋舵瀯锛屽彲浠ヤ娇鐢?*鎵佸钩鍖栨暟缁勯摼琛?*瀹炵幇绌洪棿鍝堝笇銆?

```csharp
// 姒傚康浼唬鐮?
public struct SpatialMap
{
    // 鍗曞厓鏍煎ぇ灏?(渚嬪 2.0f)
    public float CellSize;
    // 杩欓噷鐨?Key 鏄?gridX + gridY * width
    // Value 鏄涓牸瀛愰噷绗竴涓?Entity 鐨勭储寮?
    public NativeMultiHashMap<int, Entity> Map;

    public void Add(Entity entity, float2 pos)
    {
        int2 cell = (int2)math.floor(pos / CellSize);
        int key = GetHash(cell);
        Map.Add(key, entity);
    }

    // 鏌ヨ闄勮繎鐨勫疄浣?
    public void Query(float2 pos, float radius, NativeList<Entity> result)
    {
        // 璁＄畻瑕嗙洊鐨勭綉鏍艰寖鍥?(minCell 鍒?maxCell)
        // 閬嶅巻杩欎簺缃戞牸涓殑鎵€鏈?Key
    }
}
```

---

## 馃幉 3. 闅忔満涓庢鐜?(RNG & Probability)

### 3.1 鐞嗚锛氱湡闅忔満 vs 浼殢鏈?(PRNG)

- **Input Randomness**: 鍦ㄥ仛鍐冲畾鍓嶉殢鏈猴紙濡傦細鍦板浘鐢熸垚锛夈€?
- **Output Randomness**: 鍦ㄥ仛鍐冲畾鍚庨殢鏈猴紙濡傦細鏀诲嚮鍛戒腑鐜囷級銆?*Roguelike 搴斿敖閲忛伩鍏嶈繖绉嶄綋楠岃緝宸殑闅忔満锛屾垨鑰呯敤"淇濆簳"鏈哄埗淇グ銆?*

### 3.2 瀹炶返锛氬姞鏉冮殢鏈?(Weighted Random)

鐢ㄤ簬 Loot Table锛堟帀钀借〃锛夈€?

**绠楁硶**:

1. 璁＄畻鎬绘潈閲?(Total Weight)銆?
2. 鐢熸垚 0 鍒?Total Weight 涔嬮棿鐨勯殢鏈烘暟 `r`銆?
3. 閬嶅巻鍒楄〃锛宍r -= 褰撳墠椤规潈閲峘銆?
4. 褰?`r \<= 0` 鏃讹紝閫変腑褰撳墠椤广€?

**浼樺寲 (Alias Method)**:
濡傛灉鏈夊ぇ閲忎笖涓嶅彉鐨勬潈閲嶈〃锛岄澶勭悊鎴?Alias Table 鍙皢鎶藉彇澶嶆潅搴﹂檷涓?$O(1)$銆備絾瀵逛簬涓€鑸父鎴忥紝鏅€氱殑 $O(N)$ 绾挎€ф壂鎻忚冻澶熴€?

```csharp
public static T GetWeightedRandom<T>(List<T> items, System.Func<T, float> weightSelector)
{
    float totalWeight = 0;
    foreach(var item in items) totalWeight += weightSelector(item);

    float r = UnityEngine.Random.Range(0, totalWeight);
    foreach(var item in items)
    {
        float w = weightSelector(item);
        if (r <= w) return item;
        r -= w;
    }
    return default;
}
```

### 3.3 瀹炶返锛氭礂鐗岀畻娉?(Fisher-Yates Shuffle)

鐢ㄤ簬鎶藉崱鎴?淇勭綏鏂柟鍧楀紡"鐨勬帀钀斤紙淇濊瘉涓€杞唴涓嶉噸澶嶏級銆?

```csharp
public static void Shuffle<T>(IList<T> list)
{
    int n = list.Count;
    while (n > 1)
    {
        n--;
        int k = UnityEngine.Random.Range(0, n + 1);
        (list[k], list[n]) = (list[n], list[k]); // Swap
    }
}
```

---

## 馃搱 4. 鏁板€兼彃鍊间笌骞虫粦 (Math & Interpolation)

### 4.1 绾挎€т笌闈炵嚎鎬ф彃鍊?

- **Lerp (Linear)**: $a + (b - a) * t$銆傜畝鍗曪紝鐢变簬涓斾粎鐢ㄤ簬浣嶇疆鐩磋繛銆?
- **Slerp (Spherical)**: 寮у舰鎻掑€硷紝鐢ㄤ簬**鏃嬭浆**锛屼繚璇佽閫熷害鎭掑畾銆?
- **SmoothDamp**: 绫讳技寮圭哀闃诲凹锛岀敤浜庢憚鍍忔満璺熼殢鎴?UI 鍔ㄦ晥锛屾瘮 Lerp 鏇磋嚜鐒讹紙Lerp 浼氬湪鎺ヨ繎缁堢偣鏃舵棤闄愬彉鎱級銆?

### 4.2 缂撳姩鍑芥暟 (Easing Functions)

UI 鍔ㄦ晥鐨勭伒榄傘€備笉瑕佸彧鐢ㄧ嚎鎬у彉鍖栥€?
鎺ㄨ崘浣跨敤鍏紡搴擄紙濡?$t^2$, $t^3$, $1-(1-t)^2$ 绛夛級銆?

---

## 馃殌 5. 鎬ц兘浼樺寲妯″紡 (Optimization Patterns)

### 5.1 瀵硅薄姹?(Object Pooling)

**鐞嗚**:
鍐呭瓨鍒嗛厤 (Allocation) 鍜屽瀮鍦惧洖鏀?(GC) 鏄?Unity 绉诲姩绔崱椤跨殑涓诲洜銆傚璞℃睜閫氳繃澶嶇敤瀵硅薄閬垮厤棰戠箒鐨?`Instantiate` 鍜?`Destroy`銆?

**Vampirefall 瑙勮寖**:

- 鎵€鏈夌壒鏁?(VFX)銆佷激瀹虫暟瀛?(Popups)銆佸瓙寮?(Projectiles) **蹇呴』**浣跨敤瀵硅薄姹犮€?
- 鍙湁鍏冲崱鍒囨崲鏃舵墠鍏佽澶ц妯￠攢姣併€?

### 5.2 鑴忔爣璁版ā寮?(Dirty Flag)

**鐞嗚**:
閬垮厤姣忎竴甯ч兘閲嶆柊璁＄畻澶嶆潅鏁版嵁銆傚彧鍦ㄦ暟鎹彂鐢熷彉鍖栨椂鏍囪涓?`isDirty = true`锛屽湪鑾峰彇鏁版嵁鏃跺鏋滃彂鐜拌剰鏍囪鎵嶉噸鏂拌绠楋紝鍚﹀垯杩斿洖缂撳瓨鍊笺€?

**搴旂敤**:

- **UI**: 鍙湁褰撻噾甯佸彉鍖栨椂鎵嶆洿鏂?Text 缁勪欢銆?
- **灞炴€?*: 鍙湁褰撹澶囧彉鍔ㄦ椂鎵嶉噸鏂拌绠?`FinalAttack = Base + Buffs`銆?

```csharp
public class StatSystem
{
    private float _cacheValue;
    private bool _isDirty = true;

    public void AddBuff() { _isDirty = true; }

    public float Helpers
    {
        get
        {
            if (_isDirty) Recalculate();
            return _cacheValue;
        }
    }
}
```

---

## 馃敆 鍙傝€冭祫鏂?

- 馃搫 **Game Programming Patterns**: 蹇呰缁忓吀銆?
- 馃寪 **Red Blob Games**: 鍑犱綍涓庡璺畻娉曠殑瀹濆簱銆?
- 馃摵 **GDC: "I Shot You First"**: 瀹堟湜鍏堥攱缃戠粶鍚屾涓庢彃鍊肩畻娉曘€?

