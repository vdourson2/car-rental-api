from datetime import date
from decimal import Decimal

import click
from flask import Flask
from werkzeug.security import generate_password_hash

from .extensions import db
from .models import Client, Location, Utilisateur, Vehicule


def seed_database() -> dict[str, int]:
    inserted = {"utilisateurs": 0, "clients": 0, "vehicules": 0, "locations": 0}

    user_specs = [
        {"identifiant": "admin", "mot_de_passe": "admin123"},
        {"identifiant": "agent01", "mot_de_passe": "agent123"},
    ]
    for spec in user_specs:
        existing = Utilisateur.query.filter_by(identifiant=spec["identifiant"]).first()
        if existing:
            continue
        db.session.add(
            Utilisateur(
                identifiant=spec["identifiant"],
                mot_de_passe=generate_password_hash(spec["mot_de_passe"]),
            )
        )
        inserted["utilisateurs"] += 1

    client_specs = [
        {"nom": "Jean Dupont", "contact": "jean.dupont@example.com", "numero_permis": "DUPONT-001"},
        {"nom": "Marie Lambert", "contact": "marie.lambert@example.com", "numero_permis": "LAMBERT-002"},
        {"nom": "Olivier Martin", "contact": "olivier.martin@example.com", "numero_permis": "MARTIN-003"},
    ]
    for spec in client_specs:
        existing = Client.query.filter_by(numero_permis=spec["numero_permis"]).first()
        if existing:
            continue
        db.session.add(Client(**spec))
        inserted["clients"] += 1

    vehicule_specs = [
        {
            "marque": "Renault",
            "modele": "Clio",
            "immatriculation": "AA-123-AA",
            "prix_par_jour": Decimal("45.00"),
            "statut": "disponible",
        },
        {
            "marque": "Peugeot",
            "modele": "208",
            "immatriculation": "BB-234-BB",
            "prix_par_jour": Decimal("49.00"),
            "statut": "disponible",
        },
        {
            "marque": "Toyota",
            "modele": "Corolla",
            "immatriculation": "CC-345-CC",
            "prix_par_jour": Decimal("62.00"),
            "statut": "disponible",
        },
    ]
    for spec in vehicule_specs:
        existing = Vehicule.query.filter_by(immatriculation=spec["immatriculation"]).first()
        if existing:
            continue
        db.session.add(Vehicule(**spec))
        inserted["vehicules"] += 1

    db.session.commit()

    location_specs = [
        {
            "date_debut": date(2026, 1, 10),
            "date_fin": date(2026, 1, 14),
            "prix_total": Decimal("225.00"),
            "statut": "terminee",
            "client_permis": "DUPONT-001",
            "vehicule_immatriculation": "AA-123-AA",
            "utilisateur_identifiant": "admin",
        },
        {
            "date_debut": date(2026, 2, 3),
            "date_fin": date(2026, 2, 5),
            "prix_total": Decimal("147.00"),
            "statut": "terminee",
            "client_permis": "LAMBERT-002",
            "vehicule_immatriculation": "BB-234-BB",
            "utilisateur_identifiant": "agent01",
        },
    ]
    for spec in location_specs:
        client = Client.query.filter_by(numero_permis=spec["client_permis"]).first()
        vehicule = Vehicule.query.filter_by(immatriculation=spec["vehicule_immatriculation"]).first()
        utilisateur = Utilisateur.query.filter_by(identifiant=spec["utilisateur_identifiant"]).first()

        if not client or not vehicule or not utilisateur:
            continue

        existing = (
            Location.query.filter_by(
                id_client=client.id_client,
                id_vehicule=vehicule.id_vehicule,
                id_utilisateur=utilisateur.id_utilisateur,
                date_debut=spec["date_debut"],
                date_fin=spec["date_fin"],
            ).first()
        )
        if existing:
            continue

        db.session.add(
            Location(
                date_debut=spec["date_debut"],
                date_fin=spec["date_fin"],
                prix_total=spec["prix_total"],
                statut=spec["statut"],
                id_client=client.id_client,
                id_vehicule=vehicule.id_vehicule,
                id_utilisateur=utilisateur.id_utilisateur,
            )
        )
        inserted["locations"] += 1

    db.session.commit()
    return inserted


def register_seed_command(app: Flask) -> None:
    @app.cli.command("seed")
    @click.option("--with-create", is_flag=True, help="Cree les tables depuis les modeles avant le seed.")
    def seed_command(with_create: bool) -> None:
        if with_create:
            db.create_all()
            click.echo("Tables creees avec db.create_all().")

        inserted = seed_database()
        click.echo(
            "Seed termine: "
            f"{inserted['utilisateurs']} utilisateur(s), "
            f"{inserted['clients']} client(s), "
            f"{inserted['vehicules']} vehicule(s), "
            f"{inserted['locations']} location(s) ajoute(s)."
        )
