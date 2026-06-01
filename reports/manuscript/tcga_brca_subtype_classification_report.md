# RNA-seq-Based Classification of TCGA-BRCA Molecular Subtypes Using Machine Learning and Neural Networks

## Abstract

Breast cancer is a heterogeneous disease with clinically and biologically distinct molecular subtypes. In this project, TCGA-BRCA RNA-seq expression data were used to classify four breast cancer molecular subtypes: LumA, LumB, Basal, and Her2. A reproducible machine learning pipeline was developed using transcriptomic profiles, PAM50-related subtype labels, stratified train-validation-test splitting, feature selection, classical machine learning models, and a neural network model.

After preprocessing, 821 primary tumor samples and 20,530 gene-expression features were available. The top 5,000 most variable genes were selected using the training set only, and features were standardized without test-set leakage. Logistic Regression, Random Forest, and a multilayer perceptron neural network were trained and evaluated.

Logistic Regression achieved the best test performance, with accuracy of 0.8909, balanced accuracy of 0.8995, and macro F1 score of 0.8821. The MLP neural network performed well but did not outperform the linear baseline. Model interpretation showed biologically meaningful subtype-associated genes, including ERBB2 and GRB7 for Her2, FOXC1 for Basal, and proliferation-associated genes such as BIRC5, NUF2, GTSE1, and ASPM for LumB. Pathway enrichment further supported subtype biology, identifying ERBB2 signaling in Her2, estrogen response in LumA, and E2F/cell-cycle pathways in LumB.

Overall, the results show that TCGA-BRCA molecular subtype identity is strongly encoded in RNA-seq expression profiles and can be classified accurately using interpretable machine learning models.

## 1. Introduction

Breast cancer is not a single disease but a group of molecularly distinct tumor types. Molecular subtyping helps explain differences in tumor biology, prognosis, and treatment response. Common breast cancer subtypes include LumA, LumB, Basal-like, and Her2-enriched tumors.

RNA-seq measures gene-expression levels across thousands of genes. Because molecular subtypes are partly defined by transcriptional programs, RNA-seq data can be used to classify breast cancer samples computationally.

The goal of this project was to build a beginner-to-intermediate, reproducible machine learning pipeline for classifying TCGA-BRCA molecular subtypes using RNA-seq expression data.

## 2. Objectives

The main objectives were:

1. Download and preprocess TCGA-BRCA RNA-seq expression data.
2. Fetch PAM50-related subtype labels from UCSC Xena clinical metadata.
3. Create a clean 4-class classification dataset.
4. Train baseline machine learning models.
5. Train an MLP neural network.
6. Compare model performance.
7. Interpret important subtype-associated genes.
8. Perform pathway enrichment on model-derived gene lists.
9. Create reproducible scripts, figures, tables, and documentation.

## 3. Materials and Methods

### 3.1 Dataset

The main cohort used in this project was TCGA-BRCA, representing breast invasive carcinoma.

The RNA-seq expression matrix contained:

- 20,530 genes
- 1,218 total samples
- 1,097 primary tumor samples

Only primary tumor samples were retained for modeling.

### 3.2 Molecular subtype labels

Subtype labels were obtained from TCGA-BRCA clinical metadata using UCSC Xena through `xenaPython`.

The original molecular subtype labels included:

- LumA
- LumB
- Basal
- Her2
- Normal

The Normal class was removed because it had only 23 merged samples and was not part of the main 4-class beginner objective.

Final classification classes:

- LumA
- LumB
- Basal
- Her2

### 3.3 Final modeling dataset

After merging expression data with subtype metadata and removing Normal-like samples, the final dataset contained 821 samples.

| Subtype | Samples | Percentage |
|---|---:|---:|
| LumA | 421 | 51.28% |
| LumB | 192 | 23.39% |
| Basal | 141 | 17.17% |
| Her2 | 67 | 8.16% |

### 3.4 Train-validation-test split

The dataset was split using stratified sampling:

| Split | Samples |
|---|---:|
| Train | 524 |
| Validation | 132 |
| Test | 165 |

Stratification preserved subtype proportions across splits.

### 3.5 Feature selection and scaling

The top 5,000 most variable genes were selected using the training data only.

Feature scaling was performed using `StandardScaler` fitted only on the training data. The fitted scaler was then applied to validation and test sets.

This avoided data leakage.

### 3.6 Models

Three models were trained:

1. Logistic Regression
2. Random Forest
3. MLP Neural Network

The Logistic Regression and Random Forest models used balanced class weights to reduce the effect of class imbalance.

The MLP neural network used:

- Input layer: 5,000 genes
- Hidden layer 1: 512 units
- Hidden layer 2: 128 units
- ReLU activation
- Batch normalization
- Dropout
- Cross-entropy loss with class weights
- Adam optimizer
- Early stopping

### 3.7 Evaluation metrics

The models were evaluated using:

- Accuracy
- Balanced accuracy
- Macro F1
- Weighted F1
- Classification report
- Confusion matrix

Macro F1 and balanced accuracy were important because the dataset was imbalanced.

### 3.8 Gene interpretation

Because Logistic Regression was the best-performing model, its coefficients were used for interpretation.

Positive coefficients were interpreted as genes pushing model prediction toward a subtype.

### 3.9 Pathway enrichment

Subtype-specific top positive genes were used for pathway enrichment with GSEApy/Enrichr.

Libraries included:

- MSigDB Hallmark 2020
- KEGG 2021 Human
- Reactome 2022

## 4. Results

### 4.1 Model performance

| Model | Test Accuracy | Balanced Accuracy | Macro F1 | Weighted F1 |
|---|---:|---:|---:|---:|
| Logistic Regression | 0.8909 | 0.8995 | 0.8821 | 0.8909 |
| MLP Neural Network | 0.8606 | 0.8477 | 0.8561 | 0.8555 |
| Random Forest | 0.8727 | 0.7826 | 0.8204 | 0.8635 |

Logistic Regression achieved the best overall performance.

### 4.2 Confusion matrix interpretation

The Logistic Regression test confusion matrix showed:

- Basal: 28/28 correctly classified
- Her2: 12/13 correctly classified
- LumA: 77/85 correctly classified
- LumB: 30/39 correctly classified

The main classification errors occurred between LumA and LumB.

This is biologically reasonable because both are luminal breast cancer subtypes with overlapping transcriptional programs.

### 4.3 PCA and UMAP visualization

PCA and UMAP plots were generated to visualize subtype structure in expression space.

The PCA plot showed that the first two components explained:

- PC1: 12.12%
- PC2: 8.82%

Together, PC1 and PC2 explained about 20.94% of the variance.

These visualizations help show whether molecular subtypes are separated in transcriptomic space before modeling.

### 4.4 Gene importance results

Top subtype-associated genes from Logistic Regression included:

| Subtype | Important genes | Interpretation |
|---|---|---|
| Basal | FOXC1, GDF5, FZD9, ZIC1 | Basal-like transcriptional signal |
| Her2 | ERBB2, GRB7, PGAP3, GSDMB | HER2/ERBB2-amplified biology |
| LumA | ERBB4, ADCY1, SLC40A1, GPR143 | Luminal and hormone-response-associated signal |
| LumB | BIRC5, NUF2, GTSE1, ASPM, DEPDC1 | Proliferation and cell-cycle-associated signal |

The presence of ERBB2 and GRB7 among the top Her2-associated genes strongly supports that the model learned biologically meaningful subtype features.

### 4.5 SHAP explainability results

SHAP analysis was performed for the best-performing Logistic Regression model to identify genes with high global contribution to subtype predictions.

Top global SHAP genes included:

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

These genes support multiple known breast cancer biological programs:

| Biological signal | SHAP-supported genes |
|---|---|
| HER2 signaling | GRB7, ERBB2, C17orf37 |
| Luminal/estrogen receptor biology | ESR1 |
| Proliferation and cell cycle | FOXM1, BIRC5, NUF2, RRM2, CENPA, ASPM |
| Lipid/metabolic subtype signal | FADS1, FADS2 |

SHAP therefore provided an additional model-explainability layer beyond Logistic Regression coefficients. Coefficients showed the direction of subtype association, while SHAP highlighted genes contributing strongly to predictions across the test set.

### 4.6 Pathway enrichment results

Important pathway enrichment findings included:

| Subtype | Enriched pathway | Interpretation |
|---|---|---|
| Her2 | GRB7 Events in ERBB2 Signaling | HER2 receptor signaling captured |
| LumA | Estrogen Response Early | Estrogen/luminal biology captured |
| LumB | E2F Targets | High-proliferation LumB biology captured |
| LumB | Cell Cycle | Cell-cycle biology captured |
| Basal | Elastic fibre-associated Reactome term | Modest basal-associated signal |

These results suggest that model-derived genes recover known breast cancer subtype biology.

## 5. Discussion

The strongest model was Logistic Regression, which outperformed both Random Forest and the MLP neural network by macro F1 score. This suggests that TCGA-BRCA PAM50 subtype structure is strongly represented in RNA-seq expression data and is largely linearly separable.

The MLP neural network performed well but did not outperform Logistic Regression. This does not mean neural networks are useless. Instead, it shows that deeper nonlinear models are not automatically better when the dataset is small-to-moderate in size and the subtype signal is already strong.

The biological interpretation supports the validity of the model. Her2 predictions were associated with ERBB2 and GRB7, LumA was associated with estrogen response, and LumB was associated with E2F and cell-cycle pathways.

Basal tumors were classified almost perfectly, consistent with the idea that basal-like breast cancers have a distinct transcriptomic profile.

## 6. Limitations

Important limitations include:

1. The project used one cohort only, TCGA-BRCA.
2. External validation on an independent breast cancer dataset was not yet performed.
3. Only the top 5,000 variable genes were used.
4. Pathway enrichment was based on relatively short top-gene lists.
5. The MLP neural network was not extensively tuned.
6. Clinical outcome prediction and survival analysis were not yet included.
7. Some subtype labels may depend on metadata availability and annotation quality.


## External Validation on METABRIC

To evaluate whether the TCGA-BRCA subtype classifier generalizes beyond the original cohort, external validation was performed using the independent METABRIC breast cancer cohort.

A major challenge was that TCGA-BRCA expression data are RNA-seq based, whereas METABRIC expression data are Illumina microarray based. Therefore, validation was performed using genes shared between both datasets.

The original TCGA model used 5,000 selected genes. Of these, 4,311 genes were also available in METABRIC, giving an overlap of 86.22%.

The METABRIC validation dataset contained 1,608 samples across the same four classes used in the TCGA model:

| Subtype | Samples |
|---|---:|
| LumA | 700 |
| LumB | 475 |
| Her2 | 224 |
| Basal | 209 |

Initial validation using raw METABRIC microarray expression failed because predictions collapsed mostly to LumA. This indicated strong platform shift between TCGA RNA-seq and METABRIC microarray expression.

After using METABRIC z-score expression, external validation improved substantially:

| Dataset | Accuracy | Balanced Accuracy | Macro F1 | Weighted F1 |
|---|---:|---:|---:|---:|
| TCGA test using shared genes | 0.8970 | 0.9060 | 0.8934 | 0.8970 |
| METABRIC z-score external validation | 0.8178 | 0.7840 | 0.8057 | 0.8161 |

The strongest external validation performance was observed for LumA and Basal samples. The main error pattern was LumB being misclassified as LumA, which is biologically reasonable because LumA and LumB are both luminal subtypes and share hormone-response transcriptional programs.

These results show that breast cancer molecular subtype signals are transferable across independent cohorts when platform-aware normalization is used.


## 7. Future Work

Future improvements include:

1. Perform SHAP analysis for model explainability.
2. Use Integrated Gradients for MLP interpretation.
3. Test Elastic Net, SVM, and XGBoost models.
4. Tune MLP architecture and hyperparameters.
5. Run pathway enrichment with larger subtype gene lists.
6. Perform survival analysis by subtype or prediction probability.
7. Validate the pipeline on an external breast cancer dataset.
8. Prepare a full manuscript-style report with citations.
9. Extend the pipeline to pan-cancer transcriptomic classification.

## 8. Conclusion

This project successfully built a reproducible TCGA-BRCA RNA-seq machine learning pipeline for molecular subtype classification. Logistic Regression achieved the best test performance and provided interpretable subtype-associated genes.

The model-derived gene and pathway results recovered known breast cancer biology, including ERBB2 signaling in Her2 tumors, estrogen response in LumA tumors, and E2F/cell-cycle activity in LumB tumors.

Overall, the project demonstrates that RNA-seq expression data contain strong and biologically meaningful signals for breast cancer molecular subtype classification.

## 9. Reproducibility

The full pipeline can be rerun with:

    conda activate tcga_dl
    bash run_all.sh

All main scripts are stored under `src/`, while generated results are saved under `results/`.


## 10. References

1. The Cancer Genome Atlas Network. Comprehensive molecular portraits of human breast tumours. Nature, 2012.

2. Parker JS et al. Supervised Risk Predictor of Breast Cancer Based on Intrinsic Subtypes. Journal of Clinical Oncology, 2009.

3. Weinstein JN et al. The Cancer Genome Atlas Pan-Cancer analysis project. Nature Genetics, 2013.

4. Chen EY et al. Enrichr: interactive and collaborative HTML5 gene list enrichment analysis tool. BMC Bioinformatics, 2013.

5. Kuleshov MV et al. Enrichr: a comprehensive gene set enrichment analysis web server 2016 update. Nucleic Acids Research, 2016.

6. UCSC Xena Browser / Xena Hubs were used to access TCGA-BRCA expression and clinical metadata.
