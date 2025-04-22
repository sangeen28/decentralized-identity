import os
from biometric.preprocess import preprocess_fingerprint
from biometric.minutiae import extract_minutiae
from biometric.fuzzy_extractor import fuzzy_extractor
from crypto.ca import generate_ca_keys, ca_sign_data, generate_did
from crypto.user_signature import generate_user_keys, user_sign_message, verify_user_signature

def enroll_user(image_path: str, claim: str):
    # Step 1: Fingerprint preprocessing
    processed_img = preprocess_fingerprint(image_path)
    
    # Optionally save the processed image for inspection
    processed_path = "processed_fingerprint.jpg"
    from cv2 import imwrite
    imwrite(processed_path, processed_img)
    print("Processed image saved as", processed_path)
    
    # Step 2: Minutiae extraction
    minutiae = extract_minutiae(processed_img)
    print(f"Extracted {len(minutiae)} minutiae points.")
    
    # Step 3: Fuzzy extractor to generate cryptographic key
    crypto_key, helper_data = fuzzy_extractor(minutiae)
    print("Generated cryptographic key:", crypto_key)
    
    # Step 4: CA involvement – sign biometric data and generate DID
    ca_sk, ca_vk = generate_ca_keys()  # In production, CA keys are securely stored
    biometric_data_string = helper_data  # using helper_data as a proxy for biometric features
    ca_signature = ca_sign_data(ca_sk, biometric_data_string, crypto_key)
    did = generate_did(biometric_data_string, crypto_key, ca_signature)
    print("Generated DID:", did)
    
    # Step 5: User signs a message for authentication
    user_sk, user_vk = generate_user_keys(crypto_key)
    nonce = "unique_nonce_example"  # In practice, generate a dynamic nonce
    user_signature = user_sign_message(user_sk, did, nonce)
    valid = verify_user_signature(user_vk, did, nonce, user_signature)
    print("User signature verification:", valid)
    
    # Step 6: (Optional) Integrate with blockchain – issue credential, etc.
    # This step would call functions in blockchain/web3_interaction.py
    
    return {
        "did": did,
        "crypto_key": crypto_key,
        "ca_signature": ca_signature,
        "user_signature": user_signature,
        "claim": claim
    }

if __name__ == "__main__":
    # Make sure you have a fingerprint image (e.g., 'fingerprint_sample.jpg') in the same folder or provide the path.
    image_file = "fingerprint_sample.jpg"
    if not os.path.exists(image_file):
        print(f"Fingerprint image '{image_file}' not found. Please add the sample image.")
    else:
        identity_data = enroll_user(image_file, "Name: Alice, Age: 30")
        print("Enrollment complete. Identity data:")
        for key, value in identity_data.items():
            print(f"{key}: {value}")
