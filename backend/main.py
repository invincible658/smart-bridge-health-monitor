"""
FastAPI Application Entry Point for Smart Bridge Health Monitoring System.
Exposes REST endpoints for telemetry, anomaly detection, forecasting, and AI diagnostics.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.routes import telemetry, detection, forecasting, advisory

app = FastAPI(
    title="Smart Bridge Health Monitoring API",
    description="Backend API for real-time bridge vibration analysis, anomaly detection, and RAG advisory.",
    version="1.0.0"
)

# Enable CORS for React frontend (Vite dev server runs on port 5173)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173", "*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register endpoint routers
app.include_router(telemetry.router, prefix="/api/telemetry", tags=["Telemetry"])
app.include_router(detection.router, prefix="/api/detect", tags=["Anomaly Detection"])
app.include_router(forecasting.router, prefix="/api/forecast", tags=["Forecasting"])
app.include_router(advisory.router, prefix="/api/advisory", tags=["RAG Advisory"])

@app.get("/")
def root():
    return {
        "status": "online",
        "service": "Smart Bridge Structural Health Monitoring API",
        "docs_url": "/docs"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.main:app", host="0.0.0.0", port=8000, reload=True)
