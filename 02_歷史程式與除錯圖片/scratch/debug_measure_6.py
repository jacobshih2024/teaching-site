import cv2
import numpy as np

wb_crop = cv2.imread("debug_wb_crop.png")
if wb_crop is not None:
    # Crop month "5" avoiding the underline: y from 265 to 290 (height 25px), x from 300 to 335
    month_crop = wb_crop[265:290, 300:335]
    cv2.imwrite("debug_month_no_underline.png", month_crop)
    print("Saved debug_month_no_underline.png")
    
    # Threshold it
    gray = cv2.cvtColor(month_crop, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    cv2.imwrite("debug_month_no_underline_thresh.png", thresh)
    
    # Check bounding box
    x_s, y_s, w_s, h_s = cv2.boundingRect(thresh)
    print(f"No underline stroke bounding box: x={x_s}, y={y_s}, w={w_s}, h={h_s}")
