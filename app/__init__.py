from flask import Flask, jsonify
from flask_cors import CORS

from .config import Config
from .extensions import db, migrate

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    CORS(app)  # autorise tout en dev

    db.init_app(app)
    migrate.init_app(app, db)

    from . import models  # noqa: F401
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
