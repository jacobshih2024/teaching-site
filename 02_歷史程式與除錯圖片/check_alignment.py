import cv2
import numpy as np

# Load test user ref and test layer blend
for num in [10, 11]:
    user = cv2.imread(f"test_user_ref_{num}.png")
    out = cv2.imread(f"test_layer_blend_{num}.png")
    
    if user is None or out is None:
        continue
        
    print(f"\n--- Alignment check for Image {num} ---")
    
    # Try shifts to minimize MAE
    best_mae = 999.0
    best_dx = 0
    best_dy = 0
    
    h, w, c = user.shape
    for dy in range(-5, 6):
        for dx in range(-5, 6):
            # Shift out
            M = np.float32([[1, 0, dx], [0, 1, dy]])
            shifted_out = cv2.warpAffine(out, M, (w, h), borderMode=cv2.BORDER_REPLICATE)
            
            # Compute difference
            mae = np.mean(cv2.absdiff(user, shifted_out))
            if mae < best_mae:
                best_mae = mae
                best_dx = dx
                best_dy = dy
                
    print(f"Best shift: dx={best_dx}, dy={best_dy} with MAE={best_mae:.2f}")
    
    # Let's see if the difference is mostly background (inpainting) or stroke (color)
    # Shift out by best shift
    M = np.float32([[1, 0, best_dx], [0, 1, best_dy]])
    shifted_out = cv2.warpAffine(out, M, (w, h), borderMode=cv2.BORDER_REPLICATE)
    
    # Let's check diff on the stroke region only
    # Stroke is where user has low brightness
    gray_user = cv2.cvtColor(user, cv2.COLOR_BGR2GRAY)
    stroke_mask = gray_user < 120
    
    if np.sum(stroke_mask) > 0:
        stroke_diff = cv2.absdiff(user[stroke_mask], shifted_out[stroke_mask])
        print(f"Stroke region MAE: {np.mean(stroke_diff):.2f}")
        
        # Background region diff
        bg_mask = ~stroke_mask
        bg_diff = cv2.absdiff(user[bg_mask], shifted_out[bg_mask])
        print(f"Background region MAE: {np.mean(bg_diff):.2f}")
        
        # Print actual stroke colors
        print(f"User stroke mean BGR: {np.mean(user[stroke_mask], axis=0)}")
        print(f"Shifted output stroke mean BGR: {np.mean(shifted_out[stroke_mask], axis=0)}")
