from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field

class PredictionCreate(BaseModel):
    surface_m2: float = Field(..., examples=[65.0])
    nb_pieces: int = Field(..., examples=[3])
    zone: str = Field(..., examples=["centre"])
    prediction: int
    probability: Optional[float] = None

class PredictionResponse(PredictionCreate):
    id: int
    created_at: datetime

    # Permet de convertir automatiquement un objet ORM SQLAlchemy en schéma Pydantic
    model_config = ConfigDict(from_attributes=True)