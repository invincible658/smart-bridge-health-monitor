"""
Telemetry API routes: Returns time-series vibration waveforms and FFT spectra for selected channels.
"""
from fastapi import APIRouter, Query
import numpy as np

router = APIRouter()

@router.get("/")
def get_telemetry(segment_id: int = Query(0, description="Segment index from Z24 dataset (0-1529)"),
                  channel_id: int = Query(1, description="Sensor channel number (1-27)")):
    """
    Returns time-series amplitude and FFT spectrum for visualization in Recharts.
    """
    # Placeholder returning sample telemetry slice (100 Hz, 100 points preview)
    t = np.linspace(0, 1.0, 100)
    waveform = (0.05 * np.sin(2 * np.pi * 3.85 * t) + 0.01 * np.random.randn(100)).tolist()
    
    return {
        "segment_id": segment_id,
        "channel_id": channel_id,
        "sampling_rate_hz": 100.0,
        "timestamps": t.tolist(),
        "amplitudes": waveform,
        "unit": "m/s^2"
    }
