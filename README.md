# TCGA Transcriptomics Deep Learning Project

Project name: `tcga_transcriptomics_dl`

## Overview

This project analyzes TCGA breast cancer transcriptomic data using machine learning and neural networks.

The beginner objective is to classify TCGA-BRCA breast cancer molecular subtypes using RNA-seq gene expression profiles.

## Main cohort

- TCGA-BRCA: Breast invasive carcinoma

## Main task

4-class molecular subtype classification:

- LumA
- LumB
- Basal
- Her2

The subtype labels were obtained from TCGA-BRCA PAM50-related clinical metadata using UCSC Xena.

## Dataset summary

After preprocessing and merging RNA-seq expression with PAM50 subtype labels:

| Item | Value |
|---|---:|
| Total modeling samples | 821 |
| Gene features before selection | 20,530 |
| Selected gene features for ML | 5,000 |
| Train samples | 524 |
| Validation samples | 132 |
| Test samples | 165 |

## Class distribution

| Subtype | Samples | Percentage |
|---|---:|---:|
| LumA | 421 | 51.28% |
| LumB | 192 | 23.39% |
| Basal | 141 | 17.17% |
| Her2 | 67 | 8.16% |

## Models trained

| Model | Test Accuracy | Balanced Accuracy | Macro F1 | Weighted F1 |
|---|---:|---:|---:|---:|
| Logistic Regression | 0.8909 | 0.8995 | 0.8821 | 0.8909 |
| MLP Neural Network | 0.8606 | 0.8477 | 0.8561 | 0.8555 |
| Random Forest | 0.8727 | 0.7826 | 0.8204 | 0.8635 |

## Current best model

The best current model is Logistic Regression.

Best test performance:

- Accuracy: 0.8909
- Balanced accuracy: 0.8995
- Macro F1: 0.8821

## Main biological interpretation

The strong performance of Logistic Regression suggests that TCGA-BRCA PAM50 subtype signal is highly structured and largely linearly separable in RNA-seq expression space.

Basal tumors were classified almost perfectly across models, suggesting a strong and distinct basal-like transcriptomic signature.

Most errors occurred between LumA and LumB, which is biologically reasonable because both are luminal breast cancer subtypes with partially overlapping expression programs.

The MLP neural network performed well but did not outperform Logistic Regression, showing that deeper nonlinear modeling is not automatically superior without further optimization or biological feature engineering.

## Gene importance interpretation

Because Logistic Regression was the best-performing model, its coefficients were used to identify subtype-associated genes.

Key subtype-associated genes:

| Subtype | Important positive genes | Biological interpretation |
|---|---|---|
| Basal | FOXC1, GDF5, FZD9, ZIC1 | Basal-like transcriptional signal |
| Her2 | ERBB2, GRB7, PGAP3, GSDMB | HER2/ERBB2-amplified biology |
| LumA | ERBB4, ADCY1, SLC40A1, GPR143 | Luminal and hormone-response-associated signal |
| LumB | BIRC5, NUF2, GTSE1, ASPM, DEPDC1 | Proliferation and cell-cycle-associated signal |

The presence of ERBB2 and GRB7 among the top Her2-associated genes strongly supports that the model learned biologically meaningful subtype features.


## Data sources

This project uses two public breast cancer transcriptomics datasets:

| Dataset | Platform | Role |
|---|---|---|
| TCGA-BRCA | RNA-seq | Training, validation, and testing |
| METABRIC | Illumina microarray | Independent external validation |

TCGA-BRCA expression and PAM50-related metadata were accessed through UCSC Xena. METABRIC expression and clinical files were downloaded from cBioPortal.

Detailed data-source information is available in:

    reports/data_sources.md


## External validation on METABRIC

To test whether the TCGA-BRCA subtype classifier generalizes beyond TCGA, the model was externally validated on the independent METABRIC breast cancer cohort.

Because TCGA expression data are RNA-seq-based and METABRIC expression data are Illumina microarray-based, external validation was performed carefully using genes shared between both datasets.

### Gene overlap

| Item | Value |
|---|---:|
| TCGA selected ML genes | 5,000 |
| Shared TCGA-METABRIC genes | 4,311 |
| Missing TCGA genes in METABRIC | 689 |
| Gene overlap | 86.22% |

### External validation dataset

| Subtype | METABRIC samples |
|---|---:|
| LumA | 700 |
| LumB | 475 |
| Her2 | 224 |
| Basal | 209 |
| Total | 1,608 |

### External validation performance

Using raw METABRIC microarray expression caused poor cross-platform transfer, with predictions collapsing mostly to LumA. After using METABRIC z-score expression, external validation improved substantially.

| Dataset | Accuracy | Balanced Accuracy | Macro F1 | Weighted F1 |
|---|---:|---:|---:|---:|
| TCGA test using shared genes | 0.8970 | 0.9060 | 0.8934 | 0.8970 |
| METABRIC z-score external validation | 0.8178 | 0.7840 | 0.8057 | 0.8161 |

### Interpretation

The successful METABRIC z-score validation suggests that the TCGA-trained classifier captures transferable breast cancer subtype biology. The main errors occurred between LumA and LumB, which is biologically reasonable because both are luminal subtypes with overlapping hormone-response expression programs.

This result also shows that platform-aware normalization is essential when transferring models between RNA-seq and microarray datasets.


## Pathway enrichment interpretation

Subtype-specific top genes were analyzed using pathway enrichment.

Key enrichment findings:

| Subtype | Enriched pathway | Interpretation |
|---|---|---|
| Her2 | GRB7 Events in ERBB2 Signaling | HER2 receptor signaling captured |
| LumA | Estrogen Response Early | Estrogen/luminal biology captured |
| LumB | E2F Targets and Cell Cycle | High-proliferation LumB biology captured |
| Basal | Elastic fibre-associated Reactome term | Modest signal; needs expanded basal gene interpretation |

Overall, the model-derived genes recover known breast cancer subtype biology, supporting both predictive performance and biological interpretability.

## Project workflow

Raw TCGA-BRCA expression data
↓
Primary tumor filtering
↓
PAM50 subtype metadata extraction
↓
Expression + subtype merging
↓
4-class dataset creation
↓
Train / validation / test split
↓
Top 5000 variable gene selection
↓
Feature scaling
↓
Baseline ML models
↓
MLP neural network
↓
Model evaluation
↓
Visualization and result summary

## Environment setup

Create the conda environment:

    conda env create -f envs/environment.yml

Activate the environment:

    conda activate tcga_dl

Verify Python:

    python --version
    which python

## Run full pipeline

After activating the environment, the full workflow can be reproduced with:

    bash run_all.sh

This script runs data preparation, preprocessing, model training, evaluation, gene interpretation, pathway enrichment, and visualization in the correct order.

Note: pathway enrichment depends on internet access because it queries Enrichr through GSEApy.

## Core scripts

### Data download and inspection

    python src/data/download_tcga_brca_xena.py
    python src/data/inspect_expression.py
    python src/data/fetch_brca_subtype_metadata.py

### Preprocessing

    python src/preprocessing/prepare_expression_matrix.py
    python src/preprocessing/merge_expression_metadata.py
    python src/preprocessing/create_4class_dataset.py
    python src/preprocessing/create_train_val_test_split.py
    python src/preprocessing/create_ml_features.py

### Models

    python src/models/train_logistic_regression.py
    python src/models/train_random_forest.py
    python src/models/train_mlp.py

### Evaluation and visualization

    python src/evaluation/compare_baseline_models.py
    python src/evaluation/run_shap_logistic_regression.py
    python src/evaluation/create_results_summary.py

    python src/visualization/plot_subtype_distribution.py
    python src/visualization/plot_pca_subtypes.py
    python src/visualization/plot_umap_subtypes.py
    python src/visualization/plot_model_comparison.py
    python src/visualization/plot_confusion_matrices.py

## Generated figures

Important figures generated by the project:

- subtype_distribution.png
- pca_subtype_plot.png
- umap_subtype_plot.png
- model_comparison_macro_f1.png
- model_comparison_all_metrics.png
- confusion_matrix_logistic_regression.png
- confusion_matrix_random_forest.png
- confusion_matrix_mlp.png
- mlp_training_curve.png

## Reproducibility notes

Large raw data files, processed datasets, trained model checkpoints, generated tables, and figures are ignored by Git using `.gitignore`.

The repository tracks scripts, configuration files, environment files, and documentation so the workflow can be reproduced.

## Current status

- [x] Project directory created
- [x] Conda environment created
- [x] TCGA-BRCA expression data downloaded
- [x] PAM50 subtype labels fetched
- [x] ML-ready dataset created
- [x] Train/validation/test split created
- [x] Logistic Regression baseline trained
- [x] Random Forest baseline trained
- [x] MLP neural network trained
- [x] Model comparison completed
- [x] PCA and UMAP visualizations created
- [x] Confusion matrix plots created
- [x] Results summary generated
- [x] SHAP / feature attribution for Logistic Regression
- [ ] Pathway enrichment
- [ ] Survival analysis
- [ ] Scientific report draft


## References and attribution

This project uses public cancer genomics resources and open-source computational tools.

Main resources include TCGA-BRCA, UCSC Xena, METABRIC, cBioPortal, scikit-learn, SHAP, and pathway enrichment resources.

A project-specific reference list is available in:

    reports/references.md
