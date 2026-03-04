import os


class Config:
    raw_database_url = os.getenv(
        "DATABASE_URL",
        "postgresql://car_rental:car_rental@localhost:5432/car_rental",
    )
    if raw_database_url.startswith("postgresql://"):
        SQLALCHEMY_DATABASE_URI = raw_database_url.replace(
            "postgresql://", "postgresql+psycopg://", 1
        )
    else:
        SQLALCHEMY_DATABASE_URI = raw_database_url
    SQLALCHEMY_TRACK_MODIFICATIONS = False
