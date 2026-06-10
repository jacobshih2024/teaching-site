import cv2
import numpy as np

wb_crop = cv2.imread("debug_wb_crop.png")
if wb_crop is not None:
    # Crop month "5"
    month_crop = wb_crop[270:310, 315:350]
    cv2.imwrite("debug_month_crop_correct_2.png", month_crop)
    print("Saved debug_month_crop_correct_2.png")
