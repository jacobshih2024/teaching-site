import cv2
import numpy as np
import os

def read_image_utf8(path):
    return cv2.imdecode(np.fromfile(path, dtype=np.uint8), cv2.IMREAD_COLOR)

test_dir = r"測試SKILLS_043-永興里-廢棄物清除呈報-115.05.06"
orig = read_image_utf8(os.path.join(test_dir, "LINE_ALBUM_永興里廢棄物呈報_260311_2.jpg"))
ok = read_image_utf8(os.path.join(test_dir, "LINE_ALBUM_永興里廢棄物呈報_260311_2_ok.jpg"))

if orig is not None and ok is not None:
    diff = cv2.absdiff(orig, ok)
    gray_diff = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
    non_zero = np.sum(gray_diff > 0)
    print(f"Total different pixels between original and ok: {non_zero}")
    if non_zero > 0:
        # Save diff image
        cv2.imwrite("debug_043_diff.png", diff)
        print("Saved debug_043_diff.png")
        
        # Check coordinates of difference
        diff_coords = np.argwhere(gray_diff > 0)
        y_min, x_min = np.min(diff_coords, axis=0)
        y_max, x_max = np.max(diff_coords, axis=0)
        print(f"Difference region: y in [{y_min}, {y_max}], x in [{x_min}, {x_max}]")
else:
    print("Could not load images")
