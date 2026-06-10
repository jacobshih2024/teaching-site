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

print(f"User modified {len(user_modified)} files in total.")

# Let's find files processed by OpenCV (i.e. we have _ok.jpg)
all_processed = glob.glob(os.path.join(test_dir, "*_ok.jpg"))
processed_filenames = [os.path.basename(f).replace("_ok.jpg", ".jpg") for f in all_processed]

print(f"OpenCV processed {len(processed_filenames)} files in total.")

# 1. OpenCV processed but User did NOT modify:
false_positives = [f for f in processed_filenames if f not in user_modified]
print(f"\n--- Files processed by OpenCV but NOT modified by User ({len(false_positives)} files) ---")

# Let's run template matching on these false positive files using our script's logic
# to see where it matched the "1".
img41_path = os.path.join(test_dir, 'LINE_ALBUM_頂崁里廢棄物呈報_260128_41.jpg')
img41 = read_image_utf8(img41_path)
temp_gray = cv2.cvtColor(img41[599:621, 276:290], cv2.COLOR_BGR2GRAY)

for filename in false_positives:
    file_path = os.path.join(test_dir, filename)
    img = read_image_utf8(file_path)
    if img is None:
        continue
    targ_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Run matching
    found = None
    for scale in np.linspace(0.5, 2.0, 50):
        resized = cv2.resize(temp_gray, (0,0), fx=scale, fy=scale)
        if resized.shape[0] > targ_gray.shape[0] or resized.shape[1] > targ_gray.shape[1]:
            continue
        res = cv2.matchTemplate(targ_gray, resized, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, max_loc = cv2.minMaxLoc(res)
        if found is None or max_val > found[0]:
            found = (max_val, max_loc, scale, resized.shape)
            
    if found:
        max_val, max_loc, scale, shape = found
        print(f"File: {filename} -> Matched '1' at x={max_loc[0]}, y={max_loc[1]} (Score: {max_val:.4f}, scale={scale:.3f})")
        
# 2. Let's also check if for the user_modified files, did OpenCV match the correct region?
# The user's modified region can be found by thresholding the difference between user's file and original file.
print(f"\n--- Checking alignment in User Modified Files ---")
mismatches = []
for filename in user_modified:
    orig_path = os.path.join(test_dir, filename)
    user_path = os.path.join(ok_dir, filename)
    
    img_orig = read_image_utf8(orig_path)
    img_user = read_image_utf8(user_path)
    
    # Locate user modified region
    diff = cv2.absdiff(img_orig, img_user)
    gray_diff = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray_diff, 10, 255, cv2.THRESH_BINARY)
    if np.sum(thresh) == 0:
        continue
        
    ys, xs = np.where(thresh > 0)
    user_y_min, user_y_max = np.min(ys), np.max(ys)
    user_x_min, user_x_max = np.min(xs), np.max(xs)
    
    # Get OpenCV match location
    targ_gray = cv2.cvtColor(img_orig, cv2.COLOR_BGR2GRAY)
    found = None
    for scale in np.linspace(0.5, 2.0, 50):
        resized = cv2.resize(temp_gray, (0,0), fx=scale, fy=scale)
        if resized.shape[0] > targ_gray.shape[0] or resized.shape[1] > targ_gray.shape[1]:
            continue
        res = cv2.matchTemplate(targ_gray, resized, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, max_loc = cv2.minMaxLoc(res)
        if found is None or max_val > found[0]:
            found = (max_val, max_loc, scale, resized.shape)
            
    if found:
        max_val, max_loc, scale, shape = found
        cx = max_loc[0] + shape[1] // 2
        cy = max_loc[1] + shape[0] // 2
        
        # Check if the OpenCV match center is inside the user modified region
        is_inside = (user_x_min <= cx <= user_x_max) and (user_y_min <= cy <= user_y_max)
        if not is_inside:
            mismatches.append((filename, max_loc, (user_x_min, user_x_max, user_y_min, user_y_max)))
            print(f"Mismatch: {filename} -> OpenCV matched x={max_loc[0]}, y={max_loc[1]}. User modified region: x=[{user_x_min}, {user_x_max}], y=[{user_y_min}, {user_y_max}]")

print(f"Total mismatches: {len(mismatches)}")
