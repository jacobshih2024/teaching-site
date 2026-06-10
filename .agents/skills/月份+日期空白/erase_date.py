import cv2
import numpy as np
import os
import glob
import sys
import argparse

# Force standard stdout/stderr output in UTF-8
if sys.platform.startswith('win'):
    import sys
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

def read_image_utf8(path, flags=cv2.IMREAD_COLOR):
    """安全地讀取含有中文路徑的圖片檔案"""
    try:
        nparr = np.fromfile(path, dtype=np.uint8)
        img = cv2.imdecode(nparr, flags)
        return img
    except Exception as e:
        print(f"Error reading image {path}: {e}")
        return None

def write_image_utf8(path, img, params=None):
    """安全地寫入含有中文路徑的圖片檔案"""
    try:
        ext = os.path.splitext(path)[1]
        result, nparr = cv2.imencode(ext, img, params)
        if result:
            nparr.tofile(path)
            return True
        return False
    except Exception as e:
        print(f"Error writing image to {path}: {e}")
        return False

def main():
    parser = argparse.ArgumentParser(description="自動抹除白板相片中的月份與日期數字，使兩欄位留白淨空")
    parser.add_argument("--folder", required=True, help="包含待修改 JPG 圖片的資料夾路徑")
    parser.add_argument("--ref-image", help="參考圖片路徑 (包含年份、月份與日期，預設自動搜尋包含 _41.jpg 的檔案)")
    parser.add_argument("--year-bbox", default="595,625,195,270", help="年份模板在參考圖片中的 ymin,ymax,xmin,xmax 座標 (格式: ymin,ymax,xmin,xmax)")
    parser.add_argument("--month-bbox", default="599,621,276,290", help="月份模板在參考圖片中的 ymin,ymax,xmin,xmax 座標 (格式: ymin,ymax,xmin,xmax)")
    parser.add_argument("--day-bbox", default="599,621,305,335", help="日期模板在參考圖片中的 ymin,ymax,xmin,xmax 座標 (格式: ymin,ymax,xmin,xmax)")
    parser.add_argument("--year-thresh", type=float, default=0.70, help="年份模板比對門檻 (預設 0.70)")
    parser.add_argument("--month-thresh", type=float, default=0.75, help="原月份模板比對門檻 (預設 0.75)")
    parser.add_argument("--day-thresh", type=float, default=0.75, help="原日期模板比對門檻 (預設 0.75)")
    args = parser.parse_args()

    # Parse coordinates
    try:
        y_ymin, y_ymax, y_xmin, y_xmax = map(int, args.year_bbox.split(","))
        m_ymin, m_ymax, m_xmin, m_xmax = map(int, args.month_bbox.split(","))
        d_ymin, d_ymax, d_xmin, d_xmax = map(int, args.day_bbox.split(","))
    except ValueError:
        print("[ERROR] Coordinates format incorrect. Must be: ymin,ymax,xmin,xmax")
        return

    # Find JPG files in folder
    search_path = os.path.join(args.folder, "*.jpg")
    jpg_files = glob.glob(search_path)
    # Exclude already processed files
    jpg_files = [f for f in jpg_files if not f.endswith("_ok.jpg")]

    if not jpg_files:
        print(f"[ERROR] No JPG images found in {args.folder}")
        return

    # Determine reference image
    ref_path = args.ref_image
    if not ref_path:
        # Try to find file containing _41.jpg
        candidates = [f for f in jpg_files if "_41.jpg" in f.lower()]
        if candidates:
            ref_path = candidates[0]
            print(f"Automatically selected reference image (containing _41): {ref_path}")
        else:
            ref_path = sorted(jpg_files)[0]
            print(f"Automatically selected reference image (lexicographically first): {ref_path}")
    else:
        print(f"Using specified reference image: {ref_path}")

    # Read reference image and extract templates
    ref_img = read_image_utf8(ref_path)
    if ref_img is None:
        print(f"[ERROR] Failed to load reference image: {ref_path}")
        return

    # Extract year template
    year_temp = ref_img[y_ymin:y_ymax, y_xmin:y_xmax]
    year_gray_temp = cv2.cvtColor(year_temp, cv2.COLOR_BGR2GRAY)
    
    # Extract month template
    month_temp = ref_img[m_ymin:m_ymax, m_xmin:m_xmax]
    month_gray_temp = cv2.cvtColor(month_temp, cv2.COLOR_BGR2GRAY)
    
    # Extract day template
    day_temp = ref_img[d_ymin:d_ymax, d_xmin:d_xmax]
    day_gray_temp = cv2.cvtColor(day_temp, cv2.COLOR_BGR2GRAY)

    print(f"\nStarting batch date-erasing in folder: {args.folder}")
    print("="*40)

    processed_count = 0
    skipped_count = 0
    errors_count = 0

    for idx, filepath in enumerate(jpg_files):
        filename = os.path.basename(filepath)
        try:
            target = read_image_utf8(filepath)
            if target is None:
                print(f"[ERROR] Failed to load {filename}")
                errors_count += 1
                continue
            
            targ_gray = cv2.cvtColor(target, cv2.COLOR_BGR2GRAY)
            
            # Step A: Template Matching for Year Anchor across multiple scales
            found_year = None
            for scale in np.linspace(0.8, 1.2, 20):
                resized_year = cv2.resize(year_gray_temp, (0,0), fx=scale, fy=scale)
                if resized_year.shape[0] > targ_gray.shape[0] or resized_year.shape[1] > targ_gray.shape[1]:
                    continue
                res = cv2.matchTemplate(targ_gray, resized_year, cv2.TM_CCOEFF_NORMED)
                _, max_val, _, max_loc = cv2.minMaxLoc(res)
                if found_year is None or max_val > found_year[0]:
                    found_year = (max_val, max_loc, scale, resized_year.shape)
                    
            if found_year is None or found_year[0] < args.year_thresh:
                print(f"[SKIP] {filename} (Year not found, max year confidence: {found_year[0] if found_year else 0:.4f})")
                skipped_count += 1
                continue
                
            max_val_y, max_loc_y, scale_y, shape_y = found_year
            xy, yy = max_loc_y
            
            # Initialize inpaint mask for this image
            inpaint_mask = np.zeros(target.shape[:2], dtype=np.uint8)
            
            # ---------------------------------------------
            # Step B: Process Month Erasing
            # ---------------------------------------------
            x_offset_start_m = m_xmin - y_xmin
            x_offset_end_m = m_xmax - y_xmin
            y_offset_start_m = m_ymin - y_ymin
            y_offset_end_m = m_ymax - y_ymin
            
            x_start_m = max(0, min(int(xy + (x_offset_start_m - 10) * scale_y), targ_gray.shape[1] - 1))
            x_end_m = max(0, min(int(xy + (x_offset_end_m + 10) * scale_y), targ_gray.shape[1]))
            y_start_m = max(0, min(int(yy + (y_offset_start_m - 10) * scale_y), targ_gray.shape[0] - 1))
            y_end_m = max(0, min(int(yy + (y_offset_end_m + 15) * scale_y), targ_gray.shape[0]))
            
            roi_m = targ_gray[y_start_m:y_end_m, x_start_m:x_end_m]
            
            resized_month = cv2.resize(month_gray_temp, (0,0), fx=scale_y, fy=scale_y)
            if resized_month.shape[0] <= roi_m.shape[0] and resized_month.shape[1] <= roi_m.shape[1]:
                res_m = cv2.matchTemplate(roi_m, resized_month, cv2.TM_CCOEFF_NORMED)
                _, max_val_m, _, max_loc_m = cv2.minMaxLoc(res_m)
                
                if max_val_m >= args.month_thresh:
                    xm = x_start_m + max_loc_m[0]
                    ym = y_start_m + max_loc_m[1]
                    wm, hm = resized_month.shape[1], resized_month.shape[0]
                    
                    matched_region_m = targ_gray[ym:ym+hm, xm:xm+wm]
                    _, stroke_mask_m = cv2.threshold(matched_region_m, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
                    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
                    stroke_mask_dilated_m = cv2.dilate(stroke_mask_m, kernel, iterations=2)
                    
                    # Protect horizontal grid line at the bottom
                    protect_h = max(1, int(3 * scale_y))
                    if stroke_mask_dilated_m.shape[0] > protect_h:
                        stroke_mask_dilated_m[-protect_h:, :] = 0
                        
                    inpaint_mask[ym:ym+hm, xm:xm+wm] = np.maximum(inpaint_mask[ym:ym+hm, xm:xm+wm], stroke_mask_dilated_m)
            
            # ---------------------------------------------
            # Step C: Process Day Erasing
            # ---------------------------------------------
            x_offset_start_d = d_xmin - y_xmin
            x_offset_end_d = d_xmax - y_xmin
            y_offset_start_d = d_ymin - y_ymin
            y_offset_end_d = d_ymax - y_ymin
            
            x_start_d = max(0, min(int(xy + (x_offset_start_d - 10) * scale_y), targ_gray.shape[1] - 1))
            x_end_d = max(0, min(int(xy + (x_offset_end_d + 10) * scale_y), targ_gray.shape[1]))
            y_start_d = max(0, min(int(yy + (y_offset_start_d - 10) * scale_y), targ_gray.shape[0] - 1))
            y_end_d = max(0, min(int(yy + (y_offset_end_d + 15) * scale_y), targ_gray.shape[0]))
            
            roi_d = targ_gray[y_start_d:y_end_d, x_start_d:x_end_d]
            
            resized_day = cv2.resize(day_gray_temp, (0,0), fx=scale_y, fy=scale_y)
            if resized_day.shape[0] <= roi_d.shape[0] and resized_day.shape[1] <= roi_d.shape[1]:
                res_d = cv2.matchTemplate(roi_d, resized_day, cv2.TM_CCOEFF_NORMED)
                _, max_val_d, _, max_loc_d = cv2.minMaxLoc(res_d)
                
                if max_val_d >= args.day_thresh:
                    xd = x_start_d + max_loc_d[0]
                    yd = y_start_d + max_loc_d[1]
                    wd, hd = resized_day.shape[1], resized_day.shape[0]
                    
                    matched_region_d = targ_gray[yd:yd+hd, xd:xd+wd]
                    _, stroke_mask_d = cv2.threshold(matched_region_d, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
                    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
                    stroke_mask_dilated_d = cv2.dilate(stroke_mask_d, kernel, iterations=2)
                    
                    # Protect horizontal grid line at the bottom
                    protect_h = max(1, int(3 * scale_y))
                    if stroke_mask_dilated_d.shape[0] > protect_h:
                        stroke_mask_dilated_d[-protect_h:, :] = 0
                        
                    inpaint_mask[yd:yd+hd, xd:xd+wd] = np.maximum(inpaint_mask[yd:yd+hd, xd:xd+wd], stroke_mask_dilated_d)
            
            # Step D: Apply Combined Inpaint
            if np.sum(inpaint_mask) > 0:
                inpainted = cv2.inpaint(target, inpaint_mask, 3, cv2.INPAINT_TELEA)
                
                # Save output inside "OKK" folder
                okk_dir = os.path.join(args.folder, "OKK")
                os.makedirs(okk_dir, exist_ok=True)
                base_name, _ = os.path.splitext(filename)
                output_filename = f"{base_name}_ok.jpg"
                output_path = os.path.join(okk_dir, output_filename)
                
                write_image_utf8(output_path, inpainted)
                print(f"[OK] {filename} -> OKK\\{output_filename} (month & day erased)")
                processed_count += 1
            else:
                print(f"[SKIP] {filename} (No matching month/day digits found to erase)")
                skipped_count += 1
            
        except Exception as e:
            print(f"[ERROR] Failed to process {filename}. Error: {e}")
            errors_count += 1

    print("\n" + "="*40)
    print("Batch Date-Erasing Summary:")
    print(f"Total processed and erased: {processed_count}")
    print(f"Total skipped (no target): {skipped_count}")
    print(f"Errors encountered: {errors_count}")
    print("="*40)

if __name__ == "__main__":
    main()
