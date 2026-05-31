"""
Plot TCGA-BRCA molecular subtype distribution.

Input:
- data/processed/brca_expression_with_subtypes_4class.csv

Output:
- results/figures/subtype_distribution.png
- results/tables/subtype_distribution.csv

Purpose:
Visualize class imbalance before model training.
"""

from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt


INPUT_PATH = Path("data/processed/brca_expression_with_subtypes_4class.csv")
FIGURE_DIR = Path("results/figures")
TABLE_DIR = Path("results/tables")

OUTPUT_FIGURE = FIGURE_DIR / "subtype_distribution.png"
OUTPUT_TABLE = TABLE_DIR / "subtype_distribution.csv"

TARGET_COLUMN = "molecular_subtype"


def main():
    print("Loading dataset...")
    df = pd.read_csv(INPUT_PATH)

    print("Dataset shape:", df.shape)

    counts = df[TARGET_COLUMN].value_counts()
    percentages = (df[TARGET_COLUMN].value_counts(normalize=True) * 100).round(2)

    summary = pd.DataFrame({
        "subtype": counts.index,
        "count": counts.values,
        "percentage": percentages.values,
    })

    print("\nSubtype distribution:")
    print(summary)

    FIGURE_DIR.mkdir(parents=True, exist_ok=True)
    TABLE_DIR.mkdir(parents=True, exist_ok=True)

    summary.to_csv(OUTPUT_TABLE, index=False)

    plt.figure(figsize=(7, 5))
    plt.bar(summary["subtype"], summary["count"])
    plt.xlabel("Molecular subtype")
    plt.ylabel("Number of samples")
    plt.title("TCGA-BRCA 4-Class Molecular Subtype Distribution")

    for i, row in summary.iterrows():
        plt.text(
            i,
            row["count"] + 5,
            f'{row["count"]}\n({row["percentage"]}%)',
            ha="center",
            va="bottom",
        )

    plt.tight_layout()
    plt.savefig(OUTPUT_FIGURE, dpi=300)
    plt.close()

    print("\nSaved figure:", OUTPUT_FIGURE)
    print("Saved table:", OUTPUT_TABLE)
    print("✅ Subtype distribution plot created successfully.")


if __name__ == "__main__":
    main()
