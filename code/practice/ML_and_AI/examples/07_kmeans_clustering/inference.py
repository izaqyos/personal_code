#!/usr/bin/env python3
"""K-Means Inference Script"""

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
    print("K-MEANS INFERENCE DEMO")
    print("=" * 60)
    
    model, scaler, features = load_model()
    print(f"K = {model.n_clusters}")
    
    # Cluster centers
    centers = scaler.inverse_transform(model.cluster_centers_)
    print("\nCluster Centers:")
    for i, center in enumerate(centers):
        print(f"  Cluster {i}: {dict(zip(features, center.round(1)))}")
    
    # New customer samples
    samples = [
        {"recency": 5, "frequency": 20, "monetary": 500, "age": 30},    # Frequent buyer
        {"recency": 200, "frequency": 1, "monetary": 50, "age": 65},    # Inactive
        {"recency": 30, "frequency": 5, "monetary": 200, "age": 45},    # Average
    ]
    
    print("\nNew Customer Predictions:")
    print("-" * 60)
    
    for sample in samples:
        X = pd.DataFrame([sample])[features]
        X_scaled = scaler.transform(X)
        cluster = model.predict(X_scaled)[0]
        distance = np.linalg.norm(X_scaled - model.cluster_centers_[cluster])
        
        print(f"Customer: {sample}")
        print(f"  -> Cluster: {cluster}, Distance to center: {distance:.2f}")
        print()
    
    # Batch from file
    df = pd.read_csv(DATA_DIR / "customers.csv").head(10)
    X = df[features]
    X_scaled = scaler.transform(X)
    df["cluster"] = model.predict(X_scaled)
    
    print("Batch Predictions:")
    print(df[["customer_id", "recency", "frequency", "monetary", "cluster"]].to_string(index=False))


if __name__ == "__main__":
    demo_predictions()
