"""Creates a verified dataset copy in data_verified/ based on the NIH ODS review procedure.
Preserves original data/ completely untouched for test suite compatibility.
"""
import os
import sys

# Ensure dataset builder is accessible
backend_dir = os.path.dirname(os.path.abspath(__file__))
project_dir = os.path.dirname(backend_dir)
dataset_dir = os.path.join(project_dir, "dataset")

if dataset_dir not in sys.path:
    sys.path.insert(0, dataset_dir)

from build import build_verified_dataset

SRC_DIR = os.path.join(backend_dir, "data")
DST_DIR = os.path.join(backend_dir, "data_verified")

if __name__ == "__main__":
    print(f"Creating verified dataset from {SRC_DIR} into {DST_DIR}...")
    build_verified_dataset(SRC_DIR, DST_DIR)
    print("Verified dataset generated successfully.")
