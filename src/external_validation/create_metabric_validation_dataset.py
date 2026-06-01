"""
Create METABRIC external validation dataset aligned to TCGA selected genes.

Inputs:
- METABRIC expression:
  data/external/metabric/brca_metabric/data_mrna_illumina_microarray.txt

- METABRIC clinical:
  data/external/metabric/brca_metabric/data_clinical_patient.txt

- TCGA selected ML features:
  data/processed/ml/train_features.csv

Output:
- data/processed/external_validation/metabric_4class_expression_overlap.csv
- data/processed/external_validation/metabric_overlap_gene_order.txt

Important:
METABRIC is microarray-based, while TCGA is RNA-seq-based.
This script prepares a harmonized overlap dataset but does not yet make predictions.
"""

from pathlib import Path
import pandas as pd


METABRIC_DIR = Path("data/external/metabric/brca_metabric")

METABRIC_EXPR_FILE = METABRIC_DIR / "data_mrna_illumina_microarray.txt"
METABRIC_CLINICAL_FILE = METABRIC_DIR / "data_clinical_patient.txt"

TCGA_FEATURE_FILE = Path("data/processed/ml/train_features.csv")

OUTPUT_DIR = Path("data/processed/external_validation")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

OUTPUT_DATASET = OUTPUT_DIR / "metabric_4class_expression_overlap.csv"
OUTPUT_GENE_ORDER = OUTPUT_DIR / "metabric_overlap_gene_order.txt"
OUTPUT_SUMMARY = OUTPUT_DIR / "metabric_validation_dataset_summary.csv"


def load_cbioportal_clinical(path):
    """
    cBioPortal clinical files contain 4 header-like rows.
    Keep the visible column names and skip metadata rows 1, 2, and 3.
    """
    return pd.read_csv(path, sep="\t", skiprows=[1, 2, 3])


def main():
    print("Loading TCGA selected feature list...")
    tcga_train = pd.read_csv(TCGA_FEATURE_FILE)
    tcga_genes = [col for col in tcga_train.columns if col != "sample_id"]
    print("TCGA selected genes:", len(tcga_genes))

    print("\nLoading METABRIC expression...")
    expr = pd.read_csv(METABRIC_EXPR_FILE, sep="\t")
    print("Raw METABRIC expression shape:", expr.shape)

    # Remove duplicated gene symbols if present
    before = expr.shape[0]
    expr = expr.dropna(subset=["Hugo_Symbol"])
    expr["Hugo_Symbol"] = expr["Hugo_Symbol"].astype(str)
    expr = expr.drop_duplicates(subset=["Hugo_Symbol"], keep="first")
    after = expr.shape[0]
    print(f"Removed duplicated/empty gene rows: {before} -> {after}")

    # Gene x sample -> sample x gene
    expr = expr.set_index("Hugo_Symbol")
    if "Entrez_Gene_Id" in expr.columns:
        expr = expr.drop(columns=["Entrez_Gene_Id"])

    metabric_genes = set(expr.index)
    overlap_genes = [gene for gene in tcga_genes if gene in metabric_genes]

    print("Overlapping genes in TCGA order:", len(overlap_genes))
    print("Missing TCGA genes:", len(tcga_genes) - len(overlap_genes))

    metabric_expr_samples = expr.loc[overlap_genes].T
    metabric_expr_samples.index.name = "sample_id"
    metabric_expr_samples = metabric_expr_samples.reset_index()

    print("METABRIC expression sample x gene shape:", metabric_expr_samples.shape)

    print("\nLoading METABRIC clinical data...")
    clinical = load_cbioportal_clinical(METABRIC_CLINICAL_FILE)

    patient_col = "#Patient Identifier"
    subtype_col = "Pam50 + Claudin-low subtype"

    clinical_small = clinical[[patient_col, subtype_col]].copy()
    clinical_small = clinical_small.rename(
        columns={
            patient_col: "sample_id",
            subtype_col: "molecular_subtype",
        }
    )

    print("Clinical subtype counts before filtering:")
    print(clinical_small["molecular_subtype"].value_counts(dropna=False))

    keep_classes = ["LumA", "LumB", "Basal", "Her2"]
    clinical_4class = clinical_small[
        clinical_small["molecular_subtype"].isin(keep_classes)
    ].copy()

    print("\nClinical subtype counts after 4-class filtering:")
    print(clinical_4class["molecular_subtype"].value_counts())

    print("\nMerging METABRIC expression with subtype labels...")
    merged = metabric_expr_samples.merge(
        clinical_4class,
        on="sample_id",
        how="inner",
    )

    print("Merged METABRIC validation dataset shape:", merged.shape)

    print("\nMerged subtype counts:")
    print(merged["molecular_subtype"].value_counts())

    # Put metadata columns first
    ordered_cols = ["sample_id", "molecular_subtype"] + overlap_genes
    merged = merged[ordered_cols]

    merged.to_csv(OUTPUT_DATASET, index=False)
    OUTPUT_GENE_ORDER.write_text("\n".join(overlap_genes) + "\n")

    summary = pd.DataFrame([
        {"item": "tcga_selected_genes", "value": len(tcga_genes)},
        {"item": "metabric_overlapping_genes", "value": len(overlap_genes)},
        {"item": "metabric_missing_tcga_genes", "value": len(tcga_genes) - len(overlap_genes)},
        {"item": "metabric_validation_samples", "value": merged.shape[0]},
        {"item": "metabric_validation_features", "value": len(overlap_genes)},
        {"item": "LumA_samples", "value": int((merged["molecular_subtype"] == "LumA").sum())},
        {"item": "LumB_samples", "value": int((merged["molecular_subtype"] == "LumB").sum())},
        {"item": "Basal_samples", "value": int((merged["molecular_subtype"] == "Basal").sum())},
        {"item": "Her2_samples", "value": int((merged["molecular_subtype"] == "Her2").sum())},
    ])

    summary.to_csv(OUTPUT_SUMMARY, index=False)

    print("\nSaved:", OUTPUT_DATASET)
    print("Saved:", OUTPUT_GENE_ORDER)
    print("Saved:", OUTPUT_SUMMARY)

    print("\n✅ METABRIC validation dataset created successfully.")


if __name__ == "__main__":
    main()
