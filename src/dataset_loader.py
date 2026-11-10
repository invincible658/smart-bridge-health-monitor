"""
Dataset loader and splitter for Z24 Bridge telemetry.
Splits data into healthy baseline (Scenarios 0-4) and damage test scenarios (5-16).
"""
import numpy as np
from datasets import load_dataset

DATASET_NAME = "thanglexuan/Z24-dataset-processed"

def load_z24(split: str = "train"):
    """
    Loads Z24 dataset and creates normal vs anomaly masks.
    """
    dataset = load_dataset(DATASET_NAME, split=split)
    # Target structure: array of shape (N, 27, 6000)
    return dataset
