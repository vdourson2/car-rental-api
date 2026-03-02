# Diagramme d’entités – Application de gestion de location de voitures

```mermaid
erDiagram
    VEHICULE {
        int id_vehicule
        string marque
        string modele
        string immatriculation
        float prix_par_jour
        string statut
    }

    CLIENT {
        int id_client
        string nom
        string contact
        string numero_permis
    }

    LOCATION {
        int id_location
        date date_debut
        date date_fin
        float prix_total
    }

    UTILISATEUR {
        int id_utilisateur
        string identifiant
        string mot_de_passe
    }

    CLIENT ||--o{ LOCATION : "effectue"
    VEHICULE ||--o{ LOCATION : "concerne"
    UTILISATEUR ||--o{ LOCATION : "cree"
