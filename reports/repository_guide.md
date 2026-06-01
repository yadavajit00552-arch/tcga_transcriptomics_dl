# Repository Guide

## Project

Interpretable Cross-Cohort Transcriptomic Classification of Breast Cancer Molecular Subtypes Using TCGA-BRCA and METABRIC

## Main purpose

This repository contains a reproducible computational biology pipeline for breast cancer molecular subtype classification using TCGA-BRCA RNA-seq expression data and METABRIC external validation.

## Main reports

| File | Purpose |
|---|---|
| README.md | Public-facing project overview |
| reports/final_project_summary.md | Complete final project summary |
| reports/manuscript/tcga_brca_subtype_classification_report.md | Scientific report draft |
| reports/project_interview_summary.md | Interview explanation and defense |
| reports/metabric_external_validation_results.md | METABRIC validation results |
| reports/external_validation_plan.md | External validation planning |
| reports/metabric_data_download_notes.md | METABRIC download notes |

## Main source-code folders

| Folder | Purpose |
|---|---|
| src/data/ | Download and inspect TCGA-BRCA data |
| src/preprocessing/ | Prepare expression matrix, metadata, splits, ML features |
| src/models/ | Train Logistic Regression, Random Forest, and MLP |
| src/evaluation/ | Model comparison, SHAP, pathway enrichment, result summaries |
| src/visualization/ | Generate report-ready plots |
| src/external_validation/ | METABRIC inspection, dataset preparation, and prediction |

## Main pipeline command

After activating the conda environment:

    conda activate tcga_dl
    bash run_all.sh

## Key TCGA result

| Model | Test Accuracy | Balanced Accuracy | Macro F1 | Weighted F1 |
|---|---:|---:|---:|---:|
| Logistic Regression | 0.8909 | 0.8995 | 0.8821 | 0.8909 |

## Key METABRIC external validation result

Using 4,311 genes shared between TCGA and METABRIC:

| Dataset | Accuracy | Balanced Accuracy | Macro F1 | Weighted F1 |
|---|---:|---:|---:|---:|
| TCGA test using shared genes | 0.8970 | 0.9060 | 0.8934 | 0.8970 |
| METABRIC z-score external validation | 0.8178 | 0.7840 | 0.8057 | 0.8161 |

## Important biological interpretation

| Subtype | Main recovered biology |
|---|---|
| Her2 | ERBB2 / GRB7 signaling |
| LumA | Estrogen-response biology |
| LumB | E2F targets, cell cycle, proliferation |
| Basal | Distinct basal-like transcriptomic signal |

## External validation scripts

| Script | Purpose |
|---|---|
| src/external_validation/inspect_metabric_files.py | Inspect downloaded METABRIC files |
| src/external_validation/check_metabric_tcga_overlap.py | Check TCGA-METABRIC gene/sample overlap |
| src/external_validation/create_metabric_validation_dataset.py | Create raw METABRIC validation dataset |
| src/external_validation/create_metabric_zscore_validation_dataset.py | Create z-score METABRIC validation dataset |
| src/external_validation/predict_metabric_with_tcga_logistic_regression.py | Raw METABRIC prediction attempt |
| src/external_validation/predict_metabric_zscore_with_tcga_logistic_regression.py | Successful z-score external validation |

## Data policy

Large raw, processed, model, and result files are ignored by Git.

Tracked files include source code, configuration, environment files, reports, and documentation.

Ignored files include TCGA raw expression matrices, METABRIC downloaded data, processed CSV datasets, model checkpoints, generated figures, and large result tables.

## Main scientific conclusion

Breast cancer molecular subtype identity is strongly encoded in transcriptomic profiles. The TCGA-trained classifier recovered known subtype biology and externally validated on METABRIC after platform-aware z-score normalization.

## Main technical lesson

Cross-platform transcriptomic prediction requires careful normalization. Raw METABRIC microarray expression caused poor transfer, while METABRIC z-score expression improved external validation performance substantially.
