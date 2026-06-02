# TCGA-BRCA Transcriptomics Deep Learning Project: Interview Summary

## 1. One-line project explanation

I built a reproducible machine learning and neural network pipeline to classify TCGA-BRCA breast cancer molecular subtypes using RNA-seq gene expression data, and then interpreted the model using important genes and pathway enrichment.

## 2. Big picture

Breast cancer has different molecular subtypes such as LumA, LumB, Basal, and Her2.

These subtypes behave differently biologically and clinically.

RNA-seq gives gene-expression values for thousands of genes, so the main question was:

Can we use transcriptomic profiles to predict breast cancer molecular subtype?

## 3. Dataset used

I used the TCGA-BRCA cohort.

Raw expression data:

- 20,530 genes
- 1,218 total samples
- 1,097 primary tumor samples

After merging with subtype metadata and removing the small Normal-like group:

- Final modeling samples: 821
- Classes: LumA, LumB, Basal, Her2

Class distribution:

| Subtype | Samples |
|---|---:|
| LumA | 421 |
| LumB | 192 |
| Basal | 141 |
| Her2 | 67 |

## 4. What I did step by step

1. Downloaded TCGA-BRCA RNA-seq expression data.
2. Filtered primary tumor samples.
3. Fetched PAM50 subtype labels from UCSC Xena.
4. Merged expression data with subtype labels.
5. Removed the small Normal class.
6. Created a 4-class classification dataset.
7. Split data into train, validation, and test sets using stratification.
8. Selected top 5,000 variable genes using train data only.
9. Scaled features using train data only.
10. Trained Logistic Regression.
11. Trained Random Forest.
12. Trained an MLP neural network.
13. Compared model performance.
14. Extracted important genes from Logistic Regression coefficients.
15. Performed pathway enrichment.
16. Generated plots and a reproducible run_all.sh pipeline.

## 5. Why stratified split was important

The dataset was imbalanced.

LumA had the most samples and Her2 had the fewest.

So I used stratified splitting to preserve the subtype proportions in train, validation, and test sets.

This avoids a situation where the small Her2 class becomes underrepresented in one split.

## 6. Why I used macro F1 and balanced accuracy

Accuracy alone can be misleading in imbalanced datasets.

Macro F1 treats all classes equally.

Balanced accuracy averages recall across classes.

So these metrics are better for checking whether the model performs well on minority classes like Her2.

## 7. Models trained

| Model | Test Accuracy | Balanced Accuracy | Macro F1 |
|---|---:|---:|---:|
| Logistic Regression | 0.8909 | 0.8995 | 0.8821 |
| MLP Neural Network | 0.8606 | 0.8477 | 0.8561 |
| Random Forest | 0.8727 | 0.7826 | 0.8204 |

## 8. Best model

The best model was Logistic Regression.

It achieved:

- Test accuracy: 0.8909
- Balanced accuracy: 0.8995
- Macro F1: 0.8821

## 9. Why Logistic Regression beat MLP

This suggests that TCGA-BRCA molecular subtype signal is strongly and largely linearly separable in RNA-seq expression space.

In simple words:

The subtype groups already have clear gene-expression patterns, so a simpler linear model can separate them well.

The MLP was useful as a neural network benchmark, but it did not outperform Logistic Regression.

This also shows that deep learning is not always better, especially when:

- sample size is moderate
- signal is already strong
- model interpretability matters
- linear structure is sufficient

## 10. What the model learned biologically

Logistic Regression coefficients were used to find genes that pushed predictions toward each subtype.

Important genes:

| Subtype | Important genes | Meaning |
|---|---|---|
| Basal | FOXC1, FZD9, ZIC1 | Basal-like transcriptional signal |
| Her2 | ERBB2, GRB7, PGAP3, GSDMB | HER2/ERBB2 subtype biology |
| LumA | ERBB4, ADCY1, SLC40A1, GPR143 | Luminal/hormone-associated biology |
| LumB | BIRC5, NUF2, GTSE1, ASPM, DEPDC1 | Proliferation and cell-cycle biology |

The strongest validation was that Her2 prediction was associated with ERBB2 and GRB7.

That means the model learned real breast cancer biology, not random noise.

## 11. Pathway enrichment findings

The subtype-specific genes were tested for pathway enrichment.

Important results:

| Subtype | Enriched pathway | Interpretation |
|---|---|---|
| Her2 | GRB7 Events in ERBB2 Signaling | HER2 receptor signaling captured |
| LumA | Estrogen Response Early | Luminal hormone biology captured |
| LumB | E2F Targets / Cell Cycle | High-proliferation LumB biology captured |
| Basal | Elastic fibre / EMT-related signal | Weaker basal-associated signal |

## 12. SHAP explainability findings

I also added SHAP explainability for the best model, Logistic Regression.

SHAP helped identify which genes contributed most strongly to predictions across the test set.

Top SHAP genes included:

- FADS1
- GRB7
- GTSE1
- CENPA
- ASPM
- FOXM1
- ESR1
- DEPDC1
- NUF2
- ERBB2
- BIRC5

The important point is that SHAP again recovered biologically meaningful genes:

| Signal | SHAP genes |
|---|---|
| HER2 biology | GRB7, ERBB2, C17orf37 |
| Luminal/ER biology | ESR1 |
| Cell cycle/proliferation | FOXM1, BIRC5, NUF2, RRM2, CENPA, ASPM |
| Lipid/metabolic signal | FADS1, FADS2 |

So now the interpretation has two layers:

1. Logistic Regression coefficients show which genes push toward each subtype.
2. SHAP shows which genes contribute most strongly to predictions globally.

## 13. Main scientific conclusion

RNA-seq expression profiles can classify TCGA-BRCA molecular subtypes with high accuracy.

The best model was Logistic Regression, suggesting that breast cancer subtype identity is strongly encoded in transcriptomic expression and is largely linearly separable.

The model-derived genes and pathways recovered known breast cancer biology.

## 14. How I would explain this in 30 seconds

I built a reproducible TCGA-BRCA RNA-seq machine learning pipeline to classify breast cancer molecular subtypes. I used PAM50 subtype labels, filtered primary tumors, created train-validation-test splits, selected the top 5,000 variable genes, and trained Logistic Regression, Random Forest, and an MLP neural network. Logistic Regression performed best with around 89% test accuracy and 0.88 macro F1, suggesting that subtype signal is strongly linearly separable. I then interpreted the model and found biologically meaningful genes such as ERBB2 and GRB7 for Her2, FOXC1 for Basal, and cell-cycle genes like BIRC5 and NUF2 for LumB. Pathway enrichment confirmed ERBB2 signaling, estrogen response, and E2F/cell-cycle pathways.

## 15. How I would explain this in 2 minutes

This project focused on classifying TCGA-BRCA breast cancer molecular subtypes using RNA-seq gene expression data. I started with the TCGA-BRCA expression matrix and filtered primary tumor samples. Then I fetched PAM50-related subtype metadata from UCSC Xena and merged it with expression data.

After removing the small Normal-like class, I created a 4-class dataset with LumA, LumB, Basal, and Her2 samples. I used stratified splitting to create train, validation, and test sets, because the dataset was imbalanced. Feature selection was done using only the training set, where I selected the top 5,000 most variable genes, followed by standard scaling.

I trained three models: Logistic Regression, Random Forest, and an MLP neural network. Logistic Regression performed best, with test accuracy around 0.89 and macro F1 around 0.88. This suggests that breast cancer molecular subtypes are strongly encoded in RNA-seq expression and can be separated well using a linear model.

For interpretation, I extracted Logistic Regression coefficients. The Her2 subtype was associated with ERBB2, GRB7, PGAP3, and GSDMB, which strongly validates that the model learned real HER2 biology. LumB was associated with proliferation and cell-cycle genes such as BIRC5, NUF2, GTSE1, and ASPM. Pathway enrichment confirmed ERBB2 signaling for Her2, estrogen response for LumA, and E2F/cell-cycle pathways for LumB.

Overall, the project shows not only predictive performance but also biological interpretability.

## 16. Important limitations

1. The project used only TCGA-BRCA.
2. External validation is still needed.
3. MLP hyperparameter tuning was limited.
4. Pathway enrichment used top 30 positive genes per subtype.
5. Survival analysis was not yet performed.
6. Some subtype labels depend on metadata completeness.

## 17. Future work

Next steps:

1. SHAP analysis for feature attribution.
2. Integrated Gradients for MLP interpretation.
3. External validation on another breast cancer dataset.
4. Survival analysis by subtype or model probability.
5. Hyperparameter tuning for neural networks.
6. Testing SVM, Elastic Net, or XGBoost.
7. Expanding to pan-cancer subtype classification.

## 18. Most important thing to remember

This project is strong because it is not only predictive.

It also connects:

Data → model → genes → pathways → biology

That makes it a computational biology project, not just a machine learning exercise.



## METABRIC External Validation

I also externally validated the TCGA-trained model on the independent METABRIC breast cancer cohort.

This was important because TCGA uses RNA-seq expression data, while METABRIC uses Illumina microarray expression data. So this tested whether the subtype signal learned from TCGA could transfer across cohorts and platforms.

The TCGA model used 5,000 selected genes, and 4,311 of these genes overlapped with METABRIC. After filtering METABRIC to the same four classes, the external validation dataset contained 1,608 samples.

Raw METABRIC microarray expression initially failed because the model predicted almost all samples as LumA. This showed a platform-shift problem.

After switching to METABRIC z-score expression, performance improved strongly:

- METABRIC external accuracy: 0.8178
- METABRIC balanced accuracy: 0.7840
- METABRIC macro F1: 0.8057
- METABRIC weighted F1: 0.8161

Interview explanation:

The key lesson was that external validation is not only about applying a model to another dataset. The expression scale and platform matter. TCGA RNA-seq and METABRIC microarray data are not directly comparable in raw form. Once I used METABRIC z-score expression, the model recovered transferable subtype biology.

Best short answer:

I trained a TCGA-BRCA RNA-seq subtype classifier and externally validated it on METABRIC. Raw microarray expression failed due to platform shift, but using METABRIC z-score expression improved external validation to 0.818 accuracy and 0.806 macro F1. This showed that breast cancer subtype signals are transferable across cohorts when normalization is handled carefully.



## Survival Analysis Extension

After external validation, I added survival analysis using METABRIC clinical outcome data.

I merged TCGA-model-predicted METABRIC subtype labels with overall survival months and survival status from the METABRIC clinical file.

The survival analysis showed that true subtype groups had expected survival differences. LumA had the longest median survival, while Basal had the shortest.

Importantly, model-predicted subtype groups also showed survival separation:

- Predicted LumA median survival: 128.07 months
- Predicted LumB median survival: 108.52 months
- Predicted Basal median survival: 84.28 months
- Predicted Her2 median survival: 77.30 months

This suggests that the model predictions were not only statistically accurate but also clinically meaningful.

Best short answer:

After external validation, I performed survival analysis in METABRIC. Both true and model-predicted subtype groups showed survival separation, supporting that the classifier captured clinically relevant subtype biology.
