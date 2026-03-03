from sqlalchemy.exc import IntegrityError
from werkzeug.security import check_password_hash, generate_password_hash

from app.models import Utilisateur
from app.repositories import UtilisateurRepository

from .exceptions import AuthenticationError, ConflictError, NotFoundError, ValidationError


class UtilisateurService:
    def __init__(self, repository: UtilisateurRepository):
        self.repository = repository

    def list_utilisateurs(self) -> list[Utilisateur]:
        return self.repository.list_all()

    def get_utilisateur(self, utilisateur_id: int) -> Utilisateur:
        utilisateur = self.repository.get_by_id(utilisateur_id)
        if not utilisateur:
            raise NotFoundError("Utilisateur introuvable.")
        return utilisateur

    def create_utilisateur(self, data: dict) -> Utilisateur:
        identifiant = (data.get("identifiant") or "").strip()
        mot_de_passe = (data.get("mot_de_passe") or "").strip()
        if not identifiant or not mot_de_passe:
            raise ValidationError("identifiant et mot_de_passe sont obligatoires.")

        utilisateur = Utilisateur(
            identifiant=identifiant,
            mot_de_passe=generate_password_hash(mot_de_passe),
        )
        try:
            return self.repository.add(utilisateur)
        except IntegrityError as exc:
            raise ConflictError("identifiant deja utilise.") from exc

    def update_utilisateur(self, utilisateur_id: int, data: dict) -> Utilisateur:
        utilisateur = self.get_utilisateur(utilisateur_id)

        if "identifiant" in data:
            identifiant = (data.get("identifiant") or "").strip()
            if not identifiant:
                raise ValidationError("identifiant ne peut pas etre vide.")
            utilisateur.identifiant = identifiant

        if "mot_de_passe" in data:
            mot_de_passe = (data.get("mot_de_passe") or "").strip()
            if not mot_de_passe:
                raise ValidationError("mot_de_passe ne peut pas etre vide.")
            utilisateur.mot_de_passe = generate_password_hash(mot_de_passe)

        try:
            self.repository.commit()
            return utilisateur
        except IntegrityError as exc:
            raise ConflictError("identifiant deja utilise.") from exc

    def delete_utilisateur(self, utilisateur_id: int) -> None:
        utilisateur = self.get_utilisateur(utilisateur_id)
        self.repository.delete(utilisateur)

    def authenticate(self, data: dict) -> Utilisateur:
        identifiant = (data.get("identifiant") or "").strip()
        mot_de_passe = (data.get("mot_de_passe") or "").strip()
        if not identifiant or not mot_de_passe:
            raise ValidationError("identifiant et mot_de_passe sont obligatoires.")

        utilisateur = self.repository.get_by_identifiant(identifiant)
        if not utilisateur or not check_password_hash(utilisateur.mot_de_passe, mot_de_passe):
            raise AuthenticationError("Identifiants invalides.")

        return utilisateur
