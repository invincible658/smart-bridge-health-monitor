"""
Automated Integration Tests for Phase 4: FastAPI REST API Endpoints.
Uses FastAPI's Starlette TestClient to test all HTTP routes without needing an active network port.
"""
from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

def test_root_endpoint():
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "online"
    assert "/docs" in data["docs_url"]

def test_telemetry_endpoint():
    response = client.get("/api/telemetry?segment_id=10&channel_id=14&points=50")
    assert response.status_code == 200
    data = response.json()
    assert data["channel_id"] == 14
    assert len(data["waveform"]) == 50
    assert "spectrum" in data
    assert data["fundamental_frequency_hz"] > 0

def test_detection_and_explain_endpoints():
    # Test detection
    res_detect = client.post("/api/detect/", json={"segment_id": 450})
    assert res_detect.status_code == 200
    data_detect = res_detect.json()
    assert data_detect["is_anomaly"] is True
    assert data_detect["indicator_color"] == "red"
    
    # Test SHAP explain
    res_explain = client.post("/api/detect/explain", json={"segment_id": 450})
    assert res_explain.status_code == 200
    data_explain = res_explain.json()
    assert len(data_explain["shap_features"]) > 0
    assert "ch14_dominant_freq" in data_explain["summary_text"]

def test_forecasting_endpoint():
    response = client.get("/api/forecast/?steps=7&degrading=true")
    assert response.status_code == 200
    data = response.json()
    assert "chart_data" in data
    assert data["breach_predicted"] is True
    assert data["critical_threshold_hz"] == 3.50

def test_advisory_endpoints():
    # Test RAG report generation
    req_payload = {
        "segment_id": 450,
        "anomaly_score": -0.42,
        "shap_summary": "- ch14_dominant_freq: +0.48",
        "top_channels": [14, 15],
        "forecast_warning": "Breach in 5 steps"
    }
    res_advisory = client.post("/api/advisory/", json=req_payload)
    assert res_advisory.status_code == 200
    data_adv = res_advisory.json()
    assert "advisory_text" in data_adv
    assert len(data_adv["advisory_text"]) > 50
    
    # Test chat endpoint
    res_chat = client.post("/api/advisory/chat", json={"message": "What is the standard for pier settlement?"})
    assert res_chat.status_code == 200
    assert "reply" in res_chat.json()
