import cv2
import numpy as np

def read_image_utf8(path):
    return cv2.imdecode(np.fromfile(path, dtype=np.uint8), cv2.IMREAD_COLOR)

ref_path = r"測試SKILLS_08\LINE_ALBUM_頂崁里廢棄物呈報_260128_2.jpg"
img = read_image_utf8(ref_path)

if img is not None:
    # Year: 595,625,155,210
    # Month: 595,620,235,260
    # Let's crop day region around 595,625,290,345
    crop = img[590:630, 290:345]
    cv2.imwrite("debug_08_day.png", crop)
    print("Saved debug_08_day.png")
else:
    print("Could not load image")
