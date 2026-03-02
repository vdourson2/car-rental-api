from flask import Blueprint, jsonify

api_bp = Blueprint("api", __name__)

@api_bp.get("/health")
def health():
    return jsonify({"status": "ok"})

@api_bp.get("/cars")
def list_cars():
    cars = [
        {"id": 1, "model": "Toyota Corolla", "available": True},
        {"id": 2, "model": "Ford Focus", "available": False},
    ]
    return jsonify(cars)