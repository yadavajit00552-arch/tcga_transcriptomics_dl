"""
Compare baseline model performance.

Inputs:
- results/tables/logistic_regression_test_metrics.csv
- results/tables/random_forest_test_metrics.csv

Output:
- results/tables/model_comparison_summary.csv

Purpose:
Create one clean table comparing baseline model performance.
"""

from pathlib import Path
import pandas as pd


RESULTS_TABLE_DIR = Path("results/tables")

MODEL_FILES = {
    "Logistic Regression": RESULTS_TABLE_DIR / "logistic_regression_test_metrics.csv",
    "Random Forest": RESULTS_TABLE_DIR / "random_forest_test_metrics.csv",
}

OUTPUT_PATH = RESULTS_TABLE_DIR / "model_comparison_summary.csv"


def main():
    rows = []

    for model_name, path in MODEL_FILES.items():
        print(f"Loading: {path}")

        if not path.exists():
            raise FileNotFoundError(f"Missing metrics file: {path}")

        metrics = pd.read_csv(path)
        row = metrics.iloc[0].to_dict()
        row["model"] = model_name
        rows.append(row)

    comparison = pd.DataFrame(rows)

    comparison = comparison[
        [
            "model",
            "split",
            "accuracy",
            "balanced_accuracy",
            "macro_f1",
            "weighted_f1",
        ]
    ]

    comparison = comparison.sort_values("macro_f1", ascending=False)

    print("\nModel comparison:")
    print(comparison)

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    comparison.to_csv(OUTPUT_PATH, index=False)

    print("\nSaved:", OUTPUT_PATH)
    print("✅ Baseline model comparison completed successfully.")


if __name__ == "__main__":
    main()
