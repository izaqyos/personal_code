#!/usr/bin/env python3
"""
Random Forest Training Script

Usage:
    python train.py
    python train.py --n-estimators 100 --max-depth 10
"""

import argparse
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

SCRIPT_DIR = Path(__file__).parent
DATA_DIR = SCRIPT_DIR.parent / "data"
MODEL_DIR = SCRIPT_DIR / "model"


def train_model(
    n_estimators: int = 100,
    max_depth: int | None = None,
    test_size: float = 0.2,
    random_state: int = 42,
) -> dict:
    """Train Random Forest classifier."""
    print(f"\n{'='*60}")
    print(f"Training RANDOM FOREST (n_trees={n_estimators})")
    print(f"{'='*60}")
    
    # Load data
    df = pd.read_csv(DATA_DIR / "iris.csv")
    X = df.drop("species", axis=1)
    y = df["species"]
    
    le = LabelEncoder()
    y_encoded = le.fit_transform(y)
    
    print(f"\nDataset: {len(X)} samples, {X.shape[1]} features")
    
    # Split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y_encoded, test_size=test_size, random_state=random_state, stratify=y_encoded
    )
    
    # Train
    model = RandomForestClassifier(
        n_estimators=n_estimators,
        max_depth=max_depth,
        oob_score=True,
        random_state=random_state,
        n_jobs=-1,
    )
    model.fit(X_train, y_train)
    
    # Evaluate
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    
    print("\n" + "-" * 40)
    print("RESULTS")
    print("-" * 40)
    print(f"Test Accuracy: {accuracy:.4f}")
    print(f"OOB Score:     {model.oob_score_:.4f}")
    
    # Feature Importance
    print("\n" + "-" * 40)
    print("FEATURE IMPORTANCE")
    print("-" * 40)
    
    importance_df = pd.DataFrame({
        "feature": X.columns,
        "importance": model.feature_importances_,
    }).sort_values("importance", ascending=False)
    
    for _, row in importance_df.iterrows():
        bar = "█" * int(row["importance"] * 30)
        print(f"{row['feature']:<15} {row['importance']:.4f} {bar}")
    
    # n_estimators comparison
    print("\n" + "-" * 40)
    print("N_ESTIMATORS COMPARISON")
    print("-" * 40)
    
    for n in [10, 50, 100, 200]:
        rf = RandomForestClassifier(n_estimators=n, oob_score=True, random_state=random_state)
        rf.fit(X_train, y_train)
        acc = accuracy_score(y_test, rf.predict(X_test))
        print(f"n_estimators={n:3d}: acc={acc:.4f}, oob={rf.oob_score_:.4f}")
    
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred, target_names=le.classes_))
    
    # Save
    MODEL_DIR.mkdir(exist_ok=True)
    joblib.dump(model, MODEL_DIR / "model.joblib")
    joblib.dump(le, MODEL_DIR / "label_encoder.joblib")
    joblib.dump(list(X.columns), MODEL_DIR / "features.joblib")
    
    print(f"\nModel saved to: {MODEL_DIR / 'model.joblib'}")
    
    return {"model": model, "accuracy": accuracy}


def main():
    parser = argparse.ArgumentParser(description="Train Random Forest")
    parser.add_argument("--n-estimators", type=int, default=100)
    parser.add_argument("--max-depth", type=int, default=None)
    
    args = parser.parse_args()
    train_model(n_estimators=args.n_estimators, max_depth=args.max_depth)


if __name__ == "__main__":
    main()
