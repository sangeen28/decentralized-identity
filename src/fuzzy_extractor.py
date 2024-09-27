import hashlib
import random

class FuzzyExtractor:
    def __init__(self, tolerance=10):
        self.tolerance = tolerance
    
    def gen(self, biometric_data):
        # Generate a random salt
        salt = random.getrandbits(128)
        
        # Hash the biometric data with the salt
        hashed_data = hashlib.sha256(biometric_data + salt.to_bytes(16, 'big')).hexdigest()
        
        # Generate helper data
        helper_data = salt
        
        return hashed_data, helper_data
    
    def rep(self, biometric_data, helper_data):
        # Regenerate the hash using the biometric data and helper data (salt)
        hashed_data = hashlib.sha256(biometric_data + helper_data.to_bytes(16, 'big')).hexdigest()
        
        return hashed_data

fuzzy_extractor = FuzzyExtractor()

hashed_data, helper_data = fuzzy_extractor.gen(minutiae_points.tobytes())

regenerated_data = fuzzy_extractor.rep(minutiae_points.tobytes(), helper_data)

assert hashed_data == regenerated_data, "Biometric data does not match!"

