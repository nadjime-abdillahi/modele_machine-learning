import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

# URL de connexion PostgreSQL (pilote psycopg2)
DATABASE_URL = "postgresql://admin_ml:Daroussi92.@localhost:5432/ml_database"

# Charge les variables du fichier .env
load_dotenv()

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://admin_ml:Daroussi92.@localhost:5432/ml_database",
)

engine = create_engine(DATABASE_URL)
# 1. Création du moteur SQLAlchemy
engine = create_engine(
    DATABASE_URL,
    echo=False,          # Passer à True pour afficher les requêtes SQL dans la console
    pool_pre_ping=True, # Vérifie la validité des connexions dans le pool
)
print("good")
# 2. Fabrique de sessions
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 3. Classe Base v2 pour tous les modèles ORM
class Base(DeclarativeBase):
    pass

# 4. Dépendance FastAPI pour obtenir une session DB par requête
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()