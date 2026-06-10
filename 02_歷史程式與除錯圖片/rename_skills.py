import os
import json

root = r"c:\Users\jacob2024\OneDrive\文件\2026_05_13_工研院_4天_行政與財務流程AI自動化_打造高效能行政財務AI部隊-臺北班\0603_pocase"
skills_dir = os.path.join(root, ".agents", "skills")

rename_map = {
    "course-content-authoring": "2606_課程教材編寫",
    "course-corporate-edition": "2606_企業客製化版本",
    "course-ebook-publishing": "2606_電子書與手冊出版",
    "course-outline-design": "2606_課程大綱設計",
    "green-wilderness-notice": "2606_綠野門市公告範本",
    "static-spa-conversion": "2606_講義網頁化工具",
    "static-spa-interactions": "2606_網頁互動美化加強",
    "teaching-site": "2606_教學網站核心主程式",
    "teaching-site-design-system": "2606_教學網站視覺設計",
    "web-content-audit": "2606_網站檔案一致性檢查",
    "web-visual-assets": "2606_網頁配圖與AI生圖",
    "web-visual-verification": "2606_網頁畫面自動測試"
}

# 1. Rename directories
for old_name, new_name in rename_map.items():
    old_path = os.path.join(skills_dir, old_name)
    new_path = os.path.join(skills_dir, new_name)
    if os.path.exists(old_path):
        try:
            os.rename(old_path, new_path)
            print(f"[RENAME FOLDER] {old_name} -> {new_name}")
        except Exception as e:
            print(f"[ERROR] Renaming folder {old_name}: {e}")
    else:
        print(f"[SKIP] Folder not found: {old_name}")

# 2. Update skills-lock.json
lock_file = os.path.join(root, "skills-lock.json")
if os.path.exists(lock_file):
    try:
        with open(lock_file, "r", encoding="utf-8") as f:
            data = json.load(f)
        
        new_skills = {}
        for key, val in data.get("skills", {}).items():
            if key in rename_map:
                new_key = rename_map[key]
                # Update skillPath inside val
                if "skillPath" in val:
                    # e.g., "course-content-authoring/SKILL.md" -> "2606_課程教材編寫/SKILL.md"
                    val["skillPath"] = val["skillPath"].replace(key + "/", new_key + "/")
                new_skills[new_key] = val
                print(f"[UPDATE LOCK JSON] Key: {key} -> {new_key}")
            else:
                new_skills[key] = val
        
        data["skills"] = new_skills
        
        with open(lock_file, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print("skills-lock.json successfully updated.")
    except Exception as e:
        print(f"[ERROR] Updating skills-lock.json: {e}")
else:
    print("skills-lock.json not found in root.")
