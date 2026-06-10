import cv2
import numpy as np
import os

def read_image_utf8(path):
    return cv2.imdecode(np.fromfile(path, dtype=np.uint8), cv2.IMREAD_COLOR)

test_dir = r"測試SKILLS_004-頂崁里-廢棄物清除呈報-115.05.13"

# Check image 1
img1 = read_image_utf8(os.path.join(test_dir, "LINE_ALBUM_頂崁里廢棄物呈報_260128_1.jpg"))
if img1 is not None:
    # Let's save a resized version to check what it looks like
    h, w = img1.shape[:2]
    resized = cv2.resize(img1, (w // 4, h // 4))
    cv2.imwrite("debug_img1.png", resized)
    print("Saved debug_img1.png")

# Check image 10
img10 = read_image_utf8(os.path.join(test_dir, "LINE_ALBUM_頂崁里廢棄物呈報_260128_10.jpg"))
if img10 is not None:
    h, w = img10.shape[:2]
    resized = cv2.resize(img10, (w // 4, h // 4))
    cv2.imwrite("debug_img10.png", resized)
    print("Saved debug_img10.png")
