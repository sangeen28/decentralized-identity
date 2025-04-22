import hashlib

def fuzzy_extractor(minutiae_points, salt: bytes = b'secure_salt'):
    """
    Simulate a fuzzy extractor by sorting minutiae data and hashing it with a salt
    to generate a stable cryptographic key.
    """
    # Sort minutiae to reduce ordering variability
    sorted_points = sorted(minutiae_points, key=lambda p: (p['x'], p['y']))
    
    # Create a string representation of minutiae points
    data_string = ''.join([f"{p['x']}-{p['y']}-{p['type']};" for p in sorted_points])
    
    # Generate key using SHA-256
    hasher = hashlib.sha256()
    hasher.update(data_string.encode('utf-8'))
    hasher.update(salt)
    key = hasher.hexdigest()
    
    # In this simple example, helper data is the serialized minutiae string
    helper_data = data_string
    return key, helper_data
