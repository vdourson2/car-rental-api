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
genai.configure(api_key=os.getenv("aze"))
# Pour dev rapide :
# genai.configure(api_key="TA_CLE_GEMINI_ICI")


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
            model_name="gemini-1.5-flash",
            generation_config={
                # Niveau de créativité / aléatoire
                "temperature": temperature,

                # Nucleus sampling : diversité contrôlée
                "top_p": 1.0,

                # Limite des candidats probables
                "top_k": 40,

                # Nombre maximum de tokens générés
                "max_output_tokens": 512,
            }
        )

        response = model.generate_content(prompt)

        return jsonify({
            "response": response.text
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500