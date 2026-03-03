from flask import Blueprint, jsonify, request
import google.generativeai as genai
import os

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


@api_bp.get("/health")
def health():
    """
    Health check endpoint.

    Returns:
        JSON:
            status (str): Indique que l'API fonctionne correctement.
    """
    return jsonify({"status": "ok"})


@api_bp.get("/cars")
def list_cars():
    """
    Retourne la liste des voitures disponibles dans le système.

    Returns:
        JSON (list):
            id (int): Identifiant unique de la voiture.
            model (str): Nom du modèle.
            available (bool): Disponibilité pour location.
    """
    cars = [
        {"id": 1, "model": "Toyota Corolla", "available": True},
        {"id": 2, "model": "Ford Focus", "available": False},
    ]
    return jsonify(cars)


import json
import re

@api_bp.route("/generate", methods=["POST"])
def generate():
    """
    Génère une description premium en sortie JSON stricte.

    Body attendu:
        {
            "prompt": "...",
            "temperature": 0.4
        }

    Retour:
        {
            "description": "..."
        }
    """

    data = request.get_json()

    user_prompt = data.get("prompt")
    temperature = data.get("temperature", 0.7)

    if not user_prompt:
        return jsonify({"error": "Prompt is required"}), 400

    try:
        model = genai.GenerativeModel(
            model_name="gemini-1.5-flash-latest",
            generation_config={
                "temperature": temperature,
                "top_p": 1.0,
                "top_k": 40,
                "max_output_tokens": 512,
            }
        )

        # 🔒 On force la réponse JSON
        prompt = f"""
        Réponds UNIQUEMENT en JSON valide.
        Format attendu :

        {{
          "description": "string"
        }}

        Description demandée :
        {user_prompt}
        """

        response = model.generate_content(prompt)

        raw_text = response.text.strip()

        # 🧠 Nettoyage si le modèle entoure le JSON avec ```json
        raw_text = re.sub(r"^```json", "", raw_text)
        raw_text = re.sub(r"```$", "", raw_text).strip()

        parsed = json.loads(raw_text)

        return jsonify(parsed)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@api_bp.get("/models")
def list_models():
    models = []
    for m in genai.list_models():
        models.append({
            "name": m.name,
            "supported_generation_methods": getattr(m, "supported_generation_methods", [])
        })
    return jsonify(models)