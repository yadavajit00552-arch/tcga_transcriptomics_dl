"""
Fetch TCGA-BRCA molecular subtype metadata from UCSC Xena.

Input:
- TCGA.BRCA.sampleMap/BRCA_clinicalMatrix from Xena hub

Output:
- data/processed/brca_subtype_metadata.csv

Main target:
- PAM50Call_RNAseq decoded into molecular_subtype
"""

from pathlib import Path
import pandas as pd
import xenaPython as xena


HUB = "https://tcga.xenahubs.net"
DATASET = "TCGA.BRCA.sampleMap/BRCA_clinicalMatrix"

OUTPUT_PATH = Path("data/processed/brca_subtype_metadata.csv")

FIELDS = [
    "PAM50Call_RNAseq",
    "PAM50_mRNA_nature2012",
    "ER_Status_nature2012",
    "PR_Status_nature2012",
    "HER2_Final_Status_nature2012",
]


CODE_MAPS = {
    "PAM50Call_RNAseq": {
        1: "Normal",
        2: "LumA",
        3: "LumB",
        4: "Basal",
        5: "Her2",
    },
    "PAM50_mRNA_nature2012": {
        1: "Luminal A",
        2: "Basal-like",
        3: "Luminal B",
        4: "HER2-enriched",
        5: "Normal-like",
    },
    "ER_Status_nature2012": {
        1: "Positive",
        2: "Negative",
        3: "Indeterminate",
    },
    "PR_Status_nature2012": {
        1: "Negative",
        2: "Positive",
        3: "Indeterminate",
    },
    "HER2_Final_Status_nature2012": {
        1: "Negative",
        2: "Positive",
        3: "Equivocal",
    },
}


def decode_value(value, field):
    """Decode Xena categorical numeric codes into readable labels."""
    if value == "NaN" or pd.isna(value):
        return pd.NA

    try:
        code = int(value)
    except (ValueError, TypeError):
        return value

    return CODE_MAPS.get(field, {}).get(code, value)


def main():
    print("Hub:", HUB)
    print("Dataset:", DATASET)

    print("Fetching sample IDs...")
    samples = xena.dataset_samples(HUB, DATASET, None)

    print("Number of clinical samples:", len(samples))

    print("Fetching clinical fields:")
    for field in FIELDS:
        print("-", field)

    fetched = xena.dataset_fetch(HUB, DATASET, samples, FIELDS)

    metadata = pd.DataFrame({"sample_id": samples})

    for field, values in zip(FIELDS, fetched):
        metadata[field] = values
        metadata[field + "_decoded"] = [
            decode_value(value, field) for value in values
        ]

    metadata["molecular_subtype"] = metadata["PAM50Call_RNAseq_decoded"]

    print("Raw metadata shape:", metadata.shape)

    before = metadata.shape[0]
    metadata = metadata.dropna(subset=["molecular_subtype"]).copy()
    after = metadata.shape[0]

    print("Samples before subtype filtering:", before)
    print("Samples with molecular subtype:", after)

    print("\nSubtype counts:")
    print(metadata["molecular_subtype"].value_counts(dropna=False))

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    metadata.to_csv(OUTPUT_PATH, index=False)

    print("\nSaved:", OUTPUT_PATH)
    print("\nPreview:")
    print(metadata.head())


if __name__ == "__main__":
    main()
