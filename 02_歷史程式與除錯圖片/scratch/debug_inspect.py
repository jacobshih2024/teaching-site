import cv2
import numpy as np
import os

def read_image_utf8(path):
    return cv2.imdecode(np.fromfile(path, dtype=np.uint8), cv2.IMREAD_COLOR)

# Paths
test_dir = r"測試SKILLS_004-頂崁里-廢棄物清除呈報-115.05.13"
ref_path = r"case001\test_004-頂崁里-廢棄物清除呈報-115.05.13\LINE_ALBUM_頂崁里廢棄物呈報_260128_41.jpg"

ref_img = read_image_utf8(ref_path)
year_temp = ref_img[595:625, 195:270]
year_gray = cv2.cvtColor(year_temp, cv2.COLOR_BGR2GRAY)

img_path = os.path.join(test_dir, "LINE_ALBUM_頂崁里廢棄物呈報_260128_2.jpg")
img = read_image_utf8(img_path)

if img is not None:
    targ_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Match year
    found_year = None
    for scale in np.linspace(0.5, 2.0, 50):
        resized_year = cv2.resize(year_gray, (0,0), fx=scale, fy=scale)
        if resized_year.shape[0] > targ_gray.shape[0] or resized_year.shape[1] > targ_gray.shape[1]:
            continue
        res = cv2.matchTemplate(targ_gray, resized_year, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, max_loc = cv2.minMaxLoc(res)
        if found_year is None or max_val > found_year[0]:
            found_year = (max_val, max_loc, scale, resized_year.shape)
            
    if found_year:
        max_val_y, max_loc_y, scale_y, shape_y = found_year
        print(f"Year matched with score: {max_val_y:.4f} at scale {scale_y:.3f}")
        xy, yy = max_loc_y
        
        # Crop the region around year and month and save it
        h_img, w_img = img.shape[:2]
        x_start = max(0, int(xy - 10 * scale_y))
        x_end = min(w_img, int(xy + 150 * scale_y))
        y_start = max(0, int(yy - 10 * scale_y))
        y_end = min(h_img, int(yy + 40 * scale_y))
        
        crop = img[y_start:y_end, x_start:x_end]
        cv2.imwrite("debug_crop_2.png", crop)
        print("Saved debug_crop_2.png")
    else:
        print("Year not found at all")
else:
    print("Could not load image 2")
