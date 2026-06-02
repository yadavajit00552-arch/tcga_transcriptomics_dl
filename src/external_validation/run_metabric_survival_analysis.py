"""
Survival analysis on METABRIC external validation predictions.

Goal:
Test whether true subtypes and TCGA-model-predicted subtypes show survival differences
in the METABRIC external validation cohort.

Inputs:
- METABRIC z-score prediction file:
  results/tables/external_validation/metabric_zscore_external_logistic_regression_predictions.csv

- METABRIC clinical patient file:
  data/external/metabric/brca_metabric/data_clinical_patient.txt

Outputs:
- results/tables/external_validation/metabric_survival_dataset.csv
- results/tables/external_validation/metabric_survival_logrank_results.csv
- results/figures/metabric_survival_by_true_subtype.png
- results/figures/metabric_survival_by_predicted_subtype.png
"""

from pathlib import Path
import itertools

import pandas as pd
import matplotlib.pyplot as plt

from lifelines import KaplanMeierFitter
from lifelines.statistics import logrank_test


PRED_FILE = Path(
    "results/tables/external_validation/metabric_zscore_external_logistic_regression_predictions.csv"
)

CLINICAL_FILE = Path(
    "data/external/metabric/brca_metabric/data_clinical_patient.txt"
)

TABLE_OUT_DIR = Path("results/tables/external_validation")
FIG_OUT_DIR = Path("results/figures")

TABLE_OUT_DIR.mkdir(parents=True, exist_ok=True)
FIG_OUT_DIR.mkdir(parents=True, exist_ok=True)

SURVIVAL_DATASET_OUT = TABLE_OUT_DIR / "metabric_survival_dataset.csv"
LOGRANK_OUT = TABLE_OUT_DIR / "metabric_survival_logrank_results.csv"

FIG_TRUE_OUT = FIG_OUT_DIR / "metabric_survival_by_true_subtype.png"
FIG_PRED_OUT = FIG_OUT_DIR / "metabric_survival_by_predicted_subtype.png"


def load_cbioportal_clinical(path):
    """
    cBioPortal clinical files contain 4 metadata-like rows.
    Keep visible column names and skip rows 1, 2, and 3.
    """
    return pd.read_csv(path, sep="\t", skiprows=[1, 2, 3])


def clean_os_status(status):
    """
    cBioPortal METABRIC OS status commonly appears like:
    0:LIVING
    1:DECEASED

    Return:
    1 = event/death
    0 = censored/alive
    """
    if pd.isna(status):
        return pd.NA

    s = str(status).strip().lower()

    if "deceased" in s or s.startswith("1:"):
        return 1

    if "living" in s or s.startswith("0:"):
        return 0

    return pd.NA


def plot_km(df, group_col, output_file, title):
    kmf = KaplanMeierFitter()

    plt.figure(figsize=(8, 6))

    group_order = ["Basal", "Her2", "LumA", "LumB"]

    for group in group_order:
        sub = df[df[group_col] == group].copy()

        if sub.empty:
            continue

        kmf.fit(
            durations=sub["overall_survival_months"],
            event_observed=sub["os_event"],
            label=f"{group} (n={len(sub)})",
        )

        kmf.plot_survival_function(ci_show=False)

    plt.title(title)
    plt.xlabel("Overall survival time (months)")
    plt.ylabel("Survival probability")
    plt.tight_layout()
    plt.savefig(output_file, dpi=300)
    plt.close()

    print("Saved figure:", output_file)


def pairwise_logrank(df, group_col):
    results = []
    groups = sorted(df[group_col].dropna().unique())

    for g1, g2 in itertools.combinations(groups, 2):
        d1 = df[df[group_col] == g1]
        d2 = df[df[group_col] == g2]

        test = logrank_test(
            d1["overall_survival_months"],
            d2["overall_survival_months"],
            event_observed_A=d1["os_event"],
            event_observed_B=d2["os_event"],
        )

        results.append({
            "grouping": group_col,
            "group_1": g1,
            "group_2": g2,
            "n_group_1": len(d1),
            "n_group_2": len(d2),
            "test_statistic": test.test_statistic,
            "p_value": test.p_value,
        })

    return results


def main():
    print("Loading METABRIC prediction file...")
    pred = pd.read_csv(PRED_FILE)
    print("Prediction shape:", pred.shape)
    print(pred.head())

    print("\nLoading METABRIC clinical file...")
    clinical = load_cbioportal_clinical(CLINICAL_FILE)
    print("Clinical shape:", clinical.shape)

    clinical_small = clinical[
        [
            "#Patient Identifier",
            "Overall Survival (Months)",
            "Overall Survival Status",
            "Pam50 + Claudin-low subtype",
        ]
    ].copy()

    clinical_small = clinical_small.rename(
        columns={
            "#Patient Identifier": "sample_id",
            "Overall Survival (Months)": "overall_survival_months",
            "Overall Survival Status": "overall_survival_status",
            "Pam50 + Claudin-low subtype": "clinical_pam50_subtype",
        }
    )

    clinical_small["overall_survival_months"] = pd.to_numeric(
        clinical_small["overall_survival_months"],
        errors="coerce",
    )

    clinical_small["os_event"] = clinical_small["overall_survival_status"].apply(
        clean_os_status
    )

    print("\nClinical survival status counts:")
    print(clinical_small["overall_survival_status"].value_counts(dropna=False))

    print("\nCleaned OS event counts:")
    print(clinical_small["os_event"].value_counts(dropna=False))

    print("\nMerging predictions with survival data...")
    df = pred.merge(clinical_small, on="sample_id", how="inner")

    print("Merged shape before survival filtering:", df.shape)

    df = df.dropna(subset=["overall_survival_months", "os_event"]).copy()
    df["os_event"] = df["os_event"].astype(int)

    print("Merged shape after survival filtering:", df.shape)

    print("\nTrue subtype counts:")
    print(df["true_subtype"].value_counts())

    print("\nPredicted subtype counts:")
    print(df["predicted_subtype"].value_counts())

    print("\nMedian survival by true subtype:")
    print(df.groupby("true_subtype")["overall_survival_months"].median())

    print("\nMedian survival by predicted subtype:")
    print(df.groupby("predicted_subtype")["overall_survival_months"].median())

    df.to_csv(SURVIVAL_DATASET_OUT, index=False)
    print("\nSaved survival dataset:", SURVIVAL_DATASET_OUT)

    print("\nCreating Kaplan-Meier plots...")
    plot_km(
        df,
        group_col="true_subtype",
        output_file=FIG_TRUE_OUT,
        title="METABRIC Overall Survival by True Subtype",
    )

    plot_km(
        df,
        group_col="predicted_subtype",
        output_file=FIG_PRED_OUT,
        title="METABRIC Overall Survival by TCGA-Model Predicted Subtype",
    )

    print("\nRunning pairwise log-rank tests...")
    results = []
    results.extend(pairwise_logrank(df, "true_subtype"))
    results.extend(pairwise_logrank(df, "predicted_subtype"))

    results_df = pd.DataFrame(results)
    results_df.to_csv(LOGRANK_OUT, index=False)

    print(results_df)
    print("\nSaved log-rank results:", LOGRANK_OUT)

    print("\n✅ METABRIC survival analysis completed successfully.")


if __name__ == "__main__":
    main()
