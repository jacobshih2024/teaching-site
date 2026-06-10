import cv2
import numpy as np
import os

def read_image_utf8(path):
    return cv2.imdecode(np.fromfile(path, dtype=np.uint8), cv2.IMREAD_COLOR)

test_dir = r"測試SKILLS_043-永興里-廢棄物清除呈報-115.05.06"
img = read_image_utf8(os.path.join(test_dir, "LINE_ALBUM_永興里廢棄物呈報_260311_2.jpg"))

if img is not None:
    h, w = img.shape[:2]
    # Crop bottom-left
    wb_crop = img[int(h*0.5):h, 0:int(w*0.5)]
    cv2.imwrite("debug_043_wb_2.png", wb_crop)
    print("Saved debug_043_wb_2.png")
