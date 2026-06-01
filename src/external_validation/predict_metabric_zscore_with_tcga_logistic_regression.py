"""
External validation of TCGA-trained Logistic Regression model on METABRIC.

Strategy:
- Use only genes shared between TCGA selected ML features and METABRIC expression.
- Retrain Logistic Regression on TCGA train set using overlapping genes only.
- Evaluate on TCGA test set using the same overlapping genes.
- Apply the TCGA-trained scaler and model to METABRIC.
- Report METABRIC z-score external validation metrics.

Important:
TCGA data = RNA-seq
METABRIC data = Illumina microarray

So this is a cross-platform validation experiment.
"""

from pathlib import Path
import pandas as pd
import numpy as np

from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    balanced_accuracy_score,
    f1_score,
    classification_report,
    confusion_matrix,
)


TCGA_ML_DIR = Path("data/processed/ml")
METABRIC_DATASET = Path(
    "data/processed/external_validation/metabric_4class_zscore_expression_overlap.csv"
)
METABRIC_GENE_ORDER = Path(
    "data/processed/external_validation/metabric_zscore_overlap_gene_order.txt"
)

OUTPUT_DIR = Path("results/tables/external_validation")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def save_confusion_matrix(y_true, y_pred, labels, output_file):
    cm = confusion_matrix(y_true, y_pred, labels=labels)
    cm_df = pd.DataFrame(cm, index=labels, columns=labels)
    cm_df.to_csv(output_file)
    return cm_df


def make_metrics(y_true, y_pred, split_name):
    return {
        "split": split_name,
        "accuracy": accuracy_score(y_true, y_pred),
        "balanced_accuracy": balanced_accuracy_score(y_true, y_pred),
        "macro_f1": f1_score(y_true, y_pred, average="macro"),
        "weighted_f1": f1_score(y_true, y_pred, average="weighted"),
    }


def main():
    print("Loading TCGA ML data...")
    X_train = pd.read_csv(TCGA_ML_DIR / "train_features.csv")
    X_test = pd.read_csv(TCGA_ML_DIR / "test_features.csv")

    y_train_df = pd.read_csv(TCGA_ML_DIR / "train_labels.csv")
    y_test_df = pd.read_csv(TCGA_ML_DIR / "test_labels.csv")

    y_train = y_train_df["molecular_subtype"]
    y_test = y_test_df["molecular_subtype"]

    print("TCGA train shape:", X_train.shape)
    print("TCGA test shape:", X_test.shape)

    print("\nLoading METABRIC validation dataset...")
    metabric = pd.read_csv(METABRIC_DATASET)
    print("METABRIC validation shape:", metabric.shape)

    overlap_genes = METABRIC_GENE_ORDER.read_text().splitlines()
    print("Overlapping genes used:", len(overlap_genes))

    # Safety checks
    missing_in_tcga_train = [g for g in overlap_genes if g not in X_train.columns]
    missing_in_metabric = [g for g in overlap_genes if g not in metabric.columns]

    if missing_in_tcga_train:
        raise ValueError(f"Genes missing in TCGA train: {len(missing_in_tcga_train)}")

    if missing_in_metabric:
        raise ValueError(f"Genes missing in METABRIC: {len(missing_in_metabric)}")

    print("\nSubsetting TCGA and METABRIC to shared genes...")
    X_train_overlap = X_train[overlap_genes]
    X_test_overlap = X_test[overlap_genes]

    X_metabric = metabric[overlap_genes]
    y_metabric = metabric["molecular_subtype"]

    print("X_train_overlap:", X_train_overlap.shape)
    print("X_test_overlap:", X_test_overlap.shape)
    print("X_metabric:", X_metabric.shape)

    print("\nMETABRIC subtype counts:")
    print(y_metabric.value_counts())

    print("\nEncoding labels using TCGA train labels...")
    label_encoder = LabelEncoder()
    y_train_encoded = label_encoder.fit_transform(y_train)
    y_test_encoded = label_encoder.transform(y_test)
    y_metabric_encoded = label_encoder.transform(y_metabric)

    class_names = list(label_encoder.classes_)
    print("Class encoding:")
    for i, cls in enumerate(class_names):
        print(f"{cls}: {i}")

    print("\nChecking missing values before imputation...")
    print("TCGA train missing values:", int(X_train_overlap.isna().sum().sum()))
    print("TCGA test missing values:", int(X_test_overlap.isna().sum().sum()))
    print("METABRIC missing values:", int(X_metabric.isna().sum().sum()))

    print("\nImputing missing values...")
    imputer = SimpleImputer(strategy="median")

    # Fit imputer only on TCGA train data to avoid external-validation leakage.
    X_train_imputed = imputer.fit_transform(X_train_overlap)
    X_test_imputed = imputer.transform(X_test_overlap)
    X_metabric_imputed = imputer.transform(X_metabric)

    print("\nScaling data...")
    scaler = StandardScaler()

    # Fit scaler only on TCGA train data to avoid external-validation leakage.
    X_train_scaled = scaler.fit_transform(X_train_imputed)
    X_test_scaled = scaler.transform(X_test_imputed)

    # For METABRIC, apply TCGA-trained imputer and scaler only.
    # This is strict external validation, but cross-platform shift may reduce performance.
    X_metabric_scaled = scaler.transform(X_metabric_imputed)

    print("\nTraining Logistic Regression on TCGA overlap genes...")
    model = LogisticRegression(
        max_iter=5000,
        solver="saga",
        penalty="l2",
        class_weight="balanced",
        random_state=42,
    )

    model.fit(X_train_scaled, y_train_encoded)
    print("✅ Model trained.")

    print("\nPredicting TCGA test set...")
    tcga_test_pred_encoded = model.predict(X_test_scaled)
    tcga_test_pred = label_encoder.inverse_transform(tcga_test_pred_encoded)

    print("\nPredicting METABRIC z-score external validation set...")
    metabric_pred_encoded = model.predict(X_metabric_scaled)
    metabric_pred = label_encoder.inverse_transform(metabric_pred_encoded)

    # Metrics
    tcga_metrics = make_metrics(y_test, tcga_test_pred, "tcga_test_overlap_genes")
    metabric_metrics = make_metrics(y_metabric, metabric_pred, "metabric_zscore_external_validation")

    metrics_df = pd.DataFrame([tcga_metrics, metabric_metrics])

    print("\nMetrics:")
    print(metrics_df)

    print("\nTCGA test classification report:")
    print(classification_report(y_test, tcga_test_pred, labels=class_names))

    print("\nMETABRIC z-score external validation classification report:")
    print(classification_report(y_metabric, metabric_pred, labels=class_names))

    # Save predictions
    tcga_pred_df = pd.DataFrame({
        "sample_id": X_test["sample_id"] if "sample_id" in X_test.columns else np.arange(len(y_test)),
        "true_subtype": y_test,
        "predicted_subtype": tcga_test_pred,
    })

    metabric_pred_df = pd.DataFrame({
        "sample_id": metabric["sample_id"],
        "true_subtype": y_metabric,
        "predicted_subtype": metabric_pred,
    })

    # Save confusion matrices
    tcga_cm = save_confusion_matrix(
        y_test,
        tcga_test_pred,
        class_names,
        OUTPUT_DIR / "tcga_test_overlap_logistic_regression_confusion_matrix.csv",
    )

    metabric_cm = save_confusion_matrix(
        y_metabric,
        metabric_pred,
        class_names,
        OUTPUT_DIR / "metabric_zscore_external_logistic_regression_confusion_matrix.csv",
    )

    print("\nTCGA overlap-gene confusion matrix:")
    print(tcga_cm)

    print("\nMETABRIC z-score external validation confusion matrix:")
    print(metabric_cm)

    metrics_file = OUTPUT_DIR / "metabric_zscore_external_validation_metrics.csv"
    tcga_pred_file = OUTPUT_DIR / "tcga_test_overlap_logistic_regression_predictions.csv"
    metabric_pred_file = OUTPUT_DIR / "metabric_zscore_external_logistic_regression_predictions.csv"

    metrics_df.to_csv(metrics_file, index=False)
    tcga_pred_df.to_csv(tcga_pred_file, index=False)
    metabric_pred_df.to_csv(metabric_pred_file, index=False)

    print("\nSaved:", metrics_file)
    print("Saved:", tcga_pred_file)
    print("Saved:", metabric_pred_file)

    print("\n✅ METABRIC z-score external validation completed successfully.")


if __name__ == "__main__":
    main()
