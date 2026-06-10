import cv2
import numpy as np
import os
import glob

def read_image_utf8(path):
    return cv2.imdecode(np.fromfile(path, dtype=np.uint8), cv2.IMREAD_COLOR)

# Paths
ok_dir = r"case001\ok_004-頂崁里-廢棄物清除呈報-115.05.13"
test_dir = r"case001\test_004-頂崁里-廢棄物清除呈報-115.05.13"

orig_files = glob.glob(os.path.join(test_dir, "LINE_ALBUM_*.jpg"))
orig_files = [f for f in orig_files if not f.endswith("_ok.jpg")]

user_modified = []
for file_path in orig_files:
    filename = os.path.basename(file_path)
    user_path = os.path.join(ok_dir, filename)
    if os.path.exists(user_path):
        img_orig = read_image_utf8(file_path)
        img_user = read_image_utf8(user_path)
        if img_orig is not None and img_user is not None:
            if np.mean(cv2.absdiff(img_orig, img_user)) > 0.1:
                user_modified.append(filename)

print(f"User modified {len(user_modified)} files in total.\n")

for filename in sorted(user_modified):
    orig_path = os.path.join(test_dir, filename)
    user_path = os.path.join(ok_dir, filename)
    
    img_orig = read_image_utf8(orig_path)
    img_user = read_image_utf8(user_path)
    
    diff = cv2.absdiff(img_orig, img_user)
    gray_diff = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray_diff, 10, 255, cv2.THRESH_BINARY)
    
    if np.sum(thresh) > 0:
        ys, xs = np.where(thresh > 0)
        x_min, x_max = np.min(xs), np.max(xs)
        y_min, y_max = np.min(ys), np.max(ys)
        w = x_max - x_min
        h = y_max - y_min
        print(f"File: {filename} -> User Modified Region: x=[{x_min}, {x_max}] (w={w}), y=[{y_min}, {y_max}] (h={h})")
    else:
        print(f"File: {filename} -> No difference found!")
