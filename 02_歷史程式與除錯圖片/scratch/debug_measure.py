import cv2
import numpy as np

wb_crop = cv2.imread("debug_wb_crop.png")
if wb_crop is not None:
    # Let's crop the date row: y from 260 to 325, x from 80 to 380
    date_row = wb_crop[260:320, 80:380]
    cv2.imwrite("debug_date_row.png", date_row)
    print("Saved debug_date_row.png")
    
    # Let's crop year "115" specifically: y from 270 to 310, x from 145 to 195
    year_crop = wb_crop[270:310, 145:195]
    cv2.imwrite("debug_year_crop.png", year_crop)
    print("Saved debug_year_crop.png")

    # Let's crop month "5" specifically: y from 270 to 310, x from 220 to 255
    month_crop = wb_crop[270:310, 220:255]
    cv2.imwrite("debug_month_crop.png", month_crop)
    print("Saved debug_month_crop.png")
