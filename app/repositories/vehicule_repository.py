from app.extensions import db
from app.models import Vehicule


class VehiculeRepository:
    def list_all(self) -> list[Vehicule]:
        return Vehicule.query.order_by(Vehicule.id_vehicule.asc()).all()

    def get_by_id(self, vehicule_id: int) -> Vehicule | None:
        return Vehicule.query.get(vehicule_id)

    def add(self, vehicule: Vehicule) -> Vehicule:
        db.session.add(vehicule)
        db.session.commit()
        return vehicule

    def commit(self) -> None:
        db.session.commit()

    def delete(self, vehicule: Vehicule) -> None:
        db.session.delete(vehicule)
        db.session.commit()
