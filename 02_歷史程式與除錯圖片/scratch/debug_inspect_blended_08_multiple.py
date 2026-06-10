import cv2
import numpy as np
import os

def read_image_utf8(path):
    return cv2.imdecode(np.fromfile(path, dtype=np.uint8), cv2.IMREAD_COLOR)

test_dir = r"測試SKILLS_08"
img2 = read_image_utf8(os.path.join(test_dir, "LINE_ALBUM_頂崁里廢棄物呈報_260128_2_ok.jpg"))
img3 = read_image_utf8(os.path.join(test_dir, "LINE_ALBUM_頂崁里廢棄物呈報_260128_3_ok.jpg"))

if img2 is not None and img3 is not None:
    # Crop date rows
    crop2 = img2[580:640, 140:340]
    crop3 = img3[580:640, 140:340]
    
    cv2.imwrite("debug_blended_08_img2.png", crop2)
    cv2.imwrite("debug_blended_08_img3.png", crop3)
    print("Saved debug_blended_08_img2.png and debug_blended_08_img3.png")
else:
    print("Could not load output images")
