#!/usr/bin/env python3
"""
K-Means Clustering Training Script

Usage:
    python train.py
    python train.py --k 4
"""

import argparse
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from sklearn.preprocessing import StandardScaler

SCRIPT_DIR = Path(__file__).parent
DATA_DIR = SCRIPT_DIR.parent / "data"
MODEL_DIR = SCRIPT_DIR / "model"


def train_model(
    k: int = 3,
    random_state: int = 42,
) -> dict:
    """Train K-Means clustering model."""
    print(f"\n{'='*60}")
    print(f"Training K-MEANS CLUSTERING (k={k})")
    print(f"{'='*60}")
    
    # Load customer data
    df = pd.read_csv(DATA_DIR / "customers.csv")
    features = ["recency", "frequency", "monetary", "age"]
    X = df[features]
    
    print(f"\nDataset: {len(X)} samples, {len(features)} features")
    print(f"Features: {features}")
    
    # Scale features
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    # Train model
    model = KMeans(n_clusters=k, init="k-means++", n_init=10, random_state=random_state)
    model.fit(X_scaled)
    
    # Metrics
    inertia = model.inertia_
    silhouette = silhouette_score(X_scaled, model.labels_)
    
    print("\n" + "-" * 40)
    print("RESULTS")
    print("-" * 40)
    print(f"Inertia:         {inertia:.2f}")
    print(f"Silhouette Score: {silhouette:.4f}")
    
    # Cluster sizes
    print("\nCluster Sizes:")
    unique, counts = np.unique(model.labels_, return_counts=True)
    for cluster, count in zip(unique, counts):
        print(f"  Cluster {cluster}: {count} samples ({count/len(X)*100:.1f}%)")
    
    # Cluster centers (original scale)
    centers_original = scaler.inverse_transform(model.cluster_centers_)
    print("\nCluster Centers (original scale):")
    print(f"{'Cluster':<8}", end="")
    for feat in features:
        print(f"{feat:>12}", end="")
    print()
    print("-" * (8 + 12 * len(features)))
    
    for i, center in enumerate(centers_original):
        print(f"{i:<8}", end="")
        for val in center:
            print(f"{val:>12.2f}", end="")
        print()
    
    # Elbow Method
    print("\n" + "-" * 40)
    print("ELBOW METHOD (k vs Inertia)")
    print("-" * 40)
    
    inertias = []
    silhouettes = []
    k_range = range(2, 10)
    
    for test_k in k_range:
        km = KMeans(n_clusters=test_k, init="k-means++", n_init=10, random_state=random_state)
        km.fit(X_scaled)
        inertias.append(km.inertia_)
        silhouettes.append(silhouette_score(X_scaled, km.labels_))
    
    for test_k, inert, sil in zip(k_range, inertias, silhouettes):
        bar = "█" * int(inert / max(inertias) * 20)
        print(f"k={test_k}: inertia={inert:>8.0f} silhouette={sil:.4f} {bar}")
    
    # Save
    MODEL_DIR.mkdir(exist_ok=True)
    joblib.dump(model, MODEL_DIR / "model.joblib")
    joblib.dump(scaler, MODEL_DIR / "scaler.joblib")
    joblib.dump(features, MODEL_DIR / "features.joblib")
    
    print(f"\nModel saved to: {MODEL_DIR / 'model.joblib'}")
    
    return {"model": model, "inertia": inertia, "silhouette": silhouette}


def main():
    parser = argparse.ArgumentParser(description="Train K-Means")
    parser.add_argument("--k", type=int, default=3, help="Number of clusters")
    
    args = parser.parse_args()
    train_model(k=args.k)


if __name__ == "__main__":
    main()
