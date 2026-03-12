"""
Tests — Issuer Service
"""

import sys
import os

# Allow imports from project root
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))


class TestIssuerService:
    """Placeholder tests for the Issuer Service."""

    def test_credential_issue_route_exists(self):
        """Verify the issuer app can be created."""
        # Deferred import so tests can be collected even without Flask installed
        from issuer.app import create_app

        app = create_app()
        assert app is not None

    def test_health_endpoint(self):
        """Health endpoint returns ok."""
        from issuer.app import create_app

        app = create_app()
        client = app.test_client()
        resp = client.get("/health")
        assert resp.status_code == 200
        assert resp.get_json()["service"] == "issuer"

    def test_issue_missing_body_returns_400(self):
        """POST /credentials/issue with no body returns 400."""
        from issuer.app import create_app

        app = create_app()
        client = app.test_client()
        resp = client.post("/credentials/issue", json={})
        assert resp.status_code == 400
