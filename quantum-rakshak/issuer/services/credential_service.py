"""
Issuer Service — Credential Service
Business logic for creating and signing verifiable credentials.
"""

import uuid
import json
import hashlib
from datetime import datetime, timezone

from utils.dilithium_signer import DilithiumSigner
from services.fabric_client import FabricClient


class CredentialService:
    """Handles credential issuance, signing, and registration."""

    def __init__(self):
        self.signer = DilithiumSigner()
        self.fabric_client = FabricClient()

    def issue(self, holder_did: str, claims: dict) -> dict:
        """
        Issue a verifiable credential.

        1. Build the credential payload
        2. Sign with Dilithium
        3. Register metadata on Fabric

        Args:
            holder_did: The DID of the credential holder.
            claims: Key-value claims for the credential.

        Returns:
            The signed verifiable credential as a dict.
        """
        credential_id = f"urn:uuid:{uuid.uuid4()}"
        issuance_date = datetime.now(timezone.utc).isoformat()

        # Build credential structure (W3C VC-like)
        credential = {
            "@context": [
                "https://www.w3.org/2018/credentials/v1",
                "https://w3id.org/security/suites/dilithium-2023/v1",
            ],
            "id": credential_id,
            "type": ["VerifiableCredential"],
            "issuer": self.signer.get_issuer_did(),
            "issuanceDate": issuance_date,
            "credentialSubject": {
                "id": holder_did,
                **claims,
            },
        }

        # Sign the credential
        credential_bytes = json.dumps(credential, sort_keys=True).encode("utf-8")
        signature = self.signer.sign(credential_bytes)

        credential["proof"] = {
            "type": "CrystalsDilithiumSignature2023",
            "created": issuance_date,
            "verificationMethod": self.signer.get_issuer_did(),
            "proofPurpose": "assertionMethod",
            "signatureValue": signature,
        }

        # Register credential metadata on Fabric
        credential_hash = hashlib.sha256(credential_bytes).hexdigest()
        self.fabric_client.register_credential(
            credential_id=credential_id,
            credential_hash=credential_hash,
            issuer_did=self.signer.get_issuer_did(),
            holder_did=holder_did,
        )

        return credential

    def revoke(self, credential_id: str) -> dict:
        """
        Revoke a credential by updating its status on Fabric.

        Args:
            credential_id: The unique credential identifier.

        Returns:
            Confirmation dict.
        """
        self.fabric_client.revoke_credential(credential_id)
        return {
            "status": "revoked",
            "credential_id": credential_id,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
