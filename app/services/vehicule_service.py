from decimal import Decimal, InvalidOperation

from sqlalchemy.exc import IntegrityError

from app.models import Vehicule
from app.repositories import VehiculeRepository

from .exceptions import ConflictError, NotFoundError, ValidationError


class VehiculeService:
    def __init__(self, repository: VehiculeRepository):
        self.repository = repository

    def list_vehicules(self) -> list[Vehicule]:
        return self.repository.list_all()

    def get_vehicule(self, vehicule_id: int) -> Vehicule:
        vehicule = self.repository.get_by_id(vehicule_id)
        if not vehicule:
            raise NotFoundError("Vehicule introuvable.")
        return vehicule

    def create_vehicule(self, data: dict) -> Vehicule:
        marque = (data.get("marque") or "").strip()
        modele = (data.get("modele") or "").strip()
        immatriculation = (data.get("immatriculation") or "").strip()
        prix_par_jour = self._parse_positive_decimal(
            data.get("prix_par_jour"), "prix_par_jour"
        )
        statut = (data.get("statut") or "disponible").strip().lower()

        if not marque or not modele or not immatriculation:
            raise ValidationError(
                "marque, modele et immatriculation sont obligatoires."
            )
        if statut not in ("disponible", "loue"):
            raise ValidationError("statut doit etre 'disponible' ou 'loue'.")

        vehicule = Vehicule(
            marque=marque,
            modele=modele,
            immatriculation=immatriculation,
            prix_par_jour=prix_par_jour,
            statut=statut,
        )
        try:
            return self.repository.add(vehicule)
        except IntegrityError as exc:
            raise ConflictError("immatriculation deja utilisee.") from exc

    def update_vehicule(self, vehicule_id: int, data: dict) -> Vehicule:
        vehicule = self.get_vehicule(vehicule_id)

        if "marque" in data:
            marque = (data.get("marque") or "").strip()
            if not marque:
                raise ValidationError("marque ne peut pas etre vide.")
            vehicule.marque = marque
        if "modele" in data:
            modele = (data.get("modele") or "").strip()
            if not modele:
                raise ValidationError("modele ne peut pas etre vide.")
            vehicule.modele = modele
        if "immatriculation" in data:
            immatriculation = (data.get("immatriculation") or "").strip()
            if not immatriculation:
                raise ValidationError("immatriculation ne peut pas etre vide.")
            vehicule.immatriculation = immatriculation
        if "prix_par_jour" in data:
            vehicule.prix_par_jour = self._parse_positive_decimal(
                data.get("prix_par_jour"), "prix_par_jour"
            )
        if "statut" in data:
            statut = (data.get("statut") or "").strip().lower()
            if statut not in ("disponible", "loue"):
                raise ValidationError("statut doit etre 'disponible' ou 'loue'.")
            vehicule.statut = statut

        try:
            self.repository.commit()
            return vehicule
        except IntegrityError as exc:
            raise ConflictError("immatriculation deja utilisee.") from exc

    def delete_vehicule(self, vehicule_id: int) -> None:
        vehicule = self.get_vehicule(vehicule_id)
        self.repository.delete(vehicule)

    @staticmethod
    def _parse_positive_decimal(value: object, field_name: str) -> Decimal:
        try:
            parsed = Decimal(str(value))
        except (InvalidOperation, TypeError):
            raise ValidationError(f"{field_name} doit etre un nombre valide.") from None
        if parsed <= 0:
            raise ValidationError(f"{field_name} doit etre superieur a 0.")
        return parsed.quantize(Decimal("0.01"))
