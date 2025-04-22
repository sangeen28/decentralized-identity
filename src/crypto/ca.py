import hashlib
from ecdsa import SigningKey, SECP256k1

def generate_ca_keys():
    """
    Generate a CA ECDSA key pair using SECP256k1 curve.
    """
    ca_sk = SigningKey.generate(curve=SECP256k1)
    ca_vk = ca_sk.get_verifying_key()
    return ca_sk, ca_vk

def ca_sign_data(ca_sk, biometric_data: str, crypto_key: str) -> str:
    """
    CA signs the concatenation of biometric data and the cryptographic key.
    """
    message = (biometric_data + crypto_key).encode('utf-8')
    signature = ca_sk.sign(message)
    return signature.hex()

def generate_did(biometric_data: str, crypto_key: str, ca_signature: str) -> str:
    """
    Generate a Decentralized Identifier (DID) by hashing the biometric data, crypto key, and CA signature.
    """
    did_data = (biometric_data + crypto_key + ca_signature).encode('utf-8')
    did = hashlib.sha256(did_data).hexdigest()
    return did
