"""
Data download and verification script for the Z24 Bridge Dataset from Hugging Face.
Repository: thanglexuan/Z24-dataset-processed
"""
import os
import numpy as np
from datasets import load_dataset

DATASET_NAME = "thanglexuan/Z24-dataset-processed"
CACHE_DIR = os.path.join(os.path.dirname(__file__), "cache")

def download_and_inspect():
    print(f"[*] Fetching '{DATASET_NAME}' from Hugging Face Hub...")
    os.makedirs(CACHE_DIR, exist_ok=True)
    
    # Load dataset from Hugging Face
    ds = load_dataset(DATASET_NAME)
    print(f"[+] Dataset fetched successfully!")
    print(f"[*] Available splits: {list(ds.keys())}")
    
    # Inspect primary split structure
    split_name = "train" if "train" in ds else list(ds.keys())[0]
    sample = ds[split_name]
    print(f"[*] Split '{split_name}' contains {len(sample)} records.")
    print(f"[*] Column names: {sample.column_names}")
    
    return ds

if __name__ == "__main__":
    download_and_inspect()
