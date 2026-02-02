#!/usr/bin/env python3
"""
SVM Training Script

Train SVM with different kernels on iris data.

Usage:
    python train.py
    python train.py --kernel rbf --C 1.0
"""

import argparse
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from sklearn.metrics import accuracy_score, classification_report
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.svm import SVC

SCRIPT_DIR = Path(__file__).parent
DATA_DIR = SCRIPT_DIR.parent / "data"
MODEL_DIR = SCRIPT_DIR / "model"


def train_model(
    kernel: str = "rbf",
    C: float = 1.0,
    gamma: str = "scale",
    test_size: float = 0.2,
    random_state: int = 42,
) -> dict:
    """Train SVM classifier."""
    print(f"\n{'='*60}")
    print(f"Training SVM (kernel={kernel}, C={C}, gamma={gamma})")
    print(f"{'='*60}")
    
    # Load data
    df = pd.read_csv(DATA_DIR / "iris.csv")
    X = df.drop("species", axis=1)
    y = df["species"]
    
    le = LabelEncoder()
    y_encoded = le.fit_transform(y)
    
    print(f"\nDataset: {len(X)} samples")
    
    # Split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y_encoded, test_size=test_size, random_state=random_state, stratify=y_encoded
    )
    
    # Scale
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    # Train model
    model = SVC(kernel=kernel, C=C, gamma=gamma, probability=True, random_state=random_state)
    model.fit(X_train_scaled, y_train)
    
    # Evaluate
    y_pred = model.predict(X_test_scaled)
    accuracy = accuracy_score(y_test, y_pred)
    
    print("\n" + "-" * 40)
    print("RESULTS")
    print("-" * 40)
    print(f"Accuracy: {accuracy:.4f}")
    print(f"Support Vectors: {model.n_support_} (total: {sum(model.n_support_)})")
    
    # Compare kernels
    print("\n" + "-" * 40)
    print("KERNEL COMPARISON")
    print("-" * 40)
    
    X_scaled = scaler.fit_transform(X)
    for test_kernel in ["linear", "poly", "rbf", "sigmoid"]:
        svm = SVC(kernel=test_kernel, C=C, random_state=random_state)
        svm.fit(X_train_scaled, y_train)
        acc = accuracy_score(y_test, svm.predict(X_test_scaled))
        print(f"{test_kernel:<10}: {acc:.4f}")
    
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred, target_names=le.classes_))
    
    # Save
    MODEL_DIR.mkdir(exist_ok=True)
    joblib.dump(model, MODEL_DIR / "model.joblib")
    joblib.dump(scaler, MODEL_DIR / "scaler.joblib")
    joblib.dump(le, MODEL_DIR / "label_encoder.joblib")
    joblib.dump(list(X.columns), MODEL_DIR / "features.joblib")
    
    print(f"\nModel saved to: {MODEL_DIR / 'model.joblib'}")
    
    return {"model": model, "accuracy": accuracy}


def main():
    parser = argparse.ArgumentParser(description="Train SVM")
    parser.add_argument("--kernel", type=str, default="rbf",
                       choices=["linear", "poly", "rbf", "sigmoid"])
    parser.add_argument("--C", type=float, default=1.0)
    parser.add_argument("--gamma", type=str, default="scale")
    
    args = parser.parse_args()
    train_model(kernel=args.kernel, C=args.C, gamma=args.gamma)


if __name__ == "__main__":
    main()
