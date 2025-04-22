// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract DecentralizedIdentity {
    struct Credential {
        string did;
        string claim;
        string caSignature;
        bool revoked;
    }
    
    mapping(string => Credential) public credentials;
    
    event CredentialIssued(string did, string claim);
    event CredentialRevoked(string did);
    
    // Issue a credential (access control to be added in production)
    function issueCredential(string memory did, string memory claim, string memory caSignature) public {
        Credential memory cred = Credential({
            did: did,
            claim: claim,
            caSignature: caSignature,
            revoked: false
        });
        credentials[did] = cred;
        emit CredentialIssued(did, claim);
    }
    
    // Verify if a credential exists and is not revoked
    function verifyCredential(string memory did) public view returns (bool) {
        Credential memory cred = credentials[did];
        return (!cred.revoked && bytes(cred.did).length > 0);
    }
    
    // Revoke a credential (only authorized entities should perform this)
    function revokeCredential(string memory did) public {
        require(bytes(credentials[did].did).length > 0, "Credential does not exist");
        credentials[did].revoked = true;
        emit CredentialRevoked(did);
    }
}
