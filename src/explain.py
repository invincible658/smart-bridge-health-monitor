"""
Explainable AI (XAI) Module using SHAP (SHapley Additive exPlanations).
Explains why an anomaly score was assigned by attributing contributions to specific
vibration features and sensor channels.
"""
import shap
import numpy as np
import pandas as pd

def get_tree_explainer(model):
    """
    Creates and returns a shap.TreeExplainer for the trained Isolation Forest model.
    """
    return shap.TreeExplainer(model)

def explain_prediction(
    explainer,
    scaler,
    sample_features_df: pd.DataFrame,
    top_k: int = 5
):
    """
    Calculates SHAP attribution scores for a single segment (1 row of features).
    
    Parameters:
        explainer: Trained shap.TreeExplainer
        scaler: Fitted StandardScaler
        sample_features_df: DataFrame with 1 row of extracted features
        top_k: Number of highest-contributing features to return
        
    Returns:
        dict: Top culprits and formatted diagnostic summary string
    """
    feature_names = list(sample_features_df.columns)
    sample_scaled = scaler.transform(sample_features_df)
    
    # Calculate SHAP values
    shap_values = explainer.shap_values(sample_scaled)
    
    # Isolation Forest SHAP outputs 1D or 2D array depending on shap version
    if isinstance(shap_values, list):
        vals = shap_values[0]
    else:
        vals = shap_values
        
    if vals.ndim > 1:
        vals = vals[0]
        
    # Create sorted Series of feature contributions
    contributions = pd.Series(vals, index=feature_names)
    
    # Sort by descending positive impact (pushed anomaly score higher)
    top_culprits = contributions.sort_values(ascending=False).head(top_k)
    
    # Generate human-readable summary text for RAG prompt ingestion
    summary_lines = []
    top_dict = []
    
    for feat, score in top_culprits.items():
        summary_lines.append(f"- {feat}: attribution score {score:+.3f}")
        top_dict.append({
            "feature": feat,
            "attribution": float(score)
        })
        
    summary_text = "\n".join(summary_lines)
    
    # Safely extract scalar for base expected value
    base_val = 0.0
    if hasattr(explainer, "expected_value"):
        exp_arr = np.ravel(explainer.expected_value)
        if len(exp_arr) > 0:
            base_val = float(exp_arr[0])
            
    return {
        "top_features": top_dict,
        "summary_text": summary_text,
        "base_value": base_val
    }
