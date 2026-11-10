"""
Telemetry API Routes for Smart Bridge Structural Health Monitoring.
Streams multi-channel vibration time-series waveforms and FFT frequency spectra
for real-time visualization in Recharts/Chart.js.
"""
from fastapi import APIRouter, Query
import numpy as np
from scipy.fft import rfft, rfftfreq

router = APIRouter()

@router.get("/")
def get_telemetry(
    segment_id: int = Query(0, description="Segment index from Z24 dataset (0-1529)"),
    channel_id: int = Query(14, ge=1, le=27, description="Sensor channel number (1-27)"),
    points: int = Query(100, ge=10, le=1000, description="Number of downsampled points for UI waveform")
):
    """
    Returns time-series vibration amplitudes and FFT frequency spectrum for the selected sensor channel.
    """
    fs = 100.0  # 100 Hz sampling rate
    duration = 60.0  # 60 seconds per segment = 6000 samples
    total_samples = int(fs * duration)
    
    # Simulate realistic bridge modal response based on segment ID
    # Segments > 400 represent damaged states with lower modal frequency and higher noise
    is_damage = segment_id > 400
    base_freq = 3.42 if is_damage else 3.85
    noise_level = 0.08 if is_damage else 0.02
    
    t_full = np.linspace(0, duration, total_samples, endpoint=False)
    # 1st bending mode + 2nd torsional mode + ambient noise
    wave_full = (
        0.05 * np.sin(2 * np.pi * base_freq * t_full) +
        0.02 * np.sin(2 * np.pi * 7.4 * t_full) +
        noise_level * np.random.randn(total_samples)
    )
    
    # Compute FFT frequency spectrum (up to 30 Hz Nyquist cutoff)
    fft_vals = np.abs(rfft(wave_full))
    freqs = rfftfreq(total_samples, d=1.0 / fs)
    mask_30hz = (freqs > 0.5) & (freqs <= 30.0)
    
    spectrum_data = [
        {"frequency": float(round(f, 2)), "amplitude": float(round(amp, 4))}
        for f, amp in zip(freqs[mask_30hz][::5], fft_vals[mask_30hz][::5])  # downsample for speed
    ]
    
    # Downsample time-series waveform for smooth UI line chart rendering
    step = total_samples // points
    time_series_data = [
        {"time": f"{round(t, 2)}s", "amplitude": float(round(amp, 4))}
        for t, amp in zip(t_full[::step][:points], wave_full[::step][:points])
    ]
    
    return {
        "segment_id": segment_id,
        "channel_id": channel_id,
        "sampling_rate_hz": fs,
        "fundamental_frequency_hz": base_freq,
        "is_damaged_state": is_damage,
        "waveform": time_series_data,
        "spectrum": spectrum_data[:50]
    }
