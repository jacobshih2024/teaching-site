import cv2
import numpy as np
import os

def read_image_utf8(path):
    return cv2.imdecode(np.fromfile(path, dtype=np.uint8), cv2.IMREAD_COLOR)

# Load image 41
test_dir = r"case001\test_004-頂崁里-廢棄物清除呈報-115.05.13"
img41_path = os.path.join(test_dir, 'LINE_ALBUM_頂崁里廢棄物呈報_260128_41.jpg')
img41 = read_image_utf8(img41_path)

# Crop the date area on the whiteboard (around x=200 to 400, y=550 to 650)
date_crop = img41[550:650, 200:400]
cv2.imwrite("date_crop_41.png", date_crop)
print(f"Date crop saved. Let's find matches of the month '1' template inside this region.")

# Template Month 1 is cropped from: img41[599:621, 276:290]
temp = img41[599:621, 276:290]
temp_gray = cv2.cvtColor(temp, cv2.COLOR_BGR2GRAY)
crop_gray = cv2.cvtColor(date_crop, cv2.COLOR_BGR2GRAY)

# Find all locations with template matching
res = cv2.matchTemplate(crop_gray, temp_gray, cv2.TM_CCOEFF_NORMED)
loc = np.where(res >= 0.75)

print("\nMatches found in date crop (relative coordinates):")
matches = []
for pt in zip(*loc[::-1]):
    # Filter matches to avoid overlapping
    overlap = False
    for m in matches:
        if abs(m[0] - pt[0]) < 10 and abs(m[1] - pt[1]) < 10:
            overlap = True
            break
    if not overlap:
        score = res[pt[1], pt[0]]
        # Absolute coordinates on original image:
        abs_x = pt[0] + 200
        abs_y = pt[1] + 550
        matches.append((pt[0], pt[1], score, abs_x, abs_y))
        print(f"  Relative x={pt[0]}, y={pt[1]} (Score: {score:.4f}) -> Abs x={abs_x}, y={abs_y}")
