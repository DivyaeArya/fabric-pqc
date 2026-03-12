"""
Verifier Service — Verify Routes
REST API endpoints for verifying verifiable credentials.
"""

from flask import Blueprint, request, jsonify
from services.verification_service import VerificationService

verify_bp = Blueprint("verify", __name__)
verification_service = VerificationService()


@verify_bp.route("/verify", methods=["POST"])
def verify_credential():
    """
    Verify a verifiable credential.

    Performs:
        1. Dilithium signature verification
        2. Revocation status check on Fabric

    Request JSON:
        {
            "credential": { ... },
            "issuer_public_key": "<base64-encoded Dilithium public key>"
        }

    Returns:
        200: Verification result (valid/invalid + details)
        400: Missing fields
    """
    data = request.get_json()

    if not data:
        return jsonify({"error": "Request body is required"}), 400

    credential = data.get("credential")
    issuer_public_key = data.get("issuer_public_key")

    if not credential:
        return jsonify({"error": "credential is required"}), 400
    if not issuer_public_key:
        return jsonify({"error": "issuer_public_key is required"}), 400

    try:
        result = verification_service.verify(credential, issuer_public_key)
        status_code = 200 if result["valid"] else 200  # always 200; validity in body
        return jsonify(result), status_code
    except Exception as e:
        return jsonify({"error": str(e)}), 500
