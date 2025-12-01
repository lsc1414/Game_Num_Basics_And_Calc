# 🎨 UI/UX 设计与交互规范 (Interface Guidelines)

本文档定义了 Project Vampirefall 的用户界面风格、层级结构及交互反馈标准。

---

## 1. 视觉风格 (Visual Style)

*   **关键词:** 哥特 (Gothic)、极简 (Minimalist)、血与金 (Blood & Gold)。
*   **色板 (Palette):**
    *   *Primary:* 深红 (#8B0000) - 生命，危险，强调。
    *   *Secondary:* 暗金 (#B8860B) - 稀有度，货币，UI 边框。
    *   *Background:* 炭黑 (#1A1A1A) 带噪点纹理 - 面板背景。
    *   *Text:* 乳白 (#F5F5F5) - 正文； 灰色 (#808080) - 辅助说明。
*   **字体:**
    *   *标题:* Serif (衬线体)，类似 Cinzel，营造史诗感。
    *   *正文:* Sans-Serif (无衬线)，类似 Roboto/Inter，保证易读性。

## 2. 界面层级 (Layer Hierarchy)

Unity Canvas 的 `Sorting Order` 规划：

1.  **World Space UI (Order -10):** 
    *   血条 (Health Bars)、伤害飘字 (Floating Text)。跟随单位移动。
2.  **Gameplay HUD (Order 0):** 
    *   技能栏、小地图、任务追踪。常驻屏幕。
3.  **Windows / Panels (Order 100):** 
    *   背包、角色面板、商店。打断操作，半透明背景遮罩。
4.  **Popups / Dialogs (Order 500):** 
    *   确认框 ("Are you sure?"), 剧情对话。模态窗口 (Modal)。
5.  **System Overlay (Order 1000):** 
    *   Loading 界面、网络断开提示、版本号水印。

## 3. 交互反馈 (Interaction Feedback)

好的 UI 必须是“活”的。

### 3.1 按钮状态 (Button States)
*   **Normal:** 默认状态。
*   **Hover:** 亮度 +20%，轻微放大 (Scale 1.05)，播放 "Hover_Tick" 音效。
*   **Pressed:** 亮度 -20%，稍微下沉 (Scale 0.95)，播放 "Click_Confirm" 音效。
*   **Disabled:** 灰度化 (Grayscale)，透明度 50%，不响应射线。

### 3.2 拾取反馈 (Loot Feedback)
*   当拾取物品时，UI 上不仅要有文字提示，物品图标应有一个从世界坐标飞向背包按钮的 **Trail 动画**。

### 3.3 伤害飘字 (Floating Combat Text)
*   为了避免遮挡，采用 **动态堆叠算法**:
    *   **普通伤害:** 白色，小字，向周围随机散开。
    *   **暴击 (Crit):** 黄色/橙色，大字，加粗，震动一下。
    *   **状态 (Status):** 文字提示 (e.g., "Ignited!"), 对应元素颜色。

## 4. 适配与布局 (Responsive Layout)

*   **锚点 (Anchors):** 所有 HUD 元素必须吸附屏幕边缘（左上、右下等）。
*   **安全区 (Safe Area):** 考虑到手机/主机可能有刘海或过扫描，UI 元素应保留 5% 的边距 (Padding)。
*   **比例缩放:** 
    *   PC: 保持 UI 物理尺寸适中。
    *   Steam Deck: UI 整体缩放系数 x1.2，确保 7寸屏可见。

