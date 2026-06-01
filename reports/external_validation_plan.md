# External Validation Plan: TCGA-BRCA Model on METABRIC

## Goal

Validate whether the TCGA-BRCA RNA-seq subtype classifier generalizes to an independent breast cancer cohort.

## Proposed external cohort

METABRIC breast cancer cohort.

## Why METABRIC?

- Independent breast cancer cohort
- Large sample size
- Widely used in breast cancer transcriptomics
- Contains clinical and molecular subtype information
- Suitable for testing cross-cohort model generalization

## Key challenge

The current model was trained on TCGA-BRCA RNA-seq data.

METABRIC expression data is commonly microarray-based, so direct validation requires careful harmonization.

## External validation workflow

1. Download METABRIC expression and clinical subtype metadata.
2. Identify subtype labels comparable to TCGA PAM50 labels.
3. Map gene identifiers to official gene symbols.
4. Intersect METABRIC genes with the TCGA selected 5,000 genes.
5. Keep only overlapping genes.
6. Reorder METABRIC genes to match TCGA feature order.
7. Handle missing TCGA-selected genes if some are unavailable.
8. Apply the scaler fitted on TCGA training data only.
9. Load the trained TCGA Logistic Regression model or retrain exactly using TCGA training data.
10. Predict METABRIC subtypes.
11. Compare predictions with METABRIC subtype labels.
12. Report accuracy, balanced accuracy, macro F1, and confusion matrix.
13. Interpret failure modes, especially LumA vs LumB confusion.

## Expected outcome

If the model generalizes well, it supports the idea that breast cancer subtype transcriptomic structure is robust across cohorts.

If performance drops, likely reasons include:

- RNA-seq vs microarray platform differences
- batch effects
- cohort-specific preprocessing
- different subtype annotation methods
- missing or mismatched gene symbols

## Recommended first implementation

Start with a script that only checks available METABRIC files and gene overlap.

Suggested script name:

src/external_validation/inspect_metabric_overlap.py

## Future improvement

Use batch correction or domain adaptation before prediction.

Possible approaches:

- ComBat batch correction
- z-score normalization within cohort
- training only on PAM50/core genes
- external validation using a reduced shared gene panel
