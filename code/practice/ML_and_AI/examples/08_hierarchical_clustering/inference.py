#!/usr/bin/env python3
"""Hierarchical Clustering Inference Script"""

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
        joblib.load(MODEL_DIR / "labels.joblib"),
    )


def demo_predictions():
    print("\n" + "=" * 60)
    print("HIERARCHICAL CLUSTERING INFERENCE DEMO")
    print("=" * 60)
    
    model, scaler, features, labels = load_model()
    print(f"Linkage: {model.linkage}, N Clusters: {model.n_clusters}")
    
    # Load original data with labels
    df = pd.read_csv(DATA_DIR / "customers.csv")
    df["cluster"] = labels
    
    # Cluster profiles
    print("\nCluster Profiles (means):")
    print(df.groupby("cluster")[features].mean().round(2).to_string())
    
    # Sample from each cluster
    print("\n" + "-" * 60)
    print("Sample Customers per Cluster:")
    print("-" * 60)
    
    for cluster in range(model.n_clusters):
        sample = df[df["cluster"] == cluster].head(3)
        print(f"\nCluster {cluster}:")
        print(sample[["customer_id", "recency", "frequency", "monetary", "age"]].to_string(index=False))
    
    # For new data, we need to retrain (hierarchical doesn't have predict)
    print("\n" + "-" * 60)
    print("Note: Hierarchical clustering doesn't support predict() for new data.")
    print("For new points, either retrain or use nearest cluster centroid.")
    print("-" * 60)
    
    # Show centroid approximation
    centroids = df.groupby("cluster")[features].mean()
    print("\nCluster Centroids (for nearest-neighbor assignment):")
    print(centroids.round(2).to_string())


if __name__ == "__main__":
    demo_predictions()
