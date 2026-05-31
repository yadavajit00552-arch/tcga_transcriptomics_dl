"""
Extract important genes from Logistic Regression model.

Inputs:
- data/processed/ml/train_features.csv
- data/processed/ml/train_labels.csv

Outputs:
- results/tables/logistic_regression_coefficients_all.csv
- results/tables/logistic_regression_top_genes_by_subtype.csv

Purpose:
Identify genes that contribute most strongly to each TCGA-BRCA subtype prediction.
"""

from pathlib import Path
import pandas as pd

from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import LabelEncoder


ML_DIR = Path("data/processed/ml")
RESULTS_TABLE_DIR = Path("results/tables")

TARGET_COLUMN = "molecular_subtype"
RANDOM_SEED = 42
TOP_N = 30


def main():
    RESULTS_TABLE_DIR.mkdir(parents=True, exist_ok=True)

    print("Loading train features and labels...")

    X_train = pd.read_csv(ML_DIR / "train_features.csv")
    y_train = pd.read_csv(ML_DIR / "train_labels.csv")

    X_train = X_train.drop(columns=["sample_id"])
    y_train = y_train[TARGET_COLUMN]

    print("X_train shape:", X_train.shape)
    print("y_train shape:", y_train.shape)

    label_encoder = LabelEncoder()
    y_encoded = label_encoder.fit_transform(y_train)

    print("\nClass encoding:")
    for class_name, encoded_value in zip(label_encoder.classes_, range(len(label_encoder.classes_))):
        print(f"{class_name}: {encoded_value}")

    print("\nTraining Logistic Regression model again for coefficient extraction...")

    model = LogisticRegression(
        max_iter=5000,
        class_weight="balanced",
        random_state=RANDOM_SEED,
        solver="lbfgs",
    )

    model.fit(X_train, y_encoded)

    print("✅ Model trained.")

    genes = X_train.columns.tolist()
    classes = label_encoder.classes_.tolist()

    all_rows = []
    top_rows = []

    for class_index, class_name in enumerate(classes):
        coefficients = model.coef_[class_index]

        coef_df = pd.DataFrame({
            "subtype": class_name,
            "gene": genes,
            "coefficient": coefficients,
            "absolute_coefficient": abs(coefficients),
        })

        coef_df = coef_df.sort_values("absolute_coefficient", ascending=False)
        all_rows.append(coef_df)

        top_positive = coef_df.sort_values("coefficient", ascending=False).head(TOP_N).copy()
        top_positive["direction"] = "positive"

        top_negative = coef_df.sort_values("coefficient", ascending=True).head(TOP_N).copy()
        top_negative["direction"] = "negative"

        top_rows.append(top_positive)
        top_rows.append(top_negative)

        print(f"\nTop positive genes for {class_name}:")
        print(top_positive[["gene", "coefficient"]].head(10))

        print(f"\nTop negative genes for {class_name}:")
        print(top_negative[["gene", "coefficient"]].head(10))

    all_coefficients = pd.concat(all_rows, axis=0, ignore_index=True)
    top_genes = pd.concat(top_rows, axis=0, ignore_index=True)

    all_output = RESULTS_TABLE_DIR / "logistic_regression_coefficients_all.csv"
    top_output = RESULTS_TABLE_DIR / "logistic_regression_top_genes_by_subtype.csv"

    all_coefficients.to_csv(all_output, index=False)
    top_genes.to_csv(top_output, index=False)

    print("\nSaved all coefficients:", all_output)
    print("Saved top genes:", top_output)
    print("✅ Logistic Regression gene extraction completed successfully.")


if __name__ == "__main__":
    main()
