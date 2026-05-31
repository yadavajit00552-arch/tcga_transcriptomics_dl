"""
Create subtype-specific gene lists for pathway enrichment.

Input:
- results/tables/logistic_regression_top_genes_by_subtype.csv

Outputs:
- results/tables/gene_lists/Basal_top_positive_genes.txt
- results/tables/gene_lists/Her2_top_positive_genes.txt
- results/tables/gene_lists/LumA_top_positive_genes.txt
- results/tables/gene_lists/LumB_top_positive_genes.txt

Purpose:
Prepare clean gene lists for downstream pathway enrichment analysis.
"""

from pathlib import Path
import pandas as pd


INPUT_PATH = Path("results/tables/logistic_regression_top_genes_by_subtype.csv")
OUTPUT_DIR = Path("results/tables/gene_lists")

TOP_N = 30


def main():
    print("Loading top Logistic Regression genes...")
    df = pd.read_csv(INPUT_PATH)

    print("Input shape:", df.shape)

    positive_df = df[df["direction"] == "positive"].copy()

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    for subtype in sorted(positive_df["subtype"].unique()):
        subtype_df = positive_df[positive_df["subtype"] == subtype].copy()
        subtype_df = subtype_df.sort_values("coefficient", ascending=False).head(TOP_N)

        genes = subtype_df["gene"].dropna().astype(str).tolist()

        output_path = OUTPUT_DIR / f"{subtype}_top_positive_genes.txt"

        with open(output_path, "w") as file:
            for gene in genes:
                file.write(gene + "\n")

        print(f"\n{subtype}: {len(genes)} genes")
        print(genes[:10])
        print("Saved:", output_path)

    print("\n✅ Subtype gene lists created successfully.")


if __name__ == "__main__":
    main()
