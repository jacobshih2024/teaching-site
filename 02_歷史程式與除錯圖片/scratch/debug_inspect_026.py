import cv2
import numpy as np
import os

def read_image_utf8(path):
    return cv2.imdecode(np.fromfile(path, dtype=np.uint8), cv2.IMREAD_COLOR)

test_dir = r"測試SKILLS_ok_026-同慶里-廢棄物清除呈報-115.05.06"
img_path = os.path.join(test_dir, "LINE_ALBUM_同慶里廢棄物呈報_260311_2.jpg")
img = read_image_utf8(img_path)

if img is not None:
    # Save a resized version of the whole image to check
    h, w = img.shape[:2]
    resized = cv2.resize(img, (w // 4, h // 4))
    cv2.imwrite("debug_026_img2.png", resized)
    print("Saved debug_026_img2.png")
else:
    print("Could not load image 2")
