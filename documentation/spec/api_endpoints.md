# Documentation API - Car Rental

Cette documentation decrit les endpoints exposes par le backend Flask.

Base URL (dev): `http://localhost:5000/api`

## Conventions

- Format d'echange: `application/json`
- Dates: format `YYYY-MM-DD`
- Erreurs metier: `{"error": "message"}`
- Codes d'erreur frequents:
  - `400` validation
  - `401` authentification
  - `404` ressource introuvable
  - `409` conflit (unicite, indisponibilite, contrainte DB)

## Health

### `GET /health`
Verifie que l'API repond.

Reponse `200`:
```json
{"status": "ok"}
```

## Vehicules

### `GET /vehicles`
Liste tous les vehicules.

Reponse `200`:
```json
[
  {
    "id_vehicule": 1,
    "marque": "Toyota",
    "modele": "Corolla",
    "immatriculation": "1-ABC-123",
    "prix_par_jour": 45.0,
    "statut": "disponible"
  }
]
```

### `GET /vehicles/{vehicule_id}`
Retourne un vehicule.

Reponses:
- `200` vehicule trouve
- `404` vehicule introuvable

### `POST /vehicles`
Cree un vehicule.

Body:
```json
{
  "marque": "Toyota",
  "modele": "Corolla",
  "immatriculation": "1-ABC-123",
  "prix_par_jour": 45.0,
  "statut": "disponible"
}
```

Reponses:
- `201` cree
- `400` champs invalides
- `409` immatriculation deja utilisee

### `PUT /vehicles/{vehicule_id}`
Met a jour un vehicule (partiel accepte).

Reponses:
- `200` mis a jour
- `400`, `404`, `409`

### `DELETE /vehicles/{vehicule_id}`
Supprime un vehicule.

Reponses:
- `204` supprime
- `404` introuvable
- `409` si contrainte FK

### `GET /cars` (legacy)
Format simplifie conserve pour compatibilite UI.

Reponse `200`:
```json
[
  {"id": 1, "model": "Toyota Corolla", "available": true}
]
```

## Clients

### `GET /clients`
Liste tous les clients.

### `GET /clients/{client_id}`
Retourne un client.

### `POST /clients`
Cree un client.

Body:
```json
{
  "nom": "Alice Dupont",
  "contact": "alice@email.com",
  "numero_permis": "BE-123456"
}
```

Reponses:
- `201` cree
- `400` validation
- `409` numero_permis deja utilise

### `PUT /clients/{client_id}`
Met a jour un client.

### `DELETE /clients/{client_id}`
Supprime un client.

Codes usuels: `200/204/400/404/409`

## Utilisateurs

### `GET /users`
Liste les utilisateurs (sans mot de passe).

### `GET /users/{utilisateur_id}`
Retourne un utilisateur (sans mot de passe).

### `POST /users`
Cree un utilisateur. Le mot de passe est hash en base.

Body:
```json
{
  "identifiant": "admin",
  "mot_de_passe": "secret"
}
```

Reponses:
- `201` cree
- `400` validation
- `409` identifiant deja utilise

### `PUT /users/{utilisateur_id}`
Met a jour identifiant et/ou mot de passe.

### `DELETE /users/{utilisateur_id}`
Supprime un utilisateur.

## Authentification

### `POST /auth/login`
Authentification simple identifiant/mot de passe.

Body:
```json
{
  "identifiant": "admin",
  "mot_de_passe": "secret"
}
```

Reponses:
- `200` authentifie
```json
{
  "message": "Authentification reussie.",
  "utilisateur": {
    "id_utilisateur": 1,
    "identifiant": "admin"
  }
}
```
- `400` champs manquants
- `401` identifiants invalides

## Locations

### `GET /locations`
Liste toutes les locations.

### `GET /locations/{location_id}`
Retourne une location.

### `POST /locations`
Cree une location.

Body:
```json
{
  "id_client": 1,
  "id_vehicule": 2,
  "id_utilisateur": 1,
  "date_debut": "2026-03-10",
  "date_fin": "2026-03-12"
}
```

Regles appliquees:
- Vehicule doit etre `disponible` (US5/US6)
- Refus de chevauchement avec location active (US6)
- `prix_total` calcule automatiquement (US8)
- Vehicule passe a `loue` a la creation (US7)

Reponse `201`:
```json
{
  "id_location": 10,
  "date_debut": "2026-03-10",
  "date_fin": "2026-03-12",
  "prix_total": 135.0,
  "statut": "active",
  "id_client": 1,
  "id_vehicule": 2,
  "id_utilisateur": 1
}
```

Erreurs:
- `400` date invalide
- `404` client/vehicule/utilisateur introuvable
- `409` vehicule deja loue / indisponible

### `POST /locations/{location_id}/close`
Cloture une location (US7).

Effets:
- `location.statut` devient `terminee`
- `vehicule.statut` repasse a `disponible`

Reponses:
- `200` cloturee
- `404` introuvable
- `409` deja terminee

### `DELETE /locations/{location_id}`
Supprime une location.

Comportement:
- Si la location etait `active`, le vehicule repasse `disponible`.

Reponses:
- `204` supprimee
- `404` introuvable

## Endpoint Gemini

### `POST /generate`
Endpoint utilitaire de generation de texte via Gemini.

Body:
```json
{
  "prompt": "Donne moi une description de vehicule.",
  "temperature": 0.7
}
```

Reponses:
- `200` succes
- `400` prompt manquant
- `500` erreur fournisseur
