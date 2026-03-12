"""
Issuer Service — Dilithium Signer
Delegates to the shared common.pqc_crypto module.
"""

import sys
import os
import logging

# Ensure common/ is importable
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from common.pqc_crypto import DilithiumCrypto, DilithiumKeyPair  # noqa: E402

logger = logging.getLogger(__name__)


class DilithiumSigner:
    """Issues Dilithium signatures using the shared crypto module."""

    def __init__(self, variant: str | None = None):
        self.crypto = DilithiumCrypto(variant=variant or "Dilithium3")
        self._keys: DilithiumKeyPair = self.crypto.generate_keys()
        logger.info("DilithiumSigner ready (variant=%s)", self.crypto.variant)

    def sign(self, message: bytes) -> str:
        """Sign raw bytes and return a base64-encoded signature."""
        return self.crypto.sign_data(self._keys.private_key, message)

    def get_public_key_b64(self) -> str:
        """Return the base64-encoded public key."""
        return self._keys.public_key_b64

    def get_issuer_did(self) -> str:
        """Derive a did:key identifier from the public key."""
        pk_short = self._keys.public_key_b64[:32]
        return f"did:key:z{pk_short}"
