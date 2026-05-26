"""
Query UCSC Xena TCGA hub datasets.

Goal:
Find available TCGA-BRCA datasets related to:
1. phenotype
2. clinical
3. subtype
4. PAM50
5. sampleMap

This helps us locate molecular subtype labels for classification.
"""

import xenaPython as xena


HUB = "https://tcga.xenahubs.net"


def main():
    print("Querying Xena hub:")
    print(HUB)

    datasets = xena.all_datasets(HUB)

    print("\nTotal datasets found:", len(datasets))

    keywords = [
        "BRCA",
        "brca",
        "subtype",
        "Subtype",
        "PAM50",
        "pam50",
        "clinical",
        "phenotype",
        "sampleMap",
    ]

    print("\nMatching datasets:")
    matches = []

    for dataset in datasets:
        dataset_str = str(dataset)
        if any(keyword in dataset_str for keyword in keywords):
            matches.append(dataset_str)

    for item in matches:
        print(item)

    print("\nTotal matching datasets:", len(matches))


if __name__ == "__main__":
    main()
