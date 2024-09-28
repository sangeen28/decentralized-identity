import json
from web3 import Web3

w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:8545'))
contract_abi = '[...]'  # Replace with actual contract ABI
contract_address = '0xYourContractAddress'  # Replace with actual contract address
contract = w3.eth.contract(address=contract_address, abi=contract_abi)

def store_data_on_blockchain(did, credential):
    """
    Store the issued credential on the blockchain using a smart contract.
    """
    txn = contract.functions.storeCredential(did, json.dumps(credential)).buildTransaction({
        'from': w3.eth.accounts[0],  # Use the first account from Ganache
        'gas': 2000000,
        'gasPrice': w3.toWei('50', 'gwei'),
        'nonce': w3.eth.getTransactionCount(w3.eth.accounts[0]),
    })

    signed_txn = w3.eth.account.signTransaction(txn, private_key="0xYourPrivateKey")
    txn_hash = w3.eth.sendRawTransaction(signed_txn.rawTransaction)
    receipt = w3.eth.waitForTransactionReceipt(txn_hash)
    return receipt


def verify_data_on_blockchain(did):
    """
    Retrieve and verify the credential from the blockchain.
    """
    try:
        stored_credential = contract.functions.getCredential(did).call()
        if stored_credential:
            return json.loads(stored_credential)
        return None
    except Exception as e:
        print(f"Error verifying credential on blockchain: {e}")
        return None


def issue_credential(did, cryptographic_key):
    """
    Issue the credential by storing the DID and cryptographic key on the blockchain.
    """
    credential = {
        "did": did,
        "cryptographic_key": cryptographic_key
    }
    store_data_on_blockchain(did, credential)
    return credential


def verify_credential(did, provided_key):
    """
    Verify the provided key against the stored credential.
    """
    stored_credential = verify_data_on_blockchain(did)
    if stored_credential:
        stored_key = stored_credential["cryptographic_key"]
        return stored_key == provided_key
    return False


if __name__ == "__main__":
    # DID and cryptographic key from the Fuzzy Extractor (Simulated values)
    did = "did:example:123456789abcdef"
    cryptographic_key = "1234567890abcdef"  # Example key; should be the result of Fuzzy Extractor
    
    issued_credential = issue_credential(did, cryptographic_key)
    print(f"Credential issued and stored: {issued_credential}")

    provided_key = "1234567890abcdef"  # Example key; should be the result of Fuzzy Extractor
    verification_status = verify_credential(did, provided_key)
    print(f"Verification Status: {verification_status}")
