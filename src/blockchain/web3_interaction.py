from web3 import Web3

# Example configuration for a local Ganache instance
ganache_url = "http://127.0.0.1:7545"
web3 = Web3(Web3.HTTPProvider(ganache_url))
if not web3.isConnected():
    raise ConnectionError("Web3 is not connected to Ganache")

def load_contract(abi, bytecode, account, private_key):
    """
    Deploy the smart contract using Web3.py.
    """
    Contract = web3.eth.contract(abi=abi, bytecode=bytecode)
    tx_dict = Contract.constructor().buildTransaction({
        'from': account,
        'nonce': web3.eth.get_transaction_count(account),
        'gas': 3000000,
        'gasPrice': web3.toWei('20', 'gwei')
    })
    signed_txn = web3.eth.account.sign_transaction(tx_dict, private_key=private_key)
    tx_hash = web3.eth.send_raw_transaction(signed_txn.rawTransaction)
    tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
    return web3.eth.contract(address=tx_receipt.contractAddress, abi=abi)
