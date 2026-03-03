from app.extensions import db
from app.models import Client


class ClientRepository:
    def list_all(self) -> list[Client]:
        return Client.query.order_by(Client.id_client.asc()).all()

    def get_by_id(self, client_id: int) -> Client | None:
        return Client.query.get(client_id)

    def add(self, client: Client) -> Client:
        db.session.add(client)
        db.session.commit()
        return client

    def commit(self) -> None:
        db.session.commit()

    def delete(self, client: Client) -> None:
        db.session.delete(client)
        db.session.commit()
