"""
Verifier Service — Verification Service
Orchestrates signature verification and revocation checks.
"""

import json
import logging
from datetime import datetime, timezone

from utils.dilithium_verifier import DilithiumVerifier
from services.fabric_client import FabricClient

logger = logging.getLogger(__name__)


class VerificationService:
    """Coordinates Dilithium signature verification and Fabric revocation checks."""

    def __init__(self):
        self.verifier = DilithiumVerifier()
        self.fabric_client = FabricClient()

    def verify(self, credential: dict, issuer_public_key_b64: str) -> dict:
        """
        Verify a verifiable credential end-to-end.

        Steps:
            1. Extract proof / signature from the credential.
            2. Verify Dilithium signature against the issuer's public key.
            3. Query Fabric for revocation status.

        Args:
            credential:           The full VC dict (with proof).
            issuer_public_key_b64: Base64-encoded Dilithium public key.

        Returns:
            Dict with verification outcome.
        """
        credential_id = credential.get("id", "unknown")
        proof = credential.get("proof", {})
        signature_b64 = proof.get("signatureValue")

        if not signature_b64:
            return self._result(credential_id, False, "Missing proof/signatureValue")

        # Reconstruct the signed payload (credential without proof)
        cred_without_proof = {k: v for k, v in credential.items() if k != "proof"}
        message = json.dumps(cred_without_proof, sort_keys=True).encode("utf-8")

        # Step 1: Verify Dilithium signature
        sig_valid = self.verifier.verify(message, signature_b64, issuer_public_key_b64)
        if not sig_valid:
            return self._result(credential_id, False, "Dilithium signature verification failed")

        # Step 2: Check revocation on Fabric
        revocation = self.fabric_client.check_revocation(credential_id)
        if revocation.get("revoked"):
            return self._result(credential_id, False, "Credential has been revoked")

        return self._result(credential_id, True, "Credential is valid")

    @staticmethod
    def _result(credential_id: str, valid: bool, message: str) -> dict:
        """Build a standardised verification result dict."""
        return {
            "credential_id": credential_id,
            "valid": valid,
            "message": message,
            "verified_at": datetime.now(timezone.utc).isoformat(),
        }
