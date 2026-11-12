
import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    SECRET_KEY = os.getenv(
        "SECRET_KEY",
        "dev-secret-change-locally"
    )

    
    DATABASE_URL = os.getenv(
        "DATABASE_URL",
        "sqlite:///smart_url_shortener.db"
    )

    # Use psycopg2 driver for PostgreSQL
    if DATABASE_URL.startswith("postgres://"):
        DATABASE_URL = DATABASE_URL.replace(
            "postgres://",
            "postgresql+psycopg2://",
            1
        )
    elif DATABASE_URL.startswith("postgresql://"):
        DATABASE_URL = DATABASE_URL.replace(
           "postgresql://",
           "postgresql+psycopg2://",
            1
        )

    SQLALCHEMY_DATABASE_URI = DATABASE_URL


    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"
