import cv2
import numpy as np
import os

def read_image_utf8(path):
    return cv2.imdecode(np.fromfile(path, dtype=np.uint8), cv2.IMREAD_COLOR)

# Load the original image from folder 08
ref_path = r"測試SKILLS_08\LINE_ALBUM_頂崁里廢棄物呈報_260128_2.jpg"
target = read_image_utf8(ref_path)
targ_gray = cv2.cvtColor(target, cv2.COLOR_BGR2GRAY)

# Coordinates for Month "1"
x_start = 235
y_start = 595
w = 260 - 235
h = 620 - 595

matched_region = targ_gray[y_start:y_start+h, x_start:x_start+w]
_, stroke_mask = cv2.threshold(matched_region, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
stroke_mask_dilated = cv2.dilate(stroke_mask, kernel, iterations=2)

# Save mask WITHOUT protection
inpaint_mask_no_prot = np.zeros(target.shape[:2], dtype=np.uint8)
inpaint_mask_no_prot[y_start:y_start+h, x_start:x_start+w] = stroke_mask_dilated
inpainted_no_prot = cv2.inpaint(target, inpaint_mask_no_prot, 3, cv2.INPAINT_TELEA)

# Save mask WITH protection (protect bottom 3 rows)
stroke_mask_dilated_prot = stroke_mask_dilated.copy()
stroke_mask_dilated_prot[-3:, :] = 0
inpaint_mask_prot = np.zeros(target.shape[:2], dtype=np.uint8)
inpaint_mask_prot[y_start:y_start+h, x_start:x_start+w] = stroke_mask_dilated_prot
inpainted_prot = cv2.inpaint(target, inpaint_mask_prot, 3, cv2.INPAINT_TELEA)

# Crop both to compare
crop_no_prot = inpainted_no_prot[580:640, 140:340]
crop_prot = inpainted_prot[580:640, 140:340]

cv2.imwrite("debug_crop_no_prot.png", crop_no_prot)
cv2.imwrite("debug_crop_prot.png", crop_prot)
print("Saved debug_crop_no_prot.png and debug_crop_prot.png")
