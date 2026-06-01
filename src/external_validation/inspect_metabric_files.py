"""
Inspect METABRIC external validation files.

Expected location:
- data/external/metabric/

Purpose:
This script checks which METABRIC files are present and previews their structure.
It is designed as the first step before external validation.

It does not assume fixed filenames yet.
"""

from pathlib import Path
import pandas as pd


METABRIC_DIR = Path("data/external/metabric")

SUPPORTED_EXTENSIONS = [
    ".csv",
    ".tsv",
    ".txt",
]


def detect_separator(path):
    """Guess file separator from extension."""
    suffix = path.suffix.lower()

    if suffix == ".csv":
        return ","

    return "\t"


def inspect_table(path):
    """Inspect one tabular file."""
    sep = detect_separator(path)

    print("\n" + "=" * 80)
    print(f"File: {path}")
    print(f"Detected separator: {repr(sep)}")
    print("=" * 80)

    try:
        df_preview = pd.read_csv(path, sep=sep, nrows=5)
    except Exception as error:
        print(f"Could not read file: {error}")
        return

    print("Preview shape:", df_preview.shape)
    print("First 20 columns:")
    print(df_preview.columns[:20].tolist())

    print("\nFirst 5 rows and first 8 columns:")
    print(df_preview.iloc[:, :8])

    possible_subtype_cols = [
        col for col in df_preview.columns
        if any(keyword in col.lower() for keyword in ["subtype", "pam50", "claudin", "er_status", "her2", "pr_status"])
    ]

    if possible_subtype_cols:
        print("\nPossible subtype/clinical columns:")
        for col in possible_subtype_cols:
            print("-", col)
    else:
        print("\nNo obvious subtype/clinical columns found in preview.")


def main():
    print("METABRIC directory:", METABRIC_DIR)

    if not METABRIC_DIR.exists():
        raise FileNotFoundError(f"Missing directory: {METABRIC_DIR}")

    files = [
        path for path in METABRIC_DIR.iterdir()
        if path.is_file() and path.suffix.lower() in SUPPORTED_EXTENSIONS
    ]

    print("Number of supported files found:", len(files))

    if not files:
        print("\nNo METABRIC table files found yet.")
        print("Place downloaded METABRIC expression and clinical files in:")
        print(METABRIC_DIR)
        print("\nSupported extensions: .csv, .tsv, .txt")
        return

    print("\nFiles found:")
    for path in files:
        print("-", path.name)

    for path in files:
        inspect_table(path)

    print("\n✅ METABRIC file inspection completed.")


if __name__ == "__main__":
    main()
