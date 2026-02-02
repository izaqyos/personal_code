#!/usr/bin/env python3
"""
PCA Training Script

Usage:
    python train.py
    python train.py --n-components 2
"""

import argparse
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

SCRIPT_DIR = Path(__file__).parent
DATA_DIR = SCRIPT_DIR.parent / "data"
MODEL_DIR = SCRIPT_DIR / "model"


def train_model(
    n_components: int | None = None,
) -> dict:
    """Train PCA model."""
    print(f"\n{'='*60}")
    print("Training PCA")
    print(f"{'='*60}")
    
    # Load iris data (4 features)
    df = pd.read_csv(DATA_DIR / "iris.csv")
    features = ["sepal_length", "sepal_width", "petal_length", "petal_width"]
    X = df[features]
    y = df["species"]
    
    print(f"\nDataset: {len(X)} samples, {len(features)} features")
    print(f"Original Features: {features}")
    
    # Scale
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    # Full PCA to analyze variance
    pca_full = PCA()
    pca_full.fit(X_scaled)
    
    print("\n" + "-" * 40)
    print("EXPLAINED VARIANCE ANALYSIS")
    print("-" * 40)
    
    cumulative = np.cumsum(pca_full.explained_variance_ratio_)
    
    print(f"{'PC':<5} {'Variance %':>12} {'Cumulative %':>15}")
    print("-" * 35)
    
    for i, (var, cum) in enumerate(zip(pca_full.explained_variance_ratio_, cumulative)):
        bar = "█" * int(var * 40)
        print(f"PC{i+1:<3} {var*100:>11.2f}% {cum*100:>14.2f}%  {bar}")
    
    # Train final model
    n_comp = n_components or len(features)
    pca = PCA(n_components=n_comp)
    X_transformed = pca.fit_transform(X_scaled)
    
    print(f"\n" + "-" * 40)
    print(f"FINAL MODEL (n_components={n_comp})")
    print("-" * 40)
    print(f"Variance retained: {sum(pca.explained_variance_ratio_)*100:.2f}%")
    print(f"Original dims: {X_scaled.shape[1]} -> Reduced dims: {X_transformed.shape[1]}")
    
    # Principal component loadings
    print("\nComponent Loadings (feature contributions):")
    loadings = pd.DataFrame(
        pca.components_.T,
        columns=[f"PC{i+1}" for i in range(n_comp)],
        index=features,
    )
    print(loadings.round(3).to_string())
    
    # Show transformed data sample
    print("\nTransformed Data (first 5 samples):")
    transformed_df = pd.DataFrame(
        X_transformed[:5],
        columns=[f"PC{i+1}" for i in range(n_comp)],
    )
    transformed_df["species"] = y[:5].values
    print(transformed_df.round(3).to_string(index=False))
    
    # Save
    MODEL_DIR.mkdir(exist_ok=True)
    joblib.dump(pca, MODEL_DIR / "model.joblib")
    joblib.dump(scaler, MODEL_DIR / "scaler.joblib")
    joblib.dump(features, MODEL_DIR / "features.joblib")
    
    print(f"\nModel saved to: {MODEL_DIR / 'model.joblib'}")
    
    return {"model": pca, "variance_explained": sum(pca.explained_variance_ratio_)}


def main():
    parser = argparse.ArgumentParser(description="Train PCA")
    parser.add_argument("--n-components", type=int, default=None,
                       help="Number of components (default: all)")
    
    args = parser.parse_args()
    train_model(n_components=args.n_components)


if __name__ == "__main__":
    main()
