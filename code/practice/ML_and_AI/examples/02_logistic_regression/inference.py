#!/usr/bin/env python3
"""
Logistic Regression Inference Script

Load trained model and make predictions.

Usage:
    python inference.py
"""

from pathlib import Path

import joblib
import numpy as np
import pandas as pd

# Paths
SCRIPT_DIR = Path(__file__).parent
MODEL_DIR = SCRIPT_DIR / "model"
DATA_DIR = SCRIPT_DIR.parent / "data"


def load_model():
    """Load trained model and preprocessing artifacts."""
    model = joblib.load(MODEL_DIR / "model.joblib")
    scaler = joblib.load(MODEL_DIR / "scaler.joblib")
    encoders = joblib.load(MODEL_DIR / "encoders.joblib")
    features = joblib.load(MODEL_DIR / "features.joblib")
    num_cols = joblib.load(MODEL_DIR / "num_cols.joblib")
    threshold = joblib.load(MODEL_DIR / "threshold.joblib")
    
    return model, scaler, encoders, features, num_cols, threshold


def preprocess_input(df: pd.DataFrame, encoders: dict, scaler, features: list, num_cols: list) -> pd.DataFrame:
    """Preprocess input data for prediction."""
    df = df.copy()
    
    # Encode categorical columns
    for col, encoder in encoders.items():
        if col in df.columns:
            df[col] = encoder.transform(df[col])
    
    # Scale numerical columns
    df[num_cols] = scaler.transform(df[num_cols])
    
    return df[features]


def predict(data: pd.DataFrame) -> tuple[np.ndarray, np.ndarray]:
    """Make predictions on input data."""
    model, scaler, encoders, features, num_cols, threshold = load_model()
    
    X = preprocess_input(data, encoders, scaler, features, num_cols)
    
    proba = model.predict_proba(X)[:, 1]
    pred = (proba >= threshold).astype(int)
    
    return pred, proba


def demo_predictions():
    """Demonstrate predictions with sample customers."""
    print("\n" + "=" * 60)
    print("INFERENCE DEMO")
    print("=" * 60)
    
    model, scaler, encoders, features, num_cols, threshold = load_model()
    print(f"Using threshold: {threshold}")
    
    # Sample customers
    samples = pd.DataFrame([
        {"tenure": 1, "monthly_charges": 80, "total_charges": 80, "contract": "month-to-month", "internet_service": "fiber"},
        {"tenure": 48, "monthly_charges": 50, "total_charges": 2400, "contract": "two_year", "internet_service": "dsl"},
        {"tenure": 12, "monthly_charges": 90, "total_charges": 1080, "contract": "one_year", "internet_service": "fiber"},
        {"tenure": 2, "monthly_charges": 95, "total_charges": 190, "contract": "month-to-month", "internet_service": "fiber"},
    ])
    
    # Preprocess and predict
    X = preprocess_input(samples, encoders, scaler, features, num_cols)
    proba = model.predict_proba(X)[:, 1]
    pred = (proba >= threshold).astype(int)
    
    print("\nSample Predictions:")
    print("-" * 70)
    print(f"{'Tenure':>7} {'Monthly':>8} {'Contract':<15} {'Prob':>7} {'Prediction':<10}")
    print("-" * 70)
    
    for i, row in samples.iterrows():
        status = "CHURN" if pred[i] == 1 else "STAY"
        print(
            f"{row['tenure']:>7} "
            f"${row['monthly_charges']:>7.0f} "
            f"{row['contract']:<15} "
            f"{proba[i]:>7.2%} "
            f"{status:<10}"
        )
    
    # Batch prediction from file
    print("\n" + "-" * 70)
    print("Batch Prediction (first 10 from churn.csv)")
    print("-" * 70)
    
    df = pd.read_csv(DATA_DIR / "churn.csv").head(10)
    pred, proba = predict(df.drop("churn", axis=1))
    
    df["predicted_proba"] = proba
    df["predicted"] = pred
    df["correct"] = (df["churn"] == df["predicted"]).map({True: "✓", False: "✗"})
    
    print(df[["tenure", "monthly_charges", "contract", "churn", "predicted_proba", "predicted", "correct"]].to_string(index=False))
    
    accuracy = (df["churn"] == df["predicted"]).mean()
    print(f"\nAccuracy on sample: {accuracy:.1%}")


def main():
    demo_predictions()


if __name__ == "__main__":
    main()
