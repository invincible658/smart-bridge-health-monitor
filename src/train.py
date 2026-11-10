"""
Model training module:
Fits an Isolation Forest solely on undamaged bridge operational segments.
"""
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
import joblib

def train_isolation_forest(X_train_normal, contamination: float = 0.05, n_estimators: int = 200):
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X_train_normal)
    
    model = IsolationForest(
        n_estimators=n_estimators,
        contamination=contamination,
        random_state=42
    )
    model.fit(X_scaled)
    return model, scaler
