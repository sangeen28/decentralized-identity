import json
from web3 import Web3

# Load compiled contract ABI and bytecode (assumed to be in a JSON file)
with open('src/blockchain/DecentralizedIdentity.json') as f:
    contract_json = json.load(f)
abi = contract_json['abi']
bytecode = contract_json['bytecode']

# Connect to Ganache
ganache_url = "http://127.0.0.1:7545"
web3 = Web3(Web3.HTTPProvider(ganache_url))
account = web3.eth.accounts[0]
private_key = "YOUR_PRIVATE_KEY_HERE"  # replace with your Ganache account key

# Deploy the contract
Contract = web3.eth.contract(abi=abi, bytecode=bytecode)
tx = Contract.constructor().buildTransaction({
    'from': account,
    'nonce': web3.eth.get_transaction_count(account),
    'gas': 3000000,
    'gasPrice': web3.toWei('20', 'gwei')
})
signed_tx = web3.eth.account.sign_transaction(tx, private_key=private_key)
tx_hash = web3.eth.send_raw_transaction(signed_tx.rawTransaction)
receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
print("Contract deployed at address:", receipt.contractAddress)
