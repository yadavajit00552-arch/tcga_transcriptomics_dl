"""
Train baseline Random Forest model for TCGA-BRCA subtype classification.

Inputs:
- data/processed/ml/train_features.csv
- data/processed/ml/val_features.csv
- data/processed/ml/test_features.csv
- data/processed/ml/train_labels.csv
- data/processed/ml/val_labels.csv
- data/processed/ml/test_labels.csv

Outputs:
- results/tables/random_forest_validation_metrics.csv
- results/tables/random_forest_test_metrics.csv
- results/tables/random_forest_test_predictions.csv
- results/tables/random_forest_test_confusion_matrix.csv
- results/tables/random_forest_feature_importance.csv

Purpose:
Create a nonlinear baseline model before neural networks.
"""

from pathlib import Path
import pandas as pd

from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    balanced_accuracy_score,
    classification_report,
    confusion_matrix,
    f1_score,
)


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


def evaluate_model(model, X, y_true, split_name):
    """Evaluate model and return metrics/predictions/confusion matrix."""
    y_pred = model.predict(X)

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

    labels = sorted(y_true.unique().tolist())
    cm = confusion_matrix(y_true, y_pred, labels=labels)
    cm_df = pd.DataFrame(cm, index=labels, columns=labels)

    print(f"\n{split_name} confusion matrix:")
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
        "true_label": y_true.values,
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

    print("\nTraining Random Forest model...")

    model = RandomForestClassifier(
        n_estimators=500,
        max_depth=None,
        min_samples_split=2,
        min_samples_leaf=1,
        class_weight="balanced",
        random_state=RANDOM_SEED,
        n_jobs=-1,
    )

    model.fit(X_train, y_train)

    print("✅ Model training completed.")

    val_metrics, val_predictions, val_cm = evaluate_model(
        model,
        X_val,
        y_val,
        "validation",
    )

    test_metrics, test_predictions, test_cm = evaluate_model(
        model,
        X_test,
        y_test,
        "test",
    )

    val_predictions.insert(0, "sample_id", val_sample_ids.values)
    test_predictions.insert(0, "sample_id", test_sample_ids.values)

    feature_importance = pd.DataFrame({
        "gene": X_train.columns,
        "importance": model.feature_importances_,
    }).sort_values("importance", ascending=False)

    print("\nTop 20 Random Forest important genes:")
    print(feature_importance.head(20))

    val_metrics.to_csv(
        RESULTS_TABLE_DIR / "random_forest_validation_metrics.csv",
        index=False,
    )

    test_metrics.to_csv(
        RESULTS_TABLE_DIR / "random_forest_test_metrics.csv",
        index=False,
    )

    test_predictions.to_csv(
        RESULTS_TABLE_DIR / "random_forest_test_predictions.csv",
        index=False,
    )

    val_cm.to_csv(
        RESULTS_TABLE_DIR / "random_forest_validation_confusion_matrix.csv"
    )

    test_cm.to_csv(
        RESULTS_TABLE_DIR / "random_forest_test_confusion_matrix.csv"
    )

    feature_importance.to_csv(
        RESULTS_TABLE_DIR / "random_forest_feature_importance.csv",
        index=False,
    )

    print("\nSaved results in:", RESULTS_TABLE_DIR)
    print("✅ Random Forest baseline completed successfully.")


if __name__ == "__main__":
    main()
