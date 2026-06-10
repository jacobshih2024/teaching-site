from psd_tools import PSDImage
import numpy as np
import cv2
import os

psd_path = r"測試SKILLS_08_2\09.psd"
psd = PSDImage.open(psd_path)

for i, layer in enumerate(psd):
    try:
        img_pil = layer.composite()
        img_np = np.array(img_pil)
        cv2.imwrite(f"debug_09_layer_{i}.png", cv2.cvtColor(img_np, cv2.COLOR_RGBA2BGRA))
        print(f"Layer {i} composite saved successfully.")
    except Exception as e:
        print(f"Layer {i} composite failed: {e}")
