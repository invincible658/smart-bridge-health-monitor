"""
Comprehensive Unit Test Suite for Phase 2:
- Isolation Forest Model Training and Persistence
- ROC-AUC Evaluation on Damaged vs. Normal Splits
- ARIMA Stiffness Degradation Trend Forecasting
- SHAP Feature Attribution Diagnostics
"""
import os
import shutil
import tempfile
import numpy as np
import pandas as pd
import pytest

from src.train import train_isolation_forest, save_model_artifacts, load_model_artifacts
from src.evaluate import evaluate_detector
from src.forecast import forecast_stiffness_trend
from src.explain import get_tree_explainer, explain_prediction

@pytest.fixture
def synthetic_data():
    """Generates synthetic normal baseline and damaged anomaly features for testing."""
    np.random.seed(42)
    n_features = 20
    
    # 60 normal training samples
    X_train = pd.DataFrame(
        np.random.normal(loc=0.0, scale=1.0, size=(60, n_features)),
        columns=[f"feat_{i}" for i in range(n_features)]
    )
    
    # 40 test samples (20 normal, 20 anomalies with shifted distribution)
    normal_test = np.random.normal(loc=0.0, scale=1.0, size=(20, n_features))
    anomaly_test = np.random.normal(loc=4.0, scale=2.0, size=(20, n_features))
    
    X_test = pd.DataFrame(
        np.vstack([normal_test, anomaly_test]),
        columns=[f"feat_{i}" for i in range(n_features)]
    )
    y_test = np.array([0] * 20 + [1] * 20)
    
    return X_train, X_test, y_test

def test_model_training_and_serialization(synthetic_data):
    X_train, _, _ = synthetic_data
    model, scaler = train_isolation_forest(X_train, n_estimators=25)
    
    temp_dir = tempfile.mkdtemp()
    try:
        model_path, scaler_path = save_model_artifacts(model, scaler, save_dir=temp_dir)
        assert os.path.exists(model_path)
        assert os.path.exists(scaler_path)
        
        loaded_model, loaded_scaler = load_model_artifacts(model_dir=temp_dir)
        assert loaded_model is not None
        assert loaded_scaler is not None
    finally:
        shutil.rmtree(temp_dir)

def test_model_evaluation(synthetic_data):
    X_train, X_test, y_test = synthetic_data
    model, scaler = train_isolation_forest(X_train, n_estimators=50)
    
    metrics = evaluate_detector(model, scaler, X_test, y_test)
    
    assert "roc_auc" in metrics
    assert metrics["roc_auc"] > 0.80  # Outliers should be cleanly separated
    assert metrics["mean_damage_score"] > metrics["mean_normal_score"]

def test_arima_forecasting():
    # Sequence of declining modal frequencies (e.g. progressive pier settlement)
    declining_freqs = np.array([3.85, 3.84, 3.82, 3.80, 3.76, 3.72, 3.66, 3.60, 3.55])
    
    forecast_results = forecast_stiffness_trend(
        declining_freqs,
        order=(1, 1, 0),
        steps=7,
        critical_threshold_hz=3.50
    )
    
    assert "mean_forecast" in forecast_results
    assert len(forecast_results["mean_forecast"]) == 7
    assert len(forecast_results["lower_bound"]) == 7
    assert len(forecast_results["upper_bound"]) == 7
    # Since trajectory is declining and ends near 3.55, a breach should be anticipated
    assert forecast_results["breach_predicted"] is True
    assert forecast_results["steps_to_breach"] is not None

def test_shap_explainability(synthetic_data):
    X_train, X_test, _ = synthetic_data
    model, scaler = train_isolation_forest(X_train, n_estimators=25)
    
    explainer = get_tree_explainer(model)
    # Explain first anomaly row (index 25)
    sample_row = X_test.iloc[[25]]
    explanation = explain_prediction(explainer, scaler, sample_row, top_k=3)
    
    assert "top_features" in explanation
    assert len(explanation["top_features"]) == 3
    assert "summary_text" in explanation
    assert len(explanation["summary_text"]) > 0
