import time
import numpy as np


class ModelLoadError(Exception):
    """Exception personnalisée lors de l'échec de chargement du modèle."""
    pass


def preprocess_data(data: dict) -> np.ndarray:
    """Valide et transforme les données d'entrée brutes en tableau NumPy 2D."""
    try:
        age = float(data["age"])
        income = float(data["income"])
        credit_score = float(data["credit_score"])
    except (ValueError, TypeError, KeyError) as e:
        raise ValueError(f"Données d'entrée invalides pour le prétraitement : {e}")

    return np.array([[age, income, credit_score]])


def predict(features: np.ndarray) -> tuple[int, float]:
    """Exécute la prédiction sur les caractéristiques fournies.

    Retourne :
        tuple: (prédiction [0 ou 1], probabilité [0.0 à 1.0])
    """
    if not isinstance(features, np.ndarray) or features.shape[1] != 3:
        raise ValueError("Les features doivent être un ndarray de forme (N, 3)")

    # Extrait les variables pour la logique ou le modèle
    age, income, credit_score = features[0]

    # Simulation de la logique de prédiction / modèle ML
    # Remplacez ce bloc par l'appel à votre modèle réel (joblib/pickle)
    score_normalise = (credit_score / 850) * 0.6 + (income / 100000) * 0.4

    probability = float(np.clip(score_normalise, 0.05, 0.95))
    prediction = 1 if probability >= 0.5 else 0

    return prediction, probability