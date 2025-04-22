import cv2
import numpy as np

def extract_minutiae(processed_img: np.ndarray, threshold: int = 50):
    """
    Extract minutiae points from a preprocessed fingerprint image using gradient-based segmentation.
    Classify points as 'ending' or 'bifurcation' based on local neighborhood.
    """
    # Compute image gradients using Sobel operators
    grad_x = cv2.Sobel(processed_img, cv2.CV_64F, 1, 0, ksize=3)
    grad_y = cv2.Sobel(processed_img, cv2.CV_64F, 0, 1, ksize=3)
    gradient_magnitude = np.sqrt(grad_x**2 + grad_y**2)
    gradient_magnitude = np.uint8(gradient_magnitude)
    
    # Threshold to create binary image
    _, binary_img = cv2.threshold(gradient_magnitude, threshold, 255, cv2.THRESH_BINARY)
    
    minutiae_points = []
    rows, cols = binary_img.shape
    for y in range(1, rows - 1):
        for x in range(1, cols - 1):
            if binary_img[y, x] == 255:
                # Get 3x3 neighborhood
                neighborhood = binary_img[y-1:y+2, x-1:x+2]
                count = int(np.count_nonzero(neighborhood)) - 1  # exclude center
                if count == 1:
                    minutiae_points.append({'x': x, 'y': y, 'type': 'ending'})
                elif count > 2:
                    minutiae_points.append({'x': x, 'y': y, 'type': 'bifurcation'})
    return minutiae_points
