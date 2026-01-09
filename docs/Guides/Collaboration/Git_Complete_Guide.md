---
sidebarTitle: "Git 鎸囧崡缁煎悎鎸囧崡"
---

# Git 鎸囧崡缁煎悎鎸囧崡

> 鏈枃妗ｇ敱浠ヤ笅鏂囦欢鍚堝苟鐢熸垚 (2026-01-09)



---


{/* 鏉ユ簮: Dev_Guides\Collaboration\Git_Advanced_Guide_For_Programmers.md */}

## 馃悪 Git 鏋佸鐢熷瓨鎸囧崡锛氫粠鍛戒护琛屽埌绉佹湁浜戞惌寤?

> **闈㈠悜瀵硅薄**: 绋嬪簭鍛?(Programmers)銆?
> **鐩爣**: 鎺屾彙 Git 鐨勨€滈粦榄旀硶鈥濓紝澶勭悊澶嶆潅鐨勫垎鏀鐞嗐€佸啿绐佽В鍐筹紝骞跺浼氭惌寤哄洟闃熺殑绉佹湁浠ｇ爜浠撳簱銆?

## 1. 甯哥敤鍛戒护閫熸煡 (The Cheat Sheet)

### 1.1 鍩虹鎿嶄綔
```bash
git init                    # 鍒濆鍖栦粨搴?
git clone <url>             # 鍏嬮殕杩滅▼浠撳簱
git status                  # 鏌ョ湅褰撳墠鐘舵€?(蹇呯敤!)
git add .                   # 娣诲姞鎵€鏈変慨鏀瑰埌鏆傚瓨鍖?
git commit -m "feat: xxx"   # 鎻愪氦
git pull                    # 鎷夊彇鏇存柊 (鐩稿綋浜?fetch + merge)
git push                    # 鎺ㄩ€佷慨鏀?
```

### 1.2 鍒嗘敮鎿嶄綔 (Branching)
```bash
git branch                  # 鍒楀嚭鏈湴鍒嗘敮
git branch -a               # 鍒楀嚭鎵€鏈夊垎鏀?(鍚繙绋?
git checkout -b feature/A   # 鍒涘缓骞跺垏鎹㈠埌 feature/A 鍒嗘敮
git checkout develop        # 鍒囨崲鍥?develop
git merge feature/A         # 鎶?feature/A 鍚堝苟杩涘綋鍓嶅垎鏀?
git branch -d feature/A     # 鍒犻櫎鍒嗘敮
```

### 1.3 鍚庢倲鑽?(Undo)
```bash
git checkout -- file.cs     # 涓㈠純宸ヤ綔鍖虹殑淇敼 (杩樻病 add)
git reset HEAD file.cs      # 鎶婃殏瀛樺尯鐨勪慨鏀规挙鍥炲伐浣滃尯 (add 浜嗕絾娌?commit)
git reset --soft HEAD^      # 鎾ら攢鏈€杩戜竴娆?commit (浠ｇ爜淇濈暀鍦ㄦ殏瀛樺尯)
git reset --hard HEAD^      # 褰诲簳鍥為€€鍒颁笂涓増鏈?(浠ｇ爜鍏ㄩ儴涓㈠純锛屾厧鐢?)
git commit --amend          # 淇敼鏈€杩戜竴娆?commit 鐨勬敞閲?
```

### 1.4 鏆傚瓨鐜板満 (Stash)
褰撲綘姝ｅ湪淇?Bug锛岀獊鐒惰€佹澘璁╀綘鍒囧垎鏀幓鏀瑰彟涓€涓揣鎬?Bug锛?
```bash
git stash                   # 鎶婂綋鍓嶆湭鎻愪氦鐨勪慨鏀光€滆棌鈥濊捣鏉?
git checkout hotfix/001     # 鍒囧垎鏀幓淇?Bug...
# ... 淇畬鍥炴潵 ...
git checkout develop
git stash pop               # 鎶娾€滆棌鈥濊捣鏉ョ殑浠ｇ爜杩樺師鍥炴潵
```

## 2. 杩涢樁鎶€宸?(Advanced Skills)

### 2.1 Rebase (鍙樺熀) vs Merge
*   **Merge**: 淇濈暀鐪熷疄鐨勫巻鍙茶褰曪紝浼氭湁 "Merge branch 'xxx'" 鐨勬彁浜ゃ€傞€傚悎鍏叡鍒嗘敮鍚堝苟銆?
*   **Rebase**: 鎶婁綘鐨勬彁浜も€滄帴鈥濆湪鐩爣鍒嗘敮鐨勬渶鏂版彁浜ゅ悗闈€傚巻鍙茶褰曟槸涓€鏉＄洿绾匡紝闈炲父骞插噣銆?
    *   `git pull --rebase`: 鎷夊彇浠ｇ爜鏃惰嚜鍔ㄥ彉鍩?(鎺ㄨ崘閰嶇疆)銆?
    *   `git rebase develop`: 鍦?feature 鍒嗘敮涓婏紝鎶?develop 鐨勬渶鏂颁唬鐮佸灚鍦ㄤ笅闈€?

### 2.2 Cherry-pick (鎽樻ū妗?
鍙兂瑕佹煇涓垎鏀噷鐨?*鏌愪竴娆?*鎻愪氦锛岃€屼笉鏄暣涓垎鏀紵
```bash
git log                     # 鎵惧埌閭ｄ釜 commit 鐨?hash (渚嬪 a1b2c3d)
git cherry-pick a1b2c3d     # 鎶婅繖涓?commit 澶嶅埗鍒板綋鍓嶅垎鏀?
```

### 2.3 瑙ｅ喅鍐茬獊 (Conflict Resolution)

#### A. 鏂囨湰鏂囦欢鍐茬獊
1.  **瀹氫綅**: 鎵撳紑鍐茬獊鏂囦欢锛屾壘鍒?`<<<<<<<`, `=======`, `>>>>>>>` 鏍囪銆?
2.  **淇敼**: 鍐冲畾淇濈暀鍝儴鍒嗕唬鐮侊紙鎴栬€呴兘淇濈暀锛夛紝鍒犻櫎鏍囪绗﹀彿銆?

3.  **鎻愪氦**: `git add` + `git commit`銆?

#### B. 浜岃繘鍒舵枃浠跺啿绐?(Binary Conflict) - **鍏抽敭锛?*
鍥剧墖銆佹ā鍨嬨€丏LL 鏃犳硶鍚堝苟鍐呭锛屽繀椤?*浜岄€変竴**銆?

**鍛戒护琛屾柟妗?*:

*   **淇濈暀鎴戠殑 (Mine)**: 鎴戞敼浜嗗浘锛屾垜瑕佽鐩栨湇鍔″櫒鐨勩€?
    ```bash
    git checkout --ours path/to/image.png
    git add path/to/image.png
    ```

*   **淇濈暀浠栫殑 (Theirs)**: 鍒汉鐨勫浘鏄鐨勶紝鎴戞斁寮冩垜鐨勪慨鏀广€?
    ```bash
    git checkout --theirs path/to/image.png
    git add path/to/image.png
    ```

*   娉ㄦ剰锛氬湪 `git merge` 鏃讹紝`--ours` 鏄寚褰撳墠鍒嗘敮锛宍--theirs` 鏄寚瑕佸悎骞惰繘鏉ョ殑鍒嗘敮銆備絾鍦?`git rebase` 鏃讹紝閫昏緫鏄弽鐨勶紒鍔″繀鍏堝浠姐€?

**GUI 鏂规 (Sourcetree / TortoiseGit)**:

1.  鍦ㄥ啿绐佹枃浠朵笂鍙抽敭銆?
2.  閫夋嫨 `Resolve using 'Mine'` (浣跨敤鎴戠殑鐗堟湰) 鎴?`Resolve using 'Theirs'` (浣跨敤杩滅▼鐗堟湰)銆?

3.  宸ュ叿浼氳嚜鍔ㄦ墽琛屼笂杩板懡浠ゅ苟鏍囪涓哄凡瑙ｅ喅銆?

**缁堟瀬鏂规: 閿佸畾 (Locking)**
涓轰簡閬垮厤浜岃繘鍒跺啿绐侊紝鏈€濂界殑鍔炴硶鏄?*涓嶈璁╁啿绐佸彂鐢?*銆?

*   浣跨敤 LFS 鐨勯攣瀹氬姛鑳? `git lfs lock image.png`銆?
*   杩欐牱褰撲綘鍦ㄤ慨鏀规椂锛屽埆浜烘棤娉曟帹閫佽繖涓枃浠讹紝鐩村埌浣?`unlock`銆?

## 3. 鎼缓绉佹湁 Git 鏈嶅姟鍣?(Self-Hosted Git)

瀵逛簬涓嶆兂鎶婁唬鐮佹斁鍦?GitHub/Gitee 鐨勫洟闃燂紝鎺ㄨ崘鎼缓 **Gitea** (杞婚噺绾? 鎴?**GitLab** (鍔熻兘鍏?銆?

### 3.1 鏂规 A: Gitea (鎺ㄨ崘锛屾瀬杞婚噺)
閫傚悎灏忓洟闃燂紝涓€涓簩杩涘埗鏂囦欢鎼炲畾锛屽唴瀛樺崰鐢ㄦ瀬浣庛€?

**鎼缓姝ラ (Windows/Linux)**:

1.  **涓嬭浇**: 鍘?[Gitea 瀹樼綉](https://gitea.io) 涓嬭浇瀵瑰簲绯荤粺鐨勫彲鎵ц鏂囦欢銆?
2.  **杩愯**: 鐩存帴鍙屽嚮杩愯 (浼氬惎鍔?Web 鏈嶅姟鍣紝榛樿绔彛 3000)銆?

3.  **閰嶇疆**: 娴忚鍣ㄨ闂?`localhost:3000`锛岄娆¤繍琛屼細杩涘叆瀹夎鍚戝銆?

    *   鏁版嵁搴撻€?`SQLite3` (鏈€绠€鍗曪紝鏃犻渶瀹夎 MySQL)銆?
    *   璁剧疆绠＄悊鍛樿处鍙枫€?
4.  **灞€鍩熺綉璁块棶**: 纭繚闃茬伀澧欏紑鏀?3000 绔彛銆傞槦鍙嬪彲浠ラ€氳繃 `http://192.168.x.x:3000` 璁块棶銆?

### 3.2 鏂规 B: 灞€鍩熺綉瑁镐粨搴?(Bare Repo)
鏈€鍘熷鐨勬柟娉曪紝涓嶉渶瑕佷换浣?Web 鐣岄潰銆?

1.  **鏈嶅姟鍣ㄧ (鎵惧彴鐢佃剳鍋氫富鏈?**:
    ```bash
    mkdir vampirefall.git
    cd vampirefall.git
    git init --bare  # 鍒濆鍖栬８浠撳簱 (娌℃湁宸ヤ綔鍖猴紝鍙湁鏁版嵁搴?
    ```

2.  **鍏变韩**: 灏?`vampirefall.git` 鏂囦欢澶硅缃负**缃戠粶鍏变韩鏂囦欢澶?* (Windows SMB)銆?

3.  **瀹㈡埛绔?*:
    ```bash
    git clone //SERVER_IP/Shared/vampirefall.git
    ```

## 4. Unity 椤圭洰鐨?.gitignore (蹇呮妱)

```gitignore
# Unity folders
/[Ll]ibrary/
/[Tt]emp/
/[Oo]bj/
/[Bb]uild/
/[Bb]uilds/
/[Ll]ogs/
/[Mm]emoryCaptures/

# Visual Studio / JetBrains
.vs/
.idea/
*.sln
*.csproj
*.unityproj

# OS
.DS_Store
Thumbs.db
```

## 5. LFS 閰嶇疆 (澶ф枃浠跺瓨鍌?

瀵逛簬澶т簬 100MB 鐨勬枃浠?(PSD, FBX)锛屽繀椤荤敤 LFS銆?

1.  **瀹夎**: `git lfs install`
2.  **閰嶇疆**:
    ```bash
    git lfs track "*.psd"
    git lfs track "*.fbx"
    git lfs track "*.wav"
    ```

3.  **鎻愪氦**: 杩欎細鐢熸垚涓€涓?`.gitattributes` 鏂囦欢锛屽姟蹇呮妸瀹冩彁浜や笂鍘汇€?

---

**涓€鍙ヨ瘽蹇犲憡**: 
**姘歌繙涓嶈鍦ㄤ富鍒嗘敮 (master/develop) 涓婄洿鎺ュ啓浠ｇ爜銆?*
**Commit 鏃╋紝Commit 鍕ゃ€?*



---


{/* 鏉ユ簮: Dev_Guides\Collaboration\Git_Commit_Standards.md */}

## 馃悪 Git 鐗堟湰绠＄悊涓?Commit Log 瑙勮寖 (Git Standards)

> **鏍稿績鐞嗗康**: **Commit Log 鏄啓缁欎汉鐪嬬殑锛屼笉鏄啓缁欐満鍣ㄧ湅鐨勩€?*
> 涓€涓ソ鐨?Commit Log 搴旇鑳藉洖绛斾笁涓棶棰橈細
> 1.  **鏀逛簡浠€涔堬紵** (What)
> 2.  **涓轰粈涔堟敼锛?* (Why)
> 3.  **鎬庝箞鏀圭殑锛?* (How - 鍙€夛紝濡傛灉鏄鏉傞€昏緫)

## 1. Commit Message 鏍煎紡瑙勮寖

閲囩敤涓氱晫鏍囧噯鐨?**Angular Commit Convention**锛岀粨鏋勫涓嬶細

```text
<type>(<scope>): <subject>

<body>

<footer>
```

### 1.1 Type (蹇呭～)
鐢ㄤ竴涓瘝鎻忚堪鏀瑰姩鐨勬€ц川锛?

*   **feat**: 鏂板姛鑳?(Feature)銆?
*   **fix**: 淇ˉ Bug銆?
*   **docs**: 浠呬慨鏀逛簡鏂囨。 (濡?README)銆?
*   **style**: 鏍煎紡淇敼 (涓嶅奖鍝嶄唬鐮佽繍琛岀殑鍙樺姩锛屽绌烘牸銆佺缉杩?銆?
*   **refactor**: 閲嶆瀯 (鍗充笉鏄柊澧炲姛鑳斤紝涔熶笉鏄慨鏀?bug 鐨勪唬鐮佸彉鍔?銆?
*   **perf**: 鎬ц兘浼樺寲銆?
*   **test**: 澧炲姞娴嬭瘯鎴栦慨鏀规祴璇曘€?
*   **chore**: 鏋勫缓杩囩▼鎴栬緟鍔╁伐鍏风殑鍙樺姩 (濡?.gitignore, package.json)銆?
*   **art**: 缇庢湳璧勬簮鎻愪氦 (璐村浘銆佹ā鍨嬨€侀鍒朵綋)銆?

### 1.2 Scope (閫夊～)
鐢ㄦ嫭鍙疯鏄庡奖鍝嶇殑鑼冨洿 (妯″潡/鍔熻兘)锛?

*   `feat(Tower)`: 濉旈槻妯″潡銆?
*   `fix(UI)`: 鐣岄潰妯″潡銆?
*   `art(VFX)`: 鐗规晥璧勬簮銆?

### 1.3 Subject (蹇呭～)
绠€鐭殑鎻忚堪锛屼笉瓒呰繃 50 涓瓧绗︺€?

*   **鍘熷垯**: 鍔ㄨ瘝寮€澶达紝浣跨敤绁堜娇鍙ャ€?
*   *Good*: "Add double jump mechanic" (娣诲姞浜屾璺虫満鍒?
*   *Bad*: "Fixed some bugs" (淇簡涓€浜沚ug -> **淇簡鍟ワ紵锛?*)

### 1.4 Body (閫夊～锛屼絾鎺ㄨ崘)
璇︾粏鎻忚堪銆?

*   瑙ｉ噴**涓轰粈涔?*瑕佸仛杩欎釜淇敼锛?
*   瑙ｉ噴**涔嬪墠**鏄€庝箞鏍风殑锛?*鐜板湪**鏄€庝箞鏍风殑锛?
*   濡傛灉鏄慨澶?Bug锛屾弿杩?*澶嶇幇姝ラ**鎴?*鏍瑰洜**銆?

### 1.5 Footer (閫夊～)
*   鍏宠仈鐨?Issue 鎴栦换鍔?ID銆?
*   `Closes #123`
*   `BREAKING CHANGE`: 濡傛灉鏈夌牬鍧忔€ф洿鏂帮紙濡傛敼浜嗗瓨妗ｆ牸寮忥級锛屽繀椤诲ぇ鍐欐敞鏄庯紒

## 2. 馃摑 鏍囧噯 Commit Log Demo (鎶勪綔涓氬尯)

璇峰洟闃熸垚鍛樼洿鎺ュ鍒朵互涓嬫ā鏉夸慨鏀广€?

### 鍦烘櫙 A: 淇浜嗕竴涓?Bug
```text
fix(Combat): 淇绠鏀婚€熻繃蹇鑷翠激瀹充涪澶辩殑闂

鍘熷洜: 
涔嬪墠鐨勬敾鍑诲喎鍗磋鏃跺櫒浣跨敤 Time.deltaTime 绱姞锛屽湪浣庡抚鐜囦笅浼氭湁娴偣璇樊銆?

淇敼:
鏀圭敤 Time.time 鏃堕棿鎴宠繘琛屽喎鍗村垽瀹氥€?

Closes #405
```

### 鍦烘櫙 B: 寮€鍙戜簡涓€涓柊鍔熻兘
```text
feat(Roguelike): 鏂板澶╄祴 "鐏劙绮鹃€?

鏁堟灉:
鎵€鏈夐€犳垚鐗╃悊浼ゅ鐨勯槻寰″锛岀幇鍦ㄦ湁 30% 姒傜巼闄勫姞鐐圭噧鏁堟灉銆?

鎶€鏈粏鑺?
1. 鍦?DamageCalculator 涓柊澧炰簡 ElementCheck 閫昏緫銆?
2. 鏂板浜?Buff_Ignite 鑴氭湰銆?
```

### 鍦烘櫙 C: 鎻愪氦缇庢湳璧勬簮
```text
art(Enemy): 鎻愪氦 Level 3 绮捐嫳鎬?"鐭冲ご浜? 璧勬簮

鍖呭惈:
1. 妯″瀷: Golem_L3.fbx (甯?LOD)
2. 璐村浘: T_Golem_D/N/M_01.png (ASTC 鍘嬬缉)
3. 鍔ㄧ敾: Anim_Golem_Walk/Attack/Die

娉ㄦ剰:
鏉愯川鐞冧娇鐢ㄤ簡鏂扮殑 Toon Shader锛岃绋嬪簭纭鏄惁鏀寔 GPU Instancing銆?
```

### 鍦烘櫙 D: 鎬ц兘浼樺寲
```text
perf(Pathfinding): 浼樺寲澶ч噺鍗曚綅瀵昏矾鏃剁殑 CPU 鍗犵敤

涔嬪墠浣跨敤 NavMeshAgent.SetDestination 姣忓抚璋冪敤锛屽鑷翠富绾跨▼鍗￠】銆?
鐜板湪鏀逛负姣?10 甯?(0.2s) 鏇存柊涓€娆¤矾寰勶紝骞跺惎鐢ㄤ簡 Job System 杩涜璺濈璁＄畻銆?

鎬ц兘鎻愬崌:
鍚屽睆 500 鍗曚綅鏃讹紝Update 鑰楁椂浠?8ms 闄嶈嚦 1.5ms銆?
```

## 3. 鍒嗘敮绠＄悊绛栫暐 (Branching Strategy)

### 3.1 鍒嗘敮鍛藉悕
*   **master / main**: 闅忔椂鍙彂甯冪殑绋冲畾鐗堟湰銆?*缁濆绂佹鐩存帴 Push**銆?
*   **develop**: 寮€鍙戜富鍒嗘敮銆傛墍鏈?Feature 鍒嗘敮鍚堝叆杩欓噷銆?
*   **feat/xxx**: 鍔熻兘鍒嗘敮銆傚 `feat/login_system`銆?
*   **fix/xxx**: 淇鍒嗘敮銆傚 `fix/crash_on_start`銆?
*   **art/xxx**: 缇庢湳璧勬簮鍒嗘敮銆?

### 3.2 宸ヤ綔娴?(Workflow)
1.  鎺ュ埌浠诲姟 "寮€鍙戠櫥褰曠郴缁?銆?
2.  鍩轰簬 `develop` 鍒囧嚭 `feat/login`銆?

3.  寮€鍙?.. 鎻愪氦... (澶氭 Commit)銆?

4.  寮€鍙戝畬姣曪紝鎺ㄩ€佸埌杩滅▼銆?

5.  鍙戣捣 **Pull Request (PR)** 鍚堝叆 `develop`銆?

6.  **Code Review**: 鍚屼簨妫€鏌ヤ唬鐮侊紝纭鏃犺鍚?Approve銆?

7.  鍚堝苟銆?

## 4. 宸ュ叿寮哄埗绾︽潫 (Enforcement)

涓轰簡闃叉浜轰负鍋锋噿锛屽缓璁儴缃?**Git Hooks**銆?

### 4.1 commit-msg Hook
鍦?`.git/hooks/commit-msg` 涓坊鍔犺剼鏈紝浣跨敤姝ｅ垯琛ㄨ揪寮忔鏌?Commit Message 鏍煎紡銆傚鏋滀笉绗﹀悎 `<type>(<scope>): <subject>` 鏍煎紡锛岀洿鎺ユ嫆缁濇彁浜ゃ€?

### 4.2 pre-commit Hook
鍦ㄦ彁浜ゅ墠鑷姩杩愯锛?

*   浠ｇ爜鏍煎紡鍖?(CSharpier / Format)銆?
*   绠€鍗曠殑闈欐€佹鏌?(濡傛湁鏃犲甫 `Debug.Log` 鐨勪唬鐮?銆?

---

**鏈€鍚庨€氱墥**: 
"Update", "Fix bug", "Backup", "..." 杩欑 Commit Message 涓€缁忓彂鐜帮紝**璇疯鍏ㄧ粍鍠濆ザ鑼?*銆?

---

## 馃摎 鎵╁睍闃呰涓庡弬鑰冩爣鍑?(References)

### 馃實 琛屼笟鏍囧噯
*   **[Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/)**
    *   鏈枃妗ｅ熀浜庢瑙勮寖銆傚畠鏄洰鍓嶆渶娴佽鐨?Commit Message 鏍囧噯锛岃 Angular, React, Electron 绛夋暟涓囦釜寮€婧愰」鐩噰鐢ㄣ€?
*   **[Semantic Versioning 2.0.0](https://semver.org/)** (璇箟鍖栫増鏈帶鍒?
    *   瑙ｉ噴浜嗕负浠€涔?`BREAKING CHANGE` 浼氬鑷村ぇ鐗堟湰鍙?+1 (v1.0.0 -> v2.0.0)銆?

### 馃敡 鑷姩鍖栧伐鍏?
*   **[Husky](https://github.com/typicode/husky)**
    *   鏈€娴佽鐨?Git Hooks 宸ュ叿銆傚彲浠ョ敤瀹冨湪 `git commit` 涔嬪墠鑷姩杩愯 Lint 妫€鏌ャ€?
*   **[Commitlint](https://github.com/conventional-changelog/commitlint)**
    *   涓€涓懡浠よ宸ュ叿锛岀敤鏉ユ鏌?Commit Message 鏄惁绗﹀悎 Conventional Commits 瑙勮寖銆傚缓璁泦鎴愬埌 CI/CD 娴佺▼涓€?

### 馃摉 娣卞害鏂囩珷
*   **[How to Write a Git Commit Message](https://cbea.ms/git-commit/)** (Chris Beams)
    *   杩欑瘒鍗氬琚棤鏁颁汉寮曠敤锛岃缁嗚В閲婁簡鈥滀负浠€涔堣鐢ㄧ浣垮彞鈥濄€佲€滀负浠€涔堥琛屼笉鑳借秴杩?0涓瓧绗︹€濄€?




---


{/* 鏉ユ簮: Dev_Guides\Collaboration\GitHub_PR_Workflow.md */}

## 馃悪 GitHub 宸ヤ綔娴佷笌 PR 鏈€浣冲疄璺?(GitHub Flow & PR Guide)

> **鏍稿績鐞嗗康**: **涓诲垎鏀?(main/develop) 鏄鍦ｄ笉鍙镜鐘殑**銆備换浣曚唬鐮佹兂瑕佽繘鍏ヤ富鍒嗘敮锛屽繀椤荤粡杩囪嚦灏戜竴鍙岀溂鐫涚殑妫€鏌?(Code Review)銆傝繖涓繃绋嬪氨鍙?**Pull Request (PR)**銆?

## 1. 鏍囧噯宸ヤ綔娴?(The Flow)

### 1.1 Fork vs Branch
*   **寮€婧愭ā寮?(Fork)**: 浣犳病鏈夊師浠撳簱鐨勫啓鏉冮檺銆備綘鎶婁粨搴?`Fork` 鍒颁綘鑷繁鍚嶄笅锛屾敼瀹屽悗鍚戝師浠撳簱鍙戣捣 PR銆?
*   **鍥㈤槦妯″紡 (Branch)**: 浣犳湁鍐欐潈闄愩€備綘鐩存帴鍦ㄥ師浠撳簱閲屽垏涓€涓?`feature/xxx` 鍒嗘敮锛屾敼瀹屽悗鍚?`develop` 鍙戣捣 PR銆?
*   **Vampirefall 鎺ㄨ崘**: **鍥㈤槦妯″紡**銆傛晥鐜囨洿楂樸€?

### 1.2 瀹屾暣鐢熷懡鍛ㄦ湡
1.  **鏂板缓鍒嗘敮**: 鍩轰簬鏈€鏂?`develop` 鍒涘缓 `feat/tower_fire`銆?
2.  **鎻愪氦浠ｇ爜**: 鍦?`feat/tower_fire` 涓?commit銆?

3.  **鍙戣捣 PR**: 鍦?GitHub/Gitea 缃戦〉涓婄偣鍑?"New Pull Request"銆?

    *   *Source*: `feat/tower_fire`
    *   *Target*: `develop`
4.  **Code Review**: 浣犵殑鍚屼簨鏀跺埌閫氱煡锛岃繘鏉ユ鏌ヤ唬鐮侊紝鍐欒瘎璁恒€?

5.  **淇敼鍙嶉**: 鏍规嵁鍚屼簨鐨勫缓璁紝缁х画鍦?`feat/tower_fire` 涓婃彁浜や慨鏀广€?

6.  **鍚堝苟 (Merge)**: 鍚屼簨鐐硅禐 (Approve) 鍚庯紝鐐瑰嚮 "Squash and Merge"銆?

7.  **鍒犻櫎鍒嗘敮**: 瀹屼簨鍚庡垹鎺?`feat/tower_fire`銆?

## 2. 濡備綍鍐欎竴涓紭绉€鐨?PR 鎻忚堪锛?

PR 鐨勬弿杩板喅瀹氫簡 Reviewer 鐨勫績鎯呭拰瀹℃牳閫熷害銆?

### 2.1 鏍囬 (Title)
*   鏍煎紡: `<Type>: <Subject>` (鍚?Commit Message)
*   渚嬪瓙: `feat: 瀹炵幇鐏劙濉旂殑鐕冪儳閫昏緫`

### 2.2 妯℃澘 (Template)
寤鸿鍦ㄤ粨搴撴牴鐩綍寤轰竴涓?`.github/PULL_REQUEST_TEMPLATE.md`锛屽唴瀹瑰涓嬶細

```markdown
## 馃摑 鏀瑰姩鎽樿
瀹炵幇浜嗙伀鐒板鐨勫熀纭€閫昏緫锛屽寘鎷?DoT 浼ゅ鍜岃瑙夌壒鏁堛€?

## 馃摳 鎴浘/GIF (閫夊～)
[杩欓噷鏀句竴寮犵伀鐒板鏀诲嚮鎬墿鐨?GIF锛岃儨杩囧崈瑷€涓囪]

## 馃敆 鍏宠仈 Issue
Closes #102

## 鉁?鑷祴娓呭崟
- [x] 濉旇兘姝ｅ父鏀诲嚮
- [x] 鐕冪儳浼ゅ鏁板€兼纭?
- [x] 鎬墿姝讳骸鍚庣壒鏁堟秷澶?
- [x] 娌℃湁浜х敓 GC Alloc
```

## 3. Code Review 绀间华涓庢爣鍑?

### 3.1 Reviewer (瀹℃牳鑰? 鐨勮亴璐?
*   **鐪嬮€昏緫**: 浠ｇ爜鏄惁瀹炵幇浜嗛渶姹傦紵鏈夋病鏈夋槑鏄剧殑 Bug锛?
*   **鐪嬭鑼?*: 鍙橀噺鍚嶆槸鍚﹁鑼冿紵鏈夋病鏈夊啓娉ㄩ噴锛?
*   **鐪嬫€ц兘**: 鏈夋病鏈夊湪 Update 閲?`new List`锛熸湁娌℃湁姝诲惊鐜闄╋紵
*   **璇皵**: **瀵逛簨涓嶅浜?*銆?
    *   *Bad*: "浣犺繖浠ｇ爜鍐欏緱澶儌浜嗐€?
    *   *Good*: "杩欓噷鍙兘浼氫骇鐢?GC锛屽缓璁敼鐢ㄥ璞℃睜銆?

### 3.2 Submitter (鎻愪氦鑰? 鐨勫績鎬?
*   **涓嶈鐜荤拑蹇?*: 鍒汉鎸囧嚭鐨勯棶棰樻槸涓轰簡椤圭洰濂斤紝涓嶆槸閽堝浣犮€?
*   **瑙ｉ噴**: 濡傛灉浣犱笉璁ゅ悓 Reviewer 鐨勬剰瑙侊紝璇峰湪璇勮閲岃В閲婁綘鐨勭悊鐢憋紝鎴栬€呯嚎涓嬫矡閫氥€?
*   **鍙婃椂鍝嶅簲**: 鍒彂浜?PR 灏变笉绠′簡锛屽埆浜烘彁浜嗘剰瑙佽刀绱ф敼銆?

## 4. Merge 绛栫暐锛歋quash vs Merge

鐐瑰嚮 Merge 鎸夐挳鏃讹紝鏈変笁绉嶉€夐」锛?

### 4.1 Create a merge commit (鏅€氬悎骞?
*   淇濈暀鎵€鏈夊巻鍙茶褰曘€傚鏋滀綘鐨勫垎鏀笂鏈?100 涓?"fix typo" 鐨勫瀮鍦炬彁浜わ紝瀹冧滑閮戒細杩涘叆涓诲垎鏀€?
*   **璇勪环**: 鉂?**鑴?*銆備笉鎺ㄨ崘銆?

### 4.2 Squash and merge (鍘嬬缉鍚堝苟) - **鎺ㄨ崘**
*   鎶婁綘鍒嗘敮涓婄殑 100 涓彁浜?*鍘嬬缉鎴?1 涓?*鎻愪氦锛屽悎鍏ヤ富鍒嗘敮銆?
*   **璇勪环**: 鉁?**骞插噣**銆備富鍒嗘敮鐨勫巻鍙茶褰曢潪甯告竻鏅帮紝涓€涓姛鑳藉搴斾竴涓?Commit銆?

### 4.3 Rebase and merge (鍙樺熀鍚堝苟)
*   鎶婁綘鐨勬彁浜ょ洿鎺ユ帴鍒颁富鍒嗘敮鍚庨潰锛屽儚浠庢潵娌″垎鍙夎繃涓€鏍枫€?
*   **璇勪环**: 鈿狅笍 **楂橀闄?*銆傚鏋滀笉浠呬繚鐣欎簡鍨冨溇鎻愪氦锛岃繕娌℃湁 Merge 鑺傜偣锛屽嚭闂寰堥毦鍥為€€銆?

## 5. 甯歌闂

*   **PR 鍐茬獊浜嗘€庝箞鍔烇紵**: 
    *   鍦ㄦ湰鍦?`git pull origin develop` (鎶婁富鍒嗘敮鏈€鏂颁唬鐮佹媺涓嬫潵)銆?
    *   鏈湴瑙ｅ啿绐併€?
    *   `git push` 鏇存柊浣犵殑 PR 鍒嗘敮銆侴itHub 浼氳嚜鍔ㄦ洿鏂扮姸鎬併€?
*   **PR 澶ぇ浜嗘€庝箞鍔烇紵**: 
    *   濡傛灉涓€涓?PR 鏀逛簡 50 涓枃浠讹紝娌′汉鎰挎剰鐪嬨€?
    *   **鎷嗗垎**: 鍏堟彁涓€涓?`feat/tower_base` (鍙湁鍩虹被)锛屽悎鍏ュ悗鍐嶆彁 `feat/tower_fire`銆?

---

**涓€鍙ヨ瘽鎬荤粨**: 
**PR 鏄唬鐮佽川閲忕殑瀹堥棬鍛樸€?*
**娌℃湁 Review 鐨勪唬鐮侊紝灏辨槸鍩嬪湪椤圭洰閲岀殑闆枫€?*




---


{/* 鏉ユ簮: Dev_Guides\Collaboration\SVN_vs_Git_Migration_Guide.md */}

## 馃悽 SVN vs 馃悪 Git锛氭繁搴﹀姣斾笌鏋佺畝涓婃墜鎸囧崡

> **鍐欏湪鍓嶉潰**: 寰堝鍥㈤槦锛堝挨鍏舵槸缇庢湳鍚屽锛変範鎯簡 SVN 鐨勨€滅洿瑙傗€濓紝瀵?Git 鎰熷埌鎭愭儳銆傚叾瀹?Git 骞舵病鏈夐偅涔堥毦锛屽彧鏄€昏緫鍙樹簡銆?
> **鏍稿績鍖哄埆**: **SVN 鏄泦涓紡鐨?(鏈嶅姟鍣ㄥ潖浜嗗ぇ瀹堕兘寰楀仠宸?锛孏it 鏄垎甯冨紡鐨?(姣忎釜浜虹數鑴戦噷閮芥湁涓€浠藉畬鏁寸殑鐗堟湰搴?銆?*

## 1. 娣卞害瀵规瘮鍒嗘瀽 (Analysis)

### 1.1 涓轰粈涔堢編鏈枩娆?SVN锛?
*   **鏂囦欢閿佸畾 (Locking)**: SVN 鍙互鍦ㄤ綘缂栬緫 `Hero.psd` 鏃垛€滈攣浣忊€濆畠锛屽埆浜哄氨涓嶈兘鏀逛簡銆傝繖瀵逛簩杩涘埗鏂囦欢锛堝浘鐗囥€佹ā鍨嬶級鑷冲叧閲嶈锛岄槻姝㈠啿绐併€侴it 榛樿娌℃湁閿侊紙闇€瑕?LFS 鎻掍欢锛夈€?
*   **灞€閮ㄦ鍑?*: SVN 鍙互鍙笅杞介」鐩殑 `Art/Characters` 鏂囦欢澶广€侴it 蹇呴』鎶婃暣涓粨搴擄紙鍖呮嫭浣犱笉鍏冲績鐨勪唬鐮佸拰鏂囨。锛夊叏鎷変笅鏉ャ€?
*   **鏉冮檺鎺у埗**: SVN 鍙互绮剧‘鎺у埗鈥滅編鏈彧鑳借鍐?Art 鐩綍锛屼笉鑳界 Code 鐩綍鈥濄€侴it 閫氬父鏄粨搴撶骇鍒殑鏉冮檺锛堣涔堥兘鑳借鍐欙紝瑕佷箞閮戒笉鑳斤級銆?

### 1.2 涓轰粈涔堢▼搴忓枩娆?Git锛?
*   **鍒嗘敮 (Branching)**: Git 鍒囧垎鏀槸绉掔骇鐨勩€傛瘡涓姛鑳戒竴涓垎鏀紝浜掍笉褰卞搷銆係VN 鍒囧垎鏀緢閲嶏紝鑰屼笖鍚堝苟浠ｇ爜绠€鐩存槸鍣╂ⅵ銆?
*   **绂荤嚎宸ヤ綔**: Git 鍙互鍦ㄦ病缃戠殑鏃跺€欐彁浜や唬鐮侊紙Commit 鍒版湰鍦帮級锛岀瓑鏈夌綉浜嗗啀鎺ㄩ€佸埌鏈嶅姟鍣ㄣ€係VN 娌＄綉灏卞簾浜嗐€?
*   **瀹夊叏鎬?*: Git 姣忎釜浜虹殑鐢佃剳閲岄兘鏈夊畬鏁村浠姐€傛湇鍔″櫒鐐镐簡锛岄殢渚挎壘鍙扮數鑴戝氨鑳芥仮澶嶃€係VN 鏈嶅姟鍣ㄧ偢浜嗕笖娌″浠斤紝椤圭洰灏辨病浜嗐€?

### 1.3 缁撹锛歏ampirefall 璇ラ€夎皝锛?
*   **浠ｇ爜/閰嶇疆**: **蹇呴』鐢?Git**銆傚垎鏀鐞嗗拰鍚堝苟鏄浜哄崗浣滅殑鍒氶渶銆?
*   **缇庢湳澶ц祫婧?(PSD/MAX)**: 
    *   鏂规 A: 缁х画鐢?SVN 绠＄悊婧愭枃浠讹紝瀵煎嚭鍚庣殑璧勬簮 (FBX/PNG) 杩?Git銆?
    *   鏂规 B: 鍏ㄩ潰杞?Git锛屼絾蹇呴』寮€鍚?**Git LFS (Large File Storage)** 骞堕厤缃枃浠堕攣銆?

---

## 2. 馃悪 Git 鏋佺畝涓婃墜鎸囧崡 (缇庢湳/绛栧垝涓撶敤鐗?

**蹇樻帀鍛戒护琛岋紒** 鎴戜滑鎺ㄨ崘浣跨敤 **Sourcetree** 鎴?**GitHub Desktop** 鎴?**TortoiseGit** (灏忎箤榫燂紝闀垮緱璺?SVN 寰堝儚)銆?

### 2.1 鏍稿績姒傚康瀵瑰簲琛?(SVN -> Git)

|          浣犲湪 SVN 鍋氱殑鎿嶄綔          |          鍦?Git 閲岀殑瀵瑰簲鎿嶄綔          |          鍖哄埆          |
|          :---          |          :---          |          :---          |
|          **Update** (鏇存柊)          |          **Pull** (鎷夊彇)          |          娌″尯鍒紝閮芥槸鎶婃湇鍔″櫒鐨勪笢瑗挎媺涓嬫潵銆?         |
|          **Commit** (鎻愪氦)          |          **Commit** (鎻愪氦) + **Push** (鎺ㄩ€?          |          **杩欐槸鏈€澶х殑鍧戯紒** <br />SVN 鎻愪氦灏卞畬浜嬩簡銆?br>Git 鎻愪氦鍙槸瀛樺埌**浣犺嚜宸辩數鑴?*閲岋紝蹇呴』鍐嶇偣涓€涓?**Push** 鎵嶈兘浼犲埌鏈嶅姟鍣ㄧ粰鍒汉鐪嬨€?         |
|          **Revert** (杩樺師)          |          **Discard** / **Reset**          |          鏀惧純淇敼锛岃繕鍘熷埌涓婃鎻愪氦鐨勭姸鎬併€?         |
|          **Lock** (閿佸畾)          |          **LFS Lock**          |          闇€瑕佷笓闂ㄩ厤缃?LFS 鎵嶈兘鐢ㄣ€?         |

### 2.2 鍌荤摐寮忓伐浣滄祦 (Daily Workflow)

鍋囪浣犱娇鐢?**TortoiseGit** (鍥犱负瀹冨拰 SVN 鎿嶄綔鏈€鍍?锛?

#### 绗竴姝ワ細鏃╀笂寮€宸?(Pull)
1.  鍦ㄩ」鐩枃浠跺す涓婂彸閿?-> `TortoiseGit` -> `Pull`銆?
2.  鐐?`OK`銆?

3.  **鐩殑**: 纭繚浣犳嬁鍒扮殑鏄渶鏂扮増鏈紝闃叉鍜屽埆浜哄啿绐併€?

#### 绗簩姝ワ細骞叉椿 (Work)
*   鏀?Excel锛岀敾鍥撅紝鏀瑰満鏅?.. 闅忎究寮勩€?

#### 绗笁姝ワ細涓嬬彮鎻愪氦 (Commit + Push)
1.  鍙抽敭 -> `Git Commit -> "master"`銆?
2.  **鍕鹃€?*浣犱慨鏀圭殑鏂囦欢銆?

3.  鍦?Message 妗嗛噷鍐欙細`art: 淇敼浜嗗惛琛€楝间富瑙掔殑妯″瀷璐村浘`銆?

4.  鐐瑰嚮 `Commit`銆?

5.  **鍏抽敭鍔ㄤ綔**: 姝ゆ椂寮圭獥宸︿笅瑙掍細鏈変竴涓?`Push` 鎸夐挳锛?*涓€瀹氳鐐逛竴涓嬶紒** (鎴栬€?Commit 瀹屽崟鐙彸閿?-> `Push`)銆?

6.  **鐩殑**: 鍙湁 Push 鎴愬姛浜嗭紝浣犵殑涓滆タ鎵嶇畻鐪熸鎻愪氦浜嗐€?

### 2.3 閬囧埌鍐茬獊鎬庝箞鍔烇紵 (Conflict)
*   **鐜拌薄**: Push 澶辫触锛屾彁绀?`Updates were rejected`銆?
*   **鍘熷洜**: 浣犳敼浜?`Data.xlsx`锛屽皬鐜嬩篃鏀逛簡 `Data.xlsx`锛岃€屼笖浠栨瘮浣犲厛 Push銆?
*   **瑙ｅ喅**:
    1.  鍏堢偣 `Pull`銆侴it 浼氳瘯鍥惧悎骞躲€?
    2.  濡傛灉鍚堝苟澶辫触锛屾枃浠朵笂浼氭湁涓劅鍙瑰彿銆?

    3.  **绛栧垝/缇庢湳**: 鍒厡锛佺洿鎺ユ壘绋嬪簭甯繖锛屾垨鑰?*澶囦唤浣犵殑鏂囦欢**锛岃繕鍘?(Revert)锛屾媺鍙栨渶鏂?(Pull)锛屽啀鎶婁綘鐨勬敼鍔ㄨ鐩栦笂鍘汇€?

    4.  **绋嬪簭**: 浣跨敤 Merge Tool 瑙ｅ喅鍐茬獊銆?

## 3. 馃殌 缁欎富绋嬬殑寤鸿锛氬浣曞钩婊戣縼绉伙紵

1.  **淇濈暀 SVN 涔犳儻**: 缁欑編鏈 **TortoiseGit**锛屽洜涓哄彸閿彍鍗曠殑鎿嶄綔涔犳儻鍜?SVN 鍑犱箮涓€鏍凤紝瀛︿範鎴愭湰鏈€浣庛€?
2.  **蹇界暐鏂囦欢閰嶇疆 (.gitignore)**:

    *   鍔″繀鎶?`Library/`, `Temp/`, `Logs/`, `.vs/` 灞忚斀鎺夈€係VN 浠ュ墠鍙兘鎶婅繖浜涘瀮鍦鹃兘浼犱笂鍘讳簡锛孏it 缁濆涓嶈銆?
3.  **LFS 寮哄埗寮€鍚?*:

    *   閰嶇疆 `.gitattributes`锛屾妸 `*.psd`, `*.fbx`, `*.png`, `*.wav` 鍏ㄩ儴璧?LFS銆傚惁鍒?1涓湀鍚庝綘鐨?Git 浠撳簱浼氬ぇ鍒版媺涓嶄笅鏉ャ€?

---

**涓€鍙ヨ瘽鎬荤粨**: 
**Git = SVN + "鏈湴浠撳簱"**銆?
浠ュ墠鏄?`鍐欏畬 -> 涓婁紶`銆?
鐜板湪鏄?`鍐欏畬 -> 瀛樻湰鍦?(Commit) -> 涓婁紶 (Push)`銆?
澶氫簡涓€姝ワ紝浣嗘洿瀹夊叏銆?




