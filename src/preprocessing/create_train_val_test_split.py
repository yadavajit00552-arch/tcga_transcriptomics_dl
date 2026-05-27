"""
Create stratified train/validation/test split for TCGA-BRCA 4-class subtype dataset.

Input:
- data/processed/brca_expression_with_subtypes_4class.csv

Outputs:
- data/processed/splits/train.csv
- data/processed/splits/val.csv
- data/processed/splits/test.csv

Purpose:
Prepare reproducible train/validation/test datasets for ML and neural network models.
"""

from pathlib import Path
import pandas as pd
from sklearn.model_selection import train_test_split


INPUT_PATH = Path("data/processed/brca_expression_with_subtypes_4class.csv")
OUTPUT_DIR = Path("data/processed/splits")

RANDOM_SEED = 42
TEST_SIZE = 0.20
VAL_SIZE_FROM_REMAINING = 0.20

TARGET_COLUMN = "molecular_subtype"


def print_class_counts(name, df):
    """Print class counts and percentages."""
    counts = df[TARGET_COLUMN].value_counts()
    percentages = (df[TARGET_COLUMN].value_counts(normalize=True) * 100).round(2)

    summary = pd.DataFrame({
        "count": counts,
        "percentage": percentages
    })

    print(f"\n{name} shape:", df.shape)
    print(summary)


def main():
    print("Loading dataset...")
    df = pd.read_csv(INPUT_PATH)

    print("Input file:", INPUT_PATH)
    print("Full dataset shape:", df.shape)

    print_class_counts("Full dataset", df)

    print("\nCreating train/test split...")
    train_val_df, test_df = train_test_split(
        df,
        test_size=TEST_SIZE,
        random_state=RANDOM_SEED,
        stratify=df[TARGET_COLUMN],
    )

    print("Creating train/validation split...")
    train_df, val_df = train_test_split(
        train_val_df,
        test_size=VAL_SIZE_FROM_REMAINING,
        random_state=RANDOM_SEED,
        stratify=train_val_df[TARGET_COLUMN],
    )

    print_class_counts("Train dataset", train_df)
    print_class_counts("Validation dataset", val_df)
    print_class_counts("Test dataset", test_df)

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    train_path = OUTPUT_DIR / "train.csv"
    val_path = OUTPUT_DIR / "val.csv"
    test_path = OUTPUT_DIR / "test.csv"

    train_df.to_csv(train_path, index=False)
    val_df.to_csv(val_path, index=False)
    test_df.to_csv(test_path, index=False)

    print("\nSaved files:")
    print(train_path)
    print(val_path)
    print(test_path)

    total_after_split = len(train_df) + len(val_df) + len(test_df)
    print("\nTotal rows after split:", total_after_split)

    if total_after_split != len(df):
        raise ValueError("Split row count does not match original dataset.")

    print("✅ Stratified split completed successfully.")


if __name__ == "__main__":
    main()
