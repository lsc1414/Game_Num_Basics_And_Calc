---
sidebarTitle: "娓告垙寮€鍙戝伐鍏烽摼鎸囧崡锛氬姞閫熻凯浠ｇ殑绉樺瘑姝﹀櫒"
---

# 馃洜锔?娓告垙寮€鍙戝伐鍏烽摼鎸囧崡锛氬姞閫熻凯浠ｇ殑绉樺瘑姝﹀櫒

## 馃摎 1. 鐞嗚鍩虹 (Theoretical Basis)

### 1.1 鑷姩鍖栫殑閲戝瓧濉?(The Automation Pyramid)

- **鎵嬪姩鎿嶄綔 (Manual)**: 鐏垫椿鎬ч珮锛屼絾閲嶅鎴愭湰楂橈紝鏄撳嚭閿欍€傞€傜敤浜庡師鍨嬫湡銆?
- **鑴氭湰杈呭姪 (Scripting)**: 鎵瑰鐞嗘枃浠躲€佺畝鍗曠殑缂栬緫鍣ㄨ彍鍗曘€傝В鍐冲崟鐐归噸澶嶉棶棰樸€?
- **绠＄嚎鍖?(Pipeline)**: 澶氫釜宸ュ叿涓茶仈锛屾暟鎹嚜鍔ㄦ祦杞€備緥濡傦細缇庢湳鎻愪氦 -> 鑷姩瀵煎叆 -> 鑷姩鍘嬬缉 -> 鑷姩鐢熸垚棰勫埗浣撱€?
- **鏅鸿兘鍖?(Intelligence)**: AI 杈呭姪鐢熸垚銆佽嚜鍔ㄥ寲鍥炲綊娴嬭瘯銆?

### 1.2 DevOps 鍦ㄦ父鎴忎腑鐨勫簲鐢?

- **CI (鎸佺画闆嗘垚)**: 鎻愪氦浠ｇ爜鍚庯紝鏈嶅姟鍣ㄨ嚜鍔ㄧ紪璇戙€佹鏌ラ敊璇€?
- **CD (鎸佺画浜や粯)**: 姣忓ぉ锛堟垨姣忓皬鏃讹級鑷姩鎵撳嚭涓€涓彲鐜╃殑鐗堟湰锛屼緵绛栧垝鍜屾祴璇曢獙璇併€?
- **鏍稿績浠峰€?*: 缂╃煭鍙嶉寰幆銆備粠"鍐欏畬浠ｇ爜"鍒?鍦ㄦ墜鏈轰笂鐜╁埌"锛屾椂闂磋秺鐭紝寮€鍙戞晥鐜囪秺楂樸€?

## 馃洜锔?2. 瀹炶返搴旂敤 (Practical Implementation) - Vampirefall 閫傞厤

### 2.1 馃帹 缇庢湳绠＄嚎 (Art Pipeline)

- **璧勪骇瀵煎叆鍚庡鐞?(AssetPostprocessor)**:
    - **鐥涚偣**: 缇庢湳姣忔瀵煎叆璐村浘閮借鎵嬪姩閫?"Android", "Override", "ASTC_6x6"銆?
    - **瑙ｅ喅**: 缂栧啓 `OnPreprocessTexture` 鑴氭湰銆傛牴鎹枃浠跺す璺緞锛堝 `Assets/UI/Icons`锛夛紝鑷姩璁剧疆鍘嬬缉鏍煎紡銆丮ipmap 寮€鍏炽€?
    ```csharp
    // 绀轰緥: Assets/Editor/TextureImporterAutomation.cs
    public class TextureImporterAutomation : AssetPostprocessor
    {
        void OnPreprocessTexture()
        {
            TextureImporter importer = (TextureImporter)assetImporter;
            // 鑷姩璇嗗埆 UI 鏂囦欢澶?
            if (assetPath.Contains("Assets/UI"))
            {
                importer.textureType = TextureImporterType.Sprite;
                importer.mipmapEnabled = false; // UI 涓嶉渶瑕?Mipmap

                // 瀹夊崜骞冲彴璁剧疆
                TextureImporterPlatformSettings androidSettings = new TextureImporterPlatformSettings();
                androidSettings.name = "Android";
                androidSettings.overridden = true;
                androidSettings.format = TextureImporterFormat.ASTC_6x6; // 鍧囪　鍘嬬缉
                importer.SetPlatformTextureSettings(androidSettings);
            }
        }
    }
    ```

- **TA 宸ュ叿闆?*:
    - **Shader 鍙樹綋鍓旈櫎 (Shader Stripping)**: 鑷姩鍓旈櫎鐢ㄤ笉鍒扮殑 Shader 鍙樹綋锛屽ぇ骞呭噺灏忓寘浣擄紝鍔犲揩鎵撳寘閫熷害銆?
    - **Substance to Unity**: 鏉愯川搴撹嚜鍔ㄥ寲妗ユ帴銆?
- **UI 鑷姩鍖?*:
    - **Figma Importer**: 鐩存帴浠庤璁＄鐢熸垚 Unity UI 棰勫埗浣擄紙鎺ㄨ崘 `Doozy UI` 鎴栬嚜鐮斿伐鍏凤級銆?
    - **鍥鹃泦鑷姩鎵撳寘 (Sprite Atlas)**: 閬垮厤杩愯鏃?DrawCall 鐖嗙偢銆?

### 2.2 馃 绛栧垝绠＄嚎 (Design Pipeline)

- **閰嶇疆琛ㄥ伐浣滄祦 (Data Workflow)**:
    - **宸ュ叿**: **Luban** (寮虹儓鎺ㄨ崘) 鎴?**EasyTables**銆?
    - **娴佺▼**: Excel/Google Sheets -> 瀵艰〃宸ュ叿 -> 鐢熸垚 C# 浠ｇ爜 + 浜岃繘鍒舵暟鎹?-> Unity銆?
    - **浼樺娍**: 寮虹被鍨嬫鏌ワ紙濉敊 ID 鐩存帴鎶ラ敊锛夛紝鏀寔澶嶆潅鏁版嵁缁撴瀯锛堝祵濂楀垪琛ㄣ€佸鎬侊級锛屽姞杞介€熷害鏋佸揩銆?
    ```xml
    {/* 绀轰緥: Luban 瀹氫箟 (Defines.xml) */}
    <bean name="Item">
        <var name="id" type="int"/>
        <var name="name" type="string"/>
        <var name="rarity" type="ERarity"/> {/* 鏋氫妇绫诲瀷 */}
    </bean>
    <table name="TbItem" value="Item" input="Item.xlsx" output="Item.bin"/>
    ```

- **鍏冲崱璁捐宸ュ叿**:
    - **Tilemap 绗斿埛**: 鑷姩澶勭悊杞杩炴帴 (Rule Tile)銆?
    - **闅忔満绉嶅瓙棰勮**: 鍦ㄧ紪杈戝櫒閲岀洿鎺ラ瑙堜笉鍚?Seed 鐢熸垚鐨勫湴鍥撅紝涓嶉渶瑕佽繍琛屾父鎴忋€?
- **闈欐€佸垎鏋?(Static Analysis)**:
    - 缂栧啓缂栬緫鍣ㄨ彍鍗?`Tools/Verify All Data`銆備竴閿鏌ユ墍鏈夋帀钀借〃鏄惁閰嶇疆浜嗕笉瀛樺湪鐨勭墿鍝?ID锛屾€墿鏁板€兼槸鍚︿负璐熸暟銆?
    ```csharp
    // 绀轰緥: Luban 鑷畾涔夐獙璇佸櫒 (LubanValidator.cs)
    // 鍦ㄥ姞杞藉畬鎵€鏈夐厤缃〃鍚庯紝鎵ц娣卞害妫€鏌?
    public static void ValidateAll()
    {
        var tables = Tables.Instance; // Luban 鐢熸垚鐨勫叆鍙?

        foreach (var monster in tables.TbMonster.DataList)
        {
            // 楠岃瘉 1: 鎺夎惤 ID 鏄惁瀛樺湪浜庢帀钀借〃涓?(澶栭敭妫€鏌?
            if (!tables.TbLoot.ContainsKey(monster.DropId))
            {
                Debug.LogError($"閰嶇疆閿欒: 鎬墿 {monster.Id} 鐨勬帀钀絀D {monster.DropId} 涓嶅瓨鍦紒");
            }

            // 楠岃瘉 2: 鎶€鑳?ID 鍒楄〃妫€鏌?
            foreach (int skillId in monster.SkillIds)
            {
                if (!tables.TbSkill.ContainsKey(skillId))
                {
                    Debug.LogError($"閰嶇疆閿欒: 鎬墿 {monster.Id} 寮曠敤浜嗘棤鏁堟妧鑳?{skillId}");
                }
            }
        }
        Debug.Log("閰嶇疆琛ㄩ獙璇佸畬鎴?);
    }
    ```

### 2.3 馃捇 绋嬪簭绠＄嚎 (Engineering Pipeline)

- **浠ｇ爜鐢熸垚 (Code Generation)**:
    - **缃戠粶鍗忚**: 浣跨敤 Protobuf 鎴?Flatbuffers 瀹氫箟鍗忚锛岃嚜鍔ㄧ敓鎴?C# 鍜屾湇鍔″櫒绔唬鐮併€?
    - **浜嬩欢鎬荤嚎**: 鑷姩鎵弿鎵€鏈変簨浠剁被鍨嬶紝鐢熸垚寮虹被鍨嬬殑璁㈤槄/鍙戝竷鎺ュ彛锛岄伩鍏嶅瓧绗︿覆鎷煎啓閿欒銆?
    - **UI 浠ｇ爜鐢熸垚 (UI Binding)**:
        - **鐥涚偣**: 鎵嬪啓 `public Button btnStart;` 鐒跺悗鍦?Inspector 閲屾嫋鎷斤紝瀹规槗涓㈠け寮曠敤銆?
        - **瑙ｅ喅**: 缂栧啓宸ュ叿閬嶅巻 Prefab锛岃嚜鍔ㄧ敓鎴?View 绫诲苟缁戝畾寮曠敤銆?
      
    ```csharp
    // 绀轰緥: 鑷姩鐢熸垚 UI 缁戝畾浠ｇ爜 (UIGenerator.cs)
    // 閬嶅巻 Prefab锛屾壘鍒版墍鏈変互 "btn_" 寮€澶寸殑鑺傜偣锛岃嚜鍔ㄧ敓鎴?C# 寮曠敤
    public class UIGenerator
    {
        [MenuItem("Tools/UI/Generate Code")]
        public static void Generate()
        {
            GameObject prefab = Selection.activeGameObject;
            StringBuilder sb = new StringBuilder();
            sb.AppendLine($"public class {prefab.name}View : MonoBehaviour {{");

            foreach (Transform child in prefab.GetComponentsInChildren<Transform>(true))
            {
                // 绾﹀畾浼樹簬閰嶇疆: 浠?btn_ 寮€澶寸殑鑺傜偣鑷姩鐢熸垚 Button 寮曠敤
                if (child.name.StartsWith("btn_"))
                {
                    sb.AppendLine($"    public Button {child.name};");
                }
                else if (child.name.StartsWith("txt_"))
                {
                    sb.AppendLine($"    public TextMeshProUGUI {child.name};");
                }
            }
            sb.AppendLine("}");
            // 鍐欏叆 .cs 鏂囦欢...
        }
    }
    ```
    

- **鏋勫缓鑷姩鍖?(Build Automation)**:
    - **Jenkins / GitHub Actions / TeamCity**:
        - **Commit Build**: 姣忔鎻愪氦锛岃窇涓€閬嶅崟鍏冩祴璇曘€?
        - **Nightly Build**: 姣忔櫄鑷姩鎵撳嚭 Android/iOS 鍖咃紝涓婁紶鍒板唴缃戞湇鍔″櫒锛屽苟閫氳繃椋炰功/閽夐拤鏈哄櫒浜洪€氱煡缇ょ粍銆?
      
    ```yaml
    # 绀轰緥: GitHub Actions (main.yml)
    name: Build Android
    on: [push]
    jobs:
      build:
        runs-on: ubuntu-latest
        steps:
          - uses: actions/checkout@v2
          - uses: game-ci/unity-builder@v2
            with:
              targetPlatform: Android
              androidAppBundle: false
              androidKeystoreName: user.keystore
              androidKeystorePass: ${{ secrets.KEYSTORE_PASS }}
    ```
    

- **璐ㄩ噺鎺у埗**:
    - **Roslyn Analyzers**: 寮哄埗鎵ц浠ｇ爜瑙勮寖锛堝锛氱姝㈠湪 Update 閲屼娇鐢?`FindObjectOfType`锛夈€?
    - **Odin Inspector**: 鏋侀€熸墿灞曠紪杈戝櫒銆傜敤鍑犺浠ｇ爜缁欑瓥鍒掑仛鍑哄ソ鐢ㄧ殑鎶€鑳界紪杈戝櫒锛岃€屼笉鏄啓鍑犵櫨琛?`OnInspectorGUI`銆?

    ```csharp
    // 绀轰緥: 鎶€鑳界紪杈戝櫒 (SkillData.cs)
    public class SkillData : ScriptableObject
    {
        [LabelText("鎶€鑳藉悕绉?)]
        public string skillName;

        [ValueDropdown("GetAllSkillIcons")] // 涓嬫媺閫夋嫨鍥炬爣
        [PreviewField(50)] // 棰勮鍥?
        public Sprite icon;

        [TableList] // 鍒楄〃鏄剧ず涓鸿〃鏍?
        public List<SkillEffect> effects;

        // 鑾峰彇鎵€鏈夊浘鏍囩殑杈呭姪鍑芥暟
        private IEnumerable GetAllSkillIcons() { ... }
    }
    ```

## 馃専 3. 涓氱晫浼樼妗堜緥 (Industry Best Practices)

### 3.1 澶у瀷鍥㈤槦 (Ubisoft/EA)

- **鍏变韩寮曟搸缁?*: 鏁扮櫨浜虹淮鎶や竴濂楀唴閮ㄥ紩鎿庡拰宸ュ叿閾俱€?
- **閬ユ祴绯荤粺 (Telemetry)**: 璁板綍缂栬緫鍣ㄩ噷姣忎釜鎸夐挳鐨勭偣鍑绘鏁般€傚鏋滄煇涓伐鍏锋病浜虹敤锛屽氨鐮嶆帀锛涘鏋滄煇涓搷浣滃お棰戠箒锛屽氨浼樺寲瀹冦€?

### 3.2 鐙珛/涓瀷鍥㈤槦 (Indie/Mid-size)

- **鍊熷姏鎵撳姏**: 娌¤祫婧愯嚜鐮斿紩鎿庯紝灏变拱鏈€濂界殑鎻掍欢銆?
    - **Odin Inspector**: 缂栬緫鍣ㄦ墿灞曠鍣ㄣ€?
    - **Rewired / Input System**: 杈撳叆绠＄悊銆?
    - **A\* Pathfinding Pro**: 瀵昏矾銆?
    - **DOTween**: 鍔ㄧ敾銆?
- **灏忓洟闃熺殑鑷姩鍖?*:
    - 涓嶈鎼缓澶嶆潅鐨?Jenkins 闆嗙兢銆傚啓涓€涓畝鍗曠殑 `BuildScript.cs`锛岄厤鍚?Windows 璁″垝浠诲姟锛屾瘡鏅氬湪涓€鍙伴棽缃殑 PC 涓婃墦鍖呭嵆鍙€?

### 2.4 馃攳 璋冭瘯涓庢€ц兘鍒嗘瀽宸ュ叿 (Debug & Profiling Tools)

#### 2.4.1 Unity Profiler 杩涢樁浣跨敤

- **鐥涚偣**: Profiler 鏁版嵁澶锛屼笉鐭ラ亾鐪嬪摢閲屻€?
- **鎶€宸?*:
    - **Deep Profile**: 绮剧‘鍒版瘡涓嚱鏁帮紝浣嗕細鎷栨參娓告垙銆傚彧鍦ㄥ畾浣嶆€ц兘鐡堕鏃跺紑鍚€?
    - **Hierarchy 瑙嗗浘**: 鎸夎皟鐢ㄦ爤鏌ョ湅锛屾壘鍑烘渶鑰楁椂鐨勮皟鐢ㄩ摼銆?
    - **Timeline 瑙嗗浘**: 鏌ョ湅鍗曞抚鍐呯殑璇︾粏鏃跺簭锛岃瘖鏂崱椤裤€?

    ```csharp
    // 鑷畾涔夋€ц兘鏍囪 (ProfilerMarker)
    using Unity.Profiling;

    public class CombatSystem : MonoBehaviour
    {
        static readonly ProfilerMarker s_CalculateDamage = new ProfilerMarker("CombatSystem.CalculateDamage");

        public float CalculateDamage(float baseDamage)
        {
            using (s_CalculateDamage.Auto()) // 鑷姩璁℃椂杩欐浠ｇ爜
            {
                // 澶嶆潅鐨勪激瀹宠绠?..
                return baseDamage * 1.5f;
            }
        }
    }
    ```

#### 2.4.2 鍐呭瓨鍒嗘瀽宸ュ叿

- **Memory Profiler Package**: Unity 瀹樻柟鎻掍欢锛屽彲瑙嗗寲鍐呭瓨鍗犵敤銆?
    - **蹇収瀵规瘮**: 鎶撲袱涓揩鐓э紝瀵规瘮鍐呭瓨澧為暱锛屾壘鍐呭瓨娉勬紡銆?
    - **寮曠敤鏌ョ湅**: 鐐瑰嚮鏌愪釜瀵硅薄锛岀湅璋佹寔鏈夊畠鐨勫紩鐢紙涓轰粈涔堟病琚?GC 鍥炴敹锛夈€?
- **甯歌闂**:
    - **闂寘鎹曡幏**: Lambda 琛ㄨ揪寮忔剰澶栨崟鑾蜂簡澶у璞°€?
    - **闈欐€佸彉閲?*: 闀跨敓鍛藉懆鏈熺殑 `static List` 绉疮浜嗗ぇ閲忔暟鎹€?
    - **浜嬩欢鏈敞閿€**: `OnEnable` 娉ㄥ唽浜嗕簨浠讹紝浣?`OnDisable` 蹇樿娉ㄩ攢銆?

    ```csharp
    // 閿欒绀轰緥: 浜嬩欢娉勬紡
    void OnEnable()
    {
        EventBus.OnPlayerDeath += HandleDeath; // 鉂?蹇樿娉ㄩ攢
    }

    // 姝ｇ‘绀轰緥
    void OnDisable()
    {
        EventBus.OnPlayerDeath -= HandleDeath; // 鉁?鎴愬鍑虹幇
    }
    ```

#### 2.4.3 宕╂簝鏀堕泦涓庡垎鏋?

- **宸ュ叿閫夋嫨**:
    - **Unity Cloud Diagnostics**: Unity 瀹樻柟鍏嶈垂鏂规锛岃嚜鍔ㄦ敹闆嗗穿婧冩棩蹇椼€?
    - **Bugly / Crashlytics**: 鑵捐鍜?Google 鐨勬柟妗堬紝鏀寔绗﹀彿琛ㄨ繕鍘熷爢鏍堛€?
    - **Sentry**: 寮€婧愭柟妗堬紝鏀寔鑷缓鏈嶅姟鍣ㄣ€?
- **鏈€浣冲疄璺?*:
    - **绗﹀彿琛ㄤ笂浼?*: 鎵撳寘鏃惰嚜鍔ㄤ笂浼?Symbols 鏂囦欢锛屽惁鍒欑湅鍒扮殑鍫嗘爤閮芥槸鍦板潃锛屾棤娉曞畾浣嶃€?
    - **鑷畾涔夐敊璇笂鎶?*:
    ```csharp
    // 鍏抽敭閫昏緫鍔?try-catch锛屼富鍔ㄤ笂鎶?
    try
    {
        LoadPlayerData();
    }
    catch (Exception e)
    {
        // 涓婃姤鍒板穿婧冨钩鍙帮紝闄勫甫鐜╁ID銆佽澶囦俊鎭?
        CrashReporter.Report(e, new Dictionary<string, string>()
        {
            { "PlayerID", playerID },
            { "Level", currentLevel.ToString() }
        });
    }
    ```

#### 2.4.4 绉诲姩绔皟璇曞伐鍏?

- **Unity Remote 5**: 鍦ㄧ紪杈戝櫒閲岃繍琛岋紝瀹炴椂鍚屾鍒版墜鏈哄睆骞曘€傞€傚悎蹇€熼獙璇佽Е鎽搁€昏緫銆?
- **Android Logcat / Xcode Console**: 鏌ョ湅鍘熺敓鏃ュ織锛岃瘖鏂惎鍔ㄥ穿婧冦€?
- **Wireless Debugging**: Android 11+ 鏀寔鏃犵嚎璋冭瘯锛屾憜鑴辨暟鎹嚎鏉熺細銆?
  ```bash
  # Android 鏃犵嚎璋冭瘯閰嶇疆
  adb tcpip 5555
  adb connect 192.168.1.100:5555
  ```

- **鍦ㄥ睆璋冭瘯鑿滃崟 (In-Game Debug Menu)**:
    - **鐥涚偣**: 鎵嬫満涓婃棤娉曟墦鏂偣锛岄毦浠ヨ皟璇曘€?
    - **瑙ｅ喅**: 鍋氫竴涓诞绐楋紝鏄剧ず FPS銆佸唴瀛樸€佺綉缁滃欢杩燂紝鎻愪緵浣滃紛鎸夐挳锛堜竴閿€氬叧銆佹棤闄愰噾甯侊級銆?
    ```csharp
    // 绀轰緥: 绠€鏄撹皟璇曡彍鍗?(DebugMenu.cs)
    public class DebugMenu : MonoBehaviour
    {
        private bool showMenu = false;

        void Update()
        {
            // 涓夋寚鍚屾椂鐐瑰嚮灞忓箷锛屽紑鍚皟璇曡彍鍗?
            if (Input.touchCount == 3)
            {
                showMenu = !showMenu;
            }
        }

        void OnGUI()
        {
            if (!showMenu) return;

            GUILayout.BeginArea(new Rect(10, 10, 300, 400));
            GUILayout.Label("FPS: " + (1.0f / Time.deltaTime).ToString("F1"));
            GUILayout.Label("Memory: " + (GC.GetTotalMemory(false) / 1024 / 1024) + " MB");

            if (GUILayout.Button("鏃犳晫妯″紡"))
            {
                PlayerController.Instance.SetGodMode(true);
            }

            if (GUILayout.Button("璺宠繃褰撳墠鍏冲崱"))
            {
                LevelManager.Instance.CompleteLevel();
            }

            GUILayout.EndArea();
        }
    }
    ```

### 2.5 馃И 娴嬭瘯宸ュ叿閾?(Testing Toolchain)

#### 2.5.1 鍗曞厓娴嬭瘯 (Unit Testing)

- **妗嗘灦**: Unity Test Framework (鍩轰簬 NUnit)銆?
- **閫傜敤鍦烘櫙**: 娴嬭瘯绾€昏緫浠ｇ爜锛堝浼ゅ璁＄畻銆佹帀钀界畻娉曪級銆?

  ```csharp
  // 绀轰緥: 浼ゅ璁＄畻鍗曞厓娴嬭瘯 (DamageCalculatorTests.cs)
  using NUnit.Framework;

  public class DamageCalculatorTests
  {
      [Test]
      public void TestCriticalHit()
      {
          // Arrange: 鍑嗗娴嬭瘯鏁版嵁
          float baseDamage = 100f;
          float critMultiplier = 2.0f;

          // Act: 鎵ц琚祴璇曠殑浠ｇ爜
          float result = DamageCalculator.Calculate(baseDamage, isCritical: true, critMultiplier);

          // Assert: 楠岃瘉缁撴灉
          Assert.AreEqual(200f, result, 0.01f); // 鍏佽娴偣璇樊
      }

      [Test]
      public void TestDefenseReduction()
      {
          // 娴嬭瘯闃插尽鍔涘噺浼ゅ叕寮? Damage * 100 / (100 + Defense)
          float damage = 100f;
          float defense = 100f;
          float result = DamageCalculator.ApplyDefense(damage, defense);
          Assert.AreEqual(50f, result, 0.01f); // 100 * 100 / 200 = 50
      }
  }
  ```

- **娴嬭瘯椹卞姩寮€鍙?(TDD)**: 鍏堝啓娴嬭瘯鐢ㄤ緥锛屽啀瀹炵幇鍔熻兘銆傞€傚悎鏍稿績鏁板€肩郴缁熴€?

#### 2.5.2 闆嗘垚娴嬭瘯 (Integration Testing)

- **鍦烘櫙**: 娴嬭瘯澶氫釜绯荤粺鍗忎綔锛堝鎴樻枟绯荤粺 + 鎶€鑳界郴缁?+ Buff 绯荤粺锛夈€?
- **PlayMode Tests**: 鍦ㄨ繍琛屾椂鐜涓祴璇曪紝鍙互鍔犺浇鍦烘櫙銆佺敓鎴?GameObject銆?

  ```csharp
  // 绀轰緥: 鎴樻枟闆嗘垚娴嬭瘯 (CombatIntegrationTests.cs)
  using UnityEngine.TestTools;
  using System.Collections;

  public class CombatIntegrationTests
  {
      [UnityTest]
      public IEnumerator TestPlayerAttackEnemy()
      {
          // 鍔犺浇鎴樻枟鍦烘櫙
          SceneManager.LoadScene("BattleScene");
          yield return null; // 绛夊緟涓€甯э紝鍦烘櫙鍔犺浇瀹屾垚

          // 鐢熸垚鐜╁鍜屾晫浜?
          var player = GameObject.Find("Player").GetComponent<PlayerController>();
          var enemy = GameObject.Find("Enemy").GetComponent<EnemyController>();

          float initialHP = enemy.CurrentHP;

          // 鎵ц鏀诲嚮
          player.Attack(enemy);

          // 绛夊緟浼ゅ缁撶畻锛堝彲鑳芥湁寤惰繜锛?
          yield return new WaitForSeconds(0.5f);

          // 楠岃瘉鏁屼汉琛€閲忓噺灏?
          Assert.Less(enemy.CurrentHP, initialHP);
      }
  }
  ```

#### 2.5.3 鎬ц兘鍥炲綊娴嬭瘯 (Performance Regression Testing)

- **Unity Performance Testing Package**: 瀹樻柟鎻掍欢锛岃嚜鍔ㄨ窇鎬ц兘鍩哄噯娴嬭瘯銆?
- **搴旂敤**: 姣忔鎵撳寘鍓嶏紝鑷姩璺戜竴閬嶅叧閿満鏅紝纭繚甯х巼娌℃湁涓嬮檷銆?

  ```csharp
  // 绀轰緥: 鎬ц兘鍩哄噯娴嬭瘯 (PerformanceTests.cs)
  using Unity.PerformanceTesting;

  public class PerformanceTests
  {
      [Test, Performance]
      public void MeasureSpawnPerformance()
      {
          Measure.Method(() =>
          {
              // 鐢熸垚 100 涓晫浜?
              for (int i = 0; i \< 100; i++)
              {
                  Object.Instantiate(enemyPrefab);
              }
          })
          .WarmupCount(10)     // 棰勭儹 10 娆?
          .MeasurementCount(50) // 娴嬮噺 50 娆?
          .Run();
      }
  }
  ```

#### 2.5.4 鑷姩鍖?UI 娴嬭瘯

- **宸ュ叿**: **Appium** (璺ㄥ钩鍙? 鎴?**Altom Unity Tester**銆?
- **鍦烘櫙**: 妯℃嫙鐜╁鐐瑰嚮鎸夐挳锛岃窇瀹屾暣涓柊鎵嬫暀绋嬶紝妫€鏌ユ槸鍚﹀穿婧冦€?
- **鎸戞垬**: UI 鍙樺寲棰戠箒锛岀淮鎶ゆ垚鏈珮銆傚缓璁彧娴嬫牳蹇冩祦绋嬶紙鐧诲綍銆侀娆′粯璐癸級銆?

### 2.6 馃摝 鐗堟湰绠＄悊鏈€浣冲疄璺?(Version Control Best Practices)

#### 2.6.1 Git 閰嶇疆浼樺寲

- **.gitignore**: 閬垮厤鎻愪氦 Unity 鐢熸垚鏂囦欢銆?

  ```gitignore
  # Unity 鐢熸垚鏂囦欢
  /[Ll]ibrary/
  /[Tt]emp/
  /[Oo]bj/
  /[Bb]uild/
  /[Bb]uilds/
  /[Ll]ogs/

  # Visual Studio
  .vs/
  *.csproj
  *.sln
  *.suo

  # Rider
  .idea/

  # OS
  .DS_Store
  Thumbs.db
  ```

- **.gitattributes**: 寮哄埗浣跨敤 LF 鎹㈣绗︼紝閬垮厤璺ㄥ钩鍙板啿绐併€?

  ```gitattributes
  # 鎵€鏈夋枃鏈枃浠朵娇鐢?LF
  * text=auto eol=lf

  # Unity 鍦烘櫙/棰勫埗浣撲娇鐢?YAML 妯″紡锛屾柟渚垮悎骞?
  *.unity merge=unityyamlmerge eol=lf
  *.prefab merge=unityyamlmerge eol=lf

  # 浜岃繘鍒舵枃浠朵笉鍋氭枃鏈鐞?
  *.png binary
  *.jpg binary
  *.ogg binary
  ```

#### 2.6.2 Git LFS (Large File Storage)

- **鐥涚偣**: 缇庢湳璧勬簮浣撶Н澶э紝鐩存帴鎻愪氦鍒?Git 浼氬鑷翠粨搴撹啫鑳€锛屽厠闅嗘瀬鎱€?
- **瑙ｅ喅**: 浣跨敤 Git LFS 瀛樺偍澶ф枃浠讹紙鑷姩涓婁紶鍒?CDN锛夈€?

  ```bash
  # 瀹夎 Git LFS
  git lfs install

  # 閰嶇疆杩借釜瑙勫垯 (.gitattributes)
  *.psd filter=lfs diff=lfs merge=lfs -text
  *.png filter=lfs diff=lfs merge=lfs -text
  *.ogg filter=lfs diff=lfs merge=lfs -text
  *.mp4 filter=lfs diff=lfs merge=lfs -text
  ```

- **娉ㄦ剰**: LFS 鏈夋祦閲忛檺鍒躲€傚缓璁敤鑷缓鏈嶅姟鍣紙濡傝吘璁?CODING锛夋垨浠樿垂濂楅銆?

#### 2.6.3 鍒嗘敮绛栫暐 (Branching Strategy)

- **Git Flow** (閫傚悎澶у洟闃?:
    - `main`: 绾夸笂鐗堟湰锛屽彧鎺ュ彈鍙戝竷鍒嗘敮鍚堝苟銆?
    - `develop`: 寮€鍙戜富鍒嗘敮锛屾墍鏈夊姛鑳藉垎鏀悎骞跺埌杩欓噷銆?
    - `feature/*`: 鍔熻兘鍒嗘敮锛堝 `feature/new-tower`锛夈€?
    - `release/*`: 鍙戝竷鍊欓€夊垎鏀紝閿佸畾鍔熻兘锛屽彧淇?Bug銆?
    - `hotfix/*`: 绱ф€ヤ慨澶嶏紝鐩存帴浠?`main` 鎷夊嚭銆?
- **Trunk-Based** (閫傚悎灏忓洟闃?:
    - 鍙湁涓€涓?`main` 鍒嗘敮锛屾墍鏈変汉閮藉線杩欓噷鎻愪氦銆?
    - 鐢?Feature Flags 鎺у埗鏈畬鎴愬姛鑳斤紙浠ｇ爜閲屽姞寮€鍏筹紝榛樿鍏抽棴锛夈€?

#### 2.6.4 鍐茬獊澶勭悊鎶€宸?

- **棰勫埗浣?鍦烘櫙鍐茬獊**: 浣跨敤 **UnityYAMLMerge** 宸ュ叿鏅鸿兘鍚堝苟銆?
    - 閰嶇疆璺緞锛歚C:\Program Files\Unity\Hub\Editor\2021.3.0f1\Editor\Data\Tools\UnityYAMLMerge.exe`
    - 淇敼 `.git/config`:

    ```ini
    [merge]
    tool = unityyamlmerge

    [mergetool "unityyamlmerge"]
    cmd = 'C:/Program Files/Unity/Hub/Editor/2021.3.0f1/Editor/Data/Tools/UnityYAMLMerge.exe' merge -p "$BASE" "$REMOTE" "$LOCAL" "$MERGED"
    trustExitCode = false
    ```

- **閬垮厤鍐茬獊**: 绛栧垝鍜岀編鏈笉瑕佺洿鎺ユ敼鍦烘櫙鏂囦欢锛岃€屾槸鏀规垚 Prefab 宓屽銆傛瘡浜鸿礋璐ｄ笉鍚岀殑 Prefab銆?

#### 2.6.5 Git Hooks 鑷姩鍖?

- **Pre-Commit Hook**: 鎻愪氦鍓嶈嚜鍔ㄦ牸寮忓寲浠ｇ爜銆佹鏌ュ懡鍚嶈鑼冦€?
  ```bash
  # .git/hooks/pre-commit
  #!/bin/sh
  # 妫€鏌ユ槸鍚︽湁瓒呰繃 100MB 鐨勬枃浠讹紙蹇樿鐢?LFS锛?
  for file in $(git diff --cached --name-only); do
      if [ -f "$file" ]; then
          size=$(wc -c \< "$file")
          if [ $size -gt 104857600 ]; then
              echo "閿欒: $file 瓒呰繃 100MB锛岃浣跨敤 Git LFS!"
              exit 1
          fi
      fi
  done
  ```

### 2.7 馃 鍗忎綔涓庢矡閫氬伐鍏?(Collaboration Tools)

#### 2.7.1 鏂囨。鍗忎綔

- **Notion / 璇泙**: 鍥㈤槦鐭ヨ瘑搴擄紝璁板綍璁捐鏂囨。銆佷細璁邯瑕併€?
- **Miro / FigJam**: 鍦ㄧ嚎鐧芥澘锛屽ご鑴戦鏆淬€佺粯鍒剁郴缁熸灦鏋勫浘銆?
- **Markdown**: 绾枃鏈枃妗ｏ紝鏂逛究鐗堟湰绠＄悊銆傛帹鑽愮敤 **Typora** 鎴?**Obsidian** 缂栬緫銆?

#### 2.7.2 浠诲姟绠＄悊

- **Jira**: 澶у洟闃熸爣閰嶏紝鏀寔 Scrum銆佺湅鏉裤€佺敇鐗瑰浘銆?
- **Trello / Teambition**: 杞婚噺绾х湅鏉匡紝閫傚悎灏忓洟闃熴€?
- **GitHub Projects**: 鐩存帴鍦ㄤ唬鐮佷粨搴撻噷绠＄悊浠诲姟锛孖ssue 鍜?Pull Request 鑱斿姩銆?

#### 2.7.3 浠ｇ爜瀹℃煡 (Code Review)

- **宸ュ叿**: GitHub Pull Request銆丟itLab Merge Request銆?
- **鏈€浣冲疄璺?*:
    - **灏?PR**: 姣忔涓嶈秴杩?300 琛屾敼鍔紝鏂逛究瀹℃煡銆?
    - **鑷姩鍖栨鏌?*: CI 鑷姩璺戝崟鍏冩祴璇曪紝閫氳繃鎵嶈兘鍚堝苟銆?
    - **妯℃澘**: Pull Request 鎻忚堪妯℃澘锛屽己鍒跺～鍐?鏀逛簡浠€涔?銆?涓轰粈涔堟敼"銆?鎬庝箞娴嬭瘯"銆?

    ```markdown
    ## 鏀瑰姩璇存槑
    - 鏂板鎶€鑳界郴缁?
    - 淇濉旈槻璺緞瀵昏矾 Bug

    ## 娴嬭瘯姝ラ
    1. 杩涘叆鍏冲崱 1-3
    2. 鏀剧疆鐏劙濉?
    3. 楠岃瘉鏁屼汉浼氱粫璺?

    ## 鎴浘/瑙嗛

    [闄勪笂婕旂ず GIF]
    ```

#### 2.7.4 瀹炴椂娌熼€?

- **Discord / Slack**: 杩滅▼鍥㈤槦甯哥敤锛屾敮鎸佽闊炽€佸睆骞曞叡浜€佹満鍣ㄤ汉闆嗘垚銆?
- **鑵捐浼氳 / 椋炰功**: 鍥藉唴鍥㈤槦鍙嬪ソ锛岄泦鎴?OKR銆佹棩鍘嗐€佹枃妗ｃ€?
- **Git Bot 闆嗘垚**: 鎻愪氦浠ｇ爜鍚庯紝鑷姩鍦ㄧ兢閲岄€氱煡銆?
  ```yaml
  # 绀轰緥: GitHub Actions 閫氱煡椋炰功缇?(feishu-notify.yml)
  - name: Notify Feishu
    run: |
      curl -X POST https://open.feishu.cn/open-apis/bot/v2/hook/YOUR_WEBHOOK \
      -H 'Content-Type: application/json' \
      -d '{
        "msg_type": "text",
        "content": {
          "text": "锟?鏂扮増鏈凡鍙戝竷锛佺増鏈彿: v1.2.3"
        }
      }'
  ```

### 2.8 馃幍 闊抽宸ュ叿閾?(Audio Pipeline)

#### 2.8.1 闊虫晥绠＄悊

- **FMOD / Wwise**: 琛屼笟鏍囧噯涓棿浠讹紝鏀寔鍔ㄦ€侀煶涔愩€?D 闊虫晥銆佸弬鏁板寲鎺у埗銆?
    - **浼樺娍**: 涓嶇敤鍐欎唬鐮佸氨鑳借皟闊虫晥鍙傛暟锛堥煶閲忋€佹贩鍝嶃€佹护娉㈠櫒锛夈€?
    - **鑷姩鍖?*: 闊抽甯堝湪 FMOD Studio 閲岃皟濂斤紝瀵煎嚭 Bank 鏂囦欢锛孶nity 鑷姩鍔犺浇銆?
- **Unity AudioMixer**: Unity 鍐呯疆鏂规锛岄€傚悎绠€鍗曢」鐩€?
    - **鎶€宸?*: 鐢?Snapshot 鍒囨崲鍦烘櫙闊虫晥锛堝杩涘叆娲炵┐锛岃嚜鍔ㄥ姞娣峰搷锛夈€?

#### 2.8.2 闊抽璧勬簮浼樺寲

- **鍘嬬缉鏍煎紡閫夋嫨**:
    - **鑳屾櫙闊充箰**: Vorbis (OGG)锛屽帇缂╂瘮楂橈紝閫傚悎闀块煶棰戙€?
    - **鐭煶鏁?*: ADPCM锛岃В鍘嬪揩锛岄€傚悎棰戠箒鎾斁鐨勮剼姝ュ０銆佹灙澹般€?
    - **瀵圭櫧**: MP3锛屽吋瀹规€уソ銆?
- **Load Type**:
    - **Decompress On Load**: 涓€娆℃€цВ鍘嬪埌鍐呭瓨锛屽崰鍐呭瓨浣嗘€ц兘濂姐€傞€傚悎鐭煶鏁堛€?
    - **Compressed In Memory**: 鎾斁鏃惰В鍘嬶紝鐪佸唴瀛樹絾鑰?CPU銆傞€傚悎鑳屾櫙闊充箰銆?
    - **Streaming**: 杈规挱杈硅锛屾渶鐪佸唴瀛橈紝浣嗚鐩樺彲鑳藉崱椤裤€?

#### 2.8.3 闊抽鑷姩鍖栧伐鍏?

- **鎵归噺褰掍竴鍖栭煶閲?*: 鐢?**FFmpeg** 鑷姩璋冩暣鎵€鏈夐煶鏁堢殑鍝嶅害锛岄伩鍏嶅拷澶у拷灏忋€?
  ```bash
  # 鎵归噺澶勭悊闊虫晥锛屽綊涓€鍖栧埌 -16 LUFS
  for file in *.wav; do
      ffmpeg-normalize "$file" -o "normalized_$file" -t -16
  done
  ```

### 2.9 馃實 鏈湴鍖栧伐鍏?(Localization Tools)

#### 2.9.1 Unity Localization Package

- **瀹樻柟鎻掍欢**: 鏀寔澶氳瑷€瀛楃涓层€佽祫浜ф湰鍦板寲锛堝涓枃鐢ㄥ畫浣擄紝鏃ユ枃鐢ㄩ粦浣擄級銆?
- **娴佺▼**:
    1. 鍒涘缓 String Table锛屽～鍏ユ墍鏈夋枃鏈紙ID + 鍚勮瑷€缈昏瘧锛夈€?
    2. 浠ｇ爜閲岀敤 `LocalizedString` 寮曠敤锛岃嚜鍔ㄦ牴鎹綋鍓嶈瑷€鍒囨崲銆?

     ```csharp
     using UnityEngine.Localization;

     public LocalizedString welcomeText; // 鍦?Inspector 閲岄€夋嫨 String Table 鐨勬煇涓€椤?

     void Start()
     {
         // 寮傛鍔犺浇鏈湴鍖栧瓧绗︿覆
         welcomeText.GetLocalizedStringAsync().Completed += (op) =>
         {
             Debug.Log(op.Result); // 涓枃鏄剧ず"娆㈣繋"锛岃嫳鏂囨樉绀?Welcome"
         };
     }
     ```

- **璧勪骇鏈湴鍖?*: 涓嶅悓璇█鐢ㄤ笉鍚屽浘鐗囷紙濡傛父鎴?Logo锛夈€?

#### 2.9.2 缈昏瘧鍗忎綔

- **POEditor / Crowdin**: 鍦ㄧ嚎缈昏瘧骞冲彴锛屾敮鎸佸浜哄崗浣溿€佹満鍣ㄧ炕璇戣緟鍔┿€?
- **瀵煎叆瀵煎嚭**: 缇庢湳/绛栧垝鍦?Excel 閲屽～缈昏瘧锛岀敤鑴氭湰涓€閿鍏ュ埌 Unity銆?
  ```csharp
  // 绀轰緥: Excel 杞?String Table (L10nImporter.cs)
  [MenuItem("Tools/Import Localization from Excel")]
  public static void ImportFromExcel()
  {
      var excel = new ExcelReader("Localization.xlsx");
      var table = LocalizationSettings.StringDatabase.GetTable("UI_Texts");

      foreach (var row in excel.Rows)
      {
          string key = row["Key"];
          string zh = row["Chinese"];
          string en = row["English"];

          table.AddEntry(key, zh); // 娣诲姞涓枃
          table.GetEntry(key).Locales["en"].Value = en; // 娣诲姞鑻辨枃
      }

      EditorUtility.SetDirty(table);
  }
  ```

### 2.10 馃敟 鐑洿鏂颁笌 LiveOps 宸ュ叿 (Hot Update & LiveOps)

#### 2.10.1 鐑洿鏂版柟妗?

- **HybridCLR (鍘?huatuo)**: Unity 瀹樻柟鏀寔鐨?C# 鐑洿鏂版柟妗堬紝鍩轰簬 IL2CPP銆?
    - **浼樺娍**: 鍙互鐑洿鏂颁笟鍔￠€昏緫浠ｇ爜锛堢瓥鍒掓敼鏁板€间笉鐢ㄩ噸鏂板彂鍖咃級銆?
    - **闄愬埗**: 涓嶈兘鏂板鍘熺敓鎻掍欢锛圓ndroid .so 鏂囦欢锛夈€?
- **AssetBundle**: 璧勬簮鐑洿鏂帮紝甯哥敤浜庢洿鏂扮編鏈祫婧愩€侀厤缃〃銆?
    - **宸ュ叿**: **Addressables** (Unity 瀹樻柟鎺ㄨ崘) 鎴?**YooAsset** (鍥藉唴寮€婧愭柟妗?銆?
    - **娴佺▼**: 鏈嶅姟鍣ㄦ斁鏂扮殑 AssetBundle锛屽鎴风鍚姩鏃舵鏌ョ増鏈彿锛屼笅杞芥洿鏂般€?

#### 2.10.2 杩愯惀娲诲姩閰嶇疆鍖?

- **Remote Config**: Unity 瀹樻柟鎻掍欢锛屾棤闇€鏇存柊鍖呭氨鑳芥敼閰嶇疆锛堝鍟嗗煄鎶樻墸銆佹椿鍔ㄥ紑鍏筹級銆?

  ```csharp
  // 绀轰緥: 浠庢湇鍔″櫒璇诲彇娲诲姩閰嶇疆
  using Unity.RemoteConfig;

  void Start()
  {
      ConfigManager.FetchCompleted += OnConfigFetched;
      ConfigManager.FetchConfigs();
  }

  void OnConfigFetched(ConfigResponse response)
  {
      bool isDoubleExpEvent = ConfigManager.appConfig.GetBool("doubleExpEvent");
      float discountRate = ConfigManager.appConfig.GetFloat("shopDiscount");

      if (isDoubleExpEvent)
      {
          GameManager.Instance.ExpMultiplier = 2.0f;
      }
  }
  ```

#### 2.10.3 A/B 娴嬭瘯

- **宸ュ叿**: **Firebase Remote Config** + **Analytics**銆?
- **鍦烘櫙**: 鏂版墜鏁欑▼鏀圭増锛?0% 鐜╁璧版柊娴佺▼锛?0% 璧版棫娴佺▼锛岀湅鍝釜鐣欏瓨鐜囬珮銆?

### 2.11 馃搳 鏁版嵁鍒嗘瀽涓庣洃鎺у伐鍏?(Analytics & Monitoring)

#### 2.11.1 鏁版嵁鍩嬬偣

- **宸ュ叿**: **Unity Analytics** (鍏嶈垂) / **Firebase Analytics** / **绁炵瓥鏁版嵁** (鍥藉唴)銆?
- **鍏抽敭鎸囨爣**:
    - **DAU/MAU**: 鏃ユ椿/鏈堟椿銆?
    - **鐣欏瓨鐜?*: 棣栨棩鐣欏瓨銆? 鏃ョ暀瀛樸€?
    - **ARPPU**: 浠樿垂鐜╁骞冲潎鏀跺叆銆?
    - **婕忔枟鍒嗘瀽**: 鏂版墜鏁欑▼鍚勬楠ょ殑娴佸け鐜囥€?
- **鍩嬬偣绀轰緥**:
  ```csharp
  // 璁板綍鐜╁瀹屾垚鏂版墜鏁欑▼
  Analytics.CustomEvent("tutorial_complete", new Dictionary<string, object>()
  {
      { "duration", Time.time }, // 鏁欑▼鐢ㄦ椂
      { "skipped", false }        // 鏄惁璺宠繃
  });
  ```

#### 2.11.2 瀹炴椂鐩戞帶

- **鏈嶅姟鍣ㄧ洃鎺?*: **Prometheus** + **Grafana**锛岀洃鎺ф湇鍔″櫒 CPU銆佸唴瀛樸€佸湪绾夸汉鏁般€?
- **瀹㈡埛绔洃鎺?*:
    - **宕╂簝鐜?*: 姣忔棩宕╂簝鐜囦笉瓒呰繃 0.5%銆?
    - **鍗￠】鐜?*: 缁熻浣庝簬 30 FPS 鐨勭帺瀹跺崰姣斻€?
    - **鍏冲崱閫氳繃鐜?*: 鏌愬叧鍗￠€氳繃鐜囦綆浜?10%锛岃鏄庨毦搴﹁璁℃湁闂銆?

#### 2.11.3 鏃ュ織鑱氬悎

- **ELK Stack** (Elasticsearch + Logstash + Kibana): 鏀堕泦鎵€鏈夊鎴风鍜屾湇鍔″櫒鏃ュ織锛屽彲瑙嗗寲鍒嗘瀽銆?
- **搴旂敤**: 鐜╁鍙嶉"绗簩鍏虫墦涓嶈繃"锛屾悳绱粬鐨勬棩蹇楋紝鍙戠幇鏄煇涓?Bug 瀵艰嚧鐨勩€?

## 馃幆 3.3 瀹炵敤灏忔妧宸?(Practical Tips & Tricks)

### 3.3.1 缂栬緫鍣ㄥ揩鎹烽敭鑷畾涔?

- **宸ュ叿**: **Shortcut Manager** (Unity 2019.1+)銆?
- **鎺ㄨ崘鑷畾涔?*:
    - `Ctrl+Shift+C`: 蹇€熷垱寤虹┖ GameObject 骞堕噸鍛藉悕銆?
    - `Ctrl+D` 鏀逛负 `Ctrl+Shift+D`: 閬垮厤璇Е澶嶅埗銆?
    - `Alt+G`: 蹇€熷垎缁勯€変腑鐨勫璞°€?

### 3.3.2 ScriptableObject 浣滀负閰嶇疆涓績

- **鐥涚偣**: 鍏ㄥ眬閰嶇疆鏁ｈ惤鍦ㄥ悇涓?Manager 鐨?`public static int maxHP = 100;`銆?
- **瑙ｅ喅**: 鐢?ScriptableObject 闆嗕腑绠＄悊銆?

  ```csharp
  // 绀轰緥: 娓告垙閰嶇疆 (GameConfig.asset)
  [CreateAssetMenu(fileName = "GameConfig", menuName = "Config/GameConfig")]
  public class GameConfig : ScriptableObject
  {
      public int playerMaxHP = 100;
      public float enemySpawnRate = 2.0f;
      public int startingGold = 500;
  }

  // 鍗曚緥璁块棶
  public static class Config
  {
      private static GameConfig _instance;
      public static GameConfig Instance
      {
          get
          {
              if (_instance == null)
                  _instance = Resources.Load<GameConfig>("GameConfig");
              return _instance;
          }
      }
  }

  // 浣跨敤
  int hp = Config.Instance.playerMaxHP;
  ```

### 3.3.3 涓€閿竻鐞嗛」鐩?

- **缂栬緫鍣ㄨ彍鍗?*: 瀹氭湡娓呯悊鏃犵敤璧勬簮锛屽噺灏忓寘浣撱€?

  ```csharp
  [MenuItem("Tools/Cleanup/Remove Empty Folders")]
  public static void RemoveEmptyFolders()
  {
      // 鎵弿鎵€鏈夋枃浠跺す锛屽垹闄ょ┖鏂囦欢澶?
  }

  [MenuItem("Tools/Cleanup/Find Unused Assets")]
  public static void FindUnusedAssets()
  {
      // 鍒嗘瀽鎵€鏈?Prefab/Scene锛屾爣璁颁粠鏈紩鐢ㄧ殑璧勬簮
  }
  ```

### 3.3.4 蹇€熷師鍨嬪伐鍏?

- **ProBuilder**: 鍦?Unity 閲岀洿鎺ュ缓妯★紝閫傚悎鍏冲崱鐧界洅銆?
- **Polybrush**: 鍦板舰鍒凤紝蹇€熺粯鍒惰崏鍦般€佺煶澶淬€?
- **Cinemachine**: 闀滃ご绯荤粺锛? 鍒嗛挓鎼炲畾璺熼殢闀滃ご銆佽繃鍦哄姩鐢汇€?

### 3.3.5 璧勪骇鍟嗗簵鎻掍欢鎺ㄨ崘

- **蹇呭鎻掍欢**:
    - **Odin Inspector**: 缂栬緫鍣ㄥ寮猴紝鎻愬崌 10 鍊嶇敓浜у姏銆?
    - **DOTween**: 琛ラ棿鍔ㄧ敾锛屾€ц兘浼樹簬 Unity 鑷甫銆?
    - **UniRx**: 鍝嶅簲寮忕紪绋嬶紝浼橀泤澶勭悊寮傛閫昏緫銆?
    - **Extenject (Zenject)**: 渚濊禆娉ㄥ叆妗嗘灦锛岃В鑰︿唬鐮併€?
- **缇庢湳宸ュ叿**:
    - **Amplify Shader Editor**: 鍙鍖?Shader 缂栬緫鍣ㄣ€?
    - **Bakery GPU Lightmapper**: 瓒呭揩鐨勫厜鐓х儤鐒欍€?

### 3.3.6 璺ㄥ钩鍙版瀯寤鸿嚜鍔ㄥ寲

- **涓€閿骞冲彴鎵撳寘**: 鍐欎釜缂栬緫鍣ㄨ彍鍗曪紝涓€娆℃墦鍑?Android銆乮OS銆乄indows 涓変釜骞冲彴鐨勫寘銆?

  ```csharp
  [MenuItem("Tools/Build All Platforms")]
  public static void BuildAll()
  {
      BuildPipeline.BuildPlayer(GetScenes(), "Builds/Android/game.apk", BuildTarget.Android, BuildOptions.None);
      BuildPipeline.BuildPlayer(GetScenes(), "Builds/iOS", BuildTarget.iOS, BuildOptions.None);
      BuildPipeline.BuildPlayer(GetScenes(), "Builds/Windows/game.exe", BuildTarget.StandaloneWindows64, BuildOptions.None);
  }

  static string[] GetScenes()
  {
      return EditorBuildSettings.scenes.Select(s => s.path).ToArray();
  }
  ```

## 锟金煍?4. 鍙傝€冭祫鏂?(References)

- 馃洜锔?**Luban**: [寮哄ぇ鐨勯厤缃〃宸ュ叿](https://github.com/focus-creative-games/luban)
- 馃洜锔?**Odin Inspector**: [Unity 缂栬緫鍣ㄦ墿灞曠粓鏋佹柟妗圿(https://odininspector.com/)
- 馃洜锔?**HybridCLR**: [C# 鐑洿鏂版柟妗圿(https://github.com/focus-creative-games/hybridclr)
- 馃洜锔?**YooAsset**: [璧勬簮鐑洿鏂版鏋禲(https://github.com/tuyoogame/YooAsset)
- 馃搫 **Blog**: [Automating Unity Builds with GitHub Actions](https://game.ci/docs/github/getting-started)
- 馃搫 **Blog**: [Unity Memory Profiler 浣跨敤鎸囧崡](https://docs.unity3d.com/Packages/com.unity.memoryprofiler@latest)
- 馃摵 **GDC**: [Tools Development at Insomniac Games](https://www.youtube.com/results?search_query=gdc+tools+development)
- 馃摵 **GDC**: [Automated Testing in Unity](https://www.youtube.com/results?search_query=gdc+automated+testing+unity)
- 馃摎 **Book**: _Game Programming Patterns_ by Robert Nystrom

---

## 馃摑 鎬荤粨 (Summary)

浼樼鐨勫伐鍏烽摼鏄珮鏁堟父鎴忓紑鍙戠殑鍩虹煶銆傝浣忎互涓嬪師鍒欙細

1. **鑷姩鍖栦竴鍒囧彲鑷姩鍖栫殑**锛氬鏋滄煇涓搷浣滈噸澶嶈秴杩?3 娆★紝灏辫€冭檻鍐欒剼鏈€?
2. **灏芥棭闆嗘垚 CI/CD**锛氫笉瑕佺瓑椤圭洰鍚庢湡鎵嶆悶鎸佺画闆嗘垚锛岃秺鏃╄秺濂姐€?

3. **鎶曡祫缂栬緫鍣ㄥ伐鍏?*锛氳姳 1 澶╂椂闂村啓涓€涓伐鍏凤紝鑳借妭鐪佸洟闃?100 澶╃殑鎵嬪姩鎿嶄綔銆?

4. **鏁版嵁椹卞姩璁捐**锛氱瓥鍒掕兘鍦?Excel 閲屾敼鐨勶紝灏变笉瑕佸啓姝诲湪浠ｇ爜閲屻€?

5. **鐩戞帶鍜屽弽棣?*锛氭病鏈夋暟鎹敮鎸佺殑浼樺寲閮芥槸鐩茬洰鐨勩€?

宸ュ叿閾炬病鏈夐摱寮癸紝鏍规嵁鍥㈤槦瑙勬ā鍜岄」鐩渶姹傜伒娲婚€夋嫨銆傚皬鍥㈤槦涓嶈杩囧害宸ョ▼鍖栵紝澶у洟闃熶笉瑕佸拷瑙嗗伐鍏锋姇璧勩€?

