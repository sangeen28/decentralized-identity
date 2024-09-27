import cv2
import numpy as np
import matplotlib.pyplot as plt

def shi_tomasi_feature_extraction(image_path, max_corners=100, quality_level=0.01, min_distance=10):
    # Load the input image in grayscale
    img = cv2.imread(image_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    corners = cv2.goodFeaturesToTrack(gray, maxCorners=max_corners, qualityLevel=quality_level, minDistance=min_distance)
    corners = np.int0(corners)

    for i in corners:
        x, y = i.ravel()
        cv2.circle(img, (x, y), 5, (0, 255, 0), -1)

    plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    plt.title("Shi-Tomasi Corner Detection")
    plt.show()

    return corners

image_path = "fingerprint_sample.jpg"  

corners = shi_tomasi_feature_extraction(image_path)

print("Extracted Corners (Features):")
for corner in corners:
    print(corner.ravel())

