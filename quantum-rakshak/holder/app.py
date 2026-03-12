"""
Quantum Rakshak — Holder Wallet
Flask application factory.
"""

from flask import Flask
from routes.wallet_routes import wallet_bp
from config import Config


def create_app():
    """Create and configure the Flask application."""
    app = Flask(__name__)
    app.config.from_object(Config)

    # Register blueprints
    app.register_blueprint(wallet_bp, url_prefix="/wallet")

    @app.route("/health")
    def health():
        return {"status": "ok", "service": "holder"}

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=app.config.get("PORT", 5002), debug=True)
