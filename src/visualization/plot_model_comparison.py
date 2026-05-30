"""
Create model comparison plots.

Input:
- results/tables/model_comparison_summary.csv

Outputs:
- results/figures/model_comparison_macro_f1.png
- results/figures/model_comparison_all_metrics.png

Purpose:
Generate publication-ready figures comparing model performance.
"""

from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt


INPUT_PATH = Path("results/tables/model_comparison_summary.csv")
OUTPUT_DIR = Path("results/figures")


def main():
    print("Loading model comparison table...")
    df = pd.read_csv(INPUT_PATH)

    print("\nInput table:")
    print(df)

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    # Plot 1: Macro F1 comparison
    macro_f1_df = df.sort_values("macro_f1", ascending=True)

    plt.figure(figsize=(8, 5))
    plt.barh(macro_f1_df["model"], macro_f1_df["macro_f1"])
    plt.xlabel("Test Macro F1 Score")
    plt.ylabel("Model")
    plt.title("TCGA-BRCA Subtype Classification: Macro F1 Comparison")
    plt.xlim(0, 1)
    plt.tight_layout()

    macro_f1_path = OUTPUT_DIR / "model_comparison_macro_f1.png"
    plt.savefig(macro_f1_path, dpi=300)
    plt.close()

    print("\nSaved:", macro_f1_path)

    # Plot 2: All metrics comparison
    metrics = ["accuracy", "balanced_accuracy", "macro_f1", "weighted_f1"]
    plot_df = df[["model"] + metrics].copy()

    x = range(len(plot_df["model"]))
    width = 0.18

    plt.figure(figsize=(10, 6))

    for i, metric in enumerate(metrics):
        positions = [value + (i - 1.5) * width for value in x]
        plt.bar(positions, plot_df[metric], width=width, label=metric)

    plt.xticks(list(x), plot_df["model"], rotation=20, ha="right")
    plt.ylabel("Score")
    plt.xlabel("Model")
    plt.title("TCGA-BRCA Subtype Classification: Model Performance Comparison")
    plt.ylim(0, 1)
    plt.legend()
    plt.tight_layout()

    all_metrics_path = OUTPUT_DIR / "model_comparison_all_metrics.png"
    plt.savefig(all_metrics_path, dpi=300)
    plt.close()

    print("Saved:", all_metrics_path)
    print("✅ Model comparison plots created successfully.")


if __name__ == "__main__":
    main()
