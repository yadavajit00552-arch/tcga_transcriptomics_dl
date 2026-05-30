"""
Create PCA plot of TCGA-BRCA samples colored by molecular subtype.

Inputs:
- data/processed/ml/train_features.csv
- data/processed/ml/val_features.csv
- data/processed/ml/test_features.csv
- data/processed/ml/train_labels.csv
- data/processed/ml/val_labels.csv
- data/processed/ml/test_labels.csv

Outputs:
- results/figures/pca_subtype_plot.png
- results/tables/pca_explained_variance.csv

Purpose:
Visualize whether breast cancer molecular subtypes naturally separate
in transcriptomic expression space.
"""

from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA


ML_DIR = Path("data/processed/ml")
FIGURE_DIR = Path("results/figures")
TABLE_DIR = Path("results/tables")

OUTPUT_FIGURE = FIGURE_DIR / "pca_subtype_plot.png"
OUTPUT_TABLE = TABLE_DIR / "pca_explained_variance.csv"

TARGET_COLUMN = "molecular_subtype"


def load_split(split_name):
    """Load one split and attach labels."""
    features = pd.read_csv(ML_DIR / f"{split_name}_features.csv")
    labels = pd.read_csv(ML_DIR / f"{split_name}_labels.csv")

    merged = features.merge(labels, on="sample_id", how="inner")
    merged["split"] = split_name

    return merged


def main():
    print("Loading ML-ready train/validation/test data...")

    train_df = load_split("train")
    val_df = load_split("val")
    test_df = load_split("test")

    df = pd.concat([train_df, val_df, test_df], axis=0, ignore_index=True)

    print("Combined shape:", df.shape)

    metadata_cols = ["sample_id", TARGET_COLUMN, "split"]
    gene_cols = [col for col in df.columns if col not in metadata_cols]

    print("Number of samples:", df.shape[0])
    print("Number of gene features:", len(gene_cols))

    X = df[gene_cols]

    print("Running PCA...")
    pca = PCA(n_components=2, random_state=42)
    pcs = pca.fit_transform(X)

    plot_df = pd.DataFrame({
        "sample_id": df["sample_id"],
        "molecular_subtype": df[TARGET_COLUMN],
        "split": df["split"],
        "PC1": pcs[:, 0],
        "PC2": pcs[:, 1],
    })

    explained_variance = pca.explained_variance_ratio_ * 100

    print("Explained variance:")
    print("PC1:", round(explained_variance[0], 2), "%")
    print("PC2:", round(explained_variance[1], 2), "%")

    print("\nSubtype counts:")
    print(plot_df["molecular_subtype"].value_counts())

    FIGURE_DIR.mkdir(parents=True, exist_ok=True)
    TABLE_DIR.mkdir(parents=True, exist_ok=True)

    variance_df = pd.DataFrame({
        "principal_component": ["PC1", "PC2"],
        "explained_variance_percent": explained_variance,
    })
    variance_df.to_csv(OUTPUT_TABLE, index=False)

    plt.figure(figsize=(8, 6))

    for subtype in sorted(plot_df["molecular_subtype"].unique()):
        subset = plot_df[plot_df["molecular_subtype"] == subtype]
        plt.scatter(
            subset["PC1"],
            subset["PC2"],
            label=subtype,
            alpha=0.75,
            s=35,
        )

    plt.xlabel(f"PC1 ({explained_variance[0]:.2f}% variance)")
    plt.ylabel(f"PC2 ({explained_variance[1]:.2f}% variance)")
    plt.title("TCGA-BRCA RNA-seq PCA by Molecular Subtype")
    plt.legend(title="Subtype")
    plt.tight_layout()

    plt.savefig(OUTPUT_FIGURE, dpi=300)
    plt.close()

    print("\nSaved figure:", OUTPUT_FIGURE)
    print("Saved variance table:", OUTPUT_TABLE)
    print("✅ PCA subtype plot created successfully.")


if __name__ == "__main__":
    main()
