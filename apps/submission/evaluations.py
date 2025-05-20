import pandas as pd
from sklearn.metrics import (
    mean_squared_error,
    mean_absolute_error,
    r2_score,
    mean_squared_log_error
)
# import numpy as np
import json
def evaluate_submission(submission_path, reference_path, metric='mse'):
    """
    Évalue une soumission et retourne un score ou une erreur au format JSON.
    Paramètres :
    - submission_path (str) : chemin du fichier CSV soumis
    - reference_path (str) : chemin du fichier de vérité
    - metric (str) : métrique ('mse', 'mae', 'rmse', 'r2', 'msle')
    Retour :
    - dict : { 'status': 'success', 'score': float, 'metric': str }
             ou { 'status': 'error', 'message': str }
    """
    try:
        # Chargement des fichiers
        sub_df = pd.read_csv(submission_path)
        ref_df = pd.read_csv(reference_path)
        # Vérification des colonnes
        required_columns = {'id', 'target'}
        if not required_columns.issubset(sub_df.columns) or not required_columns.issubset(ref_df.columns):
            return {
                "status": "error",
                "message": "Le fichier doit contenir les colonnes 'id' et 'target'."
            }
        # Vérification de la taille
        if sub_df.shape[0] != ref_df.shape[0]:
            return {
                "status": "error",
                "message": f"Le nombre de lignes attendus n'est pas exact, on s'attend à {sub_df.shape[0]} au lieu de {ref_df.shape[0]}"
            }
        # Vérification de la correspondance des identifiants
        merged = pd.merge(ref_df, sub_df, on='id', suffixes=('_true', '_pred'))
        if merged.shape[0] != ref_df.shape[0]:
            return {
                "status": "error",
                "message": "Certains identifiants de la soumission ne correspondent pas au fichier témoin."
            }
        # Extraction des valeurs
        y_true = merged['target_true'].values
        y_pred = merged['target_pred'].values
        # Dictionnaire des métriques disponibles
        metrics = {
            'mse': mean_squared_error,
            'mae': mean_absolute_error,
            'rmse': lambda y_t, y_p: mean_squared_error(y_t, y_p, squared=False),
            'r2': r2_score,
            'msle': mean_squared_log_error
        }
        if metric not in metrics:
            return {
                "status": "error",
                "message": f"Métrique '{metric}' non supportée. Choisissez parmi : {list(metrics.keys())}"
            }
        # Calcul du score
        score = metrics[metric](y_true, y_pred)
        return {
            "status": "success",
            "metric": metric,
            "score": float(score)
        }
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }