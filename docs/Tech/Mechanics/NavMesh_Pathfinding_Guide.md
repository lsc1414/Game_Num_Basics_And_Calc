---
sidebarTitle: "馃Л NavMesh 瀵昏矾涓庣姸鎬佹帶鍒舵寚鍗?
---

# 馃Л NavMesh 瀵昏矾涓庣姸鎬佹帶鍒舵寚鍗?

鏈枃妗ｈ缁嗛槓杩?Project Vampirefall 涓晫浜哄浣曞埄鐢?Unity NavMesh 绯荤粺杩涜瀵昏矾锛岄噸鐐硅В鏋?*寮傚父鐘舵€?(CC)** 涓嬬殑瀵昏矾鎺у埗锛屼互鍙?*鍔ㄦ€侀樆鎸?(濉旈槻)** 鐨勫疄鐜扮粏鑺傘€?

---

## 1. 鏍稿績缁勪欢鏋舵瀯 (Core Components)

鍦?Unity 涓紝瀵昏矾涓嶄粎浠呮槸 `SetDestination`銆傚浜庡鏉傜殑 ARPG + TD 娓告垙锛屾垜浠渶瑕佺簿缁嗘帶鍒?`NavMeshAgent`銆?

### 1.1 Agent 閰嶇疆鐨勬渶浣冲疄璺?
*   **Acceleration (鍔犻€熷害):** 璁句负鏋侀珮 (濡?60-100)銆傞槻姝㈡€墿璧锋鈥滄粦姝モ€濇垨杞集鈥滄紓绉烩€濄€傛垜浠渶瑕佸搷搴旂伒鏁忕殑绉诲姩銆?
*   **Angular Speed (杞€?:** 璁句负 360 鎴栨洿楂樸€傛€墿搴旇鑳界灛闂磋浆韬紝鑰屼笉鏄儚鍧﹀厠涓€鏍锋參鎱㈣浆銆?
*   **Auto Braking (鑷姩鍒硅溅):** 
    *   **杩戞垬鎬?** `True`銆傞槻姝㈠啿杩囧ご銆?
    *   **杩滅▼鎬?** `False`銆傚畠浠渶瑕佸钩婊戝湴绉诲姩鍒板皠绋嬭竟缂樺苟鍋滄銆?
*   **Avoidance Priority (閬胯浼樺厛绾?:**
    *   **Boss/Elite:** 0-20 (浼樺厛绾ч珮锛屾帹鐫€鍒汉璧?銆?
    *   **Minion:** 50-99 (浼樺厛绾т綆锛屼細琚尋寮€)銆?
    *   *鎶€宸?* 鍔ㄦ€佽皟鏁翠紭鍏堢骇銆傚綋鎬墿杩涘叆鏀诲嚮鐘舵€佹椂锛屾彁楂樹紭鍏堢骇锛岄槻姝㈣璺繃鐨勯槦鍙嬫尋姝€?

---

## 2. 鐘舵€佹帶鍒朵笌瀵昏矾浜や簰 (CC & Pathfinding)

杩欐槸 ARPG 寮€鍙戜腑鏈€瀹规槗鍑?Bug 鐨勫湴鏂癸細濡備綍璁?`NavMeshAgent` 姝ｇ‘鍝嶅簲鈥滃啺鍐烩€濄€佲€滃嚮閫€鈥濈瓑鐗╃悊鏁堟灉锛?

### 鉂勶笍 2.1 鍑忛€?(Slow)
*   **瀹炵幇:** 鐩存帴淇敼 `agent.speed`銆?
*   **鍙犲姞瑙勫垯:** 
    *   寤鸿浣跨敤 **涔樻硶鍙犲姞**锛歚FinalSpeed = BaseSpeed * (1 - SlowA) * (1 - SlowB)`銆?
    *   璁剧疆涓嬮檺锛歚Mathf.Max(FinalSpeed, 0.5f)`锛岄槻姝㈤€熷害鍑忎负 0 瀵艰嚧鍔ㄧ敾鎾斁寮傚父銆?

### 馃 2.2 瀹氳韩/鍐板喕 (Root / Freeze)
*   **閿欒鍋氭硶:** `agent.enabled = false`銆傝繖浼氬鑷存€墿澶卞幓纰版挒浣撶Н锛屾垨鑰呯灛闂撮噸缃矾寰勩€?
*   **姝ｇ‘鍋氭硶:** `agent.isStopped = true`銆?
    *   淇濈暀璺緞鏁版嵁 (Path Pending)锛屽彧鏄殏鍋滅Щ鍔ㄣ€?
    *   鍚屾椂绂佺敤 `Animator` 鐨勭Щ鍔ㄥ弬鏁帮紝闃叉鍘熷湴澶┖姝ャ€?
*   **鎭㈠:** `agent.isStopped = false`銆?

### 馃挮 2.3 鐪╂檿 (Stun)
*   **鍖哄埆:** 瀹氳韩鏃舵€墿杩樿兘鏀诲嚮/杞ご锛岀湬鏅曟椂瀹屽叏鐦棯銆?
*   **瀹炵幇:**
    1.  `agent.isStopped = true`銆?
    2.  `agent.updateRotation = false` (绂佹杞ご)銆?

    3.  閫昏緫灞傜鐢?AI 鐘舵€佹満 (`FSM.Pause()`)銆?

### 馃 2.4 鍑婚€€ (Knockback) 鈥斺€?*鏈€闅剧偣*
`NavMeshAgent` 鍜?`Rigidbody` 鏄瀵瑰ご銆侫gent 璇曞浘鍚搁檮鍦ㄥ湴闈紝Rigidbody 璇曞浘椋炲嚭鍘汇€?

*   **鏍囧噯娴佺▼:**
    1.  **Disable Agent:** `agent.enabled = false` (蹇呴』褰诲簳鍏虫帀锛屽惁鍒欏畠浼氬己鍒舵妸鍧愭爣鎷夊洖 NavMesh 涓?銆?
    2.  **Add Force:** `rb.isKinematic = false`; `rb.AddForce(ExplosionForce)`.

    3.  **Wait:** 绛夊緟鍑婚€€鏃堕棿锛堝 0.5绉掞級鎴栫瓑寰呴€熷害鎺ヨ繎 0銆?

    4.  **Re-enable Agent:** 

        *   `rb.isKinematic = true`.
        *   `agent.Warp(transform.position)` (鍏抽敭锛佸憡璇?Agent 鎴戠灛绉诲埌浜嗘柊浣嶇疆).
        *   `agent.enabled = true`.
        *   `agent.SetDestination(Target)` (閲嶆柊瀵昏矾).

---

## 3. 瀹炵敤妗堜緥澶у叏 (Practical Use Cases)

### 鈿旓笍 Case A: 鍒拌揪鏀诲嚮璺濈 (Reaching Attack Range)
褰撴€墿杩涘叆灏勭▼鏃讹紝濡備綍浼橀泤鍦板仠涓嬫潵鏀诲嚮锛岃€屼笉鏄帹鐫€鐜╁璧帮紵

*   **鏍稿績閫昏緫:** 涓嶈渚濊禆 `StoppingDistance`锛岃嚜宸辨墜鍔ㄦ帶鍒躲€?
*   **娴佺▼:**
    1.  **Check:** 姣忓抚妫€娴?`Distance(Self, Target) \<= AttackRange`銆?
    2.  **Stop:** 婊¤冻鏉′欢鏃讹紝绔嬪嵆 `agent.isStopped = true`銆?

    3.  **Rotate:** 鏀诲嚮鏃舵墜鍔ㄨ皟鐢?`transform.LookAt(Target)` (鎴栬€呮彃鍊兼棆杞?锛屼繚璇佹湞鍚戞纭€?

    4.  **Resume:** 濡傛灉鐩爣璺戝嚭灏勭▼ `Distance > AttackRange * 1.2` (杩熸粸闃堝€?锛屽垯 `agent.isStopped = false` 缁х画杩藉嚮銆?

#### 浣撶Н淇 (Size Adjustment)
鍦ㄥ闃蹭腑锛屽閫氬父鏈夊緢澶х殑纰版挒浣撶Н锛堝 `Radius = 2.0m`锛夛紝鑰屽皬鎬彧鏈?`Radius = 0.5m`銆傜洿鎺ヨ绠?`Vector3.Distance` (涓績鐐硅窛绂? 浼氬鑷村皬鎬创鐫€濉旂珯锛屾垨鑰呮墦涓嶅埌濉斻€?

*   **鍏紡淇:** `EffectiveRange = AttackRange + TargetRadius + SelfRadius`銆?
    *   **Center-to-Center:** 榛樿璺濈璁＄畻鏄腑蹇冨涓績銆?
    *   **Edge-to-Edge:** 鎴戜滑甯屾湜鐨勬槸鈥滆竟缂樺杈圭紭鈥濄€?
    *   閫氳繃鍔犱笂鍙屾柟鍗婂緞锛屾垜浠畻鍑虹殑鏄€滀负浜嗚姝﹀櫒纰板埌瀵规柟杈圭紭锛屼袱涓腑蹇冪偣闇€瑕佺殑鏈€澶ц窛绂烩€濄€?
*   **杩戞垬鍒ゅ畾:**
    *   瀵逛簬杩戞垬鏀诲嚮锛?*涓嶉渶瑕?*鐪熷疄鐨勭墿鐞嗙鎾烇紙姝﹀櫒纰板埌濉旓級銆?
    *   **Hitbox Lag:** 渚濊禆鐗╃悊纰版挒浼氬鑷村洜涓哄姩鐢诲欢杩熴€佸抚鐜囨尝鍔ㄨ€岄€犳垚鐨勫垽瀹氫涪澶便€?
    *   **鏈€浣冲疄璺?** 鍙鍦?`AttackAnimation` 鐨勫叧閿抚 (Impact Frame) 瑙﹀彂鏃讹紝妫€娴?`Distance \<= EffectiveRange` 鍗冲彲鍒ゅ畾浼ゅ銆傝繖鏄渶绋冲畾銆佹墜鎰熸渶濂界殑鍋氭硶銆?

### 馃П Case B: 鍔ㄦ€侀樆鎸′笌鍫佃矾妫€娴?(Dynamic Blocking)
鍦ㄥ闃叉ā寮忎笅锛岀帺瀹舵斁濉斾笉鑳芥妸鎬墿鐨勮矾褰诲簳鍫垫 (Maze Blocking Rule)銆?

*   **缁勪欢:** 濉旈鍒朵綋涓婃寕 `NavMeshObstacle`銆?
*   **璁剧疆:** `Carve = true` (蹇呴』鍕鹃€夛紝鍚﹀垯鎬墿浼氱┛杩囧幓鎴栬鎸ゅ紑锛岃€屼笉鏄粫璺?銆?
*   **鏀剧疆鍓嶆娴嬬畻娉?**
    1.  铏氭嫙鏀剧疆涓€涓?Obstacle (涓嶆樉绀猴紝鍙弬涓庤绠?銆?
    2.  璋冪敤 `NavMesh.CalculatePath(SpawnPoint, NexusPoint, AreaMask, pathResult)`銆?

    3.  妫€鏌?`pathResult.status == NavMeshPathStatus.PathComplete`銆?

    4.  濡傛灉鏄?`Partial` 鎴?`Invalid`锛岃鏄庤矾琚牭姝讳簡锛岀姝㈢帺瀹跺缓閫犮€?

### 馃暦锔?Case C: 鐖/璺宠穬 (Off-Mesh Links)
璁╂€墿鍍忚湗铔涗竴鏍风炕瓒婂煄澧欙紝鎴栬€呰烦杩囨矡澹戙€?

*   **鍦烘櫙:** 鍍靛案浠庡湴闈㈣烦涓?2妤煎钩鍙版敾鍑荤帺瀹躲€?
*   **瀹炵幇:**
    1.  鍦ㄥ湴鍥惧叧閿繛鎺ョ偣鏀剧疆 `OffMeshLink` 缁勪欢銆?
    2.  褰?Agent 璧板埌 Link 鍏ュ彛鏃讹紝`agent.isOnOffMeshLink` 鍙樹负 `true`銆?

    3.  **鎺ョ鎺у埗:** 

        *   `agent.autoTraverseOffMeshLink = false` (绂佹鑷姩鐬Щ)銆?
        *   鎾斁鈥滆烦璺冣€濆姩鐢汇€?
        *   浣跨敤 `Coroutine` 骞虫粦绉诲姩 Agent 鐨?`transform` 鍒?Link 鐨勫彟涓€绔€?
        *   鍒拌揪鍚庯紝`agent.CompleteOffMeshLink()`锛屼氦杩樻帶鍒舵潈銆?

### 馃幁 Case D: 娓稿嚮/椋庣瓭 (Kiting)
寮撶鎵嬩笉浠呰杩界帺瀹讹紝杩樿淇濇寔璺濈銆?

*   **绗ㄥ姙娉?** 鍙璺濈 < 5绫筹紝灏卞悜鍚庤窇銆傚鏄撳崱澧欒銆?
*   **NavMesh 鍔炴硶 (SamplePosition):**
    1.  璁＄畻鍙嶅悜鍚戦噺: `Dir = (SelfPos - TargetPos).normalized`.
    2.  鐩爣鐐? `FleePos = SelfPos + Dir * 5.0f`.

    3.  **閲囨牱鏈夋晥鎬?** `NavMesh.SamplePosition(FleePos, out hit, 2.0f, AreaMask)`.

    4.  濡傛灉閲囨牱鎴愬姛锛宍SetDestination(hit.position)`銆?

    5.  濡傛灉閲囨牱澶辫触锛堣儗鍚庢槸澧欙級锛屽垯鍚戜晶闈㈠鎵惧悜閲忥紙鍙変箻锛夐噸璇曘€?

### 馃悳 Case E: 鎷ユ尋澶勭悊 (Crowd Separation)
鍑犵櫨涓兊灏告尋鍦ㄤ竴璧凤紝浜掔浉鎺ㄦ尋瀵艰嚧鍗￠】銆?

*   **RVO (Reciprocal Velocity Obstacles):** Unity 鍐呯疆鐨勯伩闅溿€?
    *   *缂虹偣:* 娑堣€?CPU锛屼笖瀹规槗璁╂€墿鐪嬭捣鏉ュ儚閱夋眽涔辨檭銆?
*   **浼樺寲鏂规:**
    1.  **闄嶄綆 RVO Quality:** 鍦?Project Settings 閲屾妸 Agent 鐨勯伩闅滆川閲忚皟浣庛€?
    2.  **鍏抽棴閮ㄥ垎 RVO:** 鍙湁鍓嶆帓鎬墿寮€鍚?Obstacle Avoidance锛屽悗鎺掓€墿鍏抽棴锛堝弽姝ｅ畠浠彧瑕佽窡鐫€鍓嶆帓璧帮級銆?

    3.  **娴佸満 (Flow Field) 鏇夸唬:** 濡傛灉鍚屽睆瓒呰繃 200 涓崟浣嶏紝**鏀惧純 NavMeshAgent**銆?

        *   浣跨敤 `NavMesh.CalculatePath` 绠楀嚭涓€鍙ｈ矾寰勩€?
        *   鎵€鏈夋€墿鍙牴鎹矾寰勪笂鐨勨€滃悜閲忓満鈥濈Щ鍔?`transform.Translate`銆?
        *   浠呭湪鏀诲嚮鏈€鍚庨樁娈靛惎鐢?Agent 杩涜绮剧‘瀹氫綅銆?

---

## 4. 浠ｇ爜鐗囨锛氬畨鍏ㄧ殑鍑婚€€澶勭悊

```csharp
public class NavMeshMovement : MonoBehaviour
{
    [SerializeField] private NavMeshAgent _agent;
    [SerializeField] private Rigidbody _rb;

    // 鍗忕▼锛氬鐞嗗嚮閫€
    public IEnumerator ApplyKnockback(Vector3 force, float duration)
    {
        // 1. 鍒囨柇 NavMesh 杩炴帴
        _agent.isStopped = true; // 鍏堝仠閫昏緫
        _agent.enabled = false;  // 鍐嶅叧缁勪欢 (閲嶈椤哄簭)
        _rb.isKinematic = false; // 寮€鍚墿鐞?

        // 2. 鏂藉姞鍔?
        _rb.AddForce(force, ForceMode.Impulse);

        // 3. 绛夊緟鐗╃悊妯℃嫙
        yield return new WaitForSeconds(duration);

        // 4. 鎭㈠ NavMesh
        _rb.velocity = Vector3.zero;
        _rb.isKinematic = true;
        
        // 瀵绘壘鏈€杩戠殑鏈夋晥鍦伴潰锛岄槻姝㈠崱鍦ㄥ閲?
        if (NavMesh.SamplePosition(transform.position, out NavMeshHit hit, 2.0f, NavMesh.AllAreas))
        {
            _agent.Warp(hit.position); // 鐬Щ鍥炵綉鏍?
            _agent.enabled = true;
            _agent.isStopped = false;
        }
        else
        {
            // 寮傚父澶勭悊锛氳鍑婚鍑哄湴鍥句簡锛岀洿鎺ュ姝?
            GetComponent<Health>().Kill(); 
        }
    }
}
```

---

## 5. 甯歌鍧戠偣閫熸煡 (Troubleshooting)

|          鐜拌薄          |          鍘熷洜          |          瑙ｅ喅鏂规          |
|          :---          |          :---          |          :---          |
|          **鎬墿鍘熷湴杞湀**          |          鐩爣鐐瑰湪鑴氫笅锛屼絾鍥犱负 StoppingDistance 娌″仠浣忋€?         |          澧炲ぇ `StoppingDistance` 鎴栨娴?`agent.remainingDistance < Threshold` 鎵嬪姩 Stop銆?         |
|          **鎬墿绌垮**          |          閫熷害澶揩锛屾垨 `NavMeshObstacle` 娌℃湁寮€ `Carve`銆?         |          寮€鍚?`Carve`锛涘浜庢瀬蹇崟浣嶏紝鏀圭敤 Raycast 妫€娴嬪墠鏂归殰纰嶃€?         |
|          **娴┖/闄峰叆鍦颁笅**          |          Agent 鐨?`BaseOffset` 璁剧疆涓嶅锛屾垨妯″瀷鍘熺偣涓嶅湪鑴氬簳銆?         |          璋冩暣 `BaseOffset`锛涚‘淇濈編鏈ā鍨嬬殑 Pivot 鍦ㄨ剼搴曚腑蹇冦€?         |
|          **鎬ц兘鏆磋穼**          |          姣忎竴甯ч兘瀵?100 涓€皟鐢?`SetDestination`銆?         |          蹇呴』闄愬埗棰戠巼锛佷娇鐢ㄥ崗绋嬫瘡 0.2s 鏇存柊涓€娆¤矾寰勶紝鎴栦粎褰撶洰鏍囩Щ鍔ㄨ秴杩?1绫虫椂鏇存柊銆?         |

