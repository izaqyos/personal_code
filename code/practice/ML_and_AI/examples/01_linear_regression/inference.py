#!/usr/bin/env python3
"""
Linear Regression Inference Script

Load trained model and make predictions.

Usage:
    python inference.py
    python inference.py --sqft 2000 --bedrooms 3 --bathrooms 2 --age 10 --garage 2
"""

import argparse
from pathlib import Path

import joblib
import numpy as np
import pandas as pd

# Paths
SCRIPT_DIR = Path(__file__).parent
MODEL_DIR = SCRIPT_DIR / "model"
DATA_DIR = SCRIPT_DIR.parent / "data"


def load_model():
    """Load trained model and scaler."""
    model_path = MODEL_DIR / "model.joblib"
    scaler_path = MODEL_DIR / "scaler.joblib"
    features_path = MODEL_DIR / "features.joblib"
    
    if not model_path.exists():
        raise FileNotFoundError(
            f"Model not found at {model_path}. Run train.py first."
        )
    
    model = joblib.load(model_path)
    scaler = joblib.load(scaler_path)
    features = joblib.load(features_path)
    
    return model, scaler, features


def predict_single(
    sqft: int,
    bedrooms: int,
    bathrooms: int,
    age: int,
    garage: int,
) -> float:
    """
    Predict house price for a single sample.
    
    Args:
        sqft: Square footage
        bedrooms: Number of bedrooms
        bathrooms: Number of bathrooms
        age: House age in years
        garage: Garage capacity
    
    Returns:
        Predicted price
    """
    model, scaler, features = load_model()
    
    # Create feature array in correct order
    X = pd.DataFrame([[sqft, bedrooms, bathrooms, age, garage]], columns=features)
    X_scaled = scaler.transform(X)
    
    prediction = model.predict(X_scaled)[0]
    return prediction


def predict_batch(data_path: str | Path) -> pd.DataFrame:
    """
    Predict prices for a batch of houses.
    
    Args:
        data_path: Path to CSV with housing features
    
    Returns:
        DataFrame with predictions
    """
    model, scaler, features = load_model()
    
    df = pd.read_csv(data_path)
    X = df[features]
    X_scaled = scaler.transform(X)
    
    predictions = model.predict(X_scaled)
    df["predicted_price"] = predictions
    
    return df


def demo_predictions():
    """Demonstrate predictions with sample houses."""
    model, scaler, features = load_model()
    
    print("\n" + "=" * 60)
    print("INFERENCE DEMO")
    print("=" * 60)
    
    # Sample houses
    samples = [
        {"sqft": 1500, "bedrooms": 2, "bathrooms": 1, "age": 20, "garage": 1},
        {"sqft": 2500, "bedrooms": 4, "bathrooms": 2, "age": 5, "garage": 2},
        {"sqft": 3500, "bedrooms": 5, "bathrooms": 3, "age": 0, "garage": 2},
        {"sqft": 1000, "bedrooms": 1, "bathrooms": 1, "age": 40, "garage": 0},
    ]
    
    print("\nSample Predictions:")
    print("-" * 60)
    print(f"{'SqFt':>6} {'Bed':>4} {'Bath':>5} {'Age':>4} {'Gar':>4} {'Predicted Price':>15}")
    print("-" * 60)
    
    for sample in samples:
        X = pd.DataFrame([sample], columns=features)
        X_scaled = scaler.transform(X)
        pred = model.predict(X_scaled)[0]
        
        print(
            f"{sample['sqft']:>6} "
            f"{sample['bedrooms']:>4} "
            f"{sample['bathrooms']:>5} "
            f"{sample['age']:>4} "
            f"{sample['garage']:>4} "
            f"${pred:>14,.0f}"
        )
    
    # Batch prediction on test data
    print("\n" + "-" * 60)
    print("Batch Prediction (first 5 from housing.csv)")
    print("-" * 60)
    
    df = pd.read_csv(DATA_DIR / "housing.csv").head()
    X = df[features]
    X_scaled = scaler.transform(X)
    predictions = model.predict(X_scaled)
    
    df["predicted"] = predictions
    df["error"] = df["price"] - df["predicted"]
    
    print(df[["sqft", "bedrooms", "price", "predicted", "error"]].to_string(index=False))


def main():
    parser = argparse.ArgumentParser(description="Linear Regression Inference")
    parser.add_argument("--sqft", type=int, help="Square footage")
    parser.add_argument("--bedrooms", type=int, help="Number of bedrooms")
    parser.add_argument("--bathrooms", type=int, help="Number of bathrooms")
    parser.add_argument("--age", type=int, help="House age in years")
    parser.add_argument("--garage", type=int, help="Garage capacity")
    parser.add_argument("--data", type=str, help="Path to CSV for batch prediction")
    
    args = parser.parse_args()
    
    # Check if custom input provided
    if all([args.sqft, args.bedrooms, args.bathrooms, args.age is not None, args.garage is not None]):
        prediction = predict_single(
            args.sqft, args.bedrooms, args.bathrooms, args.age, args.garage
        )
        print(f"\nPredicted Price: ${prediction:,.0f}")
    
    elif args.data:
        results = predict_batch(args.data)
        print(results)
    
    else:
        # Run demo
        demo_predictions()


if __name__ == "__main__":
    main()
