"""
Common — Credential & Presentation Schemas
JSON structure definitions for Verifiable Credentials and Verifiable Presentations.
"""


def verifiable_credential_template() -> dict:
    """
    Return a blank Verifiable Credential template (W3C VC Data Model).

    Returns:
        A dict with standard VC fields set to placeholder values.
    """
    return {
        "@context": [
            "https://www.w3.org/2018/credentials/v1",
            "https://w3id.org/security/suites/dilithium-2023/v1",
        ],
        "id": "",
        "type": ["VerifiableCredential"],
        "issuer": "",
        "issuanceDate": "",
        "credentialSubject": {},
        "proof": {},
    }


def verifiable_presentation_template() -> dict:
    """
    Return a blank Verifiable Presentation template.

    Returns:
        A dict with standard VP fields.
    """
    return {
        "@context": ["https://www.w3.org/2018/credentials/v1"],
        "type": ["VerifiablePresentation"],
        "id": "",
        "holder": "",
        "verifiableCredential": [],
    }


REQUIRED_VC_FIELDS = [
    "@context",
    "id",
    "type",
    "issuer",
    "issuanceDate",
    "credentialSubject",
    "proof",
]


def validate_credential(credential: dict) -> tuple[bool, str]:
    """
    Validate that a credential dict contains all required fields.

    Args:
        credential: The credential dict to validate.

    Returns:
        Tuple of (is_valid, error_message).
    """
    for field in REQUIRED_VC_FIELDS:
        if field not in credential:
            return False, f"Missing required field: {field}"

    if "VerifiableCredential" not in credential.get("type", []):
        return False, "type must include 'VerifiableCredential'"

    return True, ""
