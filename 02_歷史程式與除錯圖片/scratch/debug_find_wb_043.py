import cv2
import numpy as np
import os

def read_image_utf8(path):
    return cv2.imdecode(np.fromfile(path, dtype=np.uint8), cv2.IMREAD_COLOR)

test_dir = r"測試SKILLS_043-永興里-廢棄物清除呈報-115.05.06"

for i in range(1, 16):
    img_name = f"LINE_ALBUM_永興里廢棄物呈報_260311_{i}.jpg"
    img_path = os.path.join(test_dir, img_name)
    img = read_image_utf8(img_path)
    if img is not None:
        h, w = img.shape[:2]
        # Let's save a thumbnail of all images to see which ones are whiteboards
        resized = cv2.resize(img, (120, 90))
        # Print if the image is likely a whiteboard (whiteboards are very bright/white)
        # Let's write the thumbnails to a folder debug_thumbs
        os.makedirs("debug_thumbs", exist_ok=True)
        cv2.imwrite(f"debug_thumbs/thumb_{i}.png", resized)
        
        # Let's print some info to find the whiteboard
        # A whiteboard usually has a large white region. We can check average brightness
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        mean_val = np.mean(gray)
        print(f"Image {i}: size {w}x{h}, mean brightness {mean_val:.1f}")
