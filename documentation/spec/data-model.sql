-- =========================
-- Table UTILISATEUR
-- =========================
CREATE TABLE utilisateur (
    id_utilisateur SERIAL PRIMARY KEY,
    identifiant VARCHAR(50) NOT NULL UNIQUE,
    mot_de_passe VARCHAR(255) NOT NULL
);

-- =========================
-- Table CLIENT
-- =========================
CREATE TABLE client (
    id_client SERIAL PRIMARY KEY,
    nom VARCHAR(100) NOT NULL,
    contact VARCHAR(100) NOT NULL,
    numero_permis VARCHAR(50) NOT NULL UNIQUE
);

-- =========================
-- Table VEHICULE
-- =========================
CREATE TABLE vehicule (
    id_vehicule SERIAL PRIMARY KEY,
    marque VARCHAR(50) NOT NULL,
    modele VARCHAR(50) NOT NULL,
    immatriculation VARCHAR(20) NOT NULL UNIQUE,
    prix_par_jour NUMERIC(10,2) NOT NULL CHECK (prix_par_jour > 0),
    statut VARCHAR(20) NOT NULL CHECK (statut IN ('disponible', 'loue'))
);

-- =========================
-- Table LOCATION
-- =========================
CREATE TABLE location (
    id_location SERIAL PRIMARY KEY,
    date_debut DATE NOT NULL,
    date_fin DATE NOT NULL,
    prix_total NUMERIC(10,2) NOT NULL CHECK (prix_total >= 0),

    id_client INT NOT NULL,
    id_vehicule INT NOT NULL,
    id_utilisateur INT NOT NULL,

    CONSTRAINT fk_client
        FOREIGN KEY (id_client)
        REFERENCES client(id_client)
        ON DELETE RESTRICT,

    CONSTRAINT fk_vehicule
        FOREIGN KEY (id_vehicule)
        REFERENCES vehicule(id_vehicule)
        ON DELETE RESTRICT,

    CONSTRAINT fk_utilisateur
        FOREIGN KEY (id_utilisateur)
        REFERENCES utilisateur(id_utilisateur)
        ON DELETE RESTRICT,

    CONSTRAINT chk_dates
        CHECK (date_fin >= date_debut)
);

-- =========================
-- Index utiles
-- =========================
CREATE INDEX idx_location_client ON location(id_client);
CREATE INDEX idx_location_vehicule ON location(id_vehicule);
CREATE INDEX idx_location_dates ON location(date_debut, date_fin);