"""
Advisory & AI Inspector API Routes.
Connects ChromaDB RAG retrieval and Groq/Gemini LLM incident advisory generation.
"""
from fastapi import APIRouter
from pydantic import BaseModel
from src.report_generator import generate_incident_advisory, answer_inspector_query

router = APIRouter()

class AdvisoryRequest(BaseModel):
    segment_id: int = 450
    anomaly_score: float = -0.42
    shap_summary: str = "- ch14_dominant_freq: attribution score +0.48\n- ch15_kurtosis: attribution score +0.26"
    top_channels: list[int] = [14, 15]
    forecast_warning: str = "Critical threshold breach predicted at step T+6"

class ChatRequest(BaseModel):
    message: str

@router.post("/")
def get_advisory(req: AdvisoryRequest):
    """
    Retrieves matching historical failure cases from ChromaDB and synthesizes an inspection advisory.
    """
    res = generate_incident_advisory(
        segment_id=req.segment_id,
        anomaly_score=req.anomaly_score,
        shap_summary=req.shap_summary,
        top_channels=req.top_channels,
        forecast_warning=req.forecast_warning
    )
    return res

@router.post("/chat")
def chat_inspector(req: ChatRequest):
    """
    Answers natural language questions asked by engineers using the RAG knowledge base.
    """
    reply = answer_inspector_query(req.message)
    return {
        "user_query": req.message,
        "reply": reply
    }
