import cv2
import numpy as np

def read_image_utf8(path):
    return cv2.imdecode(np.fromfile(path, dtype=np.uint8), cv2.IMREAD_COLOR)

ref_path = r"測試SKILLS_08\LINE_ALBUM_頂崁里廢棄物呈報_260128_2.jpg"
img = read_image_utf8(ref_path)

if img is not None:
    # Let's crop from y=580 to 650, x=140 to 360
    crop = img[580:650, 140:360]
    cv2.imwrite("debug_original_line.png", crop)
    print("Saved debug_original_line.png")
else:
    print("Could not load image")
