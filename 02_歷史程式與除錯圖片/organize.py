import os
import shutil
import glob

root = r"c:\Users\jacob2024\OneDrive\文件\2026_05_13_工研院_4天_行政與財務流程AI自動化_打造高效能行政財務AI部隊-臺北班\0603_pocase"

# Create directories
test_db_dir = os.path.join(root, "01_測試與範例照片庫")
history_dir = os.path.join(root, "02_歷史程式與除錯圖片")

os.makedirs(test_db_dir, exist_ok=True)
os.makedirs(history_dir, exist_ok=True)

# 1. Move root-level test folders
root_test_folders = [
    "測試SKILLS_08",
    "測試SKILLS_08_2",
    "測試SKILLS_08_空白",
    "測試SKILLS_08_雙空白"
]

for f in root_test_folders:
    src = os.path.join(root, f)
    dst = os.path.join(test_db_dir, f)
    if os.path.exists(src):
        try:
            shutil.move(src, dst)
            print(f"[MOVE] Root Folder: {f} -> 01_測試與範例照片庫")
        except Exception as e:
            print(f"[ERROR] Moving {f}: {e}")

# 2. Move inner case001 test folders
case001_dir = os.path.join(root, "case001")
inner_test_folders = [
    "測試SKILLS_004-頂崁里-廢棄物清除呈報-115.05.13",
    "測試SKILLS_ok_026-同慶里-廢棄物清除呈報-115.05.06",
    "測試SKILLS_043-永興里-廢棄物清除呈報-115.05.06"
]

if os.path.exists(case001_dir):
    for f in inner_test_folders:
        src = os.path.join(case001_dir, f)
        dst = os.path.join(test_db_dir, f)
        if os.path.exists(src):
            try:
                shutil.move(src, dst)
                print(f"[MOVE] Case001 Inner Folder: {f} -> 01_測試與範例照片庫")
            except Exception as e:
                print(f"[ERROR] Moving inner {f}: {e}")
                
    # Now move case001 itself to test_db
    try:
        shutil.move(case001_dir, os.path.join(test_db_dir, "case001"))
        print("[MOVE] Folder: case001 -> 01_測試與範例照片庫")
    except Exception as e:
        print(f"[ERROR] Moving case001: {e}")

# 3. Move other folders to history
folders_to_history = [
    "008_2",
    "debug_thumbs",
    "green-wilderness-notice",
    "jacob",
    "scratch"
]

for f in folders_to_history:
    src = os.path.join(root, f)
    dst = os.path.join(history_dir, f)
    if os.path.exists(src):
        try:
            shutil.move(src, dst)
            print(f"[MOVE] Folder: {f} -> 02_歷史程式與除錯圖片")
        except Exception as e:
            print(f"[ERROR] Moving folder {f}: {e}")

# 4. Move loose python files in root (except this script itself)
this_script = "organize.py"
for f in glob.glob(os.path.join(root, "*.py")):
    basename = os.path.basename(f)
    if basename == this_script:
        continue
    dst = os.path.join(history_dir, basename)
    try:
        shutil.move(f, dst)
        print(f"[MOVE] File: {basename} -> 02_歷史程式與除錯圖片")
    except Exception as e:
        print(f"[ERROR] Moving file {basename}: {e}")

# 5. Move loose png files in root
for f in glob.glob(os.path.join(root, "*.png")):
    basename = os.path.basename(f)
    dst = os.path.join(history_dir, basename)
    try:
        shutil.move(f, dst)
        print(f"[MOVE] File: {basename} -> 02_歷史程式與除錯圖片")
    except Exception as e:
        print(f"[ERROR] Moving file {basename}: {e}")

print("\nWorkspace organization script finished running.")
