"""
Create METABRIC z-score external validation dataset aligned to TCGA selected genes.

Inputs:
- METABRIC z-score expression:
  data/external/metabric/brca_metabric/data_mrna_illumina_microarray_zscores_ref_diploid_samples.txt

- METABRIC clinical:
  data/external/metabric/brca_metabric/data_clinical_patient.txt

- TCGA selected ML features:
  data/processed/ml/train_features.csv

Output:
- data/processed/external_validation/metabric_4class_zscore_expression_overlap.csv
- data/processed/external_validation/metabric_zscore_overlap_gene_order.txt

Purpose:
This dataset is intended for cross-platform validation, because METABRIC is microarray-based
while TCGA is RNA-seq-based.
"""

from pathlib import Path
import pandas as pd


METABRIC_DIR = Path("data/external/metabric/brca_metabric")

METABRIC_ZSCORE_FILE = METABRIC_DIR / "data_mrna_illumina_microarray_zscores_ref_diploid_samples.txt"
METABRIC_CLINICAL_FILE = METABRIC_DIR / "data_clinical_patient.txt"

TCGA_FEATURE_FILE = Path("data/processed/ml/train_features.csv")

OUTPUT_DIR = Path("data/processed/external_validation")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

OUTPUT_DATASET = OUTPUT_DIR / "metabric_4class_zscore_expression_overlap.csv"
OUTPUT_GENE_ORDER = OUTPUT_DIR / "metabric_zscore_overlap_gene_order.txt"
OUTPUT_SUMMARY = OUTPUT_DIR / "metabric_zscore_validation_dataset_summary.csv"


def load_cbioportal_clinical(path):
    return pd.read_csv(path, sep="\t", skiprows=[1, 2, 3])


def main():
    print("Loading TCGA selected feature list...")
    tcga_train = pd.read_csv(TCGA_FEATURE_FILE)
    tcga_genes = [col for col in tcga_train.columns if col != "sample_id"]
    print("TCGA selected genes:", len(tcga_genes))

    print("\nLoading METABRIC z-score expression...")
    zexpr = pd.read_csv(METABRIC_ZSCORE_FILE, sep="\t")
    print("Raw METABRIC z-score expression shape:", zexpr.shape)

    before = zexpr.shape[0]
    zexpr = zexpr.dropna(subset=["Hugo_Symbol"])
    zexpr["Hugo_Symbol"] = zexpr["Hugo_Symbol"].astype(str)
    zexpr = zexpr.drop_duplicates(subset=["Hugo_Symbol"], keep="first")
    after = zexpr.shape[0]
    print(f"Removed duplicated/empty gene rows: {before} -> {after}")

    zexpr = zexpr.set_index("Hugo_Symbol")

    if "Entrez_Gene_Id" in zexpr.columns:
        zexpr = zexpr.drop(columns=["Entrez_Gene_Id"])

    metabric_genes = set(zexpr.index)
    overlap_genes = [gene for gene in tcga_genes if gene in metabric_genes]

    print("Overlapping genes in TCGA order:", len(overlap_genes))
    print("Missing TCGA genes:", len(tcga_genes) - len(overlap_genes))

    metabric_zexpr_samples = zexpr.loc[overlap_genes].T
    metabric_zexpr_samples.index.name = "sample_id"
    metabric_zexpr_samples = metabric_zexpr_samples.reset_index()

    print("METABRIC z-score sample x gene shape:", metabric_zexpr_samples.shape)

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

    print("\nMerging METABRIC z-score expression with subtype labels...")
    merged = metabric_zexpr_samples.merge(
        clinical_4class,
        on="sample_id",
        how="inner",
    )

    print("Merged METABRIC z-score validation dataset shape:", merged.shape)

    print("\nMerged subtype counts:")
    print(merged["molecular_subtype"].value_counts())

    ordered_cols = ["sample_id", "molecular_subtype"] + overlap_genes
    merged = merged[ordered_cols]

    merged.to_csv(OUTPUT_DATASET, index=False)
    OUTPUT_GENE_ORDER.write_text("\n".join(overlap_genes) + "\n")

    summary = pd.DataFrame([
        {"item": "tcga_selected_genes", "value": len(tcga_genes)},
        {"item": "metabric_zscore_overlapping_genes", "value": len(overlap_genes)},
        {"item": "metabric_missing_tcga_genes", "value": len(tcga_genes) - len(overlap_genes)},
        {"item": "metabric_zscore_validation_samples", "value": merged.shape[0]},
        {"item": "metabric_zscore_validation_features", "value": len(overlap_genes)},
        {"item": "LumA_samples", "value": int((merged["molecular_subtype"] == "LumA").sum())},
        {"item": "LumB_samples", "value": int((merged["molecular_subtype"] == "LumB").sum())},
        {"item": "Basal_samples", "value": int((merged["molecular_subtype"] == "Basal").sum())},
        {"item": "Her2_samples", "value": int((merged["molecular_subtype"] == "Her2").sum())},
    ])

    summary.to_csv(OUTPUT_SUMMARY, index=False)

    print("\nSaved:", OUTPUT_DATASET)
    print("Saved:", OUTPUT_GENE_ORDER)
    print("Saved:", OUTPUT_SUMMARY)

    print("\n✅ METABRIC z-score validation dataset created successfully.")


if __name__ == "__main__":
    main()
