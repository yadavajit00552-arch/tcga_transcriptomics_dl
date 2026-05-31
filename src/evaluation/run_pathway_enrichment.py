"""
Run pathway enrichment analysis for subtype-specific Logistic Regression gene lists.

Inputs:
- results/tables/gene_lists/Basal_top_positive_genes.txt
- results/tables/gene_lists/Her2_top_positive_genes.txt
- results/tables/gene_lists/LumA_top_positive_genes.txt
- results/tables/gene_lists/LumB_top_positive_genes.txt

Outputs:
- results/tables/pathway_enrichment/<Subtype>_<Library>_enrichment.csv
- results/tables/pathway_enrichment/pathway_enrichment_summary.csv

Purpose:
Interpret model-derived subtype gene lists using pathway enrichment.
"""

from pathlib import Path
import pandas as pd
import gseapy as gp


GENE_LIST_DIR = Path("results/tables/gene_lists")
OUTPUT_DIR = Path("results/tables/pathway_enrichment")

GENE_SET_LIBRARIES = [
    "MSigDB_Hallmark_2020",
    "KEGG_2021_Human",
    "Reactome_2022",
]


def read_gene_list(path):
    """Read one gene list text file."""
    with open(path, "r") as file:
        genes = [line.strip() for line in file if line.strip()]
    return genes


def safe_name(text):
    """Make safe filename from library/subtype name."""
    return text.replace(" ", "_").replace("/", "_")


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    gene_list_files = sorted(GENE_LIST_DIR.glob("*_top_positive_genes.txt"))

    if not gene_list_files:
        raise FileNotFoundError(f"No gene lists found in {GENE_LIST_DIR}")

    summary_rows = []

    for gene_file in gene_list_files:
        subtype = gene_file.name.replace("_top_positive_genes.txt", "")
        genes = read_gene_list(gene_file)

        print(f"\nSubtype: {subtype}")
        print(f"Number of genes: {len(genes)}")
        print("First 10 genes:", genes[:10])

        for library in GENE_SET_LIBRARIES:
            print(f"Running enrichment: {library}")

            try:
                enr = gp.enrichr(
                    gene_list=genes,
                    gene_sets=library,
                    organism="human",
                    outdir=None,
                    cutoff=1.0,
                )

                result = enr.results.copy()

                output_path = OUTPUT_DIR / f"{subtype}_{safe_name(library)}_enrichment.csv"
                result.to_csv(output_path, index=False)

                print("Saved:", output_path)

                if not result.empty:
                    top = result.sort_values("Adjusted P-value").iloc[0]

                    summary_rows.append({
                        "subtype": subtype,
                        "library": library,
                        "top_term": top.get("Term"),
                        "adjusted_p_value": top.get("Adjusted P-value"),
                        "combined_score": top.get("Combined Score"),
                        "overlap": top.get("Overlap"),
                        "genes": top.get("Genes"),
                    })

                    print("Top term:", top.get("Term"))
                    print("Adjusted P-value:", top.get("Adjusted P-value"))
                else:
                    summary_rows.append({
                        "subtype": subtype,
                        "library": library,
                        "top_term": "No result",
                        "adjusted_p_value": None,
                        "combined_score": None,
                        "overlap": None,
                        "genes": None,
                    })

            except Exception as error:
                print(f"⚠️ Enrichment failed for {subtype} - {library}: {error}")

                summary_rows.append({
                    "subtype": subtype,
                    "library": library,
                    "top_term": "FAILED",
                    "adjusted_p_value": None,
                    "combined_score": None,
                    "overlap": None,
                    "genes": None,
                })

    summary = pd.DataFrame(summary_rows)
    summary_path = OUTPUT_DIR / "pathway_enrichment_summary.csv"
    summary.to_csv(summary_path, index=False)

    print("\nSaved summary:", summary_path)
    print("\nSummary preview:")
    print(summary)

    print("\n✅ Pathway enrichment completed.")


if __name__ == "__main__":
    main()
