from psd_tools import PSDImage
import numpy as np
import cv2
import os

psd_path = r"測試SKILLS_043-永興里-廢棄物清除呈報-115.05.06\08.psd"
psd = PSDImage.open(psd_path)

print(f"PSD structure: {psd}")
for i, layer in enumerate(psd):
    print(f"Layer {i}: name={layer.name}, kind={layer.kind}, visible={layer.is_visible()}, size={layer.size}")
    try:
        img_pil = layer.composite()
        img_np = np.array(img_pil)
        print(f"  Shape: {img_np.shape}")
        # Save layer
        cv2.imwrite(f"debug_layer_{i}.png", cv2.cvtColor(img_np, cv2.COLOR_RGBA2BGRA))
    except Exception as e:
        print(f"  Error composite layer {i}: {e}")
