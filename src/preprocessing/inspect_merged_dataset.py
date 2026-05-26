"""
Inspect merged TCGA-BRCA expression + subtype dataset.

Input:
- data/processed/brca_expression_with_subtypes.csv

Checks:
1. Shape
2. Label distribution
3. Missing values
4. Duplicate sample IDs
5. Gene feature count
6. Metadata columns
"""

from pathlib import Path
import pandas as pd


INPUT_PATH = Path("data/processed/brca_expression_with_subtypes.csv")

METADATA_COLUMNS = [
    "sample_id",
    "molecular_subtype",
    "PAM50Call_RNAseq_decoded",
    "PAM50_mRNA_nature2012_decoded",
    "ER_Status_nature2012_decoded",
    "PR_Status_nature2012_decoded",
    "HER2_Final_Status_nature2012_decoded",
]


def main():
    df = pd.read_csv(INPUT_PATH)

    print("Input file:", INPUT_PATH)
    print("Shape:", df.shape)

    print("\nSubtype counts:")
    print(df["molecular_subtype"].value_counts())

    print("\nSubtype percentages:")
    print((df["molecular_subtype"].value_counts(normalize=True) * 100).round(2))

    duplicate_count = df["sample_id"].duplicated().sum()
    print("\nDuplicate sample IDs:", duplicate_count)

    total_missing = df.isna().sum().sum()
    print("Total missing values:", total_missing)

    missing_by_metadata = df[METADATA_COLUMNS].isna().sum()
    print("\nMissing values in metadata columns:")
    print(missing_by_metadata)

    gene_columns = [col for col in df.columns if col not in METADATA_COLUMNS]
    print("\nNumber of gene feature columns:", len(gene_columns))

    numeric_gene_columns = df[gene_columns].select_dtypes(include="number").columns
    print("Numeric gene feature columns:", len(numeric_gene_columns))

    print("\nFirst 10 gene columns:")
    print(gene_columns[:10])

    print("\nPreview:")
    print(df[METADATA_COLUMNS].head())


if __name__ == "__main__":
    main()
