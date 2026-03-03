from app.extensions import db
from app.models import Utilisateur


class UtilisateurRepository:
    def list_all(self) -> list[Utilisateur]:
        return Utilisateur.query.order_by(Utilisateur.id_utilisateur.asc()).all()

    def get_by_id(self, utilisateur_id: int) -> Utilisateur | None:
        return Utilisateur.query.get(utilisateur_id)

    def get_by_identifiant(self, identifiant: str) -> Utilisateur | None:
        return Utilisateur.query.filter_by(identifiant=identifiant).first()

    def add(self, utilisateur: Utilisateur) -> Utilisateur:
        db.session.add(utilisateur)
        db.session.commit()
        return utilisateur

    def commit(self) -> None:
        db.session.commit()

    def delete(self, utilisateur: Utilisateur) -> None:
        db.session.delete(utilisateur)
        db.session.commit()
