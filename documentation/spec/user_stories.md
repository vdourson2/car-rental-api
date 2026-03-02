# User Stories – Application de gestion de location de voitures

## 1. Objectif

Décrire les fonctionnalités principales de l’application sous forme de user stories, afin de faciliter la compréhension des besoins et la planification du développement.

---

## 2. User Stories – Gestion des véhicules

### US1 – Ajouter un véhicule

**En tant qu’** administrateur  
**Je veux** ajouter un véhicule dans le système  
**Afin de** pouvoir le proposer à la location.

**Critères d’acceptation :**

- Le formulaire permet de saisir la marque, le modèle, l’immatriculation et le prix par jour.
- Le véhicule est créé avec le statut « disponible ».

---

### US2 – Consulter la liste des véhicules

**En tant qu’** administrateur  
**Je veux** consulter la liste des véhicules  
**Afin de** connaître leur disponibilité.

**Critères d’acceptation :**

- Tous les véhicules sont affichés avec leur statut.
- Un véhicule loué n’est pas marqué comme disponible.

---

## 3. User Stories – Gestion des clients

### US3 – Ajouter un client

**En tant qu’** administrateur  
**Je veux** créer un client  
**Afin de** pouvoir lui attribuer une location.

**Critères d’acceptation :**

- Le nom, les coordonnées et le numéro de permis sont obligatoires.
- Le client est enregistré dans la base de données.

---

### US4 – Consulter un client

**En tant qu’** administrateur  
**Je veux** consulter les informations d’un client  
**Afin de** vérifier son identité avant une location.

**Critères d’acceptation :**

- Les informations du client sont affichées clairement.
- Les données sont en lecture seule.

---

## 4. User Stories – Gestion des locations

### US5 – Créer une location

**En tant qu’** administrateur  
**Je veux** créer une location pour un client et un véhicule  
**Afin de** formaliser la location.

**Critères d’acceptation :**

- Un client et un véhicule doivent être sélectionnés.
- Les dates de début et de fin doivent être renseignées.
- Le véhicule doit être disponible au moment de la création.

---

### US6 – Empêcher la double location

**En tant qu’** système  
**Je veux** empêcher la location d’un véhicule déjà loué  
**Afin d’** éviter les conflits de réservation.

**Critères d’acceptation :**

- Le système refuse la création si le véhicule est déjà loué.
- Un message d’erreur explicite est affiché.

---

### US7 – Clôturer une location

**En tant qu’** administrateur  
**Je veux** terminer une location  
**Afin de** rendre le véhicule de nouveau disponible.

**Critères d’acceptation :**

- Le statut du véhicule passe à « disponible ».
- La location est marquée comme terminée.

---

## 5. User Stories – Calcul du prix

### US8 – Calcul automatique du prix

**En tant qu’** administrateur  
**Je veux** que le prix total soit calculé automatiquement  
**Afin de** éviter les erreurs de calcul.

**Critères d’acceptation :**

- Le prix dépend du nombre de jours de location.
- Le prix est affiché avant validation de la location.

---

## 6. User Stories – Requirements non fonctionnels

### US9 – Authentification simple

**En tant qu’** utilisateur  
**Je veux** m’authentifier pour accéder à l’application  
**Afin de** sécuriser les données.

**Critères d’acceptation :**

- Un identifiant et un mot de passe sont requis.
- L’accès est refusé sans authentification valide.

---

### US10 – Persistance des données

**En tant qu’** administrateur  
**Je veux** que les données soient sauvegardées  
**Afin de** ne pas perdre d’informations en cas de redémarrage.

**Critères d’acceptation :**

- Les données sont stockées dans une base de données.
- Les données restent accessibles après redémarrage du système.

---
