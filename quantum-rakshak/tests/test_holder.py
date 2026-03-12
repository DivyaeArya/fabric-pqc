"""
Tests — Holder Wallet
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))


class TestHolderWallet:
    """Placeholder tests for the Holder Wallet."""

    def test_holder_app_creates(self):
        """Verify the holder app can be created."""
        from holder.app import create_app

        app = create_app()
        assert app is not None

    def test_health_endpoint(self):
        """Health endpoint returns ok."""
        from holder.app import create_app

        app = create_app()
        client = app.test_client()
        resp = client.get("/health")
        assert resp.status_code == 200
        assert resp.get_json()["service"] == "holder"

    def test_store_missing_credential_returns_400(self):
        """POST /wallet/store with no credential returns 400."""
        from holder.app import create_app

        app = create_app()
        client = app.test_client()
        resp = client.post("/wallet/store", json={})
        assert resp.status_code == 400
