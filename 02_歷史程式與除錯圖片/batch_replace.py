import cv2
import numpy as np
import os
import glob

def read_image_utf8(path, flags=cv2.IMREAD_COLOR):
    return cv2.imdecode(np.fromfile(path, dtype=np.uint8), flags)

def write_image_utf8(path, img):
    _, ext = os.path.splitext(path)
    is_success, im_buf_arr = cv2.imencode(ext, img)
    if is_success:
        im_buf_arr.tofile(path)
        return True
    return False

# Base directory
folder_path = r'case001\test_004-頂崁里-廢棄物清除呈報-115.05.13'

# 1. Ensure transparent template (0513_layer1.png) is extracted from PSD
t5_path = os.path.join(folder_path, '0513_layer1.png')
psd_path = os.path.join(folder_path, '0513.psd')

if not os.path.exists(t5_path):
    print("Extracting transparent layer 1 from PSD dynamically...")
    try:
        from psd_tools import PSDImage
        psd = PSDImage.open(psd_path)
        layer1 = psd[1]  # Layer 1 containing digit 5
        img_pil = layer1.composite()
        img_np = np.array(img_pil)
        img_bgra = cv2.cvtColor(img_np, cv2.COLOR_RGBA2BGRA)
        write_image_utf8(t5_path, img_bgra)
        print("Transparent layer saved successfully.")
    except Exception as e:
        print(f"Error extracting layer from PSD: {e}")
        # Fallback to standard 0513_psd.png if it exists
        fallback_path = os.path.join(folder_path, '0513_psd.png')
        if os.path.exists(fallback_path):
            print("Using fallback 0513_psd.png")
            t5_path = fallback_path
        else:
            print("Error: Missing template files!")
            exit(1)

# Load transparent template (BGRA)
t5_bgra = read_image_utf8(t5_path, cv2.IMREAD_UNCHANGED)
if t5_bgra is None:
    print("Error: Could not load template 5!")
    exit(1)

t5_bgr = t5_bgra[:, :, :3].astype(float)
t5_alpha = t5_bgra[:, :, 3].astype(float) / 255.0

# 2. Load templates from image 41
img41_path = os.path.join(folder_path, 'LINE_ALBUM_頂崁里廢棄物呈報_260128_41.jpg')
img41 = read_image_utf8(img41_path)
if img41 is None:
    print("Error: Missing reference image 41 for month template!")
    exit(1)

# Year template (115.)
year_temp = img41[595:625, 195:270]
year_gray = cv2.cvtColor(year_temp, cv2.COLOR_BGR2GRAY)

# Month "1" template
month_temp = img41[599:621, 276:290]
month_gray = cv2.cvtColor(month_temp, cv2.COLOR_BGR2GRAY)

# Find all JPG files in the directory
jpg_files = glob.glob(os.path.join(folder_path, 'LINE_ALBUM_*.jpg'))

processed_count = 0
skipped_count = 0
errors_count = 0

print(f"Starting batch processing of {len(jpg_files)} files...\n")

for file_path in jpg_files:
    filename = os.path.basename(file_path)
    
    # Skip already output files
    if filename.endswith('_ok.jpg') or filename.endswith('_test_ok.jpg') or 'crop' in filename or 'compare' in filename:
        continue
        
    try:
        target = read_image_utf8(file_path)
        if target is None:
            print(f"[ERROR] Could not open {filename}")
            errors_count += 1
            continue
            
        targ_gray = cv2.cvtColor(target, cv2.COLOR_BGR2GRAY)
        
        # Step A: Match Year "115." to anchor the date horizontal line
        found_year = None
        for scale in np.linspace(0.5, 2.0, 50):
            resized_year = cv2.resize(year_gray, (0,0), fx=scale, fy=scale)
            if resized_year.shape[0] > targ_gray.shape[0] or resized_year.shape[1] > targ_gray.shape[1]:
                continue
            res = cv2.matchTemplate(targ_gray, resized_year, cv2.TM_CCOEFF_NORMED)
            _, max_val, _, max_loc = cv2.minMaxLoc(res)
            if found_year is None or max_val > found_year[0]:
                found_year = (max_val, max_loc, scale, resized_year.shape)
                
        if found_year is None or found_year[0] < 0.70:
            print(f"[SKIP] {filename} (Year 115. not found, max year confidence: {found_year[0] if found_year else 0:.4f})")
            skipped_count += 1
            continue
            
        max_val_y, max_loc_y, scale_y, shape_y = found_year
        xy, yy = max_loc_y
        
        # Step B: Define a strict ROI that ONLY covers the Month column relative to the year anchor
        x_start = int(xy + 65 * scale_y)
        x_end = int(xy + 102 * scale_y)
        y_start = int(yy - 10 * scale_y)
        y_end = int(yy + 35 * scale_y)
        
        h_img, w_img = targ_gray.shape
        x_start = max(0, min(x_start, w_img - 1))
        x_end = max(0, min(x_end, w_img))
        y_start = max(0, min(y_start, h_img - 1))
        y_end = max(0, min(y_end, h_img))
        
        roi = targ_gray[y_start:y_end, x_start:x_end]
        
        # Step C: Match Month "1" ONLY within this strict ROI
        resized_month = cv2.resize(month_gray, (0,0), fx=scale_y, fy=scale_y)
        
        if resized_month.shape[0] > roi.shape[0] or resized_month.shape[1] > roi.shape[1]:
            print(f"[SKIP] {filename} (ROI too small for month template)")
            skipped_count += 1
            continue
            
        res_m = cv2.matchTemplate(roi, resized_month, cv2.TM_CCOEFF_NORMED)
        _, max_val_m, _, max_loc_m = cv2.minMaxLoc(res_m)
        
        # Confidence threshold for the month "1" template inside the ROI
        if max_val_m < 0.75:
            print(f"[SKIP] {filename} (Month 1 not found in ROI, score: {max_val_m:.4f})")
            skipped_count += 1
            continue
            
        # Map ROI coordinate back to absolute coordinate
        x = x_start + max_loc_m[0]
        y = y_start + max_loc_m[1]
        w, h = resized_month.shape[1], resized_month.shape[0]
        
        # Step D: Precise stroke-based inpainting to clean the original "1"
        matched_region = targ_gray[y:y+h, x:x+w]
        _, stroke_mask = cv2.threshold(matched_region, 120, 255, cv2.THRESH_BINARY_INV)
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
        stroke_mask = cv2.dilate(stroke_mask, kernel, iterations=1)
        
        inpaint_mask = np.zeros(target.shape[:2], dtype=np.uint8)
        inpaint_mask[y:y+h, x:x+w] = stroke_mask
        inpainted = cv2.inpaint(target, inpaint_mask, 3, cv2.INPAINT_TELEA)
        
        # Step E: Resize transparent digit "5" template using scale_y
        new_w = int(t5_bgra.shape[1] * scale_y)
        new_h = int(t5_bgra.shape[0] * scale_y)
        
        resized_t5_bgr = cv2.resize(t5_bgr, (new_w, new_h), interpolation=cv2.INTER_AREA)
        resized_t5_alpha = cv2.resize(t5_alpha, (new_w, new_h), interpolation=cv2.INTER_AREA)
        
        # Align centers of new digit 5 and original digit 1
        center_x = x + w // 2
        center_y = y + h // 2
        paste_x = center_x - new_w // 2
        paste_y = center_y - new_h // 2
        
        # Step F: Vectorized Multiply blending with 62% opacity
        output = inpainted.copy()
        
        # Calculate overlapping boundaries
        x1, y1 = max(0, paste_x), max(0, paste_y)
        x2 = min(output.shape[1], paste_x + new_w)
        y2 = min(output.shape[0], paste_y + new_h)
        
        tx1 = x1 - paste_x
        ty1 = y1 - paste_y
        tx2 = tx1 + (x2 - x1)
        ty2 = ty1 + (y2 - y1)
        
        if (x2 > x1) and (y2 > y1):
            bg_slice = output[y1:y2, x1:x2].astype(float)
            blend_slice = resized_t5_bgr[ty1:ty2, tx1:tx2]
            alpha_slice = resized_t5_alpha[ty1:ty2, tx1:tx2, np.newaxis] * 0.62  # 62% opacity factor
            
            # Blend formula: Output = BG * (1 - Alpha) + (BG * Blend / 255) * Alpha
            blended = bg_slice * (1.0 - alpha_slice) + (bg_slice * blend_slice / 255.0) * alpha_slice
            output[y1:y2, x1:x2] = np.clip(blended, 0, 255).astype(np.uint8)
            
        # Output file
        base_name, _ = os.path.splitext(filename)
        output_filename = f"{base_name}_ok.jpg"
        output_path = os.path.join(folder_path, output_filename)
        
        write_image_utf8(output_path, output)
        print(f"[OK] {filename} -> {output_filename} (month score: {max_val_m:.4f}, scale: {scale_y:.3f})")
        processed_count += 1
        
    except Exception as e:
        print(f"[ERROR] Failed to process {filename}. Error: {e}")
        errors_count += 1

print("\n" + "="*40)
print("Batch Processing Summary:")
print(f"Total processed and modified: {processed_count}")
print(f"Total skipped (no 1月): {skipped_count}")
print(f"Errors encountered: {errors_count}")
print("="*40)
