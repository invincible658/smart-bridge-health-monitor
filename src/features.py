"""
Physics-Informed Feature Engineering Module for Structural Health Monitoring.
Extracts:
- Time-Domain: RMS, Peak-to-Peak, Kurtosis, Skewness
- Frequency-Domain: FFT Dominant Frequency (modal peak), Spectral Entropy
"""
import numpy as np
import pandas as pd
from scipy.fft import rfft, rfftfreq
from scipy.stats import kurtosis, skew

def extract_channel_features(sig: np.ndarray, fs: float = 100.0) -> dict:
    """
    Computes time-domain and frequency-domain dynamic features for a single 1D sensor signal.
    """
    # --- Time-Domain Metrics ---
    # RMS: Root Mean Square represents effective vibration energy
    rms_val = float(np.sqrt(np.mean(sig ** 2)))
    
    # Peak-to-Peak: Measures maximum dynamic amplitude swing
    ptp_val = float(np.ptp(sig))
    
    # Kurtosis: High kurtosis indicates sharp impulse impacts (cracking / spalling)
    kurt_val = float(kurtosis(sig, fisher=True))
    
    # Skewness: Asymmetry indicates directional structural load / settlement
    skew_val = float(skew(sig))
    
    # --- Frequency-Domain Metrics (FFT) ---
    n = len(sig)
    fft_vals = np.abs(rfft(sig))
    freqs = rfftfreq(n, d=1.0 / fs)
    
    # Exclude DC static component (0 Hz)
    fft_no_dc = fft_vals[1:]
    freqs_no_dc = freqs[1:]
    
    if len(fft_no_dc) > 0 and np.sum(fft_no_dc) > 0:
        # Dominant frequency: Peak vibration frequency (corresponds to bridge mode)
        dom_idx = int(np.argmax(fft_no_dc))
        dom_freq = float(freqs_no_dc[dom_idx])
        
        # Spectral Entropy: Measures frequency dispersion
        # (Healthy = concentrated energy; Damaged = energy distributed across frequencies)
        psd = fft_no_dc ** 2
        psd_norm = psd / (np.sum(psd) + 1e-12)
        spectral_entropy = float(-np.sum(psd_norm * np.log(psd_norm + 1e-12)))
    else:
        dom_freq = 0.0
        spectral_entropy = 0.0
        
    return {
        "rms": rms_val,
        "peak_to_peak": ptp_val,
        "kurtosis": kurt_val,
        "skewness": skew_val,
        "dominant_freq": dom_freq,
        "spectral_entropy": spectral_entropy
    }

def extract_segment_features(segment_27_channels: np.ndarray, fs: float = 100.0) -> dict:
    """
    Extracts features across all 27 channels for a single segment.
    Returns a flat dictionary ready for DataFrame row insertion.
    """
    row_features = {}
    num_channels = segment_27_channels.shape[0]
    
    for ch in range(num_channels):
        prefix = f"ch{ch+1}_"
        ch_feats = extract_channel_features(segment_27_channels[ch, :], fs=fs)
        for key, val in ch_feats.items():
            row_features[f"{prefix}{key}"] = val
            
    return row_features

def build_feature_dataframe(batch_segments: np.ndarray, fs: float = 100.0) -> pd.DataFrame:
    """
    Converts a batch of shape (N, 27, 6000) into a pandas DataFrame of shape (N, 27 * 6).
    """
    rows = []
    for i in range(len(batch_segments)):
        rows.append(extract_segment_features(batch_segments[i], fs=fs))
    return pd.DataFrame(rows)
