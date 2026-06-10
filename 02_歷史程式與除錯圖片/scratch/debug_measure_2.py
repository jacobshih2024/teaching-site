import cv2
import numpy as np

wb_crop = cv2.imread("debug_wb_crop.png")
if wb_crop is not None:
    # Crop year "115"
    year_crop = wb_crop[270:310, 230:290]
    cv2.imwrite("debug_year_crop_correct.png", year_crop)
    print("Saved debug_year_crop_correct.png")

    # Crop month "5"
    month_crop = wb_crop[270:310, 340:380]
    cv2.imwrite("debug_month_crop_correct.png", month_crop)
    print("Saved debug_month_crop_correct.png")
