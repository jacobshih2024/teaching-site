import cv2
import numpy as np
import os

def read_image_utf8(path):
    return cv2.imdecode(np.fromfile(path, dtype=np.uint8), cv2.IMREAD_COLOR)

test_dir = r"測試SKILLS_08"
img_path = os.path.join(test_dir, "LINE_ALBUM_頂崁里廢棄物呈報_260128_2.jpg")
img = read_image_utf8(img_path)

if img is not None:
    h, w = img.shape[:2]
    print(f"Image 2 size: {w}x{h}")
    
    # Save a crop of the date row to inspect whiteboard coordinates
    # For Case 004 (頂崁里), the original date is "中華民國115 年 1 月 28 日"
    # Let's crop x: 150 to 350, y: 580 to 640
    crop = img[580:640, 150:350].copy()
    
    # Draw vertical lines to measure
    for x_offset in range(0, 200, 10):
        x_pos = x_offset
        cv2.line(crop, (x_pos, 0), (x_pos, 60), (0, 0, 255), 1)
        if x_offset % 20 == 0:
            cv2.putText(crop, str(150 + x_offset), (x_pos, 15), cv2.FONT_HERSHEY_SIMPLEX, 0.3, (0, 255, 0), 1)
            
    cv2.imwrite("debug_08_ruler.png", crop)
    print("Saved debug_08_ruler.png")
else:
    print("Could not load image 2")
