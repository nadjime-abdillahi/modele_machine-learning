import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker


# Si SQLALCHEMY_DATABASE_URI est définie (ex: dans la CI), on l'utilise, sinon SQLite en mémoire pour les tests
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///:memory:")

# SQLite requiert un paramètre spécial pour le multi-threading
connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}

engine = create_engine(DATABASE_URL, connect_args=connect_args)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
