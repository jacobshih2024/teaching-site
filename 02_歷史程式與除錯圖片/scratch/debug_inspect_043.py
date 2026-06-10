import cv2
import numpy as np
import os

def read_image_utf8(path):
    return cv2.imdecode(np.fromfile(path, dtype=np.uint8), cv2.IMREAD_COLOR)

test_dir = r"測試SKILLS_043-永興里-廢棄物清除呈報-115.05.06"
img_path = os.path.join(test_dir, "LINE_ALBUM_永興里廢棄物呈報_260311_10.jpg")
img = read_image_utf8(img_path)

if img is not None:
    print(f"Image dimensions: {img.shape}")
    # Save resized whole image
    h, w = img.shape[:2]
    resized = cv2.resize(img, (w // 4, h // 4))
    cv2.imwrite("debug_043_img10.png", resized)
    print("Saved debug_043_img10.png")
    
    # Also save a crop of the bottom region where whiteboards usually are: y from 0.5*h to h, x from 0 to 0.6*w
    wb_crop = img[int(h*0.5):h, 0:int(w*0.6)]
    cv2.imwrite("debug_043_wb_crop.png", wb_crop)
    print("Saved debug_043_wb_crop.png")
else:
    print("Could not load image 10")
