import cv2
import numpy as np
import os

def read_image_utf8(path):
    return cv2.imdecode(np.fromfile(path, dtype=np.uint8), cv2.IMREAD_COLOR)

test_dir = r"測試SKILLS_ok_026-同慶里-廢棄物清除呈報-115.05.06"
img_path = os.path.join(test_dir, "LINE_ALBUM_同慶里廢棄物呈報_260311_2_ok.jpg")
img = read_image_utf8(img_path)

if img is not None:
    # Save a crop around the month digit to verify blending
    # In img, the matched year was found at scale 0.99 (almost 1.0).
    # Since year is at y: 595-635, x: 230-290, let's crop the date row: y: 580-640, x: 200-360
    crop = img[580:640, 200:360]
    cv2.imwrite("debug_blended_026_img2.png", crop)
    print("Saved debug_blended_026_img2.png")
else:
    print("Could not load output image")
