# Decentralized Identity System

This repository implements a decentralized biometric identity system that integrates:
- **Biometric Processing:** Fingerprint acquisition, image enhancement, and minutiae extraction.
- **Fuzzy Extractor:** Generating a stable cryptographic key from biometric data.
- **Cryptography & CA:** Generating digital signatures (using ECDSA) and issuing a Decentralized Identifier (DID) with Certificate Authority (CA) involvement.
- **Blockchain Integration:** Smart contract to manage verifiable credentials, DID issuance, and credential revocation.

## Prerequisites

- Python 3.9+
- Node.js and npm (for Solidity development and deployment)
- Ganache (or a local Ethereum test network)

## Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/decentralized-identity.git
   cd decentralized-identity-system
