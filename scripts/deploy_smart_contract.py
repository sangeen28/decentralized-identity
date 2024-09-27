from web3 import Web3
from solcx import compile_source
import json

web3 = Web3(Web3.HTTPProvider('http://127.0.0.1:8545'))

contract_source_code = '''
pragma solidity ^0.8.0;

contract CredentialManager {
    struct Credential {
        string digitalIdentifier;
        string cryptographicKey;
    }

    mapping(string => Credential) private credentials;

    function storeCredential(string memory digitalIdentifier, string memory credentialData) public {
        credentials[digitalIdentifier] = Credential(digitalIdentifier, credentialData);
    }

    function getCredential(string memory digitalIdentifier) public view returns (string memory) {
        return credentials[digitalIdentifier].cryptographicKey;
    }
}
'''

compiled_sol = compile_source(contract_source_code)
contract_interface = compiled_sol['<stdin>:CredentialManager']

CredentialManager = web3.eth.contract(abi=contract_interface['abi'], bytecode=contract_interface['bin'])
tx_hash = CredentialManager.constructor().transact({'from': web3.eth.accounts[0]})
tx_receipt = web3.eth.waitForTransactionReceipt(tx_hash)
contract_address = tx_receipt.contractAddress

with open('contract_details.json', 'w') as f:
    json.dump({
        'abi': contract_interface['abi'],
        'address': contract_address
    }, f)

print(f'Contract deployed at address: {contract_address}')
