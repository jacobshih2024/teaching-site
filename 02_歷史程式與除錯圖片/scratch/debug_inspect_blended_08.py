import cv2
import numpy as np
import os

def read_image_utf8(path):
    return cv2.imdecode(np.fromfile(path, dtype=np.uint8), cv2.IMREAD_COLOR)

test_dir = r"測試SKILLS_08"
img_path = os.path.join(test_dir, "LINE_ALBUM_頂崁里廢棄物呈報_260128_2_ok.jpg")
img = read_image_utf8(img_path)

if img is not None:
    # Save a crop around the month digit to verify blending
    # Year: 595:625, 155:210
    crop = img[580:640, 140:340]
    cv2.imwrite("debug_blended_08_img2.png", crop)
    print("Saved debug_blended_08_img2.png")
else:
    print("Could not load output image")
