import os


def build_openapi_spec() -> dict:
    server_url = os.getenv("OPENAPI_SERVER_URL", "http://localhost:5000")

    return {
        "openapi": "3.0.3",
        "info": {"title": "Car Rental API", "version": "1.0.0"},
        "tags": [
            {"name": "Health", "description": "Verification de l'etat du service"},
            {"name": "Vehicules", "description": "Gestion du parc de vehicules"},
            {"name": "Clients", "description": "Gestion des clients"},
            {"name": "Utilisateurs", "description": "Gestion des utilisateurs"},
            {
                "name": "Authentification",
                "description": "Login et verification d'identite",
            },
            {"name": "Locations", "description": "Gestion des reservations/location"},
            {"name": "IA", "description": "Endpoints Gemini"},
        ],
        "servers": [
            {
                "url": server_url,
                "description": "Backend API",
            }
        ],
        "paths": {
            "/api/health": {
                "get": {
                    "tags": ["Health"],
                    "summary": "Health check",
                    "responses": {"200": {"description": "Service disponible"}},
                }
            },
            "/api/vehicles": {
                "get": {
                    "tags": ["Vehicules"],
                    "summary": "Lister les vehicules",
                    "responses": {"200": {"description": "Liste des vehicules"}},
                },
                "post": {
                    "tags": ["Vehicules"],
                    "summary": "Creer un vehicule",
                    "requestBody": {
                        "required": True,
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "required": [
                                        "marque",
                                        "modele",
                                        "immatriculation",
                                        "prix_par_jour",
                                    ],
                                    "properties": {
                                        "marque": {"type": "string"},
                                        "modele": {"type": "string"},
                                        "immatriculation": {"type": "string"},
                                        "prix_par_jour": {"type": "number"},
                                        "statut": {
                                            "type": "string",
                                            "enum": ["disponible", "loue"],
                                        },
                                    },
                                }
                            }
                        },
                    },
                    "responses": {"201": {"description": "Vehicule cree"}},
                },
            },
            "/api/vehicles/{vehicule_id}": {
                "get": {
                    "tags": ["Vehicules"],
                    "summary": "Obtenir un vehicule",
                    "parameters": [
                        {
                            "name": "vehicule_id",
                            "in": "path",
                            "required": True,
                            "schema": {"type": "integer"},
                        }
                    ],
                    "responses": {
                        "200": {"description": "Vehicule trouve"},
                        "404": {"description": "Introuvable"},
                    },
                },
                "put": {
                    "tags": ["Vehicules"],
                    "summary": "Mettre a jour un vehicule",
                    "parameters": [
                        {
                            "name": "vehicule_id",
                            "in": "path",
                            "required": True,
                            "schema": {"type": "integer"},
                        }
                    ],
                    "requestBody": {
                        "required": True,
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "properties": {
                                        "marque": {"type": "string"},
                                        "modele": {"type": "string"},
                                        "immatriculation": {"type": "string"},
                                        "prix_par_jour": {"type": "number"},
                                        "statut": {
                                            "type": "string",
                                            "enum": ["disponible", "loue"],
                                        },
                                    },
                                }
                            }
                        },
                    },
                    "responses": {"200": {"description": "Vehicule mis a jour"}},
                },
                "delete": {
                    "tags": ["Vehicules"],
                    "summary": "Supprimer un vehicule",
                    "parameters": [
                        {
                            "name": "vehicule_id",
                            "in": "path",
                            "required": True,
                            "schema": {"type": "integer"},
                        }
                    ],
                    "responses": {"204": {"description": "Vehicule supprime"}},
                },
            },
            "/api/clients": {
                "get": {
                    "tags": ["Clients"],
                    "summary": "Lister les clients",
                    "responses": {"200": {"description": "Liste des clients"}},
                },
                "post": {
                    "tags": ["Clients"],
                    "summary": "Creer un client",
                    "requestBody": {
                        "required": True,
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "required": ["nom", "contact", "numero_permis"],
                                    "properties": {
                                        "nom": {"type": "string"},
                                        "contact": {"type": "string"},
                                        "numero_permis": {"type": "string"},
                                    },
                                }
                            }
                        },
                    },
                    "responses": {"201": {"description": "Client cree"}},
                },
            },
            "/api/clients/{client_id}": {
                "get": {
                    "tags": ["Clients"],
                    "summary": "Obtenir un client",
                    "parameters": [
                        {
                            "name": "client_id",
                            "in": "path",
                            "required": True,
                            "schema": {"type": "integer"},
                        }
                    ],
                    "responses": {
                        "200": {"description": "Client trouve"},
                        "404": {"description": "Introuvable"},
                    },
                },
                "put": {
                    "tags": ["Clients"],
                    "summary": "Mettre a jour un client",
                    "parameters": [
                        {
                            "name": "client_id",
                            "in": "path",
                            "required": True,
                            "schema": {"type": "integer"},
                        }
                    ],
                    "requestBody": {
                        "required": True,
                        "content": {"application/json": {"schema": {"type": "object"}}},
                    },
                    "responses": {"200": {"description": "Client mis a jour"}},
                },
                "delete": {
                    "tags": ["Clients"],
                    "summary": "Supprimer un client",
                    "parameters": [
                        {
                            "name": "client_id",
                            "in": "path",
                            "required": True,
                            "schema": {"type": "integer"},
                        }
                    ],
                    "responses": {"204": {"description": "Client supprime"}},
                },
            },
            "/api/users": {
                "get": {
                    "tags": ["Utilisateurs"],
                    "summary": "Lister les utilisateurs",
                    "responses": {"200": {"description": "Liste des utilisateurs"}},
                },
                "post": {
                    "tags": ["Utilisateurs"],
                    "summary": "Creer un utilisateur",
                    "requestBody": {
                        "required": True,
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "required": ["identifiant", "mot_de_passe"],
                                    "properties": {
                                        "identifiant": {"type": "string"},
                                        "mot_de_passe": {"type": "string"},
                                    },
                                }
                            }
                        },
                    },
                    "responses": {"201": {"description": "Utilisateur cree"}},
                },
            },
            "/api/users/{utilisateur_id}": {
                "get": {
                    "tags": ["Utilisateurs"],
                    "summary": "Obtenir un utilisateur",
                    "parameters": [
                        {
                            "name": "utilisateur_id",
                            "in": "path",
                            "required": True,
                            "schema": {"type": "integer"},
                        }
                    ],
                    "responses": {
                        "200": {"description": "Utilisateur trouve"},
                        "404": {"description": "Introuvable"},
                    },
                },
                "put": {
                    "tags": ["Utilisateurs"],
                    "summary": "Mettre a jour un utilisateur",
                    "parameters": [
                        {
                            "name": "utilisateur_id",
                            "in": "path",
                            "required": True,
                            "schema": {"type": "integer"},
                        }
                    ],
                    "requestBody": {
                        "required": True,
                        "content": {"application/json": {"schema": {"type": "object"}}},
                    },
                    "responses": {"200": {"description": "Utilisateur mis a jour"}},
                },
                "delete": {
                    "tags": ["Utilisateurs"],
                    "summary": "Supprimer un utilisateur",
                    "parameters": [
                        {
                            "name": "utilisateur_id",
                            "in": "path",
                            "required": True,
                            "schema": {"type": "integer"},
                        }
                    ],
                    "responses": {"204": {"description": "Utilisateur supprime"}},
                },
            },
            "/api/auth/login": {
                "post": {
                    "tags": ["Authentification"],
                    "summary": "Authentifier un utilisateur",
                    "requestBody": {
                        "required": True,
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "required": ["identifiant", "mot_de_passe"],
                                    "properties": {
                                        "identifiant": {"type": "string"},
                                        "mot_de_passe": {"type": "string"},
                                    },
                                }
                            }
                        },
                    },
                    "responses": {"200": {"description": "Authentification reussie"}},
                }
            },
            "/api/locations": {
                "get": {
                    "tags": ["Locations"],
                    "summary": "Lister les locations",
                    "responses": {"200": {"description": "Liste des locations"}},
                },
                "post": {
                    "tags": ["Locations"],
                    "summary": "Creer une location",
                    "requestBody": {
                        "required": True,
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "required": [
                                        "date_debut",
                                        "date_fin",
                                        "id_client",
                                        "id_vehicule",
                                        "id_utilisateur",
                                    ],
                                    "properties": {
                                        "date_debut": {
                                            "type": "string",
                                            "format": "date",
                                        },
                                        "date_fin": {
                                            "type": "string",
                                            "format": "date",
                                        },
                                        "id_client": {"type": "integer"},
                                        "id_vehicule": {"type": "integer"},
                                        "id_utilisateur": {"type": "integer"},
                                    },
                                }
                            }
                        },
                    },
                    "responses": {"201": {"description": "Location creee"}},
                },
            },
            "/api/locations/{location_id}": {
                "get": {
                    "tags": ["Locations"],
                    "summary": "Obtenir une location",
                    "parameters": [
                        {
                            "name": "location_id",
                            "in": "path",
                            "required": True,
                            "schema": {"type": "integer"},
                        }
                    ],
                    "responses": {
                        "200": {"description": "Location trouvee"},
                        "404": {"description": "Introuvable"},
                    },
                },
                "delete": {
                    "tags": ["Locations"],
                    "summary": "Supprimer une location",
                    "parameters": [
                        {
                            "name": "location_id",
                            "in": "path",
                            "required": True,
                            "schema": {"type": "integer"},
                        }
                    ],
                    "responses": {"204": {"description": "Location supprimee"}},
                },
            },
            "/api/locations/{location_id}/close": {
                "post": {
                    "tags": ["Locations"],
                    "summary": "Cloturer une location",
                    "parameters": [
                        {
                            "name": "location_id",
                            "in": "path",
                            "required": True,
                            "schema": {"type": "integer"},
                        }
                    ],
                    "responses": {"200": {"description": "Location cloturee"}},
                }
            },
            "/api/models": {
                "get": {
                    "tags": ["IA"],
                    "summary": "Lister les modeles Gemini",
                    "responses": {"200": {"description": "Liste des modeles"}},
                }
            },
            "/api/generate": {
                "post": {
                    "tags": ["IA"],
                    "summary": "Generer du texte via Gemini",
                    "requestBody": {
                        "required": True,
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "required": ["prompt"],
                                    "properties": {
                                        "prompt": {"type": "string"},
                                        "temperature": {
                                            "type": "number",
                                            "default": 0.7,
                                        },
                                    },
                                }
                            }
                        },
                    },
                    "responses": {"200": {"description": "Texte genere"}},
                }
            },
        },
    }
