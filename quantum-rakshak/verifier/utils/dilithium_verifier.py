"""
Verifier Service — Dilithium Verifier
Delegates to the shared common.pqc_crypto module.
"""

import sys
import os
import base64
import logging

# Ensure common/ is importable
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from common.pqc_crypto import DilithiumCrypto  # noqa: E402

logger = logging.getLogger(__name__)


class DilithiumVerifier:
    """Verifies Dilithium signatures using the shared crypto module."""

    def __init__(self, variant: str | None = None):
        self.crypto = DilithiumCrypto(variant=variant or "Dilithium3")
        logger.info("DilithiumVerifier ready (variant=%s)", self.crypto.variant)

    def verify(self, message: bytes, signature_b64: str, public_key_b64: str) -> bool:
        """
        Verify a Dilithium signature.

        Args:
            message:        Raw message bytes.
            signature_b64:  Base64-encoded signature.
            public_key_b64: Base64-encoded public key.

        Returns:
            True if valid, False otherwise.
        """
        public_key = base64.b64decode(public_key_b64)
        return self.crypto.verify_signature(public_key, message, signature_b64)
