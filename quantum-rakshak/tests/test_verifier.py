"""
Tests — Verifier Service
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))


class TestVerifierService:
    """Placeholder tests for the Verifier Service."""

    def test_verifier_app_creates(self):
        """Verify the verifier app can be created."""
        from verifier.app import create_app

        app = create_app()
        assert app is not None

    def test_health_endpoint(self):
        """Health endpoint returns ok."""
        from verifier.app import create_app

        app = create_app()
        client = app.test_client()
        resp = client.get("/health")
        assert resp.status_code == 200
        assert resp.get_json()["service"] == "verifier"

    def test_verify_missing_body_returns_400(self):
        """POST /credentials/verify with no body returns 400."""
        from verifier.app import create_app

        app = create_app()
        client = app.test_client()
        resp = client.post("/credentials/verify", json={})
        assert resp.status_code == 400
