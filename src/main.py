if __name__ == "__main__":


  
    Shi_tomasi = ShiTomasi()
    corners = shi_Tomasi.shi_tomasi_feature_extraction()

    fuzzy_extractor = FuzzyExtractor()
    biometric_key = fuzzy_extractor.generate_key(corners)
    print("Generated Cryptographic Key from Fingerprint:", biometric_key.hex())

    did_manager = DIDManager()
    print(f"User DID: {did_manager.did}")

    user_data = {"name": "Alice", "age": 25, "biometric_key": biometric_key.hex()}
    credential = did_manager.issue_credential(user_data)
    print("Credential issued:", credential)

    receipt = did_manager.store_credential_on_blockchain(credential)
    print("Credential stored on blockchain with transaction receipt:", receipt)

    verification_status = did_manager.verify_credential(credential)
    print("Credential verification status:", verification_status)
