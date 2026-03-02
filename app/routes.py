from flask import Blueprint, jsonify

api_bp = Blueprint('api', __name__)

@api_bp.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "ok"})

@api_bp.route('/cars', methods=['GET'])
def list_cars():
    cars = [
        {"id": 1, "model": "Toyota Corolla", "available": true},
        {"id": 2, "model": "Ford Focus", "available": false},
    ]
    return jsonify(cars)

def register_routes(app):
    app.register_blueprint(api_bp, url_prefix='/api')
