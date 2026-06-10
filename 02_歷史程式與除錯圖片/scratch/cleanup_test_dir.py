import os
import glob
import shutil

test_dir = r"測試SKILLS_004-頂崁里-廢棄物清除呈報-115.05.13"
source_dir = r"case001\test_004-頂崁里-廢棄物清除呈報-115.05.13"

# 1. List all files in the test directory
files = os.listdir(test_dir)

# 2. Delete LINE_ALBUM_*.jpg files where the number is > 10 or ends with _ok.jpg
for f in files:
    if f.startswith("LINE_ALBUM_") and f.endswith(".jpg"):
        # Extract number
        # Filename format: LINE_ALBUM_頂崁里廢棄物呈報_260128_X.jpg or LINE_ALBUM_頂崁里廢棄物呈報_260128_X_ok.jpg
        name_part = f.replace("LINE_ALBUM_頂崁里廢棄物呈報_260128_", "").replace(".jpg", "")
        if name_part.endswith("_ok"):
            # Delete _ok files to clean up
            os.remove(os.path.join(test_dir, f))
            print(f"Deleted output file: {f}")
            continue
            
        try:
            num = int(name_part)
            if num > 10:
                os.remove(os.path.join(test_dir, f))
                print(f"Deleted extra file: {f}")
        except ValueError:
            # Not a simple number, could be modified or different format, delete just to be safe
            pass

# 3. Restore files 1 to 10 as original unmodified from source_dir
for i in range(1, 11):
    filename = f"LINE_ALBUM_頂崁里廢棄物呈報_260128_{i}.jpg"
    src_path = os.path.join(source_dir, filename)
    dst_path = os.path.join(test_dir, filename)
    if os.path.exists(src_path):
        shutil.copy2(src_path, dst_path)
        print(f"Restored original unmodified: {filename}")
