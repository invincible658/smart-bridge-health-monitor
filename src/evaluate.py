"""
Evaluation metrics:
Computes ROC-AUC, Precision, Recall, and decision boundary diagnostics on damage scenarios.
"""
from sklearn.metrics import roc_auc_score, classification_report

def evaluate_detector(model, scaler, X_test, y_test):
    X_scaled = scaler.transform(X_test)
    scores = -model.decision_function(X_scaled)  # higher = more anomalous
    auc = roc_auc_score(y_test, scores)
    return auc, scores
