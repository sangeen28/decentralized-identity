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
