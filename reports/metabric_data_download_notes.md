# METABRIC Data Download Notes

## Goal

Obtain METABRIC expression and clinical subtype metadata for external validation of the TCGA-BRCA subtype classifier.

## Recommended source 1: cBioPortal

Study name:

Breast Cancer (METABRIC, Nature 2012 & Nat Commun 2016)

Study ID:

brca_metabric

URL:

https://www.cbioportal.org/study?id=brca_metabric

Useful files to look for:

- clinical sample data
- clinical patient data
- mRNA expression data
- molecular subtype / PAM50 subtype column if available

## Recommended source 2: Kaggle processed METABRIC

Dataset:

Breast Cancer Gene Expression Profiles (METABRIC)

This may be easier to download manually, but may contain a smaller processed gene panel rather than full transcriptome.

## Where to place downloaded files

Put downloaded METABRIC files here:

data/external/metabric/

Supported extensions for the current inspection script:

- .csv
- .tsv
- .txt

## After placing files

Run:

python src/external_validation/inspect_metabric_files.py

This will show:

- available files
- shape of each file
- first columns
- first rows
- possible subtype/clinical columns

## External validation caution

TCGA-BRCA expression was RNA-seq based, while METABRIC expression is commonly microarray-based.

So external validation requires:

1. gene symbol harmonization
2. overlapping feature selection
3. matching feature order
4. use of TCGA-trained scaler only
5. careful interpretation of performance drop due to platform differences
