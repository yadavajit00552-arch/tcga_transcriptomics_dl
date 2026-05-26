"""
Prepare TCGA-BRCA expression matrix for machine learning.

Input:
- data/raw/TCGA-BRCA.HiSeqV2.tsv

Output:
- data/processed/brca_expression_primary_tumor.csv

Steps:
1. Load raw expression matrix
2. Keep only primary tumor samples ending with '-01'
3. Transpose matrix from genes x samples to samples x genes
4. Save ML-ready expression matrix
"""

from pathlib import Path
import pandas as pd


RAW_EXPRESSION_PATH = Path("data/raw/TCGA-BRCA.HiSeqV2.tsv")
OUTPUT_PATH = Path("data/processed/brca_expression_primary_tumor.csv")


def main():
    print("Loading expression matrix...")
    df = pd.read_csv(RAW_EXPRESSION_PATH, sep="\t")

    print("Raw expression shape:", df.shape)

    gene_col = df.columns[0]
    print("Gene column:", gene_col)

    sample_cols = df.columns[1:]

    primary_tumor_samples = [
        sample_id for sample_id in sample_cols
        if sample_id.split("-")[-1] == "01"
    ]

    print("Total samples:", len(sample_cols))
    print("Primary tumor samples:", len(primary_tumor_samples))

    df_primary = df[[gene_col] + primary_tumor_samples].copy()

    # Set gene names as index
    df_primary = df_primary.set_index(gene_col)

    # Transpose: genes x samples -> samples x genes
    expression_ml = df_primary.T

    # Add sample_id column
    expression_ml.index.name = "sample_id"
    expression_ml = expression_ml.reset_index()

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    expression_ml.to_csv(OUTPUT_PATH, index=False)

    print("ML-ready expression shape:", expression_ml.shape)
    print("Saved:", OUTPUT_PATH)

    print("\nPreview:")
    print(expression_ml.iloc[:5, :8])


if __name__ == "__main__":
    main()
