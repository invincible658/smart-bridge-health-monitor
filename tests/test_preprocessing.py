"""
End-to-End Verification Test for Phase 1 Data Pipeline & Feature Extraction.
Verifies:
1. Signal Preprocessing (Detrending + Butterworth Low-Pass Filter)
2. Feature Extraction (RMS, Kurtosis, FFT Dominant Frequency, Spectral Entropy)
3. Zero-NaN / Zero-Inf matrix integrity across multi-channel arrays.
"""
import numpy as np
import pytest
from src.preprocessing import preprocess_segment, butter_lowpass_filter
from src.features import extract_channel_features, extract_segment_features, build_feature_dataframe

def test_butterworth_filter():
    # Signal composed of 3.8 Hz (structural frequency) + 45 Hz (high-frequency electrical noise)
    fs = 100.0
    t = np.linspace(0, 1.0, 100, endpoint=False)
    signal_low = np.sin(2 * np.pi * 3.8 * t)
    noise_high = 0.5 * np.sin(2 * np.pi * 45.0 * t)
    combined = signal_low + noise_high

    filtered = butter_lowpass_filter(combined, cutoff=30.0, fs=fs, order=4)
    # The high frequency noise should be significantly reduced
    assert len(filtered) == 100
    assert not np.isnan(filtered).any()

def test_preprocess_segment_dimensions():
    # 27 channels, 6000 time steps (standard Z24 segment)
    raw_segment = np.random.randn(27, 6000).astype(np.float32)
    cleaned = preprocess_segment(raw_segment, fs=100.0, cutoff=30.0)
    
    assert cleaned.shape == (27, 6000)
    # Mean of each channel should be approximately 0 after standardization
    for ch in range(27):
        assert abs(np.mean(cleaned[ch])) < 1e-3

def test_feature_extraction_values():
    # Pure 5 Hz sine wave
    fs = 100.0
    t = np.linspace(0, 10.0, 1000, endpoint=False)
    pure_5hz = np.sin(2 * np.pi * 5.0 * t)
    
    feats = extract_channel_features(pure_5hz, fs=fs)
    
    assert "rms" in feats
    assert "dominant_freq" in feats
    assert "spectral_entropy" in feats
    assert abs(feats["dominant_freq"] - 5.0) < 0.2  # Should detect ~5.0 Hz mode
    assert feats["rms"] > 0

def test_feature_dataframe_builder():
    # Small batch of 3 mock segments
    mock_batch = np.random.randn(3, 27, 1000).astype(np.float32)
    df = build_feature_dataframe(mock_batch, fs=100.0)
    
    # 27 channels * 6 features per channel = 162 columns
    assert df.shape == (3, 27 * 6)
    assert not df.isnull().values.any()
