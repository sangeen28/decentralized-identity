import logging

# Set up logging
logging.basicConfig(level=logging.INFO)

def main():
    try:
        logging.info("Starting Shi-Tomasi feature extraction...")
        shi_tomasi = ShiTomasi()  # Ensure the class is correctly named
        corners = shi_tomasi.shi_tomasi_feature_extraction("fingerprint_sample.jpg")

        if corners is None:
            logging.error("Failed to extract features from fingerprint image.")
            return

        logging.info(f"Extracted {len(corners)} feature points.")

        logging.info("Generating cryptographic key from biometric data...")
        fuzzy_extractor = FuzzyExtractor()
        biometric_key, helper_data = fuzzy_extractor.gen(corners.tobytes())

        logging.info(f"Generated Cryptographic Key: {biometric_key.hex()}")

        logging.info("Creating user DID and issuing credential...")
        did_manager = DIDManager()
        logging.info(f"User DID: {did_manager.did}")

        user_data = {
            "name": "Alice",
            "age": 25,
            "biometric_key": biometric_key.hex()  # Ensure key is in hex format
        }

        credential = did_manager.issue_credential(user_data)
        logging.info(f"Credential issued: {credential}")

        logging.info("Storing credential on the blockchain...")
        receipt = did_manager.store_credential_on_blockchain(credential)
        logging.info(f"Credential stored on blockchain. Transaction receipt: {receipt}")

        logging.info("Verifying credential...")
        verification_status = did_manager.verify_credential(credential, biometric_key.hex())

        if verification_status:
            logging.info("Credential verification succeeded!")
        else:
            logging.error("Credential verification failed.")

    except Exception as e:
        logging.error(f"An error occurred: {e}", exc_info=True)


if __name__ == "__main__":
    main()
