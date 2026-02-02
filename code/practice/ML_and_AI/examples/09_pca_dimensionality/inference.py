#!/usr/bin/env python3
"""PCA Inference Script"""

from pathlib import Path
import joblib
import numpy as np
import pandas as pd

SCRIPT_DIR = Path(__file__).parent
MODEL_DIR = SCRIPT_DIR / "model"
DATA_DIR = SCRIPT_DIR.parent / "data"


def load_model():
    return (
        joblib.load(MODEL_DIR / "model.joblib"),
        joblib.load(MODEL_DIR / "scaler.joblib"),
        joblib.load(MODEL_DIR / "features.joblib"),
    )


def demo_predictions():
    print("\n" + "=" * 60)
    print("PCA INFERENCE DEMO")
    print("=" * 60)
    
    pca, scaler, features = load_model()
    n_comp = pca.n_components_
    
    print(f"Components: {n_comp}")
    print(f"Variance Explained: {sum(pca.explained_variance_ratio_)*100:.2f}%")
    
    # Load and transform data
    df = pd.read_csv(DATA_DIR / "iris.csv")
    X = df[features]
    X_scaled = scaler.transform(X)
    X_transformed = pca.transform(X_scaled)
    
    # Show transformation
    print("\nOriginal -> Transformed (first 5):")
    print("-" * 60)
    
    for i in range(5):
        orig = X.iloc[i].values.round(2)
        trans = X_transformed[i].round(3)
        print(f"  {list(orig)} -> {list(trans)}")
    
    # Reconstruction
    print("\n" + "-" * 60)
    print("RECONSTRUCTION (transform -> inverse_transform)")
    print("-" * 60)
    
    X_reconstructed = pca.inverse_transform(X_transformed)
    X_reconstructed = scaler.inverse_transform(X_reconstructed)
    
    reconstruction_error = np.mean((X.values - X_reconstructed) ** 2)
    print(f"Mean Squared Reconstruction Error: {reconstruction_error:.6f}")
    
    print("\nOriginal vs Reconstructed (sample):")
    sample_idx = 0
    print(f"  Original:      {list(X.iloc[sample_idx].values.round(3))}")
    print(f"  Reconstructed: {list(X_reconstructed[sample_idx].round(3))}")
    
    # New sample
    print("\n" + "-" * 60)
    print("Transform New Sample")
    print("-" * 60)
    
    new_sample = [[5.5, 3.0, 4.0, 1.5]]
    scaled = scaler.transform(new_sample)
    transformed = pca.transform(scaled)
    
    print(f"Input:       {new_sample[0]}")
    print(f"Transformed: {list(transformed[0].round(3))}")


if __name__ == "__main__":
    demo_predictions()
