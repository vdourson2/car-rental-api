# Scope réduit – Application de gestion de location de voitures

## 1. Objectif

Développer une application simple permettant de gérer la location de voitures pour une petite agence.  
Ce scope correspond à un MVP ou à un projet académique.

---

## 2. Requirements fonctionnels

### RF1 – Gestion des véhicules

- Le système doit permettre d’ajouter et de consulter des véhicules.
- Chaque véhicule doit contenir les informations suivantes :
  - Marque
  - Modèle
  - Immatriculation
  - Prix par jour
  - Statut (disponible / loué)

### RF2 – Gestion des clients

- Le système doit permettre de créer et consulter des clients.
- Chaque client doit contenir :
  - Nom
  - Coordonnées de contact
  - Numéro de permis de conduire

### RF3 – Gestion des locations

- Le système doit permettre de créer une location associant un client et un véhicule.
- Le système doit empêcher la location d’un véhicule déjà loué.
- Les dates de début et de fin de location doivent être enregistrées.

### RF4 – Calcul du prix

- Le système doit calculer automatiquement le prix total de la location en fonction du nombre de jours.

---

## 3. Requirements non fonctionnels

### RNF1 – Sécurité

- L’accès à l’application doit être protégé par une authentification simple.

### RNF2 – Simplicité d’utilisation

- L’interface doit être simple et intuitive.
- Aucune formation préalable ne doit être nécessaire pour utiliser l’application.

### RNF3 – Persistance des données

- Les données doivent être stockées de manière persistante dans une base de données.

---

## 4. Hors scope

Les fonctionnalités suivantes sont explicitement exclues :

- Paiement en ligne
- Facturation détaillée
- Gestion de maintenance des véhicules
- Gestion avancée des rôles utilisateurs
- Application mobile dédiée
