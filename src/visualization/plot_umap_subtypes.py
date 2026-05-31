"""
Create UMAP plot of TCGA-BRCA samples colored by molecular subtype.

Inputs:
- data/processed/ml/train_features.csv
- data/processed/ml/val_features.csv
- data/processed/ml/test_features.csv
- data/processed/ml/train_labels.csv
- data/processed/ml/val_labels.csv
- data/processed/ml/test_labels.csv

Output:
- results/figures/umap_subtype_plot.png

Purpose:
Visualize nonlinear transcriptomic structure and subtype clustering.
"""

from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import umap


ML_DIR = Path("data/processed/ml")
FIGURE_DIR = Path("results/figures")

OUTPUT_FIGURE = FIGURE_DIR / "umap_subtype_plot.png"

TARGET_COLUMN = "molecular_subtype"
RANDOM_SEED = 42


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

    print("Running UMAP...")
    reducer = umap.UMAP(
        n_neighbors=15,
        min_dist=0.1,
        n_components=2,
        metric="euclidean",
        random_state=RANDOM_SEED,
    )

    embedding = reducer.fit_transform(X)

    plot_df = pd.DataFrame({
        "sample_id": df["sample_id"],
        "molecular_subtype": df[TARGET_COLUMN],
        "split": df["split"],
        "UMAP1": embedding[:, 0],
        "UMAP2": embedding[:, 1],
    })

    print("\nSubtype counts:")
    print(plot_df["molecular_subtype"].value_counts())

    FIGURE_DIR.mkdir(parents=True, exist_ok=True)

    plt.figure(figsize=(8, 6))

    for subtype in sorted(plot_df["molecular_subtype"].unique()):
        subset = plot_df[plot_df["molecular_subtype"] == subtype]
        plt.scatter(
            subset["UMAP1"],
            subset["UMAP2"],
            label=subtype,
            alpha=0.75,
            s=35,
        )

    plt.xlabel("UMAP1")
    plt.ylabel("UMAP2")
    plt.title("TCGA-BRCA RNA-seq UMAP by Molecular Subtype")
    plt.legend(title="Subtype")
    plt.tight_layout()

    plt.savefig(OUTPUT_FIGURE, dpi=300)
    plt.close()

    print("\nSaved figure:", OUTPUT_FIGURE)
    print("✅ UMAP subtype plot created successfully.")


if __name__ == "__main__":
    main()
