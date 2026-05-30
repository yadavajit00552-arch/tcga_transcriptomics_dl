"""
Train MLP neural network for TCGA-BRCA subtype classification.

Inputs:
- data/processed/ml/train_features.csv
- data/processed/ml/val_features.csv
- data/processed/ml/test_features.csv
- data/processed/ml/train_labels.csv
- data/processed/ml/val_labels.csv
- data/processed/ml/test_labels.csv

Outputs:
- results/tables/mlp_validation_metrics.csv
- results/tables/mlp_test_metrics.csv
- results/tables/mlp_test_predictions.csv
- results/tables/mlp_validation_confusion_matrix.csv
- results/tables/mlp_test_confusion_matrix.csv
- results/tables/mlp_training_history.csv
- results/figures/mlp_training_curve.png
- results/models/mlp_model.pt

Purpose:
Train an MLP neural network model for molecular subtype classification.
"""

from pathlib import Path
import random

import numpy as np
import pandas as pd
import torch
from torch import nn
from torch.utils.data import DataLoader, TensorDataset

from sklearn.metrics import (
    accuracy_score,
    balanced_accuracy_score,
    classification_report,
    confusion_matrix,
    f1_score,
)
from sklearn.preprocessing import LabelEncoder

import matplotlib.pyplot as plt


# -----------------------------
# Paths and parameters
# -----------------------------
ML_DIR = Path("data/processed/ml")
RESULTS_TABLE_DIR = Path("results/tables")
RESULTS_MODEL_DIR = Path("results/models")
RESULTS_FIGURE_DIR = Path("results/figures")

TARGET_COLUMN = "molecular_subtype"
RANDOM_SEED = 42

BATCH_SIZE = 32
EPOCHS = 100
LEARNING_RATE = 0.001
PATIENCE = 15


# -----------------------------
# Reproducibility
# -----------------------------
def set_seed(seed: int = 42):
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)

    if torch.backends.mps.is_available():
        torch.mps.manual_seed(seed)

    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)


# -----------------------------
# Model
# -----------------------------
class MLP(nn.Module):
    def __init__(self, input_dim: int, hidden_dim: int, output_dim: int, dropout: float = 0.3):
        super().__init__()

        self.network = nn.Sequential(
            nn.Linear(input_dim, hidden_dim),
            nn.BatchNorm1d(hidden_dim),
            nn.ReLU(),
            nn.Dropout(dropout),

            nn.Linear(hidden_dim, hidden_dim // 2),
            nn.BatchNorm1d(hidden_dim // 2),
            nn.ReLU(),
            nn.Dropout(dropout),

            nn.Linear(hidden_dim // 2, output_dim),
        )

    def forward(self, x):
        return self.network(x)


# -----------------------------
# Data loading
# -----------------------------
def load_data():
    print("Loading ML-ready data...")

    train_features = pd.read_csv(ML_DIR / "train_features.csv")
    val_features = pd.read_csv(ML_DIR / "val_features.csv")
    test_features = pd.read_csv(ML_DIR / "test_features.csv")

    train_labels = pd.read_csv(ML_DIR / "train_labels.csv")
    val_labels = pd.read_csv(ML_DIR / "val_labels.csv")
    test_labels = pd.read_csv(ML_DIR / "test_labels.csv")

    sample_col = "sample_id"

    train_sample_ids = train_features[sample_col].astype(str).values
    val_sample_ids = val_features[sample_col].astype(str).values
    test_sample_ids = test_features[sample_col].astype(str).values

    X_train = train_features.drop(columns=[sample_col]).values.astype(np.float32)
    X_val = val_features.drop(columns=[sample_col]).values.astype(np.float32)
    X_test = test_features.drop(columns=[sample_col]).values.astype(np.float32)

    y_train_raw = train_labels[TARGET_COLUMN].values
    y_val_raw = val_labels[TARGET_COLUMN].values
    y_test_raw = test_labels[TARGET_COLUMN].values

    label_encoder = LabelEncoder()
    y_train = label_encoder.fit_transform(y_train_raw)
    y_val = label_encoder.transform(y_val_raw)
    y_test = label_encoder.transform(y_test_raw)

    print(f"X_train shape: {X_train.shape}")
    print(f"X_val shape: {X_val.shape}")
    print(f"X_test shape: {X_test.shape}")

    print("\nClass encoding:")
    for class_name, class_id in zip(label_encoder.classes_, label_encoder.transform(label_encoder.classes_)):
        print(f"{class_name}: {class_id}")

    return (
        X_train,
        X_val,
        X_test,
        y_train,
        y_val,
        y_test,
        train_sample_ids,
        val_sample_ids,
        test_sample_ids,
        label_encoder,
    )


# -----------------------------
# Evaluation helper
# -----------------------------
def evaluate_model(model, X, y, sample_ids, label_encoder, device, split_name: str):
    model.eval()

    X_tensor = torch.tensor(X, dtype=torch.float32).to(device)

    with torch.no_grad():
        logits = model(X_tensor)
        probabilities = torch.softmax(logits, dim=1).cpu().numpy()
        y_pred = np.argmax(probabilities, axis=1)

    y_true_labels = label_encoder.inverse_transform(y)
    y_pred_labels = label_encoder.inverse_transform(y_pred)

    accuracy = accuracy_score(y, y_pred)
    balanced_acc = balanced_accuracy_score(y, y_pred)
    macro_f1 = f1_score(y, y_pred, average="macro")
    weighted_f1 = f1_score(y, y_pred, average="weighted")

    print(f"\n{split_name} metrics:")
    print(f"Accuracy: {round(accuracy, 4)}")
    print(f"Balanced accuracy: {round(balanced_acc, 4)}")
    print(f"Macro F1: {round(macro_f1, 4)}")
    print(f"Weighted F1: {round(weighted_f1, 4)}")

    print(f"\n{split_name} classification report:")
    print(classification_report(y_true_labels, y_pred_labels, target_names=label_encoder.classes_))

    cm = confusion_matrix(y_true_labels, y_pred_labels, labels=label_encoder.classes_)
    cm_df = pd.DataFrame(cm, index=label_encoder.classes_, columns=label_encoder.classes_)

    print(f"\n{split_name} confusion matrix:")
    print(cm_df)

    metrics_df = pd.DataFrame(
        [
            {
                "split": split_name,
                "accuracy": accuracy,
                "balanced_accuracy": balanced_acc,
                "macro_f1": macro_f1,
                "weighted_f1": weighted_f1,
            }
        ]
    )

    predictions_df = pd.DataFrame(
        {
            "sample_id": sample_ids,
            "true_label": y_true_labels,
            "predicted_label": y_pred_labels,
        }
    )

    # Add probability columns
    for i, class_name in enumerate(label_encoder.classes_):
        predictions_df[f"prob_{class_name}"] = probabilities[:, i]

    predictions_df["confidence"] = probabilities.max(axis=1)
    predictions_df["correct"] = predictions_df["true_label"] == predictions_df["predicted_label"]

    metrics_df.to_csv(RESULTS_TABLE_DIR / f"mlp_{split_name}_metrics.csv", index=False)
    cm_df.to_csv(RESULTS_TABLE_DIR / f"mlp_{split_name}_confusion_matrix.csv")
    predictions_df.to_csv(RESULTS_TABLE_DIR / f"mlp_{split_name}_predictions.csv", index=False)

    return metrics_df, predictions_df, cm_df


# -----------------------------
# Main
# -----------------------------
def main():
    set_seed(RANDOM_SEED)

    RESULTS_TABLE_DIR.mkdir(parents=True, exist_ok=True)
    RESULTS_MODEL_DIR.mkdir(parents=True, exist_ok=True)
    RESULTS_FIGURE_DIR.mkdir(parents=True, exist_ok=True)

    if torch.backends.mps.is_available():
        device = torch.device("mps")
    elif torch.cuda.is_available():
        device = torch.device("cuda")
    else:
        device = torch.device("cpu")

    print(f"Using device: {device}")

    (
        X_train,
        X_val,
        X_test,
        y_train,
        y_val,
        y_test,
        train_sample_ids,
        val_sample_ids,
        test_sample_ids,
        label_encoder,
    ) = load_data()

    train_dataset = TensorDataset(
        torch.tensor(X_train, dtype=torch.float32),
        torch.tensor(y_train, dtype=torch.long),
    )

    val_dataset = TensorDataset(
        torch.tensor(X_val, dtype=torch.float32),
        torch.tensor(y_val, dtype=torch.long),
    )

    train_loader = DataLoader(train_dataset, batch_size=BATCH_SIZE, shuffle=True)
    val_loader = DataLoader(val_dataset, batch_size=BATCH_SIZE, shuffle=False)

    input_dim = X_train.shape[1]
    hidden_dim = 256
    output_dim = len(label_encoder.classes_)

    model = MLP(input_dim=input_dim, hidden_dim=hidden_dim, output_dim=output_dim, dropout=0.3).to(device)

    criterion = nn.CrossEntropyLoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=LEARNING_RATE, weight_decay=1e-4)

    print("\nTraining MLP model...")

    best_val_loss = float("inf")
    best_epoch = 0
    epochs_without_improvement = 0
    best_model_state = None

    history = []

    for epoch in range(1, EPOCHS + 1):
        model.train()
        train_losses = []

        for batch_X, batch_y in train_loader:
            batch_X = batch_X.to(device)
            batch_y = batch_y.to(device)

            optimizer.zero_grad()
            logits = model(batch_X)
            loss = criterion(logits, batch_y)
            loss.backward()
            optimizer.step()

            train_losses.append(loss.item())

        train_loss = float(np.mean(train_losses))

        model.eval()
        val_losses = []

        with torch.no_grad():
            for batch_X, batch_y in val_loader:
                batch_X = batch_X.to(device)
                batch_y = batch_y.to(device)

                logits = model(batch_X)
                loss = criterion(logits, batch_y)

                val_losses.append(loss.item())

        val_loss = float(np.mean(val_losses))

        history.append(
            {
                "epoch": epoch,
                "train_loss": train_loss,
                "val_loss": val_loss,
            }
        )

        if epoch == 1 or epoch % 10 == 0:
            print(f"Epoch {epoch:03d} | Train loss: {train_loss:.4f} | Val loss: {val_loss:.4f}")

        if val_loss < best_val_loss:
            best_val_loss = val_loss
            best_epoch = epoch
            epochs_without_improvement = 0
            best_model_state = model.state_dict()
        else:
            epochs_without_improvement += 1

        if epochs_without_improvement >= PATIENCE:
            print(f"Early stopping at epoch {epoch}. Best epoch: {best_epoch}")
            break

    if best_model_state is not None:
        model.load_state_dict(best_model_state)

    print("✅ Model training completed.")
    print(f"Best validation loss: {best_val_loss:.4f}")
    print(f"Best epoch: {best_epoch}")

    # Save training history
    history_df = pd.DataFrame(history)
    history_path = RESULTS_TABLE_DIR / "mlp_training_history.csv"
    history_df.to_csv(history_path, index=False)
    print(f"Saved training history to: {history_path}")

    # Save training curve plot
    plt.figure(figsize=(8, 5))
    plt.plot(history_df["epoch"], history_df["train_loss"], label="Train loss")
    plt.plot(history_df["epoch"], history_df["val_loss"], label="Validation loss")
    plt.axvline(best_epoch, linestyle="--", label=f"Best epoch = {best_epoch}")
    plt.xlabel("Epoch")
    plt.ylabel("Loss")
    plt.title("MLP Training and Validation Loss")
    plt.legend()
    plt.tight_layout()

    plot_path = RESULTS_FIGURE_DIR / "mlp_training_curve.png"
    plt.savefig(plot_path, dpi=300)
    plt.close()
    print(f"Saved training curve to: {plot_path}")

    # Evaluate
    evaluate_model(model, X_val, y_val, val_sample_ids, label_encoder, device, "validation")
    evaluate_model(model, X_test, y_test, test_sample_ids, label_encoder, device, "test")

    # Save model
    model_path = RESULTS_MODEL_DIR / "mlp_model.pt"
    torch.save(model.state_dict(), model_path)

    print(f"\nSaved results in: {RESULTS_TABLE_DIR}")
    print(f"Saved model in: {model_path}")
    print("✅ MLP neural network completed successfully.")


if __name__ == "__main__":
    main()
