import cv2
import numpy as np
import os
import glob

def read_image_utf8(path, flags=cv2.IMREAD_COLOR):
    return cv2.imdecode(np.fromfile(path, dtype=np.uint8), flags)

test_dir = r"測試SKILLS_08"
ref_path = os.path.join(test_dir, "LINE_ALBUM_頂崁里廢棄物呈報_260128_2.jpg")
ref_img = read_image_utf8(ref_path)

# Year template coordinates for 08 folder
y_ymin, y_ymax, y_xmin, y_xmax = 595, 625, 155, 210
year_temp = ref_img[y_ymin:y_ymax, y_xmin:y_xmax]
year_gray_temp = cv2.cvtColor(year_temp, cv2.COLOR_BGR2GRAY)

jpg_files = glob.glob(os.path.join(test_dir, "LINE_ALBUM_*.jpg"))

print("Analyzing images for dynamic opacity calculation:")
for file_path in sorted(jpg_files):
    if file_path.endswith("_ok.jpg"):
        continue
    img = read_image_utf8(file_path)
    if img is None:
        continue
    
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Match year to find location in this specific image
    found_year = None
    for scale in np.linspace(0.8, 1.2, 20):
        resized_year = cv2.resize(year_gray_temp, (0,0), fx=scale, fy=scale)
        if resized_year.shape[0] > gray.shape[0] or resized_year.shape[1] > gray.shape[1]:
            continue
        res = cv2.matchTemplate(gray, resized_year, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, max_loc = cv2.minMaxLoc(res)
        if found_year is None or max_val > found_year[0]:
            found_year = (max_val, max_loc, scale, resized_year.shape)
            
    if found_year is not None and found_year[0] >= 0.70:
        max_val_y, max_loc_y, scale_y, shape_y = found_year
        xy, yy = max_loc_y
        
        # Extract year region
        year_region = gray[yy:yy+shape_y[0], xy:xy+shape_y[1]]
        
        # Otsu thresholding
        _, thresh = cv2.threshold(year_region, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
        
        # Calculate mean ink and background
        ink_pixels = year_region[thresh > 0]
        bg_pixels = year_region[thresh == 0]
        
        if len(ink_pixels) > 0 and len(bg_pixels) > 0:
            mean_ink = np.mean(ink_pixels)
            mean_bg = np.mean(bg_pixels)
            # Standard contrast ratio formula
            contrast_ratio = 1.0 - (mean_ink / mean_bg)
            
            # Let's map it to an opacity value. Since 0.62 is normal, let's see what contrast_ratio is
            print(f"File: {os.path.basename(file_path)}: year confidence={max_val_y:.3f}, mean_ink={mean_ink:.1f}, mean_bg={mean_bg:.1f}, contrast_ratio={contrast_ratio:.3f}")
        else:
            print(f"File: {os.path.basename(file_path)}: failed to separate ink/bg")
    else:
        print(f"File: {os.path.basename(file_path)}: Year not matched")
