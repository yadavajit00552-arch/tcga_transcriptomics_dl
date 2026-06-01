# METABRIC External Validation Results

## Goal

The goal of this step was to test whether the TCGA-BRCA subtype classifier can generalize to an independent breast cancer cohort.

## External cohort

External validation cohort:

METABRIC breast cancer cohort from cBioPortal.

## Why METABRIC?

METABRIC is an independent breast cancer cohort with expression data and subtype annotations. It is useful for testing whether subtype-associated transcriptomic signals learned from TCGA-BRCA transfer to another breast cancer dataset.

## Key challenge

TCGA-BRCA expression data are RNA-seq based, while METABRIC expression data are Illumina microarray based.

This creates a platform-shift problem:

TCGA RNA-seq scale  
↓  
model learns TCGA expression boundaries  
↓  
METABRIC raw microarray scale is different  
↓  
external prediction may fail unless expression is normalized carefully

## Gene overlap

| Item | Value |
|---|---:|
| TCGA selected ML genes | 5,000 |
| METABRIC overlapping genes | 4,311 |
| Missing TCGA-selected genes in METABRIC | 689 |
| Gene overlap percentage | 86.22% |

## METABRIC validation dataset

Only four subtype classes were retained to match the TCGA model:

| Subtype | Samples |
|---|---:|
| LumA | 700 |
| LumB | 475 |
| Her2 | 224 |
| Basal | 209 |
| Total | 1,608 |

Classes excluded:

- Normal
- claudin-low
- NC
- missing subtype labels

## Raw METABRIC expression validation

The first external validation attempt used raw/processed METABRIC microarray expression values.

Result:

| Metric | Value |
|---|---:|
| Accuracy | 0.4353 |
| Balanced accuracy | 0.2500 |
| Macro F1 | 0.1516 |
| Weighted F1 | 0.2641 |

The model predicted almost all samples as LumA. This showed strong cross-platform scale mismatch between TCGA RNA-seq and METABRIC raw microarray data.

## METABRIC z-score external validation

A second validation was performed using METABRIC z-score expression values.

This substantially improved performance.

| Metric | Value |
|---|---:|
| Accuracy | 0.8178 |
| Balanced accuracy | 0.7840 |
| Macro F1 | 0.8057 |
| Weighted F1 | 0.8161 |

## METABRIC z-score confusion matrix

| True / Predicted | Basal | Her2 | LumA | LumB |
|---|---:|---:|---:|---:|
| Basal | 165 | 31 | 4 | 9 |
| Her2 | 1 | 154 | 21 | 48 |
| LumA | 0 | 13 | 647 | 40 |
| LumB | 0 | 8 | 118 | 349 |

## Interpretation

The z-score external validation result shows that the TCGA-trained Logistic Regression classifier captures transferable breast cancer subtype biology.

Strongest external validation performance was observed for LumA and Basal samples.

The main classification errors were:

- LumB misclassified as LumA
- Her2 misclassified as LumB
- Some Basal samples misclassified as Her2

The LumA/LumB confusion is biologically reasonable because both are luminal subtypes with overlapping hormone-response expression programs. LumB separation often depends more strongly on proliferation and cell-cycle expression.

## Main conclusion

Strict external validation using raw METABRIC microarray expression failed due to platform shift. However, using METABRIC z-score expression enabled successful cross-cohort validation, achieving 0.8178 accuracy and 0.8057 macro F1.

This supports the conclusion that breast cancer molecular subtype signals are robust and transferable across cohorts when platform-aware normalization is used.

## Report-ready summary

External validation on METABRIC demonstrated that cross-platform normalization is essential. A TCGA-trained Logistic Regression model using 4,311 genes shared with METABRIC achieved 0.897 accuracy on TCGA test data. When applied to raw METABRIC microarray expression, predictions collapsed to LumA due to platform shift. After using METABRIC z-score expression, external validation improved substantially to 0.818 accuracy and 0.806 macro F1, supporting the transferability of subtype-associated transcriptomic signals across independent breast cancer cohorts.
