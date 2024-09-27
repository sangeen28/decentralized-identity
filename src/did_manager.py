from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric.utils import Prehashed
from web3 import Web3

w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:8545'))

contract_abi = '[...]'
contract_address = '0xYourContractAddress'

contract = w3.eth.contract(address=contract_address, abi=contract_abi)

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
        credential = {
            "id": self.did,
            "data": user_data
        }
        signature = self.sign_data(credential)
        credential['signature'] = signature
        return credential

    def sign_data(self, data):
        message = str(data).encode()
        signature = self.private_key.sign(
            message,
            ec.ECDSA(Prehashed(hashes.SHA256()))
        )
        return signature.hex()

    def store_credential_on_blockchain(self, credential):
        txn = contract.functions.storeCredential(self.did, credential['data'], credential['signature']).buildTransaction({
            'from': w3.eth.accounts[0],  # Use the first account from Ganache
            'gas': 2000000,
            'gasPrice': w3.toWei('50', 'gwei'),
            'nonce': w3.eth.getTransactionCount(w3.eth.accounts[0]),
        })

        signed_txn = w3.eth.account.signTransaction(txn, private_key="0xYourPrivateKey")
        txn_hash = w3.eth.sendRawTransaction(signed_txn.rawTransaction)
        receipt = w3.eth.waitForTransactionReceipt(txn_hash)
        return receipt

    def verify_credential(self, credential):
        public_key = self.public_key
        signature = bytes.fromhex(credential['signature'])
        data = str(credential['data']).encode()

        # Verify the signature
        try:
            public_key.verify(signature, data, ec.ECDSA(Prehashed(hashes.SHA256())))
            return True
        except Exception as e:
            return False

# Example Usage
if __name__ == "__main__":
    manager = DIDManager()

    print(f"User DID: {manager.did}")

    user_data = {"name": "Alice", "age": 25}
    credential = manager.issue_credential(user_data)
    print("Credential issued:", credential)

    receipt = manager.store_credential_on_blockchain(credential)
    print("Credential stored on blockchain with transaction receipt:", receipt)

    verification_status = manager.verify_credential(credential)
    print("Credential verification status:", verification_status)

