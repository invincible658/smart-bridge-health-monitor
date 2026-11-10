"""
Digital signal processing routines:
- Detrending (DC offset removal)
- Butterworth 4th-order low-pass filtering (cutoff = 30 Hz)
- Per-channel standardization
"""
import numpy as np
from scipy import signal

def preprocess_segment(segment: np.ndarray, sample_rate: float = 100.0, cutoff: float = 30.0) -> np.ndarray:
    """
    Apply DSP cleaning to a multi-channel signal segment of shape (channels, samples).
    """
    processed = np.zeros_like(segment)
    nyquist = 0.5 * sample_rate
    b, a = signal.butter(4, cutoff / nyquist, btype='low')
    
    for ch in range(segment.shape[0]):
        detrended = signal.detrend(segment[ch, :])
        filtered = signal.filtfilt(b, a, detrended)
        std_val = np.std(filtered)
        if std_val > 1e-8:
            processed[ch, :] = (filtered - np.mean(filtered)) / std_val
        else:
            processed[ch, :] = filtered
            
    return processed
