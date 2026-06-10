import cv2
import numpy as np
import os

def read_image_utf8(path):
    return cv2.imdecode(np.fromfile(path, dtype=np.uint8), cv2.IMREAD_COLOR)

test_dir = r"測試SKILLS_043-永興里-廢棄物清除呈報-115.05.06"
img = read_image_utf8(os.path.join(test_dir, "LINE_ALBUM_永興里廢棄物呈報_260311_2.jpg"))

if img is not None:
    # Crop using the same coordinates as Case 026
    year_crop = img[590:625, 230:290]
    month_crop = img[590:615, 300:335]
    
    cv2.imwrite("debug_043_year.png", year_crop)
    cv2.imwrite("debug_043_month.png", month_crop)
    print("Saved debug_043_year.png and debug_043_month.png")
