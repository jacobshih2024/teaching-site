import cv2
import numpy as np
import os
from psd_tools import PSDImage

test_dir = r"測試SKILLS_043-永興里-廢棄物清除呈報-115.05.06"
psd_path = os.path.join(test_dir, "08.psd")
psd = PSDImage.open(psd_path)
layer = psd[1]
img_pil = layer.composite()
t5_bgra = cv2.cvtColor(np.array(img_pil), cv2.COLOR_RGBA2BGRA)

alpha = t5_bgra[:, :, 3]
print(f"Alpha channel shape: {alpha.shape}")
print(f"Min alpha: {np.min(alpha)}, Max alpha: {np.max(alpha)}")
print(f"Number of non-zero pixels: {np.sum(alpha > 0)}")

# Let's check the BGR values as well
bgr = t5_bgra[:, :, :3]
print(f"BGR min: {np.min(bgr)}, max: {np.max(bgr)}")
