"""
Common — Shared Constants
"""

# Dilithium algorithm variants supported by liboqs
DILITHIUM_VARIANTS = [
    "Dilithium2",
    "Dilithium3",
    "Dilithium5",
]

# Default variant
DEFAULT_DILITHIUM_VARIANT = "Dilithium3"

# Credential statuses
CREDENTIAL_STATUS_ACTIVE = "active"
CREDENTIAL_STATUS_REVOKED = "revoked"

# W3C contexts
W3C_VC_CONTEXT = "https://www.w3.org/2018/credentials/v1"
DILITHIUM_SUITE_CONTEXT = "https://w3id.org/security/suites/dilithium-2023/v1"

# Proof type
DILITHIUM_PROOF_TYPE = "CrystalsDilithiumSignature2023"
