"""
Train baseline Logistic Regression model for TCGA-BRCA subtype classification.

Inputs:
- data/processed/ml/train_features.csv
- data/processed/ml/val_features.csv
- data/processed/ml/test_features.csv
- data/processed/ml/train_labels.csv
- data/processed/ml/val_labels.csv
- data/processed/ml/test_labels.csv

Outputs:
- results/tables/logistic_regression_validation_metrics.csv
- results/tables/logistic_regression_test_metrics.csv
- results/tables/logistic_regression_test_predictions.csv

Purpose:
Create a simple baseline model before neural networks.
"""

from pathlib import Path
import pandas as pd

from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    balanced_accuracy_score,
    classification_report,
    confusion_matrix,
    f1_score,
)
from sklearn.preprocessing import LabelEncoder


ML_DIR = Path("data/processed/ml")
RESULTS_TABLE_DIR = Path("results/tables")

RANDOM_SEED = 42
TARGET_COLUMN = "molecular_subtype"


def load_features_and_labels(split_name):
    """Load feature matrix and labels for a split."""
    features_path = ML_DIR / f"{split_name}_features.csv"
    labels_path = ML_DIR / f"{split_name}_labels.csv"

    X = pd.read_csv(features_path)
    y = pd.read_csv(labels_path)

    sample_ids = X["sample_id"].copy()

    X = X.drop(columns=["sample_id"])
    y = y[TARGET_COLUMN]

    return X, y, sample_ids


def evaluate_model(model, X, y_true_encoded, label_encoder, split_name):
    """Evaluate model and return metrics/predictions."""
    y_pred_encoded = model.predict(X)

    y_true = label_encoder.inverse_transform(y_true_encoded)
    y_pred = label_encoder.inverse_transform(y_pred_encoded)

    accuracy = accuracy_score(y_true, y_pred)
    balanced_accuracy = balanced_accuracy_score(y_true, y_pred)
    macro_f1 = f1_score(y_true, y_pred, average="macro")
    weighted_f1 = f1_score(y_true, y_pred, average="weighted")

    print(f"\n{split_name} metrics:")
    print("Accuracy:", round(accuracy, 4))
    print("Balanced accuracy:", round(balanced_accuracy, 4))
    print("Macro F1:", round(macro_f1, 4))
    print("Weighted F1:", round(weighted_f1, 4))

    print(f"\n{split_name} classification report:")
    print(classification_report(y_true, y_pred))

    print(f"\n{split_name} confusion matrix:")
    labels = list(label_encoder.classes_)
    cm = confusion_matrix(y_true, y_pred, labels=labels)
    cm_df = pd.DataFrame(cm, index=labels, columns=labels)
    print(cm_df)

    metrics = pd.DataFrame([
        {
            "split": split_name,
            "accuracy": accuracy,
            "balanced_accuracy": balanced_accuracy,
            "macro_f1": macro_f1,
            "weighted_f1": weighted_f1,
        }
    ])

    predictions = pd.DataFrame({
        "true_label": y_true,
        "predicted_label": y_pred,
    })

    return metrics, predictions, cm_df


def main():
    RESULTS_TABLE_DIR.mkdir(parents=True, exist_ok=True)

    print("Loading ML-ready data...")

    X_train, y_train, train_sample_ids = load_features_and_labels("train")
    X_val, y_val, val_sample_ids = load_features_and_labels("val")
    X_test, y_test, test_sample_ids = load_features_and_labels("test")

    print("X_train shape:", X_train.shape)
    print("X_val shape:", X_val.shape)
    print("X_test shape:", X_test.shape)

    label_encoder = LabelEncoder()
    y_train_encoded = label_encoder.fit_transform(y_train)
    y_val_encoded = label_encoder.transform(y_val)
    y_test_encoded = label_encoder.transform(y_test)

    print("\nClass encoding:")
    for class_name, encoded_value in zip(label_encoder.classes_, range(len(label_encoder.classes_))):
        print(f"{class_name}: {encoded_value}")

    print("\nTraining Logistic Regression model...")

    model = LogisticRegression(
        max_iter=5000,
        class_weight="balanced",
        random_state=RANDOM_SEED,
        solver="lbfgs",
        n_jobs=-1,
    )

    model.fit(X_train, y_train_encoded)

    print("✅ Model training completed.")

    val_metrics, val_predictions, val_cm = evaluate_model(
        model,
        X_val,
        y_val_encoded,
        label_encoder,
        "validation",
    )

    test_metrics, test_predictions, test_cm = evaluate_model(
        model,
        X_test,
        y_test_encoded,
        label_encoder,
        "test",
    )

    val_predictions.insert(0, "sample_id", val_sample_ids.values)
    test_predictions.insert(0, "sample_id", test_sample_ids.values)

    val_metrics.to_csv(
        RESULTS_TABLE_DIR / "logistic_regression_validation_metrics.csv",
        index=False,
    )

    test_metrics.to_csv(
        RESULTS_TABLE_DIR / "logistic_regression_test_metrics.csv",
        index=False,
    )

    test_predictions.to_csv(
        RESULTS_TABLE_DIR / "logistic_regression_test_predictions.csv",
        index=False,
    )

    val_cm.to_csv(
        RESULTS_TABLE_DIR / "logistic_regression_validation_confusion_matrix.csv"
    )

    test_cm.to_csv(
        RESULTS_TABLE_DIR / "logistic_regression_test_confusion_matrix.csv"
    )

    print("\nSaved results in:", RESULTS_TABLE_DIR)
    print("✅ Logistic Regression baseline completed successfully.")


if __name__ == "__main__":
    main()
