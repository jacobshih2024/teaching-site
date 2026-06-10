import cv2
import numpy as np
import os
import glob

def read_image_utf8(path):
    return cv2.imdecode(np.fromfile(path, dtype=np.uint8), cv2.IMREAD_COLOR)

# Paths
test_dir = r"case001\test_004-頂崁里-廢棄物清除呈報-115.05.13"

# Load image 41 to get templates
img41_path = os.path.join(test_dir, 'LINE_ALBUM_頂崁里廢棄物呈報_260128_41.jpg')
img41 = read_image_utf8(img41_path)

# Year template (115.)
year_temp = img41[595:625, 195:270]
year_gray = cv2.cvtColor(year_temp, cv2.COLOR_BGR2GRAY)

# Month 1 template
month_temp = img41[599:621, 276:290]
month_gray = cv2.cvtColor(month_temp, cv2.COLOR_BGR2GRAY)

# List of files to test (user-modified and false positives)
test_files = glob.glob(os.path.join(test_dir, "LINE_ALBUM_*.jpg"))
test_files = [f for f in test_files if not f.endswith("_ok.jpg")]

print(f"Testing matching on {len(test_files)} files...")

successful_matches = 0
failed_matches = 0

for file_path in sorted(test_files):
    filename = os.path.basename(file_path)
    img = read_image_utf8(file_path)
    if img is None:
        continue
        
    targ_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # 1. Match the year "115."
    # We run multi-scale template matching for the year
    found_year = None
    for scale in np.linspace(0.5, 2.0, 50):
        resized_year = cv2.resize(year_gray, (0,0), fx=scale, fy=scale)
        if resized_year.shape[0] > targ_gray.shape[0] or resized_year.shape[1] > targ_gray.shape[1]:
            continue
        res = cv2.matchTemplate(targ_gray, resized_year, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, max_loc = cv2.minMaxLoc(res)
        if found_year is None or max_val > found_year[0]:
            found_year = (max_val, max_loc, scale, resized_year.shape)
            
    if found_year and found_year[0] >= 0.75:
        max_val_y, max_loc_y, scale_y, shape_y = found_year
        xy, yy = max_loc_y
        wy, hy = shape_y[1], shape_y[0]
        
        # Define the search ROI for month "1" based on the year's position:
        # The month is to the right of the year.
        # Year crop is 75px wide (at scale=1.0). The month "1" in image 41 is at x=276, which is 81px from the start of the year crop (x=195).
        # So the month "1" starts at: xy + 81 * scale_y
        # We can search in a small region:
        # x range: [xy + 70 * scale_y, xy + 105 * scale_y]
        # y range: [yy - 5 * scale_y, yy + 10 * scale_y]
        x_start = int(xy + 65 * scale_y)
        x_end = int(xy + 115 * scale_y)
        y_start = int(yy - 10 * scale_y)
        y_end = int(yy + 15 * scale_y)
        
        # Crop the search region
        # Ensure coordinates are within image bounds
        h_img, w_img = targ_gray.shape
        x_start = max(0, min(x_start, w_img - 1))
        x_end = max(0, min(x_end, w_img))
        y_start = max(0, min(y_start, h_img - 1))
        y_end = max(0, min(y_end, h_img))
        
        roi = targ_gray[y_start:y_end, x_start:x_end]
        
        # Match Month 1 ONLY inside this ROI
        resized_month = cv2.resize(month_gray, (0,0), fx=scale_y, fy=scale_y)
        if resized_month.shape[0] <= roi.shape[0] and resized_month.shape[1] <= roi.shape[1]:
            res_m = cv2.matchTemplate(roi, resized_month, cv2.TM_CCOEFF_NORMED)
            _, max_val_m, _, max_loc_m = cv2.minMaxLoc(res_m)
            
            # Map ROI coordinate back to absolute coordinate
            abs_x_m = x_start + max_loc_m[0]
            abs_y_m = y_start + max_loc_m[1]
            
            print(f"File: {filename} -> Year matched (score: {max_val_y:.3f}). Month '1' in ROI score: {max_val_m:.3f} at absolute x={abs_x_m}, y={abs_y_m}")
            successful_matches += 1
        else:
            print(f"File: {filename} -> Year matched but ROI is too small for month!")
            failed_matches += 1
    else:
        print(f"File: {filename} -> Failed to match Year '115.' (max score: {found_year[0] if found_year else 0:.3f})")
        failed_matches += 1

print(f"\nSummary: Successful year + ROI matches: {successful_matches}, Failed: {failed_matches}")
