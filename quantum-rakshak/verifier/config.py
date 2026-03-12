"""
Verifier Service — Configuration
"""

import os


class Config:
    """Application configuration loaded from environment variables."""

    # Flask
    DEBUG = os.getenv("FLASK_DEBUG", "1") == "1"
    PORT = int(os.getenv("VERIFIER_PORT", 5003))

    # Dilithium
    DILITHIUM_VARIANT = os.getenv("DILITHIUM_VARIANT", "Dilithium3")

    # Hyperledger Fabric
    FABRIC_PEER_ADDRESS = os.getenv("FABRIC_PEER_ADDRESS", "localhost:7051")
    FABRIC_CHANNEL_NAME = os.getenv("FABRIC_CHANNEL_NAME", "rakshakchannel")
    FABRIC_CHAINCODE_NAME = os.getenv("FABRIC_CHAINCODE_NAME", "credential_registry")
    FABRIC_MSP_ID = os.getenv("FABRIC_MSP_ID", "Org1MSP")
    FABRIC_WALLET_PATH = os.getenv("FABRIC_WALLET_PATH", "./wallet")
    FABRIC_CONNECTION_PROFILE = os.getenv("FABRIC_CONNECTION_PROFILE", "./network/connection.json")
