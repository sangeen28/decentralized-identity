# Decentralized Identity Management System

## Overview
This project implements a decentralized identity management system, leveraging biometric fingerprint data for secure identification. The key components used in this system include:

- **Shi-Tomasi Corner Detection**: For biometric fingerprint feature extraction.
- **Fuzzy Extractor**: To generate cryptographic keys from the biometric data, ensuring secure and unique user identification.
- **DID (Decentralized Identifier) Manager**: For creating and managing Decentralized Identifiers (DIDs) that facilitate decentralized identity management.
- **Solidity Smart Contract**: To securely store user credentials on the blockchain, ensuring tamper-proof and decentralized storage.
- **Python Integration**: To connect all the components and interact with the Ethereum blockchain effectively.

## Prerequisites

Before you begin, ensure the following software and libraries are installed on your machine:

- **Python 3.x**: For integrating the components and scripting interactions with the blockchain.
- **Solidity Compiler (solc)**: To compile the Solidity smart contracts.
- **Ganache** (or any other local Ethereum blockchain): For setting up a local Ethereum development environment.
- **Node.js**: If you choose to use **Truffle** for managing and deploying smart contracts.
- **Web3.py**: A Python library for interacting with the Ethereum blockchain.
- **OpenCV**: To implement Shi-Tomasi corner detection for fingerprint feature extraction.
- **Cryptography Library**: For generating cryptographic keys from biometric data.

## Installation & Setup

1. **Python & Virtual Environment**:  
   It's recommended to use a virtual environment to manage dependencies. Install Python and set up a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
