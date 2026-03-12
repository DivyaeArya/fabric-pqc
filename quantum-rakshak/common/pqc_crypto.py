"""
Quantum Rakshak — Post-Quantum Cryptography Module
====================================================

Implements CRYSTALS-Dilithium digital signatures using the Open Quantum Safe
(OQS) liboqs-python library.

Classes:
    DilithiumCrypto — key generation, signing, and verification.

Standalone usage:
    python -m common.pqc_crypto
"""

from __future__ import annotations

import base64
import hashlib
import json
import logging
from dataclasses import dataclass
from typing import Any

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# OQS availability check
# ---------------------------------------------------------------------------
try:
    import oqs                          # type: ignore[import-untyped]
    OQS_AVAILABLE = True
except ImportError:
    OQS_AVAILABLE = False
    logger.warning(
        "liboqs-python is not installed — DilithiumCrypto will run in MOCK mode. "
        "Install with:  pip install liboqs-python"
    )

# ---------------------------------------------------------------------------
# Supported algorithm variants
# ---------------------------------------------------------------------------
SUPPORTED_VARIANTS = ("Dilithium2", "Dilithium3", "Dilithium5")
DEFAULT_VARIANT = "Dilithium3"


# ---------------------------------------------------------------------------
# Key-pair container
# ---------------------------------------------------------------------------
@dataclass(frozen=True)
class DilithiumKeyPair:
    """Immutable container for a Dilithium key-pair."""

    public_key: bytes
    private_key: bytes
    variant: str

    # -- convenience helpers ------------------------------------------------

    @property
    def public_key_b64(self) -> str:
        """Base64-encoded public key."""
        return base64.b64encode(self.public_key).decode()

    @property
    def private_key_b64(self) -> str:
        """Base64-encoded private (secret) key."""
        return base64.b64encode(self.private_key).decode()

    def __repr__(self) -> str:
        pk_preview = self.public_key_b64[:24] + "…"
        return (
            f"DilithiumKeyPair(variant={self.variant!r}, "
            f"pub={pk_preview}, pub_len={len(self.public_key)}, "
            f"sec_len={len(self.private_key)})"
        )


# ---------------------------------------------------------------------------
# Core crypto class
# ---------------------------------------------------------------------------
class DilithiumCrypto:
    """
    Post-quantum digital-signature operations using CRYSTALS-Dilithium.

    All data is **SHA-256 hashed** before signing so that the actual
    Dilithium sign / verify calls always operate on a fixed-size 32-byte
    digest, regardless of the original payload size.

    Parameters
    ----------
    variant : str, optional
        Dilithium security level — one of ``Dilithium2``, ``Dilithium3``
        (default), or ``Dilithium5``.

    Example
    -------
    >>> crypto = DilithiumCrypto()
    >>> keys  = crypto.generate_keys()
    >>> sig   = crypto.sign_data(keys.private_key, {"name": "Alice"})
    >>> valid = crypto.verify_signature(keys.public_key, {"name": "Alice"}, sig)
    >>> assert valid is True
    """

    def __init__(self, variant: str = DEFAULT_VARIANT) -> None:
        if variant not in SUPPORTED_VARIANTS:
            raise ValueError(
                f"Unsupported variant {variant!r}. "
                f"Choose from {SUPPORTED_VARIANTS}"
            )
        self.variant = variant
        self._mock = not OQS_AVAILABLE

        mode = "LIVE (liboqs)" if not self._mock else "MOCK"
        logger.info("DilithiumCrypto initialised — variant=%s  mode=%s", variant, mode)

    # ------------------------------------------------------------------
    # Key generation
    # ------------------------------------------------------------------
    def generate_keys(self) -> DilithiumKeyPair:
        """
        Generate a fresh Dilithium key-pair.

        Returns
        -------
        DilithiumKeyPair
            An immutable container with ``public_key`` and ``private_key``
            as raw ``bytes``, plus convenience ``*_b64`` properties.
        """
        if not self._mock:
            signer = oqs.Signature(self.variant)
            public_key = signer.generate_keypair()
            private_key = signer.export_secret_key()
            logger.info(
                "Generated Dilithium key-pair — pub=%d bytes, sec=%d bytes",
                len(public_key),
                len(private_key),
            )
        else:
            # Deterministic mock keys for reproducible dev / testing
            public_key = hashlib.sha256(b"mock-public-key").digest()
            private_key = hashlib.sha256(b"mock-private-key").digest()
            logger.info("Generated MOCK Dilithium key-pair")

        return DilithiumKeyPair(
            public_key=public_key,
            private_key=private_key,
            variant=self.variant,
        )

    # ------------------------------------------------------------------
    # Signing
    # ------------------------------------------------------------------
    def sign_data(
        self,
        private_key: bytes,
        data: dict[str, Any] | str | bytes,
    ) -> str:
        """
        Sign arbitrary data with a Dilithium private key.

        The data is canonicalised (sorted-key JSON), SHA-256 hashed, and
        then signed.

        Parameters
        ----------
        private_key : bytes
            The raw private (secret) key.
        data : dict | str | bytes
            The payload to sign.  Dicts are serialised to canonical JSON
            automatically.

        Returns
        -------
        str
            Base64-encoded signature.
        """
        digest = self._prepare_digest(data)

        if not self._mock:
            signer = oqs.Signature(self.variant, private_key)
            signature = signer.sign(digest)
            logger.debug("Signed digest (%s) — sig=%d bytes", digest.hex()[:16], len(signature))
        else:
            signature = self._mock_sign(digest, private_key)
            logger.debug("MOCK-signed digest (%s)", digest.hex()[:16])

        return base64.b64encode(signature).decode()

    # ------------------------------------------------------------------
    # Verification
    # ------------------------------------------------------------------
    def verify_signature(
        self,
        public_key: bytes,
        data: dict[str, Any] | str | bytes,
        signature: str,
    ) -> bool:
        """
        Verify a Dilithium signature.

        Parameters
        ----------
        public_key : bytes
            The raw public key of the signer.
        data : dict | str | bytes
            The original payload that was signed.
        signature : str
            Base64-encoded signature string.

        Returns
        -------
        bool
            ``True`` if the signature is valid, ``False`` otherwise.
        """
        digest = self._prepare_digest(data)
        sig_bytes = base64.b64decode(signature)

        if not self._mock:
            try:
                verifier = oqs.Signature(self.variant)
                is_valid = verifier.verify(digest, sig_bytes, public_key)
                logger.debug("Signature valid: %s", is_valid)
                return bool(is_valid)
            except Exception as exc:
                logger.error("Verification failed with exception: %s", exc)
                return False
        else:
            expected = self._mock_sign(digest, b"")  # mock ignores key
            is_valid = sig_bytes == expected
            logger.debug("MOCK verification result: %s", is_valid)
            return is_valid

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------
    @staticmethod
    def _canonicalise(data: dict[str, Any] | str | bytes) -> bytes:
        """Convert data to a deterministic byte representation."""
        if isinstance(data, bytes):
            return data
        if isinstance(data, dict):
            return json.dumps(data, sort_keys=True, separators=(",", ":")).encode()
        return str(data).encode()

    @classmethod
    def _prepare_digest(cls, data: dict[str, Any] | str | bytes) -> bytes:
        """Canonicalise → SHA-256 hash."""
        canonical = cls._canonicalise(data)
        return hashlib.sha256(canonical).digest()

    @staticmethod
    def _mock_sign(digest: bytes, _private_key: bytes) -> bytes:
        """Deterministic mock signature (HMAC-like) for dev without liboqs."""
        return hashlib.sha512(digest + b"mock-dilithium-secret").digest()


# ---------------------------------------------------------------------------
# Example / self-test
# ---------------------------------------------------------------------------
def _example() -> None:
    """Run a quick round-trip demo of key-gen → sign → verify."""
    print("=" * 64)
    print("  Quantum Rakshak — Dilithium Signature Demo")
    print("=" * 64)

    crypto = DilithiumCrypto(variant="Dilithium3")
    mode = "MOCK" if crypto._mock else "LIVE (liboqs)"
    print(f"\n  Mode     : {mode}")
    print(f"  Variant  : {crypto.variant}\n")

    # 1. Generate keys
    keys = crypto.generate_keys()
    print(f"  Public key  : {keys.public_key_b64[:48]}…  ({len(keys.public_key)} bytes)")
    print(f"  Private key : {keys.private_key_b64[:48]}…  ({len(keys.private_key)} bytes)\n")

    # 2. Sign a credential
    credential = {
        "type": "VerifiableCredential",
        "issuer": "did:key:zExampleIssuer",
        "credentialSubject": {
            "id": "did:key:zExampleHolder",
            "name": "Alice",
            "degree": "MSc Quantum Computing",
        },
    }
    signature = crypto.sign_data(keys.private_key, credential)
    print(f"  Signature   : {signature[:48]}…\n")

    # 3. Verify — should be True
    valid = crypto.verify_signature(keys.public_key, credential, signature)
    print(f"  ✔ Verification (correct data)  : {valid}")

    # 4. Tamper — should be False
    tampered = {**credential, "credentialSubject": {**credential["credentialSubject"], "name": "Eve"}}
    invalid = crypto.verify_signature(keys.public_key, tampered, signature)
    print(f"  ✘ Verification (tampered data) : {invalid}")

    print("\n" + "=" * 64)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    _example()
