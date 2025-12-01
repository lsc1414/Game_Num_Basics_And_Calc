# 📦 Unity 资产管理实战指南 (Unity Asset Management Guide)

**文档目标：** 解决“包体过大”、“加载过慢”和“资源丢失”的三大顽疾。
**核心理念：** 资产不仅是美术画出来的图，更是内存里实打实的字节。

---

## 1. 👻 Meta 文件：资产的灵魂

很多新手最容易犯的错误就是：**在 Windows 资源管理器里直接删除或移动文件，而不是在 Unity 编辑器里操作。**

*   **原理：** Unity 不通过文件名来引用资源，而是通过 `.meta` 文件里的 **GUID** (全局唯一标识符)。
*   **事故现场：**
    *   你在文件夹里把 `Player.png` 改名为 `Hero.png`。
    *   Unity 找不到 `Player.png` 的 meta 文件，以为它被删了。
    *   Unity 为 `Hero.png` 生成一个新的 meta 文件（新的 GUID）。
    *   **结果：** 场景里所有引用 `Player.png` 的地方全部变成 **Missing (紫红色)**。
*   **铁律：** **永远在 Unity Project 窗口里移动、重命名、删除文件。** 如果必须在外部操作，请确保连同 `.meta` 文件一起操作。

---

## 2. 📉 导入设置：性能优化的第一战场

美术给你的图可能是 4K 的 PNG，音频可能是 50MB 的 WAV。直接用就是灾难。

### 2.1 🖼️ 纹理 (Textures)
*   **Max Size (最大尺寸):**
    *   UI 图片：通常 2048 或 1024 够了。不要让 4K 图进手机包。
    *   **规则：** 永远只用“够用”的尺寸。在 Scene 视图拉近看，不模糊即可。
*   **Compression (压缩格式):**
    *   **PC:** DXT1/DXT5 (Crunched)。
    *   **Android:** ASTC (推荐) 或 ETC2。
    *   **iOS:** ASTC (推荐) 或 PVRTC。
    *   **坑：** 不要选 "True Color" 或 "RGBA 32 bit"，除非是 UI 渐变色出现了严重色阶。压缩能节省 90% 的显存。
*   **Read/Write Enabled:**
    *   **默认关掉！** 除非你要在代码里用 `GetPixel()` 修改图片。开启它会导致内存占用**翻倍**（显存一份，内存一份）。

### 2.2 🔊 音频 (Audio)
*   **Force To Mono (强制单声道):**
    *   **必选！** 除非是 3D 环绕声效。手机外放听不出立体声，勾选这个能省一半内存。
*   **Load Type (加载方式):**
    *   **Decompress On Load:** 适合短音效（UI 点击、枪声）。解压后驻留内存，响应快。
    *   **Compressed In Memory:** 适合中等长度音效。
    *   **Streaming (流式加载):** **背景音乐 (BGM) 必选！** 别把 50MB 的 BGM 一次性加载到内存里，边放边读。

---

## 3. 🚫 Resources 文件夹：甜蜜的陷阱

Unity 有一个特殊的文件夹叫 `Resources`。
*   **用法：** `Resources.Load("Path")`。简单方便。
*   **代价：**
    1.  **启动慢：** 游戏启动时，Unity 会建立一个红黑树索引，把 `Resources` 下所有文件的路径记下来。文件越多，启动黑屏越久。
    2.  **内存无法释放：** 极其容易造成内存泄漏。
    3.  **无法热更：** 打包后就封死在包里了，想改一张图必须重新发包。
*   **结论：** **严禁使用 Resources 文件夹**（除非是极其核心的配置，如 Logo 或启动预制体）。

---

## 4. 🏗️ Addressables：现代化的资源管理

既然 `Resources` 不能用，用什么？官方推荐 **Addressables** 系统。

*   **核心理念：** 通过“地址（字符串）”加载资源，而不管资源是在本地、在服务器、还是在包里。
*   **优势：**
    *   **内存管理：** 自动计算引用计数。引用为 0 时自动卸载（Unload），杜绝内存泄漏。
    *   **热更新 (DLC):** 只要把资源包 (AssetBundle) 扔到服务器上，勾选“Remote”，玩家就能边玩边下载，无需更新 App。
    *   **异步加载：** `Addressables.LoadAssetAsync<GameObject>("Hero")`。
*   **实战建议：** 不要等项目快上线了再切 Addressables，**立项第一天就用**。

---

## 5. 🐘 Git 大文件存储 (LFS)

游戏项目通常包含巨大的二进制文件（PSD, FBX, MP4）。
*   **问题：** Git 擅长处理代码（文本），不擅长处理大文件。每次修改 PSD，Git 都会存一份完整的副本，仓库迅速膨胀到 10GB+。
*   **解法：** 使用 **Git LFS (Large File Storage)**。
*   **配置 (`.gitattributes`):**
    ```text
    *.psd filter=lfs diff=lfs merge=lfs -text
    *.fbx filter=lfs diff=lfs merge=lfs -text
    *.wav filter=lfs diff=lfs merge=lfs -text
    *.mp4 filter=lfs diff=lfs merge=lfs -text
    ```
*   **效果：** Git 仓库里只存一个指针（几KB），真正的文件存在专门的 LFS 服务器上。拉取速度飞快。

---

## 6. 🧹 资产清理与维护

*   **查找引用 (Find References):**
    *   右键资源 -> "Find References In Scene"。
    *   推荐插件：**Reference Finder**。能帮你找出“哪些图片从来没被用过”，然后放心删除。
*   **重复资源 (Duplicates):**
    *   经常出现这种情况：A 目录里有一份 `Button.png`，B 目录里也有一份一模一样的。
    *   这会导致包体变大，内存浪费。定期检查重复文件。

---

## 7. 🏷️ 命名规范 (Naming Convention)

没有规范，就是混乱的开始。

*   **资源前缀 (Prefix):**
    *   `T_Icon_Sword.png` (Texture)
    *   `M_Metal.mat` (Material)
    *   `S_Explosion.wav` (Sound)
    *   `P_Goblin.prefab` (Prefab)
*   **好处：** 在搜索框里搜 `t:Texture Sword` 就能精准找到图片，而不是材质球。
