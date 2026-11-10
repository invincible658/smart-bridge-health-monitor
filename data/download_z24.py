"""Data download and caching utilities for Z24 Bridge Dataset from Hugging Face."""
from datasets import load_dataset
import os

DATASET_NAME = "thanglexuan/Z24-dataset-processed"

def download_data():
    print(f"Fetching dataset '{DATASET_NAME}' from Hugging Face...")
    ds = load_dataset(DATASET_NAME)
    print("Dataset successfully fetched and cached!")
    return ds

if __name__ == "__main__":
    download_data()
