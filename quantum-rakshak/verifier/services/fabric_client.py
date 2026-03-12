"""
Verifier Service — Fabric Client
Interface with Hyperledger Fabric to check credential revocation status.
"""

import json
import logging
from config import Config

logger = logging.getLogger(__name__)


class FabricClient:
    """Gateway to Hyperledger Fabric credential-registry chaincode (read-only)."""

    def __init__(self):
        self.peer_address = Config.FABRIC_PEER_ADDRESS
        self.channel = Config.FABRIC_CHANNEL_NAME
        self.chaincode = Config.FABRIC_CHAINCODE_NAME
        self.msp_id = Config.FABRIC_MSP_ID
        logger.info(
            "FabricClient initialised — peer=%s channel=%s chaincode=%s",
            self.peer_address,
            self.channel,
            self.chaincode,
        )

    def check_revocation(self, credential_id: str) -> dict:
        """
        Evaluate a QueryCredential transaction to check revocation status.

        Args:
            credential_id: The credential identifier to look up.

        Returns:
            Dict with 'revoked' bool and optional metadata.
        """
        # TODO: Integrate with fabric-gateway Python SDK
        # For prototype, simulate a non-revoked response
        logger.info("QueryCredential (revocation check) — id=%s", credential_id)

        result = {
            "credential_id": credential_id,
            "revoked": False,
            "status": "active",
        }
        logger.info("Query result: %s", json.dumps(result))
        return result
