from datetime import date

from app.extensions import db
from app.models import Location


class LocationRepository:
    def list_all(self) -> list[Location]:
        return Location.query.order_by(Location.id_location.asc()).all()

    def get_by_id(self, location_id: int) -> Location | None:
        return Location.query.get(location_id)

    def add(self, location: Location) -> Location:
        db.session.add(location)
        db.session.commit()
        return location

    def commit(self) -> None:
        db.session.commit()

    def delete(self, location: Location) -> None:
        db.session.delete(location)
        db.session.commit()

    def has_overlapping_active_location(self, id_vehicule: int, date_debut: date, date_fin: date) -> bool:
        overlapping = (
            Location.query.filter(Location.id_vehicule == id_vehicule)
            .filter(Location.statut == "active")
            .filter(Location.date_debut <= date_fin)
            .filter(Location.date_fin >= date_debut)
            .first()
        )
        return overlapping is not None
