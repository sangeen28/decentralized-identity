import json
from blockchain import store_data_on_blockchain, verify_data_on_blockchain

def issue_credential(did, cryptographic_key):
    credential = {
        "did": did,
        "cryptographic_key": cryptographic_key.hex()
    }
    store_data_on_blockchain(did, credential)
    return credential

def verify_credential(did, provided_key):
    stored_credential = verify_data_on_blockchain(did)
    if stored_credential:
        return stored_credential["cryptographic_key"] == provided_key.hex()
    return False

