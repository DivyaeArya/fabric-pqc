"""
Quantum Rakshak — Verifier Service
Flask application factory.
"""

from flask import Flask
from routes.verify_routes import verify_bp
from config import Config


def create_app():
    """Create and configure the Flask application."""
    app = Flask(__name__)
    app.config.from_object(Config)

    # Register blueprints
    app.register_blueprint(verify_bp, url_prefix="/credentials")

    @app.route("/health")
    def health():
        return {"status": "ok", "service": "verifier"}

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=app.config.get("PORT", 5003), debug=True)
