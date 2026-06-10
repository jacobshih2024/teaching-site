from psd_tools import PSDImage
import numpy as np
import cv2
import os

psd_path = r"測試SKILLS_08\08_OK.psd"
psd = PSDImage.open(psd_path)

print(f"PSD structure: {psd}")
for i, layer in enumerate(psd):
    print(f"Layer {i}: name={layer.name}, kind={layer.kind}, visible={layer.is_visible()}, size={layer.size}")
