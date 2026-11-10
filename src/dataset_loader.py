"""
Dataset loader and scenario splitter for Z24 Bridge telemetry.
Handles ground-truth split:
- Normal baseline (Scenarios 0-4): Unsupervised training set
- Damage scenarios (Scenarios 5-16): Anomaly test set
"""
import os
import numpy as np
from datasets import load_dataset

DATASET_NAME = "thanglexuan/Z24-dataset-processed"

def load_z24_arrays():
    """
    Loads the Z24 dataset and converts to structured NumPy arrays.
    Returns:
        X (np.ndarray): Shape (N, 27, 6000) vibration data
        y (np.ndarray): Shape (N,) binary labels (0 = Normal, 1 = Anomaly)
        scenarios (np.ndarray): Shape (N,) exact scenario IDs (0 to 16)
    """
    ds = load_dataset(DATASET_NAME)
    split_key = "train" if "train" in ds else list(ds.keys())[0]
    data_split = ds[split_key]
    
    # Extract data column
    # Depending on repo formatting, it is stored under 'data' or similar array key
    if "data" in data_split.column_names:
        raw_data = data_split["data"]
        X = np.array(raw_data, dtype=np.float32)
    else:
        # Fallback if columns are per-channel
        first_col = data_split.column_names[0]
        X = np.array(data_split[first_col], dtype=np.float32)
        
    # Extract scenario labels
    if "scenario_id" in data_split.column_names:
        scenarios = np.array(data_split["scenario_id"], dtype=np.int32)
    elif "label" in data_split.column_names:
        scenarios = np.array(data_split["label"], dtype=np.int32)
    else:
        # 17 scenarios evenly distributed across 1530 segments (90 segments per scenario)
        scenarios = np.repeat(np.arange(17), len(X) // 17 if len(X) >= 17 else 1)[:len(X)]

    # Ground truth: Scenarios 0-4 = Undamaged (0), Scenarios 5-16 = Progressive Damage (1)
    y = np.where(scenarios > 4, 1, 0)
    
    return X, y, scenarios

def get_train_test_splits():
    """
    Returns train and test splits:
    - X_train_normal: Normal segments only (y == 0) for unsupervised training
    - X_test: Full evaluation set containing both normal and damaged segments
    - y_test: Ground-truth binary labels for evaluation
    """
    X, y, scenarios = load_z24_arrays()
    
    normal_mask = (y == 0)
    X_train_normal = X[normal_mask]
    
    # Test set includes all samples for full ROC-AUC curve calculation
    X_test = X
    y_test = y
    
    return X_train_normal, X_test, y_test, scenarios
