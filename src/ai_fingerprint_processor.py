import cv2
import numpy as np
import matplotlib.pyplot as plt

def shi_tomasi_feature_extraction(image_path, max_corners=100, quality_level=0.01, min_distance=10):
    # Load the input image in grayscale
    img = cv2.imread(image_path)
    
    if img is None:
        print("Error: Image not found or unable to load.")
        return None
    
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    gray = cv2.GaussianBlur(gray, (5, 5), 0)

    corners = cv2.goodFeaturesToTrack(gray, maxCorners=max_corners, qualityLevel=quality_level, minDistance=min_distance)
    
    if corners is None:
        print("No corners detected.")
        return None
    
    corners = np.int0(corners)

    for i in corners:
        x, y = i.ravel()
        cv2.circle(img, (x, y), 5, (0, 255, 0), -1)

    # Display the image with detected corners
    plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    plt.title("Shi-Tomasi Corner Detection")
    plt.show()

    return corners

def save_features(corners, output_file):
    np.savetxt(output_file, corners.reshape(-1, 2), fmt="%d", delimiter=",")
    print(f"Features saved to {output_file}")

image_path = "fingerprint_sample.jpg"  

corners = shi_tomasi_feature_extraction(image_path)

if corners is not None:
    print("Extracted Corners (Features):")
    for corner in corners:
        print(corner.ravel())

    save_features(corners, "extracted_features.txt")
