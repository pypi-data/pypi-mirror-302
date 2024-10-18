"""Module for data extraction."""

import os
import requests


def extract(url="https://archive.ics.uci.edu/ml/machine-learning-databases/adult/adult.data"):
    """Downloads the Adult dataset."""
    data_dir = "data"
    os.makedirs(data_dir, exist_ok=True)
    file_path = os.path.join(data_dir, "adult.data")

    if os.path.exists(file_path):
        print("Adult dataset already exists.")
        return

    print("Downloading Adult dataset...")
    response = requests.get(url)
    if response.status_code == 200:
        with open(file_path, "wb") as f:
            f.write(response.content)
        print("Download complete.")
    else:
        print(f"Failed to download Adult dataset. Status code: {response.status_code}")
