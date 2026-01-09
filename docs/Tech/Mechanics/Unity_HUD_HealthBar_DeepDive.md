---
sidebarTitle: "馃└ Unity HUD & 琛€鏉＄郴缁熸渶浣冲疄璺?
---

# 馃└ Unity HUD & 琛€鏉＄郴缁熸渶浣冲疄璺?

鍦?RPG銆佸闃叉垨 Roguelike 娓告垙涓紝琛€鏉★紙Health Bar锛変笉浠呮槸鏁版嵁鏄剧ず锛屾洿鏄垬鏂楀弽棣堢殑鏍稿績銆?
鏈寚鍗楀皢娣卞叆鎺㈣涓夌涓嶅悓閲忕骇鐨勮鏉″疄鐜版柟妗堬紝浠ュ強濡備綍鍒朵綔鈥滄嫵鎷冲埌鑲夆€濈殑瑙嗚鍙嶉銆?

---

## 1. 鏋舵瀯閫夊瀷锛氫笁绉嶆祦娲剧殑鏉冭　

鍦ㄥ姩鎵嬪啓浠ｇ爜鍓嶏紝蹇呴』鏍规嵁娓告垙绫诲瀷閫夋嫨鏋舵瀯銆?

|          鏂规          |          瀹炵幇鏂瑰紡          |          浼樼偣          |          缂虹偣          |          閫傜敤鍦烘櫙          |
|          :---          |          :---          |          :---          |          :---          |          :---          |
|          **A. World Space Canvas**          |          姣忎釜鍗曚綅澶撮《鎸備竴涓?World Space 鐨?Canvas銆?         |          1. 寮€鍙戞瀬蹇?br>2. 鐗╃悊渚濋檮锛岃嚜甯﹂€忚缂╂斁          |          1. **鎬ц兘鏈€宸?* (姣忎釜 Canvas 閮芥槸鐙珛 DrawCall)<br />2. 杩滆窛绂荤湅涓嶆竻 (澶皬)          |          灏戦噺绮捐嫳鎬€佷富瑙掋€丅OSS          |
|          **B. Screen Space Mapping**          |          涓€涓叏灞?UI Canvas锛岄€氳繃鑴氭湰璁＄畻鍧愭爣璺熼殢 3D 鍗曚綅銆?         |          1. **鎬ц兘杈冨ソ** (UI 鍚堟壒)<br />2. 澶у皬鎭掑畾锛屾竻鏅伴攼鍒?br>3. 涓嶄細绌挎ā          |          1. 闇€瑕佹暟瀛﹁绠?(WorldToScreen)<br />2. 闇€瑕佸鐞嗛伄鎸″墧闄?         |          澶у鏁?RPG銆丮OBA (鑻遍泟鑱旂洘鏂瑰紡)          |
|          **C. GPU Instancing / Mesh**          |          涓嶄娇鐢?uGUI锛岀洿鎺ュ湪鎬殑妯″瀷涓婃柟鐢讳竴涓?Quad 闈㈢墖锛岀敤 Shader 鎺у埗杩涘害銆?         |          1. **鎬ц兘鏋佽嚧** (鏀寔娴烽噺鍗曚綅)<br />2. 0 GC          |          1. 鍒朵綔澶嶆潅 (闇€鍐?Shader)<br />2. 闅句互瀹炵幇澶嶆潅 UI 鍔ㄧ敾          |          **鍚歌楝煎垢瀛樿€呯被**銆佽秴澶氬崟浣嶅闃?         |

> 馃挕 **Vampirefall 寤鸿:** 
> *   **鏅€氭€墿:** 鏂规 B (瀵硅薄姹犵鐞?UI) 鎴?鏂规 C (濡傛灉鍚屽睆 > 200)銆?
> *   **涓昏/Boss:** 鏂规 B (涓轰簡鏇寸簿缁嗙殑 UI 鐗规晥)銆?

---

## 2. 鏍稿績瀹炶返锛歋creen Space Mapping (涓绘祦鏂规)

杩欐槸鏈€骞宠　鐨勬柟妗堛€傛垜浠娇鐢ㄤ竴涓粺涓€鐨?`HUD Manager` 鏉ョ鐞嗘墍鏈夎鏉°€?

### 2.1 鍩虹璺熼殢鑴氭湰 (鏃犳姈鍔ㄧ増)
鍏抽敭鐐瑰湪浜庝娇鐢?`LateUpdate` 骞跺湪鍧愭爣杞崲鏃跺鐞?Canvas 鐨勭缉鏀俱€?

```csharp
// 鎸傚湪 UI 琛€鏉￠鍒朵綋涓?
public class UI_HealthBar : MonoBehaviour {
    public Transform targetUnit;     // 杩借釜鐨?3D 鐩爣
    public Vector3 worldOffset = new Vector3(0, 2f, 0); // 澶撮《鍋忕Щ
    
    private RectTransform _rectTransform;
    private Canvas _parentCanvas;
    private Camera _mainCamera;

    void Awake() {
        _rectTransform = GetComponent<RectTransform>();
        _parentCanvas = GetComponentInParent<Canvas>();
        _mainCamera = Camera.main;
    }

    // 浣跨敤 LateUpdate 纭繚鍦ㄧ墿浣撶Щ鍔ㄥ悗鎵嶆洿鏂?UI锛岄伩鍏嶆姈鍔?
    void LateUpdate() {
        \text{if} (targetUnit == null) {
            Destroy(gameObject); // 鎴栧洖鏀惰繘瀵硅薄姹?
            return;
        }

        UpdatePosition();
    }

    void UpdatePosition() {
        // 1. 鎬ц兘浼樺寲锛氳閿ヤ綋鍓旈櫎
        // 濡傛灉鐗╀綋鍦ㄧ浉鏈鸿儗鍚庯紝鐩存帴闅愯棌 UI
        Vector3 viewportPos = _mainCamera.WorldToViewportPoint(targetUnit.position);
        bool isVisible = viewportPos.z > 0 && viewportPos.x > 0 && viewportPos.x \< 1 && viewportPos.y > 0 && viewportPos.y \< 1;
        
        // 绠€鍗曠殑鏄鹃殣鍒囨崲 (鍙互浣跨敤 CanvasGroup 鍋氭贰鍏ユ贰鍑?
        gameObject.SetActive(isVisible); 
        \text{if} (!isVisible) return;

        // 2. 鍧愭爣杞崲鏍稿績 (鍙傝€?RectTransform 娣卞害瑙ｆ瀽鏂囨。)
        Vector2 screenPos = _mainCamera.WorldToScreenPoint(targetUnit.position + worldOffset);
        
        Vector2 localPos;
        RectTransformUtility.ScreenPointToLocalPointInRectangle(
            _parentCanvas.transform as RectTransform,
            screenPos,
            _parentCanvas.renderMode == RenderMode.ScreenSpaceOverlay ? null : _mainCamera,
            out localPos
        );

        _rectTransform.anchoredPosition = localPos;
    }
}
```

---

## 3. 瑙嗚鎵撶（锛氬浣曞仛鍑衡€滄墦鍑绘劅鈥?(The Juice)

骞插反宸寸殑琛€鏉℃墸鍑忔槸娌℃湁鐏甸瓊鐨勩€傛垜浠渶瑕佲€滅紦鍐叉潯 (Damage Buffer)鈥濆拰鈥滄诞鍔ㄦ暟瀛椻€濄€?

### 3.1 鍙屽眰琛€鏉?(缂撳啿鍔ㄧ敾)
*   **鍓嶆櫙鏉?(Red):** 鐬棿鎵ｅ噺锛屼唬琛ㄥ綋鍓嶇湡瀹炶閲忋€?
*   **鑳屾櫙缂撳啿鏉?(Yellow/White):** 寤惰繜涓€灏忔鏃堕棿鍚庯紝骞虫粦鍑忓皯銆?
*   **鍘熺悊:** 鍒╃敤瑙嗚宸睍绀衡€滃垰鍒氬彈鍒颁簡澶氬皯浼ゅ鈥濄€?

```csharp
public class UI_HealthBar_Juice : MonoBehaviour {
    public Image healthFill;      // 鐪熷疄鐨勮鏉?(绾?
    public Image bufferFill;      // 缂撳啿鐨勮鏉?(榛?鐧?
    
    private float _targetFill = 1f;
    private float _bufferSpeed = 0.5f;
    private float _bufferDelay = 0.5f;
    private float _lastHitTime;

    public void OnDamage(float currentHp, float maxHp) {
        // 1. 鐬棿鏇存柊鐪熷疄琛€鏉?
        _targetFill = currentHp / maxHp;
        healthFill.fillAmount = _targetFill;
        
        // 2. 閲嶇疆缂撳啿璁℃椂鍣?
        _lastHitTime = Time.time;
        
        // 娉ㄦ剰: 杩欓噷涓嶆洿鏂?bufferFill锛岃瀹冩粸鍚?
    }

    void Update() {
        // 寤惰繜涓€娈垫椂闂村悗鍐嶅紑濮嬬缉鍑忕紦鍐叉潯
        \text{if} (Time.time > _lastHitTime + _bufferDelay) {
            \text{if} (bufferFill.fillAmount > _targetFill) {
                // 骞虫粦鎻掑€?(Lerp)
                bufferFill.fillAmount = Mathf.Lerp(bufferFill.fillAmount, _targetFill, Time.deltaTime * 5f);
                
                // 鎴栬€呭寑閫熷噺灏?(鏇村父瑙佷簬纭牳娓告垙)
                // bufferFill.fillAmount -= _bufferSpeed * Time.deltaTime;
            }
        }
    }
}
```

### 3.2 浼ゅ璺冲瓧 (Floating Text)
涓嶈鐩存帴 Instantiate锛佽繖浼氫骇鐢熷ぇ閲忓瀮鍦惧唴瀛?(GC)銆?

*   **鍏抽敭鎶€鏈?** 瀵硅薄姹?(Object Pooling)銆?
*   **杩愬姩杞ㄨ抗:** 
    *   **鏅€氫激瀹?** 鍚戜笂婕傛诞骞舵贰鍑恒€?
    *   **鏆村嚮 (Crit):** 瀛椾綋鍙樺ぇ + 闇囧姩 + 寮虹儓鐨勯鑹?(閲?绾?銆?
*   **甯冨眬:** 浣跨敤 `WorldToScreenPoint` 杞崲浣嶇疆锛屼絾鍦?UI 灞€閮ㄥ潗鏍囩郴涓仛鍔ㄧ敾銆?

---

## 4. 鎬ц兘榛戠鎶€锛欸PU Instancing 琛€鏉?(娴烽噺鍗曚綅涓撶敤)

褰撳睆骞曚笂鏈?500 涓晫浜烘椂锛孶GUI 鐨勫紑閿€锛圠ayout Rebuild + DrawCall锛夊皢鏃犳硶鎵垮彈銆傛鏃跺簲鏀惧純 UGUI銆?

### 4.1 鍘熺悊
1.  鍦ㄦ瘡涓晫浜烘ā鍨嬪ご椤舵斁涓€涓瀬绠€鍗曠殑 `Quad` (闈㈢墖) 鎴?`SpriteRenderer`銆?
2.  浣跨敤鏀寔 **GPU Instancing** 鐨?Shader銆?

3.  浣跨敤 `MaterialPropertyBlock` 淇敼鍗曚釜琛€鏉＄殑杩涘害锛岃€屼笉鏄?`material.SetFloat` (鍚庤€呬細鐮村潖鍚堟壒锛屽鑷?500 涓?DrawCall)銆?

### 4.2 浠ｇ爜瀹炵幇鐗囨

```csharp
// 鎸傚湪鏁屼汉韬笂锛屾帶鍒跺ご椤剁殑 MeshRenderer
public class GPU_HealthBar : MonoBehaviour {
    public MeshRenderer barRenderer;
    
    // 闈欐€佸彉閲忥紝閬垮厤閲嶅鍒涘缓
    private static MaterialPropertyBlock _propBlock;
    private static readonly int _FillPropId = Shader.PropertyToID("_Fill");

    void Awake() {
        \text{if} (_propBlock == null) _propBlock = new MaterialPropertyBlock();
    }

    public void UpdateHealth(float pct) {
        // 鑾峰彇褰撳墠鐨勫睘鎬у潡
        barRenderer.GetPropertyBlock(_propBlock);
        
        // 淇敼鍊?
        _propBlock.SetFloat(_FillPropId, pct);
        
        // 搴旂敤鍥炲幓 (杩欎竴姝ヤ笉浼氱牬鍧?GPU Instancing)
        barRenderer.SetPropertyBlock(_propBlock);
    }
}
```

### 4.3 Shader 绠€杩?(HLSL)
浣犻渶瑕佸啓涓€涓畝鍗曠殑 Shader锛屾帴鍙?`_Fill` 鍙傛暟銆?
```hlsl
// Fragment Shader 鐗囨
fixed4 frag (v2f i) : SV_Target {
    // i.uv.x 鏄?0~1 鐨勬í鍚戝潗鏍?
    // _Fill 鏄綋鍓嶈閲忕櫨鍒嗘瘮
    
    // 濡傛灉褰撳墠鍍忕礌浣嶇疆 > 琛€閲忔瘮渚嬶紝鏄剧ず鑳屾櫙鑹?榛?锛屽惁鍒欐樉绀鸿鏉¤壊(绾?
    fixed4 col = i.uv.x > _Fill ? _BackgroundColor : _ForegroundColor;
    return col;
}
```

---

## 5. 鎬荤粨锛氭渶浣冲疄璺垫鏌ユ竻鍗?

1.  **姘歌繙涓嶈** 鍦?Update 涓敤 `GetComponent` 鎴?`Find`銆?
2.  **浜嬩欢椹卞姩:** 琛€鏉¤剼鏈簲璇ヨ闃?`HealthChanged` 浜嬩欢锛岃€屼笉鏄瘡甯у幓鏌?`player.currentHp`銆?

3.  **鍙鎬т紭鍖?** 灞忓箷澶栫殑琛€鏉?*鍋滄鏇存柊浣嶇疆**锛岀敋鑷崇洿鎺?Disable銆?

4.  **灞傜骇绠＄悊:** 琛€鏉″簲璇ュ湪鎵€鏈?3D 鐗╀綋涔嬩笂锛屼絾鍦ㄥ叏灞?UI (濡傛殏鍋滆彍鍗? 涔嬩笅銆傞€氬父璁剧疆 Canvas 鐨?`Sort Order`銆?

5.  **鏁存暟瀵归綈:** 濡傛灉浣跨敤鍍忕礌椋?UI锛岀‘淇濆潗鏍?`RoundToInt`锛屽惁鍒欒鏉¤竟缂樹細妯＄硦銆?

