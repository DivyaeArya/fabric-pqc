"""
Holder Wallet — Wallet Service
Local JSON-file-based credential storage and presentation builder.
"""

import os
import json
import uuid
import logging
from datetime import datetime, timezone

from config import Config

logger = logging.getLogger(__name__)


class WalletService:
    """Manages local credential storage and verifiable-presentation generation."""

    def __init__(self):
        self.storage_path = Config.STORAGE_PATH
        os.makedirs(self.storage_path, exist_ok=True)
        logger.info("WalletService initialised — storage=%s", self.storage_path)

    def _credential_filepath(self, credential_id: str) -> str:
        """Return the file path for a given credential ID."""
        safe_name = credential_id.replace(":", "_").replace("/", "_")
        return os.path.join(self.storage_path, f"{safe_name}.json")

    def store(self, credential: dict) -> dict:
        """
        Persist a credential to local storage.

        Args:
            credential: The full verifiable credential dict.

        Returns:
            Confirmation with credential_id.
        """
        credential_id = credential.get("id", f"urn:uuid:{uuid.uuid4()}")
        filepath = self._credential_filepath(credential_id)

        with open(filepath, "w") as f:
            json.dump(credential, f, indent=2)

        logger.info("Stored credential %s → %s", credential_id, filepath)
        return {
            "status": "stored",
            "credential_id": credential_id,
        }

    def present(self, credential_id: str) -> dict | None:
        """
        Build a Verifiable Presentation wrapping a stored credential.

        Args:
            credential_id: The credential identifier to present.

        Returns:
            A Verifiable Presentation dict, or None if credential is not found.
        """
        filepath = self._credential_filepath(credential_id)

        if not os.path.exists(filepath):
            logger.warning("Credential not found: %s", credential_id)
            return None

        with open(filepath, "r") as f:
            credential = json.load(f)

        presentation = {
            "@context": ["https://www.w3.org/2018/credentials/v1"],
            "type": ["VerifiablePresentation"],
            "id": f"urn:uuid:{uuid.uuid4()}",
            "holder": credential.get("credentialSubject", {}).get("id", "unknown"),
            "verifiableCredential": [credential],
            "created": datetime.now(timezone.utc).isoformat(),
        }

        logger.info("Created VP for credential %s", credential_id)
        return presentation

    def list_all(self) -> list[dict]:
        """
        List summary info for all stored credentials.

        Returns:
            List of dicts with id, issuer, and issuanceDate for each credential.
        """
        credentials = []
        for filename in os.listdir(self.storage_path):
            if not filename.endswith(".json"):
                continue
            filepath = os.path.join(self.storage_path, filename)
            try:
                with open(filepath, "r") as f:
                    cred = json.load(f)
                credentials.append(
                    {
                        "id": cred.get("id"),
                        "issuer": cred.get("issuer"),
                        "issuanceDate": cred.get("issuanceDate"),
                        "type": cred.get("type"),
                    }
                )
            except (json.JSONDecodeError, IOError) as e:
                logger.error("Failed to read %s: %s", filepath, e)

        return credentials
