"""
Download TCGA-BRCA transcriptomics and metadata files from UCSC Xena.

Beginner goal:
Classify breast cancer molecular subtypes using RNA-seq expression data.

Files downloaded:
1. TCGA-BRCA HTSeq FPKM expression matrix
2. TCGA-BRCA phenotype / clinical metadata

Note:
Downloaded files are stored in data/raw/ and ignored by Git.
"""

from pathlib import Path
import gzip
import shutil
import yaml
import requests


XENA_FILES = {
    "expression_hiseqv2_gz": {
        "url": "https://tcga.xenahubs.net/download/TCGA.BRCA.sampleMap/HiSeqV2.gz",
        "output_gz": "data/raw/TCGA-BRCA.HiSeqV2.tsv.gz",
        "output_tsv": "data/raw/TCGA-BRCA.HiSeqV2.tsv",
    },

}


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


def download_file(url: str, output_path: str) -> None:
    """Download a file from URL to output path."""
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    if output_path.exists() and output_path.stat().st_size > 0:
        print(f"✅ Already exists: {output_path}")
        return

    print(f"⬇️  Downloading: {url}")

    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Macintosh; Apple Silicon Mac OS X) "
            "AppleWebKit/537.36 Chrome/120 Safari/537.36"
        )
    }

    with requests.get(
        url,
        stream=True,
        timeout=120,
        headers=headers,
        allow_redirects=True,
    ) as response:
        print(f"HTTP status: {response.status_code}")
        print(f"Final URL: {response.url}")
        response.raise_for_status()

        with open(output_path, "wb") as file:
            for chunk in response.iter_content(chunk_size=1024 * 1024):
                if chunk:
                    file.write(chunk)

    print(f"✅ Downloaded: {output_path}")


def gunzip_file(gz_path: str, output_path: str) -> None:
    """Uncompress .gz file to .tsv."""
    gz_path = Path(gz_path)
    output_path = Path(output_path)

    if output_path.exists() and output_path.stat().st_size > 0:
        print(f"✅ Already uncompressed: {output_path}")
        return

    print(f"📦 Uncompressing: {gz_path}")
    with gzip.open(gz_path, "rb") as f_in:
        with open(output_path, "wb") as f_out:
            shutil.copyfileobj(f_in, f_out)

    print(f"✅ Created: {output_path}")


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
        raise RuntimeError("Could not reach Xena. Check internet connection or firewall.")

    print("\nDownloading TCGA-BRCA files:")
    for file_info in XENA_FILES.values():
        download_file(file_info["url"], file_info["output_gz"])
        gunzip_file(file_info["output_gz"], file_info["output_tsv"])

    print("\n✅ Download step completed successfully.")


if __name__ == "__main__":
    main()
