from flask import Flask, jsonify
from flask_cors import CORS

def create_app():
    app = Flask(__name__)
    CORS(app)  # autorise tout en dev

    from .routes import api_bp
    app.register_blueprint(api_bp, url_prefix="/api")

    @app.get("/openapi.json")
    def openapi():
        return jsonify({
            "openapi": "3.0.0",
            "info": {"title": "Car Rental API", "version": "1.0.0"},
            "paths": {}
        })

    return app