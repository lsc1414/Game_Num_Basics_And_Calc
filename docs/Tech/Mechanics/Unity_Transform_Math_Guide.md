---
sidebarTitle: "馃搻 Unity Transform 鏁板鍙樻崲涓庢渶浣冲疄璺?
---

# 馃搻 Unity Transform 鏁板鍙樻崲涓庢渶浣冲疄璺?

Transform 鏄?Unity 涓渶鍩虹涔熸渶閲嶈鐨勭粍浠讹紝瀹冨畾涔変簡鐗╀綋鍦ㄧ┖闂翠腑鐨?*浣嶇疆 (Position)**銆?*鏃嬭浆 (Rotation)** 鍜?**缂╂斁 (Scale)**銆傛繁鍒荤悊瑙ｅ叾鑳屽悗鐨勭嚎鎬т唬鏁板師鐞嗭紝瀵逛簬缂栧啓楂樻€ц兘銆佹棤 Bug 鐨勪唬鐮佽嚦鍏抽噸瑕併€?

---

## 1. 鍧愭爣绌洪棿 (Coordinate Spaces)

Unity 涓瓨鍦ㄥ涓祵濂楃殑鍧愭爣绯伙紝鐞嗚В瀹冧滑涔嬮棿鐨勮浆鎹㈡槸鎵€鏈夊彉鎹㈢殑鍩虹銆?

### 1.1 甯哥敤绌洪棿

- **妯″瀷绌洪棿 (Local/Object Space):** 椤剁偣鐩稿浜庢ā鍨嬫灑杞寸偣 (Pivot) 鐨勪綅缃€?
- **涓栫晫绌洪棿 (World/Global Space):** 鐩稿浜庢父鎴忎笘鐣屽師鐐?(0,0,0) 鐨勪綅缃€?
- **瑙傚療绌洪棿 (View/Camera Space):** 鐩稿浜庢憚鍍忔満鐨勪綅缃€?
- **灞忓箷绌洪棿 (Screen Space):** 鍍忕礌鍧愭爣 (x, y)锛屽乏涓嬭涓?(0,0)銆?
- **瑙嗗彛绌洪棿 (Viewport Space):** 褰掍竴鍖栧睆骞曞潗鏍?(0~1)銆?

### 1.2 鍙樻崲鐭╅樀 (Transformation Matrix)

涓€涓墿浣撲粠妯″瀷绌洪棿鍙樻崲鍒颁笘鐣岀┖闂达紝鏈川涓婃槸涔樹互涓€涓?$4 \times 4$鐭╅樀$M_{Local \to World}$銆?

$$M = T \cdot R \cdot S$$

- **椤哄簭鑷冲叧閲嶈:** 鍏堢缉鏀?($S$)锛屽啀鏃嬭浆 ($R$)锛屾渶鍚庡钩绉?($T$)銆?
- **鐭╅樀涔樻硶涓嶆弧瓒充氦鎹㈠緥:** $R \cdot T \neq T \cdot R$銆傚鏋滈『搴忛敊浜嗭紝鐗╀綋浼氱粫鐫€涓栫晫鍘熺偣鏃嬭浆锛岃€屼笉鏄粫鐫€鑷韩鏃嬭浆銆?

---

## 2. 鏃嬭浆 (Rotation) 鈥斺€?鏈€澶х殑鍧?

Unity 鎻愪緵浜嗕笁绉嶆柟寮忔潵琛ㄧず鏃嬭浆锛屾贩鐢ㄥ畠浠槸 Bug 涔嬫簮銆?

### 2.1 娆ф媺瑙?(Euler Angles) - `transform.eulerAngles`

- **鐩磋:** (x, y, z) 鍒嗗埆浠ｈ〃缁?X, Y, Z 杞存棆杞殑瑙掑害銆?
- **浼樼偣:** 浜虹被鏄撹锛孖nspector 闈㈡澘閲屾樉绀虹殑灏辨槸杩欎釜銆?
- **鑷村懡缂虹偣:** **涓囧悜鑺傛閿?(Gimbal Lock)**銆傚綋涓棿杞?(Y) 鏃嬭浆 90 搴︽椂锛孹 杞村拰 Z 杞撮噸鍚堬紝澶卞幓涓€涓嚜鐢卞害銆?
- **鏈€浣冲疄璺?** 浠呭湪 UI 鏄剧ず鎴栫畝鍗曠殑鍒濆鍖栬缃椂浣跨敤銆?*涓ョ**鍦?Update 涓娆ф媺瑙掕繘琛岀疮鍔犺绠楋紙濡?`angles += speed * dt`锛夈€?

### 2.2 鍥涘厓鏁?(Quaternion) - `transform.rotation`

- **鍘熺悊:** 澶嶆暟鎵╁睍 $(x, y, z, w)$銆?
- **浼樼偣:** 鏃犳閿侊紝鎻掑€煎钩婊?(Slerp)锛岃绠楁晥鐜囬珮銆?
- **缂虹偣:** 浜虹被鏃犳硶鐩磋鐞嗚В鏁板€煎惈涔夈€?
- **甯哥敤 API:**
  - `Quaternion.Identity`: 鏃犳棆杞€?
  - `Quaternion.Euler(x, y, z)`: 娆ф媺瑙?-> 鍥涘厓鏁般€?
  - `Quaternion.LookRotation(forward, up)`: 鍒涘缓涓€涓湞鍚?`forward` 鐨勬棆杞€?
  - `Quaternion.Angle(q1, q2)`: 璁＄畻涓や釜鏃嬭浆闂寸殑澶硅銆?

### 2.3 鐭╅樀/鍚戦噺娉?(Vector Math)

- **forward/up/right:** 鐩存帴鎿嶄綔杞村悜閲忋€?
- **搴旂敤:** `transform.forward` 鏈川涓婃槸 `rotation * Vector3.forward`銆?

---

## 3. 绌洪棿鍙樻崲 API 璇﹁В

### 3.1 鐐广€佸悜閲忎笌鏂瑰悜鐨勫尯鍒?

- **Point (鐐?:** 鍙椾綅缃€佹棆杞€佺缉鏀惧奖鍝嶃€?
  - `TransformPoint()`: Local -> World
  - `InverseTransformPoint()`: World -> Local
- **Direction (鏂瑰悜):** **涓嶅彈浣嶇疆 (Translation) 褰卞搷**锛屽彈鏃嬭浆褰卞搷銆傞€氬父鐢ㄤ簬娉曠嚎銆侀€熷害鏂瑰悜銆?
  - `TransformDirection()`: Local -> World
  - `InverseTransformDirection()`: World -> Local
- **Vector (鍚戦噺):** 鍙楁棆杞拰**缂╂斁**褰卞搷锛屼笉鍙椾綅缃奖鍝嶃€?
  - `TransformVector()`: Local -> World (甯︾缉鏀?

### 3.3 鐗瑰埆绡囷細UI 鍧愭爣绯昏浆鎹?(The UI Coordinate Problem)

UI 绯荤粺 (`RectTransform`) 铏界劧缁ф壙鑷?Transform锛屼絾鍦ㄥ潗鏍囪浆鎹笂鏈変竴涓法澶х殑鈥滄柇灞傗€濓細**娓叉煋妯″紡 (Render Mode)**銆?

1.  **Screen Space - Overlay:**

    - UI 鐩存帴缁樺埗鍦ㄥ睆骞曟渶涓婂眰銆?
    - **娌℃湁涓栫晫鍧愭爣姒傚康**锛堟垨鑰呰锛屼笘鐣屽潗鏍?= 灞忓箷鍍忕礌鍧愭爣锛夈€?
    - `position.x` 灏辨槸灞忓箷涓婄殑鍍忕礌 X銆?
    - 杞崲鏃?*涓嶉渶瑕?* Camera 鍙傛暟 (浼?`null`)銆?

2.  **Screen Space - Camera / World Space:**

    - UI 鏄?3D 涓栫晫涓殑瀹炰綋鏉垮瓙锛屾湁纭畾鐨勬繁搴?(Z)銆?
    - 鍙楅€忚 (Perspective) 褰卞搷锛氳繎澶ц繙灏忋€?
    - 杞崲鏃?*蹇呴』**浼犲叆娓叉煋璇?Canvas 鐨?Camera锛屽惁鍒欏皠绾挎娴嬩細鍋忕銆?

**鏍稿績鐞嗚:**
鍦ㄥ鐞?UI 浜や簰锛堝榧犳爣鐐瑰嚮銆佺墿浣撻鍚?UI锛夋椂锛屾案杩滀笉瑕佽瘯鍥剧洿鎺モ€滃姞鍑忓潗鏍団€濄€傚繀椤诲鎵句竴涓?*鍏叡鍙傝€冪郴**鈥斺€旈€氬父鏄?*灞忓箷绌洪棿 (Screen Space)**銆?

- 3D 涓栫晫 -> **灞忓箷** \<- UI 灞€閮?
- UI A -> **灞忓箷** \<- UI B

---

### 3.2 鏈€浣冲疄璺垫渚?

#### 妗堜緥 A: 瀛愬脊鍙戝皠浣嶇疆

**閿欒:** `bullet.position = transform.position + new Vector3(0, 0, 1);`  
**闂:** 鍙湁褰撶墿浣撴湞鍚戜笘鐣?Z 杞翠笖鏃犵缉鏀炬椂鎵嶅銆? 
**姝ｇ‘:** `bullet.position = transform.TransformPoint(new Vector3(0, 0, 1));`  
**鎴栬€?** `bullet.position = transform.position + transform.forward * 1.0f;`

#### 妗堜緥 B: AI 鐩稿鍧愭爣鍒ゆ柇

鍒ゆ柇 "鏁屼汉鏄惁鍦ㄦ垜鐨勫彸鍓嶆柟"銆?
**鏂规硶:** 灏嗘晫浜哄潗鏍囪浆鎹㈠埌鎴戠殑灞€閮ㄧ┖闂淬€?

```csharp
Vector3 localPos = transform.InverseTransformPoint(enemy.position);
if (localPos.z > 0 && localPos.x > 0) {
    // 鍦ㄥ彸鍓嶆柟 (Local Z鏄墠, Local X鏄彸)
}
```

#### 妗堜緥 C: 鐩稿鏂瑰悜鐨勫姏 (Relative Force)

涓€涓墿浣撳悜鍓嶅彂灏勪竴涓姏锛堜緥濡傜帺瀹跺啿鍒猴紝鍐插埡鏂瑰悜鏄鑹查潰鍚戠殑鏂瑰悜锛夈€?

```csharp
// 閿欒: 浼氫竴鐩存湞鐫€涓栫晫Z杞存柟鍚戝啿鍒?
// rigidbody.AddForce(Vector3.forward * speed);

// 姝ｇ‘: 鏈濈潃鐗╀綋鐨勬湰鍦癴orward鏂瑰悜鍐插埡
rigidbody.AddForce(transform.forward * speed, ForceMode.Impulse);
```

#### 妗堜緥 D: 鏃嬭浆闄愬埗 (Rotation Constraint)

渚嬪锛屾憚鍍忔満缁曠潃鐜╁鏃嬭浆锛屼絾瑕佷繚鎸佹憚鍍忔満 Y 杞村缁堟寚鍚戜笘鐣?Y 杞达紙涓嶅€炬枩锛夈€?

```csharp
// 閿欒: 绠€鍗昄ookAt浼氫娇鎽勫儚鏈篫杞存寚鍚戠帺瀹讹紝浣嗗彲鑳戒細鍊炬枩
// transform.LookAt(player.position);

// 姝ｇ‘: 鍒涘缓涓€涓彧鍦╕杞存棆杞殑LookRotation
Vector3 directionToPlayer = player.position - transform.position;
Quaternion targetRotation = Quaternion.LookRotation(directionToPlayer, Vector3.up); // Vector3.up 寮哄埗Y杞村悜涓?
transform.rotation = Quaternion.Slerp(transform.rotation, targetRotation, Time.deltaTime * rotationSpeed);
```

#### 妗堜緥 E: 灞忓箷鍧愭爣鍒颁笘鐣屽潗鏍?(Screen to World)

渚嬪锛岀偣鍑诲睆骞曞彂灏勫皠绾挎垨鐢熸垚鐗╀綋銆?

```csharp
// 1. 榧犳爣鐐瑰嚮鐨勫睆骞曞潗鏍?
Vector3 screenPos = Input.mousePosition;

// 2. 杞崲涓轰笘鐣屽潗鏍?(闇€瑕佹繁搴?
// 濡傛灉宸茬煡Z杞磋窛绂伙細
Vector3 worldPos = Camera.main.ScreenToWorldPoint(new Vector3(screenPos.x, screenPos.y, distanceToCamera));

// 濡傛灉闇€瑕佸皠绾挎娴?(鏇村父瑙?:
Ray ray = Camera.main.ScreenPointToRay(screenPos);
if (Physics.Raycast(ray, out RaycastHit hit)) {
    Debug.Log("Clicked at world position: " + hit.point);
    // 鍦?hit.point 浣嶇疆鐢熸垚鐗╀綋
}
```

#### 妗堜緥 F: 缁曠偣鏃嬭浆 (Rotate Around Point)

璁╀竴涓墿浣擄紙濡傚崼鏄熴€佸儦鏈猴級缁曠潃鍙︿竴涓偣锛堝琛屾槦銆佺帺瀹讹級鏃嬭浆銆?

```csharp
// 鍋囪 this.transform 鏄崼鏄燂紝targetTransform 鏄鏄?
// point: 鏃嬭浆鐨勪腑蹇冪偣
Vector3 point = targetTransform.position;
// axis: 鏃嬭浆杞?(閫氬父鏄疺ector3.up锛屽嵆缁昚杞?
Vector3 axis = Vector3.up;
// angle: 姣忓抚鏃嬭浆鐨勮搴?
float rotationSpeed = 50f; // 搴?绉?
float angle = rotationSpeed * Time.deltaTime;

transform.RotateAround(point, axis, angle);
```

#### 妗堜緥 G: 骞虫粦 LookAt (Smooth LookAt)

璁╃墿浣撳钩婊戝湴杞悜鐩爣锛岃€屼笉鏄灛鏃舵棆杞€傝繖瀵逛簬鎽勫儚鏈鸿窡闅忋€佺偖濉旇浆鍔ㄧ瓑鍦烘櫙闈炲父閲嶈銆?

```csharp
// 鍋囪 target 鏄鐪嬪悜鐨勭洰鏍?
Vector3 directionToTarget = target.position - transform.position;
// 璁＄畻鐩爣鏃嬭浆锛屽己鍒跺彧鍦╕杞存棆杞紝閬垮厤X/Z杞村€炬枩
Quaternion targetRotation = Quaternion.LookRotation(directionToTarget, Vector3.up);

// 浣跨敤 Slerp (鐞冮潰绾挎€ф彃鍊? 鎴?RotateTowards 骞虫粦杩囨浮
float rotationSpeed = 5f; // 鏃嬭浆閫熷害
transform.rotation = Quaternion.Slerp(transform.rotation, targetRotation, Time.deltaTime * rotationSpeed);

// 鎴栬€呬娇鐢?RotateTowards (鏇寸簿纭帶鍒舵渶澶ц浆瑙?
// float maxDegreesDelta = rotationSpeed * Time.deltaTime * 100f; // 鍋囪姣忕杞?00搴?
// transform.rotation = Quaternion.RotateTowards(transform.rotation, targetRotation, maxDegreesDelta);
```

#### 妗堜緥 H: 骞虫粦绉诲姩 (Smooth Movement)

璁╃墿浣撳钩婊戝湴绉诲姩鍒扮洰鏍囦綅缃€?

```csharp
// 鍋囪 targetPos 鏄绉诲姩鍒扮殑鐩爣浣嶇疆
Vector3 targetPos = new Vector3(10, 0, 0);
float moveSpeed = 5f; // 绉诲姩閫熷害

// MoveTowards: 浠ユ亽瀹氶€熷害绉诲姩鍒扮洰鏍囷紝涓嶄細瓒呰繃鐩爣
transform.position = Vector3.MoveTowards(transform.position, targetPos, moveSpeed * Time.deltaTime);

// Lerp (绾挎€ф彃鍊?: 姣忔绉诲姩鐩爣鍜屽綋鍓嶄綅缃箣闂寸殑涓€閮ㄥ垎锛岃秺鎺ヨ繎鐩爣瓒婃參
// float lerpFactor = 0.1f; // 姣忔绉诲姩褰撳墠璺濈鐨?0%
// transform.position = Vector3.Lerp(transform.position, targetPos, lerpFactor);
```

#### 妗堜緥 I: 3D 鐗╀綋椋炲悜 UI (World Object to UI Fly Effect) - 杩涢樁鐗?

缁忓吀闇€姹傦細鎬墿鎺夎惤閲戝竵锛堜笘鐣屽潗鏍囷級锛岄噾甯佹嬀鍙栧悗椋炲悜 UI 涓婄殑閲戝竵鏍忥紙灞忓箷鍧愭爣锛夈€?
**鍒濈骇闄烽槺:** 鐩存帴鐢?`position` 璧嬪€硷紝鍦ㄤ笉鍚屽垎杈ㄧ巼鎴?UI 閿氱偣璁剧疆涓嬩細鍋忕Щ銆? 
**鏍稿績鍘熺悊:** 浣跨敤 `RectTransformUtility` 灏嗗睆骞曞潗鏍囪浆鎹负**灞€閮?UI 鍧愭爣**銆?

```csharp
// 鍦烘櫙鍋囪锛?
// 1. worldCoin: 鎺夎惤鍦ㄥ湴涓婄殑閲戝竵 (3D)
// 2. uiGoldIcon: UI涓婄殑閲戝竵鍥炬爣 (RectTransform, 鍙兘鏈夊悇绉?Anchor 璁剧疆)
// 3. uiCoinPrefab: 椋炶鐗规晥棰勫埗浣?(UI鍏冪礌)
// 4. effectsCanvas: 涓撻棬鐢ㄤ簬鎾斁鐗规晥鐨?Canvas (Overlay 鎴?Camera 妯″紡)

public void PlayCoinFlyEffect(Transform worldCoin) {
    // --- 绗竴姝ワ細纭畾璧风偣 (World -> Screen -> Local UI) ---
    Vector3 screenPos = Camera.main.WorldToScreenPoint(worldCoin.position);

    // 灏嗗睆骞曞潗鏍囪浆鎹负 effectsCanvas 涓嬬殑灞€閮ㄥ潗鏍?
    // 杩欐牱鏃犺 Canvas 缂╂斁妯″紡濡備綍锛岄兘鑳戒繚璇佷綅缃纭?
    RectTransformUtility.ScreenPointToLocalPointInRectangle(
        (RectTransform)effectsCanvas.transform,
        screenPos,
        effectsCanvas.worldCamera, // 濡傛灉鏄?Overlay 妯″紡锛岃繖閲屼紶 null
        out Vector2 startLocalPos
    );

    // --- 绗簩姝ワ細纭畾缁堢偣 (Target UI -> Screen -> Local UI) ---
    // 鍗充娇 uiGoldIcon 鍦ㄥ彟涓€涓?Canvas 涓旀湁澶嶆潅鐨勯敋鐐癸紝
    // 鎴戜滑涔熷厛杞垚閫氱敤鐨勫睆骞曞潗鏍囷紝鍐嶈浆鍥?effectsCanvas 鐨勫眬閮ㄥ潗鏍?

    // 1. 鑾峰彇鐩爣鍦ㄥ睆骞曚笂鐨勭粷瀵逛綅缃?(澶勭悊璺?Canvas 鐨勫叧閿?
    // 娉ㄦ剰: 濡傛灉鐩爣 UI 鏄?Overlay 妯″紡锛寃orldCamera 浼?null
    Vector3 targetWorldPos = uiGoldIcon.position;
    Vector2 targetScreenPos = RectTransformUtility.WorldToScreenPoint(
        uiGoldIconCanvas.worldCamera,
        targetWorldPos
    );

    // 2. 杞洖鐗规晥灞傜殑灞€閮ㄥ潗鏍?
    RectTransformUtility.ScreenPointToLocalPointInRectangle(
        (RectTransform)effectsCanvas.transform,
        targetScreenPos,
        effectsCanvas.worldCamera,
        out Vector2 endLocalPos
    );

    // --- 绗笁姝ワ細鐢熸垚骞堕琛?---
    GameObject flyingCoin = Instantiate(uiCoinPrefab, effectsCanvas.transform);
    RectTransform flyRect = flyingCoin.GetComponent<RectTransform>();

    // 閲嶈: 閲嶇疆閿氱偣涓轰腑蹇冿紝閬垮厤鐖剁骇閿氱偣褰卞搷
    flyRect.anchoredPosition = startLocalPos;
    flyRect.anchorMin = new Vector2(0.5f, 0.5f);
    flyRect.anchorMax = new Vector2(0.5f, 0.5f);
    flyRect.pivot = new Vector2(0.5f, 0.5f);

    StartCoroutine(FlyToTarget(flyRect, endLocalPos));
}

IEnumerator FlyToTarget(RectTransform coin, Vector2 targetPos) {
    // 浣跨敤 anchoredPosition 杩涜绉诲姩锛屼繚璇佸湪 UI 鍧愭爣绯诲唴鐨勬纭€?
    float duration = 0.6f;
    float elapsed = 0;
    Vector2 startPos = coin.anchoredPosition;

    while (elapsed \< duration) {
        elapsed += Time.deltaTime;
        float t = elapsed / duration;
        t = t * t * (3f - 2f * t); // SmoothStep

        coin.anchoredPosition = Vector2.Lerp(startPos, targetPos, t);
        yield return null;
    }

    Destroy(coin.gameObject);
    // AddGold();
}
```

**鎬荤粨:** 瑙ｅ喅 UI 鍧愭爣涔遍鐨勭粓鏋佹硶瀹濇槸 **"灞忓箷鍧愭爣 (Screen Point)" 浣滀负涓浆绔?*锛岄厤鍚?`RectTransformUtility.ScreenPointToLocalPointInRectangle`銆?

> 馃挕 **娣卞叆瀛︿範 UI 鏁板:** 鍏充簬 Anchors銆丳ivot銆丼izeDelta 鐨勬繁灞傚師鐞嗗強鏇村 UI 閫傞厤鎶€宸э紝璇峰弬闃呬笓闂ㄦ枃妗ｏ細
> **[Unity RectTransform 娣卞害瑙ｆ瀽 (The Math of UI)](./Unity_RectTransform_DeepDive.md)**

---

## 4. 鏍稿績鍚戦噺鏁板涓庡嚑浣曠洿瑙?(Vector Math Intuition)

鍦?Gameplay 缂栫▼涓紝鐞嗚В鍚戦噺鐨勭偣涔樺拰鍙変箻姣旇浣忓叕寮忔洿閲嶈銆傚畠浠槸鎴樻枟閫昏緫锛堝瑙嗛噹銆佸垽瀹氾級鐨勬暟瀛﹀熀鐭炽€?

### 4.1 鐐圭Н (Dot Product) - `Vector3.Dot(A, B)`

- **鏁板瀹氫箟:** $|A||B|\cos\theta$
- **鍑犱綍鎰忎箟:** 琛￠噺涓や釜鍚戦噺鐨勬柟鍚?*鐩镐技绋嬪害**锛屾垨鑰呭悜閲?A 鍦ㄥ悜閲?B 涓婄殑**鎶曞奖闀垮害**銆?
- **搴旂敤鍦烘櫙:**

  1.  **瑙嗛噹妫€娴?(FOV):** 鍒ゆ柇鏁屼汉鏄惁鍦ㄧ帺瀹跺墠鏂瑰す瑙掑唴銆?

      ```csharp
      Vector3 toEnemy = (enemy.position - transform.position).normalized;
      // Dot > 0.5f 澶х害鎰忓懗鐫€鍦ㄥ墠鏂?60搴﹁寖鍥村唴 (cos(60)=0.5)
      // Dot > 0 鍦ㄥ墠鏂?180搴﹁寖鍥村唴
      if (Vector3.Dot(transform.forward, toEnemy) > 0.5f) { /* 鍦ㄨ閲庡唴 */ }
      ```

  2.  **鑳屽埡鍒ゅ畾 (Backstab):** 鍒ゆ柇鏀诲嚮鏄惁鏉ヨ嚜鏁屼汉鑳屽悗銆?

      - 濡傛灉 `Dot(enemy.forward, player.forward) > 0.8`锛岃鏄庝袱浜烘湞鍚戝熀鏈竴鑷达紝鏄儗鍚庢敾鍑汇€?

  3.  **鍏夌収璁＄畻:** 婕弽灏勮绠椾腑锛屽厜绾挎柟鍚戜笌娉曠嚎鐨勭偣绉喅瀹氫寒搴︺€?

### 4.2 鍙夌Н (Cross Product) - `Vector3.Cross(A, B)`

- **鏁板瀹氫箟:** 鐢熸垚涓€涓悓鏃跺瀭鐩翠簬 A 鍜?B 鐨勬柊鍚戦噺锛堟硶鍚戦噺锛夈€傞伒瀹堝彸鎵嬪畾鍒欍€?
- **鍑犱綍鎰忎箟:** 纭畾涓や釜鍚戦噺鏋勬垚鐨?*骞抽潰**鍙婂叾**娉曠嚎**銆?
- **搴旂敤鍦烘櫙:**

  1.  **宸﹀彸鍒ゆ柇:** 鍒ゆ柇鏁屼汉鍦ㄦ垜鐨勫乏杈硅繕鏄彸杈广€?

      ```csharp
      Vector3 toEnemy = enemy.position - transform.position;
      Vector3 cross = Vector3.Cross(transform.forward, toEnemy);
      // 鍦?Unity (宸︽墜鍧愭爣绯? 涓?
      // cross.y > 0閫氬父鍦ㄥ彸渚? cross.y \< 0鍦ㄥ乏渚?(鍙栧喅浜庡叿浣撹酱鍚戣瀹?
      ```

  2.  **鏋勫缓鍧愭爣绯?** 宸茬煡 Forward 鍜?Up锛屾眰 Right銆?

      - `Right = Cross(Up, Forward)` (娉ㄦ剰椤哄簭褰卞搷鏂瑰悜)

---

## 5. 鐭╅樀鐨勨€滃熀鍚戦噺鈥濊瑙?(Basis Vectors)

涓嶈鎶婂彉鎹㈢煩闃电湅浣滀竴鍫嗘灟鐕ョ殑鏁板瓧銆?x4 鐭╅樀鐨勫墠涓夊垪锛屽疄闄呬笂灏辨槸璇ョ墿浣撳眬閮ㄥ潗鏍囪酱鍦?*涓栫晫绌洪棿**涓殑琛ㄧず銆?

$$

\begin{bmatrix}
\color{red}{R_x} & \color{green}{U_x} & \color{blue}{F_x} & T_x \\
\color{red}{R_y} & \color{green}{U_y} & \color{blue}{F_y} & T_y \\
\color{red}{R_z} & \color{green}{U_z} & \color{blue}{F_z} & T_z \\
0 & 0 & 0 & 1
\end{bmatrix}


$$

- **绗竴鍒?(Red):** 鐗╀綋鐨?`transform.right` (灞€閮?X 杞?
- **绗簩鍒?(Green):** 鐗╀綋鐨?`transform.up` (灞€閮?Y 杞?
- **绗笁鍒?(Blue):** 鐗╀綋鐨?`transform.forward` (灞€閮?Z 杞?
- **绗洓鍒?** 鐗╀綋鐨?`transform.position` (浣嶇Щ)

**娣卞埢鐞嗚В:** 鏃嬭浆涓€涓墿浣擄紝鏈川涓婂氨鏄畾涔夎繖涓変釜鍩哄悜閲忥紙Right, Up, Forward锛夋寚鍚戝摢閲屻€?

---

## 6. 鐗╃悊涓庡彉鎹㈢殑鍐茬獊 (Physics vs Transform)

杩欐槸涓€涓瀬鏄撹蹇借鐨勭悊璁洪櫡闃便€?

- **鐜拌薄:** 鐩存帴淇敼甯?`Rigidbody` 鎴?`Collider` 鐗╀綋鐨?`transform.position`銆?
- **鐞嗚鍚庢灉 (Teleportation):**
  - 鐗╃悊寮曟搸璁や负鐗╀綋鏄?*鐬Щ**杩囧幓鐨勶紝閫熷害涓?0銆?
  - **绌垮 (Tunneling):** 杩欎竴甯у湪澧欏墠锛屼笅涓€甯у湪澧欏悗锛屼腑闂存病鏈夋娴嬪埌纰版挒銆?
  - **鐮村潖鎻掑€?** 瀵艰嚧鍒氫綋杩愬姩鍗￠】鎴栨姈鍔ㄣ€?
- **姝ｇ‘鍋氭硶:**
  - **鐬Щ:** 浣跨敤 `rigidbody.position = newPos` (绫讳技 transform 浣嗛€氱煡鐗╃悊寮曟搸)銆?
  - **绉诲姩:** 浣跨敤 `rigidbody.MovePosition(newPos)` (骞虫粦绉诲姩锛屼細涓庢部閫旂墿浣撶鎾?銆?
  - **鏂藉姏:** 浣跨敤 `rigidbody.AddForce()`銆?

---

## 7. 灞傜骇鍏崇郴 (Hierarchy) 涓庢€ц兘

### 7.1 鑲剰鏍囪 (Dirty Flag)

Unity 鐨?Transform 绯荤粺浣跨敤鈥滆偖鑴忔爣璁扳€濇ā寮忋€?

- 褰撲綘淇敼鐖剁墿浣撶殑 Transform 鏃讹紝鎵€鏈夊瓙鐗╀綋骞朵笉浼氱珛鍗抽噸鏂拌绠椾笘鐣屽潗鏍囥€?
- 瀹冧滑浼氳鏍囪涓?`Dirty`銆?
- 鍙湁褰撲綘涓嬫璁块棶瀛愮墿浣撶殑 `.position` 鎴?`.rotation` 鏃讹紝鎵嶄細瑙﹀彂閫掑綊璁＄畻 (Recursion)銆?

### 7.2 鎬ц兘闄烽槺

- **娣卞害灞傜骇:** 灞傜骇瓒婃繁锛岃绠楀紑閿€瓒婂ぇ銆?
- **棰戠箒璇诲啓:** 鍦ㄤ竴甯у唴鍙嶅璇诲彇 `position` 浼氬己鍒堕噸绠椼€?
  - _Bad:_ `for(i) { x += transform.position.x; }`
  - _Good:_ `Vector3 pos = transform.position; for(i) { x += pos.x; }`
- **缂╂斁 (Scale):** 灏介噺淇濇寔 Scale 涓?(1,1,1)銆傞潪缁熶竴缂╂斁 (Non-uniform scale) 浼氬鑷寸墿鐞嗗紩鎿庤绠楀鏉傚寲锛屽苟鐮村潖鎵瑰鐞?(Batching)銆?

### 7.3 `transform.hasChanged`

- **鐢ㄩ€?** 鏋佸叾楂樻晥鍦版鏌ョ墿浣撹嚜涓婁竴甯т互鏉ユ槸鍚︾Щ鍔ㄨ繃銆?
- **鍦烘櫙:** 鍙湁褰撶墿浣撶Щ鍔ㄦ椂锛屾墠鏇存柊绌洪棿绱㈠紩 (Grid/QuadTree)銆?
  ```csharp
  if (transform.hasChanged) {
      UpdateSpatialGrid();
      transform.hasChanged = false; // 蹇呴』鎵嬪姩閲嶇疆
  }
  ```

---

## 8. 鏁板鍙樻崲閫熸煡琛?(Cheat Sheet)

| 闇€姹?                          | 鍏紡/API                                                                      |
| :----------------------------- | :---------------------------------------------------------------------------- |
| **鐗╀綋 A 鏈濆悜鐗╀綋 B**          | `transform.rotation = Quaternion.LookRotation(B.pos - A.pos);`                |
| **骞虫粦鏃嬭浆鍚戠洰鏍?*             | `transform.rotation = Quaternion.RotateTowards(current, target, speed * dt);` |
| **鑾峰彇 B 鍦?A 鍧愭爣绯讳笅鐨勪綅缃?* | `Vector3 localPos = A.InverseTransformPoint(B.position);`                     |
| **缁曟煇涓偣 P 鏃嬭浆**            | `transform.RotateAround(P, axis, angle);`                                     |
| **璁＄畻璺濈 (涓嶅紑鏂?**          | `(A - B).sqrMagnitude` (鐢ㄤ簬姣旇緝璺濈锛屾€ц兘浼樹簬 `.distance`)                   |
| **灏嗗悜閲忔姇褰卞埌骞抽潰**           | `Vector3.ProjectOnPlane(vector, planeNormal);`                                |
| **鍚戦噺鍙嶅皠 (瀛愬脊鍙嶅脊)**        | `Vector3.Reflect(velocity, wallNormal);`                                      |
| **妫€鏌ユ槸鍚﹀湪鍓嶆柟 (瑙嗛噹)**      | `Vector3.Dot(transform.forward, (target - me).normalized) > 0`                |
| **妫€鏌ュ湪宸﹁繕鏄彸**             | `Vector3.Cross(transform.forward, targetDir).y` (\>0 鍙? \\<0 宸?              |
| **涓ゅ悜閲忓す瑙?*                 | `Vector3.Angle(dirA, dirB);` (杩斿洖 0~180 搴?                                  |
| **涓栫晫鍧愭爣杞睆骞曞潗鏍?*         | `Camera.main.WorldToScreenPoint(worldPos)`                                    |
| **灞忓箷鍧愭爣杞笘鐣?(甯︽繁搴?**    | `Camera.main.ScreenToWorldPoint(new Vector3(x, y, depth))`                    |

