"""
Issuer Service — Credential Routes
REST API endpoints for issuing verifiable credentials.
"""

from flask import Blueprint, request, jsonify
from services.credential_service import CredentialService

credential_bp = Blueprint("credentials", __name__)
credential_service = CredentialService()


@credential_bp.route("/issue", methods=["POST"])
def issue_credential():
    """
    Issue a new verifiable credential.

    Request JSON:
        {
            "holder_did": "did:key:...",
            "claims": {
                "name": "Alice",
                "degree": "MSc Computer Science"
            }
        }

    Returns:
        201: The signed verifiable credential
        400: Missing or invalid fields
    """
    data = request.get_json()

    if not data:
        return jsonify({"error": "Request body is required"}), 400

    holder_did = data.get("holder_did")
    claims = data.get("claims")

    if not holder_did:
        return jsonify({"error": "holder_did is required"}), 400
    if not claims or not isinstance(claims, dict):
        return jsonify({"error": "claims must be a non-empty object"}), 400

    try:
        credential = credential_service.issue(holder_did, claims)
        return jsonify(credential), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@credential_bp.route("/revoke", methods=["POST"])
def revoke_credential():
    """
    Revoke a credential by its ID.

    Request JSON:
        { "credential_id": "urn:uuid:..." }

    Returns:
        200: Revocation confirmation
        400: Missing credential_id
    """
    data = request.get_json()

    if not data or not data.get("credential_id"):
        return jsonify({"error": "credential_id is required"}), 400

    try:
        result = credential_service.revoke(data["credential_id"])
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
