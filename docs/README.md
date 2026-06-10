# docs/ — Apple 風格設計師個人作品集

採用 Apple 設計語言打造的設計師個人首頁，支援 PWA、手機自動跳轉與照片滑鼠特效。

🌐 **線上預覽：** https://jacobshih2024.github.io/teaching-site/

---

## 檔案說明

| 檔案 | 說明 |
|------|------|
| `index.html` | 桌機版主頁 |
| `m.index.html` | 手機版主頁（PWA） |
| `manifest.webmanifest` | PWA 安裝設定 |
| `sw.js` | Service Worker（離線快取） |
| `icon-192.svg / icon-512.svg` | App 圖示 |
| `2025JACOB.jpg` | 主要個人照片 |
| `2025JACOB02.jpg` | 聯絡區塊背景照片 |
| `jacob/` | 原始照片來源資料夾 |

---

## 功能說明

| 功能 | 說明 |
|------|------|
| Apple 風格設計 | 白底、SF Pro 字型、咖啡棕金主色 `#A0784A` |
| 照片滑鼠特效 | 黑白 → 馬賽克 → 白 → 黑 → 換照片（110% 放大） |
| 手機自動跳轉 | 偵測到手機裝置自動導向 `m.index.html` |
| PWA 安裝 | 手機瀏覽後可「加入主畫面」成為 App |
| 離線瀏覽 | Service Worker 快取，無網路也能開啟 |

---

## 如何在本機執行

1. 安裝 VS Code 擴充套件 **Live Server**
2. 開啟 `index.html`，右下角點 **Go Live**
3. 瀏覽器自動開啟 `http://127.0.0.1:5500/docs/index.html`

---

## 替換個人照片

1. 把主照片命名為 `2025JACOB.jpg`，聯絡區背景命名為 `2025JACOB02.jpg`
2. 放入 `docs/` 目錄，覆蓋原有檔案
3. 重新整理瀏覽器即可

> 建議尺寸：正方形（1:1）或直式（3:4），解析度 1000px 以上

---

## 用 Python 修改內容（初學者適用）

> 在 `docs/` 目錄下執行以下腳本。確認已安裝 Python 3：`python --version`

### 修改姓名

```python
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

### 修改主色（咖啡棕金 → 你的品牌色）

```python
old_color = "#A0784A"
new_color = "#0071e3"   # ← 改這裡

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

### 一鍵完成所有個人化設定

```python
# setup_my_portfolio.py — 在 docs/ 目錄下執行

MY_NAME   = "你的名字"
MY_EMAIL  = "you@gmail.com"
MY_ROLE   = "品牌設計師 / UI Designer"
MY_INTRO  = "我是 ＿，專注於＿＿＿。"

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
| GitHub Pages | 免費靜態網站託管（從 `/docs` 部署） |
