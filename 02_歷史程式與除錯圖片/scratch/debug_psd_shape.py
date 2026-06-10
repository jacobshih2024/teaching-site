from psd_tools import PSDImage
import numpy as np

psd_path = r"測試SKILLS_ok_026-同慶里-廢棄物清除呈報-115.05.06\06.psd"
psd = PSDImage.open(psd_path)
layer1 = psd[1]
img_pil = layer1.composite()
img_np = np.array(img_pil)
print(f"PSD Layer 1 image shape: {img_np.shape}")

# Find alpha bounding box again
alpha = img_np[:, :, 3]
non_zero = np.nonzero(alpha)
if len(non_zero[0]) > 0:
    y_min, y_max = np.min(non_zero[0]), np.max(non_zero[0])
    x_min, x_max = np.min(non_zero[1]), np.max(non_zero[1])
    print(f"Non-zero alpha bounds: y in [{y_min}, {y_max}], x in [{x_min}, {x_max}]")
    print(f"Stroke size: h={y_max - y_min + 1}, w={x_max - x_min + 1}")
