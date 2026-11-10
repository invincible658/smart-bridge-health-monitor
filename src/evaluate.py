"""
Model Evaluation Module:
Computes ROC-AUC, classification metrics, and decision score distributions
on damaged vs. undamaged test scenarios.
"""
import numpy as np
import pandas as pd
from sklearn.metrics import roc_auc_score, classification_report, precision_recall_curve

def evaluate_detector(model, scaler, X_test_df: pd.DataFrame, y_test: np.ndarray):
    """
    Evaluates the anomaly detection model on test features.
    
    Parameters:
        model: Trained Isolation Forest model
        scaler: Trained StandardScaler
        X_test_df: Feature DataFrame of test segments
        y_test: Ground truth binary labels (0 = Normal, 1 = Damage Anomaly)
        
    Returns:
        metrics_dict: Dictionary containing ROC-AUC, mean risk scores, and summary
    """
    X_scaled = scaler.transform(X_test_df)
    
    # IsolationForest decision_function: positive = inlier, negative = outlier.
    # We negate it so higher score = higher anomaly likelihood / risk.
    raw_decision = model.decision_function(X_scaled)
    anomaly_risk_scores = -raw_decision
    
    # Discrete predictions (-1 = anomaly, 1 = normal)
    raw_preds = model.predict(X_scaled)
    binary_preds = np.where(raw_preds == -1, 1, 0)
    
    # Calculate ROC-AUC
    auc = float(roc_auc_score(y_test, anomaly_risk_scores))
    
    # Compute class-specific average anomaly scores
    normal_scores = anomaly_risk_scores[y_test == 0]
    damage_scores = anomaly_risk_scores[y_test == 1]
    
    return {
        "roc_auc": auc,
        "mean_normal_score": float(np.mean(normal_scores)) if len(normal_scores) > 0 else 0.0,
        "mean_damage_score": float(np.mean(damage_scores)) if len(damage_scores) > 0 else 0.0,
        "predictions": binary_preds,
        "anomaly_risk_scores": anomaly_risk_scores
    }
