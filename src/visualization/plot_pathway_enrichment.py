"""
Plot top pathway enrichment terms.

Input:
- results/tables/pathway_enrichment/pathway_enrichment_summary.csv

Output:
- results/figures/pathway_enrichment_top_terms.png

Purpose:
Visualize top pathway enrichment results from subtype-specific model-derived gene lists.
"""

from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


INPUT_PATH = Path("results/tables/pathway_enrichment/pathway_enrichment_summary.csv")
OUTPUT_PATH = Path("results/figures/pathway_enrichment_top_terms.png")


def shorten_term(term, max_length=45):
    """Shorten long pathway names for plotting."""
    if pd.isna(term):
        return "No result"

    term = str(term)

    if term == "FAILED":
        return "FAILED"

    if len(term) <= max_length:
        return term

    return term[:max_length] + "..."


def main():
    print("Loading pathway enrichment summary...")
    df = pd.read_csv(INPUT_PATH)

    print("Input shape:", df.shape)

    print("\nInput preview:")
    print(df)

    # Remove failed rows and rows without adjusted p-values
    plot_df = df.copy()
    plot_df = plot_df[plot_df["top_term"] != "FAILED"].copy()
    plot_df = plot_df.dropna(subset=["adjusted_p_value"]).copy()

    if plot_df.empty:
        raise ValueError("No valid enrichment results found for plotting.")

    plot_df["neg_log10_adj_p"] = -np.log10(plot_df["adjusted_p_value"].astype(float))
    plot_df["label"] = (
        plot_df["subtype"]
        + " | "
        + plot_df["library"]
        + "\n"
        + plot_df["top_term"].apply(shorten_term)
    )

    plot_df = plot_df.sort_values("neg_log10_adj_p", ascending=True)

    print("\nValid enrichment rows for plotting:")
    print(plot_df[["subtype", "library", "top_term", "adjusted_p_value", "neg_log10_adj_p"]])

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    plt.figure(figsize=(11, 7))
    plt.barh(plot_df["label"], plot_df["neg_log10_adj_p"])

    plt.xlabel("-log10 adjusted p-value")
    plt.ylabel("Subtype | Library | Top pathway")
    plt.title("Top Pathway Enrichment Terms from Model-Derived Subtype Genes")

    significance_cutoff = -np.log10(0.05)
    plt.axvline(significance_cutoff, linestyle="--", linewidth=1)
    plt.text(
        significance_cutoff,
        len(plot_df) - 0.5,
        " FDR 0.05",
        va="center",
    )

    plt.tight_layout()
    plt.savefig(OUTPUT_PATH, dpi=300, bbox_inches="tight")
    plt.close()

    print("\nSaved figure:", OUTPUT_PATH)
    print("✅ Pathway enrichment plot created successfully.")


if __name__ == "__main__":
    main()
