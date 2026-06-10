import cv2
import numpy as np
import os

def read_image_utf8(path):
    return cv2.imdecode(np.fromfile(path, dtype=np.uint8), cv2.IMREAD_COLOR)

test_dir = r"測試SKILLS_043-永興里-廢棄物清除呈報-115.05.06"
img = read_image_utf8(os.path.join(test_dir, "LINE_ALBUM_永興里廢棄物呈報_260311_2.jpg"))

if img is not None:
    # Crop the date row from x=180 to 380, y=585 to 630
    crop = img[585:630, 180:380].copy()
    
    # Draw vertical lines every 10 pixels with text labels
    for x_offset in range(0, 200, 10):
        x_pos = x_offset
        cv2.line(crop, (x_pos, 0), (x_pos, 45), (0, 0, 255), 1)
        if x_offset % 20 == 0:
            cv2.putText(crop, str(180 + x_offset), (x_pos, 15), cv2.FONT_HERSHEY_SIMPLEX, 0.3, (0, 255, 0), 1)
            
    cv2.imwrite("debug_043_ruler.png", crop)
    print("Saved debug_043_ruler.png")
