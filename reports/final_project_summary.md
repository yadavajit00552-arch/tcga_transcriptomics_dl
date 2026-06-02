# Final Project Summary

## Project Title

Interpretable Cross-Cohort Transcriptomic Classification of Breast Cancer Molecular Subtypes Using TCGA-BRCA and METABRIC

## Main Objective

To classify breast cancer molecular subtypes from TCGA-BRCA RNA-seq gene-expression data and validate whether the learned subtype signals transfer to an independent cohort, METABRIC.

## Datasets

| Dataset | Platform | Role |
|---|---|---|
| TCGA-BRCA | RNA-seq | Training, validation, testing |
| METABRIC | Illumina microarray | External validation |

## Classification Task

Four-class breast cancer molecular subtype classification:

| Class | Meaning |
|---|---|
| LumA | Luminal A |
| LumB | Luminal B |
| Basal | Basal-like |
| Her2 | HER2-enriched |

The Normal class was removed because it had few samples and the project focused on tumor subtype classification.

## TCGA Dataset Summary

| Item | Value |
|---|---:|
| Total modeling samples | 821 |
| Original gene features | 20,530 |
| Selected ML genes | 5,000 |
| Train samples | 524 |
| Validation samples | 132 |
| Test samples | 165 |

## TCGA Class Distribution

| Subtype | Samples |
|---|---:|
| LumA | 421 |
| LumB | 192 |
| Basal | 141 |
| Her2 | 67 |

## Models Compared

| Model | Test Accuracy | Balanced Accuracy | Macro F1 | Weighted F1 |
|---|---:|---:|---:|---:|
| Logistic Regression | 0.8909 | 0.8995 | 0.8821 | 0.8909 |
| MLP Neural Network | 0.8606 | 0.8477 | 0.8561 | 0.8555 |
| Random Forest | 0.8727 | 0.7826 | 0.8204 | 0.8635 |

## Best Model

Logistic Regression was the best model.

Interpretation:

The strong Logistic Regression performance suggests that breast cancer subtype signals are highly structured and largely linearly separable in transcriptomic space.

## Biological Interpretation

| Subtype | Important Signals |
|---|---|
| Her2 | ERBB2, GRB7, ERBB2 signaling |
| LumA | Estrogen response, hormone-response biology |
| LumB | E2F targets, cell cycle, proliferation |
| Basal | Distinct basal-like transcriptomic signature |

## Explainability

Model interpretation was performed using:

- Logistic Regression coefficients
- SHAP analysis
- Pathway enrichment

These analyses supported that the model learned biologically meaningful subtype signals.

## METABRIC External Validation

### Gene Overlap

| Item | Value |
|---|---:|
| TCGA selected genes | 5,000 |
| Shared TCGA-METABRIC genes | 4,311 |
| Missing TCGA genes in METABRIC | 689 |
| Gene overlap | 86.22% |

### METABRIC Validation Samples

| Subtype | Samples |
|---|---:|
| LumA | 700 |
| LumB | 475 |
| Her2 | 224 |
| Basal | 209 |
| Total | 1,608 |

## External Validation Results

Raw METABRIC microarray expression caused poor transfer due to platform shift.

Using METABRIC z-score expression improved external validation.

| Dataset | Accuracy | Balanced Accuracy | Macro F1 | Weighted F1 |
|---|---:|---:|---:|---:|
| TCGA test using shared genes | 0.8970 | 0.9060 | 0.8934 | 0.8970 |
| METABRIC z-score external validation | 0.8178 | 0.7840 | 0.8057 | 0.8161 |


## METABRIC Survival Analysis

To add clinical relevance, survival analysis was performed in METABRIC using both true subtype labels and TCGA-model-predicted subtype labels.

### Median survival by true subtype

| True subtype | Median survival months |
|---|---:|
| LumA | 130.08 |
| LumB | 104.10 |
| Her2 | 97.07 |
| Basal | 85.50 |

### Median survival by predicted subtype

| Predicted subtype | Median survival months |
|---|---:|
| LumA | 128.07 |
| LumB | 108.52 |
| Basal | 84.28 |
| Her2 | 77.30 |

Important log-rank comparisons showed significant survival separation, especially LumA vs LumB and Her2 vs LumA. This suggests that model-predicted subtypes preserve clinically meaningful survival information in METABRIC.


## Key Scientific Conclusion

Breast cancer molecular subtype identity is strongly encoded in transcriptomic data. A TCGA-trained classifier can transfer to an independent cohort when platform-aware normalization is used.

## Main Technical Lesson

External validation is affected by platform shift. TCGA RNA-seq and METABRIC microarray data are not directly comparable in raw form. Z-score normalization improved cross-cohort transfer.

## Limitations

1. TCGA and METABRIC use different expression platforms.
2. External validation was performed on one independent cohort.
3. The model used selected genes, not the full transcriptome.
4. More batch-correction methods were not yet tested.
5. Survival analysis was not yet included.

## Future Work

1. Test batch-correction methods such as ComBat.
2. Add more external breast cancer datasets.
3. Compare Elastic Net, SVM, and XGBoost.
4. Perform survival analysis using predicted subtype probabilities.
5. Add calibration analysis.
6. Extend the pipeline to pan-cancer subtype classification.

## Final Interview Summary

This project built a reproducible TCGA-BRCA transcriptomic classification pipeline using classical machine learning and neural networks. Logistic Regression performed best and recovered known breast cancer subtype biology through coefficients, SHAP, and pathway enrichment. External validation on METABRIC showed that raw cross-platform prediction failed due to RNA-seq versus microarray scale shift, but METABRIC z-score expression improved performance to 0.818 accuracy and 0.806 macro F1. This supports that subtype transcriptomic signals are transferable across cohorts when normalization is handled carefully.
