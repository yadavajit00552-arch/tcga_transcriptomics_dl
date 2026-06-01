"""
Check METABRIC expression/subtype availability and overlap with TCGA ML genes.

Purpose:
- Load METABRIC mRNA expression matrix.
- Load METABRIC clinical patient metadata.
- Identify PAM50-like subtype labels.
- Check overlap between METABRIC genes and TCGA selected ML genes.
"""

from pathlib import Path
import pandas as pd


METABRIC_DIR = Path("data/external/metabric/brca_metabric")

METABRIC_EXPR_FILE = METABRIC_DIR / "data_mrna_illumina_microarray.txt"
METABRIC_ZSCORE_FILE = METABRIC_DIR / "data_mrna_illumina_microarray_zscores_ref_diploid_samples.txt"
METABRIC_CLINICAL_FILE = METABRIC_DIR / "data_clinical_patient.txt"

TCGA_FEATURE_FILE = Path("data/processed/ml/train_features.csv")

OUTPUT_DIR = Path("results/tables/external_validation")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def load_cbioportal_clinical(path):
    """
    cBioPortal clinical files contain metadata rows starting after the header.
    The real data starts after rows:
    0 = description
    1 = datatype
    2 = priority
    3 = stable column name
    So we skip rows 1, 2, and 3, keeping original header.
    """
    df = pd.read_csv(path, sep="\t", skiprows=[1, 2, 3])
    return df


def main():
    print("Loading METABRIC expression file...")
    expr = pd.read_csv(METABRIC_EXPR_FILE, sep="\t")
    print("METABRIC expression shape:", expr.shape)

    print("\nLoading METABRIC z-score expression file...")
    zexpr = pd.read_csv(METABRIC_ZSCORE_FILE, sep="\t")
    print("METABRIC z-score expression shape:", zexpr.shape)

    print("\nLoading METABRIC clinical patient file...")
    clinical = load_cbioportal_clinical(METABRIC_CLINICAL_FILE)
    print("METABRIC clinical shape:", clinical.shape)

    print("\nClinical columns:")
    print(clinical.columns.tolist())

    subtype_col = "Pam50 + Claudin-low subtype"

    if subtype_col not in clinical.columns:
        raise ValueError(f"Subtype column not found: {subtype_col}")

    print("\nMETABRIC subtype counts:")
    print(clinical[subtype_col].value_counts(dropna=False))

    # Expression genes
    metabric_genes = set(expr["Hugo_Symbol"].dropna().astype(str))
    metabric_z_genes = set(zexpr["Hugo_Symbol"].dropna().astype(str))

    print("\nNumber of METABRIC expression genes:", len(metabric_genes))
    print("Number of METABRIC z-score genes:", len(metabric_z_genes))

    # TCGA selected genes
    print("\nLoading TCGA ML train features...")
    X_train = pd.read_csv(TCGA_FEATURE_FILE)
    tcga_genes = [col for col in X_train.columns if col != "sample_id"]
    tcga_gene_set = set(tcga_genes)

    print("Number of TCGA selected ML genes:", len(tcga_genes))

    overlap_expr = sorted(tcga_gene_set.intersection(metabric_genes))
    overlap_zexpr = sorted(tcga_gene_set.intersection(metabric_z_genes))

    print("\nOverlap with METABRIC expression genes:", len(overlap_expr))
    print("Overlap with METABRIC z-score genes:", len(overlap_zexpr))

    missing_from_metabric = sorted(tcga_gene_set - metabric_genes)
    print("TCGA selected genes missing from METABRIC expression:", len(missing_from_metabric))

    # Sample overlap
    expression_samples = set(expr.columns[2:])
    z_expression_samples = set(zexpr.columns[2:])

    patient_col = "#Patient Identifier"
    clinical_samples = set(clinical[patient_col].astype(str))

    overlap_samples_expr = sorted(expression_samples.intersection(clinical_samples))
    overlap_samples_zexpr = sorted(z_expression_samples.intersection(clinical_samples))

    print("\nExpression samples:", len(expression_samples))
    print("Z-score expression samples:", len(z_expression_samples))
    print("Clinical patients:", len(clinical_samples))
    print("Expression-clinical overlap:", len(overlap_samples_expr))
    print("Z-score expression-clinical overlap:", len(overlap_samples_zexpr))

    # Save summary
    summary = pd.DataFrame([
        {
            "item": "metabric_expression_shape",
            "value": str(expr.shape),
        },
        {
            "item": "metabric_zscore_expression_shape",
            "value": str(zexpr.shape),
        },
        {
            "item": "metabric_clinical_shape",
            "value": str(clinical.shape),
        },
        {
            "item": "tcga_selected_genes",
            "value": len(tcga_genes),
        },
        {
            "item": "overlap_tcga_metabric_expression_genes",
            "value": len(overlap_expr),
        },
        {
            "item": "overlap_tcga_metabric_zscore_genes",
            "value": len(overlap_zexpr),
        },
        {
            "item": "expression_clinical_sample_overlap",
            "value": len(overlap_samples_expr),
        },
        {
            "item": "zscore_expression_clinical_sample_overlap",
            "value": len(overlap_samples_zexpr),
        },
    ])

    summary_file = OUTPUT_DIR / "metabric_tcga_overlap_summary.csv"
    overlap_file = OUTPUT_DIR / "tcga_metabric_overlapping_genes.txt"
    missing_file = OUTPUT_DIR / "tcga_genes_missing_from_metabric.txt"

    summary.to_csv(summary_file, index=False)
    overlap_file.write_text("\n".join(overlap_expr) + "\n")
    missing_file.write_text("\n".join(missing_from_metabric) + "\n")

    print("\nSaved:", summary_file)
    print("Saved:", overlap_file)
    print("Saved:", missing_file)

    print("\n✅ METABRIC-TCGA overlap check completed.")


if __name__ == "__main__":
    main()
