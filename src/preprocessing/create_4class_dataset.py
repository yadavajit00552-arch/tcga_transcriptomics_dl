"""
Create 4-class TCGA-BRCA molecular subtype dataset.

Input:
- data/processed/brca_expression_with_subtypes.csv

Output:
- data/processed/brca_expression_with_subtypes_4class.csv

Reason:
The Normal subtype has very few samples after merging.
For beginner modeling, we remove Normal and classify:
1. LumA
2. LumB
3. Basal
4. Her2
"""

from pathlib import Path
import pandas as pd


INPUT_PATH = Path("data/processed/brca_expression_with_subtypes.csv")
OUTPUT_PATH = Path("data/processed/brca_expression_with_subtypes_4class.csv")

KEEP_CLASSES = ["LumA", "LumB", "Basal", "Her2"]


def main():
    df = pd.read_csv(INPUT_PATH)

    print("Input file:", INPUT_PATH)
    print("Original shape:", df.shape)

    print("\nOriginal subtype counts:")
    print(df["molecular_subtype"].value_counts())

    df_4class = df[df["molecular_subtype"].isin(KEEP_CLASSES)].copy()

    print("\n4-class shape:", df_4class.shape)

    print("\n4-class subtype counts:")
    print(df_4class["molecular_subtype"].value_counts())

    print("\n4-class subtype percentages:")
    print((df_4class["molecular_subtype"].value_counts(normalize=True) * 100).round(2))

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    df_4class.to_csv(OUTPUT_PATH, index=False)

    print("\nSaved:", OUTPUT_PATH)


if __name__ == "__main__":
    main()
