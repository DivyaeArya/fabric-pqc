"""
Common — DID Utilities
Helpers for generating decentralised identifiers (did:key method).
"""

import base64
import hashlib


def generate_did_key(public_key: bytes) -> str:
    """
    Generate a did:key identifier from a raw public key.

    Uses a base64-encoded fingerprint of the public key.

    Args:
        public_key: Raw public key bytes.

    Returns:
        A did:key string, e.g. did:key:z6Mk...
    """
    fingerprint = hashlib.sha256(public_key).digest()
    encoded = base64.urlsafe_b64encode(fingerprint).decode("utf-8").rstrip("=")
    return f"did:key:z{encoded}"


def parse_did(did: str) -> dict:
    """
    Parse a DID string into its components.

    Args:
        did: A DID string (e.g. did:key:z6Mk...).

    Returns:
        Dict with 'method' and 'identifier' keys.
    """
    parts = did.split(":")
    if len(parts) < 3 or parts[0] != "did":
        raise ValueError(f"Invalid DID format: {did}")

    return {
        "method": parts[1],
        "identifier": ":".join(parts[2:]),
    }
