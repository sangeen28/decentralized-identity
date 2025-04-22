import cv2
import numpy as np

def preprocess_fingerprint(image_path: str) -> np.ndarray:
    """
    Load a fingerprint image in grayscale, apply adaptive median filtering,
    and enhance the contrast using histogram equalization.
    """
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if img is None:
        raise ValueError("Image not found or invalid image path")
    
    # Adaptive median filtering (using a simple medianBlur here)
    denoised = cv2.medianBlur(img, 3)
    
    # Contrast enhancement using histogram equalization
    enhanced = cv2.equalizeHist(denoised)
    
    return enhanced
