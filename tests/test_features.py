"""Unit tests for feature engineering calculations."""
import numpy as np
from src.features import extract_channel_features

def test_extract_channel_features():
    # 100 Hz signal, 1 second = 100 samples
    sig = np.sin(2 * np.pi * 5.0 * np.linspace(0, 1.0, 100))
    feats = extract_channel_features(sig, fs=100.0)
    
    assert "rms" in feats
    assert "dominant_freq" in feats
    assert "spectral_entropy" in feats
    assert feats["rms"] > 0
    assert 4.0 <= feats["dominant_freq"] <= 6.0
