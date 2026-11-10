"""Unit test placeholder for signal pre-processing."""
import numpy as np
from src.preprocessing import preprocess_segment

def test_preprocess_shape():
    mock_data = np.random.randn(27, 6000)
    cleaned = preprocess_segment(mock_data)
    assert cleaned.shape == (27, 6000)
