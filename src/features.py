"""
Feature engineering module:
Extracts time-domain (RMS, kurtosis, peak-to-peak) and frequency-domain (FFT, spectral entropy) metrics.
"""
import numpy as np
from scipy.fft import rfft, rfftfreq
from scipy.stats import kurtosis, skew

def extract_channel_features(sig: np.ndarray, fs: float = 100.0) -> dict:
    """
    Computes time and frequency features for a single 1D time-series signal.
    """
    rms_val = np.sqrt(np.mean(sig**2))
    ptp_val = np.ptp(sig)
    kurt_val = float(kurtosis(sig))
    skew_val = float(skew(sig))
    
    n = len(sig)
    fft_mag = np.abs(rfft(sig))[1:]
    freqs = rfftfreq(n, d=1.0/fs)[1:]
    
    dom_idx = np.argmax(fft_mag)
    dom_freq = freqs[dom_idx]
    
    psd = fft_mag ** 2
    psd_norm = psd / (np.sum(psd) + 1e-12)
    entropy = -np.sum(psd_norm * np.log(psd_norm + 1e-12))
    
    return {
        "rms": rms_val,
        "peak_to_peak": ptp_val,
        "kurtosis": kurt_val,
        "skewness": skew_val,
        "dominant_freq": dom_freq,
        "spectral_entropy": entropy
    }
