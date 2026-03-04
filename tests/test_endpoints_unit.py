import unittest
from types import SimpleNamespace
from unittest.mock import Mock, patch

from sqlalchemy.exc import IntegrityError

from app import create_app
from app.services import NotFoundError


class DummyEntity:
    def __init__(self, **data):
        self._data = data
        for key, value in data.items():
            setattr(self, key, value)

    def to_dict(self):
        return self._data


class EndpointsUnitTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.config.update(TESTING=True)
        self.client = self.app.test_client()

        import app.routes as routes

        self.routes = routes
        self.client_service = Mock()
        self.vehicule_service = Mock()
        self.utilisateur_service = Mock()
        self.location_service = Mock()

        self.patchers = [
            patch.object(routes, "client_service", self.client_service),
            patch.object(routes, "vehicule_service", self.vehicule_service),
            patch.object(routes, "utilisateur_service", self.utilisateur_service),
            patch.object(routes, "location_service", self.location_service),
        ]
        for patcher in self.patchers:
            patcher.start()

    def tearDown(self):
        for patcher in reversed(self.patchers):
            patcher.stop()

    def test_openapi_endpoints_exposed(self):
        for path in ("/openapi.json", "/api/openapi.json", "/api"):
            response = self.client.get(path)
            self.assertEqual(response.status_code, 200)
            payload = response.get_json()
            self.assertIn("paths", payload)
            self.assertIn("/api/vehicles", payload["paths"])

    def test_health_endpoint(self):
        response = self.client.get("/api/health")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), {"status": "ok"})

    def test_vehicles_endpoints(self):
        self.vehicule_service.list_vehicules.return_value = [
            DummyEntity(
                id_vehicule=1,
                marque="Renault",
                modele="Clio",
                immatriculation="AA-123-AA",
                prix_par_jour=45.0,
                statut="disponible",
            )
        ]
        self.vehicule_service.get_vehicule.return_value = DummyEntity(id_vehicule=1)
        self.vehicule_service.create_vehicule.return_value = DummyEntity(
            id_vehicule=2, marque="Peugeot"
        )
        self.vehicule_service.update_vehicule.return_value = DummyEntity(
            id_vehicule=1, statut="loue"
        )

        self.assertEqual(self.client.get("/api/vehicles").status_code, 200)
        self.assertEqual(self.client.get("/api/vehicles/1").status_code, 200)
        self.assertEqual(
            self.client.post("/api/vehicles", json={"marque": "Peugeot"}).status_code,
            201,
        )
        self.assertEqual(
            self.client.put("/api/vehicles/1", json={"statut": "loue"}).status_code, 200
        )
        self.assertEqual(self.client.delete("/api/vehicles/1").status_code, 204)
        self.vehicule_service.delete_vehicule.assert_called_once_with(1)

    def test_legacy_cars_endpoint(self):
        self.vehicule_service.list_vehicules.return_value = [
            DummyEntity(
                id_vehicule=8, marque="Toyota", modele="Yaris", statut="disponible"
            ),
            DummyEntity(id_vehicule=9, marque="Ford", modele="Focus", statut="loue"),
        ]
        response = self.client.get("/api/cars")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.get_json(),
            [
                {"id": 8, "model": "Toyota Yaris", "available": True},
                {"id": 9, "model": "Ford Focus", "available": False},
            ],
        )

    def test_clients_endpoints(self):
        self.client_service.list_clients.return_value = [
            DummyEntity(id_client=1, nom="Jean")
        ]
        self.client_service.get_client.return_value = DummyEntity(
            id_client=1, nom="Jean"
        )
        self.client_service.create_client.return_value = DummyEntity(
            id_client=2, nom="Marie"
        )
        self.client_service.update_client.return_value = DummyEntity(
            id_client=1, nom="Jean Maj"
        )

        self.assertEqual(self.client.get("/api/clients").status_code, 200)
        self.assertEqual(self.client.get("/api/clients/1").status_code, 200)
        self.assertEqual(
            self.client.post("/api/clients", json={"nom": "Marie"}).status_code, 201
        )
        self.assertEqual(
            self.client.put("/api/clients/1", json={"nom": "Jean Maj"}).status_code, 200
        )
        self.assertEqual(self.client.delete("/api/clients/1").status_code, 204)
        self.client_service.delete_client.assert_called_once_with(1)

    def test_users_and_login_endpoints(self):
        self.utilisateur_service.list_utilisateurs.return_value = [
            DummyEntity(id_utilisateur=1, identifiant="admin")
        ]
        self.utilisateur_service.get_utilisateur.return_value = DummyEntity(
            id_utilisateur=1, identifiant="admin"
        )
        self.utilisateur_service.create_utilisateur.return_value = DummyEntity(
            id_utilisateur=2, identifiant="agent01"
        )
        self.utilisateur_service.update_utilisateur.return_value = DummyEntity(
            id_utilisateur=1, identifiant="admin2"
        )
        self.utilisateur_service.authenticate.return_value = DummyEntity(
            id_utilisateur=1, identifiant="admin"
        )

        self.assertEqual(self.client.get("/api/users").status_code, 200)
        self.assertEqual(self.client.get("/api/users/1").status_code, 200)
        self.assertEqual(
            self.client.post(
                "/api/users", json={"identifiant": "agent01", "mot_de_passe": "secret"}
            ).status_code,
            201,
        )
        self.assertEqual(
            self.client.put("/api/users/1", json={"identifiant": "admin2"}).status_code,
            200,
        )
        self.assertEqual(self.client.delete("/api/users/1").status_code, 204)

        login_response = self.client.post(
            "/api/auth/login", json={"identifiant": "admin", "mot_de_passe": "secret"}
        )
        self.assertEqual(login_response.status_code, 200)
        self.assertIn("utilisateur", login_response.get_json())

    def test_locations_endpoints(self):
        self.location_service.list_locations.return_value = [DummyEntity(id_location=1)]
        self.location_service.get_location.return_value = DummyEntity(id_location=1)
        self.location_service.create_location.return_value = DummyEntity(id_location=2)
        self.location_service.close_location.return_value = DummyEntity(
            id_location=1, statut="terminee"
        )

        self.assertEqual(self.client.get("/api/locations").status_code, 200)
        self.assertEqual(self.client.get("/api/locations/1").status_code, 200)
        self.assertEqual(
            self.client.post(
                "/api/locations",
                json={
                    "date_debut": "2026-01-10",
                    "date_fin": "2026-01-12",
                    "id_client": 1,
                    "id_vehicule": 1,
                    "id_utilisateur": 1,
                },
            ).status_code,
            201,
        )
        self.assertEqual(self.client.post("/api/locations/1/close").status_code, 200)
        self.assertEqual(self.client.delete("/api/locations/1").status_code, 204)
        self.location_service.delete_location.assert_called_once_with(1)

    def test_generate_success(self):
        class FakeModel:
            def __init__(self, **_kwargs):
                pass

            def generate_content(self, _prompt):
                return SimpleNamespace(text="Texte genere")

        with patch.object(self.routes.genai, "GenerativeModel", FakeModel):
            response = self.client.post(
                "/api/generate", json={"prompt": "Bonjour", "temperature": 0.2}
            )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), {"response": "Texte genere"})

    def test_generate_validation_and_error(self):
        response = self.client.post("/api/generate", json={})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.get_json(), {"error": "Prompt is required"})

        class FailingModel:
            def __init__(self, **_kwargs):
                pass

            def generate_content(self, _prompt):
                raise RuntimeError("boom")

        with patch.object(self.routes.genai, "GenerativeModel", FailingModel):
            response = self.client.post("/api/generate", json={"prompt": "test"})
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.get_json(), {"error": "boom"})

    def test_models_endpoint(self):
        fake_models = [
            SimpleNamespace(
                name="models/gemini-2.5-flash",
                supported_generation_methods=["generateContent"],
            ),
            SimpleNamespace(name="models/legacy"),
        ]
        with patch.object(self.routes.genai, "list_models", return_value=fake_models):
            response = self.client.get("/api/models")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.get_json(),
            [
                {
                    "name": "models/gemini-2.5-flash",
                    "supported_generation_methods": ["generateContent"],
                },
                {"name": "models/legacy", "supported_generation_methods": []},
            ],
        )

    def test_service_error_handler(self):
        self.vehicule_service.get_vehicule.side_effect = NotFoundError(
            "Vehicule introuvable."
        )
        response = self.client.get("/api/vehicles/999")
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.get_json(), {"error": "Vehicule introuvable."})

    def test_integrity_error_handler(self):
        self.vehicule_service.create_vehicule.side_effect = IntegrityError(
            "stmt", "params", Exception("db")
        )
        response = self.client.post("/api/vehicles", json={"marque": "X"})
        self.assertEqual(response.status_code, 409)
        self.assertEqual(
            response.get_json(), {"error": "Contrainte base de donnees violee."}
        )


if __name__ == "__main__":
    unittest.main()
