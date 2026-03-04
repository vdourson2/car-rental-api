from datetime import datetime

from app.extensions import db
from app.models import Location
from app.repositories import (
    ClientRepository,
    LocationRepository,
    UtilisateurRepository,
    VehiculeRepository,
)

from .exceptions import ConflictError, NotFoundError, ValidationError


class LocationService:
    def __init__(
        self,
        location_repository: LocationRepository,
        client_repository: ClientRepository,
        vehicule_repository: VehiculeRepository,
        utilisateur_repository: UtilisateurRepository,
    ):
        self.location_repository = location_repository
        self.client_repository = client_repository
        self.vehicule_repository = vehicule_repository
        self.utilisateur_repository = utilisateur_repository

    def list_locations(self) -> list[Location]:
        return self.location_repository.list_all()

    def get_location(self, location_id: int) -> Location:
        location = self.location_repository.get_by_id(location_id)
        if not location:
            raise NotFoundError("Location introuvable.")
        return location

    def create_location(self, data: dict) -> Location:
        id_client = data.get("id_client")
        id_vehicule = data.get("id_vehicule")
        id_utilisateur = data.get("id_utilisateur")
        date_debut = self._parse_date(data.get("date_debut"), "date_debut")
        date_fin = self._parse_date(data.get("date_fin"), "date_fin")

        if date_fin < date_debut:
            raise ValidationError(
                "date_fin doit etre superieure ou egale a date_debut."
            )

        client = self.client_repository.get_by_id(id_client)
        if not client:
            raise NotFoundError("Client introuvable.")

        vehicule = self.vehicule_repository.get_by_id(id_vehicule)
        if not vehicule:
            raise NotFoundError("Vehicule introuvable.")

        utilisateur = self.utilisateur_repository.get_by_id(id_utilisateur)
        if not utilisateur:
            raise NotFoundError("Utilisateur introuvable.")

        if vehicule.statut != "disponible":
            raise ConflictError("Vehicule deja loue.")

        if self.location_repository.has_overlapping_active_location(
            vehicule.id_vehicule, date_debut, date_fin
        ):
            raise ConflictError("Vehicule indisponible sur cet intervalle.")

        location = Location(
            date_debut=date_debut,
            date_fin=date_fin,
            client=client,
            vehicule=vehicule,
            utilisateur=utilisateur,
            statut="active",
        )
        location.calculer_prix_total()
        vehicule.statut = "loue"

        db.session.add(location)
        db.session.commit()
        return location

    def close_location(self, location_id: int) -> Location:
        location = self.get_location(location_id)
        if location.statut == "terminee":
            raise ConflictError("Location deja terminee.")

        location.statut = "terminee"
        location.vehicule.statut = "disponible"
        self.location_repository.commit()
        return location

    def delete_location(self, location_id: int) -> None:
        location = self.get_location(location_id)
        if location.statut == "active":
            location.vehicule.statut = "disponible"
        self.location_repository.delete(location)

    @staticmethod
    def _parse_date(raw_date: object, field_name: str):
        if not raw_date:
            raise ValidationError(f"{field_name} est obligatoire.")
        try:
            return datetime.strptime(str(raw_date), "%Y-%m-%d").date()
        except ValueError:
            raise ValidationError(
                f"{field_name} doit etre au format YYYY-MM-DD."
            ) from None
