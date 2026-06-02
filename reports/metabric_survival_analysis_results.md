# METABRIC Survival Analysis Results

## Goal

The goal of this analysis was to test whether METABRIC breast cancer subtype labels and TCGA-model-predicted subtype labels show clinically meaningful survival differences.

This adds a clinical-outcome layer to the project.

## Data used

| File | Purpose |
|---|---|
| results/tables/external_validation/metabric_zscore_external_logistic_regression_predictions.csv | METABRIC true and predicted subtype labels |
| data/external/metabric/brca_metabric/data_clinical_patient.txt | METABRIC overall survival data |

## Survival columns used

| Column | Meaning |
|---|---|
| Overall Survival (Months) | Survival time |
| Overall Survival Status | Living/deceased event status |

The event coding was:

| Clinical status | Event code |
|---|---:|
| 0:LIVING | 0 |
| 1:DECEASED | 1 |

## Dataset summary

After merging METABRIC predictions with survival data, 1,608 samples were available.

### True subtype counts

| True subtype | Samples |
|---|---:|
| LumA | 700 |
| LumB | 475 |
| Her2 | 224 |
| Basal | 209 |

### Predicted subtype counts

| Predicted subtype | Samples |
|---|---:|
| LumA | 790 |
| LumB | 446 |
| Her2 | 206 |
| Basal | 166 |

## Median survival by true subtype

| True subtype | Median survival months |
|---|---:|
| LumA | 130.08 |
| LumB | 104.10 |
| Her2 | 97.07 |
| Basal | 85.50 |

Interpretation:

LumA showed the longest median survival, while Basal showed the shortest median survival. This is biologically consistent with LumA generally having a better prognosis and Basal-like tumors often being more aggressive.

## Median survival by predicted subtype

| Predicted subtype | Median survival months |
|---|---:|
| LumA | 128.07 |
| LumB | 108.52 |
| Basal | 84.28 |
| Her2 | 77.30 |

Interpretation:

The TCGA-model-predicted subtype labels also preserved clinically meaningful survival differences. Predicted LumA had the best survival, while predicted Her2 and Basal groups had lower median survival.

## Important log-rank results

### True subtype comparisons

| Comparison | p-value | Interpretation |
|---|---:|---|
| LumA vs LumB | 2.92e-09 | Significant survival difference |
| Her2 vs LumA | 6.36e-08 | Significant survival difference |
| Basal vs LumA | 1.10e-02 | Significant survival difference |

### Predicted subtype comparisons

| Comparison | p-value | Interpretation |
|---|---:|---|
| Predicted LumA vs LumB | 3.29e-06 | Significant survival difference |
| Predicted Her2 vs LumA | 2.99e-08 | Significant survival difference |
| Predicted Basal vs LumA | 6.10e-02 | Borderline / not significant at 0.05 |

## Generated outputs

| Output | Purpose |
|---|---|
| results/figures/metabric_survival_by_true_subtype.png | Kaplan-Meier survival curves by true subtype |
| results/figures/metabric_survival_by_predicted_subtype.png | Kaplan-Meier survival curves by predicted subtype |
| results/tables/external_validation/metabric_survival_dataset.csv | Merged prediction-survival dataset |
| results/tables/external_validation/metabric_survival_logrank_results.csv | Pairwise log-rank test results |

## Main conclusion

METABRIC true subtypes showed expected survival differences, with LumA having the longest median survival and Basal having the shortest. Importantly, TCGA-model-predicted subtypes also preserved survival separation, suggesting that the model predictions capture clinically meaningful transcriptomic subtype signals.

## Report-ready summary

Survival analysis on METABRIC showed that both true molecular subtypes and TCGA-model-predicted subtypes were associated with overall survival differences. True LumA samples had the longest median survival, while Basal samples had the shortest. Predicted subtype groups also showed survival separation, including significant differences between predicted LumA and LumB and between predicted Her2 and LumA. This supports the clinical relevance of the transcriptomic classifier beyond classification accuracy alone.
