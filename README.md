# BlockVerify – Blockchain-powered Certificate Verification System

## Overview
BlockVerify is a decentralized application that leverages blockchain technology to provide a secure and tamper-proof certificate verification system. The project uses Ethereum smart contracts for certificate management, Streamlit for the frontend user interface, and Firebase for user authentication and data storage. It integrates IPFS for decentralized storage of certificate PDFs, ensuring immutability and trust.

## Features
- Institute users can generate and upload certificates to IPFS and record them on the blockchain.
- Verifiers can validate certificates by uploading PDFs, entering certificate IDs, or scanning QR codes.
- Secure login and registration system with Firebase authentication.
- Blockchain ensures immutability and trust in certificate verification.
- User-friendly Streamlit web interface with role-based access.
- QR code generation and decoding for easy certificate verification.

## Repository Structure
```
/ (root)
├── app.py                      # Main Streamlit app entry point
├── Dockerfile                  # Docker container configuration
├── README.md                   # Project overview and instructions
├── deployment_config.json      # Deployment configuration for contracts
├── truffle-config.js           # Truffle configuration for smart contract deployment
├── application/                # Backend and application logic
├── pages/                      # Streamlit multi-page app pages (login, verifier, institute, register)
├── utils/                      # Utility modules and helper functions (certificate utils, Streamlit UI helpers)
├── contracts/                  # Solidity smart contracts (Certification.sol)
├── migrations/                 # Truffle migration scripts
├── build/                     # Compiled contract artifacts (auto-generated)
├── db/                        # Database related files (e.g., Firebase integration)
├── assets/                    # Static assets like images and logos
├── test/                      # Test files (to be added)
```

## Technologies Used
- Ethereum blockchain and Solidity smart contracts
- Truffle framework for contract deployment
- Streamlit for frontend UI
- Firebase for authentication and user management
- IPFS (e.g., Pinata) for decentralized file storage
- Python libraries: web3.py, pdfplumber, reportlab, pyzbar

## Setup and Installation

### Prerequisites
- Python 3.8+
- Node.js and npm
- Truffle framework
- Ganache or other Ethereum node for local blockchain
- IPFS account (e.g., Pinata) for file storage
- Firebase project for authentication

### Backend Setup
1. Create and activate a Python virtual environment:
   ```bash
   python3 -m venv venv38
   source venv38/bin/activate
   ```
2. Install Python dependencies:
   ```bash
   pip install -r application/requirements.txt
   ```
3. Configure environment variables in `.env` file (API keys, Firebase config, etc.).

### Smart Contract Deployment
1. Start your local Ethereum node (e.g., Ganache).
2. Compile and deploy contracts using Truffle:
   ```bash
   truffle compile
   truffle migrate --reset
   ```

### Running the Streamlit App
1. Run the Streamlit app:
   ```bash
   streamlit run app.py --server.port 8504
   ```
2. Access the app in your browser at `http://localhost:8504`.

## Usage
- Select your role (Institute or Verifier) on the landing page.
- Institutes can generate certificates, which are saved as PDFs, uploaded to IPFS, and recorded on the blockchain.
- Verifiers can upload certificate PDFs, enter certificate IDs, or scan QR codes to verify authenticity.

## Contributing
Contributions are welcome! Please fork the repository and submit pull requests.

## License
This project is licensed under the MIT License.

## Contact
For questions or support, please contact the project maintainer.
