"""
Run SHAP explainability for Logistic Regression subtype classifier.

Inputs:
- data/processed/ml/train_features.csv
- data/processed/ml/test_features.csv
- data/processed/ml/train_labels.csv
- data/processed/ml/test_labels.csv

Outputs:
- results/tables/shap_logistic_regression_top_genes.csv
- results/figures/shap_logistic_regression_top_genes.png

Purpose:
Compute global SHAP-based gene importance for the best-performing model.
"""

from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import shap

from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import LabelEncoder


ML_DIR = Path("data/processed/ml")
RESULTS_TABLE_DIR = Path("results/tables")
RESULTS_FIGURE_DIR = Path("results/figures")

TARGET_COLUMN = "molecular_subtype"
RANDOM_SEED = 42
TOP_N = 30


def main():
    RESULTS_TABLE_DIR.mkdir(parents=True, exist_ok=True)
    RESULTS_FIGURE_DIR.mkdir(parents=True, exist_ok=True)

    print("Loading ML-ready data...")

    X_train = pd.read_csv(ML_DIR / "train_features.csv")
    X_test = pd.read_csv(ML_DIR / "test_features.csv")

    y_train = pd.read_csv(ML_DIR / "train_labels.csv")
    y_test = pd.read_csv(ML_DIR / "test_labels.csv")

    train_sample_ids = X_train["sample_id"].copy()
    test_sample_ids = X_test["sample_id"].copy()

    X_train = X_train.drop(columns=["sample_id"])
    X_test = X_test.drop(columns=["sample_id"])

    y_train = y_train[TARGET_COLUMN]
    y_test = y_test[TARGET_COLUMN]

    print("X_train shape:", X_train.shape)
    print("X_test shape:", X_test.shape)

    label_encoder = LabelEncoder()
    y_train_encoded = label_encoder.fit_transform(y_train)
    y_test_encoded = label_encoder.transform(y_test)

    print("\nClass encoding:")
    for class_name, encoded_value in zip(label_encoder.classes_, range(len(label_encoder.classes_))):
        print(f"{class_name}: {encoded_value}")

    print("\nTraining Logistic Regression model for SHAP...")
    model = LogisticRegression(
        max_iter=5000,
        class_weight="balanced",
        random_state=RANDOM_SEED,
        solver="lbfgs",
    )
    model.fit(X_train, y_train_encoded)
    print("✅ Logistic Regression trained.")

    print("\nCreating SHAP LinearExplainer...")
    explainer = shap.LinearExplainer(model, X_train)

    print("Computing SHAP values on test set...")
    shap_values = explainer.shap_values(X_test)

    genes = X_train.columns.tolist()

    # SHAP output can be list[class] or array[samples, features, classes]
    if isinstance(shap_values, list):
        # list length = number of classes, each array = samples x features
        mean_abs_by_class = []
        class_rows = []

        for class_index, class_name in enumerate(label_encoder.classes_):
            class_shap = np.abs(shap_values[class_index])
            mean_abs = class_shap.mean(axis=0)
            mean_abs_by_class.append(mean_abs)

            class_df = pd.DataFrame({
                "subtype": class_name,
                "gene": genes,
                "mean_abs_shap": mean_abs,
            }).sort_values("mean_abs_shap", ascending=False)

            class_rows.append(class_df.head(TOP_N))

        global_mean_abs = np.mean(np.vstack(mean_abs_by_class), axis=0)

    else:
        shap_array = np.array(shap_values)

        if shap_array.ndim == 3:
            # expected shape could be samples x features x classes
            if shap_array.shape[1] == len(genes):
                global_mean_abs = np.abs(shap_array).mean(axis=(0, 2))
                class_rows = []

                for class_index, class_name in enumerate(label_encoder.classes_):
                    class_shap = np.abs(shap_array[:, :, class_index])
                    mean_abs = class_shap.mean(axis=0)

                    class_df = pd.DataFrame({
                        "subtype": class_name,
                        "gene": genes,
                        "mean_abs_shap": mean_abs,
                    }).sort_values("mean_abs_shap", ascending=False)

                    class_rows.append(class_df.head(TOP_N))
            else:
                raise ValueError(f"Unexpected SHAP array shape: {shap_array.shape}")

        elif shap_array.ndim == 2:
            global_mean_abs = np.abs(shap_array).mean(axis=0)
            class_rows = []
        else:
            raise ValueError(f"Unexpected SHAP output shape: {shap_array.shape}")

    global_df = pd.DataFrame({
        "gene": genes,
        "mean_abs_shap": global_mean_abs,
    }).sort_values("mean_abs_shap", ascending=False)

    top_global = global_df.head(TOP_N).copy()

    print(f"\nTop {TOP_N} global SHAP genes:")
    print(top_global)

    output_table = RESULTS_TABLE_DIR / "shap_logistic_regression_top_genes.csv"
    top_global.to_csv(output_table, index=False)

    if class_rows:
        class_output = RESULTS_TABLE_DIR / "shap_logistic_regression_top_genes_by_subtype.csv"
        pd.concat(class_rows, axis=0, ignore_index=True).to_csv(class_output, index=False)
        print("Saved subtype SHAP table:", class_output)

    plt.figure(figsize=(8, 7))
    plot_df = top_global.sort_values("mean_abs_shap", ascending=True)
    plt.barh(plot_df["gene"], plot_df["mean_abs_shap"])
    plt.xlabel("Mean absolute SHAP value")
    plt.ylabel("Gene")
    plt.title("Top Global SHAP Genes: Logistic Regression")
    plt.tight_layout()

    output_figure = RESULTS_FIGURE_DIR / "shap_logistic_regression_top_genes.png"
    plt.savefig(output_figure, dpi=300, bbox_inches="tight")
    plt.close()

    print("\nSaved SHAP table:", output_table)
    print("Saved SHAP figure:", output_figure)
    print("✅ SHAP Logistic Regression analysis completed successfully.")


if __name__ == "__main__":
    main()
