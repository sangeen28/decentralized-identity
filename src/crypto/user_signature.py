from ecdsa import SigningKey, SECP256k1

def generate_user_keys(seed: str):
    """
    Generate a user's ECDSA key pair from a hex seed.
    This is a deterministic approach for demonstration purposes.
    """
    seed_bytes = bytes.fromhex(seed)[:32]  # ensure exactly 32 bytes for SECP256k1
    user_sk = SigningKey.from_string(seed_bytes, curve=SECP256k1)
    user_vk = user_sk.get_verifying_key()
    return user_sk, user_vk

def user_sign_message(user_sk, did: str, nonce: str) -> str:
    """
    Sign a message that is the concatenation of the DID and a nonce to prevent replay attacks.
    """
    message = (did + nonce).encode('utf-8')
    signature = user_sk.sign(message)
    return signature.hex()

def verify_user_signature(user_vk, did: str, nonce: str, signature_hex: str) -> bool:
    """
    Verify the user's signature.
    """
    message = (did + nonce).encode('utf-8')
    try:
        valid = user_vk.verify(bytes.fromhex(signature_hex), message)
        return valid
    except Exception:
        return False
