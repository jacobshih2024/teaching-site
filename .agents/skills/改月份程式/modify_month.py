import cv2
import numpy as np
import os
import glob
import argparse

def read_image_utf8(path, flags=cv2.IMREAD_COLOR):
    return cv2.imdecode(np.fromfile(path, dtype=np.uint8), flags)

def write_image_utf8(path, img):
    _, ext = os.path.splitext(path)
    is_success, im_buf_arr = cv2.imencode(ext, img)
    if is_success:
        im_buf_arr.tofile(path)
        return True
    return False

def extract_psd_layer(psd_path, layer_index, output_path):
    print(f"Extracting transparent layer {layer_index} from PSD dynamically...")
    try:
        from psd_tools import PSDImage
        psd = PSDImage.open(psd_path)
        layer = psd[layer_index]
        img_pil = layer.composite()
        img_np = np.array(img_pil)
        img_bgra = cv2.cvtColor(img_np, cv2.COLOR_RGBA2BGRA)
        write_image_utf8(output_path, img_bgra)
        print("Transparent layer saved successfully.")
        return img_bgra
    except Exception as e:
        print(f"Error extracting layer from PSD: {e}")
        return None

def main():
    parser = argparse.ArgumentParser(description="自動替換白板相片中的月份數字")
    parser.add_argument("--folder", required=True, help="包含待修改 JPG 圖片的資料夾路徑")
    parser.add_argument("--template", required=True, help="透明數字模板路徑 (PNG 或 PSD)")
    parser.add_argument("--psd-layer", type=int, default=1, help="如果模板為 PSD，指定要擷取的圖層索引 (預設為 1)")
    parser.add_argument("--ref-image", help="參考圖片路徑 (包含年份與月份模板的圖片，預設自動搜尋包含 _41.jpg 的檔案)")
    parser.add_argument("--year-bbox", default="595,625,195,270", help="年份模板在參考圖片中的 ymin,ymax,xmin,xmax 座標 (格式: ymin,ymax,xmin,xmax)")
    parser.add_argument("--month-bbox", default="599,621,276,290", help="月份模板在參考圖片中的 ymin,ymax,xmin,xmax 座標 (格式: ymin,ymax,xmin,xmax)")
    parser.add_argument("--opacity", type=float, default=0.62, help="新數字的疊合不透明度 (0.0 到 1.0，預設 0.62)")
    parser.add_argument("--year-thresh", type=float, default=0.70, help="年份模板比對門檻 (預設 0.70)")
    parser.add_argument("--month-thresh", type=float, default=0.75, help="月份模板比對門檻 (預設 0.75)")
    parser.add_argument("--no-auto-opacity", dest="auto_opacity", action="store_false", help="停用自動明暗度偵測，改用固定不透明度")
    parser.set_defaults(auto_opacity=True)
    args = parser.parse_args()

    # Parse coordinates
    try:
        y_ymin, y_ymax, y_xmin, y_xmax = map(int, args.year_bbox.split(","))
        m_ymin, m_ymax, m_xmin, m_xmax = map(int, args.month_bbox.split(","))
    except Exception as e:
        print(f"Error parsing coordinates: {e}")
        return

    # Handle transparent template
    t_path = args.template
    if t_path.lower().endswith('.psd'):
        png_temp_path = os.path.splitext(t_path)[0] + "_extracted_layer.png"
        t5_bgra = extract_psd_layer(t_path, args.psd_layer, png_temp_path)
        if t5_bgra is None:
            print("Failed to extract layer from PSD.")
            return
    else:
        t5_bgra = read_image_utf8(t_path, cv2.IMREAD_UNCHANGED)
        if t5_bgra is None:
            print(f"Error: Could not load template {t_path}")
            return

    t5_bgr = t5_bgra[:, :, :3].astype(float)
    t5_alpha = t5_bgra[:, :, 3].astype(float) / 255.0

    # Handle reference image
    ref_img_path = args.ref_image
    if not ref_img_path:
        # Try to find a file containing _41.jpg or ending with _41.jpg
        candidates = glob.glob(os.path.join(args.folder, "*_41.jpg"))
        if not candidates:
            candidates = glob.glob(os.path.join(args.folder, "*41*.jpg"))
        if candidates:
            ref_img_path = candidates[0]
            print(f"Auto-selected reference image: {ref_img_path}")
        else:
            print("Error: Reference image not provided and could not find *41.jpg in the folder.")
            return

    ref_img = read_image_utf8(ref_img_path)
    if ref_img is None:
        print(f"Error: Could not read reference image: {ref_img_path}")
        return

    # Extract year & month templates from reference image
    year_temp = ref_img[y_ymin:y_ymax, y_xmin:y_xmax]
    year_gray = cv2.cvtColor(year_temp, cv2.COLOR_BGR2GRAY)

    month_temp = ref_img[m_ymin:m_ymax, m_xmin:m_xmax]
    month_gray = cv2.cvtColor(month_temp, cv2.COLOR_BGR2GRAY)

    # Process files
    jpg_files = glob.glob(os.path.join(args.folder, 'LINE_ALBUM_*.jpg'))
    
    processed_count = 0
    skipped_count = 0
    errors_count = 0

    print(f"Starting batch processing of {len(jpg_files)} files...\n")

    for file_path in sorted(jpg_files):
        filename = os.path.basename(file_path)
        
        # Skip output files
        if filename.endswith('_ok.jpg') or filename.endswith('_test_ok.jpg') or 'crop' in filename or 'compare' in filename:
            continue
            
        try:
            target = read_image_utf8(file_path)
            if target is None:
                print(f"[ERROR] Could not open {filename}")
                errors_count += 1
                continue
                
            targ_gray = cv2.cvtColor(target, cv2.COLOR_BGR2GRAY)
            
            # Step A: Match Year
            found_year = None
            for scale in np.linspace(0.5, 2.0, 50):
                resized_year = cv2.resize(year_gray, (0,0), fx=scale, fy=scale)
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
            
                # Step B: Define strict ROI relative to Year based on coordinate offsets
            x_offset_start = m_xmin - y_xmin
            x_offset_end = m_xmax - y_xmin
            y_offset_start = m_ymin - y_ymin
            y_offset_end = m_ymax - y_ymin
            
            # Apply margins scaled with scale_y
            x_start = int(xy + (x_offset_start - 10) * scale_y)
            x_end = int(xy + (x_offset_end + 10) * scale_y)
            y_start = int(yy + (y_offset_start - 10) * scale_y)
            y_end = int(yy + (y_offset_end + 15) * scale_y)
            
            h_img, w_img = targ_gray.shape
            x_start = max(0, min(x_start, w_img - 1))
            x_end = max(0, min(x_end, w_img))
            y_start = max(0, min(y_start, h_img - 1))
            y_end = max(0, min(y_end, h_img))
            
            roi = targ_gray[y_start:y_end, x_start:x_end]
            
            # Step C: Match Month inside ROI
            resized_month = cv2.resize(month_gray, (0,0), fx=scale_y, fy=scale_y)
            
            if resized_month.shape[0] > roi.shape[0] or resized_month.shape[1] > roi.shape[1]:
                print(f"[SKIP] {filename} (ROI too small for month template)")
                skipped_count += 1
                continue
                
            res_m = cv2.matchTemplate(roi, resized_month, cv2.TM_CCOEFF_NORMED)
            _, max_val_m, _, max_loc_m = cv2.minMaxLoc(res_m)
            
            if max_val_m < args.month_thresh:
                print(f"[SKIP] {filename} (Month not found in ROI, score: {max_val_m:.4f})")
                skipped_count += 1
                continue
                
            x = x_start + max_loc_m[0]
            y = y_start + max_loc_m[1]
            w, h = resized_month.shape[1], resized_month.shape[0]
            
            # Step D: Precise stroke-based inpainting using Otsu's thresholding
            matched_region = targ_gray[y:y+h, x:x+w]
            _, stroke_mask = cv2.threshold(matched_region, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
            
            # Dilate to ensure the entire stroke boundary is clean
            kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
            stroke_mask_dilated = cv2.dilate(stroke_mask, kernel, iterations=2)
            
            # Protect horizontal grid line at the bottom
            protect_h = max(1, int(3 * scale_y))
            if stroke_mask_dilated.shape[0] > protect_h:
                stroke_mask_dilated[-protect_h:, :] = 0
            
            inpaint_mask = np.zeros(target.shape[:2], dtype=np.uint8)
            inpaint_mask[y:y+h, x:x+w] = stroke_mask_dilated
            inpainted = cv2.inpaint(target, inpaint_mask, 3, cv2.INPAINT_TELEA)
            
            # Step E: Resize new digit template dynamically based on stroke height
            non_zero_orig = np.nonzero(stroke_mask)
            if len(non_zero_orig[0]) > 0:
                stroke_h_orig = np.max(non_zero_orig[0]) - np.min(non_zero_orig[0]) + 1
                stroke_cy_orig = np.mean(non_zero_orig[0])
                stroke_cx_orig = np.mean(non_zero_orig[1])
            else:
                stroke_h_orig = h
                stroke_cy_orig = h / 2.0
                stroke_cx_orig = w / 2.0
                
            non_zero_new_full = np.nonzero(t5_alpha > 0.05)
            if len(non_zero_new_full[0]) > 0:
                stroke_h_new = np.max(non_zero_new_full[0]) - np.min(non_zero_new_full[0]) + 1
            else:
                stroke_h_new = t5_bgra.shape[0]
                
            # Calculate dynamic scale factor based on stroke height
            digit_scale = stroke_h_orig / stroke_h_new
            
            new_w = int(t5_bgra.shape[1] * digit_scale)
            new_h = int(t5_bgra.shape[0] * digit_scale)
            
            resized_t5_bgr = cv2.resize(t5_bgr, (new_w, new_h), interpolation=cv2.INTER_AREA)
            resized_t5_alpha = cv2.resize(t5_alpha, (new_w, new_h), interpolation=cv2.INTER_AREA)
            
            # Align centers by stroke centroids on the resized template
            non_zero_new = np.nonzero(resized_t5_alpha > 0.05)
            if len(non_zero_new[0]) > 0:
                stroke_cy_new = np.mean(non_zero_new[0])
                stroke_cx_new = np.mean(non_zero_new[1])
            else:
                stroke_cy_new = new_h / 2.0
                stroke_cx_new = new_w / 2.0
                
            paste_x = int(x + stroke_cx_orig - stroke_cx_new)
            paste_y = int(y + stroke_cy_orig - stroke_cy_new)
            
            # Calculate dynamic opacity based on matched year stroke contrast
            current_opacity = args.opacity
            if args.auto_opacity:
                year_region_gray = targ_gray[yy:yy+shape_y[0], xy:xy+shape_y[1]]
                _, year_stroke_mask = cv2.threshold(year_region_gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
                ink_pixels = year_region_gray[year_stroke_mask > 0]
                bg_pixels = year_region_gray[year_stroke_mask == 0]
                if len(ink_pixels) > 0 and len(bg_pixels) > 0:
                    mean_ink = np.mean(ink_pixels)
                    mean_bg = np.mean(bg_pixels)
                    contrast_ratio = 1.0 - (mean_ink / max(1.0, mean_bg))
                    # Clip to natural range [0.35, 0.85]
                    current_opacity = float(np.clip(contrast_ratio, 0.35, 0.85))

            # Step F: Blend
            output = inpainted.copy()
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
                alpha_slice = resized_t5_alpha[ty1:ty2, tx1:tx2, np.newaxis] * current_opacity
                
                blended = bg_slice * (1.0 - alpha_slice) + (bg_slice * blend_slice / 255.0) * alpha_slice
                output[y1:y2, x1:x2] = np.clip(blended, 0, 255).astype(np.uint8)
                
            okk_dir = os.path.join(args.folder, "OKK")
            os.makedirs(okk_dir, exist_ok=True)
            base_name, _ = os.path.splitext(filename)
            output_filename = f"{base_name}_ok.jpg"
            output_path = os.path.join(okk_dir, output_filename)
            
            write_image_utf8(output_path, output)
            print(f"[OK] {filename} -> OKK\\{output_filename} (month score: {max_val_m:.4f}, scale: {scale_y:.3f}, opacity: {current_opacity:.3f})")
            processed_count += 1
            
        except Exception as e:
            print(f"[ERROR] Failed to process {filename}. Error: {e}")
            errors_count += 1

    print("\n" + "="*40)
    print("Batch Processing Summary:")
    print(f"Total processed and modified: {processed_count}")
    print(f"Total skipped (no target): {skipped_count}")
    print(f"Errors encountered: {errors_count}")
    print("="*40)

if __name__ == "__main__":
    main()
