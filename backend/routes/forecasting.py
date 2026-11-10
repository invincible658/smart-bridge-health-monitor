"""
Forecasting API Routes for Structural Stiffness Degradation.
Runs ARIMA time-series modeling on modal frequencies and projects threshold breach horizons.
"""
from fastapi import APIRouter, Query
from src.forecast import forecast_stiffness_trend
import numpy as np

router = APIRouter()

@router.get("/")
def get_forecast(
    steps: int = Query(10, ge=3, le=30, description="Steps ahead to forecast"),
    degrading: bool = Query(True, description="Simulate progressive degradation vs stable baseline")
):
    """
    Returns ARIMA historical sequence, future forecast trajectory, and safety breach checks.
    """
    if degrading:
        # Declining dominant frequencies across progressive damage scenarios
        history = [3.85, 3.84, 3.82, 3.80, 3.76, 3.73, 3.68, 3.62, 3.56]
    else:
        # Stable baseline under normal operational traffic
        history = [3.85, 3.86, 3.84, 3.85, 3.83, 3.86, 3.85, 3.84, 3.85]
        
    res = forecast_stiffness_trend(
        np.array(history),
        order=(1, 1, 0),
        steps=steps,
        critical_threshold_hz=3.50
    )
    
    # Format unified chart data for Recharts
    chart_data = []
    for i, h in enumerate(history):
        chart_data.append({
            "step": f"T-{len(history) - 1 - i}",
            "historical": float(round(h, 3)),
            "forecast": None,
            "lower_bound": None,
            "upper_bound": None
        })
        
    for j in range(steps):
        chart_data.append({
            "step": f"T+{j + 1}",
            "historical": None,
            "forecast": round(res["mean_forecast"][j], 3),
            "lower_bound": round(res["lower_bound"][j], 3),
            "upper_bound": round(res["upper_bound"][j], 3)
        })
        
    return {
        "chart_data": chart_data,
        "critical_threshold_hz": res["critical_threshold_hz"],
        "breach_predicted": res["breach_predicted"],
        "steps_to_breach": res["steps_to_breach"],
        "summary": (
            f"Threshold breach (< 3.50 Hz) predicted at step T+{res['steps_to_breach']}. Immediate bearing/pier inspection advised."
            if res["breach_predicted"]
            else "Stiffness frequency remains stable above 3.50 Hz safety threshold."
        )
    }
