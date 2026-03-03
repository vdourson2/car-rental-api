from datetime import date
from decimal import Decimal

from sqlalchemy import CheckConstraint, Index

from .extensions import db


class Utilisateur(db.Model):
    __tablename__ = "utilisateur"

    id_utilisateur = db.Column(db.Integer, primary_key=True)
    identifiant = db.Column(db.String(50), nullable=False, unique=True)
    mot_de_passe = db.Column(db.String(255), nullable=False)

    locations = db.relationship("Location", back_populates="utilisateur")

    def to_dict(self) -> dict:
        return {
            "id_utilisateur": self.id_utilisateur,
            "identifiant": self.identifiant,
        }


class Client(db.Model):
    __tablename__ = "client"

    id_client = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), nullable=False)
    contact = db.Column(db.String(100), nullable=False)
    numero_permis = db.Column(db.String(50), nullable=False, unique=True)

    locations = db.relationship("Location", back_populates="client")

    def to_dict(self) -> dict:
        return {
            "id_client": self.id_client,
            "nom": self.nom,
            "contact": self.contact,
            "numero_permis": self.numero_permis,
        }


class Vehicule(db.Model):
    __tablename__ = "vehicule"
    __table_args__ = (
        CheckConstraint("prix_par_jour > 0", name="chk_vehicule_prix_positif"),
        CheckConstraint("statut IN ('disponible', 'loue')", name="chk_vehicule_statut"),
    )

    id_vehicule = db.Column(db.Integer, primary_key=True)
    marque = db.Column(db.String(50), nullable=False)
    modele = db.Column(db.String(50), nullable=False)
    immatriculation = db.Column(db.String(20), nullable=False, unique=True)
    prix_par_jour = db.Column(db.Numeric(10, 2), nullable=False)
    statut = db.Column(db.String(20), nullable=False, default="disponible", server_default="disponible")

    locations = db.relationship("Location", back_populates="vehicule")

    def to_dict(self) -> dict:
        return {
            "id_vehicule": self.id_vehicule,
            "marque": self.marque,
            "modele": self.modele,
            "immatriculation": self.immatriculation,
            "prix_par_jour": float(self.prix_par_jour),
            "statut": self.statut,
        }


class Location(db.Model):
    __tablename__ = "location"
    __table_args__ = (
        CheckConstraint("date_fin >= date_debut", name="chk_location_dates"),
        CheckConstraint("prix_total >= 0", name="chk_location_prix_total"),
        CheckConstraint("statut IN ('active', 'terminee')", name="chk_location_statut"),
        Index("idx_location_client", "id_client"),
        Index("idx_location_vehicule", "id_vehicule"),
        Index("idx_location_dates", "date_debut", "date_fin"),
    )

    id_location = db.Column(db.Integer, primary_key=True)
    date_debut = db.Column(db.Date, nullable=False)
    date_fin = db.Column(db.Date, nullable=False)
    prix_total = db.Column(db.Numeric(10, 2), nullable=False, default=Decimal("0.00"), server_default="0")
    statut = db.Column(db.String(20), nullable=False, default="active", server_default="active")

    id_client = db.Column(
        db.Integer,
        db.ForeignKey("client.id_client", ondelete="RESTRICT"),
        nullable=False,
    )
    id_vehicule = db.Column(
        db.Integer,
        db.ForeignKey("vehicule.id_vehicule", ondelete="RESTRICT"),
        nullable=False,
    )
    id_utilisateur = db.Column(
        db.Integer,
        db.ForeignKey("utilisateur.id_utilisateur", ondelete="RESTRICT"),
        nullable=False,
    )

    client = db.relationship("Client", back_populates="locations")
    vehicule = db.relationship("Vehicule", back_populates="locations")
    utilisateur = db.relationship("Utilisateur", back_populates="locations")

    def calculer_prix_total(self) -> Decimal:
        if not self.vehicule:
            raise ValueError("Un vehicule est requis pour calculer le prix total.")
        if not self.date_debut or not self.date_fin:
            raise ValueError("Les dates de debut et fin sont requises.")
        if self.date_fin < self.date_debut:
            raise ValueError("La date de fin doit etre superieure ou egale a la date de debut.")

        nb_jours = max((self.date_fin - self.date_debut).days, 0) + 1
        prix = Decimal(str(self.vehicule.prix_par_jour)) * Decimal(nb_jours)
        self.prix_total = prix.quantize(Decimal("0.01"))
        return self.prix_total

    def est_active(self, reference: date | None = None) -> bool:
        ref = reference or date.today()
        return self.statut == "active" and self.date_debut <= ref <= self.date_fin

    def to_dict(self) -> dict:
        return {
            "id_location": self.id_location,
            "date_debut": self.date_debut.isoformat(),
            "date_fin": self.date_fin.isoformat(),
            "prix_total": float(self.prix_total),
            "statut": self.statut,
            "id_client": self.id_client,
            "id_vehicule": self.id_vehicule,
            "id_utilisateur": self.id_utilisateur,
        }
