#!/usr/bin/env python3
"""
Linear Regression Training Script

Train linear regression models (Linear, Ridge, Lasso) on housing data.

Usage:
    python train.py
    python train.py --model ridge --alpha 1.0
    python train.py --model lasso --alpha 0.1
"""

import argparse
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from sklearn.linear_model import ElasticNet, Lasso, LinearRegression, Ridge
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

# Paths
SCRIPT_DIR = Path(__file__).parent
DATA_DIR = SCRIPT_DIR.parent / "data"
MODEL_DIR = SCRIPT_DIR / "model"


def load_data() -> tuple[pd.DataFrame, pd.DataFrame]:
    """Load housing data from shared data directory."""
    df = pd.read_csv(DATA_DIR / "housing.csv")
    
    # Features and target
    X = df.drop("price", axis=1)
    y = df["price"]
    
    return X, y


def train_model(
    model_type: str = "linear",
    alpha: float = 1.0,
    l1_ratio: float = 0.5,
    test_size: float = 0.2,
    random_state: int = 42,
) -> dict:
    """
    Train a linear regression model.
    
    Args:
        model_type: 'linear', 'ridge', 'lasso', or 'elasticnet'
        alpha: Regularization strength (for ridge/lasso/elasticnet)
        l1_ratio: L1 ratio for elasticnet (0=ridge, 1=lasso)
        test_size: Fraction of data for testing
        random_state: Random seed for reproducibility
    
    Returns:
        Dictionary with model, metrics, and artifacts
    """
    print(f"\n{'='*60}")
    print(f"Training {model_type.upper()} Regression")
    print(f"{'='*60}")
    
    # Load data
    X, y = load_data()
    print(f"\nDataset: {len(X)} samples, {X.shape[1]} features")
    print(f"Features: {list(X.columns)}")
    
    # Train/test split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state
    )
    print(f"Train: {len(X_train)}, Test: {len(X_test)}")
    
    # Scale features (important for regularized models)
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    # Create model
    if model_type == "linear":
        model = LinearRegression()
    elif model_type == "ridge":
        model = Ridge(alpha=alpha)
        print(f"Alpha (L2 regularization): {alpha}")
    elif model_type == "lasso":
        model = Lasso(alpha=alpha)
        print(f"Alpha (L1 regularization): {alpha}")
    elif model_type == "elasticnet":
        model = ElasticNet(alpha=alpha, l1_ratio=l1_ratio)
        print(f"Alpha: {alpha}, L1 ratio: {l1_ratio}")
    else:
        raise ValueError(f"Unknown model type: {model_type}")
    
    # Train
    print("\nTraining...")
    model.fit(X_train_scaled, y_train)
    
    # Predictions
    y_train_pred = model.predict(X_train_scaled)
    y_test_pred = model.predict(X_test_scaled)
    
    # Metrics
    metrics = {
        "train": {
            "mse": mean_squared_error(y_train, y_train_pred),
            "rmse": np.sqrt(mean_squared_error(y_train, y_train_pred)),
            "mae": mean_absolute_error(y_train, y_train_pred),
            "r2": r2_score(y_train, y_train_pred),
        },
        "test": {
            "mse": mean_squared_error(y_test, y_test_pred),
            "rmse": np.sqrt(mean_squared_error(y_test, y_test_pred)),
            "mae": mean_absolute_error(y_test, y_test_pred),
            "r2": r2_score(y_test, y_test_pred),
        },
    }
    
    # Print results
    print("\n" + "-" * 40)
    print("RESULTS")
    print("-" * 40)
    print(f"\n{'Metric':<12} {'Train':>12} {'Test':>12}")
    print("-" * 40)
    for metric in ["mse", "rmse", "mae", "r2"]:
        train_val = metrics["train"][metric]
        test_val = metrics["test"][metric]
        print(f"{metric.upper():<12} {train_val:>12.2f} {test_val:>12.2f}")
    
    # Feature importance (coefficients)
    print("\n" + "-" * 40)
    print("FEATURE COEFFICIENTS")
    print("-" * 40)
    for feature, coef in zip(X.columns, model.coef_):
        print(f"{feature:<15} {coef:>12.2f}")
    print(f"{'Intercept':<15} {model.intercept_:>12.2f}")
    
    # Save model and scaler
    MODEL_DIR.mkdir(exist_ok=True)
    model_path = MODEL_DIR / "model.joblib"
    scaler_path = MODEL_DIR / "scaler.joblib"
    
    joblib.dump(model, model_path)
    joblib.dump(scaler, scaler_path)
    
    # Save feature names for inference
    joblib.dump(list(X.columns), MODEL_DIR / "features.joblib")
    
    print(f"\nModel saved to: {model_path}")
    print(f"Scaler saved to: {scaler_path}")
    
    return {
        "model": model,
        "scaler": scaler,
        "metrics": metrics,
        "features": list(X.columns),
    }


def main():
    parser = argparse.ArgumentParser(description="Train Linear Regression")
    parser.add_argument(
        "--model",
        type=str,
        default="linear",
        choices=["linear", "ridge", "lasso", "elasticnet"],
        help="Model type",
    )
    parser.add_argument(
        "--alpha",
        type=float,
        default=1.0,
        help="Regularization strength",
    )
    parser.add_argument(
        "--l1-ratio",
        type=float,
        default=0.5,
        help="L1 ratio for ElasticNet (0=ridge, 1=lasso)",
    )
    parser.add_argument(
        "--test-size",
        type=float,
        default=0.2,
        help="Test set fraction",
    )
    
    args = parser.parse_args()
    
    train_model(
        model_type=args.model,
        alpha=args.alpha,
        l1_ratio=args.l1_ratio,
        test_size=args.test_size,
    )


if __name__ == "__main__":
    main()
