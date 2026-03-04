import os

import google.generativeai as genai
from flask import Blueprint, jsonify, request
from sqlalchemy.exc import IntegrityError

from app.repositories import ClientRepository, LocationRepository, UtilisateurRepository, VehiculeRepository
from app.services import (
    ClientService,
    LocationService,
    ServiceError,
    UtilisateurService,
    VehiculeService,
)

api_bp = Blueprint("api", __name__)

# -------------------------------------------------------------------
# Configuration Gemini
# -------------------------------------------------------------------
# Configure l'accès à l'API Gemini.
# ⚠️ En production, utiliser une variable d'environnement :
# export GEMINI_API_KEY="ta_cle"
# 
# # Pour dev rapide :
genai.configure(api_key="AIzaSyA581wHjY1v3JCMcTH8kMLQnh23AQGCXs8")

client_service = ClientService(ClientRepository())
vehicule_service = VehiculeService(VehiculeRepository())
utilisateur_service = UtilisateurService(UtilisateurRepository())
location_service = LocationService(
    LocationRepository(),
    ClientRepository(),
    VehiculeRepository(),
    UtilisateurRepository(),
)


@api_bp.errorhandler(ServiceError)
def handle_service_error(error: ServiceError):
    return jsonify({"error": error.message}), error.status_code


@api_bp.errorhandler(IntegrityError)
def handle_integrity_error(_error: IntegrityError):
    return jsonify({"error": "Contrainte base de donnees violee."}), 409


@api_bp.get("/health")
def health():
    return jsonify({"status": "ok"})


@api_bp.get("/vehicles")
def list_vehicles():
    return jsonify([vehicle.to_dict() for vehicle in vehicule_service.list_vehicules()])


@api_bp.get("/vehicles/<int:vehicule_id>")
def get_vehicle(vehicule_id: int):
    vehicle = vehicule_service.get_vehicule(vehicule_id)
    return jsonify(vehicle.to_dict())


@api_bp.post("/vehicles")
def create_vehicle():
    payload = request.get_json(silent=True) or {}
    vehicle = vehicule_service.create_vehicule(payload)
    return jsonify(vehicle.to_dict()), 201


@api_bp.put("/vehicles/<int:vehicule_id>")
def update_vehicle(vehicule_id: int):
    payload = request.get_json(silent=True) or {}
    vehicle = vehicule_service.update_vehicule(vehicule_id, payload)
    return jsonify(vehicle.to_dict())


@api_bp.delete("/vehicles/<int:vehicule_id>")
def delete_vehicle(vehicule_id: int):
    vehicule_service.delete_vehicule(vehicule_id)
    return "", 204


@api_bp.get("/cars")
def list_cars_legacy():
    vehicles = vehicule_service.list_vehicules()
    return jsonify(
        [
            {
                "id": vehicle.id_vehicule,
                "model": f"{vehicle.marque} {vehicle.modele}",
                "available": vehicle.statut == "disponible",
            }
            for vehicle in vehicles
        ]
    )


@api_bp.get("/clients")
def list_clients():
    return jsonify([client.to_dict() for client in client_service.list_clients()])


@api_bp.get("/clients/<int:client_id>")
def get_client(client_id: int):
    client = client_service.get_client(client_id)
    return jsonify(client.to_dict())


@api_bp.post("/clients")
def create_client():
    payload = request.get_json(silent=True) or {}
    client = client_service.create_client(payload)
    return jsonify(client.to_dict()), 201


@api_bp.put("/clients/<int:client_id>")
def update_client(client_id: int):
    payload = request.get_json(silent=True) or {}
    client = client_service.update_client(client_id, payload)
    return jsonify(client.to_dict())


@api_bp.delete("/clients/<int:client_id>")
def delete_client(client_id: int):
    client_service.delete_client(client_id)
    return "", 204


@api_bp.get("/users")
def list_users():
    return jsonify([user.to_dict() for user in utilisateur_service.list_utilisateurs()])


@api_bp.get("/users/<int:utilisateur_id>")
def get_user(utilisateur_id: int):
    user = utilisateur_service.get_utilisateur(utilisateur_id)
    return jsonify(user.to_dict())


@api_bp.post("/users")
def create_user():
    payload = request.get_json(silent=True) or {}
    user = utilisateur_service.create_utilisateur(payload)
    return jsonify(user.to_dict()), 201


@api_bp.put("/users/<int:utilisateur_id>")
def update_user(utilisateur_id: int):
    payload = request.get_json(silent=True) or {}
    user = utilisateur_service.update_utilisateur(utilisateur_id, payload)
    return jsonify(user.to_dict())


@api_bp.delete("/users/<int:utilisateur_id>")
def delete_user(utilisateur_id: int):
    utilisateur_service.delete_utilisateur(utilisateur_id)
    return "", 204


@api_bp.post("/auth/login")
def login():
    payload = request.get_json(silent=True) or {}
    user = utilisateur_service.authenticate(payload)
    return jsonify({"message": "Authentification reussie.", "utilisateur": user.to_dict()})


@api_bp.get("/locations")
def list_locations():
    return jsonify([location.to_dict() for location in location_service.list_locations()])


@api_bp.get("/locations/<int:location_id>")
def get_location(location_id: int):
    location = location_service.get_location(location_id)
    return jsonify(location.to_dict())


@api_bp.post("/locations")
def create_location():
    payload = request.get_json(silent=True) or {}
    location = location_service.create_location(payload)
    return jsonify(location.to_dict()), 201


@api_bp.post("/locations/<int:location_id>/close")
def close_location(location_id: int):
    location = location_service.close_location(location_id)
    return jsonify(location.to_dict())


@api_bp.delete("/locations/<int:location_id>")
def delete_location(location_id: int):
    location_service.delete_location(location_id)
    return "", 204

@api_bp.post("/generate")
def generate():
    """
    Génère un texte via l'API Google Gemini.

    Body JSON attendu:
        prompt (str, obligatoire):
            Texte envoyé au modèle.

        temperature (float, optionnel, défaut=0.7):
            Contrôle la créativité du modèle.
            - 0.0 → réponse très déterministe
            - 0.3 → factuel / stable
            - 0.7 → équilibré
            - 1.0+ → créatif / plus aléatoire

    Paramètres Gemini utilisés:
        model_name (str):
            "gemini-1.5-flash"
            → Modèle rapide et gratuit (free tier)

        generation_config (dict):
            temperature (float):
                Niveau d'aléatoire dans le choix des tokens.

            top_p (float):
                Nucleus sampling.
                Le modèle choisit parmi les tokens
                dont la probabilité cumulée atteint top_p.
                1.0 = désactivé (considère tous les tokens).

            top_k (int):
                Limite le nombre de tokens candidats
                parmi lesquels le modèle peut choisir.
                Plus bas = plus déterministe.

            max_output_tokens (int):
                Longueur maximale de la réponse générée.

    Returns:
        JSON:
            response (str): Texte généré par Gemini.

    Errors:
        400 si le prompt est absent.
        500 en cas d'erreur API.
    """

    data = request.get_json()

    prompt = data.get("prompt")
    temperature = data.get("temperature", 0.7)

    if not prompt:
        return jsonify({"error": "Prompt is required"}), 400

    try:
        model = genai.GenerativeModel(
            model_name="gemini-2.5-flash",
            generation_config={
                # Niveau de créativité / aléatoire
                "temperature": temperature,

                # Nucleus sampling : diversité contrôlée
                "top_p": 1.0,

                # Limite des candidats probables
                "top_k": 40,

                # Nombre maximum de tokens générés
                "max_output_tokens": 512,
            },
        )

        response = model.generate_content(prompt)

        print(response.text)

        json_response = jsonify({
            "response": response.text
        })

        return json_response

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@api_bp.get("/models")
def list_models():
    """Retrieve a list of available Gemini models.

    This endpoint queries the Google Gemini API via ``genai.list_models()`` and
    returns a JSON array where each element contains:
        - ``name``: The model's identifier.
        - ``supported_generation_methods``: A list of generation methods the model
          supports (e.g., ``['generateContent']``). If the attribute is missing,
          an empty list is used.

    Returns:
        Flask ``Response``: JSON response with the list of model descriptors.
    """
    models = []
    for m in genai.list_models():
        models.append({
            "name": m.name,
            "supported_generation_methods": getattr(m, "supported_generation_methods", [])
        })
    return jsonify(models)
