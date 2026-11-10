"""
Digital Signal Processing (DSP) Module for Multi-Channel Vibration Telemetry.
Operations:
1. DC Detrending (drift & static electrical bias removal)
2. Butterworth Low-Pass Filter (removes high-frequency noise above 30 Hz)
3. Z-score Channel Standardization
"""
import numpy as np
from scipy import signal

def butter_lowpass_filter(data: np.ndarray, cutoff: float = 30.0, fs: float = 100.0, order: int = 4) -> np.ndarray:
    """
    Applies a zero-phase forward-backward Butterworth low-pass filter along the time axis.
    data: 1D array of time-series samples
    """
    nyquist = 0.5 * fs
    normal_cutoff = min(cutoff / nyquist, 0.99)  # Avoid exceeding Nyquist limit
    b, a = signal.butter(order, normal_cutoff, btype='low', analog=False)
    # filtfilt avoids phase distortion
    filtered = signal.filtfilt(b, a, data)
    return filtered

def preprocess_segment(segment: np.ndarray, fs: float = 100.0, cutoff: float = 30.0) -> np.ndarray:
    """
    Preprocesses a 2D multi-channel segment of shape (channels, time_steps).
    channels: 27 accelerometer channels
    time_steps: typically 6000 points (60 seconds at 100 Hz)
    """
    if segment.ndim == 1:
        segment = segment.reshape(1, -1)
        
    num_channels, num_samples = segment.shape
    cleaned = np.zeros_like(segment, dtype=np.float32)
    
    for ch in range(num_channels):
        raw_ch = segment[ch, :]
        
        # 1. Remove DC drift and static tilt offset
        detrended = signal.detrend(raw_ch)
        
        # 2. 4th-order low-pass Butterworth filter at 30 Hz
        # (Civil bridges vibrate primarily between 0.5 Hz and 25-30 Hz)
        filtered = butter_lowpass_filter(detrended, cutoff=cutoff, fs=fs, order=4)
        
        # 3. Standardization (zero mean, unit variance per channel)
        std_dev = np.std(filtered)
        if std_dev > 1e-7:
            cleaned[ch, :] = (filtered - np.mean(filtered)) / std_dev
        else:
            cleaned[ch, :] = filtered - np.mean(filtered)
            
    return cleaned

def preprocess_batch(batch: np.ndarray, fs: float = 100.0) -> np.ndarray:
    """
    Preprocesses a 3D batch of shape (samples, channels, time_steps).
    """
    cleaned_batch = np.zeros_like(batch, dtype=np.float32)
    for i in range(len(batch)):
        cleaned_batch[i] = preprocess_segment(batch[i], fs=fs)
    return cleaned_batch
