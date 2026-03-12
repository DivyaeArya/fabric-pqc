"""
Holder Wallet — Configuration
"""

import os


class Config:
    """Application configuration loaded from environment variables."""

    # Flask
    DEBUG = os.getenv("FLASK_DEBUG", "1") == "1"
    PORT = int(os.getenv("HOLDER_PORT", 5002))

    # Local credential storage
    STORAGE_PATH = os.getenv("HOLDER_STORAGE_PATH", "./storage")
