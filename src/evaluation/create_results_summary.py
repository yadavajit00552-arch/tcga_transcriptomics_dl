"""
Create a plain-text project results summary.

Inputs:
- results/tables/model_comparison_summary.csv
- results/tables/subtype_distribution.csv
- results/tables/logistic_regression_test_confusion_matrix.csv
- results/tables/random_forest_test_confusion_matrix.csv
- results/tables/mlp_test_confusion_matrix.csv

Output:
- results/tables/project_results_summary.txt

Purpose:
Generate a concise summary of dataset, model performance,
major findings, and biological interpretation.
"""

from pathlib import Path
import pandas as pd


RESULTS_TABLE_DIR = Path("results/tables")

MODEL_COMPARISON_PATH = RESULTS_TABLE_DIR / "model_comparison_summary.csv"
SUBTYPE_DISTRIBUTION_PATH = RESULTS_TABLE_DIR / "subtype_distribution.csv"

CONFUSION_FILES = {
    "Logistic Regression": RESULTS_TABLE_DIR / "logistic_regression_test_confusion_matrix.csv",
    "Random Forest": RESULTS_TABLE_DIR / "random_forest_test_confusion_matrix.csv",
    "MLP Neural Network": RESULTS_TABLE_DIR / "mlp_test_confusion_matrix.csv",
}

OUTPUT_PATH = RESULTS_TABLE_DIR / "project_results_summary.txt"


def load_confusion_summary():
    """Create short confusion matrix interpretation."""
    summaries = []

    for model_name, path in CONFUSION_FILES.items():
        cm = pd.read_csv(path, index_col=0)

        total_correct = int(cm.values.diagonal().sum())
        total_samples = int(cm.values.sum())

        basal_correct = int(cm.loc["Basal", "Basal"]) if "Basal" in cm.index else None

        summaries.append(
            f"{model_name}: {total_correct}/{total_samples} test samples correctly classified. "
            f"Basal correct: {basal_correct}/{int(cm.loc['Basal'].sum())}."
        )

    return summaries


def main():
    print("Loading model comparison...")
    model_df = pd.read_csv(MODEL_COMPARISON_PATH)

    print("Loading subtype distribution...")
    subtype_df = pd.read_csv(SUBTYPE_DISTRIBUTION_PATH)

    best_model = model_df.sort_values("macro_f1", ascending=False).iloc[0]

    confusion_summaries = load_confusion_summary()

    lines = []

    lines.append("TCGA-BRCA Transcriptomics Deep Learning Project")
    lines.append("=" * 60)
    lines.append("")
    lines.append("Project goal")
    lines.append("-" * 60)
    lines.append(
        "Classify TCGA-BRCA breast cancer molecular subtypes using RNA-seq gene expression data."
    )
    lines.append("")
    lines.append("Cohort and task")
    lines.append("-" * 60)
    lines.append("Cohort: TCGA-BRCA")
    lines.append("Task: 4-class molecular subtype classification")
    lines.append("Classes: LumA, LumB, Basal, Her2")
    lines.append("")
    lines.append("Dataset summary")
    lines.append("-" * 60)
    total_samples = int(subtype_df["count"].sum())
    lines.append(f"Total modeling samples: {total_samples}")
    lines.append("Subtype distribution:")

    for _, row in subtype_df.iterrows():
        lines.append(
            f"- {row['subtype']}: {int(row['count'])} samples ({row['percentage']}%)"
        )

    lines.append("")
    lines.append("Model comparison")
    lines.append("-" * 60)

    for _, row in model_df.iterrows():
        lines.append(
            f"- {row['model']}: "
            f"accuracy={row['accuracy']:.4f}, "
            f"balanced_accuracy={row['balanced_accuracy']:.4f}, "
            f"macro_f1={row['macro_f1']:.4f}, "
            f"weighted_f1={row['weighted_f1']:.4f}"
        )

    lines.append("")
    lines.append("Best model")
    lines.append("-" * 60)
    lines.append(
        f"Best model by test macro F1: {best_model['model']} "
        f"(macro F1={best_model['macro_f1']:.4f}, "
        f"accuracy={best_model['accuracy']:.4f})."
    )

    lines.append("")
    lines.append("Confusion matrix interpretation")
    lines.append("-" * 60)
    for summary in confusion_summaries:
        lines.append(f"- {summary}")

    lines.append("")
    lines.append("Main biological interpretation")
    lines.append("-" * 60)
    lines.append(
        "The strong performance of Logistic Regression suggests that TCGA-BRCA PAM50 subtype "
        "signal is highly structured and largely linearly separable in RNA-seq expression space."
    )
    lines.append(
        "Basal tumors were classified almost perfectly across models, indicating a strong and distinct "
        "basal-like transcriptomic signature."
    )
    lines.append(
        "Most classification errors occurred between LumA and LumB, which is biologically reasonable "
        "because both are luminal breast cancer subtypes with partially overlapping expression programs."
    )
    lines.append(
        "The MLP neural network performed well but did not outperform Logistic Regression, suggesting "
        "that deeper nonlinear modeling is not automatically superior for this task without further "
        "optimization or additional biological feature engineering."
    )

    lines.append("")
    lines.append("Current conclusion")
    lines.append("-" * 60)
    lines.append(
        "RNA-seq expression profiles can classify TCGA-BRCA molecular subtypes with high accuracy. "
        "The best current model is Logistic Regression, providing a strong classical ML baseline "
        "against which neural network models can be compared."
    )

    summary_text = "\n".join(lines)

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(summary_text)

    print(summary_text)
    print("\nSaved:", OUTPUT_PATH)
    print("✅ Project results summary created successfully.")


if __name__ == "__main__":
    main()
