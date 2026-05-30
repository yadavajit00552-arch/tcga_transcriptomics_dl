"""
Plot confusion matrices for trained TCGA-BRCA subtype classifiers.

Inputs:
- results/tables/logistic_regression_test_confusion_matrix.csv
- results/tables/random_forest_test_confusion_matrix.csv
- results/tables/mlp_test_confusion_matrix.csv

Outputs:
- results/figures/confusion_matrix_logistic_regression.png
- results/figures/confusion_matrix_random_forest.png
- results/figures/confusion_matrix_mlp.png

Purpose:
Visualize model-specific subtype classification errors.
"""

from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt


RESULTS_TABLE_DIR = Path("results/tables")
RESULTS_FIGURE_DIR = Path("results/figures")

CONFUSION_FILES = {
    "Logistic Regression": {
        "input": RESULTS_TABLE_DIR / "logistic_regression_test_confusion_matrix.csv",
        "output": RESULTS_FIGURE_DIR / "confusion_matrix_logistic_regression.png",
    },
    "Random Forest": {
        "input": RESULTS_TABLE_DIR / "random_forest_test_confusion_matrix.csv",
        "output": RESULTS_FIGURE_DIR / "confusion_matrix_random_forest.png",
    },
    "MLP Neural Network": {
        "input": RESULTS_TABLE_DIR / "mlp_test_confusion_matrix.csv",
        "output": RESULTS_FIGURE_DIR / "confusion_matrix_mlp.png",
    },
}


def plot_confusion_matrix(cm_df, title, output_path):
    """Plot one confusion matrix."""
    plt.figure(figsize=(6, 5))

    plt.imshow(cm_df.values)
    plt.title(title)
    plt.xlabel("Predicted label")
    plt.ylabel("True label")

    plt.xticks(range(len(cm_df.columns)), cm_df.columns, rotation=45, ha="right")
    plt.yticks(range(len(cm_df.index)), cm_df.index)

    for i in range(cm_df.shape[0]):
        for j in range(cm_df.shape[1]):
            plt.text(
                j,
                i,
                str(cm_df.iloc[i, j]),
                ha="center",
                va="center",
            )

    plt.colorbar(label="Number of samples")
    plt.tight_layout()
    plt.savefig(output_path, dpi=300)
    plt.close()


def main():
    RESULTS_FIGURE_DIR.mkdir(parents=True, exist_ok=True)

    for model_name, paths in CONFUSION_FILES.items():
        input_path = paths["input"]
        output_path = paths["output"]

        print("Loading:", input_path)

        if not input_path.exists():
            raise FileNotFoundError(f"Missing confusion matrix file: {input_path}")

        cm_df = pd.read_csv(input_path, index_col=0)

        print(f"\n{model_name} confusion matrix:")
        print(cm_df)

        plot_confusion_matrix(
            cm_df=cm_df,
            title=f"{model_name}: Test Confusion Matrix",
            output_path=output_path,
        )

        print("Saved:", output_path)

    print("\n✅ Confusion matrix plots created successfully.")


if __name__ == "__main__":
    main()
