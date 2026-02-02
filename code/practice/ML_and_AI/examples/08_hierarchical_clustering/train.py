#!/usr/bin/env python3
"""
Hierarchical Clustering Training Script

Usage:
    python train.py
    python train.py --n-clusters 4 --linkage average
"""

import argparse
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from scipy.cluster.hierarchy import dendrogram, linkage
from sklearn.cluster import AgglomerativeClustering
from sklearn.metrics import silhouette_score
from sklearn.preprocessing import StandardScaler

SCRIPT_DIR = Path(__file__).parent
DATA_DIR = SCRIPT_DIR.parent / "data"
MODEL_DIR = SCRIPT_DIR / "model"


def train_model(
    n_clusters: int = 3,
    linkage_method: str = "ward",
) -> dict:
    """Train Hierarchical Clustering model."""
    print(f"\n{'='*60}")
    print(f"Training HIERARCHICAL CLUSTERING")
    print(f"{'='*60}")
    
    # Load data
    df = pd.read_csv(DATA_DIR / "customers.csv")
    features = ["recency", "frequency", "monetary", "age"]
    X = df[features]
    
    print(f"\nDataset: {len(X)} samples")
    print(f"Linkage: {linkage_method}")
    print(f"N Clusters: {n_clusters}")
    
    # Scale
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    # Compute linkage matrix for dendrogram
    Z = linkage(X_scaled, method=linkage_method)
    
    # Train model
    model = AgglomerativeClustering(
        n_clusters=n_clusters,
        linkage=linkage_method,
    )
    labels = model.fit_predict(X_scaled)
    
    # Metrics
    silhouette = silhouette_score(X_scaled, labels)
    
    print("\n" + "-" * 40)
    print("RESULTS")
    print("-" * 40)
    print(f"Silhouette Score: {silhouette:.4f}")
    
    # Cluster sizes
    print("\nCluster Sizes:")
    unique, counts = np.unique(labels, return_counts=True)
    for cluster, count in zip(unique, counts):
        print(f"  Cluster {cluster}: {count} samples ({count/len(X)*100:.1f}%)")
    
    # Cluster means
    df["cluster"] = labels
    print("\nCluster Means:")
    print(df.groupby("cluster")[features].mean().round(2).to_string())
    
    # Compare linkage methods
    print("\n" + "-" * 40)
    print("LINKAGE METHOD COMPARISON")
    print("-" * 40)
    
    for method in ["ward", "complete", "average", "single"]:
        agg = AgglomerativeClustering(n_clusters=n_clusters, linkage=method)
        lbls = agg.fit_predict(X_scaled)
        sil = silhouette_score(X_scaled, lbls)
        print(f"{method:<10}: silhouette={sil:.4f}")
    
    # N_clusters comparison
    print("\n" + "-" * 40)
    print("N_CLUSTERS COMPARISON")
    print("-" * 40)
    
    for n in range(2, 7):
        agg = AgglomerativeClustering(n_clusters=n, linkage=linkage_method)
        lbls = agg.fit_predict(X_scaled)
        sil = silhouette_score(X_scaled, lbls)
        print(f"n_clusters={n}: silhouette={sil:.4f}")
    
    # Save
    MODEL_DIR.mkdir(exist_ok=True)
    joblib.dump(model, MODEL_DIR / "model.joblib")
    joblib.dump(scaler, MODEL_DIR / "scaler.joblib")
    joblib.dump(features, MODEL_DIR / "features.joblib")
    joblib.dump(Z, MODEL_DIR / "linkage_matrix.joblib")
    joblib.dump(labels, MODEL_DIR / "labels.joblib")
    
    print(f"\nModel saved to: {MODEL_DIR / 'model.joblib'}")
    
    return {"model": model, "silhouette": silhouette}


def main():
    parser = argparse.ArgumentParser(description="Train Hierarchical Clustering")
    parser.add_argument("--n-clusters", type=int, default=3)
    parser.add_argument("--linkage", type=str, default="ward",
                       choices=["ward", "complete", "average", "single"])
    
    args = parser.parse_args()
    train_model(n_clusters=args.n_clusters, linkage_method=args.linkage)


if __name__ == "__main__":
    main()
