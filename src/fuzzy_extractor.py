import hashlib
import random
import numpy as np
import cv2

class FuzzyExtractor:
    def __init__(self, tolerance=10):
        self.tolerance = tolerance
    
    def gen(self, biometric_data):
        """
        Generate cryptographic key and helper data from biometric input (minutiae points).
        :param biometric_data: Byte format of extracted biometric data (minutiae points)
        :return: Hashed cryptographic key and helper data (salt)
        """
        salt = random.getrandbits(128)
        
        hashed_data = hashlib.sha256(biometric_data + salt.to_bytes(16, 'big')).hexdigest()
        
        helper_data = salt
        
        return hashed_data, helper_data
    
    def rep(self, biometric_data, helper_data):
        """
        Reproduce the cryptographic key using the biometric data and helper data (salt).
        :param biometric_data: Byte format of extracted biometric data (minutiae points)
        :param helper_data: Salt used to generate the original key
        :return: Reconstructed hashed cryptographic key
        """
        regenerated_data = hashlib.sha256(biometric_data + helper_data.to_bytes(16, 'big')).hexdigest()
        
        return regenerated_data


def shi_tomasi_feature_extraction(image_path, max_corners=100, quality_level=0.01, min_distance=10):
    """
    Extract Shi-Tomasi features from a fingerprint image.
    :param image_path: Path to the fingerprint image
    :return: Extracted corner points (minutiae points)
    """
    img = cv2.imread(image_path)
    
    if img is None:
        print("Error: Image not found or unable to load.")
        return None
    
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Preprocess image (Optional: Resize for uniformity, Denoise)
    gray = cv2.GaussianBlur(gray, (5, 5), 0)

    corners = cv2.goodFeaturesToTrack(gray, maxCorners=max_corners, qualityLevel=quality_level, minDistance=min_distance)
    
    if corners is None:
        print("No corners detected.")
        return None
    
    corners = np.int0(corners)

    return corners


fuzzy_extractor = FuzzyExtractor()

image_path = "fingerprint_sample.jpg"

corners = shi_tomasi_feature_extraction(image_path)

if corners is not None:
    minutiae_points_bytes = corners.tobytes()
    
    hashed_data, helper_data = fuzzy_extractor.gen(minutiae_points_bytes)
    
    print(f"Generated cryptographic key: {hashed_data}")
    print(f"Helper data (salt): {helper_data}")
    
    regenerated_data = fuzzy_extractor.rep(minutiae_points_bytes, helper_data)
    
    print(f"Regenerated cryptographic key: {regenerated_data}")
    
    assert hashed_data == regenerated_data, "Biometric data does not match!"
    print("Biometric data matches! Cryptographic keys are consistent.")
else:
    print("Feature extraction failed. Cannot proceed with Fuzzy Extractor.")
