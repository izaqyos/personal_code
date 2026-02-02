#!/usr/bin/env python3
"""
Decision Tree Training Script

Usage:
    python train.py
    python train.py --max-depth 5 --criterion entropy
"""

import argparse
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from sklearn.metrics import accuracy_score, classification_report
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.tree import DecisionTreeClassifier

SCRIPT_DIR = Path(__file__).parent
DATA_DIR = SCRIPT_DIR.parent / "data"
MODEL_DIR = SCRIPT_DIR / "model"


def train_model(
    max_depth: int | None = None,
    criterion: str = "gini",
    min_samples_split: int = 2,
    min_samples_leaf: int = 1,
    test_size: float = 0.2,
    random_state: int = 42,
) -> dict:
    """Train Decision Tree classifier."""
    print(f"\n{'='*60}")
    print(f"Training DECISION TREE")
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
    model = DecisionTreeClassifier(
        max_depth=max_depth,
        criterion=criterion,
        min_samples_split=min_samples_split,
        min_samples_leaf=min_samples_leaf,
        random_state=random_state,
    )
    model.fit(X_train, y_train)
    
    # Evaluate
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    
    print(f"\nCriterion: {criterion}")
    print(f"Max Depth: {max_depth}")
    print(f"Tree Depth: {model.get_depth()}")
    print(f"Leaves: {model.get_n_leaves()}")
    
    print("\n" + "-" * 40)
    print("RESULTS")
    print("-" * 40)
    print(f"Accuracy: {accuracy:.4f}")
    
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
    
    # Depth comparison
    print("\n" + "-" * 40)
    print("DEPTH COMPARISON")
    print("-" * 40)
    
    for depth in [1, 2, 3, 5, 10, None]:
        tree = DecisionTreeClassifier(max_depth=depth, random_state=random_state)
        tree.fit(X_train, y_train)
        acc = accuracy_score(y_test, tree.predict(X_test))
        depth_str = str(depth) if depth else "None"
        print(f"max_depth={depth_str:<5}: acc={acc:.4f}, leaves={tree.get_n_leaves()}")
    
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
    parser = argparse.ArgumentParser(description="Train Decision Tree")
    parser.add_argument("--max-depth", type=int, default=None)
    parser.add_argument("--criterion", type=str, default="gini", choices=["gini", "entropy"])
    
    args = parser.parse_args()
    train_model(max_depth=args.max_depth, criterion=args.criterion)


if __name__ == "__main__":
    main()
