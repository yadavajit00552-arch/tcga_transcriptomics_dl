# TCGA Transcriptomics Deep Learning Project

Project name: `tcga_transcriptomics_dl`

## Overview

This project analyzes TCGA breast cancer transcriptomic data using machine learning and neural networks.

The first beginner goal is to classify breast cancer molecular subtypes using RNA-seq expression data from the TCGA-BRCA cohort.

## Main cohort

- TCGA-BRCA: Breast invasive carcinoma

## Beginner objective

Classify breast cancer molecular subtypes using RNA-seq gene expression profiles.

## Planned workflow

1. Download TCGA-BRCA RNA-seq expression data
2. Download clinical and molecular subtype metadata
3. Clean and match sample identifiers
4. Preprocess expression matrix
5. Perform exploratory data analysis
6. Train baseline machine learning models
7. Train neural network models
8. Evaluate model performance
9. Interpret important genes and pathways
10. Prepare figures, tables, and report

## Environment setup

Create the conda environment:

    conda env create -f envs/environment.yml

Activate the environment:

    conda activate tcga_dl

Verify Python:

    python --version
    which python

## Reproducibility notes

Large data files, model checkpoints, logs, and generated figures are ignored by Git using `.gitignore`.

Folder structure is preserved using `.gitkeep` files.

## Current status

- [x] Project directory created
- [x] Conda environment file created
- [x] Conda environment installed
- [x] Core packages verified
- [x] `.gitignore` configured
- [x] README created
- [ ] Data download scripts
- [ ] TCGA-BRCA RNA-seq data download
- [ ] Metadata download
- [ ] Preprocessing pipeline
- [ ] Baseline models
- [ ] Neural network model
