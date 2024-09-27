from web3 import Web3
import json

# Connect to a local Ethereum node
web3 = Web3(Web3.HTTPProvider('http://127.0.0.1:8545'))

with open('contract_details.json') as f:
    contract_details = json.load(f)

contract_abi = contract_details['abi']
contract_address = contract_details['address']

contract = web3.eth.contract(address=contract_address, abi=contract_abi)

def store_data_on_blockchain(did, data):
    data_json = json.dumps(data)
    tx_hash = contract.functions.storeCredential(did, data_json).transact({'from': web3.eth.accounts[0]})
    web3.eth.waitForTransactionReceipt(tx_hash)

def verify_data_on_blockchain(did):
    stored_data = contract.functions.getCredential(did).call()
    return json.loads(stored_data) if stored_data else None
