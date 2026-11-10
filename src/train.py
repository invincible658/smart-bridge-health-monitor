"""
Model Training Module for Smart Bridge Structural Health Monitoring.
Trains an unsupervised Isolation Forest model exclusively on healthy baseline segments
(Scenarios 0-4) and serializes the trained artifacts.
"""
import os
import joblib
import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler

MODELS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "models")

def train_isolation_forest(
    features_normal_df: pd.DataFrame,
    contamination: float = 0.05,
    n_estimators: int = 200,
    random_state: int = 42
):
    """
    Fits StandardScaler and IsolationForest on normal-state feature DataFrame.
    Returns:
        model: Fitted IsolationForest
        scaler: Fitted StandardScaler
    """
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(features_normal_df)
    
    model = IsolationForest(
        n_estimators=n_estimators,
        contamination=contamination,
        random_state=random_state,
        n_jobs=-1
    )
    model.fit(X_scaled)
    
    return model, scaler

def save_model_artifacts(model, scaler, save_dir: str = None):
    """
    Saves trained Isolation Forest and Scaler objects to disk using joblib.
    """
    target_dir = save_dir or MODELS_DIR
    os.makedirs(target_dir, exist_ok=True)
    
    model_path = os.path.join(target_dir, "isolation_forest.pkl")
    scaler_path = os.path.join(target_dir, "scaler.pkl")
    
    joblib.dump(model, model_path)
    joblib.dump(scaler, scaler_path)
    
    return model_path, scaler_path

def load_model_artifacts(model_dir: str = None):
    """
    Loads saved model and scaler artifacts from disk.
    """
    target_dir = model_dir or MODELS_DIR
    model_path = os.path.join(target_dir, "isolation_forest.pkl")
    scaler_path = os.path.join(target_dir, "scaler.pkl")
    
    if not os.path.exists(model_path) or not os.path.exists(scaler_path):
        raise FileNotFoundError(f"Model artifacts not found in '{target_dir}'. Run training first.")
        
    model = joblib.load(model_path)
    scaler = joblib.load(scaler_path)
    return model, scaler
