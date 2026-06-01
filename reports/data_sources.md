# Data Sources

## Overview

This project used two publicly available breast cancer transcriptomics datasets:

| Dataset | Platform | Role in Project |
|---|---|---|
| TCGA-BRCA | RNA-seq | Main training, validation, and testing cohort |
| METABRIC | Illumina microarray | Independent external validation cohort |

The main aim was to train breast cancer subtype classifiers on TCGA-BRCA RNA-seq expression data and test whether the learned subtype signals transfer to METABRIC after platform-aware normalization.

---

## 1. TCGA-BRCA

### Dataset name

TCGA Breast Invasive Carcinoma cohort.

### Source

UCSC Xena TCGA-BRCA data hub.

### Data used

| File / Dataset | Purpose |
|---|---|
| TCGA-BRCA gene-expression matrix | RNA-seq expression features |
| BRCA clinical metadata / clinical matrix | PAM50-related subtype labels and clinical annotations |

### Expression data

The project used TCGA-BRCA RNA-seq gene-expression data.

Raw expression matrix summary:

| Item | Value |
|---|---:|
| Genes | 20,530 |
| Total samples before filtering | 1,218 |
| Primary tumor samples | 1,097 |

### Metadata

PAM50-related subtype metadata were fetched from the UCSC Xena clinical matrix.

Subtype fields inspected included:

- PAM50Call_RNAseq
- PAM50_mRNA_nature2012
- ER_Status_nature2012
- PR_Status_nature2012
- HER2_Final_Status_nature2012

### Final TCGA modeling dataset

After merging expression with subtype labels and removing the small Normal class:

| Item | Value |
|---|---:|
| Final modeling samples | 821 |
| Classes | LumA, LumB, Basal, Her2 |
| Original gene features | 20,530 |
| Selected ML features | 5,000 |

### TCGA class distribution

| Subtype | Samples |
|---|---:|
| LumA | 421 |
| LumB | 192 |
| Basal | 141 |
| Her2 | 67 |

---

## 2. METABRIC

### Dataset name

Molecular Taxonomy of Breast Cancer International Consortium cohort.

### Source

cBioPortal METABRIC breast cancer study download.

### Data archive used

The METABRIC study archive was downloaded manually from cBioPortal and placed locally under:

    data/external/metabric/

After extraction, the main folder used was:

    data/external/metabric/brca_metabric/

### Main METABRIC files used

| File | Purpose |
|---|---|
| data_mrna_illumina_microarray.txt | Raw/processed microarray expression |
| data_mrna_illumina_microarray_zscores_ref_diploid_samples.txt | Z-score expression used for successful external validation |
| data_clinical_patient.txt | PAM50 subtype labels and patient-level clinical data |
| data_clinical_sample.txt | Sample-level clinical data |

### METABRIC expression data

METABRIC is based on Illumina microarray expression, not RNA-seq.

Expression matrix summary:

| Item | Value |
|---|---:|
| Genes before duplicate removal | 20,603 |
| Unique gene symbols | 20,385 |
| Expression samples | 1,980 |

### METABRIC subtype column

The main subtype column used was:

    Pam50 + Claudin-low subtype

### METABRIC subtype distribution before filtering

| Subtype / Label | Samples |
|---|---:|
| LumA | 700 |
| LumB | 475 |
| Her2 | 224 |
| claudin-low | 218 |
| Basal | 209 |
| Normal | 148 |
| NC | 6 |
| Missing subtype label | 529 |

### Final METABRIC external validation dataset

Only the four TCGA-matched tumor classes were retained:

| Subtype | Samples |
|---|---:|
| LumA | 700 |
| LumB | 475 |
| Her2 | 224 |
| Basal | 209 |
| Total | 1,608 |

---

## 3. TCGA-METABRIC Gene Overlap

The TCGA model originally used 5,000 selected variable genes.

For external validation, only genes shared between TCGA and METABRIC were used.

| Item | Value |
|---|---:|
| TCGA selected ML genes | 5,000 |
| METABRIC-overlapping genes | 4,311 |
| Missing TCGA genes in METABRIC | 689 |
| Gene overlap | 86.22% |

---

## 4. Platform Difference

A major technical issue was that the two datasets came from different expression platforms:

| Dataset | Platform |
|---|---|
| TCGA-BRCA | RNA-seq |
| METABRIC | Illumina microarray |

Because of this platform difference, raw METABRIC microarray expression did not transfer well to the TCGA-trained model.

Raw METABRIC external validation caused predictions to collapse mostly to LumA.

Using METABRIC z-score expression improved cross-platform transfer substantially.

---

## 5. External Validation Data Used

The successful external validation used:

    data_mrna_illumina_microarray_zscores_ref_diploid_samples.txt

This z-score METABRIC expression file was aligned to the 4,311 genes shared with TCGA.

Final external validation file generated locally:

    data/processed/external_validation/metabric_4class_zscore_expression_overlap.csv

This file is not tracked by Git because it is a generated processed dataset.

---

## 6. Data Versioning and Git Policy

Large raw and processed datasets are ignored by Git.

Tracked in Git:

- source code
- scripts
- configuration files
- environment files
- reports
- documentation

Ignored by Git:

- raw TCGA expression files
- downloaded METABRIC archive
- extracted METABRIC files
- processed CSV datasets
- model checkpoints
- generated plots
- generated large result tables

This keeps the GitHub repository lightweight while preserving reproducibility through scripts.

---

## 7. Citation / Attribution Notes

This project uses public cancer genomics resources. Any formal report or publication should cite:

- The Cancer Genome Atlas / TCGA-BRCA resource
- UCSC Xena data platform
- METABRIC study
- cBioPortal
- PAM50 breast cancer subtype literature
