import hashlib
import random
import json
import numpy as np
import cv2
from web3 import Web3
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric.utils import Prehashed


web3 = Web3(Web3.HTTPProvider('http://127.0.0.1:8545'))

with open('contract_details.json') as f:
    contract_details = json.load(f)

contract_abi = contract_details['abi']
contract_address = contract_details['address']
contract = web3.eth.contract(address=contract_address, abi=contract_abi)


class FuzzyExtractor:
    def __init__(self, tolerance=10):
        self.tolerance = tolerance

    def gen(self, biometric_data):
        salt = random.getrandbits(128)
        hashed_data = hashlib.sha256(biometric_data + salt.to_bytes(16, 'big')).hexdigest()
        helper_data = salt
        return hashed_data, helper_data

    def rep(self, biometric_data, helper_data):
        hashed_data = hashlib.sha256(biometric_data + helper_data.to_bytes(16, 'big')).hexdigest()
        return hashed_data


class DIDManager:
    def __init__(self):
        self.private_key = ec.generate_private_key(ec.SECP256R1(), default_backend())
        self.public_key = self.private_key.public_key()
        self.did = self.create_did(self.public_key)

    def create_did(self, public_key):
        public_bytes = public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
        did = f"did:example:{public_bytes.hex()}"
        return did

    def issue_credential(self, user_data):
        credential = {"did": self.did, "data": user_data}
        signature = self.sign_data(credential)
        credential['signature'] = signature
        return credential

    def sign_data(self, data):
        message = str(data).encode()
        signature = self.private_key.sign(message, ec.ECDSA(Prehashed(hashes.SHA256())))
        return signature.hex()

    def verify_credential(self, credential, provided_key):
        public_key = self.public_key
        signature = bytes.fromhex(credential['signature'])
        data = str(credential['data']).encode()
        try:
            public_key.verify(signature, data, ec.ECDSA(Prehashed(hashes.SHA256())))
            return credential['data']['cryptographic_key'] == provided_key
        except Exception:
            return False


def store_data_on_blockchain(did, data):
    data_json = json.dumps(data)
    tx_hash = contract.functions.storeCredential(did, data_json).transact({'from': web3.eth.accounts[0]})
    web3.eth.waitForTransactionReceipt(tx_hash)


def verify_data_on_blockchain(did):
    stored_data = contract.functions.getCredential(did).call()
    return json.loads(stored_data) if stored_data else None


def shi_tomasi_feature_extraction(image_path, max_corners=100, quality_level=0.01, min_distance=10):
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
    return corners


if __name__ == "__main__":
    # 1. Perform Shi-Tomasi feature extraction from fingerprint image
    image_path = "fingerprint_sample.jpg"
    corners = shi_tomasi_feature_extraction(image_path)
    if corners is None:
        print("Failed to extract features")
        exit()

    minutiae_points_bytes = corners.tobytes()

    fuzzy_extractor = FuzzyExtractor()
    cryptographic_key, helper_data = fuzzy_extractor.gen(minutiae_points_bytes)
    print(f"Generated cryptographic key: {cryptographic_key}")

    manager = DIDManager()
    print(f"User DID: {manager.did}")

    user_data = {"name": "Alice", "age": 25, "cryptographic_key": cryptographic_key}
    credential = manager.issue_credential(user_data)
    print(f"Credential issued: {credential}")

    store_data_on_blockchain(manager.did, credential)
    print("Credential stored on blockchain.")

    stored_credential = verify_data_on_blockchain(manager.did)
    if stored_credential:
        print(f"Retrieved stored credential: {stored_credential}")
        verification_status = manager.verify_credential(stored_credential, cryptographic_key)
        print(f"Verification Status: {verification_status}")
    else:
        print("No credential found on the blockchain.")
