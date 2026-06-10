import cv2
import numpy as np
import os
import glob

def read_image_utf8(path):
    return cv2.imdecode(np.fromfile(path, dtype=np.uint8), cv2.IMREAD_COLOR)

# Paths
ok_dir = r"case001\ok_004-頂崁里-廢棄物清除呈報-115.05.13"
test_dir = r"case001\test_004-頂崁里-廢棄物清除呈報-115.05.13"

# Find image files that have OpenCV processed counterparts
test_ok_files = glob.glob(os.path.join(test_dir, "*_ok.jpg"))

print(f"Found {len(test_ok_files)} processed files in test folder.")

for test_ok_path in sorted(test_ok_files)[:5]: # analyze first 5 files
    filename_ok = os.path.basename(test_ok_path)
    base_name = filename_ok.replace("_ok.jpg", "")
    orig_name = base_name + ".jpg"
    
    orig_path = os.path.join(test_dir, orig_name)
    user_ok_path = os.path.join(ok_dir, orig_name)
    
    if not os.path.exists(user_ok_path):
        print(f"User ok file not found for {orig_name}, skipping.")
        continue
        
    print(f"\nAnalyzing: {orig_name}")
    
    img_orig = read_image_utf8(orig_path)
    img_user = read_image_utf8(user_ok_path)
    img_opencv = read_image_utf8(test_ok_path)
    
    if img_orig is None or img_user is None or img_opencv is None:
        print("Error loading one of the images.")
        continue
        
    # Find diff region between original and user_ok to see where user edited
    diff_user = cv2.absdiff(img_orig, img_user)
    gray_diff_user = cv2.cvtColor(diff_user, cv2.COLOR_BGR2GRAY)
    _, thresh_user = cv2.threshold(gray_diff_user, 5, 255, cv2.THRESH_BINARY)
    
    # Find diff region between original and opencv_ok
    diff_cv = cv2.absdiff(img_orig, img_opencv)
    gray_diff_cv = cv2.cvtColor(diff_cv, cv2.COLOR_BGR2GRAY)
    _, thresh_cv = cv2.threshold(gray_diff_cv, 5, 255, cv2.THRESH_BINARY)
    
    # Bounding boxes
    contours_user, _ = cv2.findContours(thresh_user, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours_cv, _ = cv2.findContours(thresh_cv, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    if contours_user and contours_cv:
        # User edit bbox
        x_u, y_u, w_u, h_u = cv2.boundingRect(np.vstack(contours_user))
        # OpenCV edit bbox
        x_c, y_c, w_c, h_c = cv2.boundingRect(np.vstack(contours_cv))
        
        print(f"User modified region: x={x_u}, y={y_u}, w={w_u}, h={h_u}")
        print(f"OpenCV modified region: x={x_c}, y={y_c}, w={w_c}, h={h_c}")
        print(f"Offset difference: dx={x_u - x_c}, dy={y_u - y_c}")
        print(f"Size difference: dw={w_u - w_c}, dh={h_u - h_c}")
        
        # Save crops of user's edit vs OpenCV's edit for review
        # Crop slightly larger region
        margin = 30
        y_min = min(y_u, y_c) - margin
        y_max = max(y_u + h_u, y_c + h_c) + margin
        x_min = min(x_u, x_c) - margin
        x_max = max(x_u + w_u, x_c + w_c) + margin
        
        # Clamp coordinates
        y_min, y_max = max(0, y_min), min(img_orig.shape[0], y_max)
        x_min, x_max = max(0, x_min), min(img_orig.shape[1], x_max)
        
        crop_orig = img_orig[y_min:y_max, x_min:x_max]
        crop_user = img_user[y_min:y_max, x_min:x_max]
        crop_opencv = img_opencv[y_min:y_max, x_min:x_max]
        
        # Save side-by-side comparison image
        combined = np.hstack([crop_orig, crop_user, crop_opencv])
        out_name = f"compare_{base_name.split('_')[-1]}.jpg"
        out_path = os.path.join(test_dir, out_name)
        
        # Write to file
        _, ext = os.path.splitext(out_path)
        is_success, im_buf_arr = cv2.imencode(ext, combined)
        if is_success:
            im_buf_arr.tofile(out_path)
            print(f"Saved comparison to: {out_name}")
    else:
        print("Could not find edit bounding boxes.")
