#!/usr/bin/env python3
"""
Logistic Regression Training Script

Train logistic regression for binary classification on churn data.

Usage:
    python train.py
    python train.py --threshold 0.3
"""

import argparse
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
)
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler

# Paths
SCRIPT_DIR = Path(__file__).parent
DATA_DIR = SCRIPT_DIR.parent / "data"
MODEL_DIR = SCRIPT_DIR / "model"


def load_and_preprocess_data() -> tuple[pd.DataFrame, pd.Series, list, list]:
    """Load and preprocess churn data."""
    df = pd.read_csv(DATA_DIR / "churn.csv")
    
    # Separate features and target
    X = df.drop("churn", axis=1)
    y = df["churn"]
    
    # Identify categorical columns
    cat_cols = X.select_dtypes(include=["object"]).columns.tolist()
    num_cols = X.select_dtypes(include=["number"]).columns.tolist()
    
    # Encode categorical columns
    encoders = {}
    for col in cat_cols:
        le = LabelEncoder()
        X[col] = le.fit_transform(X[col])
        encoders[col] = le
    
    return X, y, num_cols, cat_cols, encoders


def train_model(
    threshold: float = 0.5,
    test_size: float = 0.2,
    random_state: int = 42,
) -> dict:
    """
    Train logistic regression model.
    
    Args:
        threshold: Decision threshold for classification
        test_size: Fraction of data for testing
        random_state: Random seed
    
    Returns:
        Dictionary with model and metrics
    """
    print(f"\n{'='*60}")
    print("Training LOGISTIC REGRESSION")
    print(f"{'='*60}")
    
    # Load data
    X, y, num_cols, cat_cols, encoders = load_and_preprocess_data()
    print(f"\nDataset: {len(X)} samples")
    print(f"Features: {list(X.columns)}")
    print(f"Class distribution: {dict(y.value_counts())}")
    
    # Train/test split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state, stratify=y
    )
    print(f"Train: {len(X_train)}, Test: {len(X_test)}")
    
    # Scale numerical features
    scaler = StandardScaler()
    X_train_scaled = X_train.copy()
    X_test_scaled = X_test.copy()
    X_train_scaled[num_cols] = scaler.fit_transform(X_train[num_cols])
    X_test_scaled[num_cols] = scaler.transform(X_test[num_cols])
    
    # Train model
    print(f"\nTraining with threshold={threshold}...")
    model = LogisticRegression(
        class_weight="balanced",
        max_iter=1000,
        random_state=random_state,
    )
    model.fit(X_train_scaled, y_train)
    
    # Predictions
    y_proba = model.predict_proba(X_test_scaled)[:, 1]
    y_pred = (y_proba >= threshold).astype(int)
    
    # Metrics
    print("\n" + "-" * 40)
    print("RESULTS")
    print("-" * 40)
    
    metrics = {
        "accuracy": accuracy_score(y_test, y_pred),
        "precision": precision_score(y_test, y_pred),
        "recall": recall_score(y_test, y_pred),
        "f1": f1_score(y_test, y_pred),
        "roc_auc": roc_auc_score(y_test, y_proba),
    }
    
    print(f"\nThreshold: {threshold}")
    for name, value in metrics.items():
        print(f"{name.upper():<12}: {value:.4f}")
    
    # Confusion Matrix
    print("\nConfusion Matrix:")
    cm = confusion_matrix(y_test, y_pred)
    print(f"  TN={cm[0,0]:4d}  FP={cm[0,1]:4d}")
    print(f"  FN={cm[1,0]:4d}  TP={cm[1,1]:4d}")
    
    # Classification Report
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred, target_names=["Stayed", "Churned"]))
    
    # Feature importance (coefficients)
    print("-" * 40)
    print("FEATURE COEFFICIENTS")
    print("-" * 40)
    coef_df = pd.DataFrame({
        "feature": X.columns,
        "coefficient": model.coef_[0],
        "abs_coef": np.abs(model.coef_[0]),
    }).sort_values("abs_coef", ascending=False)
    
    for _, row in coef_df.iterrows():
        print(f"{row['feature']:<20} {row['coefficient']:>8.4f}")
    
    # Save model
    MODEL_DIR.mkdir(exist_ok=True)
    joblib.dump(model, MODEL_DIR / "model.joblib")
    joblib.dump(scaler, MODEL_DIR / "scaler.joblib")
    joblib.dump(encoders, MODEL_DIR / "encoders.joblib")
    joblib.dump(list(X.columns), MODEL_DIR / "features.joblib")
    joblib.dump(num_cols, MODEL_DIR / "num_cols.joblib")
    joblib.dump(threshold, MODEL_DIR / "threshold.joblib")
    
    print(f"\nModel saved to: {MODEL_DIR / 'model.joblib'}")
    
    return {"model": model, "metrics": metrics}


def main():
    parser = argparse.ArgumentParser(description="Train Logistic Regression")
    parser.add_argument(
        "--threshold",
        type=float,
        default=0.5,
        help="Decision threshold (default: 0.5)",
    )
    parser.add_argument(
        "--test-size",
        type=float,
        default=0.2,
        help="Test set fraction",
    )
    
    args = parser.parse_args()
    train_model(threshold=args.threshold, test_size=args.test_size)


if __name__ == "__main__":
    main()
