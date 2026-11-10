"""
Explainable AI (XAI) engine using SHAP:
Explains anomaly predictions by attributing feature importance to specific sensors and frequencies.
"""
import shap
import pandas as pd

def compute_shap_explanations(model, scaler, sample_features: pd.DataFrame):
    explainer = shap.TreeExplainer(model)
    sample_scaled = scaler.transform(sample_features)
    shap_values = explainer.shap_values(sample_scaled)
    return explainer, shap_values
