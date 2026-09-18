from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field

app = FastAPI()


# Schéma d'entrée avec validation Pydantic
class PredictRequest(BaseModel):
    age: int = Field(..., ge=0, le=120, description="L'âge doit être compris entre 0 et 120 ans")
    income: float = Field(..., ge=0.0, description="Le revenu doit être positif")
    credit_score: int = Field(..., ge=300, le=850, description="Score de crédit valide (300-850)")


# Route racine
@app.get("/")
def read_root():
    return {"status": "ok", "message": "API ML opérationnelle"}


# Route de prédiction
@app.post("/predict")
def predict_endpoint(payload: PredictRequest):
    # Logique de prédiction (remplacez par l'appel à votre modèle réel)
    try:
        # Simulation d'inférence
        prediction = 1 if payload.credit_score > 600 else 0
        probability = 0.85 if prediction == 1 else 0.15

        return {
            "prediction": prediction,
            "probability": probability
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur lors de la prédiction : {str(e)}"
        )