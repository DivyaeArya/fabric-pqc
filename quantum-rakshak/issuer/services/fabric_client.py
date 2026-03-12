"""
Issuer Service — Fabric Client
Interface with Hyperledger Fabric to register / revoke credential metadata.
"""

import json
import logging
from config import Config

logger = logging.getLogger(__name__)


class FabricClient:
    """Gateway to Hyperledger Fabric credential-registry chaincode."""

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

    def register_credential(
        self,
        credential_id: str,
        credential_hash: str,
        issuer_did: str,
        holder_did: str,
    ) -> dict:
        """
        Submit a RegisterCredential transaction to the chaincode.

        Args:
            credential_id:   Unique credential URN.
            credential_hash: SHA-256 hash of the unsigned credential.
            issuer_did:      DID of the issuer.
            holder_did:      DID of the holder.

        Returns:
            Transaction result dict.
        """
        # TODO: Integrate with fabric-gateway Python SDK
        # For prototype, simulate the transaction
        logger.info(
            "RegisterCredential — id=%s hash=%s issuer=%s holder=%s",
            credential_id,
            credential_hash,
            issuer_did,
            holder_did,
        )

        result = {
            "transaction": "RegisterCredential",
            "credential_id": credential_id,
            "status": "committed",
        }
        logger.info("Transaction result: %s", json.dumps(result))
        return result

    def revoke_credential(self, credential_id: str) -> dict:
        """
        Submit a RevokeCredential transaction to the chaincode.

        Args:
            credential_id: The credential identifier to revoke.

        Returns:
            Transaction result dict.
        """
        # TODO: Integrate with fabric-gateway Python SDK
        logger.info("RevokeCredential — id=%s", credential_id)

        result = {
            "transaction": "RevokeCredential",
            "credential_id": credential_id,
            "status": "committed",
        }
        logger.info("Transaction result: %s", json.dumps(result))
        return result
