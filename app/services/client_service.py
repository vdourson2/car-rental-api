from sqlalchemy.exc import IntegrityError

from app.models import Client
from app.repositories import ClientRepository

from .exceptions import ConflictError, NotFoundError, ValidationError


class ClientService:
    def __init__(self, repository: ClientRepository):
        self.repository = repository

    def list_clients(self) -> list[Client]:
        return self.repository.list_all()

    def get_client(self, client_id: int) -> Client:
        client = self.repository.get_by_id(client_id)
        if not client:
            raise NotFoundError("Client introuvable.")
        return client

    def create_client(self, data: dict) -> Client:
        nom = (data.get("nom") or "").strip()
        contact = (data.get("contact") or "").strip()
        numero_permis = (data.get("numero_permis") or "").strip()
        if not nom or not contact or not numero_permis:
            raise ValidationError("nom, contact et numero_permis sont obligatoires.")

        client = Client(nom=nom, contact=contact, numero_permis=numero_permis)
        try:
            return self.repository.add(client)
        except IntegrityError as exc:
            raise ConflictError("numero_permis deja utilise.") from exc

    def update_client(self, client_id: int, data: dict) -> Client:
        client = self.get_client(client_id)

        if "nom" in data:
            nom = (data.get("nom") or "").strip()
            if not nom:
                raise ValidationError("nom ne peut pas etre vide.")
            client.nom = nom
        if "contact" in data:
            contact = (data.get("contact") or "").strip()
            if not contact:
                raise ValidationError("contact ne peut pas etre vide.")
            client.contact = contact
        if "numero_permis" in data:
            numero_permis = (data.get("numero_permis") or "").strip()
            if not numero_permis:
                raise ValidationError("numero_permis ne peut pas etre vide.")
            client.numero_permis = numero_permis

        try:
            self.repository.commit()
            return client
        except IntegrityError as exc:
            raise ConflictError("numero_permis deja utilise.") from exc

    def delete_client(self, client_id: int) -> None:
        client = self.get_client(client_id)
        self.repository.delete(client)
