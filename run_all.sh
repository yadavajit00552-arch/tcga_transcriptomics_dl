#!/usr/bin/env bash

set -e

echo "============================================================"
echo "TCGA-BRCA Transcriptomics Deep Learning Pipeline"
echo "============================================================"

echo ""
echo "Step 1: Download / verify TCGA-BRCA expression data"
python src/data/download_tcga_brca_xena.py

echo ""
echo "Step 2: Inspect raw expression matrix"
python src/data/inspect_expression.py

echo ""
echo "Step 3: Prepare primary tumor expression matrix"
python src/preprocessing/prepare_expression_matrix.py

echo ""
echo "Step 4: Fetch PAM50 subtype metadata"
python src/data/fetch_brca_subtype_metadata.py

echo ""
echo "Step 5: Merge expression data with subtype metadata"
python src/preprocessing/merge_expression_metadata.py

echo ""
echo "Step 6: Inspect merged dataset"
python src/preprocessing/inspect_merged_dataset.py

echo ""
echo "Step 7: Create 4-class subtype dataset"
python src/preprocessing/create_4class_dataset.py

echo ""
echo "Step 8: Create stratified train/validation/test split"
python src/preprocessing/create_train_val_test_split.py

echo ""
echo "Step 9: Create ML-ready features"
python src/preprocessing/create_ml_features.py

echo ""
echo "Step 10: Train Logistic Regression baseline"
python src/models/train_logistic_regression.py

echo ""
echo "Step 11: Train Random Forest baseline"
python src/models/train_random_forest.py

echo ""
echo "Step 12: Train MLP neural network"
python src/models/train_mlp.py

echo ""
echo "Step 13: Compare models"
python src/evaluation/compare_baseline_models.py

echo ""
echo "Step 14: Extract Logistic Regression important genes"
python src/evaluation/extract_logistic_regression_genes.py

echo ""
echo "Step 15: Create subtype gene lists"
python src/evaluation/create_subtype_gene_lists.py

echo ""
echo "Step 16: Run pathway enrichment"
python src/evaluation/run_pathway_enrichment.py

echo ""
echo "Step 17: Create result summary"
python src/evaluation/create_results_summary.py

echo ""
echo "Step 18: Generate subtype distribution plot"
python src/visualization/plot_subtype_distribution.py

echo ""
echo "Step 19: Generate PCA plot"
python src/visualization/plot_pca_subtypes.py

echo ""
echo "Step 20: Generate UMAP plot"
python src/visualization/plot_umap_subtypes.py

echo ""
echo "Step 21: Generate model comparison plots"
python src/visualization/plot_model_comparison.py

echo ""
echo "Step 22: Generate confusion matrix plots"
python src/visualization/plot_confusion_matrices.py

echo ""
echo "Step 23: Generate Logistic Regression gene plot"
python src/visualization/plot_logistic_regression_genes.py

echo ""
echo "Step 24: Generate pathway enrichment plot"
python src/visualization/plot_pathway_enrichment.py

echo ""
echo "============================================================"
echo "✅ Pipeline completed successfully."
echo "============================================================"
