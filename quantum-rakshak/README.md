# Quantum Rakshak

**Post-Quantum Secure Self-Sovereign Identity System**

Quantum Rakshak is a prototype system that implements Self-Sovereign Identity (SSI) and Verifiable Credentials secured by post-quantum digital signatures (CRYSTALS-Dilithium) with a credential registry on Hyperledger Fabric.

---

## Architecture Overview

```
┌───────────────┐      ┌───────────────┐      ┌───────────────┐
│               │      │               │      │               │
│    Issuer     │─────▶│    Holder     │─────▶│   Verifier    │
│   Service     │      │    Wallet     │      │   Service     │
│  (port 5001)  │      │  (port 5002)  │      │  (port 5003)  │
│               │      │               │      │               │
└───────┬───────┘      └───────────────┘      └───────┬───────┘
        │                                             │
        │         ┌───────────────────────┐           │
        └────────▶│  Hyperledger Fabric   │◀──────────┘
                  │  Credential Registry  │
                  └───────────────────────┘
```

### Components

| Service | Description | Port |
|---------|-------------|------|
| **Issuer** | Issues and signs credentials using Dilithium; registers metadata on Fabric | `5001` |
| **Holder** | Stores credentials locally; presents them to verifiers | `5002` |
| **Verifier** | Verifies Dilithium signatures; checks revocation status on Fabric | `5003` |
| **Blockchain** | Hyperledger Fabric network running credential-registry chaincode | — |

### Technology Stack

- **Language:** Python 3.10+
- **Framework:** Flask
- **PQC Library:** liboqs-python (CRYSTALS-Dilithium)
- **Blockchain:** Hyperledger Fabric 2.x
- **Chaincode:** Go
- **Containers:** Docker & Docker Compose

---

## Quick Start

### 1. Clone & configure

```bash
cp .env.example .env
# Edit .env with your Fabric network settings
```

### 2. Run with Docker Compose

```bash
docker compose up --build
```

### 3. Test the services

```bash
# Issue a credential
curl -X POST http://localhost:5001/credentials/issue \
  -H "Content-Type: application/json" \
  -d '{"holder_did": "did:key:example", "claims": {"name": "Alice", "degree": "MSc"}}'

# Store credential in holder wallet
curl -X POST http://localhost:5002/wallet/store \
  -H "Content-Type: application/json" \
  -d '{"credential": { ... }}'

# Verify a credential
curl -X POST http://localhost:5003/credentials/verify \
  -H "Content-Type: application/json" \
  -d '{"credential": { ... }}'
```

---

## Project Structure

```
quantum-rakshak/
├── issuer/          # Issuer Service
├── holder/          # Holder Wallet
├── verifier/        # Verifier Service
├── blockchain/      # Fabric network & chaincode
├── common/          # Shared utilities & schemas
├── tests/           # Test suite
├── docker-compose.yml
├── .env.example
└── README.md
```

---

## Running Tests

```bash
pip install -r issuer/requirements.txt
pip install -r holder/requirements.txt
pip install -r verifier/requirements.txt
pip install pytest

python -m pytest tests/ -v
```

---

## License

This project is a research prototype developed for academic purposes.
