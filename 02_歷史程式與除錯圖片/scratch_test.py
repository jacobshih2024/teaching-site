import cv2
import numpy as np
import os

def read_image_utf8(path):
    return cv2.imdecode(np.fromfile(path, dtype=np.uint8), cv2.IMREAD_COLOR)

def write_image_utf8(path, img):
    _, ext = os.path.splitext(path)
    is_success, im_buf_arr = cv2.imencode(ext, img)
    if is_success:
        im_buf_arr.tofile(path)
        return True
    return False

# Base directory
folder_path = r'case001\test_004-頂崁里-廢棄物清除呈報-115.05.13'

# Load original image 41 to crop template on the fly
img41_path = os.path.join(folder_path, 'LINE_ALBUM_頂崁里廢棄物呈報_260128_41.jpg')
img41 = read_image_utf8(img41_path)
if img41 is None:
    print('Failed to load image 41!')
    exit(1)

# Correct month "1" template coordinates: x=276, y=599, w=14, h=22
template = img41[599:621, 276:290]

# Load digit 5 template
digit5_path = os.path.join(folder_path, '0513_psd.png')
digit5_img = read_image_utf8(digit5_path)

if digit5_img is None:
    print('Failed to load 0513_psd.png!')
    exit(1)

# Convert to grayscale
temp_gray = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
digit5_gray = cv2.cvtColor(digit5_img, cv2.COLOR_BGR2GRAY)

for num in [41, 2]:
    img_path = os.path.join(folder_path, f'LINE_ALBUM_頂崁里廢棄物呈報_260128_{num}.jpg')
    target = read_image_utf8(img_path)
    if target is None:
        continue
    targ_gray = cv2.cvtColor(target, cv2.COLOR_BGR2GRAY)
    
    # 1. Locate the "1"
    found = None
    for scale in np.linspace(0.5, 2.0, 50):
        resized = cv2.resize(temp_gray, (0,0), fx=scale, fy=scale)
        if resized.shape[0] > targ_gray.shape[0] or resized.shape[1] > targ_gray.shape[1]:
            continue
        res = cv2.matchTemplate(targ_gray, resized, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, max_loc = cv2.minMaxLoc(res)
        if found is None or max_val > found[0]:
            found = (max_val, max_loc, scale, resized.shape)
            
    max_val, max_loc, scale, shape = found
    x, y = max_loc
    w, h = shape[1], shape[0]
    
    print(f'Image {num}: Matched "1" with confidence {max_val:.4f} at x={x}, y={y}')
    
    # 2. Precise stroke-based inpainting to clear "1"
    matched_region = targ_gray[y:y+h, x:x+w]
    _, stroke_mask = cv2.threshold(matched_region, 120, 255, cv2.THRESH_BINARY_INV)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    stroke_mask = cv2.dilate(stroke_mask, kernel, iterations=1)
    
    inpaint_mask = np.zeros(target.shape[:2], dtype=np.uint8)
    inpaint_mask[y:y+h, x:x+w] = stroke_mask
    inpainted = cv2.inpaint(target, inpaint_mask, 3, cv2.INPAINT_TELEA)
    
    # 3. Resize digit 5 template
    new_w = int(digit5_img.shape[1] * scale)
    new_h = int(digit5_img.shape[0] * scale)
    resized_digit5_gray = cv2.resize(digit5_gray, (new_w, new_h), interpolation=cv2.INTER_AREA)
    
    # 4. Paste using MULTIPLY blending
    center_x = x + w // 2
    center_y = y + h // 2
    paste_x = center_x - new_w // 2
    paste_y = center_y - new_h // 2
    
    output = inpainted.copy()
    for i in range(new_h):
        for j in range(new_w):
            py = paste_y + i
            px = paste_x + j
            if 0 <= py < output.shape[0] and 0 <= px < output.shape[1]:
                # Multiply blending factor (0.0 to 1.0)
                factor = resized_digit5_gray[i, j] / 255.0
                
                # Apply multiply blending to B, G, R channels
                output[py, px] = np.clip(output[py, px].astype(float) * factor, 0, 255).astype(np.uint8)
                
    # Save crop for inspection
    crop = output[y-20:y+h+20, x-40:x+w+40]
    write_image_utf8(os.path.join(folder_path, f'crop_multiply_{num}.jpg'), crop)
    print(f'Saved multiply crop for image {num}!')
