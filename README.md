# Jacob Studio — Apple 風格設計師個人作品集

一個採用 Apple 設計語言打造的設計師個人首頁，支援 PWA（可安裝至手機桌面）、手機自動跳轉與照片滑鼠特效。

🌐 **線上預覽：** https://jacobshih2024.github.io/teaching-site/

---

## 目錄結構

```
0603_pocase/
│
├── index.html                       # 🖥️  桌機版主頁
├── m.index.html                     # 📱  手機版主頁（PWA）
├── manifest.webmanifest             # PWA 安裝設定
├── sw.js                            # Service Worker（離線快取）
├── icon-192.svg                     # App 圖示（小）
├── icon-512.svg                     # App 圖示（大）
├── 2025JACOB.jpg                    # 主要個人照片
├── 2025JACOB02.jpg                  # 聯絡區塊背景照片
├── README.md                        # 本說明文件
│
├── 04_Apple風格設計師個人首頁/       # 📂 完整備份資料夾
│   ├── index.html
│   ├── m.index.html
│   ├── manifest.webmanifest
│   ├── sw.js
│   ├── icon-192.svg / icon-512.svg
│   ├── 2025JACOB.jpg / 2025JACOB02.jpg
│   └── jacob/                       # 原始照片來源
│
├── 03_第一版GitHub網頁資料/          # 📂 第一版深色風格（參考備份）
├── 02_歷史程式與除錯圖片/            # 📂 開發過程截圖
└── 01_測試與範例照片庫/              # 📂 測試用照片
```

---

## 功能說明

| 功能 | 說明 |
|------|------|
| Apple 風格設計 | 白底、SF Pro 字型、咖啡棕金主色 `#A0784A` |
| 照片滑鼠特效 | 黑白 → 馬賽克 → 白 → 黑 → 換照片 |
| 手機自動跳轉 | 偵測到手機裝置自動導向 `m.index.html` |
| PWA 安裝 | 手機瀏覽後可「加入主畫面」成為 App |
| 離線瀏覽 | Service Worker 快取，無網路也能開啟 |

---

## 如何在本機執行

### 方法一：VS Code Live Server（推薦）
1. 安裝 VS Code 擴充套件 **Live Server**
2. 在 VS Code 開啟 `index.html`
3. 右下角點 **Go Live**
4. 瀏覽器自動開啟 `http://127.0.0.1:5500/index.html`

### 方法二：直接開啟
直接雙擊 `index.html` 在瀏覽器開啟

---

## 替換個人照片

1. 把主照片命名為 `2025JACOB.jpg`，聯絡區背景命名為 `2025JACOB02.jpg`
2. 放入專案根目錄，覆蓋原有檔案
3. 重新整理瀏覽器即可

> 建議尺寸：正方形（1:1）或直式（3:4），解析度 1000px 以上

---

## 用 Python 修改內容（初學者適用）

> 不需安裝任何額外套件，Python 內建功能即可完成。
> 確認已安裝 Python 3：在終端機輸入 `python --version`

---

### 修改姓名

```python
# 把所有「JACOB」改成你的名字

old_name = "JACOB"
new_name = "你的名字"   # ← 改這裡

for filename in ["index.html", "m.index.html"]:
    with open(filename, "r", encoding="utf-8") as f:
        content = f.read()
    content = content.replace(old_name, new_name)
    with open(filename, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"✅ {filename} 修改完成")
```

---

### 修改 Email

```python
old_email = "2005jacob@gmail.com"
new_email = "你的email@gmail.com"   # ← 改這裡

for filename in ["index.html", "m.index.html"]:
    with open(filename, "r", encoding="utf-8") as f:
        content = f.read()
    content = content.replace(old_email, new_email)
    with open(filename, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"✅ {filename} Email 已更新")
```

---

### 修改主色（咖啡棕金 → 你的品牌色）

```python
old_color = "#A0784A"
new_color = "#0071e3"   # ← 改這裡（換成你喜歡的顏色，例如藍色）

# 同時也要換 rgba 格式的顏色
old_rgb = "160, 120, 74"
new_rgb = "0, 113, 227"  # ← 對應 new_color 的 RGB 值

for filename in ["index.html", "m.index.html"]:
    with open(filename, "r", encoding="utf-8") as f:
        content = f.read()
    content = content.replace(old_color, new_color)
    content = content.replace(old_rgb, new_rgb)
    with open(filename, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"✅ {filename} 主色已更新")
```

---

### 修改自我介紹文字

```python
old_text = "我是 JACOB，一位專注於品牌識別、網站介面與數位體驗的設計師。"
new_text = "我是 ＿＿＿，一位專注於＿＿＿的設計師。"   # ← 改這裡

for filename in ["index.html", "m.index.html"]:
    with open(filename, "r", encoding="utf-8") as f:
        content = f.read()
    content = content.replace(old_text, new_text)
    with open(filename, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"✅ {filename} 自介已更新")
```

---

### 修改數據（完成專案數、客戶數、年資）

```python
changes = {
    "200+": "150+",   # 完成專案數 ← 改這裡
    "600":  "80",     # 合作客戶數 ← 改這裡
    "25Y":  "10Y",    # 設計年資   ← 改這裡
}

for filename in ["index.html", "m.index.html"]:
    with open(filename, "r", encoding="utf-8") as f:
        content = f.read()
    for old, new in changes.items():
        content = content.replace(old, new)
    with open(filename, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"✅ {filename} 數據已更新")
```

---

### 一鍵完成所有個人化設定

```python
# setup_my_portfolio.py
# 把下方資料填好，執行一次完成所有設定

MY_NAME   = "你的名字"                    # ← 填你的名字
MY_EMAIL  = "you@gmail.com"              # ← 填你的 Email
MY_ROLE   = "品牌設計師 / UI Designer"   # ← 填你的職稱
MY_INTRO  = "我是 ＿，專注於＿＿＿。"    # ← 填自我介紹

replacements = {
    "JACOB":                                                            MY_NAME,
    "2005jacob@gmail.com":                                              MY_EMAIL,
    "品牌設計師 / UI Designer / Art Direction":                          MY_ROLE,
    "我是 JACOB，一位專注於品牌識別、網站介面與數位體驗的設計師。":           MY_INTRO,
}

for filename in ["index.html", "m.index.html"]:
    with open(filename, "r", encoding="utf-8") as f:
        content = f.read()
    for old, new in replacements.items():
        content = content.replace(old, new)
    with open(filename, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"✅ {filename} 個人化完成")

print("\n🎉 全部設定完成！用瀏覽器開啟 index.html 確認結果。")
```

---

## 上傳到 GitHub

```bash
git add .
git commit -m "更新個人資料"
git push origin main
```

---

## 技術說明

| 技術 | 用途 |
|------|------|
| HTML / CSS | 頁面結構與樣式 |
| JavaScript | 照片切換特效、手機跳轉 |
| PWA | 手機安裝、離線快取 |
| Service Worker | 背景快取所有靜態檔案 |
| GitHub Pages | 免費靜態網站託管 |

---
---

# 📄 行政與財務流程AI自動化：白板日期批次無痕修改工具 🚀
> **—— 小白也能輕鬆上手的白板照片日期批次自動化影像處理指南！**

本專案是用於自動化批次修改工程、呈報或巡檢照片中**「白板日期與月份」**的工具。 
透過先進的影像處理與 AI 自動調和技術，工具能自動尋找年份、算好位置、**無痕抹除舊字跡（完美避開並保護白板的黑色格線）**，並把新的手寫字體（PSD 或 PNG）**無縫融入白板**上，保留真實的光影與質感！

---

## 📂 專案目錄結構

以下為您盤點本專案整理後的檔案結構，方便您快速尋找與放置檔案：

```text
0603_pocase/
├── .agents/
│   └── skills/                       # 🛠️ AI 助理的核心技能庫（包含三大白板功能與系統內建技能）
│       ├── 改月份程式/                # 核心腳本 1：【改月份】（手寫字正片疊底）
│       ├── 月份空白/                  # 核心腳本 2：【月份空白】（僅抹除留白）
│       ├── 月份+日期空白/             # 核心腳本 3：【月份+日期空白】（雙欄位淨空）
│       ├── 2606_課程教材編寫/          # 系統內建技能（英文原名：course-content-authoring）
│       ├── 2606_企業客製化版本/        # 系統內建技能（英文原名：course-corporate-edition）
│       ├── 2606_電子書與手冊出版/      # 系統內建技能（英文原名：course-ebook-publishing）
│       ├── 2606_課程大綱設計/          # 系統內建技能（英文原名：course-outline-design）
│       ├── 2606_綠野門市公告範本/      # 系統內建技能（英文原名：green-wilderness-notice）
│       ├── 2606_講義網頁化工具/        # 系統內建技能（英文原名：static-spa-conversion）
│       ├── 2606_網頁互動美化加強/      # 系統內建技能（英文原名：static-spa-interactions）
│       ├── 2606_教學網站核心主程式/    # 系統內建技能（英文原名：teaching-site）
│       ├── 2606_教學網站視覺設計/      # 系統內建技能（英文原名：teaching-site-design-system）
│       ├── 2606_網站檔案一致性檢查/    # 系統內建技能（英文原名：web-content-audit）
│       ├── 2606_網頁配圖與AI生圖/      # 系統內建技能（英文原名：web-visual-assets）
│       └── 2606_網頁畫面自動測試/      # 系統內建技能（英文原名：web-visual-verification）
├── 01_測試與範例照片庫/               # 📁 【照片與範例】收納所有原始照片、測試照片與 PSD 模板 (已全部歸類)
│   ├── case001/                      # 📁 測試範例原始資料夾
│   ├── 測試SKILLS_004-...            # 📁 測試案例 004（1月 改 5月）
│   ├── 測試SKILLS_ok_026-...         # 📁 測試案例 026（5月 改 6月）
│   ├── 測試SKILLS_043-...            # 📁 測試案例 043（5月 改 8月）
│   ├── 測試SKILLS_08/                # 📁 測試案例 08（1月 改 8月）
│   ├── 測試SKILLS_08_2/              # 📁 測試案例 08_2（1月 改 9月）
│   ├── 測試SKILLS_08_空白/           # 📁 測試案例 08_空白（單純抹除月份，留白）
│   └── 測試SKILLS_08_雙空白/         # 📁 測試案例 08_雙空白（同時抹除月份與日期，留白）
├── 02_歷史程式與除錯圖片/             # 📁 【歷史程式】收納所有舊腳本、除錯產生的測試圖片與歷程
├── 03_第一版GitHub網頁資料/           # 📁 【發布網頁】收納第一版發布到 GitHub Pages 的電腦版/手機版網頁檔案
├── README.md                         # 📄 本說明文件（本檔，初學者自學寶典）
└── skills-lock.json                  # ⚙️ AI 技能鎖定設定檔（請務必保留在根目錄，請勿移動）
```

### 📋 系統內建技能資料夾中英對照表

若要了解那些前綴為 `2606_` 的系統內建技能功能，可參考下表：

| 📂 中文命名資料夾 (已修改) | 📂 英文原名 (已對照) | 💡 功能簡介 |
|---|---|---|
| **`2606_課程教材編寫`** | `course-content-authoring` | 用於填寫教學講義、筆記、小測驗與範本內容。 |
| **`2606_企業客製化版本`** | `course-corporate-edition` | 用於將公開課講義，快速濃縮包裝成企業專屬一日班。 |
| **`2606_電子書與手冊出版`** | `course-ebook-publishing` | 用於將講義網頁匯出，印製成 PDF 電子書或 DOCX 手冊。 |
| **`2606_課程大綱設計`** | `course-outline-design` | 用於規劃課程的學習目標、章節骨架與時間分配。 |
| **`2606_綠野門市公告範本`** | `green-wilderness-notice` | 生成綠野選物總部發送門市同仁的培訓與行政 Email 範本。 |
| **`2606_講義網頁化工具`** | `static-spa-conversion` | 將 Markdown 講義內容直接轉化為單頁網頁 (SPA) 功能。 |
| **`2606_網頁互動美化加強`** | `static-spa-interactions` | 為靜態講義網頁增加暗色模式、進度追蹤、手機版收合等互動功能。 |
| **`2606_教學網站核心主程式`** | `teaching-site` | 用於建立、規劃互動式多天課程教學網站的核心程式。 |
| **`2606_教學網站視覺設計`** | `teaching-site-design-system` | 統一設定教學網站的色彩、字體、卡片版面等視覺風格。 |
| **`2606_網站檔案一致性檢查`** | `web-content-audit` | 自動化盤點網站資料、檢查缺圖、對照 Markdown 與資料結構。 |
| **`2606_網頁配圖與AI生圖`** | `web-visual-assets` | 用於製作網站中的配圖、講師卡、AI繪圖插圖與 QR 碼。 |
| **`2606_網頁畫面自動測試`** | `web-visual-verification` | 透過 Playwright 自動模擬點擊，測試網頁在手機與電腦版是否正常。 |

---

## 🛠️ 新手準備工作（只要 3 步，完全免費）

### 步驟 1：安裝 Python 程式語言
若您的電腦尚未安裝 Python，請至 [Python 官方網站下載](https://www.python.org/downloads/) 並進行安裝。
> ⚠️ **重要提示（小白必看）**：安裝時請務必勾選 **"Add Python to PATH"**（將 Python 新增至環境變數），否則後面執行指令時會出現「找不到指令」的錯誤！

### 步驟 2：一鍵安裝影像處理庫
在您的 Windows 鍵盤上按下 `Win + R`，輸入 `cmd` 或 `powershell` 打開終端機，複製並貼上下列指令後按 Enter 鍵執行：
```bash
pip install opencv-python numpy psd-tools
```
這會自動幫您安裝程式所需的三個免費影像庫（OpenCV 用於影像修補，NumPy 用於數學計算，psd-tools 用於解析 Photoshop PSD 檔案）。

### 步驟 3：開啟專案目錄
在檔案瀏覽器中進入 `0603_pocase` 資料夾，在視窗上方路徑列輸入 `powershell` 並按下 Enter，即可在該目錄直接打開指令視窗。

---

## 🚀 三大功能指令大全

> 💡 **小撇步**：程式執行完畢後，所有處理好的照片都會自動存在該資料夾底下的 **`OKK` 子資料夾** 中，檔名尾數會加上 `_ok.jpg`。**原始照片完全不會被覆蓋，非常安全！**

### 功能一：【改月份】（抹除舊月份並疊加新月份字體）
用於將舊的月份抹去，並自動對齊、縮放與混合新的透明月份數字模板。

| 測試案例資料夾 | 目標白板版面 | 替換動作 | 完整執行指令 (直接複製即可) |
|---|---|---|---|
| **測試SKILLS_004** | 頂崁里排版 1 | 1月 ➡️ **5月** | `python .agents/skills/改月份程式/modify_month.py --folder "01_測試與範例照片庫\測試SKILLS_004-頂崁里-廢棄物清除呈報-115.05.13" --template "01_測試與範例照片庫\case001\0513.psd" --psd-layer 1 --ref-image "01_測試與範例照片庫\case001\test_004-頂崁里-廢棄物清除呈報-115.05.13\LINE_ALBUM_頂崁里廢棄物呈報_260128_41.jpg"` |
| **測試SKILLS_ok_026** | 同慶里排版 | 5月 ➡️ **6月** | `python .agents/skills/改月份程式/modify_month.py --folder "01_測試與範例照片庫\測試SKILLS_ok_026-同慶里-廢棄物清除呈報-115.05.06" --template "01_測試與範例照片庫\測試SKILLS_ok_026-同慶里-廢棄物清除呈報-115.05.06\06.psd" --psd-layer 1 --ref-image "01_測試與範例照片庫\測試SKILLS_ok_026-同慶里-廢棄物清除呈報-115.05.06\LINE_ALBUM_同慶里廢棄物呈報_260311_2.jpg" --year-bbox "590,625,230,290" --month-bbox "590,615,300,335"` |
| **測試SKILLS_043** | 永興里排版 | 5月 ➡️ **8月** | `python .agents/skills/改月份程式/modify_month.py --folder "01_測試與範例照片庫\測試SKILLS_043-永興里-廢棄物清除呈報-115.05.06" --template "01_測試與範例照片庫\測試SKILLS_043-永興里-廢棄物清除呈報-115.05.06\08.psd" --psd-layer 1 --ref-image "01_測試與範例照片庫\測試SKILLS_043-永興里-廢棄物清除呈報-115.05.06\LINE_ALBUM_永興里廢棄物呈報_260311_2.jpg" --year-bbox "590,623,190,240" --month-bbox "590,615,280,310" --month-thresh 0.70` |
| **測試SKILLS_08** | 頂崁里排版 2 | 1月 ➡️ **8月** | `python .agents/skills/改月份程式/modify_month.py --folder "01_測試與範例照片庫\測試SKILLS_08" --template "01_測試與範例照片庫\測試SKILLS_08\08_OK.psd" --psd-layer 1 --ref-image "01_測試與範例照片庫\測試SKILLS_08\LINE_ALBUM_頂崁里廢棄物呈報_260128_2.jpg" --year-bbox "595,625,155,210" --month-bbox "595,620,235,260"` |
| **測試SKILLS_08_2** | 頂崁里排版 2 | 1月 ➡️ **9月** | `python .agents/skills/改月份程式/modify_month.py --folder "01_測試與範例照片庫\測試SKILLS_08_2" --template "01_測試與範例照片庫\測試SKILLS_08_2\09.psd" --psd-layer 3 --ref-image "01_測試與範例照片庫\測試SKILLS_08_2\LINE_ALBUM_頂崁里廢棄物呈報_260128_2.jpg" --year-bbox "595,625,155,210" --month-bbox "595,620,235,260"` |

---

### 功能二：【月份空白】（僅抹除月份數字，留白淨空）
用於單純將月份欄位的手寫數字清除為乾淨的白板背景，不融合新數字。

* **執行範例（頂崁里白板 - 抹除 1 月份）：**
  ```powershell
  python .agents/skills/月份空白/erase_month.py --folder "01_測試與範例照片庫\測試SKILLS_08_空白" --ref-image "01_測試與範例照片庫\測試SKILLS_08_空白\LINE_ALBUM_頂崁里廢棄物呈報_260128_2.jpg" --year-bbox "595,625,155,210" --month-bbox "595,620,235,260"
  ```

---

### 功能三：【月份+日期空白】（同時抹除月份與日期數字，雙欄位淨空）
用於將白板上的「月份」與「日期（日）」這兩個手寫數字同時擦除，讓兩個欄位一起變乾淨留白。

* **執行範例（頂崁里白板 - 同時抹除 1月 與 13日）：**
  ```powershell
  python .agents/skills/月份+日期空白/erase_date.py --folder "01_測試與範例照片庫\測試SKILLS_08_雙空白" --ref-image "01_測試與範例照片庫\測試SKILLS_08_雙空白\LINE_ALBUM_頂崁里廢棄物呈報_260128_2.jpg" --year-bbox "595,625,155,210" --month-bbox "595,620,235,260" --day-bbox "595,620,290,325"
  ```

---

## 🎨 新白板排版測量與 PSD 數字製作指南

### 1. 如何測量新白板的 `--year-bbox` 與 `--month-bbox` 座標？
如果您遇到全新的白板排版，只需要用 Windows 內建的**「小畫家」**開啟基準參考照片（ref-image），滑鼠指到目標文字上：
1. **測量年份「115.」或「115」的範圍**：
   * 將滑鼠移到年份區域的**最上方**和**最下方**，觀察小畫家視窗**左下角**顯示的 `Y` 座標值。例如：上方為 `595`，下方為 `625`。這就是我們的高（`ymin, ymax` = `595,625`）。
   * 將滑鼠移到年份最左側（`1` 字開頭）與最右側（點 `.` 結束），記錄 `X` 座標值。例如：最左為 `155`，最右為 `210`。這就是我們的寬（`xmin, xmax` = `155,210`）。
   * 將這四個數字寫成：`"595,625,155,210"`。這就是年份座標 `--year-bbox`！
2. **用同樣的方法測量月份欄位座標**（例如原來的 1 月）：
   * 滑鼠對準 1 月字跡周圍，量出高度範圍（例如 `595` 到 `620`）與寬度範圍（例如 `235` 到 `260`）。
   * 寫成：`"595,620,235,260"`。這就是月份座標 `--month-bbox`！

### 2. 怎麼準備透明數字模板？
* **Photoshop PSD 格式**：
  * 新建一個小畫布（例如 50x50 或 100x100 像素）。
  * 拿黑色的手繪筆刷工具寫下數字（例如 `9`），**背景必須是透明的**。
  * 儲存為 PSD 檔案。在執行程式時，需加上 `--psd-layer <圖層編號>`。
  * *如何知道圖層編號？* 程式會自動解析並在終端機印出圖層列表，通常最上面的字跡圖層是圖層 1 或 3，背景圖層是圖層 0。
* **透明 PNG 格式**（更直覺）：
  * 直接把寫有黑色字體的透明 PNG 數字圖片，作為 `--template` 參數傳入，此時**不需下** `--psd-layer` 參數。

---

## 🧑‍💻 初學者自學：如何自行修改 Python 腳本？

如果您想要調整字跡的濃淡、修改擦除的乾淨度，可以直接使用「記事本」或 Notepad++ 打開對應的 Python 腳本進行修改：

### 1. 調整預設的字體透明度（深淺）
如果您覺得新寫上去的字體太淡或太深：
* **免改 Code 的做法**：在執行指令的最後面加上 `--opacity 0.60` (數值越小越透明，0.0 到 1.0 之間)。
* **直接修改腳本**：
  * 打開 `modify_month.py` 找到 **第 42 行**：
    ```python
    parser.add_argument("--opacity", type=float, default=0.62, ...)
    ```
  * 將其中的 `default=0.62` 修改為您想要的預設透明度值（例如 `0.55` 代表 55% 的不透明度）。

### 2. 調整自動明暗度 (Auto-Opacity) 的上下限
程式會自動讀取照片中原本「115」年份手寫字跡的濃淡，自動讓融合進去的「8」或「9」跟原本字跡一樣濃淡。
* **直接修改腳本**：
  * 打開 `modify_month.py` 找到 **第 251 行** 附近：
    ```python
    # Clip to natural range [0.35, 0.85]
    current_opacity = float(np.clip(contrast_ratio, 0.35, 0.85))
    ```
  * 如果您發現某些大太陽底下的照片，自動調整後字體太淡了，可以把最低下限 `0.35` 提高，例如改為：`np.clip(contrast_ratio, 0.45, 0.85)`。
  * 若要強行停用此自動調整，在執行指令後面加上 `--no-auto-opacity` 即可。

### 3. 字跡殘留陰影？讓橡皮擦範圍變大
當字跡筆劃較粗，抹除後可能殘留原本邊緣。
* **直接修改腳本**：
  * 打開 `modify_month.py` / `erase_month.py` 找到這段：
    ```python
    # Dilate to ensure the entire stroke boundary is clean
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    stroke_mask_dilated = cv2.dilate(stroke_mask, kernel, iterations=2)
    ```
  * 將其中 `iterations=2`（膨脹次數 2）修改為 `iterations=3` 或是 `4`，遮罩就會擴大，把更粗的毛邊全部擦除乾淨。

### 4. 保護白板底部黑色框線的像素列數
若白板框線距離字體太近，擴張遮罩時可能稍微擦到了框線。
* **直接修改腳本**：
  * 在所有程式碼（如 `erase_date.py`）中，我們加上了格線保護機制：
    ```python
    # Protect horizontal grid line at the bottom
    protect_h = max(1, int(3 * scale_y))
    if stroke_mask_dilated_m.shape[0] > protect_h:
        stroke_mask_dilated_m[-protect_h:, :] = 0
    ```
  * 如果您的框線距離字跡非常遠，想要完全不保護以利把字跡寫在很下方，可以把 `3` 改為 `0`；如果框線被切掉一小部分，可以把 `3` 改為 `4` 或 `5` 像素。

---

## 🙋 常見問與答 (FAQ)

#### Q1：執行後一直顯示 `[SKIP] ... (Year not found, max year confidence: 0.5200)`？
* **原因**：表示程式找不到白板上的「115」年份標記，信心度只有 52%（低於預設門檻 70%）。這通常是照片拍攝角度太斜、反光太嚴重或太模糊。
* **解決辦法**：在指令後方加上 `--year-thresh 0.50`。這會把門檻降到 50%，程式就會放寬標準，重新捕捉到年份。

#### Q2：可以批次處理其他副檔名例如 `.png` 或是 `.jpeg` 嗎？
* **原因**：預設程式會搜尋資料夾中的 `.jpg`。
* **解決辦法**：用文字編輯器打開腳本，搜尋 `*.jpg` 並將其改為 `*.png` 或您需要的格式副檔名。
