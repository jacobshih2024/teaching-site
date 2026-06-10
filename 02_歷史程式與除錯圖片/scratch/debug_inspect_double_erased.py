import cv2
import numpy as np
import os

def read_image_utf8(path):
    return cv2.imdecode(np.fromfile(path, dtype=np.uint8), cv2.IMREAD_COLOR)

test_dir = r"測試SKILLS_08_雙空白"
img_path = os.path.join(test_dir, "LINE_ALBUM_頂崁里廢棄物呈報_260128_2_ok.jpg")
img = read_image_utf8(img_path)

if img is not None:
    # Crop the date line region to check both month and day fields
    crop = img[580:640, 140:360]
    cv2.imwrite("debug_double_erased_08_img2.png", crop)
    print("Saved debug_double_erased_08_img2.png")
else:
    print("Could not load output image")
