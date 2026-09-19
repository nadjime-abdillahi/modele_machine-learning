from typing import List
from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session
import sys
from pathlib import Path
from .database import engine, Base, get_db
import schemas
from . import models
from .ml_model import predict

sys.path.append(str(Path(__file__).resolve().parent.parent))
# Crée les tables au démarrage s'il ne s'agit pas d'un système de migration automatisé
Base.metadata.create_all(bind=engine)

app = FastAPI(title="API ML avec PostgreSQL")

# Déclaration de la route racine
@app.get("/")
def read_root():
    return {"message": "API de Machine Learning opérationnelle"}

# --- 1. CRÉER UNE ENTRÉE (INSERT) ---
@app.post("/predictions/", response_model=schemas.PredictionResponse, status_code=status.HTTP_201_CREATED)
def create_prediction_log(
        prediction_data: schemas.PredictionCreate,
        db: Session = Depends(get_db)
):
    # instanciation du modèle ORM
    db_item = models.PredictionLog(**prediction_data.model_dump())

    db.add(db_item)
    db.commit()
    db.refresh(db_item)  # Récupère l'ID généré et la date created_at
    return db_item


# --- 2. LIRE DES ENTRÉES (SELECT MULTIPLE) ---
@app.get("/predictions/", response_model=List[schemas.PredictionResponse])
def read_predictions(
        skip: int = 0,
        limit: int = 10,
        db: Session = Depends(get_db)
):
    # Synstaxe SQLAlchemy v2 : select()
    stmt = select(models.PredictionLog).offset(skip).limit(limit)
    predictions = db.scalars(stmt).all()
    return predictions


# --- 3. LIRE UNE ENTRÉE PAR ID (SELECT UNIQUE) ---
@app.get("/predictions/{prediction_id}", response_model=schemas.PredictionResponse)
def read_prediction_by_id(
        prediction_id: int,
        db: Session = Depends(get_db)
):
    stmt = select(models.PredictionLog).where(models.PredictionLog.id == prediction_id)
    prediction = db.scalar(stmt)

    if prediction is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Prédiction non trouvée"
        )
    return prediction

# --- 4. METTRE À JOUR UNE ENTRÉE (UPDATE) ---
@app.put("/predictions/{prediction_id}", response_model=schemas.PredictionResponse)
def update_prediction(
        prediction_id: int,
        prediction_data: schemas.PredictionCreate,
        db: Session = Depends(get_db)
):
    stmt = select(models.PredictionLog).where(models.PredictionLog.id == prediction_id)
    db_item = db.scalar(stmt)

    if db_item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Prédiction non trouvée"
        )

    # Mise à jour dynamique des attributs de l'objet SQLAlchemy
    for key, value in prediction_data.model_dump().items():
        setattr(db_item, key, value)

    db.commit()
    db.refresh(db_item)
    return db_item


# --- 5. SUPPRIMER UNE ENTRÉE (DELETE) ---
@app.delete("/predictions/{prediction_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_prediction(
        prediction_id: int,
        db: Session = Depends(get_db)
):
    stmt = select(models.PredictionLog).where(models.PredictionLog.id == prediction_id)
    db_item = db.scalar(stmt)

    if db_item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Prédiction non trouvée"
        )

    db.delete(db_item)
    db.commit()
    return None