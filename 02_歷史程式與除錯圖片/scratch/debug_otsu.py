import cv2
import numpy as np
import os

def read_image_utf8(path):
    return cv2.imdecode(np.fromfile(path, dtype=np.uint8), cv2.IMREAD_COLOR)

# Paths
test_dir = r"測試SKILLS_ok_026-同慶里-廢棄物清除呈報-115.05.06"
t_path = os.path.join(test_dir, "06.psd")
ref_img_path = os.path.join(test_dir, "LINE_ALBUM_同慶里廢棄物呈報_260311_2.jpg")

ref_img = read_image_utf8(ref_img_path)
h_img, w_img = ref_img.shape[:2]

# Crop templates
# Year: 595,635,230,290
# Month: 595,635,300,335
year_temp = ref_img[595:635, 230:290]
year_gray = cv2.cvtColor(year_temp, cv2.COLOR_BGR2GRAY)

month_temp = ref_img[595:635, 300:335]
month_gray = cv2.cvtColor(month_temp, cv2.COLOR_BGR2GRAY)

# Match year in image 2
img = read_image_utf8(ref_img_path)
targ_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

found_year = None
for scale in np.linspace(0.5, 2.0, 50):
    resized_year = cv2.resize(year_gray, (0,0), fx=scale, fy=scale)
    if resized_year.shape[0] > targ_gray.shape[0] or resized_year.shape[1] > targ_gray.shape[1]:
        continue
    res = cv2.matchTemplate(targ_gray, resized_year, cv2.TM_CCOEFF_NORMED)
    _, max_val, _, max_loc = cv2.minMaxLoc(res)
    if found_year is None or max_val > found_year[0]:
        found_year = (max_val, max_loc, scale, resized_year.shape)

max_val_y, max_loc_y, scale_y, shape_y = found_year
xy, yy = max_loc_y

# Month ROI
x_start = int(xy + (300 - 230 - 10) * scale_y)
x_end = int(xy + (335 - 230 + 10) * scale_y)
y_start = int(yy - 10 * scale_y)
y_end = int(yy + 50 * scale_y)

x_start = max(0, min(x_start, w_img - 1))
x_end = max(0, min(x_end, w_img))
y_start = max(0, min(y_start, h_img - 1))
y_end = max(0, min(y_end, h_img))

roi = targ_gray[y_start:y_end, x_start:x_end]
resized_month = cv2.resize(month_gray, (0,0), fx=scale_y, fy=scale_y)
res_m = cv2.matchTemplate(roi, resized_month, cv2.TM_CCOEFF_NORMED)
_, max_val_m, _, max_loc_m = cv2.minMaxLoc(res_m)

x = x_start + max_loc_m[0]
y = y_start + max_loc_m[1]
w, h = resized_month.shape[1], resized_month.shape[0]

# Try to extract stroke using OTSU
matched_region = targ_gray[y:y+h, x:x+w]
_, otsu_mask = cv2.threshold(matched_region, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
otsu_mask_dilated = cv2.dilate(otsu_mask, kernel, iterations=1)

# Check bounding box of the stroke of original matched region
x_s, y_s, w_s, h_s = cv2.boundingRect(otsu_mask)
print(f"Original matched region stroke bounding box: x={x_s}, y={y_s}, w={w_s}, h={h_s}")

# Load template 6 from PSD
from psd_tools import PSDImage
psd = PSDImage.open(t_path)
layer1 = psd[1]
img_pil = layer1.composite()
img_np = np.array(img_pil)
t6_bgra = cv2.cvtColor(img_np, cv2.COLOR_RGBA2BGRA)

# Get bounding box of transparent template 6 (non-transparent pixels)
alpha = t6_bgra[:, :, 3]
_, alpha_mask = cv2.threshold(alpha, 10, 255, cv2.THRESH_BINARY)
x_t, y_t, w_t, h_t = cv2.boundingRect(alpha_mask)
print(f"New digit template 6 stroke bounding box: x={x_t}, y={y_t}, w={w_t}, h={h_t}")

# Let's write the crop of the templates to verify
cv2.imwrite("debug_otsu_mask.png", otsu_mask_dilated)
print("Saved debug_otsu_mask.png")
