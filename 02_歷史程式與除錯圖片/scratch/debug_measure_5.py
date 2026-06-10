import cv2
import numpy as np

wb_crop = cv2.imread("debug_wb_crop.png")
if wb_crop is not None:
    # Crop month "5" avoiding grid lines: y from 275 to 305 (height 30px), x from 300 to 335
    month_crop = wb_crop[275:305, 300:335]
    cv2.imwrite("debug_month_clean.png", month_crop)
    print("Saved debug_month_clean.png")
    
    # Let's threshold it to see if we only get the digit 5
    gray = cv2.cvtColor(month_crop, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    cv2.imwrite("debug_month_clean_thresh.png", thresh)
    print("Saved debug_month_clean_thresh.png")
    
    # Check bounding box of the thresholded digit
    x_s, y_s, w_s, h_s = cv2.boundingRect(thresh)
    print(f"Clean month digit stroke bounding box: x={x_s}, y={y_s}, w={w_s}, h={h_s}")
