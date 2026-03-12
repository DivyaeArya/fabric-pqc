"""
Holder Wallet — Wallet Routes
REST API endpoints for storing and presenting credentials.
"""

from flask import Blueprint, request, jsonify
from services.wallet_service import WalletService

wallet_bp = Blueprint("wallet", __name__)
wallet_service = WalletService()


@wallet_bp.route("/store", methods=["POST"])
def store_credential():
    """
    Store a verifiable credential in the holder's local wallet.

    Request JSON:
        { "credential": { ... } }

    Returns:
        201: Storage confirmation with credential ID
        400: Missing credential
    """
    data = request.get_json()

    if not data or not data.get("credential"):
        return jsonify({"error": "credential is required"}), 400

    try:
        result = wallet_service.store(data["credential"])
        return jsonify(result), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@wallet_bp.route("/present", methods=["POST"])
def present_credential():
    """
    Create a Verifiable Presentation from a stored credential.

    Request JSON:
        { "credential_id": "urn:uuid:..." }

    Returns:
        200: The verifiable presentation
        400: Missing credential_id
        404: Credential not found
    """
    data = request.get_json()

    if not data or not data.get("credential_id"):
        return jsonify({"error": "credential_id is required"}), 400

    try:
        presentation = wallet_service.present(data["credential_id"])
        if presentation is None:
            return jsonify({"error": "Credential not found"}), 404
        return jsonify(presentation), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@wallet_bp.route("/list", methods=["GET"])
def list_credentials():
    """
    List all credentials in the wallet.

    Returns:
        200: List of stored credential summaries
    """
    try:
        credentials = wallet_service.list_all()
        return jsonify({"credentials": credentials}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
