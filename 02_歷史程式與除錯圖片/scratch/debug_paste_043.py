import cv2
import numpy as np
import os
from psd_tools import PSDImage

def read_image_utf8(path, flags=cv2.IMREAD_COLOR):
    return cv2.imdecode(np.fromfile(path, dtype=np.uint8), flags)

test_dir = r"測試SKILLS_043-永興里-廢棄物清除呈報-115.05.06"
img_path = os.path.join(test_dir, "LINE_ALBUM_永興里廢棄物呈報_260311_2.jpg")
target = read_image_utf8(img_path)

# Extract PSD layer
psd_path = os.path.join(test_dir, "08.psd")
psd = PSDImage.open(psd_path)
layer = psd[1]
img_pil = layer.composite()
t5_bgra = cv2.cvtColor(np.array(img_pil), cv2.COLOR_RGBA2BGRA)

t5_bgr = t5_bgra[:, :, :3].astype(float)
t5_alpha = t5_bgra[:, :, 3].astype(float) / 255.0

# Mock matched coordinates (we know them from the previous run)
x = 313
y = 592
w = 30
h = 25
scale_y = 0.990

# Perform Step E resizing and alignment
new_w = int(t5_bgra.shape[1] * scale_y)
new_h = int(t5_bgra.shape[0] * scale_y)

resized_t5_bgr = cv2.resize(t5_bgr, (new_w, new_h), interpolation=cv2.INTER_AREA)
resized_t5_alpha = cv2.resize(t5_alpha, (new_w, new_h), interpolation=cv2.INTER_AREA)

# Stroke centroids
matched_region = cv2.cvtColor(target[y:y+h, x:x+w], cv2.COLOR_BGR2GRAY)
_, stroke_mask = cv2.threshold(matched_region, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

non_zero_orig = np.nonzero(stroke_mask)
stroke_cy_orig = np.mean(non_zero_orig[0])
stroke_cx_orig = np.mean(non_zero_orig[1])

non_zero_new = np.nonzero(resized_t5_alpha > 0.05)
stroke_cy_new = np.mean(non_zero_new[0])
stroke_cx_new = np.mean(non_zero_new[1])

paste_x = int(x + stroke_cx_orig - stroke_cx_new)
paste_y = int(y + stroke_cy_orig - stroke_cy_new)

print(f"Template shape: {t5_bgra.shape}")
print(f"Resized shape: {new_h}x{new_w}")
print(f"Original stroke center relative: {stroke_cy_orig:.2f}, {stroke_cx_orig:.2f}")
print(f"New stroke center relative: {stroke_cy_new:.2f}, {stroke_cx_new:.2f}")
print(f"Matched coordinate x={x}, y={y}")
print(f"Calculated paste position: paste_x={paste_x}, paste_y={paste_y}")

x1, y1 = max(0, paste_x), max(0, paste_y)
x2 = min(target.shape[1], paste_x + new_w)
y2 = min(target.shape[0], paste_y + new_h)

tx1 = x1 - paste_x
ty1 = y1 - paste_y
tx2 = tx1 + (x2 - x1)
ty2 = ty1 + (y2 - y1)

print(f"Paste slice bounds: target x:[{x1}, {x2}], y:[{y1}, {y2}]")
print(f"Template slice bounds: tx:[{tx1}, {tx2}], ty:[{ty1}, ty2:[{ty2}]")

# Let's save the cropped template slice to check if it has the digit "8"
cv2.imwrite("debug_resized_template.png", (resized_t5_alpha * 255).astype(np.uint8))
print("Saved debug_resized_template.png")
