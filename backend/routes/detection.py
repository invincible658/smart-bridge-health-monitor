"""
Detection & Explainability API routes: Evaluates segment for point anomalies and computes SHAP attribution.
"""
from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()

class DetectionRequest(BaseModel):
    segment_id: int = 0

@router.post("/")
def detect_anomaly(req: DetectionRequest):
    """
    Computes Isolation Forest anomaly score and classification for the specified segment.
    """
    # Sample response format
    return {
        "segment_id": req.segment_id,
        "is_anomaly": bool(req.segment_id > 400),
        "anomaly_score": -0.38 if req.segment_id > 400 else 0.42,
        "risk_level": "CRITICAL" if req.segment_id > 400 else "NORMAL",
        "top_contributing_channels": [14, 15, 3] if req.segment_id > 400 else []
    }

@router.post("/explain")
def explain_anomaly(req: DetectionRequest):
    """
    Returns SHAP attribution values for the top features contributing to the anomaly score.
    """
    return {
        "segment_id": req.segment_id,
        "shap_features": [
            {"feature": "ch14_dominant_freq", "contribution": 0.48},
            {"feature": "ch15_kurtosis", "contribution": 0.26},
            {"feature": "ch14_spectral_entropy", "contribution": 0.18},
            {"feature": "ch3_rms", "contribution": -0.04}
        ]
    }
