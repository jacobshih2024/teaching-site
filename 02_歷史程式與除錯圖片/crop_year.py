import cv2
import numpy as np
import os

def read_image_utf8(path):
    return cv2.imdecode(np.fromfile(path, dtype=np.uint8), cv2.IMREAD_COLOR)

# Load image 41
test_dir = r"case001\test_004-頂崁里-廢棄物清除呈報-115.05.13"
img41_path = os.path.join(test_dir, 'LINE_ALBUM_頂崁里廢棄物呈報_260128_41.jpg')
img41 = read_image_utf8(img41_path)

# Let's crop the year "115" (or "115.")
# Since the month "1" is at x=276, y=599, the year "115." should be just to the left.
# Let's crop x from 195 to 270, y from 595 to 625.
year_crop = img41[595:625, 195:270]
cv2.imwrite("year_crop_41.png", year_crop)
print("Saved year_crop_41.png")
