"""
Merge TCGA-BRCA primary tumor expression matrix with molecular subtype metadata.

Inputs:
- data/processed/brca_expression_primary_tumor.csv
- data/processed/brca_subtype_metadata.csv

Output:
- data/processed/brca_expression_with_subtypes.csv

Purpose:
Create ML-ready table where each row is a tumor sample and each sample has:
1. sample_id
2. molecular_subtype label
3. gene expression features
"""

from pathlib import Path
import pandas as pd


EXPRESSION_PATH = Path("data/processed/brca_expression_primary_tumor.csv")
METADATA_PATH = Path("data/processed/brca_subtype_metadata.csv")
OUTPUT_PATH = Path("data/processed/brca_expression_with_subtypes.csv")


def main():
    print("Loading expression data...")
    expression = pd.read_csv(EXPRESSION_PATH)

    print("Loading subtype metadata...")
    metadata = pd.read_csv(METADATA_PATH)

    print("\nExpression shape:", expression.shape)
    print("Metadata shape:", metadata.shape)

    print("\nExpression sample ID preview:")
    print(expression["sample_id"].head().tolist())

    print("\nMetadata sample ID preview:")
    print(metadata["sample_id"].head().tolist())

    metadata_small = metadata[
        [
            "sample_id",
            "molecular_subtype",
            "PAM50Call_RNAseq_decoded",
            "PAM50_mRNA_nature2012_decoded",
            "ER_Status_nature2012_decoded",
            "PR_Status_nature2012_decoded",
            "HER2_Final_Status_nature2012_decoded",
        ]
    ].copy()

    merged = expression.merge(metadata_small, on="sample_id", how="inner")

    print("\nMerged shape:", merged.shape)

    print("\nSubtype counts after merge:")
    print(merged["molecular_subtype"].value_counts())

    missing_labels = merged["molecular_subtype"].isna().sum()
    print("\nMissing molecular subtype labels:", missing_labels)

    duplicate_samples = merged["sample_id"].duplicated().sum()
    print("Duplicate sample IDs:", duplicate_samples)

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    merged.to_csv(OUTPUT_PATH, index=False)

    print("\nSaved:", OUTPUT_PATH)

    print("\nPreview:")
    print(merged.iloc[:5, :10])


if __name__ == "__main__":
    main()
