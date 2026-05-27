"""
Create ML-ready feature matrices for TCGA-BRCA subtype classification.

Inputs:
- data/processed/splits/train.csv
- data/processed/splits/val.csv
- data/processed/splits/test.csv

Outputs:
- data/processed/ml/train_features.csv
- data/processed/ml/val_features.csv
- data/processed/ml/test_features.csv
- data/processed/ml/train_labels.csv
- data/processed/ml/val_labels.csv
- data/processed/ml/test_labels.csv
- data/processed/ml/selected_genes.csv

Steps:
1. Identify gene expression columns
2. Select top variable genes using train data only
3. Standardize features using train data only
4. Save scaled feature matrices and labels
"""

from pathlib import Path
import pandas as pd
from sklearn.preprocessing import StandardScaler


TRAIN_PATH = Path("data/processed/splits/train.csv")
VAL_PATH = Path("data/processed/splits/val.csv")
TEST_PATH = Path("data/processed/splits/test.csv")

OUTPUT_DIR = Path("data/processed/ml")

TARGET_COLUMN = "molecular_subtype"
TOP_VARIABLE_GENES = 5000

METADATA_COLUMNS = [
    "sample_id",
    "molecular_subtype",
    "PAM50Call_RNAseq_decoded",
    "PAM50_mRNA_nature2012_decoded",
    "ER_Status_nature2012_decoded",
    "PR_Status_nature2012_decoded",
    "HER2_Final_Status_nature2012_decoded",
]


def get_gene_columns(df):
    """Return gene expression columns only."""
    return [col for col in df.columns if col not in METADATA_COLUMNS]


def main():
    print("Loading train/validation/test splits...")

    train_df = pd.read_csv(TRAIN_PATH)
    val_df = pd.read_csv(VAL_PATH)
    test_df = pd.read_csv(TEST_PATH)

    print("Train shape:", train_df.shape)
    print("Validation shape:", val_df.shape)
    print("Test shape:", test_df.shape)

    gene_columns = get_gene_columns(train_df)
    print("\nTotal gene columns:", len(gene_columns))

    print(f"\nSelecting top {TOP_VARIABLE_GENES} variable genes using train data only...")
    train_variances = train_df[gene_columns].var(axis=0).sort_values(ascending=False)

    selected_genes = train_variances.head(TOP_VARIABLE_GENES).index.tolist()

    print("Selected genes:", len(selected_genes))
    print("Top 10 selected genes:")
    print(selected_genes[:10])

    X_train = train_df[selected_genes]
    X_val = val_df[selected_genes]
    X_test = test_df[selected_genes]

    y_train = train_df[["sample_id", TARGET_COLUMN]]
    y_val = val_df[["sample_id", TARGET_COLUMN]]
    y_test = test_df[["sample_id", TARGET_COLUMN]]

    print("\nScaling features using StandardScaler fitted on train data only...")
    scaler = StandardScaler()

    X_train_scaled = pd.DataFrame(
        scaler.fit_transform(X_train),
        columns=selected_genes,
        index=train_df["sample_id"],
    )

    X_val_scaled = pd.DataFrame(
        scaler.transform(X_val),
        columns=selected_genes,
        index=val_df["sample_id"],
    )

    X_test_scaled = pd.DataFrame(
        scaler.transform(X_test),
        columns=selected_genes,
        index=test_df["sample_id"],
    )

    X_train_scaled.index.name = "sample_id"
    X_val_scaled.index.name = "sample_id"
    X_test_scaled.index.name = "sample_id"

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    X_train_scaled.reset_index().to_csv(OUTPUT_DIR / "train_features.csv", index=False)
    X_val_scaled.reset_index().to_csv(OUTPUT_DIR / "val_features.csv", index=False)
    X_test_scaled.reset_index().to_csv(OUTPUT_DIR / "test_features.csv", index=False)

    y_train.to_csv(OUTPUT_DIR / "train_labels.csv", index=False)
    y_val.to_csv(OUTPUT_DIR / "val_labels.csv", index=False)
    y_test.to_csv(OUTPUT_DIR / "test_labels.csv", index=False)

    selected_gene_df = pd.DataFrame({
        "gene": selected_genes,
        "train_variance": train_variances.loc[selected_genes].values,
    })
    selected_gene_df.to_csv(OUTPUT_DIR / "selected_genes.csv", index=False)

    print("\nSaved ML-ready files in:", OUTPUT_DIR)

    print("\nFinal feature shapes:")
    print("X_train:", X_train_scaled.shape)
    print("X_val:", X_val_scaled.shape)
    print("X_test:", X_test_scaled.shape)

    print("\nLabel counts:")
    print("Train:")
    print(y_train[TARGET_COLUMN].value_counts())
    print("\nValidation:")
    print(y_val[TARGET_COLUMN].value_counts())
    print("\nTest:")
    print(y_test[TARGET_COLUMN].value_counts())

    print("\n✅ ML feature creation completed successfully.")


if __name__ == "__main__":
    main()
