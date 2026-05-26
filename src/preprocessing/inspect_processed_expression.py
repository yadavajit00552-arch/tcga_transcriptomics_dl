"""
Inspect processed ML-ready TCGA-BRCA primary tumor expression matrix.

Input:
- data/processed/brca_expression_primary_tumor.csv

Checks:
1. Shape
2. Duplicate sample IDs
3. Missing values
4. Numeric gene columns
5. Preview
"""

from pathlib import Path
import pandas as pd


INPUT_PATH = Path("data/processed/brca_expression_primary_tumor.csv")


def main():
    df = pd.read_csv(INPUT_PATH)

    print("Input file:", INPUT_PATH)
    print("Shape:", df.shape)

    print("\nFirst columns:")
    print(df.columns[:10].tolist())

    duplicate_count = df["sample_id"].duplicated().sum()
    print("\nDuplicate sample IDs:", duplicate_count)

    total_missing = df.isna().sum().sum()
    print("Total missing values:", total_missing)

    gene_cols = [col for col in df.columns if col != "sample_id"]
    numeric_gene_cols = df[gene_cols].select_dtypes(include="number").columns

    print("Number of gene columns:", len(gene_cols))
    print("Numeric gene columns:", len(numeric_gene_cols))

    print("\nExpression value summary for first 5 genes:")
    print(df[gene_cols[:5]].describe().T)

    print("\nPreview:")
    print(df.iloc[:5, :8])


if __name__ == "__main__":
    main()
