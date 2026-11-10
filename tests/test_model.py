"""Unit tests for model training and inference."""
import numpy as np
from src.train import train_isolation_forest

def test_train_isolation_forest():
    # 50 samples, 10 features
    X_dummy = np.random.randn(50, 10)
    model, scaler = train_isolation_forest(X_dummy, n_estimators=10)
    
    X_scaled = scaler.transform(X_dummy)
    preds = model.predict(X_scaled)
    assert len(preds) == 50
