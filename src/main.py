import logging, os
from flask import Flask, jsonify
from .config import get_settings
from .tautulli_webhook import bp as tautulli_bp

def create_app() -> Flask:
    app = Flask(__name__)
    app.register_blueprint(tautulli_bp)
    @app.get("/health")
    def health():
        return jsonify({"status":"ok"}), 200
    return app

if __name__ == "__main__":
    settings = get_settings()
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
    app = create_app()
    app.run(host="0.0.0.0", port=settings.port)
