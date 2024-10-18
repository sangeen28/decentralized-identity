import cv2
import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf  # For loading the CNN model

# Load the pre-trained DnCNN model for denoising
dncnn_model = tf.keras.models.load_model('path_to_dncnn_model.h5')

def preprocess_image_with_cnn(image):
    image_normalized = image.astype('float32') / 255.0
    image_reshaped = np.expand_dims(image_normalized, axis=0)  # Add batch dimension
    
    denoised_image = dncnn_model.predict(image_reshaped)
    
    denoised_image = np.squeeze(denoised_image) * 255.0
    return denoised_image.astype('uint8')

def shi_tomasi_feature_extraction(image_path, max_corners=100, quality_level=0.01, min_distance=10):
    # Load the input image in color
    img = cv2.imread(image_path)
    
    if img is None:
        print("Error: Image not found or unable to load.")
        return None
    
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    denoised_gray = preprocess_image_with_cnn(gray)

    corners = cv2.goodFeaturesToTrack(denoised_gray, maxCorners=max_corners, qualityLevel=quality_level, minDistance=min_distance)
    
    if corners is None:
        print("No corners detected.")
        return None
    
    corners = np.int0(corners)

    # Draw the detected corners on the original image
    for i in corners:
        x, y = i.ravel()
        cv2.circle(img, (x, y), 5, (0, 255, 0), -1)

    plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    plt.title("Shi-Tomasi Corner Detection with CNN Preprocessing")
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
