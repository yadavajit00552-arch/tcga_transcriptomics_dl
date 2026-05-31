"""
Plot top positive Logistic Regression genes by subtype.

Input:
- results/tables/logistic_regression_top_genes_by_subtype.csv

Output:
- results/figures/logistic_regression_top_genes_by_subtype.png

Purpose:
Visualize subtype-specific genes learned by the best-performing model.
"""

from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt


INPUT_PATH = Path("results/tables/logistic_regression_top_genes_by_subtype.csv")
OUTPUT_PATH = Path("results/figures/logistic_regression_top_genes_by_subtype.png")

TOP_N = 10


def main():
    print("Loading Logistic Regression top genes...")
    df = pd.read_csv(INPUT_PATH)

    print("Input shape:", df.shape)

    positive_df = df[df["direction"] == "positive"].copy()

    subtypes = sorted(positive_df["subtype"].unique())

    print("\nSubtypes found:")
    print(subtypes)

    plot_rows = []

    for subtype in subtypes:
        subtype_df = positive_df[positive_df["subtype"] == subtype].copy()
        subtype_df = subtype_df.sort_values("coefficient", ascending=False).head(TOP_N)
        subtype_df["gene_label"] = subtype_df["gene"] + " (" + subtype + ")"
        plot_rows.append(subtype_df)

        print(f"\nTop {TOP_N} positive genes for {subtype}:")
        print(subtype_df[["gene", "coefficient"]])

    plot_df = pd.concat(plot_rows, axis=0, ignore_index=True)

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    # Create one figure with one horizontal bar panel per subtype
    fig, axes = plt.subplots(
        nrows=len(subtypes),
        ncols=1,
        figsize=(8, 3.2 * len(subtypes)),
        sharex=False,
    )

    if len(subtypes) == 1:
        axes = [axes]

    for ax, subtype in zip(axes, subtypes):
        subtype_df = plot_df[plot_df["subtype"] == subtype].copy()
        subtype_df = subtype_df.sort_values("coefficient", ascending=True)

        ax.barh(subtype_df["gene"], subtype_df["coefficient"])
        ax.set_title(f"Top positive genes for {subtype}")
        ax.set_xlabel("Logistic Regression coefficient")
        ax.set_ylabel("Gene")

    plt.suptitle(
        "TCGA-BRCA subtype-associated genes from Logistic Regression",
        y=1.02,
        fontsize=14,
    )

    plt.tight_layout()
    plt.savefig(OUTPUT_PATH, dpi=300, bbox_inches="tight")
    plt.close()

    print("\nSaved figure:", OUTPUT_PATH)
    print("✅ Logistic Regression top gene plot created successfully.")


if __name__ == "__main__":
    main()
