#!/usr/bin/env python3
"""
K-Nearest Neighbors Training Script

Train KNN classifier on iris data.

Usage:
    python train.py
    python train.py --k 5 --metric euclidean
"""

import argparse
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.model_selection import cross_val_score, train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import LabelEncoder, StandardScaler

SCRIPT_DIR = Path(__file__).parent
DATA_DIR = SCRIPT_DIR.parent / "data"
MODEL_DIR = SCRIPT_DIR / "model"


def train_model(
    k: int = 5,
    metric: str = "euclidean",
    weights: str = "uniform",
    test_size: float = 0.2,
    random_state: int = 42,
) -> dict:
    """Train KNN classifier."""
    print(f"\n{'='*60}")
    print(f"Training KNN (k={k}, metric={metric}, weights={weights})")
    print(f"{'='*60}")
    
    # Load data
    df = pd.read_csv(DATA_DIR / "iris.csv")
    X = df.drop("species", axis=1)
    y = df["species"]
    
    # Encode labels
    le = LabelEncoder()
    y_encoded = le.fit_transform(y)
    
    print(f"\nDataset: {len(X)} samples, {X.shape[1]} features")
    print(f"Classes: {list(le.classes_)}")
    
    # Train/test split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y_encoded, test_size=test_size, random_state=random_state, stratify=y_encoded
    )
    
    # Scale features (critical for KNN!)
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    # Train model
    model = KNeighborsClassifier(
        n_neighbors=k,
        metric=metric,
        weights=weights,
    )
    model.fit(X_train_scaled, y_train)
    
    # Evaluate
    y_pred = model.predict(X_test_scaled)
    
    print("\n" + "-" * 40)
    print("RESULTS")
    print("-" * 40)
    print(f"Accuracy: {accuracy_score(y_test, y_pred):.4f}")
    
    # Cross-validation for K selection
    print("\n" + "-" * 40)
    print("K SELECTION (Cross-Validation)")
    print("-" * 40)
    
    X_scaled = scaler.fit_transform(X)
    for test_k in [1, 3, 5, 7, 9, 11]:
        knn = KNeighborsClassifier(n_neighbors=test_k, metric=metric)
        scores = cross_val_score(knn, X_scaled, y_encoded, cv=5)
        print(f"k={test_k:2d}: {scores.mean():.4f} (+/- {scores.std()*2:.4f})")
    
    # Confusion Matrix
    print("\nConfusion Matrix:")
    print(confusion_matrix(y_test, y_pred))
    
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred, target_names=le.classes_))
    
    # Save model
    MODEL_DIR.mkdir(exist_ok=True)
    joblib.dump(model, MODEL_DIR / "model.joblib")
    joblib.dump(scaler, MODEL_DIR / "scaler.joblib")
    joblib.dump(le, MODEL_DIR / "label_encoder.joblib")
    joblib.dump(list(X.columns), MODEL_DIR / "features.joblib")
    
    print(f"\nModel saved to: {MODEL_DIR / 'model.joblib'}")
    
    return {"model": model, "accuracy": accuracy_score(y_test, y_pred)}


def main():
    parser = argparse.ArgumentParser(description="Train KNN")
    parser.add_argument("--k", type=int, default=5, help="Number of neighbors")
    parser.add_argument("--metric", type=str, default="euclidean", 
                       choices=["euclidean", "manhattan", "cosine"])
    parser.add_argument("--weights", type=str, default="uniform",
                       choices=["uniform", "distance"])
    
    args = parser.parse_args()
    train_model(k=args.k, metric=args.metric, weights=args.weights)


if __name__ == "__main__":
    main()
