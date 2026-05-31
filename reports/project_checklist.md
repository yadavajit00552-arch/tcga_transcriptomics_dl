# TCGA-BRCA Transcriptomics Deep Learning Project Checklist

Project: tcga_transcriptomics_dl

## 1. Completed workflow

- [x] Created reproducible project folder structure
- [x] Created conda environment
- [x] Installed required Python packages
- [x] Downloaded TCGA-BRCA RNA-seq expression data
- [x] Inspected raw expression matrix
- [x] Filtered primary tumor samples
- [x] Fetched PAM50 molecular subtype metadata
- [x] Merged expression data with subtype labels
- [x] Removed small Normal class for 4-class modeling
- [x] Created stratified train/validation/test split
- [x] Selected top 5000 variable genes using train data only
- [x] Scaled features using train data only
- [x] Trained Logistic Regression baseline
- [x] Trained Random Forest baseline
- [x] Trained MLP neural network
- [x] Compared models
- [x] Extracted Logistic Regression subtype-associated genes
- [x] Created subtype-specific gene lists
- [x] Ran pathway enrichment analysis
- [x] Generated report-ready plots
- [x] Updated README with results and interpretation
- [x] Created reproducible run_all.sh pipeline runner
- [x] Verified full pipeline runs end-to-end

## 2. Dataset summary

| Item | Value |
|---|---:|
| Cohort | TCGA-BRCA |
| Task | 4-class molecular subtype classification |
| Classes | LumA, LumB, Basal, Her2 |
| Total modeling samples | 821 |
| Original gene features | 20,530 |
| Selected ML gene features | 5,000 |
| Train samples | 524 |
| Validation samples | 132 |
| Test samples | 165 |

## 3. Model comparison

| Model | Test Accuracy | Balanced Accuracy | Macro F1 | Weighted F1 |
|---|---:|---:|---:|---:|
| Logistic Regression | 0.8909 | 0.8995 | 0.8821 | 0.8909 |
| MLP Neural Network | 0.8606 | 0.8477 | 0.8561 | 0.8555 |
| Random Forest | 0.8727 | 0.7826 | 0.8204 | 0.8635 |

## 4. Best model

Best current model: Logistic Regression.

Reason:
- Highest test macro F1
- Highest balanced accuracy
- Strong performance despite simple linear structure
- Biologically interpretable coefficients

## 5. Main scientific conclusion

RNA-seq expression profiles can classify TCGA-BRCA PAM50 molecular subtypes with high accuracy.

The best model is Logistic Regression, suggesting that TCGA-BRCA subtype signal is highly structured and largely linearly separable in gene-expression space.

## 6. Main biological findings

| Subtype | Model-derived genes/pathways | Interpretation |
|---|---|---|
| Basal | FOXC1, FZD9, ZIC1 | Basal-like transcriptional signal |
| Her2 | ERBB2, GRB7, PGAP3, GSDMB; ERBB2 signaling | HER2 subtype biology captured |
| LumA | Estrogen Response Early | Luminal hormone-response biology captured |
| LumB | BIRC5, NUF2, GTSE1, ASPM; E2F Targets; Cell Cycle | Proliferation/cell-cycle biology captured |

## 7. Important generated figures

- results/figures/subtype_distribution.png
- results/figures/pca_subtype_plot.png
- results/figures/umap_subtype_plot.png
- results/figures/model_comparison_macro_f1.png
- results/figures/model_comparison_all_metrics.png
- results/figures/confusion_matrix_logistic_regression.png
- results/figures/confusion_matrix_random_forest.png
- results/figures/confusion_matrix_mlp.png
- results/figures/mlp_training_curve.png
- results/figures/logistic_regression_top_genes_by_subtype.png
- results/figures/pathway_enrichment_top_terms.png

## 8. Important generated tables

- results/tables/model_comparison_summary.csv
- results/tables/project_results_summary.txt
- results/tables/subtype_distribution.csv
- results/tables/logistic_regression_coefficients_all.csv
- results/tables/logistic_regression_top_genes_by_subtype.csv
- results/tables/pathway_enrichment/pathway_enrichment_summary.csv

## 9. Reproducibility command

After activating the conda environment:

    conda activate tcga_dl
    bash run_all.sh

## 10. Next optional advanced tasks

- [ ] SHAP analysis for Logistic Regression / MLP
- [ ] Integrated Gradients for MLP
- [ ] Pathway enrichment using larger gene sets
- [ ] Survival analysis by predicted subtype or subtype probability
- [ ] External validation on another breast cancer dataset
- [ ] Hyperparameter tuning for MLP
- [ ] Compare with SVM / Elastic Net / XGBoost
- [ ] Write full scientific report
- [ ] Prepare presentation slides

## 11. Final status

This project currently has a complete beginner-to-intermediate computational biology workflow:

Data acquisition → preprocessing → subtype classification → neural network benchmark → model comparison → gene interpretation → pathway enrichment → reproducible pipeline
