import cv2
import numpy as np
import os

def read_image_utf8(path):
    return cv2.imdecode(np.fromfile(path, dtype=np.uint8), cv2.IMREAD_COLOR)

# Paths
ok_dir = r"case001\ok_004-頂崁里-廢棄物清除呈報-115.05.13"
test_dir = r"case001\test_004-頂崁里-廢棄物清除呈報-115.05.13"

# Let's inspect image 10 and 11
for num in [10, 11, 12]:
    filename = f"LINE_ALBUM_頂崁里廢棄物呈報_260128_{num}.jpg"
    orig_path = os.path.join(test_dir, filename)
    user_path = os.path.join(ok_dir, filename)
    opencv_path = os.path.join(test_dir, f"LINE_ALBUM_頂崁里廢棄物呈報_260128_{num}_ok.jpg")
    
    if not (os.path.exists(orig_path) and os.path.exists(user_path) and os.path.exists(opencv_path)):
        print(f"Skipping {num} - missing files.")
        continue
        
    img_orig = read_image_utf8(orig_path)
    img_user = read_image_utf8(user_path)
    img_opencv = read_image_utf8(opencv_path)
    
    # User diff (clean difference, thresholding high enough to filter out JPEG noise)
    diff_user = cv2.absdiff(img_orig, img_user)
    gray_diff_user = cv2.cvtColor(diff_user, cv2.COLOR_BGR2GRAY)
    _, thresh_user = cv2.threshold(gray_diff_user, 20, 255, cv2.THRESH_BINARY)
    
    contours_user, _ = cv2.findContours(thresh_user, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if not contours_user:
        print(f"No edit found in user image {num}!")
        continue
        
    xu, yu, wu, hu = cv2.boundingRect(np.vstack(contours_user))
    print(f"\n--- Image {num} ---")
    print(f"User edit region: x={xu}, y={yu}, w={wu}, h={hu}")
    
    # Let's crop this region from all three images
    crop_orig = img_orig[yu:yu+hu, xu:xu+wu]
    crop_user = img_user[yu:yu+hu, xu:xu+wu]
    crop_opencv = img_opencv[yu:yu+hu, xu:xu+wu]
    
    # Calculate some metrics
    # 1. Background color (where the user edited vs original)
    # Let's see if the user erased the original "1" completely.
    # In the original, there was a "1". Let's check the pixel values.
    # Let's save these crops to compare them.
    cv2.imwrite(f"crop_orig_{num}.png", crop_orig)
    cv2.imwrite(f"crop_user_{num}.png", crop_user)
    cv2.imwrite(f"crop_opencv_{num}.png", crop_opencv)
    
    # Print average color of user's digit "5" vs OpenCV's digit "5"
    # The digit "5" is dark. Let's find the minimum brightness in the crop.
    gray_orig = cv2.cvtColor(crop_orig, cv2.COLOR_BGR2GRAY)
    gray_user = cv2.cvtColor(crop_user, cv2.COLOR_BGR2GRAY)
    gray_cv = cv2.cvtColor(crop_opencv, cv2.COLOR_BGR2GRAY)
    
    print(f"Original min gray: {np.min(gray_orig)}, mean: {np.mean(gray_orig):.1f}")
    print(f"User min gray: {np.min(gray_user)}, mean: {np.mean(gray_user):.1f}")
    print(f"OpenCV min gray: {np.min(gray_cv)}, mean: {np.mean(gray_cv):.1f}")
    
    # Let's check if the user's version has any "white halos" or if it is a pure overlay
    # We can inspect the distribution of pixels.
    # Let's print out the exact RGB values of the user's edit vs opencv's edit.
    # To do this, let's find the difference between user's crop and original crop.
    diff_crop = cv2.absdiff(crop_orig, crop_user)
    print("User edit diff statistics (non-zero pixels):")
    non_zero = diff_crop[np.any(diff_crop > 10, axis=-1)]
    if len(non_zero) > 0:
        print(f"  Max change: {np.max(non_zero)}, Mean change: {np.mean(non_zero):.1f}")
    else:
        print("  No significant change detected in cropped region.")
