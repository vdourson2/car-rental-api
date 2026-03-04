from flask import Flask, jsonify
from flask_cors import CORS

from .config import Config
from .extensions import db, migrate
from .openapi import build_openapi_spec
from .seed import register_seed_command

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    CORS(app)  # autorise tout en dev

    db.init_app(app)
    migrate.init_app(app, db)

    from . import models  # noqa: F401
    from .routes import api_bp
    app.register_blueprint(api_bp, url_prefix="/api")
    register_seed_command(app)

    @app.get("/openapi.json")
    def openapi():
        return jsonify(build_openapi_spec())

    @app.get("/api/openapi.json")
    def openapi_with_api_prefix():
        return jsonify(build_openapi_spec())

    @app.get("/api")
    def openapi_api_root():
        return jsonify(build_openapi_spec())

    return app
