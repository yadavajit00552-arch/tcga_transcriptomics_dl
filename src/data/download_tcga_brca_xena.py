"""
Download TCGA-BRCA transcriptomics and metadata files.

Beginner goal:
Classify breast cancer molecular subtypes using RNA-seq expression data.

This script will later download data from UCSC Xena / TCGA-related sources.
"""

from pathlib import Path
import yaml
import requests


def load_config(config_path: str = "configs/config.yaml") -> dict:
    """Load project configuration file."""
    with open(config_path, "r") as file:
        config = yaml.safe_load(file)
    return config


def check_internet(url: str = "https://xenabrowser.net") -> bool:
    """Check whether internet connection and Xena server are reachable."""
    try:
        response = requests.get(url, timeout=15)
        return response.status_code == 200
    except requests.RequestException:
        return False


def main():
    config = load_config()

    raw_dir = Path(config["data"]["raw_dir"])
    processed_dir = Path(config["data"]["processed_dir"])
    external_dir = Path(config["data"]["external_dir"])

    print("Project:", config["project"]["name"])
    print("Cohort:", config["project"]["cohort"])
    print("Beginner goal:", config["project"]["beginner_goal"])

    print("\nChecking directories:")
    for directory in [raw_dir, processed_dir, external_dir]:
        directory.mkdir(parents=True, exist_ok=True)
        print(f"✅ {directory}")

    print("\nChecking internet/Xena access:")
    if check_internet():
        print("✅ Internet working and Xena reachable")
    else:
        print("❌ Could not reach Xena. Check internet connection or firewall.")

    print("\nScript skeleton completed successfully.")


if __name__ == "__main__":
    main()
