"""
Inspect TCGA-BRCA expression matrix.

This script checks:
1. Matrix shape
2. Number of genes
3. Number of samples
4. TCGA sample type counts
5. Preview of first few genes and samples
"""

import pandas as pd


EXPRESSION_PATH = "data/raw/TCGA-BRCA.HiSeqV2.tsv"


def main():
    df = pd.read_csv(EXPRESSION_PATH, sep="\t")

    sample_cols = df.columns[1:]
    sample_types = pd.Series(
        [sample_id.split("-")[-1] for sample_id in sample_cols],
        name="sample_type"
    ).value_counts().sort_index()

    print("Expression file:", EXPRESSION_PATH)
    print("Full shape:", df.shape)
    print("Number of genes:", df.shape[0])
    print("Number of samples:", len(sample_cols))

    print("\nSample type counts:")
    print(sample_types)

    print("\nColumn preview:")
    print(df.columns[:10].tolist())

    print("\nFirst 5 rows and first 8 columns:")
    print(df.iloc[:5, :8])


if __name__ == "__main__":
    main()
