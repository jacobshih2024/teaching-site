import cv2
import numpy as np
import os

def read_image_utf8(path):
    return cv2.imdecode(np.fromfile(path, dtype=np.uint8), cv2.IMREAD_COLOR)

test_dir = r"測試SKILLS_ok_026-同慶里-廢棄物清除呈報-115.05.06"
img_path = os.path.join(test_dir, "LINE_ALBUM_同慶里廢棄物呈報_260311_2.jpg")
img = read_image_utf8(img_path)

if img is not None:
    print(f"Image dimensions: {img.shape}")
    # Let's save a crop of the bottom-left region where the whiteboard is
    # The image size is likely 1440x1080 or similar. Let's crop bottom-left: y from 500 to 1080, x from 0 to 600
    h, w = img.shape[:2]
    wb_crop = img[int(h*0.5):h, 0:int(w*0.5)]
    cv2.imwrite("debug_wb_crop.png", wb_crop)
    print("Saved debug_wb_crop.png")
